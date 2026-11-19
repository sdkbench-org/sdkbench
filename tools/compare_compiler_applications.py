"""Compare every restored-layout participant without dropping failed cases."""

from __future__ import annotations

import argparse
from collections import Counter
from itertools import combinations
import math
from pathlib import Path
from statistics import median

from compiler_candidate_report import spread, summarize
from sdkbench.p0 import Bundle
from sdkbench.p0.models import canonical_bytes, digest, require

WORKFLOWS = frozenset(
    {
        "flagquantum-ordinary-restored",
        "qiskit-transpile-restored",
        "cirq-route-cz-restored",
    }
)


def _positive_ratio(numerator: float, denominator: float) -> float | None:
    if not (math.isfinite(numerator) and math.isfinite(denominator)):
        return None
    if numerator <= 0 or denominator <= 0:
        return None
    value = numerator / denominator
    return value if math.isfinite(value) else None


def compare(summary: dict) -> dict:
    """Describe all three pairings; failed cases receive no performance ratios."""
    require(summary["publication_eligible"] is False, "Unexpected publication claim")
    by_case = {}
    coverage = {}
    for row in summary["cases"]:
        workflow = row["workflow"]
        require(workflow in WORKFLOWS, "Expected matched-restoration workflows")
        current = by_case.setdefault(row["instance"], {})
        require(workflow not in current, "Duplicate workflow within a case")
        current[workflow] = row
        coverage.setdefault(workflow, Counter())[row["status"]] += 1
    require(by_case, "Empty comparison")
    pairs = []
    for instance, rows in sorted(by_case.items()):
        require(set(rows) == WORKFLOWS, "Missing workflow within a case")
        for first, second in combinations(sorted(WORKFLOWS), 2):
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
    return {
        "schema_version": 1,
        "bundle_sha256": summary["bundle_sha256"],
        "source_summary_sha256": digest(summary),
        "independent_replay": summary["independent_replay"],
        "publication_eligible": False,
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


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--directory", type=Path, required=True)
    parser.add_argument("--bundle", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = compare(summarize(args.directory, Bundle(args.bundle)))
    with args.output.open("xb") as output:
        output.write(canonical_bytes(result))
    print(
        f"Compared {result['case_count']} complete-scope cases; publication_eligible=false"
    )


if __name__ == "__main__":
    main()
