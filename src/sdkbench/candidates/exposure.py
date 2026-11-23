"""Audit exact prior exposure without equating an absent match with novelty."""

from __future__ import annotations

import argparse
import hashlib
import math
import os
from pathlib import Path
from typing import Iterator

from ..p0.models import ContractError, canonical_bytes, digest, read_json, require

_MAX_BYTES = 32 * 1024 * 1024
_GATES = {
    "h": 1,
    "x": 1,
    "y": 1,
    "z": 1,
    "s": 1,
    "sdg": 1,
    "rx": 1,
    "ry": 1,
    "rz": 1,
    "cx": 2,
    "cz": 2,
    "swap": 2,
    "rzz": 2,
}


def operation_fingerprint(width: object, operations: object) -> str:
    """Hash ordered numeric operations, retaining idle wires and operand order.

    This is an exact representation comparison, not an equivalence test. The
    accepted numeric IR spelling is normalized to the existing fixture spelling.
    No gate cancellation, angle wrapping, synthesis or compiler is invoked.
    """
    require(type(width) is int and width > 0, "Invalid operation width")
    require(isinstance(operations, list), "Expected an operation list")
    normalized = []
    for item in operations:
        require(isinstance(item, dict), "Expected an operation object")
        if "opcode" in item:
            require(
                set(item) <= {"opcode", "wires", "params", "matrix", "metadata"},
                "Unknown IR operation fields",
            )
            require(
                item.get("matrix") is None and not item.get("metadata"),
                "Annotated or matrix IR operation is not canonicalized",
            )
            name, wires = item.get("opcode"), item.get("wires")
            require(isinstance(name, str), "Unsupported operation name")
            params = item.get("params", {})
            require(isinstance(params, dict), "Expected parameter object")
            require(
                set(params)
                == ({"theta"} if name in {"rx", "ry", "rz", "rzz"} else set()),
                "Unsupported IR parameters",
            )
            angle = params.get("theta")
        else:
            require(
                set(item) <= {"name", "qubits", "angle"},
                "Unknown fixture operation fields",
            )
            name, wires, angle = item.get("name"), item.get("qubits"), item.get("angle")
        require(isinstance(name, str) and name in _GATES, "Unsupported operation name")
        require(
            isinstance(wires, list)
            and len(wires) == _GATES[name]
            and all(type(q) is int and 0 <= q < width for q in wires)
            and len(set(wires)) == len(wires),
            "Invalid ordered operands",
        )
        value = {"name": name, "qubits": wires}
        if name in {"rx", "ry", "rz", "rzz"}:
            require(type(angle) in (int, float), "Invalid angle")
            try:
                numeric_angle = float(angle)
            except OverflowError as error:
                raise ContractError("Invalid angle") from error
            require(math.isfinite(numeric_angle), "Invalid angle")
            value["angle"] = numeric_angle
        else:
            require(angle is None, "Unexpected angle")
        normalized.append(value)
    return digest({"n_qubits": width, "operations": normalized})


def _objects(value: object, location: str = "$") -> Iterator[tuple[str, dict]]:
    if isinstance(value, dict):
        yield location, value
        for key, child in value.items():
            yield from _objects(child, f"{location}/{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from _objects(child, f"{location}/{index}")


def _inspect_json(path: Path) -> tuple[list[dict], list[dict]]:
    fingerprints, gaps = [], []
    try:
        value = read_json(path, max_bytes=_MAX_BYTES)
        for location, obj in _objects(value):
            if "operations" in obj and "n_qubits" in obj:
                width, operations = obj["n_qubits"], obj["operations"]
            elif obj.get("kind") == "flagquantum.circuit_ir":
                width, operations = obj.get("n_wires"), obj.get("instructions")
            else:
                continue
            try:
                fingerprints.append(
                    {
                        "location": location,
                        "sha256": operation_fingerprint(width, operations),
                    }
                )
            except (ContractError, KeyError) as error:
                gaps.append({"location": location, "reason": str(error)})
    except (ContractError, OSError, RecursionError) as error:
        gaps.append({"location": "$", "reason": str(error)})
    return fingerprints, gaps


def audit(preparation: Path, histories: list[Path]) -> dict:
    """Compare every prepared source against explicit historical file trees.

    Historical archives must be extracted beforehand and their archive hashes
    retained by the operator. Missing roots, symlinks and noncanonical material
    are explicit gaps; raw QASM is compared byte-for-byte only. This audit never
    certifies an unseen algorithm or undisclosed developer knowledge.
    """
    summary = read_json(preparation / "preparation.json")
    require(summary.get("complete") is True, "Preparation must be complete")
    require(histories, "At least one explicit historical root is required")
    targets, gaps = [], []
    for index, entry in enumerate(summary["inputs"]):
        directory = preparation / f"source-{index:02d}"
        raw = directory / "original.qasm"
        content = None
        if raw.is_file():
            with raw.open("rb") as stream:
                content = stream.read(1024 * 1024 + 1)
            require(len(content) <= 1024 * 1024, "Prepared source exceeds byte limit")
            declared = entry["source"]
            require(
                len(content) == declared["bytes"]
                and hashlib.sha1(
                    b"blob " + str(len(content)).encode() + b"\0" + content
                ).hexdigest()
                == declared["git_blob"],
                "Prepared source identity differs",
            )
        else:
            gaps.append(
                {
                    "source": entry["source"]["path"],
                    "reason": "Original source unavailable",
                }
            )
        target = {
            "source": entry["source"]["path"],
            "input_status": entry["status"],
            "raw_sha256": (
                hashlib.sha256(content).hexdigest() if content is not None else None
            ),
            "operation_sha256": None,
            "matches": [],
        }
        if entry["status"] == "input-admitted":
            conversion = read_json(directory / "conversion.json")
            require(
                digest(conversion) == entry["conversion_sha256"],
                "Prepared conversion identity differs",
            )
            converted = conversion["prepared"]
            require(
                converted["source_sha256"] == target["raw_sha256"],
                "Converted source identity differs",
            )
            target["operation_sha256"] = operation_fingerprint(
                converted["n_qubits"], converted["operations"]
            )
        targets.append(target)
    inventory = []
    resolved_preparation = preparation.resolve()
    for index, supplied in enumerate(histories):
        root = supplied.resolve()
        require(
            not root.is_relative_to(resolved_preparation)
            and not resolved_preparation.is_relative_to(root),
            "Historical roots must not overlap this preparation",
        )
        if not root.is_dir():
            gaps.append(
                {"root": index, "path": ".", "reason": "Historical root unavailable"}
            )
            continue
        # Ignore only Git's object database; tracked source and retained evidence
        # must be supplied explicitly, including extracted historical archives.
        paths = []

        def walk_error(error: OSError) -> None:
            gaps.append(
                {"root": index, "path": str(error.filename), "reason": str(error)}
            )

        for directory, children, files in os.walk(
            root, followlinks=False, onerror=walk_error
        ):
            children[:] = sorted(name for name in children if name != ".git")
            paths.extend(
                Path(directory) / name
                for name in children
                if (Path(directory) / name).is_symlink()
            )
            paths.extend(Path(directory) / name for name in files)
        for path in sorted(paths):
            relative = path.relative_to(root)
            if ".git" in relative.parts:
                continue
            if path.is_symlink():
                gaps.append(
                    {
                        "root": index,
                        "path": relative.as_posix(),
                        "reason": "Symlink not followed",
                    }
                )
                continue
            if not path.is_file():
                continue
            name = relative.as_posix()
            try:
                with path.open("rb") as stream:
                    content = stream.read(_MAX_BYTES + 1)
                size = len(content)
                require(size <= _MAX_BYTES, "File exceeds audit byte limit")
                raw_hash = hashlib.sha256(content).hexdigest()
                operations, file_gaps = (
                    _inspect_json(path) if path.suffix == ".json" else ([], [])
                )
            except (OSError, ContractError) as error:
                gaps.append({"root": index, "path": name, "reason": str(error)})
                continue
            inventory.append(
                {
                    "root": index,
                    "path": name,
                    "bytes": size,
                    "sha256": raw_hash,
                    "operations": operations,
                }
            )
            gaps.extend({"root": index, "path": name, **gap} for gap in file_gaps)
            if path.suffix.lower() in {".qasm", ".gz", ".zip", ".tar", ".xz", ".bz2"}:
                gaps.append(
                    {
                        "root": index,
                        "path": name,
                        "reason": "Raw bytes compared; canonical content not audited",
                    }
                )
            for target in targets:
                if raw_hash == target["raw_sha256"]:
                    target["matches"].append(
                        {"root": index, "path": name, "kind": "raw-source"}
                    )
                for value in operations:
                    if value["sha256"] == target["operation_sha256"]:
                        target["matches"].append(
                            {
                                "root": index,
                                "path": name,
                                "kind": "ordered-operations",
                                "location": value["location"],
                            }
                        )
    for target in targets:
        target["exposure_status"] = (
            "known-match" if target["matches"] else "no-exact-match-in-audited-material"
        )
    return {
        "schema_version": 1,
        "scope": "Exact prior-exposure audit; absence of a match is not proof of novelty",
        "historical_roots": [str(p.resolve()) for p in histories],
        "preparation_sha256": digest(summary),
        "targets": targets,
        "inventory": inventory,
        "gaps": gaps,
        "novelty_certified": False,
        "coverage": "Only recognized JSON objects are compared canonically. Embedded JSON strings, code, logs, notebooks, JSONL and other formats receive whole-file raw-byte comparison only; embedded source text is not detected.",
        "comparison": "Ordered gates, numeric angles and operand order; no algebraic equivalence, algorithm-family or code-history inference",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preparation", type=Path, required=True)
    parser.add_argument("--history", type=Path, action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = audit(args.preparation, args.history)
    with args.output.open("xb") as output:
        output.write(canonical_bytes(result))


if __name__ == "__main__":
    main()
