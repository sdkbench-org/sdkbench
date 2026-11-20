"""Whole-revision controls freeze once and preserve neutral paired accounting."""

import importlib.util
import shutil
from copy import deepcopy
from pathlib import Path

import pytest

from sdkbench.candidates.adapters import workflow_configuration
from sdkbench.candidates.revisions import (
    verify_revision_control,
    verify_revision_preparation,
)
from sdkbench.p0 import Registration
from sdkbench.p0.models import ContractError, canonical_bytes, digest, read_json

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def tool(monkeypatch):
    monkeypatch.syspath_prepend(str(ROOT / "tools"))
    spec = importlib.util.spec_from_file_location(
        "revision_comparison", ROOT / "tools/compare_compiler_applications.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def revision_inputs(workflow="qiskit-transpile-restored"):
    config = workflow_configuration(workflow)
    distribution = {
        "qiskit": "qiskit",
        "cirq": "cirq-core",
        "flagquantum": "flagquantum",
    }[config["sdk"]]
    registrations, inventories = [], {}
    for index in range(2):
        version = str(index + 1)
        inventory = {
            "dependencies": [
                {
                    "name": distribution,
                    "version": version,
                    "record_sha256": version * 64,
                },
                {"name": "numpy", "version": "1", "record_sha256": "a" * 64},
            ],
            "host": {"machine": "synthetic-only", "cpuinfo_sha256": str(index) * 64},
            "image_descriptor": {"platform": "test", "kernel": "test"},
            "implementation": {"runtime_source_sha256": "b" * 64},
        }
        inventory["dependency_lock_sha256"] = digest(inventory["dependencies"])
        inventory["image_descriptor_sha256"] = digest(inventory["image_descriptor"])
        reg = Registration(
            f"revision-{index}",
            [
                {
                    "name": distribution,
                    "version": version,
                    "role": "frontend",
                    "artifact_sha256": version * 64,
                },
                {
                    "name": "numpy",
                    "version": "1",
                    "role": "numerical-dependency",
                    "artifact_sha256": "a" * 64,
                },
                {
                    "name": "sdkbench",
                    "version": "test",
                    "role": "harness",
                    "artifact_sha256": "b" * 64,
                },
            ],
            {
                "profile": "CPU1-FP64",
                "precision": "float64/complex128",
                "threads": 1,
                "options": {
                    "suite": "compiler-candidate",
                    "sdk": config["sdk"],
                    "workflow": workflow,
                    "compiler_options": config,
                    "implementation_sha256": "b" * 64,
                    "source_build": {
                        "source_commit": version * 40,
                        "wheel": {"sha256": version * 64},
                    },
                },
            },
            {
                "python": "test",
                "os": "test",
                "image_sha256": inventory["image_descriptor_sha256"],
                "dependency_lock_sha256": inventory["dependency_lock_sha256"],
                "host": inventory["host"],
            },
        )
        registrations.append(reg)
        inventories[reg.stack_id] = inventory
    return registrations, inventories


@pytest.mark.parametrize(
    "workflow",
    [
        "qiskit-transpile-restored",
        "cirq-route-cz-restored",
        "flagquantum-ordinary-restored",
        "flagquantum-target-artifact",
    ],
)
def test_same_rules_admit_distinct_revisions_of_every_supported_sdk(workflow):
    registrations, inventories = revision_inputs(workflow)
    before = deepcopy((registrations, inventories))
    verify_revision_control(registrations, inventories)
    assert (registrations, inventories) == before
    for reg in registrations:
        options = reg.configuration["options"]
        source = options.pop("source_build")
        options["published_wheel"] = {
            "distribution": reg.components[0]["name"],
            "version": reg.components[0]["version"],
            "sha256": source["wheel"]["sha256"],
        }
    verify_revision_control(registrations, inventories)


@pytest.mark.parametrize(
    "fault",
    [
        "same-source",
        "missing-origin",
        "mixed-origin",
        "workflow",
        "sdk",
        "options",
        "precision",
        "threads",
        "host",
        "python",
        "image",
        "inventory-lock",
        "extra-dependency",
        "dependency-version",
        "record-prefix",
        "duplicate-dependency",
        "numerical-bytes",
        "harness-bytes",
        "inventory-host",
        "inventory-image",
        "inventory-implementation",
        "missing-frontend",
        "missing-stack",
    ],
)
def test_unmatched_revisions_are_rejected(fault):
    registrations, inventories = revision_inputs()
    reg = registrations[1]
    options = reg.configuration["options"]
    inventory = inventories[reg.stack_id]
    if fault == "same-source":
        options["source_build"]["source_commit"] = "1" * 40
    elif fault == "missing-origin":
        del options["source_build"]
    elif fault == "mixed-origin":
        source = options.pop("source_build")
        options["published_wheel"] = {
            "distribution": "qiskit",
            "version": "2",
            "sha256": source["wheel"]["sha256"],
        }
    elif fault in {"workflow", "sdk", "options"}:
        options[
            {"workflow": "workflow", "sdk": "sdk", "options": "compiler_options"}[fault]
        ] = "changed"
    elif fault in {"precision", "threads"}:
        reg.configuration[fault] = "changed"
    elif fault in {"host", "python", "image"}:
        if fault == "host":
            reg.environment["host"]["machine"] = "another-host"
        else:
            reg.environment[{"python": "python", "image": "image_sha256"}[fault]] = (
                "f" * 64
            )
    elif fault == "inventory-lock":
        reg.environment["dependency_lock_sha256"] = "f" * 64
    elif fault in {
        "extra-dependency",
        "dependency-version",
        "record-prefix",
        "duplicate-dependency",
        "missing-frontend",
    }:
        if fault == "extra-dependency":
            inventory["dependencies"].append(
                {"name": "extra", "version": "1", "record_sha256": "f" * 64}
            )
        elif fault == "dependency-version":
            inventory["dependencies"][1]["version"] = "2"
        elif fault == "record-prefix":
            inventory["dependencies"][1]["record_sha256"] = "f" * 64
        elif fault == "duplicate-dependency":
            inventory["dependencies"].append(
                {**inventory["dependencies"][1], "name": "NumPy"}
            )
        else:
            inventory["dependencies"].pop(0)
        inventory["dependency_lock_sha256"] = digest(inventory["dependencies"])
        reg.environment["dependency_lock_sha256"] = inventory["dependency_lock_sha256"]
    elif fault in {"numerical-bytes", "harness-bytes"}:
        reg.components[1 if fault == "numerical-bytes" else 2]["artifact_sha256"] = (
            "f" * 64
        )
    elif fault == "inventory-host":
        inventory["host"] = {"machine": "another-host"}
    elif fault == "inventory-image":
        inventory["image_descriptor"]["kernel"] = "other"
    elif fault == "inventory-implementation":
        inventory["implementation"]["runtime_source_sha256"] = "f" * 64
    else:
        registrations.pop()
    with pytest.raises((ContractError, KeyError, TypeError)):
        verify_revision_control(registrations, inventories)


def write_inputs(root, registrations, inventories):
    paths, inventory_paths, interpreters = [], {}, {}
    for reg in registrations:
        path = root / (reg.stack_id + ".json")
        path.write_bytes(canonical_bytes(reg.to_dict()))
        paths.append(path)
        path = root / (reg.stack_id + "-environment.json")
        path.write_bytes(canonical_bytes(inventories[reg.stack_id]))
        inventory_paths[reg.stack_id] = path
        python = root / reg.stack_id / "python"
        python.parent.mkdir()
        python.write_text("synthetic executable; never launched\n")
        python.chmod(0o700)
        interpreters[reg.stack_id] = str(python)
    return paths, inventory_paths, interpreters


@pytest.fixture(scope="module")
def joint_source(tmp_path_factory):
    tmp_path = tmp_path_factory.mktemp("revision-source")
    spec = importlib.util.spec_from_file_location(
        "revision_preparation", ROOT / "tools/prepare_compiler_applications.py"
    )
    preparation = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(preparation)
    monkeypatch = pytest.MonkeyPatch()
    registrations, inventories = revision_inputs()
    paths, inventory_paths, interpreters = write_inputs(
        tmp_path, registrations, inventories
    )
    output = tmp_path / "preparation"
    calls = []

    def admit(reg, interpreter, environment, *, inventory):
        assert not output.exists()
        assert environment["PYTHONPATH"] == str(ROOT / "src")
        assert inventory == inventories[reg.stack_id]
        calls.append(reg.stack_id)
        return {
            "registration_sha256": digest(reg.to_dict()),
            "interpreter": interpreter,
            "admission": {
                "configuration_sha256": reg.configuration_sha256,
                "environment_sha256": reg.environment_sha256,
                "independent_attestation": False,
            },
        }

    def draw(size):
        freeze = read_json(output / "freeze.json")
        assert size == 32 and len(calls) == 2
        assert freeze["revision_environments"]["inventories"] == inventories
        calls.append("draw")
        return bytes.fromhex("01" * 32)

    monkeypatch.setattr(preparation, "admit_interpreter", admit)
    monkeypatch.setattr(preparation, "implementation_fingerprint", lambda: "b" * 64)
    monkeypatch.setattr(preparation.secrets, "token_bytes", draw)
    bundle = preparation.prepare(
        ROOT / "docs/implementation",
        paths,
        output,
        profile="revision-control",
        inventories=inventory_paths,
        interpreters=interpreters,
    )
    assert calls == [r.stack_id for r in registrations] + ["draw"]
    with pytest.raises(FileExistsError):
        preparation.prepare(
            ROOT / "docs/implementation",
            paths,
            output,
            profile="revision-control",
            inventories=inventory_paths,
            interpreters=interpreters,
        )
    assert calls[-1] == "draw"
    monkeypatch.undo()
    return output, bundle, registrations


@pytest.fixture
def joint_preparation(joint_source, tmp_path):
    source, bundle, registrations = joint_source
    output = tmp_path / "evidence"
    output.mkdir()
    for name in ("freeze.json", "draw.json", "selection.json"):
        shutil.copyfile(source / name, output / name)
    for name in ("full-bundle", "cohort"):
        (output / name).symlink_to(source / name, target_is_directory=True)
    return output, bundle, deepcopy(registrations)


def context_for(prepared):
    output, bundle, registrations = prepared
    freeze = read_json(output / "freeze.json")
    environments = freeze["revision_environments"]
    admissions = {
        name: {"status": "admitted", "interpreter_probe": probe}
        for name, probe in environments["probes"].items()
    }
    registered = {r.stack_id: r.to_dict() for r in registrations}
    context = verify_revision_preparation(
        output, bundle, registered, environments["interpreters"], admissions
    )
    return context, admissions


def test_joint_freeze_preserves_thirty_cases_and_independent_evidence(
    joint_preparation,
):
    context, _ = context_for(joint_preparation)
    assert len(context["instances"]) == 30
    assert context["stack_ids"] == ["revision-0", "revision-1"]
    assert context["workflow"] == "qiskit-transpile-restored"
    output, bundle, _ = joint_preparation
    assert (
        bundle.plan["application_selection"]["freeze_sha256"]
        == context["freeze_sha256"]
    )
    assert read_json(output / "freeze.json")["campaign_wall_limit_seconds"] == 16200


@pytest.mark.parametrize(
    "fault", ["draw", "selection", "registration", "interpreter", "probe", "cohort"]
)
def test_joint_evidence_rejects_substitution(joint_preparation, fault):
    output, bundle, registrations = joint_preparation
    _, admissions = context_for(joint_preparation)
    registered = {r.stack_id: r.to_dict() for r in registrations}
    interpreters = read_json(output / "freeze.json")["revision_environments"][
        "interpreters"
    ]
    if fault in {"draw", "selection"}:
        path = output / (fault + ".json")
        value = read_json(path)
        value["freeze_sha256"] = "f" * 64
        path.write_bytes(canonical_bytes(value))
    elif fault == "registration":
        registered["revision-0"]["configuration"]["options"]["source_build"][
            "source_commit"
        ] = "f" * 40
    elif fault == "interpreter":
        interpreters["revision-0"]["python"] = "/different/python"
    elif fault == "probe":
        admissions["revision-0"]["interpreter_probe"]["interpreter"]["python"] = (
            "/different/python"
        )
    else:
        path = output / "selection.json"
        value = read_json(path)
        value["instances"].pop()
        path.write_bytes(canonical_bytes(value))
    with pytest.raises(ContractError):
        verify_revision_preparation(
            output, bundle, registered, interpreters, admissions
        )


def revision_summary(tool, prepared):
    from test_application_comparison import summary

    context, admissions = context_for(prepared)
    source = summary(tool)
    template = deepcopy(source["cases"][:2])
    # Synthetic accepted measurements exercise accounting, never SDK performance.
    source["cases"] = []
    for instance in context["instances"]:
        for index, stack in enumerate(context["stack_ids"]):
            row = deepcopy(template[index])
            row.update(instance=instance, sdk=stack, workflow=context["workflow"])
            source["cases"].append(row)
    source["bundle_sha256"] = context["bundle_sha256"]
    source["registrations"] = {r.stack_id: r.to_dict() for r in prepared[2]}
    return source, context, admissions


def test_revision_pairs_reuse_same_metrics_and_keep_failures(tool, joint_preparation):
    source, context, _ = revision_summary(tool, joint_preparation)
    result = tool.compare(source, profile="revision-control", revision_context=context)
    assert result["case_count"] == 30 and len(result["pairs"]) == 30
    pair = result["pairs"][0]
    assert (
        pair["numerator_stack"] == "revision-0"
        and pair["denominator_stack"] == "revision-1"
    )
    assert (
        pair["numerator_workflow"]
        == pair["denominator_workflow"]
        == context["workflow"]
    )
    assert pair["ratios"]["paired_block_compile_time"]["median"] == 0.5
    assert pair["ratios"]["paired_block_memory_peak"]["count"] == 10
    source["cases"][0]["status"] = "timeout"
    result = tool.compare(source, profile="revision-control", revision_context=context)
    assert sum(p["ratios"] is None for p in result["pairs"]) == 1
    assert sum(result["coverage"]["revision-0"].values()) == 30
    assert result["publication_eligible"] is False


@pytest.mark.parametrize(
    "fault", ["context", "bundle", "registration", "case", "stack", "workflow"]
)
def test_revision_comparison_refuses_unbound_or_mixed_campaigns(
    tool, joint_preparation, fault
):
    source, context, _ = revision_summary(tool, joint_preparation)
    if fault == "context":
        context = None
    elif fault == "bundle":
        source["bundle_sha256"] = "f" * 64
    elif fault == "registration":
        source["registrations"]["revision-0"]["environment"]["python"] = "other"
    elif fault == "case":
        source["cases"] = source["cases"][2:]
    else:
        source["cases"][0]["sdk" if fault == "stack" else "workflow"] = "other"
    with pytest.raises(ContractError):
        tool.compare(source, profile="revision-control", revision_context=context)


@pytest.mark.parametrize(
    "fault",
    ["dependency", "workflow", "partial-map", "same-interpreter", "probe-failure"],
)
def test_preparation_rejects_before_entropy(tmp_path, monkeypatch, fault):
    spec = importlib.util.spec_from_file_location(
        "revision_negative_preparation", ROOT / "tools/prepare_compiler_applications.py"
    )
    preparation = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(preparation)
    registrations, inventories = revision_inputs()
    if fault == "dependency":
        inventory = inventories["revision-1"]
        inventory["dependencies"][1]["record_sha256"] = "f" * 64
        inventory["dependency_lock_sha256"] = digest(inventory["dependencies"])
        registrations[1].environment["dependency_lock_sha256"] = inventory[
            "dependency_lock_sha256"
        ]
    elif fault == "workflow":
        registrations[1].configuration["options"]["workflow"] = "cirq-route-cz-restored"
    paths, inventory_paths, interpreters = write_inputs(
        tmp_path, registrations, inventories
    )
    if fault == "partial-map":
        interpreters.pop("revision-1")
    elif fault == "same-interpreter":
        interpreters["revision-1"] = interpreters["revision-0"]
    calls = []

    def admit(reg, expected, environment, *, inventory):
        calls.append(reg.stack_id)
        if len(calls) == 2:
            raise ContractError("Synthetic second environment failure")
        return {}

    monkeypatch.setattr(preparation, "admit_interpreter", admit)
    monkeypatch.setattr(
        preparation.secrets,
        "token_bytes",
        lambda _: pytest.fail("Drew entropy after failed admission"),
    )
    with pytest.raises(ContractError):
        preparation.prepare(
            ROOT / "docs/implementation",
            paths,
            tmp_path / "run",
            profile="revision-control",
            interpreters=interpreters,
            inventories=inventory_paths,
        )
    assert len(calls) == (2 if fault == "probe-failure" else 0)
    assert not (tmp_path / "run").exists()


def test_cli_replays_joint_campaign_and_retains_every_denied_case(
    tool, joint_preparation, tmp_path, monkeypatch
):
    from test_candidate_runner import seal

    from sdkbench.candidates import environment
    from sdkbench.p1a.campaign import run_campaign

    output, bundle, registrations = joint_preparation
    frozen = read_json(output / "freeze.json")["revision_environments"]
    candidates = {r.stack_id: r for r in registrations}

    def refuse(*args, **kwargs):
        raise ContractError("Synthetic environment became unavailable after freeze")

    monkeypatch.setattr(environment, "admit_interpreter", refuse)
    campaign = tmp_path / "campaign"
    run_campaign(
        bundle,
        directory=campaign,
        cgroup_parent=tmp_path,
        cpu=0,
        suite="compiler-candidate",
        candidates=candidates,
        candidate_interpreters={
            name: value["python"] for name, value in frozen["interpreters"].items()
        },
    )
    seal(campaign)
    result_path = tmp_path / "comparison.json"
    monkeypatch.setattr(
        "sys.argv",
        [
            "compare",
            "--directory",
            str(campaign),
            "--bundle",
            str(bundle.directory),
            "--output",
            str(result_path),
            "--profile",
            "revision-control",
            "--preparation",
            str(output),
        ],
    )
    tool.main()
    result = read_json(result_path)
    assert result["case_count"] == 30 and len(result["pairs"]) == 30
    assert result["independent_replay"]["blocks_verified"] == 600
    assert result["coverage"] == {name: {"access-blocked": 30} for name in candidates}
    assert result["joint_revision_control"]["freeze_sha256"] == digest(
        read_json(output / "freeze.json")
    )
    assert all(pair["ratios"] is None for pair in result["pairs"])
    with pytest.raises(FileExistsError):
        tool.main()
