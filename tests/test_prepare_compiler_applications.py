"""A reduced prospective cohort preserves acceptance and freezes before drawing."""

import importlib.util
from pathlib import Path

import pytest

from sdkbench.candidates.adapters import workflow_configuration
from sdkbench.p0 import Bundle
from sdkbench.p0.models import ContractError, canonical_bytes, digest, read_json

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def preparation():
    spec = importlib.util.spec_from_file_location(
        "prepare_applications", ROOT / "tools/prepare_compiler_applications.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def registration_paths(directory, workflows):
    paths = []
    for index, workflow in enumerate(workflows):
        payload = {
            "stack_id": f"candidate-{index}",
            "schema_version": 1,
            "components": [
                {
                    "name": "test",
                    "version": "1",
                    "role": "frontend",
                    "artifact_sha256": "a" * 64,
                }
            ],
            "configuration": {
                "profile": "CPU1-FP64",
                "precision": "float64/complex128",
                "threads": 1,
                "options": {
                    "workflow": workflow,
                    "sdk": workflow_configuration(workflow)["sdk"],
                    "compiler_options": workflow_configuration(workflow),
                    "source_build": {
                        "source_commit": "d" * 40,
                        "wheel": {"sha256": "e" * 64},
                    },
                },
            },
            "environment": {
                "python": "3.12.14",
                "os": "test",
                "image_sha256": "b" * 64,
                "dependency_lock_sha256": "c" * 64,
                "host": {"test": True, "cpuinfo_sha256": f"{index:064x}"},
            },
        }
        path = directory / f"registration-{index}.json"
        path.write_bytes(canonical_bytes(payload))
        paths.append(path)
    return paths


@pytest.mark.parametrize("profile", ["ordinary", "target-artifact", "routing-policies"])
def test_freeze_precedes_single_draw_and_selected_cases_keep_original_bytes(
    preparation,
    tmp_path,
    monkeypatch,
    profile,
):
    workflows = {
        "ordinary": preparation.WORKFLOWS,
        "target-artifact": preparation.TARGET_WORKFLOWS,
        "routing-policies": preparation.ROUTING_POLICY_WORKFLOWS,
    }[profile]
    paths = registration_paths(tmp_path, sorted(workflows))
    output = tmp_path / "campaign"
    admissions = []
    monkeypatch.setattr(
        preparation, "verify_runtime", lambda r: admissions.append(r.stack_id)
    )
    draws = []

    def draw(size):
        freeze = read_json(output / "freeze.json")
        assert size == 32 and len(freeze["registrations"]) == len(workflows)
        assert freeze["workflow_profile"] == profile
        assert len(admissions) == len(workflows)
        draws.append(size)
        return bytes.fromhex("01" * 32)

    monkeypatch.setattr(preparation.secrets, "token_bytes", draw)
    cohort = preparation.prepare(
        ROOT / "docs/implementation", paths, output, profile=profile
    )
    full = Bundle(output / "full-bundle")
    assert len(full.cases) == 60 and len(cohort.cases) == 30
    assert cohort.plan["execution_profile"] == full.plan["execution_profile"]
    assert {c["arguments"]["topology"] for c in cohort.cases.values()} == {
        "line",
        "grid",
    }
    for key, case in cohort.cases.items():
        assert case == full.cases[key]
        for field in ("fixture", "reference_artifact"):
            assert (cohort.directory / case[field]).read_bytes() == (
                full.directory / case[field]
            ).read_bytes()
    freeze = read_json(output / "freeze.json")
    assert read_json(output / "draw.json")["freeze_sha256"] == digest(freeze)
    assert read_json(output / "selection.json")["cohort_bundle_sha256"] == cohort.sha256
    with pytest.raises(FileExistsError):
        preparation.prepare(
            ROOT / "docs/implementation", paths, output, profile=profile
        )
    assert draws == [32]


def test_wrong_workflow_is_rejected_before_creating_a_draw(preparation, tmp_path):
    paths = registration_paths(
        tmp_path, ["flagquantum-ordinary", "qiskit-transpile", "cirq-route-cz"]
    )
    with pytest.raises(ContractError, match="matched-restoration"):
        preparation.prepare(ROOT / "docs/implementation", paths, tmp_path / "campaign")
    assert not (tmp_path / "campaign").exists()


def test_runtime_change_is_rejected_before_creating_a_draw(
    preparation, tmp_path, monkeypatch
):
    paths = registration_paths(tmp_path, sorted(preparation.WORKFLOWS))

    def refuse(registration):
        raise ContractError("Candidate installed component changed")

    monkeypatch.setattr(preparation, "verify_runtime", refuse)
    with pytest.raises(ContractError, match="component changed"):
        preparation.prepare(ROOT / "docs/implementation", paths, tmp_path / "campaign")
    assert not (tmp_path / "campaign").exists()


@pytest.mark.parametrize("profile", ["unknown", "target-artifact", "routing-policies"])
def test_incorrect_profile_is_rejected_before_runtime_or_entropy(
    preparation, tmp_path, monkeypatch, profile
):
    paths = registration_paths(tmp_path, sorted(preparation.WORKFLOWS))
    monkeypatch.setattr(
        preparation, "verify_runtime", lambda _: pytest.fail("Runtime admission")
    )
    monkeypatch.setattr(
        preparation.secrets, "token_bytes", lambda _: pytest.fail("Entropy draw")
    )
    with pytest.raises(ContractError):
        preparation.prepare(
            ROOT / "docs/implementation", paths, tmp_path / "run", profile=profile
        )
    assert not (tmp_path / "run").exists()


@pytest.mark.parametrize("fault", [
    "missing", "duplicate", "mixed", "source", "wheel", "environment", "host", "options",
    "missing-build",
])
def test_routing_controls_reject_unmatched_inputs_before_entropy(
    preparation, tmp_path, monkeypatch, fault,
):
    workflows = sorted(preparation.ROUTING_POLICY_WORKFLOWS)
    if fault == "missing":
        workflows.pop()
    elif fault == "duplicate":
        workflows[-1] = workflows[0]
    elif fault == "mixed":
        workflows[-1] = "qiskit-transpile-restored"
    paths = registration_paths(tmp_path, workflows)
    changed = read_json(paths[-1])
    options = changed["configuration"]["options"]
    if fault == "source":
        options["source_build"]["source_commit"] = "f" * 40
    elif fault == "wheel":
        options["source_build"]["wheel"]["sha256"] = "f" * 64
    elif fault == "environment":
        changed["environment"]["dependency_lock_sha256"] = "f" * 64
    elif fault == "host":
        changed["environment"]["host"]["cpu_models"] = ["another-host"]
    elif fault == "options":
        options["compiler_options"]["options"]["routing"] = "auto"
    elif fault == "missing-build":
        del options["source_build"]
    paths[-1].write_bytes(canonical_bytes(changed))
    monkeypatch.setattr(
        preparation, "verify_runtime", lambda _: pytest.fail("Runtime admission")
    )
    monkeypatch.setattr(
        preparation.secrets, "token_bytes", lambda _: pytest.fail("Entropy draw")
    )
    with pytest.raises(ContractError):
        preparation.prepare(
            ROOT / "docs/implementation", paths, tmp_path / "run", profile="routing-policies"
        )
    assert not (tmp_path / "run").exists()
