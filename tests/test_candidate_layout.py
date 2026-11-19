"""Matched output obligations use one independent, exact restoration policy."""

from copy import deepcopy
from itertools import permutations
from types import SimpleNamespace

import numpy as np
import pytest

from sdkbench.candidates.adapters import CompilerAdapter, workflow_configuration
from sdkbench.candidates.layout import restoration_swaps, restore_payload
from sdkbench.p0.models import ContractError, digest
from sdkbench.p0.semantics import propagate


@pytest.mark.parametrize(
    "edges",
    [
        [[0, 1], [1, 2], [2, 3]],
        [[0, 1], [0, 2], [0, 3]],
        [[0, 1], [1, 2], [2, 3], [3, 0]],
    ],
)
def test_all_four_wire_permutations_restore_complete_operator(edges):
    allowed = {frozenset(e) for e in edges}
    for layout in permutations(range(4)):
        # Independent permutation operator: logical input bits occupy layout[q].
        operator = np.zeros((16, 16), dtype=complex)
        for column in range(16):
            row = sum(((column >> q) & 1) << layout[q] for q in range(4))
            operator[row, column] = 1
        payload = {"operations": [], "final_layout": list(layout)}
        audit = restore_payload(payload, edges)
        actual = propagate(4, payload["operations"], operator, target_edges=allowed)
        np.testing.assert_allclose(actual, np.eye(16), atol=2e-14, rtol=0)
        assert payload["final_layout"] == list(range(4))
        assert audit["restoration_cz_count"] == sum(
            op["name"] == "cz" for op in payload["operations"]
        )
        assert audit["restoration_operations"] == len(payload["operations"])
        assert audit["restoration_swaps"] <= 4 * 3 // 2
        assert restoration_swaps(list(layout), edges) == restoration_swaps(
            list(layout), edges[::-1]
        )


def test_identity_and_invalid_layouts_fail_explicitly():
    payload = {
        "operations": [{"name": "rz", "qubits": [0], "angle": 0.3}],
        "final_layout": [0, 1],
    }
    original = deepcopy(payload)
    assert restore_payload(payload, [[0, 1]])["restoration_swaps"] == 0
    assert payload == original
    for layout, edges in [
        ([0, 0], [[0, 1]]),
        ([False, 1], [[0, 1]]),
        ([1, 0], []),
        ([0, 1], [[0, 2]]),
        ([], []),
    ]:
        with pytest.raises(ContractError):
            restoration_swaps(layout, edges)


def test_every_control_has_distinct_identity_and_preserves_base_configuration():
    for name in ("flagquantum-ordinary", "qiskit-transpile", "cirq-route-cz"):
        base = workflow_configuration(name)
        control = workflow_configuration(name + "-restored")
        assert digest(base) != digest(control)
        policy = control["options"].pop("postprocessing")
        assert policy["timed"] and not policy["optimization_after_restoration"]
        assert control == base


def test_restoration_is_inside_compile_timer_and_preserves_raw_cost(monkeypatch):
    from sdkbench.candidates import adapters, layout

    clock = [0.0]
    monkeypatch.setattr("time.perf_counter", lambda: clock[0])
    native = SimpleNamespace(audit={})

    def compile_source(adapter, fixture, seed):
        clock[0] += 2
        adapter.audit = {"native_compilations": 1}
        return {"operations": [], "final_layout": [1, 0]}

    original = layout.restore_payload

    def restore(payload, edges):
        clock[0] += 3
        return original(payload, edges)

    monkeypatch.setattr(adapters, "_qiskit_route", compile_source)
    monkeypatch.setattr(layout, "restore_payload", restore)
    fixture = {
        "n_qubits": 2,
        "operations": [],
        "target_edges": [[0, 1]],
        "initial_layout": "identity",
        "ancillas_allowed": 0,
    }
    adapter = CompilerAdapter(native, "qiskit-transpile-restored")
    payload = adapter.execute("route", fixture, 11)
    assert payload["compile_wall_seconds"] == 5
    assert payload["final_layout"] == [0, 1]
    assert adapter.audit["restoration_cz_count"] == 3
    assert adapter.audit["native_compilations"] == 1
