"""Reproduce a local reversed-wire block cost gap, with an independent full operator check.

Use --native-module flagquantum.compiler.lowering.native_gate_legalization for
upstream source checkouts that moved the native legalizer. The default is the
published 0.3.1 module path. No implicit API or SDK fallback is performed.
"""
import argparse
from collections import Counter
import importlib
import inspect
import json
import time
import numpy as np
import torch
import flagquantum as fq
from flagquantum.compiler import compile,CouplingMap,final_layout,optimize
from sdkbench.diagnostics.routing import BASIS,target_snapshot
from sdkbench.p0.semantics import propagate,equivalent
from sdkbench.p1b.common import compile_deadline


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--native-module',default='flagquantum.compiler.native_gate_legalization')
    parser.add_argument('--post-basis-opt',action='store_true')
    args=parser.parse_args();legalize=importlib.import_module(args.native_module).legalize_native_gates
    torch.set_num_threads(1);fixture={'n_qubits':2,'target_edges':[[0,1]]};snapshot=target_snapshot(fixture,BASIS)
    circuits={'native_swap_then_reversed_cx':[('swap',[0,1]),('cx',[1,0])],
              'equivalent_two_cx':[('cx',[1,0]),('cx',[0,1])]}
    reference=[{'name':'cx','qubits':q} for q in ([0,1],[1,0],[0,1],[1,0])]
    target=propagate(2,reference,np.eye(4,dtype=np.complex128));outcomes=[]
    for name,operations in circuits.items():
        with compile_deadline(120):
            start=time.perf_counter();circuit=fq.Circuit(2,device='cpu',dtype=torch.complex128)
            for opcode,wires in operations:circuit.gate(opcode,wires)
            routed=compile(circuit,coupling_map=CouplingMap(2,fixture['target_edges']),config=circuit.runtime_config)
            native=legalize(routed,snapshot=snapshot,max_added_operations=20000).program
            if args.post_basis_opt:native=legalize(optimize(native,optimization_level=2),snapshot=snapshot,max_added_operations=20000).program
            assert list(final_layout(routed).logical_to_physical)==[0,1]
            output=[]
            for op in native.instructions:
                assert op.matrix is None and op.name in BASIS
                item={'name':op.name,'qubits':list(op.wires)}
                if op.name in ('rx','ry','rz'):item['angle']=float(op.params['theta'])
                output.append(item)
            elapsed=time.perf_counter()-start
        actual=propagate(2,output,np.eye(4,dtype=np.complex128),target_edges={frozenset([0,1])})
        error=equivalent(actual,target,1e-8,1e-10)
        outcomes.append({'input':name,'full_cz_count':sum(op['name']=='cz' for op in output),
                         'pre_native_opcodes':dict(Counter(op.name for op in routed.instructions)),
                         'output_operations':output,'full_operator_max_error':error,'final_layout':[0,1],'compile_wall_seconds':elapsed})
    print(json.dumps({'scope':'Local correctness/cost reproducer; no cgroup or speed qualification.',
                      'sdk_version':fq.__version__,'sdk_import_file':inspect.getfile(fq),
                      'native_module':args.native_module,'post_basis_optimization':args.post_basis_opt,
                      'outcomes':outcomes},indent=2))
    return 0


if __name__=='__main__':raise SystemExit(main())
