#!/usr/bin/env python3
"""Verify and losslessly archive engineering evidence without importing any SDK."""
import argparse
import gzip
import hashlib
import json
from pathlib import Path
from sdkbench.p0 import Bundle, evaluate
from sdkbench.p0.models import canonical_bytes, read_json, require


def verify(root, bundle):
    root=Path(root).resolve(); manifest=read_json(root/'MANIFEST.json')
    actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file() and p.name!='MANIFEST.json'}
    require(actual==set(manifest['files']),'Missing or extra evidence files')
    for relative,digest in manifest['files'].items():
        path=(root/relative).resolve();require(path.is_relative_to(root),'Evidence path escapes archive')
        require(hashlib.sha256(path.read_bytes()).hexdigest()==digest,'Evidence hash mismatch: '+relative)
    replay=[]
    for path in sorted(root.glob('*/*/*/*/evidence.json')):
        evidence=read_json(path)
        stored_verdicts=evidence.get('record_verdicts')
        if stored_verdicts is not None:require(len(stored_verdicts)==len(evidence['records']),'Missing stored verdicts')
        for index,raw in enumerate(evidence['records']):
            verdict=evaluate(bundle,raw)
            if stored_verdicts is not None:
                require(verdict.status==stored_verdicts[index]['status'],'Independent replay disagrees: '+str(path))
        response=evidence.get('response')
        if response:
            require(len(response['warmups'])==len(evidence['warmup_verdicts']),'Missing warmup decisions')
            for raw,stored in zip(response['warmups'],evidence['warmup_verdicts']):
                require(evaluate(bundle,raw).status==stored['status'],'Warmup replay disagrees')
        replay.append({'path':path.relative_to(root).as_posix(),'status':evidence['block_verdict']['status']})
    require(replay,'No block evidence found')
    return {'schema_version':1,'context':read_json(root/'context.json'),'blocks_verified':len(replay),
            'files_verified':len(actual),'block_outcomes':replay,
            'reports':{p.parent.name:read_json(p) for p in root.glob('*/report.json')},
            'publication_eligible':False}


def archive(root, output):
    root=Path(root).resolve(); output=Path(output)
    require(not output.exists(),'Never overwrite archived evidence')
    files={p.relative_to(root).as_posix():{'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),
                                        'utf8':p.read_text(encoding='utf-8')}
           for p in sorted(root.rglob('*')) if p.is_file()}
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_bytes(gzip.compress(canonical_bytes({'schema_version':1,'files':files}),mtime=0))
    return hashlib.sha256(output.read_bytes()).hexdigest()


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--directory',type=Path,required=True);parser.add_argument('--bundle',type=Path,required=True)
    parser.add_argument('--archive',type=Path);parser.add_argument('--summary',type=Path)
    args=parser.parse_args(argv)
    summary=verify(args.directory,Bundle(args.bundle))
    if args.archive:summary['archive_sha256']=archive(args.directory,args.archive)
    if args.summary:
        require(not args.summary.exists(),'Never overwrite replay summary')
        args.summary.write_bytes(canonical_bytes(summary))
    print(json.dumps({'blocks_verified':summary['blocks_verified'],'files_verified':summary['files_verified'],
                      'publication_eligible':False},indent=2))
    return 0


if __name__=='__main__':raise SystemExit(main())
