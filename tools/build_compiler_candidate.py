#!/usr/bin/env python3
"""Archive an immutable Git revision and retain an observed offline wheel build.

Run in a prepared build environment. The compiler build is outside measurement;
candidate execution still requires the existing Linux resource supervisor.
"""
import argparse
import os
from pathlib import Path, PurePosixPath
import signal
import subprocess
import sys
from zipfile import ZipFile

from sdkbench.candidates.provenance import file_sha256
from sdkbench.p0.models import canonical_bytes, require
from sdkbench.p1a.provenance import capture_environment


def git(repository, *arguments):
    result = subprocess.run(['git', '-C', str(repository), *arguments],
                            capture_output=True, text=True, timeout=60, check=True)
    return result.stdout.strip()


def build_candidate(repository, revision, distribution, directory, timeout=900):
    """Build from a Git archive, preserving the command, log and input hashes."""
    root = Path(directory).resolve()
    root.mkdir(parents=True, exist_ok=True)
    require(not any(root.iterdir()), 'Never overwrite candidate build evidence')
    require(type(timeout) is int and 0 < timeout <= 3600, 'Invalid build timeout')
    require(isinstance(distribution, str) and distribution.strip(), 'Missing distribution name')
    commit = git(repository, 'rev-parse', '--verify', revision + '^{commit}')
    archive_path = root / 'source.zip'
    subprocess.run(['git', '-C', str(repository), 'archive', '--format=zip',
                    '--output=' + str(archive_path), commit], check=True, timeout=60)
    source = root / 'source'
    source.mkdir()
    with ZipFile(archive_path) as archive:
        for entry in archive.infolist():
            path = PurePosixPath(entry.filename)
            require(not path.is_absolute() and '..' not in path.parts
                    and '\\' not in entry.filename, 'Unsafe source archive member')
            require((entry.external_attr >> 16) & 0o170000 != 0o120000,
                    'Candidate source archive symlinks need explicit review')
        archive.extractall(source)
    command = [sys.executable, '-m', 'build', '--wheel', '--no-isolation',
               '--outdir', str(root), str(source)]
    environment = capture_environment()
    # Explicit build controls avoid inheriting credentials or hidden PYTHONPATH
    # overrides. Every passed value is retained with the build observation.
    controls = ('PATH', 'CC', 'CXX', 'CFLAGS', 'CXXFLAGS', 'CPPFLAGS', 'LDFLAGS',
                'SDKROOT', 'MACOSX_DEPLOYMENT_TARGET', 'CMAKE_ARGS', 'MAX_JOBS',
                'FQ_BUILD_EMBEDDED_STIM')
    build_env = {key: os.environ[key] for key in controls if key in os.environ}
    build_env.update(PIP_NO_INDEX='1', PIP_DISABLE_PIP_VERSION_CHECK='1',
                     HOME=str(root), TMPDIR=str(root), LC_ALL='C',
                     PYTHONHASHSEED='0', OMP_NUM_THREADS='1', MAX_JOBS='1')
    timed_out = False
    with (root / 'build.log').open('wb') as log:
        process = subprocess.Popen(command, stdout=log, stderr=subprocess.STDOUT,
                                   env=build_env, start_new_session=True)
        try:
            process.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            timed_out = True
            os.killpg(process.pid, signal.SIGKILL)
            process.wait(timeout=15)
    wheels = sorted(root.glob('*.whl'))
    def artifact(path):
        return {'filename': path.name, 'sha256': file_sha256(path)}
    record = {
        'schema_version': 1, 'distribution': distribution, 'source_commit': commit,
        'source_archive': artifact(archive_path),
        'wheel': artifact(wheels[0]) if len(wheels) == 1 else None,
        'command': command, 'environment': environment, 'log': artifact(root / 'build.log'),
        'returncode': process.returncode, 'independent_attestation': False,
        'build_environment': build_env, 'build_tool_sha256': file_sha256(__file__),
    }
    (root / 'build.json').write_bytes(canonical_bytes(record))
    require(not timed_out, 'Candidate build exceeded its wall budget; build evidence retained')
    require(process.returncode == 0 and len(wheels) == 1,
            'Candidate build failed or produced an ambiguous wheel set; inspect build.log')
    return record


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repository', required=True, type=Path)
    parser.add_argument('--revision', required=True)
    parser.add_argument('--distribution', required=True)
    parser.add_argument('--directory', required=True, type=Path)
    parser.add_argument('--timeout', type=int, default=900)
    args = parser.parse_args(argv)
    record = build_candidate(args.repository, args.revision, args.distribution,
                             args.directory, args.timeout)
    print(canonical_bytes(record).decode(), end='')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
