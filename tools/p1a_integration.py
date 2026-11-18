#!/usr/bin/env python3
"""Real Linux P1a qualification with complete raw evidence and explicit partial scope."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import sys

from sdkbench.p0 import Bundle
from sdkbench.p0.models import canonical_bytes
from sdkbench.p1a.campaign import run_campaign


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--bundle',type=Path,default=Path('docs/implementation'))
    parser.add_argument('--directory',type=Path,required=True)
    parser.add_argument('--cgroup-parent',type=Path,required=True)
    args=parser.parse_args()
    root=args.directory.resolve();root.mkdir(parents=True,exist_ok=True)
    if any(root.iterdir()):raise ValueError('Evidence directory must be empty')
    bundle=Bundle(args.bundle);cpu=min(os.sched_getaffinity(0))
    environment={k:os.environ[k] for k in ['LD_LIBRARY_PATH'] if k in os.environ}
    context={'schema_version':1,'source_commit':os.environ.get('GITHUB_SHA'),'github_run_id':os.environ.get('GITHUB_RUN_ID'),
             'runner_image_version':os.environ.get('ImageVersion'),'cpu':cpu,'runtime_environment':environment,
             'publication_eligible':False,'scope':'engineering integration; not a global SDK ranking'}
    (root/'context.json').write_bytes(canonical_bytes(context))
    reports={}
    try:
        # Every frozen P1a size is attempted with its original per-case cap.
        reports['all-instances']=run_campaign(bundle,directory=root/'all-instances',cgroup_parent=args.cgroup_parent,cpu=cpu,
                                              mode='qualification',runtime_environment=environment)
        # Complete fresh-process blocks for the four small integration cases.
        reports['small-protocol']=run_campaign(bundle,directory=root/'small-protocol',cgroup_parent=args.cgroup_parent,cpu=cpu,
                                              instances=['PARAM-04','OBS-04','SAMPLE-03','SAMPLE-05'],mode='protocol',runtime_environment=environment)
        summary={name:{'outcomes':report['outcomes'],'workflows':report['workflows'],'scope':report['scope'],
                       'unselected_instances':report['unselected_instances']} for name,report in reports.items()}
        (root/'integration-summary.json').write_bytes(canonical_bytes(summary))
        print(json.dumps(summary,indent=2,allow_nan=False))
        failed=any(row['qualification_status']!='accepted' for report in reports.values() for row in report['outcomes'])
        return int(failed)
    finally:
        files={path.relative_to(root).as_posix():hashlib.sha256(path.read_bytes()).hexdigest()
               for path in sorted(root.rglob('*')) if path.is_file() and path.name!='MANIFEST.json'}
        (root/'MANIFEST.json').write_bytes(canonical_bytes({'schema_version':1,'files':files}))


if __name__=='__main__':raise SystemExit(main())
