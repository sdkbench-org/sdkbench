"""A reduced prospective cohort preserves acceptance and freezes before drawing."""

import importlib.util
from pathlib import Path

import pytest

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
                "options": {"workflow": workflow},
            },
            "environment": {
                "python": "3.12.14",
                "os": "test",
                "image_sha256": "b" * 64,
                "dependency_lock_sha256": "c" * 64,
                "host": {"test": True},
            },
        }
        path = directory / f"registration-{index}.json"
        path.write_bytes(canonical_bytes(payload))
        paths.append(path)
    return paths


def test_freeze_precedes_single_draw_and_selected_cases_keep_original_bytes(
    preparation,
    tmp_path,
    monkeypatch,
):
    paths = registration_paths(tmp_path, sorted(preparation.WORKFLOWS))
    output = tmp_path / "campaign"
    admissions = []
    monkeypatch.setattr(
        preparation, "verify_runtime", lambda r: admissions.append(r.stack_id)
    )
    draws = []

    def draw(size):
        freeze = read_json(output / "freeze.json")
        assert size == 32 and len(freeze["registrations"]) == 3
        assert len(admissions) == 3
        draws.append(size)
        return bytes.fromhex("01" * 32)

    monkeypatch.setattr(preparation.secrets, "token_bytes", draw)
    cohort = preparation.prepare(ROOT / "docs/implementation", paths, output)
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
        preparation.prepare(ROOT / "docs/implementation", paths, output)
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
