"""Cirq public symbolic resolution and complex128 Simulator APIs."""
import numpy as np
from .common import AdapterBase, sampled_payload


class CirqAdapter(AdapterBase):
    def __init__(self):
        import cirq
        import sympy
        self.cirq = cirq; self.sympy = sympy

    def build(self, fixture, kind):
        cirq = self.cirq; qubits = cirq.LineQubit.range(fixture['n_qubits'])
        count = 2 * len(qubits) if kind == 'parameter' else len(fixture.get('parameters', []))
        parameters = [self.sympy.Symbol(f'p_{i:04}') for i in range(count)]; ops = []
        for op in fixture['operations']:
            q = [qubits[i] for i in op['qubits']]; name = op['name']
            if name in ('ry', 'rz'):
                value = parameters[op['parameter']] if 'parameter' in op else op['angle']
                ops.append(getattr(cirq, name)(value).on(*q))
            else:ops.append({'h': cirq.H, 'x': cirq.X, 'cx': cirq.CNOT, 'cz': cirq.CZ}[name].on(*q))
        return cirq.Circuit(ops), parameters

    def bind(self, circuit, parameters, values):
        return self.cirq.resolve_parameters(circuit, dict(zip(parameters, values)))

    def expectations(self, circuit, words, n):
        cirq = self.cirq; qubits = cirq.LineQubit.range(n)
        observables = [cirq.PauliString({qubits[q]: {'X': cirq.X, 'Y': cirq.Y, 'Z': cirq.Z}[axis]
                                       for q, axis in enumerate(word) if axis != 'I'}) for word in words]
        return cirq.Simulator(dtype=np.complex128).simulate_expectation_values(circuit, observables,
                                                                             qubit_order=list(reversed(qubits)))

    def sample(self, circuit, fixture, seed):
        cirq = self.cirq; qubits = cirq.LineQubit.range(fixture['n_qubits'])
        for name, selected in fixture['record_mapping'].items():
            circuit.append(cirq.measure(*(qubits[q] for q in selected), key=name))
        result = cirq.Simulator(dtype=np.complex128, seed=seed).run(circuit, repetitions=fixture['shots_per_replicate'])
        bits = np.zeros((fixture['shots_per_replicate'], fixture['n_qubits']), dtype=np.uint8)
        for name, selected in fixture['record_mapping'].items():
            bits[:, selected] = result.measurements[name]
        self.audit['native_executions'] += 1
        return sampled_payload(bits, fixture)
