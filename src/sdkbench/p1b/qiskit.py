"""Qiskit exact dynamics/routing and explicitly attributed Qiskit Algorithms gradients."""
import numpy as np
from ..p1a.qiskit import QiskitAdapter
from ..p1a.common import real_values
from .common import P1bBase,matrix_payload
from ..p0.models import require


class QiskitP1b(P1bBase,QiskitAdapter):
    def prepare(self, kind):
        if kind == 'gradient':
            from qiskit.primitives import StatevectorEstimator
            from qiskit_algorithms.gradients import ReverseEstimatorGradient
            from importlib.metadata import version
            require(version('qiskit-algorithms') == '0.4.0', 'Pinned gradient component mismatch')
            self.estimator_class = StatevectorEstimator
            self.gradient_class = ReverseEstimatorGradient

    def gradient(self, fixture):
        if not hasattr(self, 'gradient_class'):self.prepare('gradient')
        circuit, parameters = self.build(fixture, 'observable');self.audit['native_program_builds'] = 1
        observables = [self.Pauli(word[::-1]) for word in fixture['pauli_words']]
        self.audit['native_primal_calls'] = 1
        values = self.estimator_class(default_precision=0.).run([(circuit, observables, fixture['parameters'])]).result()[0].data.evs
        self.audit['native_derivative_calls'] = 1
        result = self.gradient_class().run([circuit] * len(observables), observables,
                    [fixture['parameters']] * len(observables), parameters=[list(parameters)] * len(observables)).result()
        self.audit['primal_expectation_requests'] = len(observables)
        self.audit['derivative_expectation_requests'] = len(observables)
        self.audit['native_executions'] = 2 * len(observables)
        return {'outputs': real_values(values, len(observables)), 'jacobian': np.asarray(result.gradients, dtype=np.float64).tolist(),
                'derivative': {'method': 'qiskit-algorithms ReverseEstimatorGradient; primal plus derivative expectation requests; internal state evolutions not exposed',
                               'quantum_evaluations': self.audit['native_executions'],
                               'components': ['qiskit==2.6.2', 'qiskit-algorithms==0.4.0']}}

    def dynamics(self,fixture):
        circuit=self.qiskit.QuantumCircuit(fixture['n_qubits'])
        for q in range(fixture['n_qubits']):
            if fixture['initial_basis_index']&(1<<q):circuit.x(q)
        for op in fixture['operations']:getattr(circuit,op['name'])(op['angle'],*op['qubits'])
        self.audit['native_program_builds']=1;self.audit['native_executions']=1
        return {'moments':real_values(self.expectations(circuit,fixture['pauli_words'],fixture['n_qubits']),len(fixture['pauli_words']))}

    def route(self,fixture,seed):
        from qiskit.quantum_info import Operator
        circuit,_=self.build(fixture,'observable');self.audit['native_program_builds']=1
        n=fixture['n_qubits'];edges=[pair for a,b in fixture['target_edges'] for pair in ([a,b],[b,a])]
        compiled=self.qiskit.transpile(circuit,basis_gates=['cz','u'],coupling_map=edges,initial_layout=list(range(n)),
                                      optimization_level=2,approximation_degree=1.,seed_transpiler=seed,
                                      qubits_initially_zero=False,num_processes=1)
        require(compiled.num_qubits==n,'Compiler introduced ancillas')
        operations=[]
        for item in compiled.data:
            qubits=[compiled.find_bit(q).index for q in item.qubits]
            if item.operation.name=='cz':operations.append({'name':'cz','qubits':qubits})
            else:
                require(len(qubits)==1,'Compiler emitted a non-target interaction')
                operations.append({'name':'unitary','qubits':qubits,'matrix':matrix_payload(Operator(item.operation).data)})
        layout=compiled.layout.final_index_layout(filter_ancillas=True) if compiled.layout else list(range(n))
        self.audit['native_compilations']=1
        return {'operations':operations,'final_layout':list(layout)}
