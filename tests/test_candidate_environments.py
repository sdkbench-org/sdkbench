"""Exercise separate installed environments without manufacturing SDK measurements."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import sysconfig
import venv
from pathlib import Path
from zipfile import ZipFile

import pytest
from test_candidate_runner import (
    admission,
    registration,
    request,
    seal,
    synthetic_supervisor,
)

from sdkbench.candidates import environment, worker
from sdkbench.candidates.replay import replay
from sdkbench.p0 import Bundle, Registration
from sdkbench.p0.models import ContractError, canonical_bytes, digest, read_json
from sdkbench.p1a import campaign

ROOT = Path(__file__).resolve().parents[1]


def synthetic_environments(root: Path) -> list[tuple[str, Registration]]:
    """Make two real venvs with import-raising synthetic SDK distributions."""
    environments = []
    for index, version in enumerate(('9.8', '9.9')):
        prefix = root / f'environment-{index}'
        venv.EnvBuilder(with_pip=False).create(prefix)
        python = str(prefix / ('Scripts/python.exe' if os.name == 'nt' else 'bin/python'))
        site = Path(subprocess.check_output(
            [python, '-c', "import sysconfig; print(sysconfig.get_path('purelib'))"],
            text=True, timeout=15,
        ).strip())
        # A nested venv does not inherit its caller's venv site-packages.
        # Share the existing test dependencies explicitly, without installation.
        shared = sorted({sysconfig.get_path('purelib'), sysconfig.get_path('platlib')})
        (site / 'shared-test-dependencies.pth').write_text('\n'.join(shared) + '\n')
        members = {
            'qiskit/__init__.py': f'raise RuntimeError("synthetic-sdk-{version}-imported")\n'.encode(),
            f'qiskit-{version}.dist-info/METADATA': f'Name: qiskit\nVersion: {version}\n'.encode(),
        }
        record = f'qiskit-{version}.dist-info/RECORD'
        members[record] = ''.join(f'{name},,\n' for name in [*members, record]).encode()
        wheel = prefix / f'qiskit-{version}-py3-none-any.whl'
        with ZipFile(wheel, 'w') as archive:
            for name, content in members.items():
                archive.writestr(name, content)
                path = site / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(content)
        release = prefix / 'release.json'
        release.write_bytes(canonical_bytes({
            'info': {'name': 'qiskit', 'version': version},
            'urls': [{'filename': wheel.name,
                      'url': 'https://files.pythonhosted.org/synthetic/' + wheel.name,
                      'packagetype': 'bdist_wheel', 'yanked': False,
                      'size': wheel.stat().st_size,
                      'digests': {'sha256': environment.file_sha256(wheel)}}],
        }))
        # This verifies the wheel, metadata, environment and import resolution
        # in the selected interpreter. Importing the fake SDK would raise.
        script = '''
import sys
from pathlib import Path
from sdkbench.candidates.provenance import create_wheel_registration
from sdkbench.candidates.adapters import workflow_configuration
from sdkbench.p0.models import canonical_bytes
root = Path(sys.argv[1])
workflow = 'qiskit-transpile-restored'
reg = create_wheel_registration(stack_id=sys.argv[2], sdk='qiskit', workflow=workflow,
    options=workflow_configuration(workflow), wheel=next(root.glob('*.whl')),
    release_metadata=root / 'release.json')
print(canonical_bytes(reg.to_dict()).decode(), end='')
'''
        output = subprocess.check_output(
            [python, '-c', script, str(prefix), f'synthetic-{index}'],
            env={**os.environ, 'PYTHONPATH': str(ROOT / 'src')}, text=True, timeout=120,
        )
        environments.append((python, Registration(**json.loads(output))))
    return environments


@pytest.fixture(scope='module')
def installed_environments(tmp_path_factory):
    return synthetic_environments(tmp_path_factory.mktemp('candidate-interpreters'))


def test_real_interpreters_admit_only_their_own_installations(installed_environments):
    env = {'PYTHONPATH': str(ROOT / 'src')}
    for index, (python, reg) in enumerate(installed_environments):
        expected = environment.interpreter_identity(python)
        observed = environment.admit_interpreter(reg, expected, env)
        assert observed['interpreter']['python'] == python
        assert observed['admission'] == admission(reg)
        other = installed_environments[1 - index][1]
        with pytest.raises(ContractError, match='admission failed'):
            environment.admit_interpreter(other, expected, env)


def test_revision_inventory_is_rechecked_in_selected_interpreter(installed_environments):
    python, reg = installed_environments[0]
    env = {'PYTHONPATH': str(ROOT / 'src')}
    output = subprocess.check_output(
        [python, '-c', ('from sdkbench.p1a.provenance import capture_environment; '
         'from sdkbench.p0.models import canonical_bytes; '
         'print(canonical_bytes(capture_environment()).decode(), end="")')],
        env={**os.environ, **env}, text=True, timeout=120,
    )
    inventory = json.loads(output)
    expected = environment.interpreter_identity(python)
    assert environment.admit_interpreter(reg, expected, env, inventory=inventory)['admission'] == admission(reg)
    inventory['host']['machine'] = 'synthetic-other-machine'
    with pytest.raises(ContractError, match='inventory changed before the joint freeze'):
        environment.admit_interpreter(reg, expected, env, inventory=inventory)


def test_real_worker_rechecks_environment_before_import(installed_environments, tmp_path):
    bundle = Bundle(ROOT / 'docs/implementation')
    for python, reg in installed_environments:
        req = request(bundle, reg)
        req['candidate_interpreter'] = environment.interpreter_identity(python)
        path = tmp_path / (reg.stack_id + '.json')
        path.write_bytes(canonical_bytes(req))
        output = subprocess.check_output(
            [python, '-m', 'sdkbench.candidates.worker', '--sdk', reg.stack_id, str(path)],
            env={**os.environ, 'PYTHONPATH': str(ROOT / 'src')}, text=True,
            stderr=subprocess.PIPE, timeout=120,
        )
        result = json.loads(output)
        assert result['candidate_admission'] == admission(reg)
        assert result['candidate_interpreter'] == req['candidate_interpreter']
        version = next(c['version'] for c in reg.components if c['role'] == 'frontend')
        assert result['sdk_version'] == version
        assert len(result['warmups']) == 2 and len(result['records']) == 3
        assert all(r['status'] == 'error' and f'synthetic-sdk-{version}-imported' in r['reason']
                   for r in result['warmups'] + result['records'])


def test_wrong_worker_interpreter_rejected_before_sdk_import(monkeypatch):
    bundle = Bundle(ROOT / 'docs/implementation')
    reg = registration()
    req = request(bundle, reg)
    req['candidate_interpreter'] = {'python': '/different/python', 'executable_sha256': 'a' * 64}
    monkeypatch.setattr(worker, 'verify_runtime', lambda _: pytest.fail('Admitted wrong interpreter'))
    monkeypatch.setattr(worker, 'load_adapter', lambda _: pytest.fail('Imported wrong environment'))
    result = worker.execute_block(reg.stack_id, req)
    assert result['candidate_admission'] is None
    assert all(r['status'] == 'error' for r in result['records'])


def fake_interpreters(tmp_path, registrations):
    result = {}
    for name in registrations:
        path = tmp_path / name / 'python'
        path.parent.mkdir()
        path.write_text('synthetic interpreter; never executed\n')
        path.chmod(0o700)
        result[name] = str(path)
    return result


def synthetic_admission(reg, expected, env):
    return {'registration_sha256': digest(reg.to_dict()),
            'interpreter': expected, 'admission': admission(reg)}


@pytest.fixture(scope='module')
def multi_campaign(tmp_path_factory):
    root = tmp_path_factory.mktemp('multi-campaign')
    bundle = Bundle(ROOT / 'docs/implementation')
    # Same workflow, two distinct stack identities. The runner must not deduplicate.
    regs = {name: registration(name) for name in ('candidate-before', 'candidate-after')}
    interpreters = fake_interpreters(root, regs)
    with pytest.MonkeyPatch.context() as patch:
        calls = synthetic_supervisor(patch, bundle)
        patch.setattr(environment, 'admit_interpreter', synthetic_admission)
        result = campaign.run_campaign(
            bundle, directory=root / 'run', cgroup_parent=root, cpu=0,
            suite='compiler-candidate', candidates=regs, candidate_interpreters=interpreters,
        )
    seal(root / 'run')
    return root / 'run', bundle, result, calls, interpreters


def test_multiple_environments_share_cases_limits_seeds_and_rotation(multi_campaign):
    root, bundle, report, calls, interpreters = multi_campaign
    assert len(calls) == 60 and len(report['outcomes']) == 6
    assert all(row['record_count'] == 30 and row['case_verdict']['status'] == 'accepted'
               for row in report['outcomes'])
    assert [req['identity']['stack_id'] for req, _ in calls[:2]] == list(interpreters)
    assert [req['identity']['stack_id'] for req, _ in calls[6:8]] == list(reversed(interpreters))
    for req, limits in calls:
        stack = req['identity']['stack_id']
        assert req['candidate_interpreter']['python'] == interpreters[stack]
        assert limits.memory_bytes == 16 * 1024**3
        assert req['compiler_seed'] == bundle.plan['execution_profile']['compiler_seeds'][req['block']]
    assert replay(root, bundle)['blocks_verified'] == 60
    assert report['publication_eligible'] is False


@pytest.mark.parametrize('fault', ['argv', 'request', 'response', 'admission', 'map', 'dropped-map'])
def test_resealed_interpreter_substitution_is_rejected(multi_campaign, tmp_path, fault):
    source, bundle, _, _, _ = multi_campaign
    root = tmp_path / 'run'
    shutil.copytree(source, root)
    name = 'candidate-before'
    folder = root / name / 'ROUTE-LINE-06/block-00'
    if fault == 'admission':
        path = root / 'admission.json'
        data = read_json(path)
        data[name]['interpreter_probe']['admission']['environment_sha256'] = 'f' * 64
    elif fault == 'map':
        path = root / 'interpreters.json'
        data = read_json(path)
        data[name]['python'] = '/substituted/python'
    elif fault == 'dropped-map':
        path = root / 'report.json'
        data = read_json(path)
        del data['candidate_interpreters_sha256']
        (root / 'interpreters.json').unlink()
    else:
        path = folder / ('request.json' if fault == 'request' else 'evidence.json')
        data = read_json(path)
        if fault == 'argv':
            data['execution']['argv'][0] = '/substituted/python'
        elif fault == 'request':
            data['candidate_interpreter']['python'] = '/substituted/python'
        else:
            data['response']['candidate_interpreter']['python'] = '/substituted/python'
    path.write_bytes(canonical_bytes(data))
    seal(root)
    with pytest.raises(ContractError):
        replay(root, bundle)


def test_missing_interpreter_keeps_failure_records_and_other_participant(multi_campaign, tmp_path, monkeypatch):
    _, bundle, _, _, _ = multi_campaign
    regs = {name: registration(name) for name in ('candidate-missing', 'candidate-present')}
    interpreters = fake_interpreters(tmp_path, regs)
    Path(interpreters['candidate-missing']).unlink()
    synthetic_supervisor(monkeypatch, bundle)
    monkeypatch.setattr(environment, 'admit_interpreter', synthetic_admission)
    root = tmp_path / 'run'
    report = campaign.run_campaign(
        bundle, directory=root, cgroup_parent=tmp_path, cpu=0,
        suite='compiler-candidate', candidates=regs, candidate_interpreters=interpreters,
    )
    assert all(row['record_count'] == 30 for row in report['outcomes'])
    assert {row['case_verdict']['status'] for row in report['outcomes']
            if row['sdk'] == 'candidate-missing'} == {'access-blocked'}
    assert {row['case_verdict']['status'] for row in report['outcomes']
            if row['sdk'] == 'candidate-present'} == {'accepted'}
    seal(root)
    assert replay(root, bundle)['blocks_verified'] == 60


def test_partial_environment_map_is_rejected_before_creating_campaign(tmp_path):
    bundle = Bundle(ROOT / 'docs/implementation')
    regs = {name: registration(name) for name in ('candidate-a', 'candidate-b')}
    root = tmp_path / 'run'
    with pytest.raises(ContractError, match='every candidate'):
        campaign.run_campaign(bundle, directory=root, cgroup_parent=tmp_path, cpu=0,
                              suite='compiler-candidate', candidates=regs,
                              candidate_interpreters={'candidate-a': sys.executable})
    assert not root.exists()


def test_admission_timeout_kills_and_reaps_the_setup_process(monkeypatch):
    reg = registration()
    selected = environment.interpreter_identity(sys.executable)
    events = []

    class Process:
        pid = 12345

        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

        def communicate(self, timeout):
            events.append(('communicate', timeout))
            if timeout == 120:
                raise subprocess.TimeoutExpired('synthetic-probe', timeout)
            return b'', b''

    monkeypatch.setattr(environment.subprocess, 'Popen', lambda *args, **kwargs: Process())
    monkeypatch.setattr(environment.os, 'killpg', lambda *args: events.append(('killpg', *args)))
    with pytest.raises(TimeoutError, match='120 seconds'):
        environment.admit_interpreter(reg, selected, {'PYTHONPATH': str(ROOT / 'src')})
    assert events == [('communicate', 120), ('killpg', 12345, environment.signal.SIGKILL),
                      ('communicate', 5)]


@pytest.mark.parametrize('selection', [
    ['candidate-a=/one/python'],
    ['candidate-a=/one/python', 'candidate-a=/two/python'],
    ['candidate-a=relative/python', 'candidate-b=/two/python'],
    ['candidate-a=/one/python', 'unregistered=/two/python'],
])
def test_cli_rejects_ambiguous_or_partial_environment_selection(tmp_path, selection, monkeypatch):
    from sdkbench.candidates import cli

    arguments = ['run', '--directory', str(tmp_path / 'run'),
                 '--cgroup-parent', str(tmp_path), '--cpu', '0']
    for name in ('candidate-a', 'candidate-b'):
        path = tmp_path / (name + '.json')
        path.write_bytes(canonical_bytes(registration(name).to_dict()))
        arguments += ['--registration', str(path)]
    for value in selection:
        arguments += ['--interpreter', value]
    monkeypatch.setattr(cli, 'run_campaign', lambda *a, **k: pytest.fail('Started invalid campaign'))
    with pytest.raises(SystemExit) as caught:
        cli.main(arguments)
    assert caught.value.code == 2
    assert not (tmp_path / 'run').exists()
