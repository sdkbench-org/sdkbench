"""New fixtures retain frozen acceptance and load through the existing bundle."""

from pathlib import Path

import pytest

from sdkbench.candidates.application_bundle import build_bundle
from sdkbench.p0.bundle import Bundle
from sdkbench.p0.models import ContractError
from sdkbench.p0.evaluators import routing
from sdkbench.candidates.adapters import CompilerAdapter
from sdkbench.p1a.common import UnsupportedCapability

BASE = Path(__file__).resolve().parents[1] / "docs/implementation"


def test_bundle_contains_complete_cohort_and_unchanged_acceptance(tmp_path):
    baseline = Bundle(BASE)
    before = {name: (BASE / name).read_bytes() for name in baseline.manifest["files"]}
    first = build_bundle(BASE, tmp_path / "first", "01" * 32)
    second = build_bundle(BASE, tmp_path / "second", "01" * 32)
    assert first.sha256 == second.sha256
    assert len(first.cases) == 60
    assert len({case["arguments"]["family"] for case in first.cases.values()}) == 5
    assert first.plan["execution_profile"] == baseline.plan["execution_profile"]
    assert first.plan["application_generation"]["evidence_class"] == "development"
    for key, case in first.cases.items():
        n = first.fixtures[key]["n_qubits"]
        original = next(
            c
            for k, c in baseline.cases.items()
            if c["workflow"] == "W03" and baseline.fixtures[k]["n_qubits"] == n
        )
        for field in (
            "acceptance",
            "case_wall_limit_seconds",
            "process_memory_limit_gib",
        ):
            assert case[field] == original[field]
        identity = first.identity(key, "test", "a" * 64, "b" * 64)
        request = first.request(identity)
        assert "reference" not in request
        assert request["fixture"] == first.fixtures[key]
    assert all(
        (BASE / name).read_bytes() == contents for name, contents in before.items()
    )
    with pytest.raises(FileExistsError):
        build_bundle(BASE, tmp_path / "first", "01" * 32)


def test_different_nonce_changes_identity_and_tamper_is_rejected(tmp_path):
    first = build_bundle(BASE, tmp_path / "first", "01" * 32)
    second = build_bundle(BASE, tmp_path / "second", "02" * 32)
    assert first.sha256 != second.sha256
    path = first.directory / next(iter(first.cases.values()))["fixture"]
    path.write_text(path.read_text() + " ")
    with pytest.raises(ContractError, match="Artifact hash mismatch"):
        Bundle(first.directory)


def test_new_qft_case_rejects_corrupt_output_through_unchanged_evaluator(tmp_path):
    bundle = build_bundle(BASE, tmp_path / "bundle", "01" * 32)
    key = "APP-QFT-LINE-06"
    with pytest.raises(ContractError, match="Program semantics differ"):
        routing(
            {
                "operations": [{"name": "h", "qubits": [q]} for q in range(6)],
                "final_layout": list(range(6)),
                "compile_wall_seconds": 0.0,
            },
            bundle.fixtures[key],
            bundle.references[key],
            bundle.cases[key],
            0,
        )


def test_numeric_candidate_refuses_symbolic_input_before_sdk_construction():
    from types import SimpleNamespace

    adapter = CompilerAdapter(SimpleNamespace(), "qiskit-transpile")
    value = {
        "n_qubits": 6,
        "operations": [{"name": "rx", "qubits": [0], "parameter": 0}],
        "parameters": [0.2],
        "initial_layout": "identity",
        "ancillas_allowed": 0,
    }
    with pytest.raises(UnsupportedCapability, match="explicit numeric bindings"):
        adapter.execute("route", value, 11)


def test_full_application_campaign_retains_denials_and_replays(tmp_path, monkeypatch):
    from sdkbench.candidates import provenance
    from sdkbench.candidates.replay import replay
    from sdkbench.p1a import campaign
    from test_candidate_runner import registration, seal

    bundle = build_bundle(BASE, tmp_path / "bundle", "01" * 32)

    def reject(_):
        raise ContractError("Synthetic unavailable installation")

    monkeypatch.setattr(provenance, "verify_runtime", reject)
    reg = registration()
    root = tmp_path / "run"
    result = campaign.run_campaign(
        bundle,
        directory=root,
        cgroup_parent=tmp_path,
        cpu=0,
        suite="compiler-candidate",
        candidates={reg.stack_id: reg},
    )
    assert len(result["outcomes"]) == 60
    assert all(row["record_count"] == 30 for row in result["outcomes"])
    seal(root)
    checked = replay(root, bundle)
    assert checked["blocks_verified"] == 600
    assert {row["status"] for row in checked["cases"]} == {"access-blocked"}
    assert not checked["publication_eligible"]
