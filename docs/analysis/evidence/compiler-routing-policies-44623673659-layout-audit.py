"""Check retained control/layout coverage and reconcile independent error values."""
from collections import Counter
from copy import deepcopy
import json
from pathlib import Path
import signal
import sys

signal.alarm(600)
sys.path.insert(0, str(Path.cwd() / "src"))
from sdkbench.p0.models import digest

root = Path(sys.argv[1]).resolve()
campaign = root / "evidence/campaign"

def read(path):
    return json.loads(path.read_text())

def write(path, value):
    with path.open("x") as out:
        json.dump(value, out, indent=2, sort_keys=True, allow_nan=False)
        out.write("\n")

registrations = read(campaign / "registrations.json")
assert len(registrations) == 4
policies = []
for registration in registrations.values():
    config = registration["configuration"]
    options = config["options"]["compiler_options"]["options"]
    assert config["threads"] == 1 and options["initial_layout"] == "identity"
    policies.append(options["postprocessing"])
assert all(policy == policies[0] for policy in policies)
assert policies[0]["timed"] is True and policies[0]["final_layout"] == "identity"

blocks = Counter()
execution_statuses = Counter()
cpu_sets = Counter()
records = Counter()
for path in sorted(campaign.glob("*/*/block-*/evidence.json")):
    evidence = read(path)
    blocks[evidence["block_verdict"]["status"]] += 1
    execution = evidence.get("execution")
    if execution is None:
        execution_statuses["no-retained-execution"] += 1
    else:
        assert execution["limits"]["memory_bytes"] == 16 * 2**30
        assert execution["network_policy"] == "seccomp-deny-sockets-and-io-uring"
        cpu_sets[execution["enforced_cpu_set"]] += 1
        assert execution["enforced_cpu_set"] == str(execution["limits"]["cpu"])
        execution_statuses[execution["execution_status"]] += 1
    response = evidence.get("response")
    for phase in ("warmups", "records"):
        retained = response[phase] if response is not None else evidence.get(phase, [])
        verdict_key = "warmup_verdicts" if phase == "warmups" else "record_verdicts"
        verdicts = evidence.get(verdict_key, [])
        for index, record in enumerate(retained):
            records[phase + ":retained"] += 1
            status = verdicts[index]["status"] if index < len(verdicts) else record["status"]
            records[phase + ":" + status] += 1
            if status == "accepted":
                placement = record["payload"]["final_layout"]
                assert placement == list(range(len(placement)))
                records[phase + ":accepted-identity-layout"] += 1
assert sum(blocks.values()) == 1200
write(root / "local-layout-resource-check.json", {
    "profile": "routing-policies", "initial_identity_registered_for_all": True,
    "common_timed_restoration_policy": policies[0],
    "external_restoration_workflows": sorted(r["configuration"]["options"]["workflow"] for r in registrations.values()),
    "native_restoration_workflows": [],
    "block_statuses": dict(blocks), "execution_statuses": dict(execution_statuses),
    "record_and_layout_counts": dict(records), "enforced_cpu_sets": dict(cpu_sets),
    "memory_cap_bytes": 16 * 2**30,
    "controls_recorded_for_all_retained_executions": True,
    "scope": "Accepted payloads have identity layout. Failed and unavailable execution evidence remains counted; recorded control policy is not independent kernel attestation.",
    "publication_eligible": False,
})
summary = read(root / "local-summary.json")
reconstructed = deepcopy(summary)
differences = []
for row in reconstructed["cases"]:
    errors = []
    for path in sorted((campaign / row["sdk"] / row["instance"]).glob("block-*/evidence.json")):
        for verdict in read(path).get("record_verdicts", []):
            if verdict["status"] == "accepted":
                errors.append(verdict["metrics"]["max_semantic_error"])
    hosted_error = max(errors) if errors else None
    if row["maximum_semantic_error"] != hosted_error:
        differences.append({"sdk": row["sdk"], "instance": row["instance"],
            "local_maximum_semantic_error": row["maximum_semantic_error"],
            "hosted_maximum_semantic_error": hosted_error})
    row["maximum_semantic_error"] = hosted_error
expected = read(root / "evidence/comparisons.json")["source_summary_sha256"]
assert digest(reconstructed) == expected
assert not {"flagquantum", "qiskit", "cirq"}.intersection(sys.modules)
write(root / "local-summary-digest-reconciliation.json", {
    "schema_version": 1, "profile": "routing-policies", "differences": differences,
    "only_fields_replaced": "cases[*].maximum_semantic_error",
    "all_other_local_summary_fields_unchanged": True,
    "hosted_summary_sha256": expected,
    "reconstructed_hosted_summary_sha256": digest(reconstructed),
    "reconstructed_digest_matches_hosted": True,
    "interpretation": "Both local and hosted semantic errors remain retained. Only their maxima are substituted to verify the original hosted digest; acceptance is unchanged.",
})
print(json.dumps({"blocks": dict(blocks), "execution_statuses": dict(execution_statuses),
    "record_layout_counts": dict(records), "semantic_error_differences": len(differences),
    "reconstructed_digest_matches_hosted": True}))
