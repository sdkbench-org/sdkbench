"""Compare every restored-layout participant without dropping failed cases."""

from __future__ import annotations

import argparse
import math
from collections import Counter
from itertools import combinations
from pathlib import Path
from statistics import median

from compiler_candidate_report import spread, summarize

from sdkbench.candidates.adapters import ROUTING_POLICY_WORKFLOWS
from sdkbench.candidates.provenance import verify_routing_policy_controls
from sdkbench.candidates.revisions import verify_revision_preparation
from sdkbench.p0 import Bundle, Registration
from sdkbench.p0.models import canonical_bytes, digest, read_json, require

WORKFLOWS = frozenset(
    {
        "flagquantum-ordinary-restored",
        "qiskit-transpile-restored",
        "cirq-route-cz-restored",
    }
)
TARGET_WORKFLOWS = (WORKFLOWS - {"flagquantum-ordinary-restored"}) | {
    "flagquantum-target-artifact"
}


def _positive_ratio(numerator: float, denominator: float) -> float | None:
    if not (math.isfinite(numerator) and math.isfinite(denominator)):
        return None
    if numerator <= 0 or denominator <= 0:
        return None
    value = numerator / denominator
    return value if math.isfinite(value) else None


def compare(summary: dict, *, profile: str = "ordinary", revision_context: dict | None = None) -> dict:
    """Describe every pairing; failed cases receive no performance ratios."""
    require(summary["publication_eligible"] is False, "Unexpected publication claim")
    profiles = {
        "ordinary": WORKFLOWS,
        "target-artifact": TARGET_WORKFLOWS,
        "routing-policies": ROUTING_POLICY_WORKFLOWS,
        "revision-control": None,
    }
    require(profile in profiles, "Unknown workflow profile")
    expected = profiles[profile]
    if profile == "revision-control":
        require(revision_context is not None
                and revision_context["registrations_sha256"] == digest(summary["registrations"])
                and revision_context["bundle_sha256"] == summary["bundle_sha256"],
                "Revision reporting requires the jointly frozen campaign context")
        expected = frozenset(revision_context["stack_ids"])
        require(len(expected) == 2 and expected == set(summary["registrations"]),
                "Revision report stack scope mismatch")
    else:
        require(revision_context is None, "Revision context requires the revision-control profile")
    if profile == "routing-policies":
        verify_routing_policy_controls([
            Registration(**raw) for raw in summary["registrations"].values()
        ])
    scopes = {
        "revision-control": (
            "Two complete revisions of one SDK workflow with matched non-frontend dependencies, "
            "configuration and host facts on one jointly drawn cohort. Whole-revision effects "
            "do not isolate a compiler pass or establish an SDK ranking."
        ),
        "ordinary": "Complete ordinary compiler workflows with restored output layout.",
        "routing-policies": (
            "Matched native routing-policy controls on one compiler revision; ordinary "
            "compilation, native legalization and timed identity restoration are included. "
            "Not an SDK ranking or an isolated router timing comparison."
        ),
        "target-artifact": (
            "Complete target-artifact versus compiler workflows; FlagQuantum includes "
            "target validation, artifact construction and serialization. Not a pure compiler timing comparison."
        ),
    }
    by_case = {}
    coverage = {}
    for row in summary["cases"]:
        workflow = row["workflow"]
        if profile == "revision-control":
            require(workflow == revision_context["workflow"], "Mixed revision workflows")
            workflow = row["sdk"]
        require(
            workflow in expected, "Expected matched-restoration workflows for profile"
        )
        current = by_case.setdefault(row["instance"], {})
        require(workflow not in current, "Duplicate workflow within a case")
        current[workflow] = row
        coverage.setdefault(workflow, Counter())[row["status"]] += 1
    require(by_case, "Empty comparison")
    if profile == "revision-control":
        require(set(by_case) == set(revision_context["instances"]),
                "Revision report does not contain the complete joint cohort")
    pairs = []
    for instance, rows in sorted(by_case.items()):
        require(set(rows) == expected, "Missing workflow within a case")
        for first, second in combinations(sorted(expected), 2):
            left, right = rows[first], rows[second]
            complete = all(
                row["status"] == "accepted"
                and row["accepted_records"] == 30
                and row["expected_records"] == 30
                for row in (left, right)
            )
            result = {
                "instance": instance,
                "numerator_workflow": first,
                "denominator_workflow": second,
                "statuses": {first: left["status"], second: right["status"]},
                "both_complete": complete,
                "ratios": None,
            }
            if profile == "revision-control":
                result.update(numerator_stack=first, denominator_stack=second,
                              numerator_workflow=left["workflow"],
                              denominator_workflow=right["workflow"])
            if complete:
                require(
                    all(
                        [b["block"] for b in row["blocks"]] == list(range(10))
                        for row in (left, right)
                    ),
                    "Incomplete or reordered blocks",
                )
                require(
                    all(
                        b["timing_eligible"] and len(b["compile_wall_seconds"]) == 3
                        for row in (left, right)
                        for b in row["blocks"]
                    ),
                    "Accepted case has ineligible timing blocks",
                )
                timing, memory = [], []
                for a, b in zip(left["blocks"], right["blocks"], strict=True):
                    timing.append(
                        _positive_ratio(
                            median(a["compile_wall_seconds"]),
                            median(b["compile_wall_seconds"]),
                        )
                    )
                    memory.append(
                        _positive_ratio(
                            a["kernel_memory_peak_bytes"], b["kernel_memory_peak_bytes"]
                        )
                        if a["kernel_memory_peak_bytes"] is not None
                        and b["kernel_memory_peak_bytes"] is not None
                        else None
                    )
                result["ratios"] = {
                    "full_cz_median": _positive_ratio(
                        left["full_cz_count_for_accepted_records"]["median"],
                        right["full_cz_count_for_accepted_records"]["median"],
                    ),
                    "dependency_depth_median": _positive_ratio(
                        left["dependency_depth_for_accepted_records"]["median"],
                        right["dependency_depth_for_accepted_records"]["median"],
                    ),
                    "paired_block_compile_time": (
                        spread(timing) if all(v is not None for v in timing) else None
                    ),
                    "paired_block_memory_peak": (
                        spread(memory) if all(v is not None for v in memory) else None
                    ),
                }
            pairs.append(result)
    result = {
        "schema_version": 1,
        "bundle_sha256": summary["bundle_sha256"],
        "source_summary_sha256": digest(summary),
        "independent_replay": summary["independent_replay"],
        "publication_eligible": False,
        "workflow_profile": profile,
        "comparison_scope": scopes[profile],
        "case_count": len(by_case),
        "coverage": {key: dict(value) for key, value in sorted(coverage.items())},
        "pairs": pairs,
        "interpretation": [
            "All participants and all cases remain in the denominator, including failures.",
            "Ratios are numerator divided by denominator; below one means less of that metric.",
            "No ratios are emitted when either full case fails, even if some records passed.",
            "Timing and memory pair the same block index; timing first takes each block's three-run median.",
            "Zero, missing or nonfinite measurements make the corresponding ratio undefined.",
            "Quartiles describe observed variation; they are not confidence intervals or significance tests.",
            "Counts use medians of independently accepted records, not SDK-reported counts.",
            "No across-case aggregate, universal winner or global SDK ranking is inferred.",
        ],
    }
    if revision_context is not None:
        result["joint_revision_control"] = revision_context
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--directory", type=Path, required=True)
    parser.add_argument("--bundle", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--profile", choices=("ordinary", "target-artifact", "routing-policies", "revision-control"), default="ordinary"
    )
    parser.add_argument("--preparation", type=Path,
                        help="Joint freeze/draw/selection directory required for revision control")
    args = parser.parse_args()
    if (args.profile == "revision-control") != (args.preparation is not None):
        parser.error("Provide --preparation exactly when using --profile revision-control")
    bundle = Bundle(args.bundle)
    summary = summarize(args.directory, bundle)
    context = None
    if args.preparation is not None:
        context = verify_revision_preparation(
            args.preparation, bundle, summary["registrations"],
            read_json(args.directory / "interpreters.json"),
            read_json(args.directory / "admission.json"),
        )
    result = compare(
        summary, profile=args.profile, revision_context=context,
    )
    with args.output.open("xb") as output:
        output.write(canonical_bytes(result))
    print(
        f"Compared {result['case_count']} complete-scope cases; publication_eligible=false"
    )


if __name__ == "__main__":
    main()
