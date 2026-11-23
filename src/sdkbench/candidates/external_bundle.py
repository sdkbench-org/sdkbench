"""Supervise external source admission and build a common unchanged-W03 bundle."""

from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import re
import sys

from ..p0.bundle import Bundle
from ..p0.models import ContractError, canonical_bytes, digest, read_json, require
from ..p0.supervisor import IsolationUnavailable, Limits, run_command
from .application_bundle import _write
from .external_qasm import convert_source


def _verified_source(root: Path, relative: str, size: int, blob: str) -> bytes:
    path = (root / relative).resolve()
    require(path.is_relative_to(root), "External source path leaves its root")
    require(
        path.stat().st_size == size and 0 < size <= 1 << 20,
        "External source size differs or exceeds preparation bound",
    )
    raw = path.read_bytes()
    actual = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
    require(actual == blob, "External source Git blob differs")
    return raw


def _edges(n: int, topology: str) -> list[list[int]]:
    if topology == "line":
        return [[q, q + 1] for q in range(n - 1)]
    columns = n // 2
    return [[q, q + 1] for q in range(n - 1) if q != columns - 1] + [
        [q, q + columns] for q in range(columns)
    ]


def prepare(
    base: Path,
    population_path: Path,
    source_root: Path,
    output: Path,
    *,
    cpu: int,
    cgroup_parent: Path,
) -> dict:
    """Retain every input decision under a 300-second/16-GiB source supervisor.

    This prepares inputs only. It does not admit a host, prove novelty, freeze an
    execution study or run any participant. Output must not exist, including for
    a failed preparation. Source/notice identities come from the prior census.
    """
    baseline = Bundle(base)
    population = read_json(population_path)
    templates = {
        baseline.fixtures[key]["n_qubits"]: case
        for key, case in baseline.cases.items()
        if case["workflow"] == "W03"
    }
    require(set(templates) == {6, 8, 12}, "Frozen W03 widths are required")
    rows = population["files"]
    require(
        rows and len({r["path"] for r in rows}) == len(rows),
        "External source census must be nonempty and unique",
    )
    require(
        population["topologies"] == ["line", "2-by-n/2-grid"],
        "External targets differ from the declared census",
    )
    root = source_root.resolve()
    notices = {}
    for name in ("LICENSE", "NOTICE"):
        path = (root / name).resolve()
        require(
            path.is_relative_to(root) and path.stat().st_size <= 1 << 20,
            "External notice leaves source root or exceeds bound",
        )
        raw = path.read_bytes()
        require(
            hashlib.sha256(raw).hexdigest() == population["licenses"][name]["sha256"],
            "External license/notice differs from declaration",
        )
        notices[name] = raw
    output.mkdir(parents=True, exist_ok=False)
    (output / "population.json").write_bytes(population_path.read_bytes())
    for name, raw in notices.items():
        (output / name).write_bytes(raw)
    limits = Limits(300, 16 * 1024**3, cpu)
    evidence, cases, fixtures = [], [], {}
    source_path = str(Path(__file__).resolve().parents[2])
    for index, row in enumerate(rows):
        entry = {"source": row, "status": "input-not-admitted"}
        evidence.append(entry)
        directory = output / f"source-{index:02d}"
        directory.mkdir()
        try:
            match = re.search(r"_n(6|8|12)\.qasm$", row["path"])
            require(match is not None, "Source width is outside declared population")
            n = int(match[1])
            raw = _verified_source(root, row["path"], row["bytes"], row["git_blob"])
            (directory / "original.qasm").write_bytes(raw)
            template = templates[n]
            fixture = baseline.fixtures[template["id"]]
            request = {
                "source": raw.decode("utf-8"),
                "probe_preparations": fixture["probe_preparations"],
            }
            _write(directory / "request.json", request)
            observed = run_command(
                [
                    sys.executable,
                    "-m",
                    "sdkbench.candidates.external_bundle",
                    "--worker",
                    "request.json",
                ],
                cwd=directory,
                cgroup_parent=cgroup_parent,
                limits=limits,
                environment={"PYTHONPATH": source_path},
            )
            _write(directory / "supervisor.json", observed)
            require(
                observed["execution_status"] == "completed",
                "Source preparation did not complete: " + observed["execution_status"],
            )
            result = json.loads(observed["stdout"])
            _write(directory / "conversion.json", result)
            require(
                result["status"] == "converted",
                result.get("reason", "Conversion refused"),
            )
            converted = result["prepared"]
            require(
                converted["n_qubits"] == n
                and converted["source_sha256"] == hashlib.sha256(raw).hexdigest(),
                "Source conversion identity differs",
            )
            require(
                isinstance(converted.get("operations"), list)
                and len(converted["operations"]) <= 20000,
                "Source conversion operation list is missing or oversized",
            )
            for topology in ("line", "grid"):
                case_id = f"EXT-{index:02d}-{topology.upper()}-{n:02d}"
                value = deepcopy(fixture)
                value.update(
                    operations=converted["operations"], target_edges=_edges(n, topology)
                )
                case = deepcopy(template)
                case.update(
                    id=case_id,
                    arguments={
                        "n": n,
                        "topology": topology,
                        "external_source": row["path"],
                    },
                    fixture=f"fixtures/{case_id}.json",
                    reference_artifact=f"references/{case_id}.json",
                    state="external-source-development-input",
                )
                cases.append(case)
                fixtures[case_id] = value
            entry.update(
                status="input-admitted",
                source_sha256=converted["source_sha256"],
                conversion_sha256=digest(result),
            )
        except (
            ContractError,
            IsolationUnavailable,
            OSError,
            UnicodeError,
            ValueError,
            KeyError,
        ) as error:
            # Input/process boundary: retain the refusal without inventing SDK outcomes.
            entry["reason"] = f"{type(error).__name__}: {error}"
        _write(output / "preparation.json", {"inputs": evidence, "complete": False})
    plan = deepcopy(baseline.plan)
    plan.update(
        protocol_id="sdkbench-compiler-external-programs",
        protocol_revision="external-v1-" + digest(population),
        status="Development input preparation; execution freeze and novelty audit pending",
        instances=cases,
        workflows=[
            {
                **deepcopy(next(w for w in plan["workflows"] if w["id"] == "W03")),
                "instances": [c["id"] for c in cases],
            }
        ],
    )
    bundle_dir = output / "bundle"
    bundle_dir.mkdir()
    _write(bundle_dir / "roadmap.json", plan)
    (bundle_dir / "candidate-packages.json").write_bytes(
        (baseline.directory / "candidate-packages.json").read_bytes()
    )
    files = ["roadmap.json", "candidate-packages.json"]
    for case in cases:
        _write(bundle_dir / case["fixture"], fixtures[case["id"]])
        _write(
            bundle_dir / case["reference_artifact"],
            {
                "method": "Unchanged W03 evaluator recomputes coherent operators/states from the common fixture",
                "source_conformance": "Retained separately; not a compiled-output verdict",
            },
        )
        files.extend((case["fixture"], case["reference_artifact"]))
    _write(
        bundle_dir / "artifacts.json",
        {
            "protocol_revision": plan["protocol_revision"],
            "files": {
                name: hashlib.sha256((bundle_dir / name).read_bytes()).hexdigest()
                for name in sorted(files)
            },
        },
    )
    bundle = Bundle(bundle_dir)
    intended = [
        {
            "source": row["path"],
            "topology": topology,
            "workflow": workflow,
            "input_status": entry["status"],
            "participant_execution": "not-started",
        }
        for row, entry in zip(rows, evidence)
        for topology in population["topologies"]
        for workflow in population["participants"]
    ]
    summary = {
        "complete": True,
        "inputs": evidence,
        "intended_outcomes": intended,
        "bundle_sha256": bundle.sha256,
        "admitted_instances": len(cases),
        "base_bundle_sha256": baseline.sha256,
        "population_sha256": digest(population),
        "source_limits": {"wall_seconds": 300, "memory_bytes": 16 * 1024**3},
        "builder_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "converter_sha256": hashlib.sha256(
            Path(sys.modules[convert_source.__module__].__file__).read_bytes()
        ).hexdigest(),
        "publication_eligible": False,
    }
    _write(output / "preparation.json", summary)
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--worker", type=Path)
    parser.add_argument("--base", type=Path)
    parser.add_argument("--population", type=Path)
    parser.add_argument("--sources", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--cpu", type=int)
    parser.add_argument("--cgroup-parent", type=Path)
    args = parser.parse_args()
    if args.worker is not None:
        request = read_json(args.worker)
        try:
            prepared = convert_source(
                request["source"], probe_preparations=request["probe_preparations"]
            )
            response = {"status": "converted", "prepared": prepared}
        except ContractError as error:
            response = {"status": "refused", "reason": str(error)}
        print(canonical_bytes(response).decode())
        return
    require(
        all(
            value is not None
            for value in (
                args.base,
                args.population,
                args.sources,
                args.output,
                args.cpu,
                args.cgroup_parent,
            )
        ),
        "Preparation requires base, population, sources, output, CPU and delegated cgroup",
    )
    result = prepare(
        args.base,
        args.population,
        args.sources,
        args.output,
        cpu=args.cpu,
        cgroup_parent=args.cgroup_parent,
    )
    print(canonical_bytes(result).decode())


if __name__ == "__main__":
    main()
