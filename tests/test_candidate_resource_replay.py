"""Resealing a campaign must not hide contradictory resource evidence."""

from pathlib import Path
import shutil

import pytest

from sdkbench.candidates.replay import replay
from sdkbench.p0 import Bundle
from sdkbench.p0.models import ContractError, canonical_bytes, read_json
from sdkbench.p1a import campaign
from test_candidate_runner import registration, seal, synthetic_supervisor


@pytest.fixture(scope="module")
def accepted_campaign(tmp_path_factory):
    bundle = Bundle(Path(__file__).resolve().parents[1] / "docs/implementation")
    root = tmp_path_factory.mktemp("resource-campaign") / "run"
    reg = registration()
    with pytest.MonkeyPatch.context() as patch:
        synthetic_supervisor(patch, bundle)
        campaign.run_campaign(
            bundle,
            directory=root,
            cgroup_parent=root.parent,
            cpu=0,
            suite="compiler-candidate",
            candidates={reg.stack_id: reg},
        )
    seal(root)
    return root, bundle, reg.stack_id


def test_complete_resource_evidence_replays(accepted_campaign):
    root, bundle, _ = accepted_campaign
    result = replay(root, bundle)
    assert result["blocks_verified"] == 30
    assert {row["status"] for row in result["cases"]} == {"accepted"}


@pytest.mark.parametrize(
    "field", ["memory_bytes", "output_bytes", "file_bytes", "tasks"]
)
def test_resealed_changed_limits_are_rejected(accepted_campaign, tmp_path, field):
    source, bundle, stack = accepted_campaign
    root = tmp_path / "run"
    shutil.copytree(source, root)
    path = root / stack / "ROUTE-LINE-06/block-00/evidence.json"
    evidence = read_json(path)
    evidence["execution"]["limits"][field] *= 2
    path.write_bytes(canonical_bytes(evidence))
    seal(root)
    with pytest.raises(ContractError, match="resource limits"):
        replay(root, bundle)


@pytest.mark.parametrize(
    "field,value",
    [
        ("returncode", 1),
        ("returncode", False),
        ("kernel_memory_peak_bytes", None),
        ("kernel_memory_peak_bytes", True),
        ("wall_seconds", None),
        ("wall_seconds", -1),
    ],
)
def test_resealed_incomplete_or_failed_execution_is_rejected(
    accepted_campaign, tmp_path, field, value
):
    source, bundle, stack = accepted_campaign
    root = tmp_path / "run"
    shutil.copytree(source, root)
    path = root / stack / "ROUTE-LINE-06/block-00/evidence.json"
    evidence = read_json(path)
    evidence["execution"][field] = value
    path.write_bytes(canonical_bytes(evidence))
    seal(root)
    with pytest.raises(ContractError):
        replay(root, bundle)


def test_resealed_cumulative_execution_overrun_is_rejected(accepted_campaign, tmp_path):
    source, bundle, stack = accepted_campaign
    root = tmp_path / "run"
    shutil.copytree(source, root)
    cap = bundle.cases["ROUTE-LINE-06"]["case_wall_limit_seconds"]
    for path in (root / stack / "ROUTE-LINE-06").glob("*/evidence.json"):
        evidence = read_json(path)
        evidence["execution"]["wall_seconds"] = cap / 9
        path.write_bytes(canonical_bytes(evidence))
    seal(root)
    with pytest.raises(ContractError, match="cumulative execution wall budget"):
        replay(root, bundle)
