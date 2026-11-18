"""Run P1a task adapters with explicit bundles and strict Linux execution controls."""
import argparse
import json
from pathlib import Path
import sys
from ..p0 import Bundle
from ..p0.models import read_json
from .campaign import run_campaign
from .common import SDKS


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--bundle', required=True, type=Path)
    parser.add_argument('--directory', required=True, type=Path)
    parser.add_argument('--cgroup-parent', required=True, type=Path)
    parser.add_argument('--cpu', type=int, required=True)
    parser.add_argument('--sdk', choices=SDKS, action='append')
    parser.add_argument('--instance', action='append', help='A declared partial scope; unselected cases remain listed')
    parser.add_argument('--mode', choices=('protocol', 'qualification'), default='protocol')
    parser.add_argument('--environment', type=Path, help='Explicit runtime environment JSON, including any pinned loader paths')
    args = parser.parse_args(argv)
    try:
        report = run_campaign(Bundle(args.bundle), directory=args.directory, cgroup_parent=args.cgroup_parent, cpu=args.cpu,
                              sdks=tuple(args.sdk or SDKS), instances=args.instance, mode=args.mode,
                              runtime_environment=read_json(args.environment) if args.environment else None)
        print(json.dumps({'mode': report['mode'], 'publication_eligible': False, 'outcomes': report['outcomes']}, indent=2, allow_nan=False))
        failed = any((row['qualification_status'] if args.mode == 'qualification' else row['case_verdict']['status']) != 'accepted'
                     for row in report['outcomes'])
        return int(failed)
    except (OSError, ValueError, TypeError, KeyError) as exc:
        print('sdkbench-p1a: ' + str(exc), file=sys.stderr); return 2


if __name__ == '__main__':raise SystemExit(main())
