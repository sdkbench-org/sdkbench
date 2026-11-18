"""Observe native compiler stages and vary declared configuration, without SDK patches."""
from collections import Counter
from contextlib import contextmanager
from dataclasses import asdict
from pathlib import Path
import sys
import numpy as np
from ..p0.models import digest, require
from ..p1b.common import compile_deadline, matrix_payload

BASIS = ('h','x','y','z','s','sdg','rx','ry','rz','cz')


def variants():
    rows = []
    for strategy in ('restore_after_each_gate','persistent_layout','auto','sabre'):
        for drop in (False, True):
            for post in (False, True):
                name = f'fq-{strategy}-{"free" if drop else "restored"}-{"post" if post else "plain"}'
                if strategy == 'restore_after_each_gate' and not drop and not post:name = 'fq-default'
                rows.append(dict(id=name, sdk='flagquantum', strategy=strategy, drop_restore=drop, post_basis=post,
                                 level=2, basis=list(BASIS), seeded=False))
    for level in (0,1):
        rows.append(dict(rows[0], id=f'fq-default-level{level}', level=level))
    rows.append(dict(rows[0], id='fq-default-rotation-basis', basis=['rx','rz','cz']))
    for method in (None,'sabre','basic','lookahead'):
        rows.append(dict(id='qiskit-'+(method or 'default'), sdk='qiskit', method=method, level=2, seeded=True))
    rows.append(dict(id='qiskit-default-level0', sdk='qiskit', method=None, level=0, seeded=True))
    rows.append(dict(id='cirq-default', sdk='cirq', seeded=False))
    return rows


def micro_fixtures(base):
    from copy import deepcopy
    prefix = [{'name':'ry','qubits':[q],'angle':.071*(q+1)} for q in range(6)]
    cx = lambda a,b: {'name':'cx','qubits':[a,b]}
    circuits = {
        'MICRO-LOCAL-CX': [cx(0,1)],
        'MICRO-LOCAL-CANCEL': [cx(0,1),cx(0,1)],
        'MICRO-LOCAL-SWAP': [cx(0,1),cx(1,0),cx(0,1)],
        'MICRO-SWAP-CX-SAME': [{'name':'swap','qubits':[0,1]},cx(0,1)],
        'MICRO-SWAP-CX-REVERSED': [{'name':'swap','qubits':[0,1]},cx(1,0)],
        'MICRO-REMOTE-REUSE': [cx(0,5),{'name':'ry','qubits':[0],'angle':.37},cx(0,5)],
    }
    result={}
    for name,operations in circuits.items():
        # Reference-only definition of SWAP; the participant receives its native SWAP.
        reference=[]
        for op in prefix+operations:
            if op['name']=='swap':
                a,b=op['qubits'];reference.extend([cx(a,b),cx(b,a),cx(a,b)])
            else:reference.append(op)
        result[name]=deepcopy(base) | {'operations':reference,'native_input_operations':prefix+operations}
    return result


def ir_summary(ir):
    two = [op for op in ir.instructions if len(op.wires)==2]
    return {'instructions':len(ir.instructions), 'opcodes':dict(Counter(op.name for op in ir.instructions)),
            'two_qubit_instructions':len(two),
            'routing_swap_phases':dict(Counter(op.metadata.get('routing_phase','unmarked') for op in two if op.name=='swap')),
            'two_qubit_sequence':[{'name':op.name,'qubits':list(op.wires),
                                   'phase':op.metadata.get('routing_phase'),
                                   'source_index':op.metadata.get('source_instruction_index')} for op in two]}


@contextmanager
def observe_flag_pipeline(trace):
    """Read-only observation of pinned Python internals; all execution uses public APIs.

    Instrumented wall times are diagnostic only. No SDK function/source is patched.
    """
    previous = sys.getprofile();require(previous is None, 'Refuse a conflicting profiler')
    def observe(frame, event, result):
        if event != 'return' or not frame.f_code.co_filename.endswith(('/compiler/pipeline.py','/compiler/routing.py')):return
        if frame.f_code.co_name in ('_optimize_to_fixed_point','route_to_topology') and hasattr(result,'instructions'):
            trace.append({'native_function':frame.f_code.co_name, **ir_summary(result)})
    sys.setprofile(observe)
    try:yield
    finally:sys.setprofile(previous)


def target_snapshot(fixture, basis):
    from flagquantum.core.target_capabilities import (CapabilityScope,TargetCapabilitySnapshot,TargetIdentity,CapabilityFact,
                  SupportStatus,FactExposure,FactSource,EvidenceReference,EvidenceLevel)
    scope=CapabilityScope(dtype='complex128')
    definition={'basis':tuple(basis),'edges':fixture['target_edges'],'n_qubits':fixture['n_qubits'],
                'meaning':'declared abstract benchmark target, not hardware evidence'}
    return TargetCapabilitySnapshot(target_identity=TargetIdentity('sdkbench-abstract-full-cz','abstract','sdkbench','0.4.0','0.1-candidate-1','offline'),
                scope=scope,captured_at='2026-11-18T00:00:00Z',valid_until='2099-01-01T00:00:00Z',
                facts=(CapabilityFact('gates.native',tuple(basis),SupportStatus.VERIFIED,FactExposure.DECLARED,FactSource('static','frozen-target-definition')),),
                evidence_refs=(EvidenceReference('frozen-target-definition',digest(definition),EvidenceLevel.BASIC,scope),))


def flagquantum_compile(adapter, fixture, config, seed):
    from flagquantum.compiler import compile, CouplingMap, final_layout, remove_layout_restore, optimize
    from flagquantum.compiler.native_gate_legalization import legalize_native_gates
    circuit,_=adapter.build(fixture,'observable');trace=[{'stage':'input',**ir_summary(circuit.to_ir())}]
    adapter.diagnostic_trace={'stages':trace}
    with observe_flag_pipeline(trace):
        routed=compile(circuit,coupling_map=CouplingMap(fixture['n_qubits'],fixture['target_edges']),
                       routing_strategy=config['strategy'],optimization_level=config['level'],config=circuit.runtime_config)
    native_metadata = {'routing':routed.metadata.get('routing'), 'selection':routed.metadata.get('routing_strategy_selection'),
                       'optimization':routed.metadata.get('optimization')}
    adapter.diagnostic_trace['native_metadata']=native_metadata
    require(list(routed.metadata['routing']['initial_logical_to_physical']) == list(range(fixture['n_qubits'])), 'Initial layout changed')
    trace.append({'stage':'compile_return',**ir_summary(routed)})
    if config['drop_restore']:routed=remove_layout_restore(routed)
    trace.append({'stage':'layout_policy',**ir_summary(routed), 'routing':routed.metadata.get('routing')})
    layout=list(final_layout(routed).logical_to_physical)
    snapshot=target_snapshot(fixture,config['basis'])
    result=legalize_native_gates(routed,snapshot=snapshot,max_added_operations=20000)
    trace.append({'stage':'first_native_basis',**ir_summary(result.program),
                  'decompositions':[asdict(r) for r in result.decompositions]})
    compiled=result.program
    if config['post_basis']:
        compiled=optimize(compiled,optimization_level=2)
        trace.append({'stage':'post_basis_optimized',**ir_summary(compiled)})
        result=legalize_native_gates(compiled,snapshot=snapshot,max_added_operations=20000)
        compiled=result.program
        trace.append({'stage':'second_native_basis',**ir_summary(compiled),
                      'decompositions':[asdict(r) for r in result.decompositions]})
    operations=[]
    for op in compiled.instructions:
        require(op.matrix is None and op.name in config['basis'],'Non-target instruction')
        item={'name':op.name,'qubits':list(op.wires)}
        if op.name in ('rx','ry','rz'):item['angle']=float(op.params['theta'])
        operations.append(item)
    return {'operations':operations,'final_layout':layout}, {'stages':trace,'native_metadata':native_metadata}


def qiskit_compile(adapter, fixture, config, seed):
    from qiskit.quantum_info import Operator
    circuit,_=adapter.build(fixture,'observable');trace=[]
    adapter.diagnostic_trace={'passes':trace}
    def observe(**kwargs):
        dag=kwargs['dag'];trace.append({'pass':type(kwargs['pass_']).__name__,'count':kwargs['count'],
                                        'opcodes':dict(dag.count_ops())})
    edges=[pair for a,b in fixture['target_edges'] for pair in ([a,b],[b,a])]
    compiled=adapter.qiskit.transpile(circuit,basis_gates=['cz','u'],coupling_map=edges,
                 initial_layout=list(range(fixture['n_qubits'])),optimization_level=config['level'],
                 routing_method=config['method'],approximation_degree=1.,seed_transpiler=seed,
                 qubits_initially_zero=False,num_processes=1,callback=observe)
    require(compiled.num_qubits==fixture['n_qubits'],'Compiler introduced ancillas')
    initial=[compiled.layout.initial_layout[q] for q in circuit.qubits]
    require(initial==list(range(fixture['n_qubits'])),'Initial layout changed')
    operations=[]
    for item in compiled.data:
        qubits=[compiled.find_bit(q).index for q in item.qubits]
        if item.operation.name=='cz':operations.append({'name':'cz','qubits':qubits})
        else:
            require(len(qubits)==1,'Non-target interaction')
            operations.append({'name':'unitary','qubits':qubits,'matrix':matrix_payload(Operator(item.operation).data)})
    return {'operations':operations,'final_layout':list(compiled.layout.final_index_layout(filter_ancillas=True))}, {'passes':trace,'initial_layout':initial}


def cirq_compile(adapter, fixture, config, seed):
    import networkx as nx
    cirq=adapter.cirq;n=fixture['n_qubits'];qubits=cirq.LineQubit.range(n)
    graph=nx.Graph();graph.add_nodes_from(qubits);graph.add_edges_from((qubits[a],qubits[b]) for a,b in fixture['target_edges'])
    if any(op['name']=='swap' for op in fixture['operations']):
        ops=[]
        for op in fixture['operations']:
            selected=[qubits[q] for q in op['qubits']]
            if op['name'] in ('ry','rz'):gate=getattr(cirq,op['name'])(op['angle'])
            else:gate={'swap':cirq.SWAP,'cx':cirq.CNOT}[op['name']]
            ops.append(gate.on(*selected))
        circuit=cirq.Circuit(ops)
    else:circuit,_=adapter.build(fixture,'observable')
    adapter.diagnostic_trace={}
    routed,initial,final=cirq.RouteCQC(graph).route_circuit(circuit,initial_mapper=cirq.HardCodedInitialMapper({q:q for q in qubits}))
    require(all(initial[q]==q for q in qubits),'Initial layout changed')
    compiled=cirq.optimize_for_target_gateset(routed,gateset=cirq.CZTargetGateset(atol=1e-12,allow_partial_czs=False),ignore_failures=False)
    operations=[]
    for op in compiled.all_operations():
        selected=[qubits.index(q) for q in op.qubits]
        if not selected:continue
        if len(selected)==1:operations.append({'name':'unitary','qubits':selected,'matrix':matrix_payload(cirq.unitary(op))})
        else:
            require(isinstance(op.gate,cirq.CZPowGate) and abs(float(op.gate.exponent)%2-1)<1e-12,'Non-full-CZ interaction')
            operations.append({'name':'cz','qubits':selected})
    def summary(c):return dict(Counter(type(op.gate).__name__ for op in c.all_operations()))
    return {'operations':operations,'final_layout':[qubits.index(final[initial[q]]) for q in qubits]}, {'input':summary(circuit),'routed':summary(routed),'target':summary(compiled),'initial_layout':list(range(n))}


def compile_variant(adapter, fixture, config, seed):
    import time
    with compile_deadline(120):
        started=time.perf_counter()
        fixture=fixture | {'operations':fixture.get('native_input_operations',fixture['operations'])}
        payload,trace={'flagquantum':flagquantum_compile,'qiskit':qiskit_compile,'cirq':cirq_compile}[config['sdk']](adapter,fixture,config,seed)
        payload['compile_wall_seconds']=time.perf_counter()-started
    return payload,trace
