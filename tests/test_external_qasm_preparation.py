"""External syntax conversion is separate from participant compilation and acceptance."""

import math

import numpy as np
import pytest

from sdkbench.candidates import external_qasm
from sdkbench.p0.models import ContractError
from sdkbench.p0.semantics import equivalent, propagate


def source(body, registers="qreg q[3]; creg c[3];"):
    return 'OPENQASM 2.0; include "qelib1.inc"; ' + registers + "\n" + body


@pytest.fixture
def native_parsers():
    pytest.importorskip("qiskit")
    pytest.importorskip("cirq")
    pytest.importorskip("ply")


def test_preparse_bounds_prevent_external_file_and_huge_register_access():
    for value in [
        source("x q[0];", "qreg q[999999999999999999999];"),
        source("x q[0];", "qreg q[8]; qreg other[8];"),
        'OPENQASM 2.0; include "/etc/passwd"; qreg q[1];',
        'OPENQASM 2.0; include/*hidden*/ "/tmp/forbidden.inc"; qreg q[1];',
        'OPENQASM 2.0; include"/tmp/forbidden.inc"; qreg q[1];',
        'OPENQASM 2.0; include "https://example.invalid/file"; qreg q[1];',
        "x" * ((1 << 20) + 1),
    ]:
        with pytest.raises(ContractError):
            external_qasm._source_text(value)
    text = external_qasm._source_text(source('// include "bad.inc";\nx q[0];'))
    assert 'include "bad.inc"' not in text
    # A // in a string is retained, so it cannot conceal a forbidden include.
    with pytest.raises(ContractError, match="built-in"):
        external_qasm._source_text('include "//etc/passwd";')


def test_u_factor_order_and_reversed_cx_have_independent_analytic_operator(
    native_parsers,
):
    theta, phi, lam = 0.37, -0.8, 1.1
    result = external_qasm.convert_source(
        source(f"U({theta},{phi},{lam}) q[2]; CX q[2],q[0];")
    )
    expected_u = np.array(
        [
            [math.cos(theta / 2), -np.exp(1j * lam) * math.sin(theta / 2)],
            [
                np.exp(1j * phi) * math.sin(theta / 2),
                np.exp(1j * (phi + lam)) * math.cos(theta / 2),
            ],
        ]
    )
    expected = np.kron(expected_u, np.eye(4))
    permutation = np.arange(8) ^ (((np.arange(8) >> 2) & 1) << 0)
    expected = expected[permutation]
    equivalent(propagate(3, result["operations"], np.eye(8)), expected, 1e-12)
    assert result["operations"] == [
        {"name": "rz", "qubits": [2], "angle": lam},
        {"name": "ry", "qubits": [2], "angle": theta},
        {"name": "rz", "qubits": [2], "angle": phi},
        {"name": "cx", "qubits": [2, 0]},
    ]
    assert result["source_conformance"]["verification"] == "full-operator"


def test_custom_definitions_keep_register_order_unused_wires_and_relative_phase(
    native_parsers,
):
    text = source(
        """
    gate pair(t) a,b { h a; cu1(t) a,b; cx b,a; }
    pair(pi/3) right[1], left[0];
    measure left -> c;
    """,
        "qreg right[2]; qreg left[1]; creg c[1];",
    )
    result = external_qasm.convert_source(text)
    assert result["n_qubits"] == 3
    assert result["register_order"] == [
        {"name": "right", "width": 2},
        {"name": "left", "width": 1},
    ]
    assert len(result["projection"]["terminal_measurements_removed"]) == 1
    # right[0] is declared but unused: an independent complete operator retains it.
    assert all(0 not in item["qubits"] for item in result["operations"])
    assert result["source_conformance"]["maximum_error"] < 1e-12


def test_toffoli_keeps_all_basis_columns_and_not_only_zero_input(native_parsers):
    result = external_qasm.convert_source(source("ccx q[2],q[0],q[1];"))
    expected = np.eye(8, dtype=complex)
    expected[:, [5, 7]] = expected[:, [7, 5]]
    equivalent(propagate(3, result["operations"], np.eye(8)), expected, 1e-12)


def test_declared_unitary_projection_records_barriers_and_terminal_measurements(
    native_parsers,
):
    result = external_qasm.convert_source(
        source(
            """
    gate custom a,b { h a; barrier a,b; cx a,b; }
    custom q[0],q[1]; barrier q; measure q -> c; barrier q;
    """
        )
    )
    assert len(result["projection"]["barriers_ignored_for_unitary_task"]) == 2
    assert result["expansion"]["definition_barriers_ignored"] == 1
    assert len(result["projection"]["terminal_measurements_removed"]) == 3
    assert result["source_conformance"]["maximum_error"] < 1e-12


@pytest.mark.parametrize(
    "body",
    [
        "measure q[0] -> c[0]; x q[1];",
        "reset q[0];",
        "if(c==1) x q[0];",
        "opaque blackbox a; blackbox q[0];",
        "rx(unresolved) q[0];",
        "x q[3];",
        "CX q[0],q[0];",
    ],
)
def test_dynamic_opaque_unresolved_and_invalid_sources_refuse(native_parsers, body):
    with pytest.raises(ContractError):
        external_qasm.convert_source(source(body))


def test_growing_and_deep_gate_definitions_refuse_before_secondary_parse(
    native_parsers, monkeypatch
):
    monkeypatch.setattr(external_qasm, "_MAX_OPERATIONS", 2)
    with pytest.raises(ContractError, match="operation budget"):
        external_qasm.convert_source(source("U(0,0,0) q[0];"))
    monkeypatch.setattr(external_qasm, "_MAX_OPERATIONS", 20000)
    monkeypatch.setattr(external_qasm, "_MAX_DEFINITION_DEPTH", 2)
    with pytest.raises(ContractError, match="depth budget"):
        external_qasm.convert_source(
            source("gate a x { h x; } gate b x { a x; } b q[0];")
        )


def test_large_width_source_requires_and_records_exactly_three_probes(native_parsers):
    text = source("h q[0]; cx q[0],q[7];", "qreg q[8];")
    with pytest.raises(ContractError, match="exactly three"):
        external_qasm.convert_source(text)
    probes = [
        [],
        [{"name": "x", "qubits": [7]}],
        [{"name": "h", "qubits": [3]}, {"name": "ry", "qubits": [0], "angle": 0.37}],
    ]
    result = external_qasm.convert_source(text, probe_preparations=probes)
    assert result["source_conformance"]["verification"] == "three-probes-only"
    assert result["source_conformance"]["maximum_error"] < 1e-12


def test_source_conformance_detects_conversion_corruption(native_parsers, monkeypatch):
    original = external_qasm._expand

    def wrong(circuit):
        operations, trace = original(circuit)
        return operations[:-1], trace

    monkeypatch.setattr(external_qasm, "_expand", wrong)
    with pytest.raises(ContractError, match="semantics differ"):
        external_qasm.convert_source(source("h q[0]; cx q[0],q[2];"))


def test_preparation_never_calls_a_compiler(native_parsers, monkeypatch):
    import qiskit
    import cirq

    def forbidden(*args, **kwargs):
        raise AssertionError("A participant compiler ran during source preparation")

    monkeypatch.setattr(qiskit, "transpile", forbidden)
    monkeypatch.setattr(cirq, "optimize_for_target_gateset", forbidden)
    monkeypatch.setattr(cirq, "RouteCQC", forbidden)
    result = external_qasm.convert_source(source("h q[0]; cx q[0],q[1];"))
    assert result["source_conformance"]["maximum_error"] < 1e-12


def test_secondary_parser_disagreement_is_not_hidden(native_parsers, monkeypatch):
    import cirq

    original = external_qasm._independent_prefix

    def wrong(text, registers):
        circuit, order = original(text, registers)
        return circuit + cirq.Circuit(cirq.Z(order[-1])), order

    monkeypatch.setattr(external_qasm, "_independent_prefix", wrong)
    with pytest.raises(ContractError, match="semantics differ"):
        external_qasm.convert_source(source("h q[0]; cx q[0],q[2];"))


def test_phase_trace_records_primitive_and_definition_phases(native_parsers):
    result = external_qasm.convert_source(source("rz(0.37) q[0]; U(0.3,0.4,0.5) q[1];"))
    assert result["expansion"]["definition_global_phases_ignored"]
    assert any(
        abs(item["global_phase_ignored"] - 0.45) < 1e-15
        for item in result["expansion"]["primitive_expansion_trace"]
    )
