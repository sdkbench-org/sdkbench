"""Synthetic lifecycle checks; no simulated outcome is published as SDK evidence."""
import json
from copy import deepcopy
from pathlib import Path

import pytest
from p0_cases import positive_payload

from sdkbench.candidates import adapters, provenance, worker
from sdkbench.p0 import Bundle, Registration, ResultRecord
from sdkbench.p0.models import (
    ContractError,
    Identity,
    canonical_bytes,
    digest,
    read_json,
)
from sdkbench.p1a import campaign

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope='module')
def bundle():
    return Bundle(ROOT / 'docs/implementation')


def registration(stack='candidate-qiskit', workflow='qiskit-transpile'):
    config = adapters.workflow_configuration(workflow)
    return Registration(stack, [{'name': config['sdk'], 'version': 'candidate-test',
                                 'role': 'frontend', 'artifact_sha256': 'a' * 64}],
                        {'profile': 'CPU1-FP64', 'precision': 'float64/complex128', 'threads': 1,
                         'options': {'suite': 'compiler-candidate', 'sdk': config['sdk'],
                                     'workflow': workflow, 'compiler_options': config,
                                     'source_build': {'source_commit': 'd' * 40,
                                                      'wheel': {'sha256': 'e' * 64}}}},
                        {'python': 'test', 'os': 'test', 'image_sha256': 'b' * 64,
                         'dependency_lock_sha256': 'c' * 64, 'host': {'scope': 'synthetic-only'}})


def admission(reg):
    return {'configuration_sha256': reg.configuration_sha256,
            'environment_sha256': reg.environment_sha256, 'independent_attestation': False}


def request(bundle, reg, mode='protocol'):
    return bundle.request(reg.identity(bundle, 'ROUTE-LINE-06'), 2) | {
        'kind': 'route', 'suite': 'compiler-candidate', 'execution_mode': mode,
        'candidate_registration': reg.to_dict()}


def test_candidate_worker_admits_before_import_and_preserves_all_calls(bundle, monkeypatch):
    reg = registration()
    calls = []
    def verify(value):
        calls.append('admit')
        return admission(value)
    class Native:
        compiler_evidence = None
    class Adapter:
        native = Native()
        def __init__(self):
            self.audit = {'native_compilations': 1}
        def execute(self, kind, fixture, seed):
            calls.append(seed)
            return positive_payload(bundle, 'ROUTE-LINE-06')
    def load(value):
        assert calls == ['admit']
        calls.append('import')
        return Adapter()
    monkeypatch.setattr(worker, 'verify_runtime', verify)
    monkeypatch.setattr(worker.metadata, 'version', lambda _: 'candidate-test')
    monkeypatch.setattr(worker, 'load_adapter', load)
    req = request(bundle, reg)
    result = worker.execute_block(reg.stack_id, req)
    assert calls[:2] == ['admit', 'import']
    assert calls[2:] == [req['compiler_seed']] * 5
    assert len(result['warmups']) == 2 and len(result['records']) == 3
    assert result['candidate_admission'] == admission(reg)
    assert result['request_sha256'] == digest(req)
    assert all(item['status'] == 'completed' for item in result['warmups'] + result['records'])


def test_admission_failure_never_imports_sdk_and_remains_in_denominator(bundle, monkeypatch):
    reg = registration()
    def reject(_):
        raise ContractError('Changed wheel')
    monkeypatch.setattr(worker, 'verify_runtime', reject)
    monkeypatch.setattr(worker, 'load_adapter', lambda _: pytest.fail('SDK import after admission failure'))
    result = worker.execute_block(reg.stack_id, request(bundle, reg))
    assert len(result['warmups']) == 2 and len(result['records']) == 3
    assert all(item['status'] == 'error' and item['payload'] is None
               for item in result['warmups'] + result['records'])
    assert result['candidate_admission'] is None


def test_unregistered_options_fail_before_native_import(monkeypatch):
    reg = registration()
    config = deepcopy(reg.configuration)
    config['options']['compiler_options']['options']['optimization_level'] = 3
    changed = Registration(reg.stack_id, reg.components, config, reg.environment)
    with pytest.raises(ContractError, match='registered configuration'):
        adapters.load_adapter(changed)


@pytest.mark.parametrize('workflow', sorted(adapters.ROUTING_POLICY_WORKFLOWS))
def test_routing_control_rejects_strategy_mutation_before_import(monkeypatch, workflow):
    from sdkbench.p1b import common
    reg = registration('candidate-policy', workflow)
    config = deepcopy(reg.configuration)
    config['options']['compiler_options']['options']['routing'] = 'sabre_layout'
    changed = Registration(reg.stack_id, reg.components, config, reg.environment)
    monkeypatch.setattr(common, 'load_adapter', lambda _: pytest.fail('Imported mutated control'))
    with pytest.raises(ContractError, match='registered configuration'):
        adapters.load_adapter(changed)


def synthetic_supervisor(monkeypatch, bundle, fault=None):
    calls = []
    monkeypatch.setattr(provenance, 'verify_runtime', admission)
    def run(argv, **kwargs):
        req = read_json(argv[-1])
        reg = Registration(**req['candidate_registration'])
        calls.append((req, kwargs['limits']))
        identity = Identity(**req['identity'])
        def record(index):
            return ResultRecord(identity, req['block'], index, 'completed',
                                positive_payload(bundle, identity.instance_id)).to_dict()
        result = {'schema_version': 1, 'request_sha256': digest(req), 'sdk': reg.stack_id,
                  'sdk_version': 'candidate-test', 'worker_pid': 123,
                  'sdk_import_wall_seconds': .1, 'warmups': [record(i) for i in range(2)],
                  'records': [record(i) for i in range(3)], 'native_audit': [], 'warnings': [],
                  'candidate_admission': admission(reg), 'compiler_evidence_files': []}
        if 'candidate_interpreter' in req:
            result['candidate_interpreter'] = req['candidate_interpreter']
        if fault == 'admission':
            result['candidate_admission'] = None
        elif fault == 'version':
            result['sdk_version'] = 'unregistered'
        elif fault == 'warmup':
            result['warmups'][0]['payload']['final_layout'] = [0] * 6
        elif fault == 'timeout':
            from dataclasses import asdict
            return {'execution_status': 'timeout', 'pid': 123, 'stdout': '', 'stderr': '',
                    'returncode': -9, 'wall_seconds': kwargs['limits'].wall_seconds,
                    'kernel_memory_peak_bytes': 1024, 'limits': asdict(kwargs['limits']),
                    'enforced_cpu_set': str(kwargs['limits'].cpu),
                    'network_policy': 'seccomp-deny-sockets-and-io-uring'}
        from dataclasses import asdict
        return {'execution_status': 'completed', 'pid': 123, 'stdout': json.dumps(result), 'stderr': '',
                'argv': argv,
                'returncode': 0, 'wall_seconds': 0.01, 'kernel_memory_peak_bytes': 1024,
                'limits': asdict(kwargs['limits']), 'enforced_cpu_set': str(kwargs['limits'].cpu),
                'network_policy': 'seccomp-deny-sockets-and-io-uring'}
    monkeypatch.setattr(campaign, 'run_command', run)
    return calls


def test_candidates_reuse_full_protocol_seeds_budgets_and_rotation(bundle, monkeypatch, tmp_path):
    calls = synthetic_supervisor(monkeypatch, bundle)
    regs = {name: registration(name) for name in ('candidate-a', 'candidate-b')}
    result = campaign.run_campaign(bundle, directory=tmp_path / 'run', cgroup_parent=tmp_path,
                                   cpu=0, suite='compiler-candidate', candidates=regs)
    assert len(calls) == 60
    assert len(result['outcomes']) == 6
    assert all(row['record_count'] == 30 and row['blocks'] == 10
               and row['case_verdict']['status'] == 'accepted' for row in result['outcomes'])
    assert not result['publication_eligible'] and result['unselected_instances'] == []
    assert [req['identity']['stack_id'] for req, _ in calls[:2]] == list(regs)
    assert [req['identity']['stack_id'] for req, _ in calls[6:8]] == list(reversed(regs))
    for req, limits in calls:
        case = bundle.cases[req['identity']['instance_id']]
        assert req['compiler_seed'] == bundle.plan['execution_profile']['compiler_seeds'][req['block']]
        assert limits.memory_bytes == 16 * 1024 ** 3
        assert 0 < limits.wall_seconds <= case['case_wall_limit_seconds']


@pytest.mark.parametrize('fault', [None, 'warmup', 'timeout'])
def test_four_policy_campaign_keeps_limits_rotation_and_failure_records(
    bundle, monkeypatch, tmp_path, fault,
):
    from sdkbench.candidates.replay import replay
    calls = synthetic_supervisor(monkeypatch, bundle, fault)
    regs = {name: registration(name, name) for name in sorted(adapters.ROUTING_POLICY_WORKFLOWS)}
    root = tmp_path / 'run'
    result = campaign.run_campaign(
        bundle, directory=root, cgroup_parent=tmp_path, cpu=0,
        suite='compiler-candidate', candidates=regs,
    )
    assert len(result['outcomes']) == 12
    assert all(row['record_count'] == 30 for row in result['outcomes'])
    assert all((row['case_verdict']['status'] == 'accepted') == (fault is None)
               for row in result['outcomes'])
    assert [req['identity']['stack_id'] for req, _ in calls[:4]] == list(regs)
    assert [req['identity']['stack_id'] for req, _ in calls[12:16]] == list(regs)[1:] + list(regs)[:1]
    for req, limits in calls:
        assert limits.memory_bytes == 16 * 1024 ** 3
        assert 0 < limits.wall_seconds <= bundle.cases[req['identity']['instance_id']]['case_wall_limit_seconds']
        assert req['compiler_seed'] == bundle.plan['execution_profile']['compiler_seeds'][req['block']]
    seal(root)
    independent = replay(root, bundle)
    assert independent['blocks_verified'] == 120
    assert len(independent['cases']) == 12


@pytest.mark.parametrize('fault', ['admission', 'version', 'warmup', 'timeout'])
def test_candidate_bad_evidence_does_not_pass(bundle, monkeypatch, tmp_path, fault):
    synthetic_supervisor(monkeypatch, bundle, fault)
    reg = registration()
    result = campaign.run_campaign(bundle, directory=tmp_path / 'run', cgroup_parent=tmp_path,
                                   cpu=0, suite='compiler-candidate', candidates={reg.stack_id: reg},
                                   instances=['ROUTE-LINE-06'])
    assert result['outcomes'][0]['record_count'] == 30
    assert result['outcomes'][0]['case_verdict']['status'] != 'accepted'


def test_parent_rejects_changed_install_before_launch(bundle, monkeypatch, tmp_path):
    def reject(_):
        raise ContractError('Changed install')
    monkeypatch.setattr(provenance, 'verify_runtime', reject)
    monkeypatch.setattr(campaign, 'run_command', lambda *a, **kw: pytest.fail('Launched rejected candidate'))
    reg = registration()
    result = campaign.run_campaign(bundle, directory=tmp_path / 'run', cgroup_parent=tmp_path,
                                   cpu=0, suite='compiler-candidate', candidates={reg.stack_id: reg})
    assert all(row['record_count'] == 30 and row['case_verdict']['status'] == 'access-blocked'
               for row in result['outcomes'])


def test_artifact_files_require_complete_matching_hashes(tmp_path):
    from sdkbench.candidates.response import verify_response
    reg = registration('candidate-artifact', 'flagquantum-target-artifact')
    name = 'compiler-evidence-measured-0.json'
    path = tmp_path / name
    path.write_bytes(canonical_bytes({'executable_artifact': '{}', 'target_snapshot_id': 'd' * 64}))
    response = {'sdk_version': 'candidate-test', 'candidate_admission': admission(reg),
                'warmups': [], 'records': [{'status': 'completed'}],
                'compiler_evidence_files': [{'phase': 'measured', 'repetition': 0,
                                            'filename': name, 'sha256': provenance.file_sha256(path)}]}
    verify_response(reg, response, tmp_path)
    path.write_text('changed')
    with pytest.raises(ContractError, match='hash mismatch'):
        verify_response(reg, response, tmp_path)
    response['compiler_evidence_files'] = []
    with pytest.raises(ContractError, match='Missing compiler evidence'):
        verify_response(reg, response, tmp_path)


def seal(directory):
    manifest = {'schema_version': 1, 'files': {
        path.relative_to(directory).as_posix(): provenance.file_sha256(path)
        for path in directory.rglob('*') if path.is_file() and path.name != 'MANIFEST.json'}}
    (directory / 'MANIFEST.json').write_bytes(canonical_bytes(manifest))


def test_full_candidate_replay_and_resealed_seed_corruption(bundle, monkeypatch, tmp_path):
    from sdkbench.candidates.replay import replay
    synthetic_supervisor(monkeypatch, bundle)
    reg = registration()
    root = tmp_path / 'run'
    campaign.run_campaign(bundle, directory=root, cgroup_parent=tmp_path,
                          cpu=0, suite='compiler-candidate', candidates={reg.stack_id: reg})
    seal(root)
    summary = replay(root, bundle)
    assert summary['blocks_verified'] == 30
    assert {row['status'] for row in summary['cases']} == {'accepted'}
    path = root / reg.stack_id / 'ROUTE-LINE-06/block-00/request.json'
    req = read_json(path)
    req['compiler_seed'] += 1
    path.write_bytes(canonical_bytes(req))
    seal(root)
    with pytest.raises(ContractError, match='request/seed binding'):
        replay(root, bundle)


def test_replay_accepts_counterbalance_order_independent_of_sorted_json(bundle, monkeypatch, tmp_path):
    from sdkbench.candidates.replay import replay
    monkeypatch.setattr(provenance, 'verify_runtime', lambda _: (_ for _ in ()).throw(ContractError('Not installed')))
    registrations = {name: registration(name) for name in ('candidate-z', 'candidate-a')}
    root = tmp_path / 'run'
    campaign.run_campaign(bundle, directory=root, cgroup_parent=tmp_path, cpu=0,
                          suite='compiler-candidate', candidates=registrations)
    seal(root)
    assert replay(root, bundle)['blocks_verified'] == 60


def test_replay_preserves_denied_candidates_and_rejects_false_acceptance(bundle, monkeypatch, tmp_path):
    from sdkbench.candidates.replay import replay
    def reject(_):
        raise ContractError('Changed install')
    monkeypatch.setattr(provenance, 'verify_runtime', reject)
    reg = registration()
    root = tmp_path / 'run'
    campaign.run_campaign(bundle, directory=root, cgroup_parent=tmp_path,
                          cpu=0, suite='compiler-candidate', candidates={reg.stack_id: reg})
    seal(root)
    summary = replay(root, bundle)
    assert {row['status'] for row in summary['cases']} == {'access-blocked'}
    path = root / reg.stack_id / 'ROUTE-LINE-06/block-00/evidence.json'
    evidence = read_json(path)
    evidence['block_verdict']['status'] = 'accepted'
    path.write_bytes(canonical_bytes(evidence))
    seal(root)
    with pytest.raises(ContractError, match='block verdict'):
        replay(root, bundle)


@pytest.mark.parametrize('fault', ['none', 'warmup', 'denied'])
def test_report_keeps_failure_denominators_and_excludes_failed_timing_blocks(bundle, monkeypatch, tmp_path, fault):
    import importlib.util
    spec = importlib.util.spec_from_file_location('candidate_report', ROOT / 'tools/compiler_candidate_report.py')
    report = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(report)
    synthetic_supervisor(monkeypatch, bundle, None if fault == 'none' else 'warmup')
    if fault == 'denied':
        def reject(_):
            raise ContractError('Changed install')
        monkeypatch.setattr(provenance, 'verify_runtime', reject)
    reg = registration()
    root = tmp_path / 'run'
    campaign.run_campaign(bundle, directory=root, cgroup_parent=tmp_path,
                          cpu=0, suite='compiler-candidate', candidates={reg.stack_id: reg})
    seal(root)
    result = report.summarize(root, bundle)
    assert len(result['cases']) == 3
    for row in result['cases']:
        assert row['expected_records'] == sum(row['measured_record_statuses'].values()) == 30
        assert row['accepted_records'] == (0 if fault == 'denied' else 30)
        assert len(row['blocks']) == 10
        if fault == 'none':
            assert row['status'] == 'accepted'
            assert row['complete_block_compile_medians_seconds']['count'] == 10
        else:
            assert row['status'] != 'accepted'
            assert row['complete_block_compile_medians_seconds'] is None
        if fault == 'denied':
            assert row['full_cz_count_for_accepted_records'] is None
    assert result['publication_eligible'] is False
