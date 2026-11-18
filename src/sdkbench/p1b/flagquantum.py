"""FlagQuantum native autograd Jacobian, fixed digital evolution and compiler passes."""
from functools import reduce
from operator import matmul
from ..p1a.flagquantum import FlagQuantumAdapter
from ..p1a.common import real_values
from ..p0.models import digest,require
from .common import P1bBase


class FlagQuantumP1b(P1bBase,FlagQuantumAdapter):
    def gradient(self,fixture):
        fq=self.fq;torch=self.torch
        circuit,parameters=self.build(fixture,'observable');self.audit['native_program_builds']=1
        observables=[reduce(matmul,[getattr(fq,axis)(q) for q,axis in enumerate(word) if axis!='I'],fq.I()) for word in fixture['pauli_words']]
        options=fq.ExecutionOptions(mode='statevector',backend='pytorch',device='cpu',precision='complex128',
                                    require_gradients=True,allow_approximate=False,allow_backend_fallback=False)
        def program(values):
            bound=circuit.bind_parameters({p.name:values[i] for i,p in enumerate(parameters)})
            result=fq.run(bound,outputs=[fq.expectation(o) for o in observables],options=options)
            self.audit['native_executions']+=1
            return torch.stack([v.reshape(()) for v in result.expectations])
        theta=torch.tensor(fixture['parameters'],dtype=torch.float64,requires_grad=True)
        with torch.enable_grad():
            self.audit['native_primal_calls']=1
            outputs=program(theta)
            self.audit['native_derivative_calls']=1
            jacobian=fq.jacobian(program,theta)
        return {'outputs':outputs.detach().cpu().tolist(),'jacobian':jacobian.detach().cpu().tolist(),
                'derivative':{'method':'flagquantum.fq.jacobian/autograd; forward-program invocation count',
                              'quantum_evaluations':self.audit['native_executions'],
                              'components':['flagquantum==0.3.1','torch=='+torch.__version__]}}

    def dynamics(self,fixture):
        fq=self.fq;torch=self.torch
        circuit=fq.Circuit(fixture['n_qubits'],device='cpu',dtype=torch.complex128)
        for q in range(fixture['n_qubits']):
            if fixture['initial_basis_index']&(1<<q):circuit.gate('x',[q])
        for op in fixture['operations']:
            circuit.gate(op['name'],op['qubits'],params={'theta':torch.tensor(op['angle'],dtype=torch.float64)})
        self.audit['native_program_builds']=1;self.audit['native_executions']=1
        return {'moments':real_values(self.expectations(circuit,fixture['pauli_words'],fixture['n_qubits']),len(fixture['pauli_words']))}

    def route(self,fixture,seed):
        from flagquantum.compiler import compile,CouplingMap,final_layout
        from flagquantum.compiler.native_gate_legalization import legalize_native_gates
        from flagquantum.core.target_capabilities import (CapabilityScope,TargetCapabilitySnapshot,TargetIdentity,CapabilityFact,
                  SupportStatus,FactExposure,FactSource,EvidenceReference,EvidenceLevel)
        circuit,_=self.build(fixture,'observable');self.audit['native_program_builds']=1
        scope=CapabilityScope(dtype='complex128');basis=('h','x','y','z','s','sdg','rx','ry','rz','cz')
        target_definition={'basis':basis,'edges':fixture['target_edges'],'n_qubits':fixture['n_qubits'],'meaning':'declared abstract benchmark target, not hardware evidence'}
        snapshot=TargetCapabilitySnapshot(target_identity=TargetIdentity('sdkbench-abstract-full-cz','abstract','sdkbench','0.4.0','0.1-candidate-1','offline'),
                    scope=scope,captured_at='2026-11-18T00:00:00Z',valid_until='2099-01-01T00:00:00Z',
                    facts=(CapabilityFact('gates.native',basis,SupportStatus.VERIFIED,FactExposure.DECLARED,FactSource('static','frozen-target-definition')),),
                    evidence_refs=(EvidenceReference('frozen-target-definition',digest(target_definition),EvidenceLevel.BASIC,scope),))
        routed=compile(circuit,coupling_map=CouplingMap(fixture['n_qubits'],fixture['target_edges']),config=circuit.runtime_config)
        compiled=legalize_native_gates(routed,snapshot=snapshot,max_added_operations=20000).program
        operations=[]
        for op in compiled.instructions:
            item={'name':op.name,'qubits':list(op.wires)}
            require(op.matrix is None and op.name in basis,'Native compiler emitted an unnormalized/non-target instruction')
            if op.name in ('rx','ry','rz'):item['angle']=float(op.params['theta'])
            operations.append(item)
        layout=final_layout(routed).logical_to_physical
        self.audit['native_compilations']=1;self.audit['compiler_seed_supported']=0
        return {'operations':operations,'final_layout':list(layout)}
