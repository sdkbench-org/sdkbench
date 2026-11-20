"""Replay a complete candidate campaign without importing participant SDKs."""
from dataclasses import asdict
from pathlib import Path

from ..p0 import Registration, ResultRecord, evaluate, evaluate_case, evaluate_workflow
from ..p0.models import digest, finite, integer, read_json, require
from ..p0.supervisor import Limits
from .provenance import file_sha256
from .response import verify_response


def replay(directory, bundle):
    root = Path(directory).resolve()
    manifest = read_json(root / 'MANIFEST.json')
    actual = {p.relative_to(root).as_posix() for p in root.rglob('*')
              if p.is_file() and p != root / 'MANIFEST.json'}
    require(actual == set(manifest['files']), 'Missing or extra campaign evidence files')
    for name, expected in manifest['files'].items():
        path = root / name
        require(path.resolve().is_relative_to(root) and not path.is_symlink(), 'Unsafe evidence path')
        require(file_sha256(path) == expected, 'Campaign evidence hash mismatch: ' + name)
    report = read_json(root / 'report.json')
    require(report['suite'] == 'compiler-candidate' and report['mode'] == 'protocol',
            'Expected a full compiler candidate campaign')
    require(report['bundle_sha256'] == bundle.sha256, 'Campaign bundle mismatch')
    require(report['publication_eligible'] is False, 'Candidate campaign is not publication-qualified')
    registrations = {name: Registration(**raw)
                     for name, raw in read_json(root / 'registrations.json').items()}
    instances = [case['id'] for case in bundle.plan['instances'] if case['kind'] == 'route']
    require(report['instances'] == instances and len(report['sdks']) == len(registrations)
            and set(report['sdks']) == set(registrations),
            'Incomplete candidate campaign scope')
    expected_pairs = {(name, instance) for name in registrations for instance in instances}
    outcomes = {(row['sdk'], row['instance']): row for row in report['outcomes']}
    require(len(outcomes) == len(report['outcomes']) and set(outcomes) == expected_pairs,
            'Missing or duplicate campaign cases')
    admissions = read_json(root / 'admission.json')
    interpreters = None
    if 'candidate_interpreters_sha256' in report or (root / 'interpreters.json').exists():
        from .environment import verify_interpreter_admission
        interpreters = read_json(root / 'interpreters.json')
        require(digest(interpreters) == report.get('candidate_interpreters_sha256')
                and set(interpreters) == set(registrations),
                'Candidate interpreter map differs from campaign scope')
        for name, selection in interpreters.items():
            require(isinstance(selection, dict) and set(selection) == {'python', 'executable_sha256'}
                    and isinstance(selection['python'], str) and Path(selection['python']).is_absolute(),
                    'Invalid candidate interpreter selection')
            if admissions[name]['status'] == 'admitted':
                value = selection['executable_sha256']
                require(isinstance(value, str) and len(value) == 64
                        and all(c in '0123456789abcdef' for c in value),
                        'Admitted interpreter lacks an executable hash')
                verify_interpreter_admission(registrations[name], selection,
                                             admissions[name]['interpreter_probe'])
    all_records = {name: [] for name in registrations}
    replayed = []
    for (name, instance), outcome in outcomes.items():
        registration = registrations[name]
        identity = registration.identity(bundle, instance)
        records = []
        statuses = []
        execution_wall_seconds = 0.0
        paths = sorted((root / name / instance).glob('*/evidence.json'))
        require(len(paths) == 10, 'Incomplete candidate block set')
        for block, path in enumerate(paths):
            require(path.parent.name == f'block-{block:02}', 'Candidate block order mismatch')
            evidence = read_json(path)
            current = [ResultRecord.from_dict(raw) for raw in evidence['records']]
            require(len(current) == 3 and all(record.identity == identity
                    and record.block == block and record.repetition == i
                    for i, record in enumerate(current)), 'Candidate record identity/count mismatch')
            verdicts = [evaluate(bundle, record, identity) for record in current]
            response = evidence.get('response')
            execution = evidence.get('execution')
            if execution is not None:
                case = bundle.cases[instance]
                limits = execution.get('limits')
                require(isinstance(limits, dict), 'Missing candidate resource limits')
                for field in ('memory_bytes', 'output_bytes', 'file_bytes', 'tasks'):
                    integer(limits.get(field), 1)
                expected_limits = asdict(Limits.for_case(case, integer(limits.get('cpu'))))
                wall_limit = finite(limits.get('wall_seconds'))
                expected_limits['wall_seconds'] = wall_limit
                require(limits == expected_limits
                        and 0 < wall_limit <= case['case_wall_limit_seconds'],
                        'Candidate resource limits differ from frozen protocol')
                elapsed = finite(execution.get('wall_seconds'))
                require(elapsed >= 0, 'Invalid candidate execution elapsed time')
                execution_wall_seconds += elapsed
                if interpreters is not None:
                    expected_argv = [interpreters[name]['python'], '-m',
                                     'sdkbench.candidates.worker', '--sdk', name,
                                     str((path.parent / 'request.json').resolve())]
                    # Evidence may be replayed after transfer. Bind the original
                    # absolute request path to the retained request's suffix.
                    argv = execution.get('argv')
                    require(isinstance(argv, list) and len(argv) == len(expected_argv)
                            and argv[:-1] == expected_argv[:-1]
                            and isinstance(argv[-1], str) and Path(argv[-1]).is_absolute()
                            and Path(argv[-1]).parts[-4:] == (name, instance, f'block-{block:02}', 'request.json'),
                            'Candidate execution used a different interpreter or worker')
                require(execution['network_policy'] == 'seccomp-deny-sockets-and-io-uring',
                        'Candidate network isolation missing')
                require(execution['enforced_cpu_set'] == str(limits['cpu']),
                        'Candidate must be pinned to one registered CPU')
            if response is not None:
                request = read_json(path.parent / 'request.json')
                expected_request = bundle.request(identity, block) | {
                    'kind': 'route', 'execution_mode': 'protocol', 'suite': 'compiler-candidate',
                    'candidate_registration': registration.to_dict()}
                if interpreters is not None:
                    expected_request['candidate_interpreter'] = interpreters[name]
                    require(response.get('candidate_interpreter') == interpreters[name],
                            'Candidate response interpreter mismatch')
                else:
                    require('candidate_interpreter' not in response,
                            'Candidate response lacks a retained interpreter map')
                require(request == expected_request and response['request_sha256'] == digest(request),
                        'Candidate request/seed binding mismatch')
                require(execution is not None and response['worker_pid'] == execution['pid'],
                        'Candidate worker is not the supervised process')
                verify_response(registration, response, path.parent)
                require(response['records'] == evidence['records'], 'Response records differ from evaluated records')
                warmups = [ResultRecord.from_dict(raw) for raw in response['warmups']]
                require(len(warmups) == 2 and all(record.identity == identity
                        and record.block == block and record.repetition == i
                        for i, record in enumerate(warmups)), 'Candidate warmup identity/count mismatch')
                warmup_verdicts = [evaluate(bundle, record, identity) for record in warmups]
                require([v.status for v in verdicts]
                        == [v['status'] for v in evidence['record_verdicts']], 'Measured verdict replay disagrees')
                require([v.status for v in warmup_verdicts]
                        == [v['status'] for v in evidence['warmup_verdicts']], 'Warmup verdict replay disagrees')
                verdicts = warmup_verdicts + verdicts
            failed = [v.status for v in verdicts if v.status != 'accepted']
            status = failed[0] if failed else 'accepted'
            if evidence.get('case_budget_remaining_seconds', 1) <= 0 and status == 'accepted':
                status = 'timeout'
            require(status == evidence['block_verdict']['status'], 'Candidate block verdict replay disagrees')
            if status == 'accepted':
                require(response is not None and execution is not None
                        and execution['execution_status'] == 'completed'
                        and admissions[name]['status'] == 'admitted',
                        'Accepted block lacks successful admission and supervised execution')
                require(type(execution.get('returncode')) is int and execution['returncode'] == 0,
                        'Accepted block has an unsuccessful process exit')
                integer(execution.get('kernel_memory_peak_bytes'), 1)
            statuses.append(status)
            records.extend(current)
        independent = evaluate_case(bundle, identity, [r.to_dict() for r in records])
        failed = [status for status in statuses if status != 'accepted']
        status = failed[0] if failed else independent.status
        if status == 'accepted':
            require(execution_wall_seconds <= bundle.cases[instance]['case_wall_limit_seconds'],
                    'Accepted candidate case exceeds its cumulative execution wall budget')
        require(outcome['record_count'] == 30 and outcome['blocks'] == 10
                and outcome['case_verdict']['status'] == status,
                'Candidate case report replay disagrees')
        all_records[name].extend(r.to_dict() for r in records)
        replayed.append({'sdk': name, 'instance': instance, 'status': status})
    for name, records in all_records.items():
        verdict = evaluate_workflow(bundle, 'W03', records)
        failed = [row['status'] for row in replayed if row['sdk'] == name and row['status'] != 'accepted']
        require(report['workflows'][name]['W03']['status'] == (failed[0] if failed else verdict.status),
                'Candidate workflow replay disagrees')
    return {'schema_version': 1, 'bundle_sha256': bundle.sha256, 'cases': replayed,
            'files_verified': len(actual), 'blocks_verified': len(expected_pairs) * 10,
            'scope': 'independent record replay; build attestation and publication review remain separate',
            'publication_eligible': False}
