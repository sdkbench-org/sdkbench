"""Prior exposure detection uses synthetic data and retains audit limitations."""

import hashlib
import json

import pytest

from sdkbench.candidates.exposure import audit, operation_fingerprint
from sdkbench.p0.models import ContractError, digest

OPS = [{"name": "rx", "qubits": [0], "angle": 1}, {"name": "cx", "qubits": [0, 1]}]


def preparation(tmp_path):
    root = tmp_path / "preparation"
    directory = root / "source-00"
    directory.mkdir(parents=True)
    raw = b"OPENQASM 2.0; qreg q[6];"
    (directory / "original.qasm").write_bytes(raw)
    conversion = {
        "status": "converted",
        "prepared": {
            "source_sha256": hashlib.sha256(raw).hexdigest(),
            "n_qubits": 6,
            "operations": OPS,
        },
    }
    (directory / "conversion.json").write_text(json.dumps(conversion))
    manifest = {
        "complete": True,
        "inputs": [
            {
                "source": {
                    "path": "synthetic_n6.qasm",
                    "bytes": len(raw),
                    "git_blob": hashlib.sha1(
                        b"blob " + str(len(raw)).encode() + b"\0" + raw
                    ).hexdigest(),
                },
                "status": "input-admitted",
                "conversion_sha256": digest(conversion),
            }
        ],
    }
    (root / "preparation.json").write_text(json.dumps(manifest))
    return root, raw


def test_detects_raw_and_nested_canonical_match(tmp_path):
    root, raw = preparation(tmp_path)
    history = tmp_path / "history"
    history.mkdir()
    (history / "source.qasm").write_bytes(raw)
    (history / "fixture.json").write_text(
        json.dumps({"fixture": {"n_qubits": 6, "operations": OPS}})
    )
    result = audit(root, [history])
    target = result["targets"][0]
    assert target["exposure_status"] == "known-match"
    assert {x["kind"] for x in target["matches"]} == {
        "raw-source",
        "ordered-operations",
    }
    assert (
        result["gaps"][0]["reason"]
        == "Raw bytes compared; canonical content not audited"
    )
    assert result["novelty_certified"] is False


def test_ir_and_fixture_spelling_match_but_wire_order_and_width_do_not():
    ir = [
        {
            "opcode": "rx",
            "wires": [0],
            "params": {"theta": 1.0},
            "matrix": None,
            "metadata": {},
        },
        {"opcode": "cx", "wires": [0, 1], "params": {}, "metadata": {}},
    ]
    expected = operation_fingerprint(6, OPS)
    assert operation_fingerprint(6, ir) == expected
    assert operation_fingerprint(8, OPS) != expected
    assert (
        operation_fingerprint(6, [OPS[0], {"name": "cx", "qubits": [1, 0]}]) != expected
    )
    assert operation_fingerprint(6, list(reversed(OPS))) != expected


@pytest.mark.parametrize(
    "operation",
    [
        {"name": "rx", "qubits": [0], "angle": float("nan")},
        {"name": "rx", "qubits": [0], "angle": 10**400},
        {"name": "cx", "qubits": [0, 0]},
        {"name": "cx", "qubits": [0, 6]},
        {"name": "rx", "qubits": [True], "angle": 1},
        {"name": "unknown", "qubits": [0]},
        {"opcode": [], "wires": [0]},
        {"opcode": "x"},
        {"qubits": [0]},
        {"name": "x", "qubits": [0], "angle": 1},
        {"name": "x", "qubits": [0], "metadata": {"condition": 1}},
        {"opcode": "rx", "wires": [0], "params": {"theta": {"$parameter": "x"}}},
        {"opcode": "x", "wires": [0], "metadata": {"condition": 1}},
    ],
)
def test_noncanonical_operations_refused(operation):
    with pytest.raises(ContractError):
        operation_fingerprint(6, [operation])


def test_missing_root_and_malformed_json_cannot_certify_novelty(tmp_path):
    root, _ = preparation(tmp_path)
    history = tmp_path / "history"
    history.mkdir()
    (history / "broken.json").write_text('{"a":1,"a":2}')
    (history / "symbolic.json").write_text(
        json.dumps(
            {
                "n_qubits": 6,
                "operations": [{"name": "rx", "qubits": [0], "angle": "theta"}],
            }
        )
    )
    (history / "archive.tar.gz").write_bytes(b"not extracted")
    result = audit(root, [history, tmp_path / "missing"])
    assert (
        result["targets"][0]["exposure_status"] == "no-exact-match-in-audited-material"
    )
    assert len(result["gaps"]) == 4
    assert result["novelty_certified"] is False


@pytest.mark.parametrize("mutation", ["source", "conversion", "incomplete"])
def test_tampered_preparation_is_rejected(tmp_path, mutation):
    root, _ = preparation(tmp_path)
    if mutation == "source":
        (root / "source-00/original.qasm").write_bytes(b"changed")
    elif mutation == "conversion":
        (root / "source-00/conversion.json").write_text("{}")
    else:
        (root / "preparation.json").write_text('{"complete":false}')
    with pytest.raises(ContractError):
        audit(root, [tmp_path / "history"])


def test_overlap_rejected_and_symlinks_reported(tmp_path):
    root, _ = preparation(tmp_path)
    with pytest.raises(ContractError, match="overlap"):
        audit(root, [tmp_path])
    history = tmp_path / "history"
    history.mkdir()
    (history / "alias").symlink_to(root, target_is_directory=True)
    (history / ".git").mkdir()
    (history / ".git/object").write_bytes(b"excluded object database")
    result = audit(root, [history])
    assert not result["inventory"]
    assert result["gaps"] == [
        {"root": 0, "path": "alias", "reason": "Symlink not followed"}
    ]


def test_cli_retains_report_and_refuses_overwrite(tmp_path, monkeypatch):
    from sdkbench.candidates.exposure import main

    root, _ = preparation(tmp_path)
    history = tmp_path / "history"
    history.mkdir()
    output = tmp_path / "audit.json"
    monkeypatch.setattr(
        "sys.argv",
        [
            "exposure",
            "--preparation",
            str(root),
            "--history",
            str(history),
            "--output",
            str(output),
        ],
    )
    main()
    value = json.loads(output.read_text())
    assert value["novelty_certified"] is False
    assert "Embedded JSON strings" in value["coverage"]
    retained = output.read_bytes()
    with pytest.raises(FileExistsError):
        main()
    assert output.read_bytes() == retained


def test_walk_permission_failure_is_a_coverage_gap(tmp_path, monkeypatch):
    root, _ = preparation(tmp_path)
    history = tmp_path / "history"
    history.mkdir()

    def denied_walk(path, *, followlinks, onerror):
        onerror(PermissionError(13, "Permission denied", str(path / "private")))
        return iter(())

    monkeypatch.setattr("sdkbench.candidates.exposure.os.walk", denied_walk)
    result = audit(root, [history])
    assert len(result["gaps"]) == 1
    assert "Permission denied" in result["gaps"][0]["reason"]
    assert result["novelty_certified"] is False


def test_missing_refused_source_remains_a_coverage_gap(tmp_path):
    root, _ = preparation(tmp_path)
    manifest = json.loads((root / "preparation.json").read_text())
    manifest["inputs"][0]["status"] = "input-refused"
    (root / "preparation.json").write_text(json.dumps(manifest))
    (root / "source-00/original.qasm").unlink()
    history = tmp_path / "history"
    history.mkdir()
    result = audit(root, [history])
    assert result["targets"][0]["raw_sha256"] is None
    assert result["gaps"][0]["reason"] == "Original source unavailable"
