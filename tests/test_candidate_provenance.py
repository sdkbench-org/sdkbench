"""Candidate identity checks use synthetic wheels, never substitute task results."""
from copy import deepcopy
from dataclasses import replace
from importlib.machinery import ModuleSpec
from pathlib import Path
from types import SimpleNamespace
from zipfile import ZipFile

import pytest

from sdkbench.candidates import provenance as candidate
from sdkbench.p0.models import ContractError, canonical_bytes


@pytest.fixture
def installed(tmp_path, monkeypatch):
    site = tmp_path / 'site'
    site.mkdir()
    files = {'qiskit/__init__.py': b'raise RuntimeError("Must not import during admission")\n',
             'qiskit/compiler.py': b'REVISION = 1\n',
             'qiskit-9.9.dist-info/METADATA': b'Name: qiskit\nVersion: 9.9\n',
             'qiskit-9.9.dist-info/RECORD': b'installer-rewritten-record'}
    wheel = tmp_path / 'candidate.whl'
    with ZipFile(wheel, 'w') as archive:
        for name, content in files.items():
            archive.writestr(name, content if not name.endswith('/RECORD') else b'wheel-record')
            path = site / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
    distribution = SimpleNamespace(version='9.9', locate_file=lambda name: site / name)
    monkeypatch.setattr(candidate.metadata, 'distribution', lambda _: distribution)
    spec = ModuleSpec('qiskit', loader=None, origin=str(site / 'qiskit/__init__.py'), is_package=True)
    spec.submodule_search_locations = [str(site / 'qiskit')]
    monkeypatch.setattr(candidate.util, 'find_spec', lambda _: spec)
    return site, wheel, spec


@pytest.fixture
def build(tmp_path, installed):
    _, wheel, _ = installed
    root = tmp_path / 'build'
    root.mkdir()
    (root / wheel.name).write_bytes(wheel.read_bytes())
    (root / 'source.zip').write_bytes(b'retained-source-archive')
    (root / 'build.log').write_bytes(b'observed synthetic build')
    record = {'schema_version': 1, 'distribution': 'qiskit', 'source_commit': 'a' * 40,
              'source_archive': {'filename': 'source.zip', 'sha256': candidate.file_sha256(root / 'source.zip')},
              'wheel': {'filename': wheel.name, 'sha256': candidate.file_sha256(wheel)},
              'log': {'filename': 'build.log', 'sha256': candidate.file_sha256(root / 'build.log')},
              'command': ['synthetic-builder', '--offline'], 'environment': {'scope': 'synthetic-only'},
              'returncode': 0, 'independent_attestation': False,
              'build_tool_sha256': 'b' * 64, 'build_environment': {'PIP_NO_INDEX': '1'}}
    (root / 'build.json').write_bytes(canonical_bytes(record))
    return root, record


def environment():
    return {'implementation': {'sdkbench_version': 'test'},
            'image_descriptor_sha256': 'c' * 64, 'dependency_lock_sha256': 'd' * 64,
            'host': {'scope': 'synthetic-only'}}


def registration(monkeypatch, build):
    root, _ = build
    monkeypatch.setattr(candidate, 'distribution_fingerprint',
                        lambda name: {'name': name, 'version': '9.9', 'artifact_sha256': 'e' * 64})
    monkeypatch.setattr(candidate, 'capture_environment', environment)
    return candidate.create_registration(stack_id='qiskit-development', sdk='qiskit',
                                         workflow='qiskit.transpile', options={'optimization_level': 2},
                                         build_directory=root)


def test_wheel_payload_and_import_resolution_are_checked_without_import(installed):
    _, wheel, _ = installed
    check = candidate.verify_installed_wheel('qiskit', wheel)
    assert check['wheel_members_checked'] == 3
    assert len(check['package_tree_sha256']) == 64


@pytest.mark.parametrize('fault', ['changed', 'missing', 'unrecorded', 'shadow', 'search-path', 'symlink'])
def test_same_version_does_not_admit_replaced_code(installed, tmp_path, fault):
    site, wheel, spec = installed
    if fault == 'changed':
        (site / 'qiskit/compiler.py').write_text('REVISION = 2\n')
    elif fault == 'missing':
        (site / 'qiskit/compiler.py').unlink()
    elif fault == 'unrecorded':
        (site / 'qiskit/injected.py').write_text('REVISION = 2\n')
    elif fault == 'shadow':
        spec.origin = str(tmp_path / 'shadow/qiskit/__init__.py')
    elif fault == 'search-path':
        spec.submodule_search_locations.append(str(tmp_path / 'shadow'))
    else:
        original = site / 'qiskit/compiler.py'
        copied = tmp_path / 'compiler.py'
        copied.write_bytes(original.read_bytes())
        original.unlink()
        original.symlink_to(copied)
    with pytest.raises(ContractError):
        candidate.verify_installed_wheel('qiskit', wheel)


@pytest.mark.parametrize('fault', ['archive', 'wheel', 'log', 'failure', 'attestation', 'path', 'commit'])
def test_build_evidence_fails_closed(build, fault):
    root, record = build
    if fault in ('archive', 'wheel', 'log'):
        key = 'source_archive' if fault == 'archive' else fault
        (root / record[key]['filename']).write_bytes(b'changed')
    elif fault == 'failure':
        record['returncode'] = 1
    elif fault == 'attestation':
        record['independent_attestation'] = True
    elif fault == 'path':
        record['log']['filename'] = '../build.log'
    else:
        record['source_commit'] = 'main'
    (root / 'build.json').write_bytes(canonical_bytes(record))
    with pytest.raises(ContractError):
        candidate.verify_build(root)


def test_candidate_identity_binds_build_and_configuration(monkeypatch, build):
    admitted = registration(monkeypatch, build)
    assert admitted.stack_id == 'qiskit-development'
    assert admitted.components[1]['version'] == '9.9'
    assert admitted.configuration['options']['source_build']['source_commit'] == 'a' * 40
    for key in ('workflow', 'compiler_options', 'source_build'):
        configuration = deepcopy(admitted.configuration)
        configuration['options'][key] = {'changed': True}
        altered = replace(admitted, configuration=configuration)
        assert altered.configuration_sha256 != admitted.configuration_sha256
    with pytest.raises(ContractError, match='historical release IDs'):
        candidate.create_registration(stack_id='qiskit', sdk='qiskit', workflow='transpile',
                                      options={'level': 2}, build_directory=build[0])


@pytest.mark.parametrize('fault', ['none', 'source', 'dependency', 'component', 'import', 'unrecorded'])
def test_worker_can_recheck_before_sdk_import(monkeypatch, build, installed, fault):
    admitted = registration(monkeypatch, build)
    if fault == 'source':
        monkeypatch.setattr(candidate, 'implementation_fingerprint', lambda: 'f' * 64)
    elif fault == 'dependency':
        monkeypatch.setattr(candidate, 'capture_environment',
                            lambda: environment() | {'dependency_lock_sha256': 'f' * 64})
    elif fault == 'component':
        monkeypatch.setattr(candidate, 'distribution_fingerprint',
                            lambda name: {'name': name, 'version': '9.9', 'artifact_sha256': 'f' * 64})
    elif fault == 'import':
        installed[2].origin = str(Path(installed[2].origin).parent / 'shadow.py')
    elif fault == 'unrecorded':
        (installed[0] / 'qiskit/injected.py').write_text('unexpected = True')
    if fault == 'none':
        result = candidate.verify_runtime(admitted)
        assert result['configuration_sha256'] == admitted.configuration_sha256
        assert result['independent_attestation'] is False
    else:
        with pytest.raises(ContractError):
            candidate.verify_runtime(admitted)


@pytest.mark.parametrize('fault', ['none', 'payload', 'version', 'distribution',
                                  'digest', 'size', 'yanked', 'origin', 'duplicate'])
def test_published_wheel_admission_and_worker_revalidation(installed, monkeypatch, tmp_path, fault):
    site, wheel, _ = installed
    monkeypatch.setattr(candidate, 'capture_environment', environment)
    monkeypatch.setattr(candidate, 'distribution_fingerprint',
                        lambda name: {'name': name, 'version': '9.9', 'artifact_sha256': 'e' * 64})
    release = {'info': {'name': 'qiskit', 'version': '9.9'}, 'urls': [{
        'filename': wheel.name, 'url': 'https://files.pythonhosted.org/packages/candidate.whl',
        'packagetype': 'bdist_wheel', 'yanked': False, 'size': wheel.stat().st_size,
        'digests': {'sha256': candidate.file_sha256(wheel)},
    }]}
    entry = release['urls'][0]
    if fault == 'payload':
        (site / 'qiskit/compiler.py').write_text('changed = True\n')
    elif fault == 'version':
        release['info']['version'] = '9.8'
    elif fault == 'distribution':
        release['info']['name'] = 'different-sdk'
    elif fault == 'digest':
        entry['digests']['sha256'] = 'f' * 64
    elif fault == 'size':
        entry['size'] += 1
    elif fault == 'yanked':
        entry['yanked'] = True
    elif fault == 'origin':
        entry['url'] = 'https://files.pythonhosted.org.example.com/candidate.whl'
    elif fault == 'duplicate':
        release['urls'].append(deepcopy(entry))
    path = tmp_path / 'release.json'
    path.write_bytes(canonical_bytes(release))
    arguments = dict(stack_id='qiskit-published', sdk='qiskit', workflow='qiskit-transpile',
                     options={'optimization_level': 2}, wheel=wheel, release_metadata=path)
    if fault != 'none':
        with pytest.raises(ContractError):
            candidate.create_wheel_registration(**arguments)
        return
    admitted = candidate.create_wheel_registration(**arguments)
    origin = admitted.configuration['options']['published_wheel']
    assert origin['sha256'] == candidate.file_sha256(wheel)
    assert origin['release_metadata_sha256'] == candidate.file_sha256(path)
    assert 'source_build' not in admitted.configuration['options']
    candidate.verify_runtime(admitted)
    (site / 'qiskit/compiler.py').write_text('changed_after_admission = True\n')
    with pytest.raises(ContractError, match='package tree changed'):
        candidate.verify_runtime(admitted)
