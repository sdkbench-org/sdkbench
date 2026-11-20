"""Audit retained prospective evidence without importing a participant SDK."""

from __future__ import annotations

import importlib.abc
import json
from pathlib import Path
import sys
import time

harness = Path.cwd().resolve()
sys.path.insert(0, str(harness / "tools"))
sys.path.insert(0, str(harness / "src"))


class DenyParticipants(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split(".", 1)[0] in {"flagquantum", "qiskit", "cirq"}:
            raise ImportError("Participant imports are forbidden during audit: " + fullname)
        return None


sys.meta_path.insert(0, DenyParticipants())

from compiler_candidate_report import summarize
from compare_compiler_applications import compare
from sdkbench.candidates.application_bundle import build_bundle
from sdkbench.candidates.provenance import (
    file_sha256,
    implementation_fingerprint,
    verify_build,
)
from sdkbench.p0 import Bundle
from sdkbench.p0.models import canonical_bytes, digest, read_json

assert Path(sys.modules["compiler_candidate_report"].__file__).resolve() == harness / "tools/compiler_candidate_report.py"
assert Path(sys.modules["compare_compiler_applications"].__file__).resolve() == harness / "tools/compare_compiler_applications.py"

root = Path(sys.argv[1]).resolve()
profile = sys.argv[2]
assert profile == "routing-policies"
run = int(sys.argv[3])
started = time.monotonic()
freeze = read_json(root / "preparation/freeze.json")
draw = read_json(root / "preparation/draw.json")
selection = read_json(root / "preparation/selection.json")
cohort = Bundle(root / "preparation/cohort")
full = Bundle(root / "preparation/full-bundle")
baseline = Bundle(harness / "docs/implementation")

assert freeze["harness_revision"] == "9ce37f85bef327603bc64f63eec7e0fddc9436ef"
assert freeze["harness_sha256"] == implementation_fingerprint()
assert freeze["preparation_source_sha256"] == file_sha256(harness / "tools/prepare_compiler_applications.py")
assert freeze["base_bundle_sha256"] == baseline.sha256
assert freeze["workflow_profile"] == profile
assert freeze["workflow_run"]["GITHUB_RUN_ID"] == str(run)
assert freeze["workflow_run"]["GITHUB_RUN_ATTEMPT"] == "1"
assert freeze["workflow_run"]["GITHUB_SHA"] == freeze["harness_revision"]
assert freeze["recorded_at_utc"] <= draw["recorded_at_utc"]
assert freeze["campaign_wall_limit_seconds"] == 16200
assert draw["freeze_sha256"] == digest(freeze)
assert draw["entropy_source"] == "secrets.token_bytes(32)"
assert draw["redraw_allowed"] is False
assert len(bytes.fromhex(draw["nonce"])) == 32
assert selection["freeze_sha256"] == digest(freeze)
assert selection["draw_sha256"] == digest(draw)
assert selection["full_bundle_sha256"] == full.sha256
assert selection["cohort_bundle_sha256"] == cohort.sha256
assert set(selection["instances"]) == set(cohort.cases)
assert len(cohort.cases) == 30 and len(full.cases) == 60

for identifier, case in cohort.cases.items():
    assert case == full.cases[identifier]
    for key in ("fixture", "reference_artifact"):
        assert (cohort.directory / case[key]).read_bytes() == (full.directory / case[key]).read_bytes()
    template = next(c for c in baseline.cases.values()
                    if c["workflow"] == "W03" and c["arguments"]["n"] == case["arguments"]["n"])
    generated_fields = {"id", "arguments", "fixture", "reference_artifact", "state"}
    assert {k: v for k, v in case.items() if k not in generated_fields} == {
        k: v for k, v in template.items() if k not in generated_fields
    }

build = verify_build(root / "flagquantum-build")
assert build["source_commit"] == "858df9dbd5ba964e8e59b3383304547710a1dee5"
assert build["build_tool_sha256"] == file_sha256(harness / "tools/build_compiler_candidate.py")
registrations = read_json(root / "campaign/registrations.json")
assert {r["stack_id"]: r for r in freeze["registrations"]} == registrations
assert len(registrations) == 4
assert all(r["configuration"]["options"]["source_build"] == build for r in registrations.values())

for sdk, distribution, version in (("qiskit", "qiskit", "2.6.2"), ("cirq", "cirq-core", "1.7.0")):
    release = read_json(root / "releases" / (distribution + ".json"))
    assert release["info"]["version"] == version
    wheels = [p for p in (root / "releases").glob("*.whl")
              if p.name.startswith(distribution.replace("-", "_") + "-")]
    assert len(wheels) == 1
    wheel = wheels[0]
    metadata = next(item for item in release["urls"] if item["filename"] == wheel.name)
    assert metadata["digests"]["sha256"] == file_sha256(wheel)
    assert metadata["size"] == wheel.stat().st_size and metadata["yanked"] is False

regeneration = root.parent / "audit-regenerated-full"
regenerated = (Bundle(regeneration) if regeneration.exists() else
               build_bundle(harness / "docs/implementation", regeneration, draw["nonce"]))
assert regenerated.sha256 == full.sha256
print(json.dumps({"phase": "provenance_verified", "profile": profile, "seconds": time.monotonic() - started}), flush=True)

summary = summarize(root / "campaign", cohort)
assert summary["independent_replay"]["blocks_verified"] == 1200
assert len(summary["cases"]) == 120
assert sum(row["expected_records"] for row in summary["cases"]) == 3600
assert summary["independent_replay"] == read_json(root / "independent-replay.json")
with (root.parent / "local-summary.json").open("xb") as stream:
    stream.write(canonical_bytes(summary))
comparison = compare(summary, profile=profile)
assert comparison["case_count"] == 30 and len(comparison["pairs"]) == 180
assert len(comparison["coverage"]) == 4
hosted_comparison = read_json(root / "comparisons.json")
for key in ("coverage", "pairs", "case_count", "workflow_profile", "bundle_sha256", "independent_replay"):
    assert comparison[key] == hosted_comparison[key], "Hosted/local comparison differs: " + key

for name, value in (("local-comparisons.json", comparison),):
    with (root.parent / name).open("xb") as stream:
        stream.write(canonical_bytes(value))
verification = {
    "schema_version": 1,
    "profile": profile,
    "run_id": run,
    "participant_imports_denied": ["flagquantum", "qiskit", "cirq"],
    "harness_revision": freeze["harness_revision"],
    "compiler_revision": build["source_commit"],
    "build_files_hash_verified": True,
    "published_wheels_hash_verified": True,
    "freeze_draw_selection_verified": True,
    "retained_nonce_regeneration_matches": True,
    "independent_replay_matches_hosted": True,
    "all_pair_metrics_and_coverage_match_hosted": True,
    "summary_digest_matches_hosted": digest(summary) == hosted_comparison["source_summary_sha256"],
    "blocks_verified": 1200,
    "case_participant_pairs": 120,
    "measured_records_expected": 3600,
    "measured_records_retained": sum(
        sum(row["measured_record_statuses"].values()) for row in summary["cases"]
    ),
    "measured_records_accepted": sum(row["accepted_records"] for row in summary["cases"]),
    "warmup_records_expected": 2400,
    "warmup_records_retained": sum(
        len(read_json(path)["warmups"])
        for path in (root / "campaign").glob("*/*/block-*/response.json")
    ),
    "report_helper_paths_verified": True,
    "elapsed_seconds": time.monotonic() - started,
    "publication_eligible": False,
}
with (root.parent / "local-verification.json").open("xb") as stream:
    stream.write(canonical_bytes(verification))
print(json.dumps(verification), flush=True)
