"""Comparison reporting retains failures and uses paired complete blocks."""

import importlib.util
from pathlib import Path
from copy import deepcopy

import pytest

from sdkbench.p0.models import ContractError

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def tool(monkeypatch):
    monkeypatch.syspath_prepend(str(ROOT / "tools"))
    spec = importlib.util.spec_from_file_location(
        "application_comparison", ROOT / "tools/compare_compiler_applications.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def summary(tool):
    rows = []
    for instance in ("case-a", "case-b"):
        for scale, workflow in enumerate(sorted(tool.WORKFLOWS), 1):
            rows.append(
                {
                    "instance": instance,
                    "workflow": workflow,
                    "status": "accepted",
                    "expected_records": 30,
                    "accepted_records": 30,
                    "full_cz_count_for_accepted_records": {"median": 6 * scale},
                    "dependency_depth_for_accepted_records": {"median": 4 * scale},
                    "blocks": [
                        {
                            "block": block,
                            "status": "accepted",
                            "timing_eligible": True,
                            "compile_wall_seconds": [
                                scale * (block + 1),
                                scale * (block + 2),
                                scale * (block + 3),
                            ],
                            "kernel_memory_peak_bytes": scale * 1024 * (block + 1),
                        }
                        for block in range(10)
                    ],
                }
            )
    return {
        "publication_eligible": False,
        "bundle_sha256": "a" * 64,
        "independent_replay": {"blocks_verified": 60},
        "cases": rows,
    }


def test_all_pairs_use_common_blocks_and_keep_full_case_denominators(tool):
    source = summary(tool)
    before = deepcopy(source)
    result = tool.compare(source)
    assert source == before
    assert result["case_count"] == 2 and len(result["pairs"]) == 6
    assert all(status == {"accepted": 2} for status in result["coverage"].values())
    row = result["pairs"][0]
    assert row["ratios"]["full_cz_median"] == 0.5
    assert row["ratios"]["paired_block_compile_time"]["median"] == 0.5
    assert row["ratios"]["paired_block_compile_time"]["count"] == 10
    assert row["ratios"]["paired_block_memory_peak"]["median"] == 0.5
    assert result["publication_eligible"] is False


def test_one_warmup_failure_excludes_whole_case_comparisons(tool):
    source = summary(tool)
    source["cases"][0]["status"] = "timeout"
    result = tool.compare(source)
    affected = [row for row in result["pairs"] if row["instance"] == "case-a"]
    assert sum(row["ratios"] is None for row in affected) == 2
    assert sum(row["ratios"] is not None for row in affected) == 1
    assert result["coverage"][source["cases"][0]["workflow"]] == {
        "timeout": 1,
        "accepted": 1,
    }
    assert result["case_count"] == 2


def test_missing_and_zero_metrics_are_not_silently_dropped(tool):
    source = summary(tool)
    row = source["cases"][0]
    row["full_cz_count_for_accepted_records"]["median"] = 0
    row["blocks"][3]["compile_wall_seconds"] = [0, 0, 0]
    row["blocks"][4]["kernel_memory_peak_bytes"] = None
    first = tool.compare(source)["pairs"][0]
    assert first["ratios"]["full_cz_median"] is None
    assert first["ratios"]["paired_block_compile_time"] is None
    assert first["ratios"]["paired_block_memory_peak"] is None


@pytest.mark.parametrize("fault", ["missing", "duplicate", "free-layout", "reordered"])
def test_incomplete_or_mixed_controls_fail_closed(tool, fault):
    source = summary(tool)
    if fault == "missing":
        source["cases"].pop()
    elif fault == "duplicate":
        source["cases"].append(deepcopy(source["cases"][0]))
    elif fault == "free-layout":
        source["cases"][0]["workflow"] = "cirq-route-cz"
    else:
        source["cases"][0]["blocks"].reverse()
    with pytest.raises(ContractError):
        tool.compare(source)


@pytest.mark.parametrize("profile", ["ordinary", "target-artifact"])
def test_cli_replays_denied_campaign_and_keeps_all_participants(
    tool, monkeypatch, tmp_path, profile
):
    from sdkbench.candidates import provenance
    from sdkbench.p0 import Bundle
    from sdkbench.p0.models import read_json
    from sdkbench.p1a import campaign
    from test_candidate_runner import registration, seal

    def reject(_):
        raise ContractError("Synthetic unavailable installation")

    monkeypatch.setattr(provenance, "verify_runtime", reject)
    bundle = Bundle(ROOT / "docs/implementation")
    workflows = tool.WORKFLOWS if profile == "ordinary" else tool.TARGET_WORKFLOWS
    candidates = {name: registration(name, name) for name in sorted(workflows)}
    root = tmp_path / "campaign"
    campaign.run_campaign(
        bundle,
        directory=root,
        cgroup_parent=tmp_path,
        cpu=0,
        suite="compiler-candidate",
        candidates=candidates,
    )
    seal(root)
    output = tmp_path / "comparisons.json"
    monkeypatch.setattr(
        "sys.argv",
        [
            "compare",
            "--directory",
            str(root),
            "--bundle",
            str(bundle.directory),
            "--output",
            str(output),
            "--profile",
            profile,
        ],
    )
    tool.main()
    result = read_json(output)
    assert result["independent_replay"]["blocks_verified"] == 90
    assert result["case_count"] == 3 and len(result["pairs"]) == 9
    assert set(result["coverage"]) == workflows
    assert result["workflow_profile"] == profile
    assert all(row == {"access-blocked": 3} for row in result["coverage"].values())
    assert all(row["ratios"] is None for row in result["pairs"])
    assert result["publication_eligible"] is False
    with pytest.raises(FileExistsError):
        tool.main()


def test_target_artifact_comparison_discloses_overhead_and_rejects_mixed_profiles(tool):
    source = summary(tool)
    for row in source["cases"]:
        if row["workflow"] == "flagquantum-ordinary-restored":
            row["workflow"] = "flagquantum-target-artifact"
    with pytest.raises(ContractError):
        tool.compare(source)
    result = tool.compare(source, profile="target-artifact")
    assert len(result["pairs"]) == 6
    assert "serialization" in result["comparison_scope"]
    assert "Not a pure compiler timing comparison" in result["comparison_scope"]
    assert set(result["coverage"]) == tool.TARGET_WORKFLOWS
    with pytest.raises(ContractError):
        tool.compare(source, profile="unknown")
