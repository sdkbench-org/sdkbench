"""FlagQuantum public Circuit, binding, observable and sampling APIs. No SDK patches."""
from functools import reduce
from operator import matmul
from .common import AdapterBase, sampled_payload
from ..p0.models import require


class FlagQuantumAdapter(AdapterBase):
    def __init__(self):
        import flagquantum as fq
        import torch
        self.fq = fq; self.torch = torch
        torch.set_num_threads(1)
        if torch.get_num_interop_threads() != 1:torch.set_num_interop_threads(1)

    def build(self, fixture, kind):
        fq = self.fq; n = fixture['n_qubits']; circuit = fq.Circuit(n, device='cpu', dtype=self.torch.complex128)
        count = 2 * n if kind == 'parameter' else len(fixture.get('parameters', []))
        parameters = [fq.Parameter(f'p_{i:04}') for i in range(count)]
        for op in fixture['operations']:
            params = {}
            if op['name'] in ('ry', 'rz'):
                value = parameters[op['parameter']] if 'parameter' in op else self.torch.tensor(op['angle'], dtype=self.torch.float64)
                params['theta'] = value
            circuit.gate(op['name'], op['qubits'], params=params)
        return circuit, parameters

    def bind(self, circuit, parameters, values):
        return circuit.bind_parameters({parameter.name: self.torch.tensor(value, dtype=self.torch.float64)
                                        for parameter, value in zip(parameters, values)})

    def options(self, **kwargs):
        return self.fq.ExecutionOptions(mode='statevector', backend='pytorch', device='cpu', precision='complex128',
                                        require_gradients=False, allow_approximate=False, allow_backend_fallback=False, **kwargs)

    def expectations(self, circuit, words, n):
        fq = self.fq
        observables = [reduce(matmul, [getattr(fq, axis)(q) for q, axis in enumerate(word) if axis != 'I'], fq.I()) for word in words]
        with self.torch.no_grad():
            result = fq.run(circuit, outputs=[fq.expectation(o) for o in observables], options=self.options())
            values = result.expectations
            require(all(value.dtype == self.torch.float64 for value in values), 'FlagQuantum returned non-float64 expectations')
            return [float(value.detach().cpu().item()) for value in values]

    def sample(self, circuit, fixture, seed):
        with self.torch.no_grad():
            result = self.fq.run(circuit, outputs=self.fq.samples(qubits=list(range(fixture['n_qubits']))),
                                 options=self.options(shots=fixture['shots_per_replicate'], seed=seed))
            bits = result.samples.detach().cpu().numpy()
        self.audit['native_executions'] += 1
        require(bits.shape == (1, fixture['shots_per_replicate'], fixture['n_qubits']), 'Wrong FlagQuantum sample batch shape')
        return sampled_payload(bits[0], fixture)
