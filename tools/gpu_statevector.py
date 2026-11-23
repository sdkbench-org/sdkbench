#!/usr/bin/env python3
"""Single-GPU statevector engineering study; no CPU fallback or global ranking."""
from __future__ import annotations
import argparse
import gc
import hashlib
import importlib.metadata
import json
import math
import os
from pathlib import Path
import platform
import subprocess
import sys
import time
import traceback

PARTICIPANTS = ('custatevec', 'flagquantum')

def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, sort_keys=True, indent=2, allow_nan=False)+'\n')

def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda:stream.read(1048576), b''):h.update(chunk)
    return h.hexdigest()

def operations(n, layers, seed):
    """Fixed asymmetric RY/RZ rotations and alternating directed CX chains."""
    out=[]
    for layer in range(layers):
        for q in range(n):
            out.extend([['ry',[q],.11+.013*((seed+layer*n+q)%37)],
                        ['rz',[q],-.23+.017*((seed+3*layer*n+q)%29)]])
        edges=range(n-1) if layer%2==0 else reversed(range(n-1))
        out.extend(['cx',[q,q+1] if layer%2==0 else [q+1,q],None] for q in edges)
    return out

def reference(n, ops):
    """Independent NumPy oracle, qubit zero is the most significant bit."""
    import numpy as np
    state=np.zeros(1<<n,dtype=np.complex128);state[0]=1
    for name,wires,angle in ops:
        if name=='cx':
            control,target=wires
            index=np.arange(len(state),dtype=np.uint64)
            low=index[(((index>>(n-1-control))&1)==1)&(((index>>(n-1-target))&1)==0)]
            high=low|(1<<(n-1-target))
            state[low],state[high]=state[high].copy(),state[low].copy()
        else:
            a=angle/2
            matrix=np.array([[math.cos(a),-math.sin(a)],[math.sin(a),math.cos(a)]]) if name=='ry' else np.diag([np.exp(-1j*a),np.exp(1j*a)])
            tensor=state.reshape([2]*n)
            state=np.moveaxis(np.tensordot(matrix,tensor,axes=(1,wires[0])),0,wires[0]).reshape(-1)
    return state

class CuStateVec:
    def __init__(self,n,ops):
        import cupy as cp
        from cuquantum.bindings import custatevec as cv
        self.cp,self.cv,self.n=cp,cv,n
        self.handle=cv.create();self.items=[];sizes=[]
        cv.set_stream(self.handle,cp.cuda.Stream.null.ptr)
        for name,wires,angle in ops:
            a=angle/2 if angle is not None else 0
            m=[[0,1],[1,0]] if name=='cx' else ([[math.cos(a),-math.sin(a)],[math.sin(a),math.cos(a)]] if name=='ry' else [[complex(math.cos(a),-math.sin(a)),0],[0,complex(math.cos(a),math.sin(a))]])
            matrix=cp.asarray(m,dtype=cp.complex128)
            controls=[n-1-wires[0]] if name=='cx' else []
            target=n-1-wires[-1]
            self.items.append((matrix,target,controls))
            sizes.append(cv.apply_matrix_get_workspace_size(self.handle,5,n,matrix.data.ptr,5,cv.MatrixLayout.ROW,0,1,len(controls),cv.ComputeType.COMPUTE_64F))
        self.workspace_bytes=max(sizes,default=0)
        self.workspace=cp.cuda.alloc(self.workspace_bytes) if self.workspace_bytes else None
    def run(self):
        cp,cv=self.cp,self.cv
        state=cp.zeros(1<<self.n,dtype=cp.complex128);state[0]=1
        for m,target,controls in self.items:
            cv.apply_matrix(self.handle,state.data.ptr,5,self.n,m.data.ptr,5,cv.MatrixLayout.ROW,0,[target],1,controls,[1]*len(controls),len(controls),cv.ComputeType.COMPUTE_64F,self.workspace.ptr if self.workspace else 0,self.workspace_bytes)
        return state
    def close(self):
        self.cv.destroy(self.handle)

def worker(args):
    import numpy as np
    import torch
    import cupy as cp
    profile=json.loads(args.profile.read_text());n=args.qubits
    assert torch.cuda.is_available() and torch.cuda.device_count()==1, 'One real CUDA device required'
    assert torch.__version__==profile['torch_runtime_version'] and torch.version.cuda==profile['cuda_runtime_version'], 'Unregistered CUDA/Torch build'
    torch.set_num_threads(1);torch.set_num_interop_threads(1)
    if args.participant=='flagquantum':
        import flagquantum as fq
    expected=np.load(args.output/'references'/f'{n}.npy',mmap_mode='r')
    ops=operations(n,profile['layers'],profile['seed'])
    dest=args.output/args.participant/f'SV-{n:02d}'/f'block-{args.block:02d}'
    dest.mkdir(parents=True,exist_ok=False)
    versions={d.metadata['Name']:d.version for d in importlib.metadata.distributions()}
    for name,version in profile['versions'].items():
        actual=importlib.metadata.version(name)
        assert actual==version, f'Unregistered version: {name} {actual}, expected {version}'
    write(dest/'environment.json',dict(python=sys.version,host=platform.node(),pid=os.getpid(),
        packages=versions,device=torch.cuda.get_device_name(0),cuda=torch.version.cuda,
        visible_device=os.environ.get('CUDA_VISIBLE_DEVICES'),affinity=sorted(os.sched_getaffinity(0))))
    records=[]
    for phase,count in [('warmup',profile['warmups']),('measured',profile['measured'])]:
        for repetition in range(count):
            gc.collect();cp.get_default_memory_pool().free_all_blocks();torch.cuda.empty_cache()
            torch.cuda.reset_peak_memory_stats()
            # Library imports and reference evaluation are outside the request.
            torch.cuda.synchronize();cp.cuda.Stream.null.synchronize()
            t0=time.perf_counter()
            if args.participant=='custatevec':
                executor=CuStateVec(n,ops)
                run=executor.run
            else:
                circuit=fq.Circuit(n,device='cuda',dtype=torch.complex128)
                for name,wires,angle in ops:
                    if name=='cx':circuit.cx(*wires)
                    else:getattr(circuit,name)(wires[0],torch.tensor(angle,dtype=torch.float64,device='cuda'))
                run=lambda:circuit.state(refresh=True)
                executor=None
            torch.cuda.synchronize();cp.cuda.Stream.null.synchronize();t1=time.perf_counter()
            state=run()
            torch.cuda.synchronize();cp.cuda.Stream.null.synchronize();t2=time.perf_counter()
            if args.participant=='custatevec':
                assert state.dtype==cp.complex128 and state.device.id==0
                host=cp.asnumpy(state).reshape(-1)
            else:
                assert state.is_cuda and state.dtype==torch.complex128
                host=state.detach().cpu().numpy().reshape(-1)
            torch.cuda.synchronize();cp.cuda.Stream.null.synchronize();t3=time.perf_counter()
            workspace=executor.workspace_bytes if executor else None
            if executor:executor.close()
            t4=time.perf_counter()
            error=float(np.max(np.abs(host-expected)))
            norm_error=float(abs(np.vdot(host,host).real-1))
            finite=bool(np.isfinite(host).all())
            output=dest/f'{phase}-{repetition}.npy';np.save(output,host,allow_pickle=False)
            records.append(dict(participant=args.participant,instance=f'SV-{n:02d}',block=args.block,
                phase=phase,repetition=repetition,status='completed',
                semantic_status='accepted' if finite and error<=profile['absolute_tolerance'] and norm_error<=profile['norm_tolerance'] else 'rejected',
                max_abs_error=error,norm_error=norm_error,
                measurements=dict(setup_seconds=t1-t0,evolution_seconds=t2-t1,d2h_seconds=t3-t2,
                    request_wall_seconds=t4-t0,cleanup_seconds=t4-t3,h2d_seconds=None),
                h2d_status='not_applicable: zero state initialized on device; gate-matrix upload belongs to setup',
                resource_observations=dict(torch_peak_allocated_bytes=torch.cuda.max_memory_allocated(),
                    torch_peak_reserved_bytes=torch.cuda.max_memory_reserved(),cupy_pool_total_bytes=cp.get_default_memory_pool().total_bytes(),
                    custatevec_workspace_bytes=workspace),
                native_calls=dict(custatevec_apply_matrix=len(ops) if executor else 0,
                    flagquantum_state=0 if executor else 1,output_cuda_verified=True,
                    custatevec_library_version=executor.cv.get_version() if executor else None),
                output=dict(path=output.relative_to(args.output).as_posix(),sha256=sha(output),bytes=output.stat().st_size)))
            write(dest/'records.json',records)
            del state,host,run
            if executor:del executor
            if args.participant=='flagquantum':del circuit
    return 0

def campaign(args):
    import numpy as np
    profile=json.loads(args.profile.read_text())
    assert args.source_commit and len(args.source_commit)==40 and args.gpu_uuid and args.container_image, 'Exact execution provenance required'
    assert not args.output.exists(), 'Never overwrite a run'
    args.output.mkdir(parents=True)
    write(args.output/'profile.json',profile)
    write(args.output/'context.json',dict(schema_version=1,suite='gpu-statevector-engineering',
        publication_eligible=False,source_commit=args.source_commit,profile_sha256=sha(args.profile),
        host=platform.node(),python=sys.version,started_unix_ns=time.time_ns(),
        physical_gpu_uuid=args.gpu_uuid,container_image=args.container_image,runner_sha256=sha(Path(__file__))))
    for n in profile['qubits']:
        (args.output/'references').mkdir(exist_ok=True)
        np.save(args.output/'references'/f'{n}.npy',reference(n,operations(n,profile['layers'],profile['seed'])),allow_pickle=False)
    outcomes=[]
    for n in profile['qubits']:
        for block in range(profile['blocks']):
            order=PARTICIPANTS if block%2==0 else PARTICIPANTS[::-1]
            for participant in order:
                prefix=args.output/participant/f'SV-{n:02d}'/f'block-{block:02d}'
                cmd=[sys.executable,__file__,'worker','--profile',str(args.profile),'--output',str(args.output),
                     '--participant',participant,'--qubits',str(n),'--block',str(block)]
                start=time.time_ns()
                try:
                    result=subprocess.run(cmd,capture_output=True,text=True,timeout=profile['block_timeout_seconds'])
                    outcome=dict(participant=participant,instance=f'SV-{n:02d}',block=block,
                        status='completed' if result.returncode==0 else 'error',returncode=result.returncode,
                        stdout=result.stdout,stderr=result.stderr,started_unix_ns=start,ended_unix_ns=time.time_ns())
                except subprocess.TimeoutExpired as exc:
                    outcome=dict(participant=participant,instance=f'SV-{n:02d}',block=block,status='timeout',
                        stdout=str(exc.stdout),stderr=str(exc.stderr),started_unix_ns=start,ended_unix_ns=time.time_ns())
                prefix.mkdir(parents=True,exist_ok=True);write(prefix/'execution.json',outcome);outcomes.append(outcome)
                path=prefix/'records.json'
                records=json.loads(path.read_text()) if path.exists() else []
                outcome['semantic_status']='accepted' if outcome['status']=='completed' and len(records)==profile['warmups']+profile['measured'] and all(r['semantic_status']=='accepted' for r in records) else 'not-accepted'
                write(prefix/'execution.json',outcome)
                write(args.output/'execution-summary.json',outcomes)
                print(participant,n,block,outcome['status'],flush=True)
    write(args.output/'MANIFEST.json',dict(schema_version=1,files={p.relative_to(args.output).as_posix():dict(sha256=sha(p),bytes=p.stat().st_size)
        for p in sorted(args.output.rglob('*')) if p.is_file()}))
    return int(any(o['status']!='completed' or o['semantic_status']!='accepted' for o in outcomes))

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('mode',choices=['campaign','worker'])
    p.add_argument('--profile',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    p.add_argument('--participant',choices=PARTICIPANTS);p.add_argument('--qubits',type=int);p.add_argument('--block',type=int)
    p.add_argument('--source-commit');p.add_argument('--gpu-uuid');p.add_argument('--container-image')
    a=p.parse_args()
    return campaign(a) if a.mode=='campaign' else worker(a)
if __name__=='__main__':raise SystemExit(main())
