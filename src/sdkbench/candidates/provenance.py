"""Bind source-build observations and installed files to existing registrations.

These checks establish artifact identity, not independent build attestation or
publication-host qualification. Historical release admission is unchanged.
"""
from importlib import metadata, util
import hashlib
from pathlib import Path, PurePosixPath
import platform
import re
import sys
from zipfile import ZipFile

from ..p0.models import digest, keys, read_json, require
from ..p0.registration import Registration
from ..p1a.common import DISTRIBUTIONS
from ..p1a.provenance import capture_environment, distribution_fingerprint


def file_sha256(path):
    hasher = hashlib.sha256()
    with Path(path).open('rb') as stream:
        while chunk := stream.read(1024 * 1024):
            hasher.update(chunk)
    return hasher.hexdigest()


def implementation_fingerprint():
    """Include new adapters and workers absent from the frozen source selector."""
    root = Path(__file__).resolve().parents[1]
    return digest({p.relative_to(root).as_posix(): file_sha256(p)
                   for p in sorted(root.rglob('*.py'))})


def package_fingerprint(root):
    """Include unrecorded source files that an installed RECORD can miss."""
    root = Path(root)
    files = {}
    for path in sorted(root.rglob('*')):
        if '__pycache__' in path.parts or path.suffix == '.pyc':
            continue
        require(not path.is_symlink(), 'Candidate package contains a symlink')
        if path.is_file():
            files[path.relative_to(root).as_posix()] = file_sha256(path)
    require(files, 'Candidate package tree is empty')
    return files


def verify_build(directory):
    """Verify the retained build files before admission, without executing them."""
    root = Path(directory).resolve()
    build = read_json(root / 'build.json')
    keys(build, ('schema_version', 'distribution', 'source_commit', 'source_archive',
                 'wheel', 'command', 'environment', 'log', 'returncode',
                 'independent_attestation', 'build_tool_sha256', 'build_environment'))
    require(build['schema_version'] == 1 and type(build['schema_version']) is int,
            'Unknown candidate build record')
    require(isinstance(build['distribution'], str) and build['distribution'].strip(),
            'Missing build distribution')
    require(isinstance(build['source_commit'], str)
            and re.fullmatch('[0-9a-f]{40}|[0-9a-f]{64}', build['source_commit']),
            'Build requires a full source commit')
    require(type(build['returncode']) is int and build['returncode'] == 0,
            'Candidate build did not succeed')
    require(build['independent_attestation'] is False,
            'Observed local build cannot assert independent attestation')
    require(isinstance(build['command'], list) and build['command']
            and all(isinstance(part, str) and part for part in build['command']),
            'Missing exact build command')
    require(isinstance(build['environment'], dict) and build['environment'],
            'Missing build environment observation')
    require(isinstance(build['build_environment'], dict) and build['build_environment'],
            'Missing explicit build environment')
    require(isinstance(build['build_tool_sha256'], str)
            and re.fullmatch('[0-9a-f]{64}', build['build_tool_sha256']),
            'Missing candidate build tool identity')
    for name in ('source_archive', 'wheel', 'log'):
        entry = build[name]
        keys(entry, ('filename', 'sha256'))
        filename = entry['filename']
        require(isinstance(filename, str) and filename not in ('', '.', '..')
                and Path(filename).name == filename and '\\' not in filename,
                'Build artifact must be a direct child')
        path = root / filename
        require(not path.is_symlink() and path.is_file(), 'Missing build artifact: ' + filename)
        require(file_sha256(path) == entry['sha256'], 'Build artifact hash mismatch: ' + name)
    require(build['wheel']['filename'].endswith('.whl'), 'Missing built wheel')
    return build


def verify_installed_wheel(distribution, wheel):
    """Check wheel payload bytes and module resolution without importing an SDK.

    RECORD is rewritten by installers and is checked through the installed-file
    fingerprint instead. Relocated wheel data requires a reviewed mapping; it
    is refused here rather than silently omitted from the provenance check.
    """
    installed = metadata.distribution(distribution)
    checked = 0
    package_members = set()
    wheel_metadata = None
    with ZipFile(wheel) as archive:
        names = archive.namelist()
        require(len(names) == len(set(names)), 'Duplicate wheel member')
        for item in archive.infolist():
            if item.is_dir():
                continue
            relative = PurePosixPath(item.filename)
            require(not relative.is_absolute() and '..' not in relative.parts
                    and '\\' not in item.filename, 'Unsafe wheel member')
            require(not any(part.endswith('.data') for part in relative.parts),
                    'Relocated wheel data requires an explicit reviewed mapping')
            if item.filename.endswith('.dist-info/RECORD'):
                continue
            content = archive.read(item)
            path = Path(installed.locate_file(item.filename))
            require(path.is_file() and not path.is_symlink(),
                    'Installed wheel member missing: ' + item.filename)
            require(file_sha256(path) == hashlib.sha256(content).hexdigest(),
                    'Installed file differs from wheel: ' + item.filename)
            if item.filename.endswith('.dist-info/METADATA'):
                require(wheel_metadata is None, 'Multiple wheel distribution metadata entries')
                from email.parser import BytesParser
                wheel_metadata = BytesParser().parsebytes(content)
            checked += 1
            package_members.add(item.filename)
    require(checked and wheel_metadata is not None, 'Wheel has no distribution payload')
    normalize = lambda name: re.sub('[-_.]+', '-', name).lower()
    require(normalize(wheel_metadata['Name'] or '') == normalize(distribution)
            and wheel_metadata['Version'] == installed.version,
            'Wheel distribution identity differs from installed SDK')
    sdk = next((s for s, name in DISTRIBUTIONS.items()
                if normalize(name) == normalize(distribution)), None)
    require(sdk is not None, 'No reviewed candidate SDK module mapping')
    spec = util.find_spec(sdk)
    expected = Path(installed.locate_file(sdk + '/__init__.py')).resolve()
    require(spec is not None and spec.origin is not None
            and Path(spec.origin).resolve() == expected,
            'SDK import resolves outside the verified wheel')
    require(spec.submodule_search_locations is not None
            and [Path(p).resolve() for p in spec.submodule_search_locations] == [expected.parent],
            'SDK import search path differs from verified wheel')
    inventory = package_fingerprint(expected.parent)
    actual_members = {sdk + '/' + name for name in inventory}
    require(actual_members == {name for name in package_members if name.startswith(sdk + '/')},
            'Installed SDK package contains unverified or missing files')
    return {'wheel_members_checked': checked, 'module_origin': str(expected),
            'package_tree_sha256': digest(inventory),
            'record_policy': 'installer RECORD excluded from wheel comparison; installed fingerprint includes it'}


def create_registration(*, stack_id, sdk, workflow, options, build_directory,
                        environment=None):
    """Register a newly built compiler/configuration using the P0 identity.

    The build directory must come from the explicit candidate build tool and its
    wheel must already be installed in this interpreter. No install or import
    of the participant SDK is performed by this function.
    """
    require(sdk in DISTRIBUTIONS, 'Unknown candidate SDK')
    require(isinstance(stack_id, str) and re.fullmatch('[a-z][a-z0-9-]*', stack_id)
            and stack_id not in DISTRIBUTIONS,
            'Candidate stack ID must differ from historical release IDs')
    require(isinstance(workflow, str) and workflow.strip(), 'Missing declared public workflow')
    require(isinstance(options, dict) and options, 'Missing declared compiler options')
    build = verify_build(build_directory)
    require(build['distribution'] == DISTRIBUTIONS[sdk], 'Candidate build distribution mismatch')
    installed_check = verify_installed_wheel(DISTRIBUTIONS[sdk],
                                           Path(build_directory) / build['wheel']['filename'])
    environment = capture_environment() if environment is None else environment
    names = [DISTRIBUTIONS[sdk], 'numpy']
    names += ['torch'] if sdk == 'flagquantum' else ['sympy', 'networkx'] if sdk == 'cirq' else []
    components = [{'name': 'sdkbench', 'version': environment['implementation']['sdkbench_version'],
                   'role': 'harness', 'artifact_sha256': implementation_fingerprint()}]
    for name in names:
        observed = distribution_fingerprint(name)
        components.append({key: observed[key] for key in ('name', 'version', 'artifact_sha256')}
                          | {'role': 'frontend' if name == DISTRIBUTIONS[sdk] else 'numerical-dependency'})
    configuration = {
        'profile': 'CPU1-FP64', 'precision': 'float64/complex128', 'threads': 1,
        'options': {'suite': 'compiler-candidate', 'sdk': sdk, 'workflow': workflow,
                    'compiler_options': options, 'source_build': build,
                    'installed_wheel_check': installed_check,
                    'implementation_sha256': implementation_fingerprint()},
    }
    return Registration(stack_id, components, configuration, {
        'python': platform.python_version(), 'os': platform.platform(),
        'image_sha256': environment['image_descriptor_sha256'],
        'dependency_lock_sha256': environment['dependency_lock_sha256'],
        'host': environment['host'],
    })


def verify_runtime(registration):
    """Reject changed code or environment before a candidate SDK is imported."""
    require(isinstance(registration, Registration), 'Expected a P0 registration')
    options = registration.configuration['options']
    require(options['suite'] == 'compiler-candidate', 'Not a candidate registration')
    require(options['implementation_sha256'] == implementation_fingerprint(),
            'Candidate harness source changed after admission')
    environment = capture_environment()
    require(environment['dependency_lock_sha256'] == registration.environment['dependency_lock_sha256'],
            'Candidate dependency environment changed after admission')
    require(platform.python_version() == registration.environment['python']
            and platform.platform() == registration.environment['os'],
            'Candidate interpreter/platform changed after admission')
    for component in registration.components:
        if component['role'] == 'harness':
            require(component['artifact_sha256'] == implementation_fingerprint(),
                    'Candidate harness component mismatch')
            continue
        actual = distribution_fingerprint(component['name'])
        require(all(actual[key] == component[key] for key in ('name', 'version', 'artifact_sha256')),
                'Candidate installed component changed: ' + component['name'])
    sdk = options['sdk']
    spec = util.find_spec(sdk)
    require(spec is not None and spec.origin == options['installed_wheel_check']['module_origin'],
            'Candidate SDK import resolution changed after admission')
    require(spec.submodule_search_locations is not None
            and list(spec.submodule_search_locations) == [str(Path(spec.origin).parent)],
            'Candidate SDK import search path changed after admission')
    require(digest(package_fingerprint(Path(spec.origin).parent))
            == options['installed_wheel_check']['package_tree_sha256'],
            'Candidate SDK package tree changed after admission')
    require(sdk not in sys.modules,
            'Candidate SDK was imported before runtime admission')
    return {'configuration_sha256': registration.configuration_sha256,
            'environment_sha256': registration.environment_sha256,
            'independent_attestation': False}
