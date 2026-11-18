#!/usr/bin/env python3
"""Run real P1b cases under strict Linux controls and retain every outcome."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import signal
import sys
from sdkbench.p0 import Bundle
from sdkbench.p0.models import canonical_bytes, read_json, require
from sdkbench.p0.supervisor import Limits, run_command
from sdkbench.p1a.campaign import run_campaign


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--bundle', type=Path, default=Path('docs/implementation'))
    parser.add_argument('--directory', type=Path, required=True)
    parser.add_argument('--cgroup-parent', type=Path, required=True)
    parser.add_argument('--scope', choices=('all-protocol', 'small-protocol'), default='all-protocol')
    args = parser.parse_args();root = args.directory.resolve();root.mkdir(parents=True, exist_ok=True)
    require(not any(root.iterdir()), 'Evidence directory must be empty')
    bundle = Bundle(args.bundle);cpu = min(os.sched_getaffinity(0))
    environment = {k: os.environ[k] for k in ['LD_LIBRARY_PATH'] if k in os.environ}
    profile = read_json(args.bundle/'p1b-profile.json')
    context = {'schema_version': 1, 'source_commit': os.environ.get('GITHUB_SHA'), 'github_run_id': os.environ.get('GITHUB_RUN_ID'),
               'runner_image_version': os.environ.get('ImageVersion'), 'cpu': cpu, 'runtime_environment': environment,
               'publication_eligible': False, 'scope': args.scope, 'profile': profile,
               'interpretation': 'engineering integration; not a global SDK ranking'}
    (root/'context.json').write_bytes(canonical_bytes(context))
    try:
        # A shortened test-only alarm proves that native code holding the GIL is terminated.
        # Production native compilations retain the frozen 120-second cap.
        script = 'from sdkbench.p1b.common import compile_deadline; import ctypes\nwith compile_deadline(.05):ctypes.PyDLL(None).sleep(3)'
        result = run_command([sys.executable, '-c', script], cwd=root, cgroup_parent=args.cgroup_parent,
                             limits=Limits.for_case(bundle.cases['ROUTE-LINE-06'], cpu), environment=environment)
        (root/'compile-deadline-check.json').write_bytes(canonical_bytes(result))
        require(result['returncode'] == -signal.SIGALRM, 'Native compiler-stage kernel alarm failed')
        selected = None if args.scope == 'all-protocol' else ['GRAD-04', 'DYN-04-S32', 'ROUTE-LINE-06']
        report = run_campaign(bundle, directory=root/args.scope, cgroup_parent=args.cgroup_parent, cpu=cpu,
                              suite='p1b', instances=selected, mode='protocol', runtime_environment=environment)
        # This checks accounting, never turns an unsupported verdict into acceptance.
        # Unknown failures (including any failure in FlagQuantum) fail integration CI.
        unexpected = []
        for row in report['outcomes']:
            gaps = [g for g in profile['expected_capability_gaps'] if g['sdk'] == row['sdk'] and g['kind'] == bundle.cases[row['instance']]['kind']]
            expected = gaps[0]['status'] if gaps else 'accepted'
            if row['case_verdict']['status'] != expected:unexpected.append(row)
        (root/'integration-summary.json').write_bytes(canonical_bytes({'outcomes': report['outcomes'], 'unexpected': unexpected,
                     'scope': args.scope, 'publication_eligible': False, 'capability_gaps_remain_non_success': True}))
        print(json.dumps({'outcomes': report['outcomes'], 'unexpected': unexpected}, indent=2, allow_nan=False))
        return int(bool(unexpected))
    finally:
        files = {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                 for p in sorted(root.rglob('*')) if p.is_file() and p.name != 'MANIFEST.json'}
        (root/'MANIFEST.json').write_bytes(canonical_bytes({'schema_version': 1, 'files': files}))


if __name__ == '__main__':raise SystemExit(main())
