"""Scheduling/failure tests use synthetic evidence only; native tests are separate."""
from copy import deepcopy
from dataclasses import replace
from pathlib import Path
from importlib import metadata
import json
import pytest
from sdkbench.p0 import Bundle, ResultRecord, evaluate
from sdkbench.p0.models import digest, read_json
from sdkbench.p1a import campaign, worker
from sdkbench.p1a.common import VERSIONS, SDKS, UnsupportedCapability
from p0_cases import positive_payload

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope='module')
def bundle():return Bundle(ROOT / 'docs/implementation')


def request(bundle, sdk='qiskit', mode='protocol', instance='PARAM-04'):
    identity = bundle.identity(instance, sdk, '1'*64, '2'*64)
    return bundle.request(identity) | {'kind': bundle.cases[instance]['kind'], 'execution_mode': mode}


@pytest.mark.parametrize('sdk', SDKS)
@pytest.mark.parametrize('fault,status', [('missing', 'install-failed'), ('unsupported', 'unsupported'), ('exception', 'error')])
def test_worker_preserves_native_failures(bundle, monkeypatch, sdk, fault, status):
    monkeypatch.setattr(worker.metadata, 'version', lambda _: VERSIONS[sdk])
    class Broken:
        def execute(self, *args):
            if fault == 'unsupported':raise UnsupportedCapability('Public feature is absent')
            raise RuntimeError('Native execution failed')
    def load(_):
        if fault == 'missing':raise ModuleNotFoundError('SDK dependency is missing')
        return Broken()
    monkeypatch.setattr(worker, 'load_adapter', load)
    response = worker.execute_block(sdk, request(bundle, sdk))
    assert len(response['warmups']) == 2 and len(response['records']) == 3
    assert {r['status'] for r in response['warmups'] + response['records']} == {status}
    assert all(r['reason'] and r['payload'] is None and not r['measurements'] for r in response['records'])


def synthetic_setup(monkeypatch, bundle, fault=None):
    calls = []
    monkeypatch.setattr(campaign, 'capture_environment', lambda: {'implementation': {'sdkbench_version': 'synthetic', 'p0_p1a_source_sha256': '1'*64},
                        'image_descriptor_sha256': '2'*64, 'dependency_lock_sha256': '3'*64, 'host': {'id': 'synthetic-only'}})
    def fingerprint(name):
        versions = {'cirq-core':'1.7.0','flagquantum':'0.3.1','qiskit':'2.6.2'}
        return {'name':name, 'version':versions.get(name,'synthetic'), 'artifact_sha256':'4'*64}
    monkeypatch.setattr(campaign, 'distribution_fingerprint', fingerprint)
    def fake_run(argv, **kwargs):
        req = read_json(argv[-1]); sdk = req['identity']['stack_id']; calls.append((sdk, req['identity']['instance_id'], req['block'], kwargs['limits']))
        if fault == 'timeout':return {'execution_status':'timeout', 'pid':111, 'stdout':'a forged successful result', 'stderr':''}
        mode = req['execution_mode']; numeric = req['kind'] != 'sampling'; measured = 3 if mode == 'protocol' and numeric else 1
        from sdkbench.p0.models import Identity
        identity = Identity(**req['identity'])
        def record(r):return ResultRecord(identity, req['block'], r, 'completed', deepcopy(positive_payload(bundle, identity.instance_id)), measurements={'outcome_wall_seconds':.01}).to_dict()
        response = {'schema_version':1, 'request_sha256':digest(req), 'sdk':sdk, 'sdk_version':VERSIONS[sdk], 'worker_pid':111,
                    'sdk_import_wall_seconds':.01, 'warmups':[record(r) for r in range(2 if mode=='protocol' and numeric else 0)],
                    'records':[record(r) for r in range(measured)], 'native_audit':[], 'warnings':[]}
        if fault == 'identity':response['records'][0]['identity']['environment_sha256']='f'*64
        if fault == 'warmup':response['warmups'][0]['payload']['outputs'][0]['X0']=.1
        if fault == 'count':response['records'].pop()
        if fault == 'pid':response['worker_pid']=222
        return {'execution_status':'completed','pid':111,'stdout':json.dumps(response),'stderr':''}
    monkeypatch.setattr(campaign, 'run_command', fake_run)
    return calls


def test_full_protocol_blocks_seeds_caps_and_rotation(bundle, monkeypatch, tmp_path):
    calls = synthetic_setup(monkeypatch, bundle)
    selected = ['PARAM-04','OBS-04','SAMPLE-03','SAMPLE-05']
    report = campaign.run_campaign(bundle,directory=tmp_path/'campaign',cgroup_parent=tmp_path,cpu=0,instances=selected)
    assert len(calls)==120
    assert all(row['case_verdict']['status']=='accepted' for row in report['outcomes'])
    assert all(row['record_count']==(10 if row['instance'].startswith('SAMPLE') else 30) for row in report['outcomes'])
    assert [sdk for sdk,instance,block,_ in calls if instance=='PARAM-04' and block==0]==list(SDKS)
    assert [sdk for sdk,instance,block,_ in calls if instance=='PARAM-04' and block==1]==[SDKS[1],SDKS[2],SDKS[0]]
    for sdk,instance,block,limits in calls:
        case=bundle.cases[instance]
        assert limits.memory_bytes==case['process_memory_limit_gib']*1024**3
        assert 0<limits.wall_seconds<=case['case_wall_limit_seconds']
    assert report['publication_eligible'] is False and report['unselected_instances']
    assert all(report['workflows'][sdk]['W08']['status']=='accepted' for sdk in SDKS)
    assert report['workflows']['qiskit']['W01']['status']=='not-measured'


def test_qualification_includes_all_eight_cases_without_claiming_complete_case(bundle, monkeypatch, tmp_path):
    calls=synthetic_setup(monkeypatch,bundle)
    report=campaign.run_campaign(bundle,directory=tmp_path/'q',cgroup_parent=tmp_path,cpu=0,mode='qualification')
    assert len(calls)==24 and not report['unselected_instances']
    assert all(x['qualification_status']=='accepted' and x['case_verdict']['status']=='not-measured' for x in report['outcomes'])
    assert all(x['blocks']==1 and x['record_count']==1 for x in report['outcomes'])


@pytest.mark.parametrize('fault', ['timeout','identity','warmup','count','pid'])
def test_false_success_and_bad_evidence_never_pass(bundle, monkeypatch, tmp_path, fault):
    synthetic_setup(monkeypatch,bundle,fault)
    report=campaign.run_campaign(bundle,directory=tmp_path/'fault',cgroup_parent=tmp_path,cpu=0,sdks=('qiskit',),instances=['PARAM-04'])
    assert report['outcomes'][0]['qualification_status']!='accepted'
    assert report['outcomes'][0]['case_verdict']['status']!='accepted'
    if fault=='timeout':
        e=read_json(tmp_path/'fault/qiskit/PARAM-04/block-00/evidence.json')
        assert all(not r['measurements'] and r['status']=='timeout' for r in e['records'])


def test_active_case_budget_never_charges_other_sdks_or_resets_itself():
    clock=[0.]; budget=campaign.ActiveCaseBudget(10,clock=lambda:clock[0])
    with budget.active():clock[0]+=3;assert budget.remaining==7
    clock[0]+=100
    assert budget.remaining==7
    with budget.active():clock[0]+=8;assert budget.remaining==0
    assert budget.remaining==0 and budget.used==11


def test_install_failure_remains_visible_for_every_case(bundle, monkeypatch, tmp_path):
    synthetic_setup(monkeypatch,bundle)
    def missing(name):raise metadata.PackageNotFoundError(name)
    monkeypatch.setattr(campaign,'distribution_fingerprint',missing)
    report=campaign.run_campaign(bundle,directory=tmp_path/'missing',cgroup_parent=tmp_path,cpu=0,mode='qualification')
    assert len(report['outcomes'])==24
    assert all(row['qualification_status']=='install-failed' for row in report['outcomes'])
    assert all(not p['execution'] for p in [read_json(path) for path in (tmp_path/'missing').glob('*/*/*/evidence.json')])


def test_profile_matches_frozen_adapter_cohort():
    profile=read_json(ROOT/'docs/implementation/p1a-profile.json')
    from sdkbench.p1a.common import WORKFLOWS
    assert profile['sdk_versions']==VERSIONS
    assert profile['workflows']==list(WORKFLOWS)
    assert not profile['publication_eligible']


def test_lossless_evidence_archive_and_independent_replay(bundle,monkeypatch,tmp_path):
    import hashlib,gzip,importlib.util
    from sdkbench.p0.models import canonical_bytes,ContractError
    synthetic_setup(monkeypatch,bundle)
    root=tmp_path/'evidence';root.mkdir()
    campaign.run_campaign(bundle,directory=root/'all-instances',cgroup_parent=tmp_path,cpu=0,mode='qualification')
    (root/'context.json').write_bytes(canonical_bytes({'source_commit':'synthetic-test-only'}))
    manifest={p.relative_to(root).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in root.rglob('*') if p.is_file()}
    (root/'MANIFEST.json').write_bytes(canonical_bytes({'files':manifest}))
    spec=importlib.util.spec_from_file_location('p1a_evidence',ROOT/'tools/p1a_evidence.py')
    tool=importlib.util.module_from_spec(spec);spec.loader.exec_module(tool)
    summary=tool.verify(root,bundle);assert summary['blocks_verified']==24
    archive=tmp_path/'raw.json.gz';sha=tool.archive(root,archive)
    assert sha==hashlib.sha256(archive.read_bytes()).hexdigest()
    decoded=json.loads(gzip.decompress(archive.read_bytes()))
    for name,entry in decoded['files'].items():
        assert entry['utf8'].encode()==(root/name).read_bytes()
        assert hashlib.sha256(entry['utf8'].encode()).hexdigest()==entry['sha256']
    (root/'all-instances/report.json').write_text('{}')
    with pytest.raises(ContractError,match='hash mismatch'):tool.verify(root,bundle)
