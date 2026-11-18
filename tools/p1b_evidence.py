#!/usr/bin/env python3
"""Replay P1b records, full cases, workflow completeness and registration bindings."""
import argparse
import json
from pathlib import Path
from sdkbench.p0 import Bundle, Registration, evaluate_case, evaluate_workflow
from sdkbench.p0.models import Identity, canonical_bytes, read_json, require
from p1a_evidence import verify, archive


def verify_cases(root, bundle):
    root = Path(root).resolve();summary = verify(root, bundle)
    checked = []
    for report_path in sorted(root.glob('*/report.json')):
        folder = report_path.parent;report = read_json(report_path)
        require(report['suite'] == 'p1b' and report['mode'] == 'protocol', 'Expected a P1b full-case campaign')
        registrations = {sdk: Registration(**raw) for sdk,raw in read_json(folder/'registrations.json').items()}
        workflow_records = {sdk: {} for sdk in registrations}
        report_cases = []
        for outcome in report['outcomes']:
            sdk = outcome['sdk'];instance = outcome['instance'];identity = registrations[sdk].identity(bundle, instance)
            blocks = [read_json(p) for p in sorted((folder/sdk/instance).glob('*/evidence.json'))]
            records = [r for block in blocks for r in block['records']]
            require(len(blocks) == 10 and len(records) == 30, 'Incomplete P1b numeric case')
            for block in blocks:
                all_records = block['records'] + (block.get('response') or {}).get('warmups', [])
                require(all(Identity(**r['identity']) == identity for r in all_records), 'Record registration binding mismatch')
                execution = block.get('execution')
                if execution:
                    case = bundle.cases[instance];limits = execution['limits']
                    require(limits['memory_bytes'] == case['process_memory_limit_gib'] * 1024**3, 'Memory cap differs from protocol')
                    require(0 < limits['wall_seconds'] <= case['case_wall_limit_seconds'], 'Wall cap exceeds protocol')
                    require(execution['network_policy'] == 'seccomp-deny-sockets-and-io-uring', 'Missing network isolation')

            verdict = evaluate_case(bundle, identity, records).to_dict()
            # An adverse warmup or cumulative-budget overrun also invalidates the case.
            failed = [b['block_verdict'] for b in blocks if b['block_verdict']['status'] != 'accepted']
            expected_status = failed[0]['status'] if failed else verdict['status']
            require(expected_status == outcome['case_verdict']['status'], 'Case replay disagrees')
            require(outcome['record_count'] == len(records) and outcome['blocks'] == len(blocks), 'Report count mismatch')
            workflow = bundle.cases[instance]['workflow']
            workflow_records[sdk].setdefault(workflow, []).extend(records)
            report_cases.append({'sdk': sdk, 'instance': instance, 'status': expected_status,
                            'independent_case_status': verdict['status'], 'records': len(records)})
        for sdk, workflows in workflow_records.items():
            for workflow, records in workflows.items():
                verdict = evaluate_workflow(bundle, workflow, records).to_dict()
                failed = [c for c in report_cases if c['sdk'] == sdk and bundle.cases[c['instance']]['workflow'] == workflow and c['status'] != 'accepted']
                expected = failed[0]['status'] if failed else verdict['status']
                require(report['workflows'][sdk][workflow]['status'] == expected, 'Workflow replay disagrees')
        checked.extend(report_cases)
    require(checked, 'No P1b cases found')
    summary['cases_verified'] = checked
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--directory', type=Path, required=True)
    parser.add_argument('--bundle', type=Path, required=True)
    parser.add_argument('--archive', type=Path)
    parser.add_argument('--summary', type=Path)
    args = parser.parse_args();summary = verify_cases(args.directory, Bundle(args.bundle))
    if args.archive:summary['archive_sha256'] = archive(args.directory, args.archive)
    if args.summary:
        require(not args.summary.exists(), 'Never overwrite replay evidence')
        args.summary.write_bytes(canonical_bytes(summary))
    print(json.dumps({'blocks_verified': summary['blocks_verified'], 'cases_verified': len(summary['cases_verified']),
                      'files_verified': summary['files_verified'], 'publication_eligible': False}, indent=2))
    return 0


if __name__ == '__main__':raise SystemExit(main())
