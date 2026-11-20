"""Register verified compiler artifacts or run the unchanged frozen routing protocol."""
import argparse
import os
from pathlib import Path

from ..p0 import Bundle, Registration
from ..p0.models import canonical_bytes, read_json
from ..p1a.campaign import run_campaign
from .adapters import WORKFLOWS, workflow_configuration
from .provenance import create_registration, create_wheel_registration, file_sha256


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest='command', required=True)
    register = subparsers.add_parser('register', help='Register an installed source-build wheel')
    register.add_argument('--stack-id', required=True)
    register.add_argument('--workflow', required=True, choices=tuple(WORKFLOWS))
    register.add_argument('--build-directory', required=True, type=Path)
    register.add_argument('--output', required=True, type=Path)
    wheel = subparsers.add_parser('register-wheel', help='Register a verified published wheel')
    wheel.add_argument('--stack-id', required=True)
    wheel.add_argument('--workflow', required=True, choices=tuple(WORKFLOWS))
    wheel.add_argument('--wheel', required=True, type=Path)
    wheel.add_argument('--release-metadata', required=True, type=Path)
    wheel.add_argument('--output', required=True, type=Path)
    run = subparsers.add_parser('run', help='Execute all three frozen routing tasks')
    run.add_argument('--registration', action='append', required=True, type=Path)
    run.add_argument('--bundle', type=Path, default=Path('docs/implementation'))
    run.add_argument('--directory', required=True, type=Path)
    run.add_argument('--cgroup-parent', required=True, type=Path)
    run.add_argument('--cpu', required=True, type=int)
    run.add_argument('--interpreter', action='append', default=[], metavar='STACK=/ABS/PYTHON',
                     help='Select every candidate environment explicitly; never select only a subset')
    replay_parser = subparsers.add_parser('replay', help='Independently replay retained candidate evidence')
    replay_parser.add_argument('--bundle', type=Path, default=Path('docs/implementation'))
    replay_parser.add_argument('--directory', required=True, type=Path)
    args = parser.parse_args(argv)
    if args.command in ('register', 'register-wheel'):
        config = workflow_configuration(args.workflow)
        common = dict(stack_id=args.stack_id, sdk=config['sdk'], workflow=args.workflow, options=config)
        if args.command == 'register':
            result = create_registration(**common, build_directory=args.build_directory)
        else:
            result = create_wheel_registration(**common, wheel=args.wheel,
                                               release_metadata=args.release_metadata)
        with args.output.open('xb') as output:
            output.write(canonical_bytes(result.to_dict()))
        return 0
    if args.command == 'replay':
        from .replay import replay
        print(canonical_bytes(replay(args.directory, Bundle(args.bundle))).decode(), end='')
        return 0
    registrations = [Registration(**read_json(path)) for path in args.registration]
    if len({r.stack_id for r in registrations}) != len(registrations):
        parser.error('Each registration needs a distinct stack ID')
    interpreters = {}
    for argument in args.interpreter:
        name, separator, python = argument.partition('=')
        if not separator or name in interpreters or not Path(python).is_absolute():
            parser.error('Interpreter selections require distinct STACK=/ABS/PYTHON entries')
        interpreters[name] = python
    if interpreters and set(interpreters) != {r.stack_id for r in registrations}:
        parser.error('Provide an interpreter for every registered stack and no other stack')
    runtime_environment = {key: os.environ[key] for key in ('LD_LIBRARY_PATH',) if key in os.environ}
    # Select this verified harness revision in fresh workers. Participant code
    # still has to resolve to its admitted wheel installation.
    runtime_environment['PYTHONPATH'] = str(Path(__file__).resolve().parents[2])
    report = run_campaign(Bundle(args.bundle), directory=args.directory,
                          cgroup_parent=args.cgroup_parent, cpu=args.cpu,
                          suite='compiler-candidate', mode='protocol',
                          runtime_environment=runtime_environment,
                          candidates={r.stack_id: r for r in registrations},
                          candidate_interpreters=interpreters or None)
    manifest = {'schema_version': 1, 'files': {
        path.relative_to(args.directory).as_posix(): file_sha256(path)
        for path in sorted(args.directory.rglob('*')) if path.is_file()}}
    with (args.directory / 'MANIFEST.json').open('xb') as output:
        output.write(canonical_bytes(manifest))
    print(canonical_bytes(report).decode(), end='')
    return int(any(row['case_verdict']['status'] != 'accepted' for row in report['outcomes']))


if __name__ == '__main__':
    raise SystemExit(main())
