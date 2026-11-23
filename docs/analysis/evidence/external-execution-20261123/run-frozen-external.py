"""Execute one frozen external campaign using the retained reviewed phase helper."""

from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os, signal, sys, time

if sys.flags.optimize:
    raise RuntimeError("Study admission requires unoptimized Python checks")

ROOT = Path("/data/sdkbench-external-inputs-staged-20261123")
OLD = Path("/data/sdkbench-compiler-qualification-20261123")
HARNESS = ROOT / "harness"
PARENT = Path("/sys/fs/cgroup/sdkbench-external-campaign-20261123")
STUDY = ROOT / "campaign-attempt-1"
PYTHON = OLD / "qualification-env/bin/python"
FREEZE = ROOT / "public-external-freeze.json"


def interrupt_owned_driver(signum, frame):
    raise InterruptedError(f"Study driver received signal {signum}")


for owned_signal in (signal.SIGHUP, signal.SIGTERM, signal.SIGINT):
    signal.signal(owned_signal, interrupt_owned_driver)


def sha(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


freeze = json.loads(FREEZE.read_text())
assert freeze["participant_execution_started"] is False
assert not STUDY.exists() and not PARENT.exists()
assert sha(Path(__file__)) == freeze["study_driver_sha256"]
helper = OLD / "run-frozen-routing-reviewed.py"
assert sha(helper) == freeze["reviewed_phase_helper_sha256"]
scope = {}
exec(
    compile(
        helper.read_text().split("assert not STUDY.exists()")[0], str(helper), "exec"
    ),
    scope,
)
scope.update(ROOT=ROOT, HARNESS=HARNESS, PARENT=PARENT, PYTHON=PYTHON, STUDY=STUDY)
scope["ENV"] = {
    **os.environ,
    "PYTHONPATH": str(HARNESS / "src"),
    "OMP_NUM_THREADS": "1",
    "OPENBLAS_NUM_THREADS": "1",
    "MKL_NUM_THREADS": "1",
    "NUMEXPR_NUM_THREADS": "1",
    "PYTHONDONTWRITEBYTECODE": "1",
    "PYTHONOPTIMIZE": "0",
    "MPLCONFIGDIR": str(ROOT / "measurement-mpl-cache"),
}


def verify_files():
    for base, section in [
        (ROOT, "input_sha256"),
        (HARNESS, "harness_python_sha256"),
        (OLD, "wheel_sha256"),
    ]:
        for relative, expected in freeze[section].items():
            assert sha(base / relative) == expected, (section, relative)


verify_files()
receipt = ROOT / "ci-gate.json"
assert sha(receipt) == freeze["ci_receipt_sha256"]
ci = json.loads(receipt.read_text())
assert (
    ci["harness_revision"] == freeze["harness_revision"]
    and ci["all_required_checks_passed"] is True
)
assert ci["check_count"] == 14
now = datetime.now(timezone.utc)
assert now <= datetime.fromisoformat(
    "2026-11-23T09:51:41+00:00"
), "Insufficient original reservation window"
assert (
    datetime.fromisoformat("2026-11-24T05:36:41+00:00") - now
).total_seconds() >= 71100
assert not scope["workers"](), "Foreign CI must drain naturally"
for name in ["resource-controls.json", "native-controls.json"]:
    assert json.loads((ROOT / name).read_text())["returncode"] == 0
before = scope["snapshot"]()
(ROOT / "host-before.json").write_text(json.dumps(before, indent=2) + "\n")
prospective = json.loads((ROOT / "prospective-host-before.json").read_text())
mutable_files = {"/proc/cpuinfo", "/proc/meminfo"}
assert (
    before["packages"] == prospective["packages"]
), "OS package baseline changed after public preparation"
assert {k: v for k, v in before["files"].items() if k not in mutable_files} == {
    k: v for k, v in prospective["files"].items() if k not in mutable_files
}, "Stable host baseline changed after public preparation"
assert before["host"].strip() == "bm-srwl-sh-zone9-d-bw1100-144g-1-10"
assert (
    before["files"][
        "/sys/devices/system/cpu/cpu96/topology/thread_siblings_list"
    ].strip()
    == "96,288"
)
topology_rows = [
    line.split() for line in before["topology"].splitlines()[1:] if line.strip()
]
assert len({(row[1], row[2]) for row in topology_rows if row[4] == "yes"}) >= 8
meminfo = {
    line.split(":", 1)[0]: int(line.split()[1]) * 1024
    for line in before["files"]["/proc/meminfo"].splitlines()
    if len(line.split()) == 3 and line.split()[2] == "kB"
}
assert meminfo["MemTotal"] >= 64 * 1024**3 and meminfo["MemAvailable"] >= 16 * 1024**3
os.sched_setaffinity(0, {96})
time.sleep(5)
stat_after = Path("/proc/stat").read_text()
assert not scope["workers"]()
activity = {}
for cpu in [96, 288]:

    def ticks(text):
        return [
            int(v)
            for line in text.splitlines()
            if line.startswith("cpu" + str(cpu) + " ")
            for v in line.split()[1:]
        ]

    delta = [y - x for x, y in zip(ticks(before["stat"]), ticks(stat_after))]
    total = sum(delta[:8])
    busy = total - delta[3] - delta[4]
    activity[str(cpu)] = {"ticks": delta, "busy_fraction": busy / total}
    assert busy == 0, "Selected core or sibling was active during admission"
(ROOT / "host-idle-interval.json").write_text(
    json.dumps(
        {
            "seconds": 5,
            "before": before["stat"],
            "after": stat_after,
            "activity": activity,
        },
        indent=2,
    )
    + "\n"
)
PARENT.mkdir(exist_ok=False)
(PARENT / "cgroup.subtree_control").write_text("+cpu +cpuset +memory +pids")
admission = {
    "freeze_sha256": sha(FREEZE),
    "ci_receipt_sha256": sha(receipt),
    "host_before_sha256": sha(ROOT / "host-before.json"),
    "admitted_at_utc": datetime.now(timezone.utc).isoformat(),
    "reservation_end_utc": "2026-11-24T05:36:41Z",
    "publication_eligible": False,
    "baseline_independent_attestation": False,
}
(ROOT / "admission.json").write_text(json.dumps(admission, indent=2) + "\n")
try:
    argv = [
        str(PYTHON),
        "-m",
        "sdkbench.candidates.cli",
        "run",
        "--bundle",
        str(ROOT / "prepared/bundle"),
        "--cpu",
        "96",
        "--cgroup-parent",
        str(PARENT),
        "--directory",
        str(STUDY),
    ]
    for stack in freeze["registrations"]:
        argv += ["--registration", str(ROOT / "registrations" / (stack + ".json"))]
    campaign = scope["phase"]("external-campaign-attempt-1", argv, 50400)
    verify_files()
    assert campaign["returncode"] in [
        0,
        1,
    ], "Campaign process failed outside retained participant outcomes"
    replay = scope["phase"](
        "external-replay-attempt-1",
        [
            str(PYTHON),
            "-m",
            "sdkbench.candidates.cli",
            "replay",
            "--bundle",
            str(ROOT / "prepared/bundle"),
            "--directory",
            str(STUDY),
        ],
        10800,
    )
    assert replay["returncode"] == 0, "Independent replay did not pass"
    summary = scope["phase"](
        "external-summary-attempt-1",
        [
            str(PYTHON),
            str(HARNESS / "tools/compiler_candidate_report.py"),
            "--bundle",
            str(ROOT / "prepared/bundle"),
            "--directory",
            str(STUDY),
            "--output",
            str(ROOT / "external-summary.json"),
        ],
        900,
    )
    assert summary["returncode"] == 0, "Bounded numerical summary did not complete"
except BaseException as error:
    (ROOT / "study-interruption.json").write_text(
        json.dumps(
            {
                "type": type(error).__name__,
                "reason": str(error),
                "utc": datetime.now(timezone.utc).isoformat(),
                "never_rerun_favorable_subsets": True,
            },
            indent=2,
        )
        + "\n"
    )
    raise
finally:
    after = scope["snapshot"]()
    (ROOT / "host-after.json").write_text(json.dumps(after, indent=2) + "\n")
    mutable = {"/proc/cpuinfo", "/proc/meminfo"}
    comparison = {
        "same_os_packages": before["packages"] == after["packages"],
        "same_stable_host_files": {
            k: v for k, v in before["files"].items() if k not in mutable
        }
        == {k: v for k, v in after["files"].items() if k not in mutable},
        "remaining_worker_cgroups": [p.name for p in PARENT.iterdir() if p.is_dir()],
        "foreign_ci_workers": scope["workers"](),
        "publication_eligible": False,
    }
    (ROOT / "host-baseline-comparison.json").write_text(
        json.dumps(comparison, indent=2) + "\n"
    )
    if (
        not comparison["remaining_worker_cgroups"]
        and not (PARENT / "cgroup.procs").read_text().strip()
    ):
        PARENT.rmdir()
    print(
        json.dumps(
            {
                "phase": "study-finalization",
                "comparison": comparison,
                "restore_original_runner_labels_required": True,
            }
        ),
        flush=True,
    )
