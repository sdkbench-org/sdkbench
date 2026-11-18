"""Qiskit public Statevector and StatevectorSampler APIs; no Aer or fallback."""
import numpy as np
from .common import AdapterBase, sampled_payload
from ..p0.models import require


class QiskitAdapter(AdapterBase):
    def __init__(self):
        import qiskit
        from qiskit.circuit import ParameterVector
        from qiskit.quantum_info import Statevector, Pauli
        from qiskit.primitives import StatevectorSampler
        self.qiskit = qiskit; self.ParameterVector = ParameterVector
        self.Statevector = Statevector; self.Pauli = Pauli; self.Sampler = StatevectorSampler

    def build(self, fixture, kind):
        n = fixture['n_qubits']; circuit = self.qiskit.QuantumCircuit(n)
        count = 2 * n if kind == 'parameter' else len(fixture.get('parameters', []))
        parameters = self.ParameterVector('p', count)
        for op in fixture['operations']:
            args = list(op['qubits'])
            if op['name'] in ('ry', 'rz'):
                value = parameters[op['parameter']] if 'parameter' in op else op['angle']
                args.insert(0, value)
            getattr(circuit, op['name'])(*args)
        return circuit, parameters

    def bind(self, circuit, parameters, values):
        return circuit.assign_parameters(dict(zip(parameters, values)), inplace=False)

    def expectations(self, circuit, words, n):
        state = self.Statevector.from_instruction(circuit)
        require(state.data.dtype == np.complex128, 'Qiskit did not return complex128 state arithmetic')
        return [state.expectation_value(self.Pauli(word[::-1])) for word in words]

    def sample(self, circuit, fixture, seed):
        for name, qubits in fixture['record_mapping'].items():
            register = self.qiskit.ClassicalRegister(len(qubits), name); circuit.add_register(register)
            for k, q in enumerate(qubits):circuit.measure(q, register[k])
        result = self.Sampler(default_shots=fixture['shots_per_replicate'], seed=seed).run([circuit]).result()[0]
        bits = np.zeros((fixture['shots_per_replicate'], fixture['n_qubits']), dtype=np.uint8)
        for name, qubits in fixture['record_mapping'].items():
            strings = getattr(result.data, name).get_bitstrings()
            require(len(strings) == len(bits), 'Missing native register shots')
            for row, value in enumerate(strings):
                integer = int(value, 2)
                for k, q in enumerate(qubits):bits[row, q] = (integer >> k) & 1
        self.audit['native_executions'] += 1
        return sampled_payload(bits, fixture)
