"""Application meaning checked without participant SDKs or recipe matrices."""

import math

import numpy as np
import pytest

from sdkbench.candidates.applications import (
    Draw,
    FAMILIES,
    TOPOLOGIES,
    WIDTHS,
    _ccx,
    application,
    fixture,
    pauli_rotation,
)
from sdkbench.p0.semantics import propagate

NONCE = "01" * 32  # Public development nonce; never prospective evidence.


def same_operator(actual, expected):
    overlap = np.vdot(actual, expected)
    assert abs(overlap) > 0
    np.testing.assert_allclose(
        actual * overlap / abs(overlap), expected, atol=2e-12, rtol=0
    )


def evolve(hamiltonian, time):
    values, vectors = np.linalg.eigh(hamiltonian)
    return (vectors * np.exp(-1j * time * values)) @ vectors.conj().T


def pauli(word):
    matrices = {
        "I": np.eye(2),
        "X": np.array([[0, 1], [1, 0]]),
        "Y": np.array([[0, -1j], [1j, 0]]),
        "Z": np.diag([1, -1]),
    }
    result = np.array([[1]])
    for letter in word[::-1]:
        result = np.kron(result, matrices[letter])
    return result


@pytest.mark.parametrize("word", [{0: "Y", 2: "X", 3: "Z"}, {1: "Y", 3: "Y"}])
def test_parity_gadget_matches_pauli_exponential(word):
    text = "".join(word.get(q, "I") for q in range(4))
    actual = propagate(4, pauli_rotation(word, 0.37), np.eye(16))
    same_operator(actual, evolve(pauli(text), 0.37 / 2))


def test_qaoa_matches_weighted_maxcut_hamiltonian():
    n = 6
    draw = Draw(NONCE, "qaoa:6")
    order = draw.permutation(n, "interaction-order")
    edges = {tuple(sorted((order[q], order[(q + 1) % n]))) for q in range(n)}
    edges.update(tuple(sorted(order[i : i + 2])) for i in range(0, n, 2))
    basis = np.arange(1 << n)
    costs = sum(
        (0.5 + draw.fraction("weight", i)) * (((basis >> a) ^ (basis >> b)) & 1)
        for i, (a, b) in enumerate(sorted(edges))
    )
    state = np.full(1 << n, 1 / math.sqrt(1 << n), dtype=complex)
    mixer = sum(pauli("I" * q + "X" + "I" * (n - q - 1)) for q in range(n))
    for layer in range(2):
        state *= np.exp(-1j * draw.angle("gamma", layer) * costs)
        state = evolve(mixer, draw.angle("beta", layer)) @ state
    same_operator(propagate(n, application(n, "qaoa", draw)), state)


def test_symmetric_ising_matches_ordered_hamiltonian_factors():
    n = 6
    draw = Draw(NONCE, "ising:6")
    order = draw.permutation(n, "interaction-order")
    transverse = sum(
        (0.5 + draw.fraction("field", q)) * pauli("I" * q + "X" + "I" * (n - q - 1))
        for q in range(n)
    )
    diagonal = np.zeros(1 << n)
    basis = np.arange(1 << n)
    for i, (a, b) in enumerate(zip(order, order[1:])):
        diagonal += (0.5 + draw.fraction("coupling", i)) * (
            1 - 2 * (((basis >> a) ^ (basis >> b)) & 1)
        )
    half = evolve(transverse, 0.1)
    step = half @ np.diag(np.exp(-0.2j * diagonal)) @ half
    actual = propagate(n, application(n, "ising", draw), np.eye(1 << n))
    same_operator(actual, np.linalg.matrix_power(step, 3))


def annihilation(n, orbital):
    result = np.zeros((1 << n, 1 << n), dtype=complex)
    for basis in range(1 << n):
        if (basis >> orbital) & 1:
            sign = (-1) ** ((basis & ((1 << orbital) - 1)).bit_count())
            result[basis ^ (1 << orbital), basis] = sign
    return result


def test_chemistry_hopping_matches_fock_operators_and_particle_number():
    n = 6
    draw = Draw(NONCE, "hopping:6")
    order = draw.permutation(n, "interaction-order")
    expected = np.eye(1 << n, dtype=complex)
    # Initial occupied-orbital preparation remains part of the complete operator.
    for q in range(n // 2):
        expected = pauli("I" * q + "X" + "I" * (n - q - 1)) @ expected
    for layer in range(2):
        for i in range(n // 2):
            p, q = sorted(order[2 * i : 2 * i + 2])
            a, b = annihilation(n, p), annihilation(n, q)
            hamiltonian = a.conj().T @ b + b.conj().T @ a
            expected = (
                evolve(hamiltonian, draw.angle("excitation", layer * n + i)) @ expected
            )
    actual = propagate(n, application(n, "hopping", draw), np.eye(1 << n))
    same_operator(actual, expected)
    state = actual[:, 0]
    assert (
        sum(abs(v) ** 2 for basis, v in enumerate(state) if basis.bit_count() != n // 2)
        < 1e-24
    )


def test_qft_matches_analytic_positive_sign_dft():
    n = 6
    actual = propagate(n, application(n, "qft", Draw(NONCE, "qft:6")), np.eye(1 << n))
    basis = np.arange(1 << n)
    expected = np.exp(2j * math.pi * np.outer(basis, basis) / (1 << n)) / math.sqrt(
        1 << n
    )
    same_operator(actual, expected)


def test_toffoli_matches_all_basis_columns_without_relative_phase():
    expected = np.eye(8, dtype=complex)
    expected[:, [3, 7]] = expected[:, [7, 3]]
    same_operator(propagate(3, _ccx(0, 1, 2), np.eye(8)), expected)


@pytest.mark.parametrize("nonce", [f"{i:064x}" for i in range(6)])
def test_coherent_repetition_restores_logical_data_and_retains_syndrome(nonce):
    n = 6
    draw = Draw(nonce, "repetition:6")
    order = draw.permutation(n, "interaction-order")
    a, b, c, s, t = order[:5]
    error = int(3 * draw.fraction("error", 0))
    syndrome = [(1, 0), (1, 1), (0, 1)][error]
    expected = np.zeros(1 << n, dtype=complex)
    angle = draw.angle("logical-state", 0)
    base = (syndrome[0] << s) | (syndrome[1] << t)
    expected[base] = math.cos(angle / 2)
    expected[base | (1 << a) | (1 << b) | (1 << c)] = math.sin(angle / 2)
    same_operator(propagate(n, application(n, "repetition", draw)), expected)


def test_all_sixty_cases_are_deterministic_bounded_connected_and_target_independent():
    for n in WIDTHS:
        for family in FAMILIES:
            cases = [fixture(n, family, topology, NONCE) for topology in TOPOLOGIES]
            assert all(case["operations"] == cases[0]["operations"] for case in cases)
            for topology, case in zip(TOPOLOGIES, cases):
                assert case == fixture(n, family, topology, NONCE)
                assert 0 < len(case["operations"]) < 1024
                assert {q for op in case["operations"] for q in op["qubits"]} == set(
                    range(n)
                )
                seen = {0}
                while True:
                    expanded = seen | {
                        q
                        for edge in case["target_edges"]
                        if seen.intersection(edge)
                        for q in edge
                    }
                    if expanded == seen:
                        break
                    seen = expanded
                assert len(seen) == n


@pytest.mark.parametrize("nonce", ["", "ab", "Z" * 64, "a" * 65])
def test_nonce_refuses_invalid_values(nonce):
    with pytest.raises(ValueError):
        Draw(nonce, "development")
