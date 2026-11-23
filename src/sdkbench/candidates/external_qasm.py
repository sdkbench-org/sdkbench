"""Prepare coherent OpenQASM 2 inputs without running a participant compiler.

Qiskit supplies syntax and gate-definition expansion. Cirq independently parses
and simulates the source. Existing SDKBench semantics checks their agreement with
the common rotation/CX input given to every participant. These are preparation
checks, not replacements for the frozen independent W03 evaluator.
"""

from __future__ import annotations

import hashlib
import importlib.metadata
import math
import re
from typing import Any, Sequence

import numpy as np

from ..p0.models import ContractError, require
from ..p0.semantics import equivalent, propagate

_MAX_SOURCE_BYTES = 1 << 20
_MAX_WIDTH = 12
_MAX_OPERATIONS = 20000
_MAX_EXPANSIONS = 200000
_MAX_DEFINITION_DEPTH = 64
_REGISTER = re.compile(r"\b(qreg|creg)\s+([A-Za-z_][A-Za-z0-9_]*)\s*\[\s*(\d+)\s*\]")
_INCLUDE = re.compile(r'\binclude\s*"([^"\n]*)"\s*;')
_BARRIER = re.compile(r"\bbarrier\b[^;{}]*;")


def _without_comments(source: str) -> str:
    # A // inside an include string is not a comment. Keep line numbers intact.
    return re.sub(
        r'"[^"\n]*"|//[^\n]*',
        lambda item: item[0] if item[0].startswith('"') else "",
        source,
    )


def _source_text(source: str) -> str:
    require(isinstance(source, str), "QASM source must be text")
    require(
        len(source.encode("utf-8")) <= _MAX_SOURCE_BYTES, "QASM source exceeds 1 MiB"
    )
    text = _without_comments(source)
    require(
        len(re.findall(r"\binclude\b", text)) == len(_INCLUDE.findall(text)),
        "Malformed or unsupported include directive",
    )
    require(
        all(name == "qelib1.inc" for name in _INCLUDE.findall(text)),
        "Only the built-in qelib1.inc include is admitted",
    )
    widths = {"qreg": 0, "creg": 0}
    for kind, _, digits in _REGISTER.findall(text):
        significant = digits.lstrip("0")
        require(len(significant) <= 2, "Register width exceeds preparation limit")
        width = int(significant or "0")
        require(1 <= width <= _MAX_WIDTH, "Register width exceeds preparation limit")
        widths[kind] += width
        require(
            widths[kind] <= _MAX_WIDTH, "Total register width exceeds preparation limit"
        )
    return text


def _coherent_prefix(circuit: Any) -> tuple[Any, dict[str, Any]]:
    from qiskit.circuit import Barrier, Gate, Measure

    require(1 <= circuit.num_qubits <= _MAX_WIDTH, "QASM width is outside 1..12")
    require(len(circuit.data) <= _MAX_EXPANSIONS, "Source instruction budget exceeded")
    prefix = circuit.copy_empty_like()
    terminal = []
    barriers = []
    measuring = False
    for index, item in enumerate(circuit.data):
        gate = item.operation
        wires = [circuit.find_bit(q).index for q in item.qubits]
        if isinstance(gate, Barrier):
            barriers.append({"source_instruction": index, "qubits": wires})
            continue
        if isinstance(gate, Measure):
            measuring = True
            terminal.append(
                {
                    "source_instruction": index,
                    "qubits": wires,
                    "clbits": [circuit.find_bit(c).index for c in item.clbits],
                }
            )
            continue
        require(
            not measuring,
            "Quantum operation after measurement is not a coherent prefix",
        )
        require(
            isinstance(gate, Gate) and not item.clbits,
            "Reset, classical control and nongate instructions are not admitted",
        )
        require(
            getattr(gate, "condition", None) is None and not gate.is_parameterized(),
            "Conditional or unresolved gates are not admitted",
        )
        prefix.append(gate, item.qubits)
    # Overall phase is outside this operator contract, including definition phases.
    prefix.global_phase = circuit.global_phase
    return prefix, {
        "terminal_measurements_removed": terminal,
        "barriers_ignored_for_unitary_task": barriers,
        "program_global_phase_ignored": float(circuit.global_phase),
    }


def _expand(circuit: Any) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    from qiskit.circuit import Barrier, Gate
    from qiskit.circuit.library import CXGate, UGate

    operations: list[dict[str, Any]] = []
    trace: list[dict[str, Any]] = []
    expanded = 0
    deepest = 0
    ignored_barriers = 0
    definition_phases = []

    def visit(
        gate: Any, wires: list[int], path: tuple[int, ...], active: frozenset[int]
    ) -> None:
        nonlocal expanded, deepest, ignored_barriers
        expanded += 1
        deepest = max(deepest, len(path))
        require(
            expanded <= _MAX_EXPANSIONS, "Gate-definition expansion budget exceeded"
        )
        require(
            len(path) <= _MAX_DEFINITION_DEPTH, "Gate-definition depth budget exceeded"
        )
        if isinstance(gate, Barrier):
            ignored_barriers += 1
            return
        require(
            isinstance(gate, Gate) and gate.num_clbits == 0,
            "Nonunitary gate definition is not admitted",
        )
        require(
            not gate.is_parameterized(), "Unresolved gate definition is not admitted"
        )
        start = len(operations)
        primitive_phase = 0.0
        if isinstance(gate, CXGate):
            require(len(wires) == 2 and len(set(wires)) == 2, "Invalid CX operands")
            operations.append({"name": "cx", "qubits": wires})
        elif isinstance(gate, UGate):
            require(len(wires) == 1 and len(gate.params) == 3, "Invalid U gate")
            theta, phi, lam = map(float, gate.params)
            require(
                all(math.isfinite(value) for value in (theta, phi, lam)),
                "Nonfinite gate angle",
            )
            # U(theta,phi,lambda) = Rz(phi) Ry(theta) Rz(lambda), up to one phase.
            # Circuit order is right factor first. Keep even zero rotations.
            primitive_phase = phi / 2 + lam / 2
            operations.extend(
                {"name": name, "qubits": wires, "angle": angle}
                for name, angle in (("rz", lam), ("ry", theta), ("rz", phi))
            )
        else:
            require(id(gate) not in active, "Cyclic gate definition is not admitted")
            definition = gate.definition
            require(
                definition is not None
                and definition.num_qubits == len(wires)
                and definition.num_clbits == 0,
                "Opaque or inconsistent gate definition",
            )
            phase = float(definition.global_phase)
            require(math.isfinite(phase), "Nonfinite definition phase")
            if phase != 0:
                definition_phases.append(
                    {"definition_path": list(path), "phase": phase}
                )
            for index, item in enumerate(definition.data):
                require(
                    not item.clbits,
                    "Classical gate-definition operands are not admitted",
                )
                selected = [wires[definition.find_bit(q).index] for q in item.qubits]
                visit(item.operation, selected, path + (index,), active | {id(gate)})
            return
        require(
            len(operations) <= _MAX_OPERATIONS, "Canonical operation budget exceeded"
        )
        trace.append(
            {
                "definition_path": list(path),
                "gate": gate.name,
                "qubits": wires,
                "canonical_start": start,
                "canonical_stop": len(operations),
                "global_phase_ignored": primitive_phase,
            }
        )

    for index, item in enumerate(circuit.data):
        visit(
            item.operation,
            [circuit.find_bit(q).index for q in item.qubits],
            (index,),
            frozenset(),
        )
    return operations, {
        "visited_definition_nodes": expanded,
        "maximum_depth": deepest,
        "definition_barriers_ignored": ignored_barriers,
        "definition_global_phases_ignored": definition_phases,
        "primitive_expansion_trace": trace,
    }


def _independent_prefix(
    text: str, register_order: list[tuple[str, int]]
) -> tuple[Any, list[Any]]:
    import cirq
    from cirq.contrib.qasm_import import circuit_from_qasm
    from cirq.contrib.qasm_import.exception import QasmException

    # Cirq's parser does not admit barriers. They carry no unitary semantics in
    # this declared task; remove only these annotations, after primary parsing.
    projected = _BARRIER.sub("", text)
    require(
        re.search(r"\bbarrier\b", projected) is None, "Unrecognized barrier statement"
    )
    try:
        parsed = circuit_from_qasm(projected)
    except QasmException as error:
        raise ContractError(
            f"Independent source parser refused input: {error}"
        ) from error
    wires = [
        cirq.NamedQubit(f"{name}_{index}")
        for name, width in register_order
        for index in range(width)
    ]
    require(
        parsed.all_qubits() <= set(wires), "Independent parser wire mapping differs"
    )
    gates = []
    for item in parsed.all_operations():
        if cirq.is_measurement(item):
            continue
        require(cirq.has_unitary(item), "Independent source is not a coherent unitary")
        gates.append(item)
    # SDKBench and Qiskit use q0 as the least significant state index bit.
    return cirq.Circuit(gates), wires[::-1]


def convert_source(
    source: str, *, probe_preparations: Sequence[Sequence[dict[str, Any]]] | None = None
) -> dict[str, Any]:
    """Convert a bounded coherent QASM 2 prefix and cross-check its source meaning.

    Requires Qiskit and Cirq with its contrib parser dependency. No SDK compiler,
    optimizer or transpiler is called. Call under an external bounded preparation
    supervisor. Widths above six require the three frozen probe preparations;
    their agreement does not prove universal operator equivalence.
    """
    text = _source_text(source)
    from qiskit import qasm2

    try:
        parsed = qasm2.loads(source, include_path=(), strict=True)
    except qasm2.QASM2ParseError as error:
        raise ContractError(f"QASM syntax admission failed: {error}") from error
    prefix, projection = _coherent_prefix(parsed)
    require(math.isfinite(float(prefix.global_phase)), "Nonfinite program phase")
    registers = [(register.name, register.size) for register in parsed.qregs]
    require(
        sum(width for _, width in registers) == parsed.num_qubits,
        "Quantum register ownership is incomplete",
    )
    if parsed.num_qubits > 6:
        require(
            probe_preparations is not None and len(probe_preparations) == 3,
            "Widths above six require exactly three frozen probe preparations",
        )
        require(
            all(len(probe) <= _MAX_OPERATIONS for probe in probe_preparations),
            "Probe preparation operation budget exceeded",
        )
    operations, expansion = _expand(prefix)
    independent, order = _independent_prefix(text, registers)
    import cirq
    from qiskit.quantum_info import Operator, Statevector

    n = parsed.num_qubits
    errors = []
    if n <= 6:
        converted = propagate(n, operations, np.eye(1 << n))
        errors.append(equivalent(converted, Operator(prefix).data, 1e-8))
        errors.append(
            equivalent(converted, independent.unitary(qubit_order=order), 1e-8)
        )
        verification = "full-operator"
    else:
        assert probe_preparations is not None
        simulator = cirq.Simulator(dtype=np.complex128, seed=0)
        for preparation in probe_preparations:
            initial = propagate(n, preparation)
            converted = propagate(n, operations, initial)
            errors.append(
                equivalent(converted, Statevector(initial).evolve(prefix).data, 1e-8)
            )
            actual = simulator.simulate(
                independent, initial_state=initial, qubit_order=order
            )
            errors.append(equivalent(converted, actual.final_state_vector, 1e-8))
        verification = "three-probes-only"
    return {
        "source_sha256": hashlib.sha256(source.encode("utf-8")).hexdigest(),
        "source_bytes": len(source.encode("utf-8")),
        "n_qubits": n,
        "register_order": [{"name": name, "width": width} for name, width in registers],
        "operations": operations,
        "projection": projection,
        "expansion": expansion,
        "source_conformance": {
            "verification": verification,
            "maximum_error": max(errors),
            "parsers": {
                name: importlib.metadata.version(name)
                for name in ("qiskit", "cirq-core", "ply")
            },
            "scope": "Preparation only; unchanged W03 acceptance still required",
        },
    }
