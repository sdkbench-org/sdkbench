"""Match whole SDK revisions without changing compiler acceptance or budgets."""

from __future__ import annotations

import re
from copy import deepcopy
from pathlib import Path

from ..p0 import Bundle, Registration
from ..p0.models import digest, read_json, require
from ..p1a.common import DISTRIBUTIONS
from .adapters import workflow_configuration
from .environment import verify_interpreter_admission


def _name(value: str) -> str:
    return re.sub(r"[-_.]+", "-", value).lower()


def _host(value: dict) -> dict:
    result = deepcopy(value)
    # Frequencies change between observations; retain the original in evidence.
    result.pop("cpuinfo_sha256", None)
    return result


def verify_inventory_observation(expected: dict, observed: dict) -> None:
    """Recheck supplied inventory facts in the selected pre-draw interpreter."""
    expected, observed = deepcopy(expected), deepcopy(observed)
    expected["host"], observed["host"] = (
        _host(expected["host"]),
        _host(observed["host"]),
    )
    require(
        expected == observed,
        "Selected interpreter inventory changed before the joint freeze",
    )


def verify_revision_control(
    registrations: list[Registration],
    inventories: dict[str, dict],
) -> None:
    """Require two immutable revisions with otherwise identical registered inputs.

    Inventories come from ``capture_environment`` in each selected interpreter.
    Exact RECORD hashes and non-frontend component bytes must match; installation
    prefix differences receive no implicit exception.
    """
    require(
        len(registrations) == 2 and len({r.stack_id for r in registrations}) == 2,
        "Revision controls require exactly two distinct stacks",
    )
    require(
        set(inventories) == {r.stack_id for r in registrations},
        "Provide a complete environment inventory for each revision",
    )
    controls, origins = [], []
    for registration in registrations:
        configuration = deepcopy(registration.configuration)
        options = configuration["options"]
        sdk, workflow = options.get("sdk"), options.get("workflow")
        require(
            sdk in DISTRIBUTIONS
            and workflow
            in {
                "flagquantum-ordinary-restored",
                "flagquantum-target-artifact",
                "qiskit-transpile-restored",
                "cirq-route-cz-restored",
            },
            "Revision controls require a supported restored-layout workflow",
        )
        require(
            options.get("suite") == "compiler-candidate"
            and options.get("compiler_options") == workflow_configuration(workflow)
            and options["compiler_options"]["sdk"] == sdk,
            "Revision workflow differs from its registered configuration",
        )
        frontend = [c for c in registration.components if c["role"] == "frontend"]
        require(
            len(frontend) == 1
            and _name(frontend[0]["name"]) == _name(DISTRIBUTIONS[sdk]),
            "Revision frontend distribution mismatch",
        )
        require(
            ("source_build" in options) != ("published_wheel" in options),
            "Each revision requires one immutable source or release identity",
        )
        if "source_build" in options:
            origin = options.pop("source_build")
            commit = origin.get("source_commit", "")
            require(
                isinstance(commit, str)
                and re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", commit)
                and re.fullmatch(
                    r"[0-9a-f]{64}", origin.get("wheel", {}).get("sha256", "")
                ),
                "Revision source and wheel identities must be immutable",
            )
            origins.append(("source", commit))
        else:
            origin = options.pop("published_wheel")
            require(
                _name(origin.get("distribution", "")) == _name(DISTRIBUTIONS[sdk])
                and origin.get("version") == frontend[0]["version"]
                and re.fullmatch(r"[0-9a-f]{64}", origin.get("sha256", "")),
                "Revision release and wheel identities must be immutable",
            )
            origins.append(("release", origin["version"]))
        # Installed origins and frontend bytes legitimately differ by revision.
        # Each is still bound to its own registration and runtime admission.
        options.pop("installed_wheel_check", None)
        inventory = inventories[registration.stack_id]
        dependencies = inventory["dependencies"]
        require(
            inventory["dependency_lock_sha256"]
            == digest(dependencies)
            == registration.environment["dependency_lock_sha256"],
            "Revision inventory differs from the registered dependency lock",
        )
        by_name = {
            _name(d["name"]): {k: v for k, v in d.items() if k != "name"}
            for d in dependencies
        }
        require(
            len(by_name) == len(dependencies), "Ambiguous dependency distribution names"
        )
        participant = by_name.pop(_name(DISTRIBUTIONS[sdk]), None)
        require(
            participant is not None
            and participant["version"] == frontend[0]["version"],
            "Inventory lacks the registered frontend version",
        )
        require(
            inventory["image_descriptor_sha256"]
            == digest(inventory["image_descriptor"])
            == registration.environment["image_sha256"]
            and _host(inventory["host"]) == _host(registration.environment["host"]),
            "Revision inventory host or image differs from registration",
        )
        environment = deepcopy(registration.environment)
        environment.pop("dependency_lock_sha256")
        environment["host"] = _host(environment["host"])
        components = sorted(
            (c for c in registration.components if c["role"] != "frontend"),
            key=lambda c: (c["role"], c["name"]),
        )
        require(
            any(c["role"] == "harness" for c in components),
            "Revision controls require the registered harness component",
        )
        controls.append(
            {
                "configuration": configuration,
                "environment": environment,
                "dependencies": by_name,
                "components": components,
                "implementation": inventory["implementation"],
            }
        )
    require(
        origins[0][0] == origins[1][0] and origins[0] != origins[1],
        "Revision controls require distinct sources or distinct published releases",
    )
    require(
        controls[0] == controls[1],
        "Revision controls must match SDK, workflow, options, dependencies, harness and host",
    )


def verify_revision_preparation(
    preparation: Path,
    bundle: Bundle,
    registrations: dict[str, dict],
    interpreters: dict,
    admissions: dict,
) -> dict:
    """Bind an independently replayed campaign to its joint freeze and draw.

    Local records cannot establish independent timestamps or host qualification.
    A campaign admission failure remains reportable; an admitted environment must
    reproduce its frozen probe exactly.
    """
    freeze = read_json(preparation / "freeze.json")
    draw = read_json(preparation / "draw.json")
    selection = read_json(preparation / "selection.json")
    require(
        freeze["workflow_profile"] == "revision-control", "Not a joint revision freeze"
    )
    frozen = {raw["stack_id"]: raw for raw in freeze["registrations"]}
    require(
        len(freeze["registrations"]) == len(frozen) == 2 and frozen == registrations,
        "Campaign registrations differ from the joint freeze",
    )
    admitted = [Registration(**raw) for raw in frozen.values()]
    verify_revision_control(admitted, freeze["revision_environments"]["inventories"])
    require(
        freeze["selection"]
        == {
            "families": ["qaoa", "ising", "hopping", "qft", "repetition"],
            "widths": [6, 8, 12],
            "topologies": ["line", "grid"],
            "case_count": 30,
        }
        and freeze["campaign_wall_limit_seconds"] == 16200
        and all(
            r.configuration["options"]["implementation_sha256"]
            == freeze["harness_sha256"]
            for r in admitted
        ),
        "Joint freeze policy or harness identity mismatch",
    )
    environments = freeze["revision_environments"]
    require(
        interpreters == environments["interpreters"] and set(admissions) == set(frozen),
        "Campaign interpreter selection differs from freeze",
    )
    require(
        len({p["python"] for p in interpreters.values()}) == 2
        and all(Path(p["python"]).is_absolute() for p in interpreters.values()),
        "Revision controls require distinct absolute interpreter paths",
    )
    require(
        len({p["executable_sha256"] for p in interpreters.values()}) == 1
        and all(
            isinstance(p["executable_sha256"], str)
            and re.fullmatch(r"[0-9a-f]{64}", p["executable_sha256"])
            for p in interpreters.values()
        ),
        "Revision controls require identical interpreter executable bytes",
    )
    for registration in admitted:
        name = registration.stack_id
        probe = environments["probes"][name]
        verify_interpreter_admission(registration, interpreters[name], probe)
        if admissions[name]["status"] == "admitted":
            require(
                admissions[name]["interpreter_probe"] == probe,
                "Campaign interpreter probe differs from the frozen admission",
            )
    require(
        draw["freeze_sha256"] == digest(freeze)
        and selection["freeze_sha256"] == digest(freeze)
        and selection["draw_sha256"] == digest(draw)
        and draw["entropy_source"] == "secrets.token_bytes(32)"
        and draw["redraw_allowed"] is False
        and re.fullmatch(r"[0-9a-f]{64}", draw["nonce"]),
        "Joint freeze/draw binding mismatch",
    )
    full = Bundle(preparation / "full-bundle")
    cohort = Bundle(preparation / "cohort")
    require(
        selection["full_bundle_sha256"] == full.sha256
        and selection["cohort_bundle_sha256"] == cohort.sha256 == bundle.sha256
        and full.plan["application_generation"]["nonce"] == draw["nonce"]
        and cohort.plan["application_generation"] == full.plan["application_generation"]
        and full.plan["application_generation"]["base_bundle_sha256"]
        == freeze["base_bundle_sha256"],
        "Campaign bundle differs from the jointly drawn selection",
    )
    chosen = [
        c
        for c in full.plan["instances"]
        if c["arguments"]["topology"] in {"line", "grid"}
    ]
    require(
        len(chosen) == 30
        and cohort.plan["instances"] == chosen
        and cohort.plan["execution_profile"] == full.plan["execution_profile"]
        and selection["instances"] == [c["id"] for c in chosen]
        and cohort.plan["application_selection"]["freeze_sha256"] == digest(freeze)
        and cohort.plan["application_selection"]["draw_sha256"] == digest(draw),
        "Joint cohort scope differs from the frozen selection",
    )
    for case in chosen:
        for field in ("fixture", "reference_artifact"):
            require(
                (cohort.directory / case[field]).read_bytes()
                == (full.directory / case[field]).read_bytes(),
                "Selected application bytes differ from the full draw",
            )
    return {
        "freeze_sha256": digest(freeze),
        "draw_sha256": digest(draw),
        "selection_sha256": digest(selection),
        "registrations_sha256": digest(frozen),
        "interpreters_sha256": digest(interpreters),
        "bundle_sha256": bundle.sha256,
        "stack_ids": sorted(frozen),
        "instances": selection["instances"],
        "workflow": admitted[0].configuration["options"]["workflow"],
    }
