"""Observed environment and installed-file provenance, never fabricated image seals."""
from importlib import metadata
import hashlib
import json
import platform
from pathlib import Path
from ..p0.models import canonical_bytes, digest
from ..p0.supervisor import host_snapshot
from .. import __version__


def distribution_fingerprint(name):
    distribution = metadata.distribution(name); hasher = hashlib.sha256(); files = 0
    for entry in sorted(distribution.files or [], key=str):
        if str(entry).endswith('.pyc') or '__pycache__' in str(entry):continue
        path = Path(distribution.locate_file(entry))
        if not path.is_file():continue
        hasher.update(str(entry).encode()); hasher.update(b'\0')
        with path.open('rb') as stream:
            while data := stream.read(1024 * 1024):hasher.update(data)
        files += 1
    if not files:raise ValueError('No installed distribution files: ' + name)
    return {'name': name, 'version': distribution.version, 'artifact_sha256': hasher.hexdigest(), 'files_hashed': files,
            'fingerprint_kind': 'installed-non-pyc-file-content'}


def source_fingerprint():
    root = Path(__file__).resolve().parents[1]; hasher = hashlib.sha256()
    for subdir in ('p0', 'p1a'):
        for path in sorted((root / subdir).glob('*.py')):
            hasher.update(path.relative_to(root).as_posix().encode()); hasher.update(b'\0'); hasher.update(path.read_bytes())
    legacy = hasher.hexdigest()
    for path in sorted((root / 'p1b').glob('*.py')):
        hasher.update(path.relative_to(root).as_posix().encode()); hasher.update(b'\0'); hasher.update(path.read_bytes())
    return {'sdkbench_version': __version__, 'p0_p1a_source_sha256': legacy, 'runtime_source_sha256': hasher.hexdigest()}


def capture_environment():
    dependencies = sorted([{'name': d.metadata['Name'], 'version': d.version,
                            'record_sha256': hashlib.sha256((d.read_text('RECORD') or '').encode()).hexdigest()}
                           for d in metadata.distributions() if d.metadata['Name']], key=lambda x: x['name'].lower())
    host = host_snapshot()
    descriptor = {'platform': platform.platform(), 'os_release': Path('/etc/os-release').read_text() if Path('/etc/os-release').exists() else None,
                  'kernel': platform.release()}
    return {'schema_version': 1, 'dependencies': dependencies, 'dependency_lock_sha256': digest(dependencies), 'host': host,
            'image_descriptor': descriptor, 'image_descriptor_sha256': digest(descriptor), 'sealed_image': False,
            'scope': 'observed engineering environment; not a qualified publication host', 'implementation': source_fingerprint()}
