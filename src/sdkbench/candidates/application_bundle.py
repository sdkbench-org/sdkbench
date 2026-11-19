"""Construct a new application bundle without modifying the frozen P0 bundle."""

from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path

from ..p0.bundle import Bundle
from ..p0.semantics import propagate
from . import applications


def _write(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )


def build_bundle(base: Path, output: Path, nonce: str) -> Bundle:
    """Create all 60 application cases under the existing W03 acceptance.

    Output must not exist. This builder records development status; prospectivity
    needs an independently frozen candidate selection and nonce draw record.
    """
    applications.Draw(nonce, "validation")
    baseline = Bundle(base)
    templates = {
        baseline.fixtures[key]["n_qubits"]: case
        for key, case in baseline.cases.items()
        if case["workflow"] == "W03"
    }
    if set(templates) != set(applications.WIDTHS):
        raise ValueError("Base bundle must contain exactly the frozen W03 widths")
    output.mkdir(parents=True, exist_ok=False)
    cases = []
    files = ["roadmap.json", "candidate-packages.json"]
    for n in applications.WIDTHS:
        for family in applications.FAMILIES:
            for topology in applications.TOPOLOGIES:
                case_id = f"APP-{family.upper()}-{topology.upper()}-{n:02d}"
                fixture = applications.fixture(n, family, topology, nonce)
                # Hashes audit exported fixtures; acceptance recomputes operators
                # or output states and never compares rounded state digests.
                probes = []
                for preparation in fixture["probe_preparations"]:
                    initial = propagate(n, preparation)
                    state = propagate(n, fixture["operations"], initial)
                    representation = [
                        [round(float(v.real), 11), round(float(v.imag), 11)]
                        for v in state
                    ]
                    probes.append(
                        hashlib.sha256(
                            json.dumps(representation, separators=(",", ":")).encode()
                        ).hexdigest()
                    )
                reference = {
                    "method": "SDK-independent state propagation; application physics anchors tested separately",
                    "probe_state_audit_sha256": probes,
                    "digest_role": "artifact audit only, never a floating-point acceptance test",
                }
                case = deepcopy(templates[n])
                case.update(
                    id=case_id,
                    arguments={"n": n, "family": family, "topology": topology},
                    fixture=f"fixtures/{case_id}.json",
                    reference_artifact=f"references/{case_id}.json",
                    state="generated-development-application",
                )
                for key, payload in (
                    ("fixture", fixture),
                    ("reference_artifact", reference),
                ):
                    _write(output / case[key], payload)
                    files.append(case[key])
                cases.append(case)
    plan = deepcopy(baseline.plan)
    generator_path = Path(applications.__file__)
    plan.update(
        protocol_id="sdkbench-compiler-applications",
        protocol_revision="applications-v1-" + nonce,
        status="Generated development corpus; prospective qualification requires a prior immutable selection and nonce record",
        instances=cases,
        workflows=[
            {
                **deepcopy(next(w for w in plan["workflows"] if w["id"] == "W03")),
                "instances": [case["id"] for case in cases],
            }
        ],
        application_generation={
            "nonce": nonce,
            "recipe_source_sha256": hashlib.sha256(
                generator_path.read_bytes()
            ).hexdigest(),
            "builder_source_sha256": hashlib.sha256(
                Path(__file__).read_bytes()
            ).hexdigest(),
            "base_bundle_sha256": baseline.sha256,
            "case_count": len(cases),
            "evidence_class": "development",
            "physics_scope": "numeric coherent circuits; no algorithmic advantage, chemistry accuracy or QEC threshold claim",
        },
    )
    _write(output / "roadmap.json", plan)
    (output / "candidate-packages.json").write_bytes(
        (baseline.directory / "candidate-packages.json").read_bytes()
    )
    _write(
        output / "artifacts.json",
        {
            "protocol_revision": plan["protocol_revision"],
            "files": {
                name: hashlib.sha256((output / name).read_bytes()).hexdigest()
                for name in sorted(files)
            },
        },
    )
    return Bundle(output)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--nonce", required=True)
    args = parser.parse_args()
    bundle = build_bundle(args.base, args.output, args.nonce)
    print(
        json.dumps(
            {
                "bundle_sha256": bundle.sha256,
                "cases": len(bundle.cases),
                "evidence_class": "development",
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
