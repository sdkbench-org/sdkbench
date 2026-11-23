#!/usr/bin/env python3
"""Replay stored full-state correctness and hash inventory without participant SDKs."""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
from gpu_statevector import operations,reference,sha,write


def verify(root):
    root=root.resolve();manifest=json.loads((root/'MANIFEST.json').read_text())
    actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file() and p.name!='MANIFEST.json'}
    assert actual==set(manifest['files']), 'Missing/extra evidence files'
    assert not any(p.is_symlink() for p in root.rglob('*')), 'Linked evidence'
    for name,pin in manifest['files'].items():
        path=(root/name).resolve();assert path.is_relative_to(root)
        assert path.stat().st_size==pin['bytes'] and sha(path)==pin['sha256'], 'Evidence bytes differ: '+name
    p=json.loads((root/'profile.json').read_text());c=json.loads((root/'context.json').read_text())
    outcomes=json.loads((root/'execution-summary.json').read_text());rows=[]
    assert c['profile_sha256']==sha(root/'profile.json')
    assert len(outcomes)==len(p['participants'])*len(p['qubits'])*p['blocks']
    seen=set();statuses={}
    for n in p['qubits']:
        oracle=reference(n,operations(n,p['layers'],p['seed']))
        stored=np.load(root/'references'/f'{n}.npy',allow_pickle=False)
        assert np.array_equal(stored,oracle), 'Stored reference differs'
        for participant in p['participants']:
            for block in range(p['blocks']):
                key=(participant,f'SV-{n:02d}',block)
                matches=[o for o in outcomes if (o['participant'],o['instance'],o['block'])==key]
                assert len(matches)==1 and key not in seen;seen.add(key);execution=matches[0]
                directory=root/participant/f'SV-{n:02d}'/f'block-{block:02d}'
                assert json.loads((directory/'execution.json').read_text())==execution
                records=json.loads((directory/'records.json').read_text()) if (directory/'records.json').exists() else []
                expected={(phase,r) for phase,count in [('warmup',p['warmups']),('measured',p['measured'])] for r in range(count)}
                if execution['status']=='completed':assert {(r['phase'],r['repetition']) for r in records}==expected and len(records)==len(expected)
                for row in records:
                    assert (row['participant'],row['instance'],row['block'])==key
                    state=np.load(root/row['output']['path'],allow_pickle=False)
                    assert state.shape==(1<<n,) and state.dtype==np.complex128
                    error=float(np.max(np.abs(state-oracle)));norm=float(abs(np.vdot(state,state).real-1))
                    decision='accepted' if np.isfinite(state).all() and error<=p['absolute_tolerance'] and norm<=p['norm_tolerance'] else 'rejected'
                    assert error==row['max_abs_error'] and norm==row['norm_error'] and decision==row['semantic_status']
                    assert row['status']=='completed' and all(v is None or isinstance(v,(int,float)) and np.isfinite(v) and v>=0 for v in row['measurements'].values())
                    statuses[decision]=statuses.get(decision,0)+1;rows.append(row)
    return dict(schema_version=1,manifest_sha256=sha(root/'MANIFEST.json'),context=c,
        files_verified=len(actual),blocks_verified=len(seen),records_verified=len(rows),record_statuses=statuses,
        publication_eligible=False,replay_scope='All stored complete complex128 states re-evaluated against deterministic independent NumPy oracle; no participant SDK rerun or resource qualification')

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--directory',type=Path,required=True);p.add_argument('--summary',type=Path,required=True);a=p.parse_args()
    assert not a.summary.exists(), 'Never overwrite receipt'
    v=verify(a.directory);write(a.summary,v);print(json.dumps(v,indent=2))
