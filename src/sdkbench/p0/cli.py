"""Repository-bundle P0 tools, separate from the legacy timing harness."""
import argparse
from dataclasses import asdict
import json
from pathlib import Path
import sys
from .bundle import Bundle
from .evaluators import evaluate, evaluate_case, evaluate_workflow
from .execution import execute_once
from .models import Identity, ResultRecord, canonical_bytes, read_json


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--bundle', type=Path, required=True, help='Directory containing the frozen roadmap and artifacts')
    commands = parser.add_subparsers(dest='command', required=True)
    commands.add_parser('inspect', help='Verify all bundle hashes and list frozen cases')
    validate = commands.add_parser('validate', help='Evaluate one result or a full case record list')
    validate.add_argument('input', type=Path)
    coverage = validate.add_mutually_exclusive_group()
    coverage.add_argument('--full-case', action='store_true')
    coverage.add_argument('--workflow', help='Require every case/block/repetition of this workflow')
    execute = commands.add_parser('execute', help='Run one reviewed adapter command with strict Linux controls')
    execute.add_argument('--identity', type=Path, required=True)
    execute.add_argument('--cgroup-parent', type=Path, required=True)
    execute.add_argument('--cpu', type=int, required=True)
    execute.add_argument('--directory', type=Path, required=True)
    execute.add_argument('--environment', type=Path, help='Explicit runtime environment JSON, e.g. pinned loader paths')
    execute.add_argument('--block', type=int, default=0)
    execute.add_argument('--repetition', type=int, default=0)
    execute.add_argument('--stage', choices=('case', 'compile'), default='case')
    execute.add_argument('argv', nargs=argparse.REMAINDER)
    args = parser.parse_args(argv)
    try:
        bundle = Bundle(args.bundle)
        if args.command == 'inspect':
            result = {'protocol_revision': bundle.plan['protocol_revision'], 'instances': list(bundle.cases), 'status': 'hash-verified-only'}
        elif args.command == 'validate':
            data = read_json(args.input)
            if args.workflow:
                if not isinstance(data, list):raise ValueError('Workflow input must be a record list')
                result = evaluate_workflow(bundle, args.workflow, data).to_dict()
            elif args.full_case:
                if not isinstance(data, list) or not data:raise ValueError('Full-case input must be a nonempty record list')
                identity = ResultRecord.from_dict(data[0]).identity
                result = evaluate_case(bundle, identity, data).to_dict()
            else:result = evaluate(bundle, data).to_dict()
        else:
            identity = Identity(**read_json(args.identity)); command = args.argv
            if command[:1] == ['--']:command = command[1:]
            result = execute_once(bundle, identity, command, cgroup_parent=args.cgroup_parent, cpu=args.cpu,
                                  directory=args.directory, block=args.block, repetition=args.repetition, stage=args.stage,
                                  environment=read_json(args.environment) if args.environment else None)
        print(canonical_bytes(result).decode(), end='')
        if args.command == 'inspect':return 0
        return 0 if result.get('verdict', result).get('status') == 'accepted' else 1
    except (ValueError, OSError, KeyError, TypeError) as exc:
        print('sdkbench-p0: ' + str(exc), file=sys.stderr); return 2


if __name__ == '__main__':raise SystemExit(main())
