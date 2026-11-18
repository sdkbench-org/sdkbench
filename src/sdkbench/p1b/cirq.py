"""Cirq-core exact evolution and native RouteCQC/CZ target synthesis."""
import numpy as np
from ..p1a.cirq import CirqAdapter
from ..p1a.common import real_values,UnsupportedCapability
from .common import P1bBase,matrix_payload
from ..p0.models import require


class CirqP1b(P1bBase,CirqAdapter):
    def gradient(self,fixture):
        raise UnsupportedCapability('Registered cirq-core 1.7.0 has no general Jacobian API. No benchmark-side derivative is substituted. TensorFlow Quantum 0.7.6 pins cirq-core 1.5.0 and is a different stack.')

    def dynamics(self,fixture):
        cirq=self.cirq;n=fixture['n_qubits'];qubits=cirq.LineQubit.range(n);ops=[]
        for q in range(n):
            if fixture['initial_basis_index']&(1<<q):ops.append(cirq.X(qubits[q]))
        for op in fixture['operations']:
            selected=[qubits[q] for q in op['qubits']]
            gate=cirq.rx(op['angle']) if op['name']=='rx' else cirq.ZZPowGate(exponent=op['angle']/np.pi,global_shift=-.5)
            ops.append(gate.on(*selected))
        self.audit['native_program_builds']=1;self.audit['native_executions']=1
        return {'moments':real_values(self.expectations(cirq.Circuit(ops),fixture['pauli_words'],n),len(fixture['pauli_words']))}

    def route(self,fixture,seed):
        import networkx as nx
        cirq=self.cirq;n=fixture['n_qubits'];qubits=cirq.LineQubit.range(n)
        graph=nx.Graph();graph.add_nodes_from(qubits);graph.add_edges_from((qubits[a],qubits[b]) for a,b in fixture['target_edges'])
        circuit,_=self.build(fixture,'observable');self.audit['native_program_builds']=1
        routed,initial,final=cirq.RouteCQC(graph).route_circuit(circuit,initial_mapper=cirq.HardCodedInitialMapper({q:q for q in qubits}))
        compiled=cirq.optimize_for_target_gateset(routed,gateset=cirq.CZTargetGateset(atol=1e-12,allow_partial_czs=False),ignore_failures=False)
        operations=[]
        for op in compiled.all_operations():
            selected=[qubits.index(q) for q in op.qubits]
            if not selected:continue  # Global phase only, permitted by the frozen unitary contract.
            if len(selected)==1:operations.append({'name':'unitary','qubits':selected,'matrix':matrix_payload(cirq.unitary(op))})
            else:
                require(isinstance(op.gate,cirq.CZPowGate) and abs(float(op.gate.exponent)%2-1)<1e-12,'Compiler emitted a non-full-CZ interaction')
                operations.append({'name':'cz','qubits':selected})
        self.audit['native_compilations']=1;self.audit['compiler_seed_supported']=0
        # RouteCQC is deterministic and exposes no seed argument. Do not claim it used one.
        return {'operations':operations,'final_layout':[qubits.index(final[initial[q]]) for q in qubits]}
