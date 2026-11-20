"""An absent optional SDK diagnostic is distinct from zero observed rewrites."""

from types import ModuleType, SimpleNamespace

import pytest

from sdkbench.candidates.adapters import CompilerAdapter


@pytest.fixture
def target_compiler(monkeypatch):
    import sys

    modules = {}
    for name in (
        "flagquantum",
        "flagquantum.compiler",
        "flagquantum.compiler.artifacts",
        "flagquantum.compiler.artifacts.artifact_compilation",
        "flagquantum.compiler.routing",
        "flagquantum.core",
        "flagquantum.core._artifacts",
        "flagquantum.core.ir",
        "flagquantum.core.target_capabilities",
    ):
        module = ModuleType(name)
        module.__path__ = []
        modules[name] = module
        monkeypatch.setitem(sys.modules, name, module)
    ir = modules["flagquantum.core.ir"]
    ir.Instruction = lambda name, wires, **kwargs: SimpleNamespace(
        name=name, wires=wires, matrix=None, **kwargs
    )
    ir.CircuitIR = lambda n, instructions, **kwargs: SimpleNamespace(
        n_wires=n, instructions=instructions, **kwargs
    )
    ir.MeasurementNode = lambda *args: args
    modules["flagquantum.core._artifacts"].ProgramArtifactV2 = SimpleNamespace(
        from_circuit_ir=lambda source, **kwargs: source
    )
    modules["flagquantum.compiler.routing"].CouplingMap = lambda n, edges: (n, edges)
    capabilities = modules["flagquantum.core.target_capabilities"]
    for name in (
        "CapabilityFact",
        "CapabilityScope",
        "EvidenceReference",
        "FactSource",
        "TargetIdentity",
    ):
        setattr(capabilities, name, lambda **kwargs: SimpleNamespace(**kwargs))
    capabilities.TargetIdentity = lambda *args: args
    capabilities.TargetCapabilitySnapshot = lambda **kwargs: SimpleNamespace(
        snapshot_id="d" * 64, **kwargs
    )
    capabilities.EvidenceLevel = SimpleNamespace(OBSERVABLE="observable")
    capabilities.FactExposure = SimpleNamespace(
        OBSERVED="observed", DECLARED="declared"
    )
    capabilities.SupportStatus = SimpleNamespace(VERIFIED="verified")
    program = SimpleNamespace(instructions=(ir.Instruction("cz", (0, 1)),))
    result = SimpleNamespace(
        legalization=SimpleNamespace(
            program=program, native_gate_legalization=SimpleNamespace(program=program)
        ),
        physical_plan=SimpleNamespace(final_logical_to_physical=(0, 1)),
        executable_artifact=SimpleNamespace(to_json=lambda: '{"synthetic":"retained"}'),
    )
    calls = []

    def compile_artifact(*args, **kwargs):
        calls.append((args, kwargs))
        return result

    modules[
        "flagquantum.compiler.artifacts.artifact_compilation"
    ].compile_circuit_artifact_for_target = compile_artifact
    return result, calls


def fixture():
    return {
        "n_qubits": 2,
        "operations": [{"name": "cz", "qubits": [0, 1]}],
        "initial_layout": "identity",
        "ancillas_allowed": 0,
        "target_edges": [[0, 1]],
    }


@pytest.mark.parametrize(
    "diagnostic, expected", [("absent", None), ("none", 0), ("rewrites", 2)]
)
def test_target_workflow_retains_artifact_without_inventing_optional_diagnostics(
    target_compiler, diagnostic, expected
):
    result, calls = target_compiler
    if diagnostic != "absent":
        result.legalization.native_block_optimization = (
            None if diagnostic == "none" else SimpleNamespace(rewrites=("a", "b"))
        )
    native = SimpleNamespace()
    adapter = CompilerAdapter(native, "flagquantum-target-artifact")
    payload = adapter.execute("route", fixture(), 11)
    assert payload["operations"] == [{"name": "cz", "qubits": [0, 1]}]
    assert payload["final_layout"] == [0, 1] and len(calls) == 1
    assert calls[0][1]["max_native_added_operations"] == 20000
    assert calls[0][1]["max_routing_added_operations"] == 20000
    assert native.compiler_evidence == {
        "executable_artifact": '{"synthetic":"retained"}',
        "target_snapshot_id": "d" * 64,
    }
    assert adapter.audit["native_block_optimization_evidence_available"] == int(
        diagnostic != "absent"
    )
    if expected is None:
        assert "accepted_block_rewrites" not in adapter.audit
    else:
        assert adapter.audit["accepted_block_rewrites"] == expected
    assert adapter.audit["native_baseline_cz_count"] == 1


@pytest.mark.parametrize(
    "fault", ["malformed-diagnostic", "compiler-error", "serialization-error"]
)
def test_required_target_work_and_invalid_present_diagnostics_still_fail(
    target_compiler, fault
):
    result, _ = target_compiler
    if fault == "malformed-diagnostic":
        result.legalization.native_block_optimization = object()
    elif fault == "serialization-error":

        def fail():
            raise RuntimeError("Synthetic serialization failure")

        result.executable_artifact.to_json = fail
    else:
        import sys

        def fail(*args, **kwargs):
            raise RuntimeError("Synthetic compilation failure")

        sys.modules[
            "flagquantum.compiler.artifacts.artifact_compilation"
        ].compile_circuit_artifact_for_target = fail
    with pytest.raises((AttributeError, RuntimeError)):
        CompilerAdapter(SimpleNamespace(), "flagquantum-target-artifact").execute(
            "route", fixture(), 11
        )


def test_replayed_report_distinguishes_absent_evidence_from_observed_zero(
    tmp_path, monkeypatch
):
    import importlib.util
    import json
    from pathlib import Path

    from test_candidate_runner import registration, seal, synthetic_supervisor

    from sdkbench.candidates.provenance import file_sha256
    from sdkbench.p0 import Bundle
    from sdkbench.p0.models import canonical_bytes
    from sdkbench.p1a import campaign

    root = Path(__file__).resolve().parents[1]
    bundle = Bundle(root / "docs/implementation")
    synthetic_supervisor(monkeypatch, bundle)
    supervisor = campaign.run_command

    def run(argv, **kwargs):
        execution = supervisor(argv, **kwargs)
        response = json.loads(execution["stdout"])
        available = int(response["sdk"] == "reported-zero")
        for phase, records in (
            ("warmup", response["warmups"]),
            ("measured", response["records"]),
        ):
            for index, record in enumerate(records):
                record["measurements"][
                    "native_block_optimization_evidence_available"
                ] = available
                if available:
                    record["measurements"]["accepted_block_rewrites"] = 0
                path = Path(kwargs["cwd"]) / f"compiler-evidence-{phase}-{index}.json"
                path.write_bytes(
                    canonical_bytes(
                        {
                            "executable_artifact": '{"synthetic":"retained"}',
                            "target_snapshot_id": "d" * 64,
                        }
                    )
                )
                response["compiler_evidence_files"].append(
                    {
                        "phase": phase,
                        "repetition": index,
                        "filename": path.name,
                        "sha256": file_sha256(path),
                    }
                )
        execution["stdout"] = json.dumps(response)
        return execution

    monkeypatch.setattr(campaign, "run_command", run)
    registrations = {
        name: registration(name, "flagquantum-target-artifact")
        for name in ("absent-evidence", "reported-zero")
    }
    directory = tmp_path / "campaign"
    campaign.run_campaign(
        bundle,
        directory=directory,
        cgroup_parent=tmp_path,
        cpu=0,
        suite="compiler-candidate",
        candidates=registrations,
    )
    seal(directory)
    spec = importlib.util.spec_from_file_location(
        "optional_diagnostic_report", root / "tools/compiler_candidate_report.py"
    )
    report_tool = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(report_tool)
    report = report_tool.summarize(directory, bundle)
    assert report["independent_replay"]["blocks_verified"] == 60
    assert len(report["cases"]) == 6
    for row in report["cases"]:
        assert row["status"] == "accepted" and row["accepted_records"] == 30
        available = row["sdk_reported_native_block_optimization_evidence_available"]
        assert available["count"] == 30
        rewrites = row["sdk_reported_accepted_block_rewrites"]
        if row["sdk"] == "absent-evidence":
            assert available["median"] == 0 and rewrites is None
        else:
            assert available["median"] == 1 and rewrites["median"] == 0
            assert rewrites["count"] == 30
    assert report["publication_eligible"] is False
