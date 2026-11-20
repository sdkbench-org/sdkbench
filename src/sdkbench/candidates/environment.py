"""Admit compiler registrations in their own interpreters without SDK imports."""

from __future__ import annotations

import argparse
import os
import signal
import subprocess
import sys
import tempfile
from pathlib import Path

from ..p0 import Registration
from ..p0.models import canonical_bytes, digest, keys, read_json, require
from ..p0.supervisor import THREAD_ENV
from .provenance import file_sha256, verify_runtime


def interpreter_identity(python: str) -> dict:
    """Retain the invocation path, including its virtual-environment prefix."""
    path = Path(python)
    require(path.is_absolute(), 'Candidate interpreter must be an absolute path')
    require(path.is_file() and os.access(path, os.X_OK), 'Candidate interpreter is unavailable')
    # Resolving a venv's Python symlink would select the base environment.
    return {'python': str(path), 'executable_sha256': file_sha256(path)}


def verify_interpreter(expected: dict) -> None:
    keys(expected, ('python', 'executable_sha256'))
    require(interpreter_identity(sys.executable) == expected,
            'Worker interpreter differs from the declared environment')


def admit_interpreter(registration: Registration, expected: dict, environment: dict,
                      *, inventory: dict | None = None) -> dict:
    """Check a target environment with a bounded, SDK-free setup process.

    This setup observation is separate from measured worker execution. It does
    not establish kernel isolation, host qualification, or build attestation.
    The measured worker repeats admission under the unchanged supervisor.
    """
    require(interpreter_identity(expected['python']) == expected,
            'Candidate interpreter changed before admission')
    env = {'PATH': '/usr/local/bin:/usr/bin:/bin', 'LANG': 'C.UTF-8',
           'PYTHONHASHSEED': '0', **environment}
    env.update({name: '1' for name in THREAD_ENV})
    env['OMP_DYNAMIC'] = env['MKL_DYNAMIC'] = 'FALSE'
    with tempfile.TemporaryDirectory(prefix='sdkbench-interpreter-admission-') as folder:
        root = Path(folder)
        path = root / 'registration.json'
        path.write_bytes(canonical_bytes(registration.to_dict()))
        env['HOME'] = env['TMPDIR'] = str(root)
        command = [expected['python'], '-m', 'sdkbench.candidates.environment', str(path)]
        if inventory is not None:
            inventory_path = root / 'inventory.json'
            inventory_path.write_bytes(canonical_bytes(inventory))
            command += ['--inventory', str(inventory_path)]
        with subprocess.Popen(command, cwd=root, env=env, stdin=subprocess.DEVNULL,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              start_new_session=True) as process:
            try:
                stdout, stderr = process.communicate(timeout=120)
            except subprocess.TimeoutExpired as exc:
                os.killpg(process.pid, signal.SIGKILL)
                process.communicate(timeout=5)
                raise TimeoutError('Candidate environment admission exceeded 120 seconds') from exc
        require(len(stdout) + len(stderr) <= 1024 * 1024,
                'Candidate environment admission output exceeded one MiB')
        require(process.returncode == 0,
                'Candidate environment admission failed: ' + stderr.decode(errors='replace')[-4096:])
        result_path = root / 'admission.json'
        result_path.write_bytes(stdout)
        result = read_json(result_path, max_bytes=1024 * 1024)
    verify_interpreter_admission(registration, expected, result)
    return result


def verify_interpreter_admission(registration: Registration, expected: dict, result: dict) -> None:
    """Check retained admission bindings without accessing the original host."""
    keys(result, ('registration_sha256', 'interpreter', 'admission'))
    require(result['registration_sha256'] == digest(registration.to_dict())
            and result['interpreter'] == expected
            and result['admission'] == {
                'configuration_sha256': registration.configuration_sha256,
                'environment_sha256': registration.environment_sha256,
                'independent_attestation': False,
            }, 'Candidate interpreter admission binding mismatch')


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('registration', type=Path)
    parser.add_argument('--inventory', type=Path)
    args = parser.parse_args()
    registration = Registration(**read_json(args.registration))
    if args.inventory is not None:
        from ..p1a.provenance import capture_environment
        from .revisions import verify_inventory_observation
        verify_inventory_observation(read_json(args.inventory), capture_environment())
    result = {'registration_sha256': digest(registration.to_dict()),
              'interpreter': interpreter_identity(sys.executable),
              'admission': verify_runtime(registration)}
    print(canonical_bytes(result).decode(), end='')


if __name__ == '__main__':
    main()
