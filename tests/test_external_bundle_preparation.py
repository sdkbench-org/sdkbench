"""External inputs keep the intended denominator and frozen W03 contracts."""

import hashlib
import json
from pathlib import Path

import pytest

from sdkbench.candidates import external_bundle as preparation
from sdkbench.p0 import Bundle
from sdkbench.p0.evaluators import routing
from sdkbench.p0.models import ContractError

BASE = Path(__file__).resolve().parents[1] / "docs/implementation"
WORKFLOWS = [
    "flagquantum-ordinary-restored",
    "flagquantum-target-artifact",
    "qiskit-transpile-restored",
    "cirq-route-cz-restored",
]


def population(tmp_path):
    root = tmp_path / "source"
    root.mkdir()
    notices = {}
    for name in ("LICENSE", "NOTICE"):
        raw = ("Synthetic test " + name).encode()
        (root / name).write_bytes(raw)
        notices[name] = {"sha256": hashlib.sha256(raw).hexdigest()}
    rows = []
    for name, n, body in (
        ("bell", 6, "h q[0]; cx q[0],q[1];"),
        ("dynamic", 8, "reset q[0];"),
    ):
        raw = (f'OPENQASM 2.0; include "qelib1.inc"; qreg q[{n}]; ' + body).encode()
        path = f"{name}_n{n}.qasm"
        (root / path).write_bytes(raw)
        rows.append(
            {
                "path": path,
                "bytes": len(raw),
                "git_blob": hashlib.sha1(
                    b"blob " + str(len(raw)).encode() + b"\0" + raw
                ).hexdigest(),
            }
        )
    manifest = tmp_path / "population.json"
    manifest.write_text(
        json.dumps(
            {
                "files": rows,
                "licenses": notices,
                "topologies": ["line", "2-by-n/2-grid"],
                "participants": WORKFLOWS,
            }
        )
    )
    return root, manifest


@pytest.fixture
def supervised(monkeypatch):
    pytest.importorskip("qiskit")
    pytest.importorskip("cirq")
    pytest.importorskip("ply")
    calls = []

    def run(argv, *, cwd, cgroup_parent, limits, environment):
        assert argv[-2:] == ["--worker", "request.json"]
        assert limits.wall_seconds == 300 and limits.memory_bytes == 16 * 1024**3
        assert environment.keys() == {"PYTHONPATH"}
        request = json.loads((cwd / "request.json").read_text())
        calls.append(request)
        try:
            result = {
                "status": "converted",
                "prepared": preparation.convert_source(
                    request["source"], probe_preparations=request["probe_preparations"]
                ),
            }
        except ContractError as error:
            result = {"status": "refused", "reason": str(error)}
        return {"execution_status": "completed", "stdout": json.dumps(result)}

    monkeypatch.setattr(preparation, "run_command", run)
    return calls


def test_preparation_preserves_contracts_denominator_and_source_notices(
    tmp_path, supervised
):
    root, manifest = population(tmp_path)
    output = tmp_path / "prepared"
    result = preparation.prepare(
        BASE, manifest, root, output, cpu=0, cgroup_parent=tmp_path
    )
    assert len(supervised) == 2
    assert result["admitted_instances"] == 2
    assert len(result["intended_outcomes"]) == 16
    assert {x["participant_execution"] for x in result["intended_outcomes"]} == {
        "not-started"
    }
    assert [x["status"] for x in result["inputs"]] == [
        "input-admitted",
        "input-not-admitted",
    ]
    assert "nongate" in result["inputs"][1]["reason"]
    for name in ("LICENSE", "NOTICE"):
        assert (output / name).read_bytes() == (root / name).read_bytes()
    bundle = Bundle(output / "bundle")
    baseline = Bundle(BASE)
    original = baseline.cases["ROUTE-LINE-06"]
    assert bundle.plan["execution_profile"] == baseline.plan["execution_profile"]
    for key, case in bundle.cases.items():
        for field in (
            "acceptance",
            "case_wall_limit_seconds",
            "process_memory_limit_gib",
        ):
            assert case[field] == original[field]
        assert (
            bundle.fixtures[key]["probe_preparations"]
            == baseline.fixtures["ROUTE-LINE-06"]["probe_preparations"]
        )
        verdict = routing(
            {
                "operations": [
                    {"name": "h", "qubits": [0]},
                    {"name": "h", "qubits": [1]},
                    {"name": "cz", "qubits": [0, 1]},
                    {"name": "h", "qubits": [1]},
                ],
                "final_layout": list(range(6)),
                "compile_wall_seconds": 0.0,
            },
            bundle.fixtures[key],
            bundle.references[key],
            case,
            0,
        )
        assert verdict["max_semantic_error"] < 1e-12
    assert not result["publication_eligible"]
    with pytest.raises(FileExistsError):
        preparation.prepare(BASE, manifest, root, output, cpu=0, cgroup_parent=tmp_path)


@pytest.mark.parametrize(
    "status", ["timeout", "out-of-memory", "error", "isolation-failed", "output-limit"]
)
def test_preparation_resource_failure_is_not_a_participant_outcome(
    tmp_path, monkeypatch, status
):
    root, manifest = population(tmp_path)
    monkeypatch.setattr(
        preparation,
        "run_command",
        lambda *a, **k: {
            "execution_status": status,
            "stdout": "",
            "stderr": "original diagnostic",
        },
    )
    result = preparation.prepare(
        BASE, manifest, root, tmp_path / "prepared", cpu=0, cgroup_parent=tmp_path
    )
    assert result["admitted_instances"] == 0
    assert len(result["intended_outcomes"]) == 16
    assert all(status in x["reason"] for x in result["inputs"])
    assert all(
        x["participant_execution"] == "not-started" for x in result["intended_outcomes"]
    )


def test_source_identity_failure_preserves_other_sources(tmp_path, supervised):
    root, manifest = population(tmp_path)
    path = root / "bell_n6.qasm"
    path.write_bytes(path.read_bytes().replace(b"h q[0]", b"x q[0]"))
    result = preparation.prepare(
        BASE, manifest, root, tmp_path / "prepared", cpu=0, cgroup_parent=tmp_path
    )
    assert len(supervised) == 1
    assert "Git blob differs" in result["inputs"][0]["reason"]
    assert len(result["intended_outcomes"]) == 16


def test_notice_mismatch_refuses_before_creating_evidence_or_starting_worker(
    tmp_path, monkeypatch
):
    root, manifest = population(tmp_path)
    (root / "NOTICE").write_text("changed")
    monkeypatch.setattr(
        preparation, "run_command", lambda *a, **k: pytest.fail("Worker must not start")
    )
    output = tmp_path / "prepared"
    with pytest.raises(ContractError, match="license/notice differs"):
        preparation.prepare(BASE, manifest, root, output, cpu=0, cgroup_parent=tmp_path)
    assert not output.exists()


def test_missing_cgroup_control_is_retained_without_execution(tmp_path, monkeypatch):
    from sdkbench.p0.supervisor import IsolationUnavailable

    root, manifest = population(tmp_path)

    def unavailable(*args, **kwargs):
        raise IsolationUnavailable("No delegated cgroup")

    monkeypatch.setattr(preparation, "run_command", unavailable)
    result = preparation.prepare(
        BASE, manifest, root, tmp_path / "prepared", cpu=0, cgroup_parent=tmp_path
    )
    assert len(result["intended_outcomes"]) == 16
    assert all("IsolationUnavailable" in x["reason"] for x in result["inputs"])


@pytest.mark.parametrize(
    "filename, expected",
    [("bell_n6.qasm", "converted"), ("dynamic_n8.qasm", "refused")],
)
def test_native_worker_command_retains_conversion_or_refusal(
    tmp_path, supervised, filename, expected
):
    import os
    import subprocess
    import sys

    root, _ = population(tmp_path)
    request = tmp_path / "request.json"
    probes = Bundle(BASE).fixtures["ROUTE-GRID-08"]["probe_preparations"]
    request.write_text(
        json.dumps(
            {"source": (root / filename).read_text(), "probe_preparations": probes}
        )
    )
    paths = [str(Path(__file__).resolve().parents[1] / "src")]
    paths.extend(
        str(Path(value).resolve())
        for value in os.environ.get("PYTHONPATH", "").split(os.pathsep)
        if value
    )
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "sdkbench.candidates.external_bundle",
            "--worker",
            str(request),
        ],
        cwd=tmp_path,
        env={**os.environ, "PYTHONPATH": os.pathsep.join(paths)},
        capture_output=True,
        text=True,
        timeout=60,
        check=True,
    )
    response = json.loads(result.stdout)
    assert response["status"] == expected
    if expected == "converted":
        assert (
            response["prepared"]["source_conformance"]["verification"]
            == "full-operator"
        )
    else:
        assert "nongate" in response["reason"]


def test_external_source_cannot_escape_the_declared_root(tmp_path, monkeypatch):
    root, manifest = population(tmp_path)
    payload = json.loads(manifest.read_text())
    outside = tmp_path / "outside_n6.qasm"
    outside.write_bytes((root / "bell_n6.qasm").read_bytes())
    payload["files"][0]["path"] = "../outside_n6.qasm"
    manifest.write_text(json.dumps(payload))
    monkeypatch.setattr(
        preparation,
        "run_command",
        lambda *a, **k: {"execution_status": "error", "stdout": ""},
    )
    result = preparation.prepare(
        BASE, manifest, root, tmp_path / "prepared", cpu=0, cgroup_parent=tmp_path
    )
    assert "leaves its root" in result["inputs"][0]["reason"]
    assert len(result["intended_outcomes"]) == 16


def test_malformed_worker_response_stays_an_input_refusal(tmp_path, monkeypatch):
    root, manifest = population(tmp_path)
    monkeypatch.setattr(
        preparation,
        "run_command",
        lambda *a, **k: {"execution_status": "completed", "stdout": "incomplete JSON"},
    )
    result = preparation.prepare(
        BASE, manifest, root, tmp_path / "prepared", cpu=0, cgroup_parent=tmp_path
    )
    assert result["admitted_instances"] == 0
    assert all("JSONDecodeError" in row["reason"] for row in result["inputs"])
    assert len(result["intended_outcomes"]) == 16


def test_incomplete_converted_payload_cannot_admit_a_source(tmp_path, monkeypatch):
    root, manifest = population(tmp_path)

    def broken(argv, *, cwd, **kwargs):
        request = json.loads((cwd / "request.json").read_text())
        width = 6 if "q[6]" in request["source"] else 8
        payload = {
            "status": "converted",
            "prepared": {
                "n_qubits": width,
                "source_sha256": hashlib.sha256(request["source"].encode()).hexdigest(),
            },
        }
        return {"execution_status": "completed", "stdout": json.dumps(payload)}

    monkeypatch.setattr(preparation, "run_command", broken)
    result = preparation.prepare(
        BASE, manifest, root, tmp_path / "prepared", cpu=0, cgroup_parent=tmp_path
    )
    assert result["admitted_instances"] == 0
    assert all(row["status"] == "input-not-admitted" for row in result["inputs"])
    assert all("operation list" in row["reason"] for row in result["inputs"])
