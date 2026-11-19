"""Participant-independent numeric compiler workloads; no SDK imports.

These recipes define development instances until a generator revision and all
candidate configurations are frozen before drawing a prospective campaign nonce.
Logical qubit zero is the least significant statevector index bit.
"""

from __future__ import annotations

import hashlib
import math
from typing import Literal, TypedDict

Family = Literal["qaoa", "ising", "hopping", "qft", "repetition"]
Topology = Literal["line", "ring", "grid", "sparse"]
FAMILIES: tuple[Family, ...] = ("qaoa", "ising", "hopping", "qft", "repetition")
TOPOLOGIES: tuple[Topology, ...] = ("line", "ring", "grid", "sparse")
WIDTHS = (6, 8, 12)


class Operation(TypedDict):
    name: str
    qubits: list[int]


class Rotation(Operation):
    angle: float


class ApplicationFixture(TypedDict):
    n_qubits: int
    operations: list[Operation | Rotation]
    target_edges: list[list[int]]
    ancillas_allowed: int
    initial_layout: str
    final_layout: str
    target_basis: str
    probe_preparations: list[list[Operation | Rotation]]
    verification: str


class Draw:
    """Domain-separated SHA-256 draws, independent of Python RNG versions."""

    def __init__(self, nonce: str, label: str) -> None:
        if len(nonce) != 64 or any(c not in "0123456789abcdef" for c in nonce):
            raise ValueError("Nonce must be 32 bytes encoded as lowercase hexadecimal")
        self.prefix = f"sdkbench-applications-v1:{nonce}:{label}"

    def fraction(self, label: str, index: int) -> float:
        digest = hashlib.sha256(
            f"{self.prefix}:{label}:{index}".encode("ascii")
        ).digest()
        return (int.from_bytes(digest[:8], "big") >> 11) / 2**53

    def angle(self, label: str, index: int) -> float:
        return math.pi * (2 * self.fraction(label, index) - 1)

    def permutation(self, n: int, label: str) -> list[int]:
        return sorted(range(n), key=lambda q: (self.fraction(label, q), q))


def gate(name: str, *qubits: int, angle: float | None = None) -> Operation | Rotation:
    if angle is None:
        return {"name": name, "qubits": list(qubits)}
    return {"name": name, "qubits": list(qubits), "angle": angle}


def target_edges(n: int, topology: Topology, draw: Draw) -> list[list[int]]:
    edges = {(q, q + 1) for q in range(n - 1)}
    if topology == "ring":
        edges.add((0, n - 1))
    elif topology == "grid":
        columns = n // 2
        edges = {
            (r * columns + c, r * columns + c + 1)
            for r in range(2)
            for c in range(columns - 1)
        }
        edges.update((c, c + columns) for c in range(columns))
    elif topology == "sparse":
        # A spanning path guarantees connectivity; a matching adds sparse chords.
        order = draw.permutation(n, "target-chords")
        for i in range(0, n, 2):
            a, b = sorted(order[i : i + 2])
            edges.add((a, b))
    elif topology != "line":
        raise ValueError("Unknown target topology")
    return [list(edge) for edge in sorted(edges)]


def pauli_rotation(word: dict[int, str], angle: float) -> list[Operation | Rotation]:
    """Emit exp(-i angle P/2), with an explicit parity ladder and inverse."""
    wires = sorted(word)
    before: list[Operation | Rotation] = []
    after: list[Operation | Rotation] = []
    for q in wires:
        if word[q] == "X":
            before.append(gate("h", q))
            after.insert(0, gate("h", q))
        elif word[q] == "Y":
            before.append(gate("rx", q, angle=math.pi / 2))
            after.insert(0, gate("rx", q, angle=-math.pi / 2))
        elif word[q] != "Z":
            raise ValueError("Pauli words must contain X, Y or Z")
    ladder = [gate("cx", a, b) for a, b in zip(wires, wires[1:])]
    return before + ladder + [gate("rz", wires[-1], angle=angle)] + ladder[::-1] + after


def _ccx(a: int, b: int, target: int) -> list[Operation | Rotation]:
    # Exact Clifford+T Toffoli decomposition, with T represented by RZ up to
    # one circuit-wide phase. Relative/conditional phases are retained.
    return [
        gate("h", target),
        gate("cx", b, target),
        gate("rz", target, angle=-math.pi / 4),
        gate("cx", a, target),
        gate("rz", target, angle=math.pi / 4),
        gate("cx", b, target),
        gate("rz", target, angle=-math.pi / 4),
        gate("cx", a, target),
        gate("rz", b, angle=math.pi / 4),
        gate("rz", target, angle=math.pi / 4),
        gate("h", target),
        gate("cx", a, b),
        gate("rz", a, angle=math.pi / 4),
        gate("rz", b, angle=-math.pi / 4),
        gate("cx", a, b),
    ]


def application(n: int, family: Family, draw: Draw) -> list[Operation | Rotation]:
    """Return a bounded application circuit in the existing W03 vocabulary."""
    if n not in WIDTHS:
        raise ValueError("Application width must be 6, 8 or 12")
    ops: list[Operation | Rotation] = []
    order = draw.permutation(n, "interaction-order")
    if family == "qaoa":
        edges = {tuple(sorted((order[q], order[(q + 1) % n]))) for q in range(n)}
        edges.update(tuple(sorted(order[i : i + 2])) for i in range(0, n, 2))
        ops.extend(gate("h", q) for q in range(n))
        for layer in range(2):
            gamma, beta = draw.angle("gamma", layer), draw.angle("beta", layer)
            for i, (a, b) in enumerate(sorted(edges)):
                weight = 0.5 + draw.fraction("weight", i)
                ops.append(gate("rzz", a, b, angle=-gamma * weight))
            ops.extend(gate("rx", q, angle=2 * beta) for q in range(n))
    elif family == "ising":
        dt = 0.2
        for _ in range(3):
            ops.extend(
                gate("rx", q, angle=(0.5 + draw.fraction("field", q)) * dt)
                for q in range(n)
            )
            ops.extend(
                gate("rzz", a, b, angle=2 * dt * (0.5 + draw.fraction("coupling", i)))
                for i, (a, b) in enumerate(zip(order, order[1:]))
            )
            ops.extend(
                gate("rx", q, angle=(0.5 + draw.fraction("field", q)) * dt)
                for q in range(n)
            )
    elif family == "hopping":
        ops.extend(gate("x", q) for q in range(n // 2))
        for layer in range(2):
            for i in range(n // 2):
                p, q = sorted(order[2 * i : 2 * i + 2])
                theta = draw.angle("excitation", layer * n + i)
                parity = {k: "Z" for k in range(p + 1, q)}
                # Jordan-Wigner a†p aq + a†q ap = (Xp Xq + Yp Yq) Zstring / 2.
                for axis in ("X", "Y"):
                    ops.extend(pauli_rotation({**parity, p: axis, q: axis}, theta))
    elif family == "qft":
        for q in reversed(range(n)):
            ops.append(gate("h", q))
            for control in reversed(range(q)):
                angle = math.pi / 2 ** (q - control)
                ops.extend(
                    [
                        gate("rz", control, angle=angle / 2),
                        gate("rz", q, angle=angle / 2),
                        gate("rzz", control, q, angle=-angle / 2),
                    ]
                )
        for a in range(n // 2):
            b = n - 1 - a
            ops.extend([gate("cx", a, b), gate("cx", b, a), gate("cx", a, b)])
    elif family == "repetition":
        a, b, c, s, t = order[:5]
        ops.extend(
            [
                gate("ry", a, angle=draw.angle("logical-state", 0)),
                gate("cx", a, b),
                gate("cx", a, c),
                gate("x", order[int(3 * draw.fraction("error", 0))]),
                gate("cx", a, s),
                gate("cx", b, s),
                gate("cx", b, t),
                gate("cx", c, t),
            ]
        )
        ops.extend(_ccx(s, t, b))
        ops.extend(
            [
                gate("x", t),
                *_ccx(s, t, a),
                gate("x", t),
                gate("x", s),
                *_ccx(s, t, c),
                gate("x", s),
            ]
        )
        ops.extend(gate("rz", q, angle=draw.angle("spectator", q)) for q in order[5:])
    else:
        raise ValueError("Unknown application family")
    return ops


def fixture(
    n: int, family: Family, topology: Topology, nonce: str
) -> ApplicationFixture:
    if family not in FAMILIES or topology not in TOPOLOGIES:
        raise ValueError("Unknown application family or topology")
    # Same application across targets; topology has its own draw domain.
    draw = Draw(nonce, f"{family}:{n}")
    probes = [
        [
            op
            for q in range(n)
            for op in (
                gate("ry", q, angle=draw.angle(f"probe-y-{p}", q)),
                gate("rz", q, angle=draw.angle(f"probe-z-{p}", q)),
            )
        ]
        for p in range(3)
    ]
    return {
        "n_qubits": n,
        "operations": application(n, family, draw),
        "target_edges": target_edges(n, topology, draw),
        "ancillas_allowed": 0,
        "initial_layout": "identity",
        "final_layout": "permitted only with explicit logical reconstruction",
        "target_basis": "arbitrary one-qubit unitaries and full CZ only",
        "probe_preparations": probes,
        "verification": "full operator at n=6; three complete-output probes at n=8,12",
    }
