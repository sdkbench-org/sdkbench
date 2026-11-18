"""P1b lifecycle, truthful non-success accounting and the native compile deadline."""
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import pytest
from sdkbench.p0 import Bundle
from sdkbench.p0.models import read_json
from sdkbench.p1a import campaign, worker
from sdkbench.p1b import common
from test_p1a_runner import synthetic_setup, request

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope='module')
def bundle():return Bundle(ROOT / 'docs/implementation')


def test_p1b_scope_compiler_seed_and_complete_accounting(bundle, monkeypatch, tmp_path):
    calls = synthetic_setup(monkeypatch, bundle)
    original = campaign.distribution_fingerprint
    monkeypatch.setattr(campaign, 'distribution_fingerprint', lambda n: original(n) | ({'version': '0.4.0'} if n == 'qiskit-algorithms' else {}))
    report = campaign.run_campaign(bundle, directory=tmp_path/'full', cgroup_parent=tmp_path, cpu=0, suite='p1b')
    assert len(calls) == 240 and len(report['outcomes']) == 24
    assert not report['unselected_instances'] and report['suite'] == 'p1b'
    assert all(row['case_verdict']['status'] == 'accepted' and row['record_count'] == 30 for row in report['outcomes'])
    registrations = read_json(tmp_path/'full/registrations.json')
    assert any(c['name'] == 'qiskit-algorithms' for c in registrations['qiskit']['components'])
    for path in (tmp_path/'full').glob('*/*/*/request.json'):
        req = read_json(path)
        assert req['suite'] == 'p1b'
        assert req['compiler_seed'] == bundle.plan['execution_profile']['compiler_seeds'][req['block']]


@pytest.mark.parametrize('status', ['unsupported', 'install-failed', 'error', 'out-of-memory'])
def test_worker_never_fabricates_success(bundle, monkeypatch, status):
    monkeypatch.setattr(worker.metadata, 'version', lambda _: common.VERSIONS['qiskit'])
    sdk = 'qiskit';req = request(bundle, sdk, instance='GRAD-04') | {'suite': 'p1b'}
    exceptions = {'unsupported': common.UnsupportedCapability('Native feature absent'), 'install-failed': ModuleNotFoundError('Native component absent'),
                  'error': RuntimeError('Native execution failed'), 'out-of-memory': MemoryError('Native allocation failed')}
    class Broken:
        def execute(self, *args):raise exceptions[status]
    monkeypatch.setattr(common, 'load_adapter', lambda _: Broken())
    response = worker.execute_block(sdk, req)
    assert len(response['records']) == 3 and len(response['warmups']) == 2
    assert all(r['status'] == status and r['payload'] is None and not r['measurements']
               for r in response['records'] + response['warmups'])


def test_worker_passes_compiler_seed_and_prepares_before_execution(bundle, monkeypatch):
    monkeypatch.setattr(worker.metadata, 'version', lambda _: common.VERSIONS['qiskit'])
    req = request(bundle, instance='ROUTE-LINE-06') | {'suite': 'p1b'};calls = []
    class Native:
        audit = {}
        def prepare(self, kind):calls.append(('prepare', kind))
        def execute(self, kind, fixture, seed):calls.append(('execute', seed));return {}
    monkeypatch.setattr(common, 'load_adapter', lambda _: Native())
    worker.execute_block('qiskit', req)
    assert calls[0] == ('prepare', 'route')
    assert calls[1:] == [('execute', req['compiler_seed'])] * 5


def test_kernel_compile_alarm_is_timeout_not_success(bundle, monkeypatch, tmp_path):
    synthetic_setup(monkeypatch, bundle)
    monkeypatch.setattr(campaign, 'run_command', lambda *a, **k:
                        {'execution_status': 'error', 'returncode': -signal.SIGALRM, 'pid': 111, 'stdout': '', 'stderr': ''})
    report = campaign.run_campaign(bundle, directory=tmp_path/'alarm', cgroup_parent=tmp_path, cpu=0,
                                   instances=['ROUTE-LINE-06'], sdks=('flagquantum',), suite='p1b')
    assert report['outcomes'][0]['case_verdict']['status'] == 'timeout'
    assert report['outcomes'][0]['record_count'] == 30


@pytest.mark.skipif(os.name != 'posix', reason='POSIX kernel timer')
def test_alarm_kills_a_gil_holding_native_call():
    script = "from sdkbench.p1b.common import compile_deadline; import ctypes\nwith compile_deadline(.05):ctypes.PyDLL(None).sleep(3)"
    result = subprocess.run([sys.executable, '-c', script], capture_output=True, timeout=10)
    assert result.returncode == -signal.SIGALRM, result.stderr.decode()


def test_profile_matches_adapter_cohort():
    profile = read_json(ROOT/'docs/implementation/p1b-profile.json')
    assert profile['sdk_versions'] == common.VERSIONS and profile['workflows'] == list(common.WORKFLOWS)
    assert profile['extensions'] == common.EXTENSIONS and not profile['publication_eligible']
