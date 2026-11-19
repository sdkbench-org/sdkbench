"""Build orchestration retains evidence and cleans timed-out process groups."""
import importlib.util
from pathlib import Path
import subprocess
from zipfile import ZipFile

import pytest

from sdkbench.p0.models import ContractError, read_json


def load_builder():
    path = Path(__file__).resolve().parents[1] / 'tools/build_compiler_candidate.py'
    spec = importlib.util.spec_from_file_location('candidate_builder', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize('outcome', ['success', 'failure', 'timeout'])
def test_build_records_exact_input_and_terminates_timeout(tmp_path, monkeypatch, outcome):
    builder = load_builder()
    root = tmp_path / 'output'
    monkeypatch.setattr(builder, 'git', lambda *_: 'a' * 40)
    def archive(argv, **kwargs):
        assert kwargs == {'check': True, 'timeout': 60}
        assert argv[-1] == 'a' * 40
        destination = next(arg.split('=', 1)[1] for arg in argv if arg.startswith('--output='))
        with ZipFile(destination, 'w') as zipped:
            zipped.writestr('pyproject.toml', '[project]\nname = "qiskit"\n')
        return subprocess.CompletedProcess(argv, 0)
    monkeypatch.setattr(builder.subprocess, 'run', archive)
    monkeypatch.setattr(builder, 'capture_environment', lambda: {'scope': 'synthetic-only'})
    calls = []
    killed = []
    class Process:
        pid = 43210
        returncode = None
        def __init__(self, command, **kwargs):
            calls.append((command, kwargs))
            assert kwargs['start_new_session'] is True
            assert 'PYTHONPATH' not in kwargs['env']
            kwargs['stdout'].write(b'retained compiler output')
        def wait(self, timeout):
            if outcome == 'timeout' and not killed:
                raise subprocess.TimeoutExpired(calls[0][0], timeout)
            self.returncode = -9 if killed else 1 if outcome == 'failure' else 0
            if self.returncode == 0:
                (root / 'qiskit.whl').write_bytes(b'synthetic-wheel')
            return self.returncode
    monkeypatch.setattr(builder.subprocess, 'Popen', Process)
    monkeypatch.setattr(builder.os, 'killpg', lambda pid, sig: killed.append((pid, sig)))
    monkeypatch.setenv('PYTHONPATH', 'unreviewed-override')
    if outcome == 'success':
        builder.build_candidate(tmp_path, 'main', 'qiskit', root, timeout=3)
    else:
        with pytest.raises(ContractError):
            builder.build_candidate(tmp_path, 'main', 'qiskit', root, timeout=3)
    record = read_json(root / 'build.json')
    assert record['source_commit'] == 'a' * 40
    assert record['command'] == calls[0][0]
    assert record['build_environment'] == calls[0][1]['env']
    assert '--no-isolation' in record['command']
    assert record['log']['sha256'] == builder.file_sha256(root / 'build.log')
    assert record['independent_attestation'] is False
    assert bool(killed) == (outcome == 'timeout')
    assert record['returncode'] == (0 if outcome == 'success' else -9 if outcome == 'timeout' else 1)
