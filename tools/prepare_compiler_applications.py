"""Freeze matched-layout registrations, draw once, and retain a reduced cohort.

The draw record documents local event ordering. It is not an independent
attestation, a publication qualification, or a replacement for replay.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import secrets
import subprocess
from datetime import UTC, datetime
from pathlib import Path

from sdkbench.candidates.adapters import ROUTING_POLICY_WORKFLOWS
from sdkbench.candidates.application_bundle import build_bundle
from sdkbench.candidates.environment import admit_interpreter, interpreter_identity
from sdkbench.candidates.provenance import (
    implementation_fingerprint,
    verify_routing_policy_controls,
    verify_runtime,
)
from sdkbench.candidates.revisions import verify_revision_control
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
FAMILIES = ("qaoa", "ising", "hopping", "qft", "repetition")
WIDTHS = (6, 8, 12)
TOPOLOGIES = ("line", "grid")


def _write_new(path: Path, value: object) -> None:
    with path.open("xb") as output:
        output.write(canonical_bytes(value))


def prepare(
    base: Path,
    registrations: list[Path],
    output: Path,
    *,
    profile: str = "ordinary",
    interpreters: dict[str, str] | None = None,
    inventories: dict[str, Path] | None = None,
) -> Bundle:
    """Retain 30 preregistered line/grid cases with unchanged acceptance."""
    profiles = {
        "ordinary": WORKFLOWS,
        "target-artifact": TARGET_WORKFLOWS,
        "routing-policies": ROUTING_POLICY_WORKFLOWS,
        "revision-control": None,
    }
    require(profile in profiles, "Unknown workflow profile")
    expected = profiles[profile]
    admitted = [Registration(**read_json(path)) for path in registrations]
    if output.exists():
        raise FileExistsError(output)
    revision_environments = None
    if profile == "revision-control":
        require(interpreters is not None and inventories is not None
                and set(interpreters) == set(inventories) == {r.stack_id for r in admitted}
                and len(set(interpreters.values())) == 2,
                "Revision controls require complete distinct interpreter and inventory selections")
        observed = {name: read_json(path) for name, path in inventories.items()}
        verify_revision_control(admitted, observed)
        identities = {name: interpreter_identity(python) for name, python in interpreters.items()}
        require(len({identity["executable_sha256"] for identity in identities.values()}) == 1,
                "Revision controls require identical interpreter executable bytes")
        environment = {key: os.environ[key] for key in ("LD_LIBRARY_PATH",) if key in os.environ}
        environment["PYTHONPATH"] = str(Path(__file__).resolve().parents[1] / "src")
        probes = {r.stack_id: admit_interpreter(r, identities[r.stack_id], environment,
                                              inventory=observed[r.stack_id])
                  for r in admitted}
        revision_environments = {"inventories": observed, "interpreters": identities, "probes": probes}
    else:
        require(interpreters is None and inventories is None,
                "Environment selections require the revision-control profile")
        _verify_profile(admitted, expected, profile)
    baseline = Bundle(base)
    output.mkdir(parents=True, exist_ok=False)
    source_root = Path(__file__).resolve().parents[1]
    revision = subprocess.check_output(
        ["git", "rev-parse", "HEAD"],
        cwd=source_root,
        text=True,
        timeout=10,
    ).strip()
    freeze = {
        "schema_version": 1,
        "recorded_at_utc": datetime.now(UTC).isoformat(),
        "harness_revision": revision,
        "harness_sha256": implementation_fingerprint(),
        "preparation_source_sha256": hashlib.sha256(
            Path(__file__).read_bytes()
        ).hexdigest(),
        "base_bundle_sha256": baseline.sha256,
        "workflow_profile": profile,
        "selection": {
            "families": list(FAMILIES),
            "widths": list(WIDTHS),
            "topologies": list(TOPOLOGIES),
            "case_count": 30,
        },
        "execution": "unchanged protocol: ten blocks, two warmups, three measured compilations",
        "campaign_wall_limit_seconds": 16200,
        "workflow_run": {
            key: os.environ.get(key)
            for key in (
                "GITHUB_REPOSITORY",
                "GITHUB_RUN_ID",
                "GITHUB_RUN_ATTEMPT",
                "GITHUB_SHA",
            )
        },
        "registrations": [r.to_dict() for r in admitted],
        "qualification": "local event record; not an independent timestamp or attestation",
    }
    if revision_environments is not None:
        freeze["revision_environments"] = revision_environments
    _write_new(output / "freeze.json", freeze)
    return _draw_cohort(base, output, freeze)


def _verify_profile(admitted: list[Registration], expected: frozenset, profile: str) -> None:
    require(
        len(admitted) == len(expected) and len({r.stack_id for r in admitted}) == len(expected),
        f"Exactly {len(expected)} distinct matched-layout registrations are required",
    )
    require(
        {r.configuration["options"]["workflow"] for r in admitted} == expected,
        "The cohort requires the matched-restoration workflows for its profile",
    )
    if profile == "routing-policies":
        verify_routing_policy_controls(admitted)
    for registration in admitted:
        verify_runtime(registration)


def _draw_cohort(base: Path, output: Path, freeze: dict) -> Bundle:
    # The freeze exists before entropy is requested. Existing directories are
    # refused before this point, so a failed campaign cannot silently redraw.
    nonce = secrets.token_bytes(32).hex()
    _write_new(
        output / "draw.json",
        {
            "schema_version": 1,
            "recorded_at_utc": datetime.now(UTC).isoformat(),
            "freeze_sha256": digest(freeze),
            "nonce": nonce,
            "entropy_source": "secrets.token_bytes(32)",
            "redraw_allowed": False,
        },
    )
    full = build_bundle(base, output / "full-bundle", nonce)
    selected = [
        case
        for case in full.plan["instances"]
        if case["arguments"]["topology"] in TOPOLOGIES
    ]
    require(
        len(selected) == 30
        and {case["arguments"]["family"] for case in selected} == set(FAMILIES)
        and {case["arguments"]["n"] for case in selected} == set(WIDTHS),
        "Unexpected application cohort shape",
    )
    cohort = output / "cohort"
    cohort.mkdir()
    # Preserve every original fixture/reference byte and all resource rules.
    # Only the explicit case selection and its content-addressed identity change.
    names = {"roadmap.json", "candidate-packages.json"} | {
        case[key] for case in selected for key in ("fixture", "reference_artifact")
    }
    for name in sorted(names):
        destination = cohort / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes((full.directory / name).read_bytes())
    plan = dict(full.plan)
    plan["instances"] = selected
    plan["workflows"] = [
        dict(full.plan["workflows"][0], instances=[c["id"] for c in selected])
    ]
    plan["application_selection"] = {
        "full_bundle_sha256": full.sha256,
        "freeze_sha256": digest(freeze),
        "draw_sha256": digest(read_json(output / "draw.json")),
        "topologies": list(TOPOLOGIES),
        "case_count": len(selected),
        "scope": "reduced 30-case matched-layout cohort; not the complete 60-case study",
    }
    (cohort / "roadmap.json").write_bytes(canonical_bytes(plan))
    manifest = dict(full.manifest)
    manifest["files"] = {name: full.manifest["files"][name] for name in sorted(names)}
    manifest["files"]["roadmap.json"] = hashlib.sha256(
        (cohort / "roadmap.json").read_bytes()
    ).hexdigest()
    _write_new(cohort / "artifacts.json", manifest)
    result = Bundle(cohort)
    _write_new(
        output / "selection.json",
        {
            "freeze_sha256": digest(freeze),
            "draw_sha256": digest(read_json(output / "draw.json")),
            "full_bundle_sha256": full.sha256,
            "cohort_bundle_sha256": result.sha256,
            "instances": [case["id"] for case in selected],
        },
    )
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", type=Path, default=Path("docs/implementation"))
    parser.add_argument("--registration", type=Path, action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--profile", choices=("ordinary", "target-artifact", "routing-policies", "revision-control"), default="ordinary"
    )
    parser.add_argument("--interpreter", action="append", metavar="STACK=/ABS/PYTHON")
    parser.add_argument("--inventory", action="append", metavar="STACK=ENVIRONMENT_JSON")
    args = parser.parse_args()
    def selections(values):
        if values is None:
            return None
        result = {}
        for value in values:
            name, separator, path = value.partition("=")
            if not separator or not name or not path or name in result:
                parser.error("Selections require distinct STACK=PATH entries")
            result[name] = path
        return result
    inventories = selections(args.inventory)
    bundle = prepare(args.base, args.registration, args.output, profile=args.profile,
                     interpreters=selections(args.interpreter),
                     inventories=None if inventories is None else {k: Path(v) for k, v in inventories.items()})
    print(
        canonical_bytes(
            {
                "bundle_sha256": bundle.sha256,
                "case_count": len(bundle.cases),
                "publication_eligible": False,
            }
        ).decode(),
        end="",
    )


if __name__ == "__main__":
    main()
