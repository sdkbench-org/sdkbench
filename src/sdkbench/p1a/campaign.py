"""Serial native task process blocks under common P0 acceptance and kernel resource limits."""
from contextlib import contextmanager
from dataclasses import replace
from importlib import metadata
import json
from pathlib import Path
import platform
import signal
import sys
import time
from ..p0 import Registration, ResultRecord, Verdict, evaluate, evaluate_case, evaluate_workflow
from ..p0.models import canonical_bytes, digest, keys, read_json, require
from ..p0.supervisor import IsolationUnavailable, Limits, run_command
from .common import DISTRIBUTIONS, VERSIONS, SDKS, WORKFLOWS
from .provenance import capture_environment, distribution_fingerprint, source_fingerprint


class ActiveCaseBudget:
    """Accumulate only this case's elapsed work across counterbalanced blocks."""
    def __init__(self, wall_seconds, clock=time.perf_counter):
        self.wall_seconds = wall_seconds; self.clock = clock; self.used = 0.; self.started = None

    @property
    def remaining(self):
        active = self.clock() - self.started if self.started is not None else 0.
        return max(0., self.wall_seconds - self.used - active)

    @contextmanager
    def active(self):
        require(self.started is None, 'Case budget already active')
        self.started = self.clock()
        try:yield self
        finally:self.used += self.clock() - self.started; self.started = None


def write(path, value):path.write_bytes(canonical_bytes(value))


def registration(sdk, environment, components, suite='p1a'):
    task_options = {}
    if suite == 'p1b':
        from ..p1b.common import CONFIGURATIONS
        task_options = CONFIGURATIONS[sdk]
    return Registration(sdk, components, {'profile': 'CPU1-FP64', 'precision': 'float64/complex128', 'threads': 1,
                        'options': {'task_configuration': task_options, 'suite': suite, 'sdk': sdk, 'expected_version': VERSIONS[sdk], 'implementation': source_fingerprint(),
                                    'backend': {'flagquantum': 'pytorch-statevector-cpu', 'qiskit': 'Statevector/StatevectorSampler',
                                                'cirq': 'Simulator-complex128'}[sdk]}},
                        {'python': platform.python_version(), 'os': platform.platform(),
                         'image_sha256': environment['image_descriptor_sha256'],
                         'dependency_lock_sha256': environment['dependency_lock_sha256'], 'host': environment['host']})


def _failure_records(identity, block, count, status, reason):
    return [ResultRecord(identity, block, r, status, reason=reason) for r in range(count)]


def run_block(bundle, identity, sdk, block, *, mode, directory, cgroup_parent, cpu, budget, runtime_environment=None, suite='p1a', candidate=None, interpreter=None):
    directory = Path(directory); directory.mkdir(parents=True, exist_ok=False)
    case = bundle.cases[identity.instance_id]; kind = case['kind']; protocol = mode == 'protocol'
    count = 3 if protocol and kind != 'sampling' else 1; warmup_count = 2 if protocol and kind != 'sampling' else 0
    request = {**bundle.request(identity, block), 'kind': kind, 'execution_mode': mode, 'suite': suite}
    if candidate is not None:
        require(suite == 'compiler-candidate' and kind == 'route', 'Candidate execution is routing-only')
        require(candidate.identity(bundle, identity.instance_id) == identity, 'Candidate registration identity mismatch')
        request['candidate_registration'] = candidate.to_dict()
    if interpreter is not None:
        require(candidate is not None, 'Interpreter selection requires a candidate registration')
        request['candidate_interpreter'] = interpreter
    write(directory / 'request.json', request)
    execution = None; response = None; warmup_verdicts = []; verdicts = []
    if budget.remaining <= 0:
        records = _failure_records(identity, block, count, 'timeout', 'Complete case wall budget exhausted before this block')
    else:
        try:
            if interpreter is not None:
                from ..candidates.environment import interpreter_identity
                require(interpreter_identity(interpreter['python']) == interpreter,
                        'Candidate interpreter changed before launch')
            elif candidate is not None:
                from ..candidates.provenance import verify_runtime
                verify_runtime(candidate)
            limits = replace(Limits.for_case(case, cpu), wall_seconds=min(case['case_wall_limit_seconds'], budget.remaining))
            module = 'sdkbench.p1a.worker' if candidate is None else 'sdkbench.candidates.worker'
            python = sys.executable if interpreter is None else interpreter['python']
            execution = run_command([python, '-m', module, '--sdk', sdk, str((directory / 'request.json').resolve())],
                                    cwd=directory, cgroup_parent=cgroup_parent, limits=limits, environment=runtime_environment)
            if execution['execution_status'] != 'completed':
                status = execution['execution_status']
                if kind == 'route' and execution.get('returncode') == -signal.SIGALRM:status = 'timeout'
                mapped = status if status in ('timeout', 'out-of-memory') else 'access-blocked' if status == 'isolation-failed' else 'error'
                records = _failure_records(identity, block, count, mapped, 'Supervisor outcome: ' + status)
            else:
                (directory / 'response.json').write_text(execution['stdout'], encoding='utf-8')
                response = read_json(directory / 'response.json')
                extra = ('candidate_admission', 'compiler_evidence_files') if candidate is not None else ()
                if interpreter is not None:
                    extra += ('candidate_interpreter',)
                keys(response, ('schema_version', 'request_sha256', 'sdk', 'sdk_version', 'worker_pid', 'sdk_import_wall_seconds', 'warmups', 'records', 'native_audit', 'warnings') + extra)
                require(response['schema_version'] == 1 and response['sdk'] == sdk and response['request_sha256'] == digest(request), 'Worker response binding mismatch')
                require(response['worker_pid'] == execution['pid'], 'Worker PID does not match supervised process')
                if interpreter is not None:
                    require(response['candidate_interpreter'] == interpreter,
                            'Worker interpreter response binding mismatch')
                if candidate is None:
                    require(response['sdk_version'] == VERSIONS[sdk], 'Worker SDK version differs from registration')
                else:
                    from ..candidates.response import verify_response
                    verify_response(candidate, response, directory)
                require(len(response['records']) == count and len(response['warmups']) == warmup_count, 'Wrong block warmup/repetition count')
                records = [ResultRecord.from_dict(r) for r in response['records']]
                for r, record in enumerate(records):
                    require(record.identity == identity and record.block == block and record.repetition == r, 'Worker returned a different invocation')
                for r, raw in enumerate(response['warmups']):
                    record = ResultRecord.from_dict(raw)
                    require(record.identity == identity and record.block == block and record.repetition == r, 'Wrong warmup identity')
                    warmup_verdicts.append(evaluate(bundle, record, identity))
        except IsolationUnavailable as exc:
            records = _failure_records(identity, block, count, 'access-blocked', str(exc))
        except ImportError as exc:
            records = _failure_records(identity, block, count, 'install-failed', str(exc))
        except (OSError, ValueError, KeyError, TypeError) as exc:
            records = _failure_records(identity, block, count, 'error', f'Invalid worker/execution evidence: {type(exc).__name__}: {exc}')
    verdicts = [evaluate(bundle, record, identity) for record in records]
    bad = [v for v in warmup_verdicts + verdicts if v.status != 'accepted']
    block_verdict = bad[0] if bad else Verdict('accepted')
    if budget.remaining <= 0 and block_verdict.status == 'accepted':block_verdict = Verdict('timeout', ('Case budget exhausted during result validation',))
    evidence = {'schema_version': 1, 'sdk': sdk, 'instance': identity.instance_id, 'block': block, 'mode': mode,
                'execution': execution, 'response': response, 'records': [r.to_dict() for r in records],
                'record_verdicts': [v.to_dict() for v in verdicts], 'warmup_verdicts': [v.to_dict() for v in warmup_verdicts],
                'block_verdict': block_verdict.to_dict(), 'case_budget_remaining_seconds': budget.remaining}
    write(directory / 'evidence.json', evidence)
    return evidence


def run_campaign(bundle, *, directory, cgroup_parent, cpu, sdks=SDKS, instances=None, mode='protocol', runtime_environment=None, suite='p1a', candidates=None, candidate_interpreters=None):
    require(mode in ('protocol', 'qualification'), 'Unknown execution mode')
    if candidate_interpreters is not None:
        require(candidates is not None and isinstance(candidate_interpreters, dict)
                and set(candidate_interpreters) == set(candidates)
                and all(isinstance(value, str) and Path(value).is_absolute()
                        for value in candidate_interpreters.values()),
                'Provide one absolute interpreter path for every candidate')
        runtime_environment = {**(runtime_environment or {}),
                               'PYTHONPATH': str(Path(__file__).resolve().parents[2])}
    if candidates is not None:
        import re
        require(suite == 'compiler-candidate' and isinstance(candidates, dict) and candidates,
                'Candidate registrations require the candidate suite')
        require(all(isinstance(value, Registration) and key == value.stack_id
                    and re.fullmatch('[a-z][a-z0-9-]*', key) and key not in SDKS
                    for key, value in candidates.items()), 'Invalid candidate registrations')
        sdks = tuple(candidates)
        selected_workflows = ('W03',)
    else:
        require(sdks and len(set(sdks)) == len(sdks) and set(sdks) <= set(SDKS), 'Invalid SDK selection')
        require(suite in ('p1a', 'p1b'), 'Unknown adapter suite')
    if candidates is None and suite == 'p1b':
        from ..p1b.common import WORKFLOWS as selected_workflows
    elif candidates is None:selected_workflows = WORKFLOWS
    available = [c['id'] for c in bundle.plan['instances'] if c['workflow'] in selected_workflows]
    selected = list(instances) if instances is not None else available
    require(selected and len(set(selected)) == len(selected) and set(selected) <= set(available), 'Invalid suite case selection')
    directory = Path(directory).resolve(); directory.mkdir(parents=True, exist_ok=True)
    require(not any(directory.iterdir()), 'Never overwrite campaign evidence')
    environment = capture_environment(); write(directory / 'environment.json', environment)
    components = {}; registrations = {}; admissions = {}
    framework = {'name': 'sdkbench', 'version': environment['implementation']['sdkbench_version'], 'role': 'harness',
                 'artifact_sha256': environment['implementation'].get('runtime_source_sha256', environment['implementation']['p0_p1a_source_sha256'])}
    cache = {}; interpreters = {}
    for sdk in sdks:
        if candidates is not None:
            registrations[sdk] = candidates[sdk]
            try:
                probe = None
                if candidate_interpreters is not None:
                    from ..candidates.environment import admit_interpreter, interpreter_identity
                    interpreters[sdk] = {'python': candidate_interpreters[sdk], 'executable_sha256': None}
                    interpreters[sdk] = interpreter_identity(candidate_interpreters[sdk])
                    probe = admit_interpreter(candidates[sdk], interpreters[sdk], runtime_environment or {})
                else:
                    from ..candidates.provenance import verify_runtime
                    verify_runtime(candidates[sdk])
                admissions[sdk] = {'status': 'admitted', 'reason': None}
                if probe is not None:
                    admissions[sdk]['interpreter_probe'] = probe
            except (OSError, ValueError, KeyError, TypeError, ImportError) as exc:
                admissions[sdk] = {'status': 'install-failed' if isinstance(exc, ImportError) else 'access-blocked',
                                   'reason': f'Candidate admission failed: {type(exc).__name__}: {exc}'}
            continue
        entries = [framework]; reason = None
        dependencies = [DISTRIBUTIONS[sdk], 'numpy'] + (['torch'] if sdk == 'flagquantum' else ['sympy', 'networkx'] if sdk == 'cirq' else [])
        if suite == 'p1b' and sdk == 'qiskit':dependencies.append('qiskit-algorithms')
        for name in dependencies:
            try:
                if name not in cache:cache[name] = distribution_fingerprint(name)
                component = cache[name]; entries.append({k: component[k] for k in ('name', 'version', 'artifact_sha256')} | {'role': 'frontend' if name == DISTRIBUTIONS[sdk] else 'gradient-extension' if name == 'qiskit-algorithms' else 'numerical-dependency'})
                if name == DISTRIBUTIONS[sdk] and component['version'] != VERSIONS[sdk]:reason = 'Pinned package mismatch: ' + name + '==' + component['version']
                if name == 'qiskit-algorithms' and component['version'] != '0.4.0':reason = 'Pinned package mismatch: qiskit-algorithms==' + component['version']
            except metadata.PackageNotFoundError:reason = 'Required distribution missing: ' + name
        components[sdk] = entries; registrations[sdk] = registration(sdk, environment, entries, suite)
        admissions[sdk] = {'status': 'install-failed' if reason and 'missing' in reason else 'access-blocked' if reason else 'admitted', 'reason': reason}
    write(directory / 'registrations.json', {s: registrations[s].to_dict() for s in sdks})
    write(directory / 'admission.json', admissions)
    if candidate_interpreters is not None:
        write(directory / 'interpreters.json', interpreters)
    cases = {}; budgets = {}; identities = {}
    for sdk in sdks:
        for instance in selected:
            key = (sdk, instance); identities[key] = registrations[sdk].identity(bundle, instance)
            cases[key] = []
    # Block-major rotation counterbalances SDK order; no participant processes overlap.
    for block in range(10 if mode == 'protocol' else 1):
        order = list(sdks)[block % len(sdks):] + list(sdks)[:block % len(sdks)]
        for instance in selected:
            for sdk in order:
                key = (sdk, instance); case = bundle.cases[instance]
                if key not in budgets:budgets[key] = ActiveCaseBudget(case['case_wall_limit_seconds'])
                # The case cap counts time spent on this case, not other SDKs' work.
                if admissions[sdk]['status'] != 'admitted':
                    count = 3 if mode == 'protocol' and case['kind'] != 'sampling' else 1
                    records = _failure_records(identities[key], block, count, admissions[sdk]['status'], admissions[sdk]['reason'])
                    evidence = {'records': [r.to_dict() for r in records], 'block_verdict': Verdict(admissions[sdk]['status'], (admissions[sdk]['reason'],)).to_dict(), 'execution': None}
                    output = directory / sdk / instance / f'block-{block:02}'; output.mkdir(parents=True); write(output / 'evidence.json', evidence)
                else:
                    with budgets[key].active():
                        extra = {'candidate': registrations[sdk]} if candidates is not None else {}
                        if candidate_interpreters is not None:
                            extra['interpreter'] = interpreters[sdk]
                        evidence = run_block(bundle, identities[key], sdk, block, mode=mode,
                                             directory=directory / sdk / instance / f'block-{block:02}', cgroup_parent=cgroup_parent,
                                             cpu=cpu, budget=budgets[key], runtime_environment=runtime_environment, suite=suite, **extra)
                    if budgets[key].remaining <= 0 and evidence['block_verdict']['status'] == 'accepted':
                        evidence['block_verdict'] = Verdict('timeout', ('Complete case budget exhausted during evidence export',)).to_dict()
                        write(directory / sdk / instance / f'block-{block:02}' / 'evidence.json', evidence)
                cases[key].append(evidence)
    outcomes = []
    for (sdk, instance), blocks in cases.items():
        records = [r for b in blocks for r in b['records']]; single = [b['block_verdict'] for b in blocks]
        failed = [v for v in single if v['status'] != 'accepted']
        case_verdict = evaluate_case(bundle, identities[(sdk, instance)], records).to_dict()
        if failed:case_verdict = failed[0]
        outcomes.append({'sdk': sdk, 'instance': instance, 'qualification_status': 'accepted' if not failed else failed[0]['status'],
                         'case_verdict': case_verdict, 'record_count': len(records), 'blocks': len(blocks),
                         'reasons': [reason for v in failed for reason in v['reasons']]})
    workflows = {}
    for sdk in sdks:
        workflows[sdk] = {}
        for workflow in selected_workflows:
            records = [r for (name, instance), blocks in cases.items() if name == sdk and bundle.cases[instance]['workflow'] == workflow for b in blocks for r in b['records']]
            verdict = evaluate_workflow(bundle, workflow, records).to_dict()
            failed = [o for o in outcomes if o['sdk'] == sdk and bundle.cases[o['instance']]['workflow'] == workflow and o['qualification_status'] != 'accepted']
            if failed:verdict = failed[0]['case_verdict']
            workflows[sdk][workflow] = verdict
    report = {'schema_version': 1, 'suite': suite, 'protocol_revision': bundle.plan['protocol_revision'], 'bundle_sha256': bundle.sha256,
              'mode': mode, 'scope': 'engineering qualification' if mode == 'qualification' else 'unqualified protocol execution',
              'publication_eligible': False, 'sdks': list(sdks), 'instances': selected, 'unselected_instances': sorted(set(available) - set(selected)),
              'outcomes': outcomes, 'workflows': workflows, 'admissions': admissions, 'implementation': source_fingerprint(),
              'remaining_gates': ['independent review', 'sealed dedicated host/image', 'reviewed participant environments']}
    if candidates is not None:
        from ..candidates.provenance import implementation_fingerprint
        report['candidate_implementation_sha256'] = implementation_fingerprint()
    if candidate_interpreters is not None:
        report['candidate_interpreters_sha256'] = digest(interpreters)
    write(directory / 'report.json', report)
    lines = ['# ' + suite.upper() + ' execution evidence', '', 'Scope: ' + report['scope'] + '. Publication eligible: false.', '',
             'No ranking is inferred. A qualification pass is one process block, not complete-case acceptance.', '',
             '| SDK | Instance | Qualification outcome | Full-case outcome | Records |', '| --- | --- | --- | --- | --- |']
    for row in outcomes:
        lines.append(f"| {row['sdk']} | {row['instance']} | {row['qualification_status']} | {row['case_verdict']['status']} | {row['record_count']} |")
    (directory / 'SUMMARY.md').write_text('\n'.join(lines) + '\n')
    return report
