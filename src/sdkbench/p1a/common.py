"""Shared task contracts and output normalization; no simulation or reference math."""
import re
import numpy as np
from ..p0.models import ContractError, finite, integer, require

SDKS = ('flagquantum', 'qiskit', 'cirq')
DISTRIBUTIONS = {'flagquantum': 'flagquantum', 'qiskit': 'qiskit', 'cirq': 'cirq-core'}
VERSIONS = {'flagquantum': '0.3.1', 'qiskit': '2.6.2', 'cirq': '1.7.0'}
WORKFLOWS = ('W01', 'W04', 'W08')
KINDS = {'W01': 'parameter', 'W04': 'observable', 'W08': 'sampling'}


class UnsupportedCapability(RuntimeError):
    """A required public SDK feature is absent, not replaced by benchmark code."""


def validate_fixture(kind, fixture):
    require(kind in KINDS.values(), 'Task kind is outside P1a')
    n = integer(fixture['n_qubits'], 1)
    require(isinstance(fixture['operations'], list), 'Operations must be a list')
    count = 2 * n if kind == 'parameter' else len(fixture.get('parameters', []))
    for op in fixture['operations']:
        name = op['name']; require(name in ('h', 'x', 'ry', 'rz', 'cx', 'cz'), 'Unsupported P1a operation')
        require(len(op['qubits']) == (2 if name in ('cx', 'cz') else 1), 'Wrong operation arity')
        for q in op['qubits']:integer(q); require(q < n, 'Out-of-range wire')
        require(len(set(op['qubits'])) == len(op['qubits']), 'Duplicate operation wire')
        if name in ('ry', 'rz'):
            require(('angle' in op) != ('parameter' in op), 'Rotation requires one angle source')
            if 'angle' in op:finite(op['angle'])
            else:integer(op['parameter']); require(op['parameter'] < count, 'Unbound parameter index')
    if kind == 'parameter':
        require(isinstance(fixture['bindings'], list) and fixture['bindings'], 'Missing parameter bindings')
        for binding in fixture['bindings']:
            require(isinstance(binding, list) and len(binding) == count, 'Missing/extra or shape-incompatible binding')
            for value in binding:finite(value)
        for name in fixture['observable_order']:local_word(name, n)
    if kind == 'observable':
        require(len(fixture['pauli_words']) == len(fixture['coefficients']), 'Observable/weight mismatch')
        for word in fixture['pauli_words']:require(len(word) == n and set(word) <= set('IXYZ'), 'Malformed Pauli word')
        for value in fixture['parameters'] + fixture['coefficients']:finite(value)


def local_word(name, n):
    matches = re.findall(r'([XYZ])(\d+)', name)
    require(matches and ''.join(axis + q for axis, q in matches) == name, 'Invalid local observable label')
    word = ['I'] * n; seen = set()
    for axis, q in matches:
        q = int(q); require(q < n and q not in seen, 'Invalid local observable wire'); seen.add(q); word[q] = axis
    return ''.join(word)


def real_values(values, count):
    values = np.asarray(values)
    require(values.shape == (count,), 'SDK returned wrong output count/shape')
    require(np.isfinite(values).all() and np.max(abs(values.imag)) <= 1e-12, 'SDK returned nonfinite or complex expectations')
    return [float(value.real) for value in values]


def sampled_payload(bits, fixture):
    """Normalize native joint shot rows. Never draw samples or compute probabilities."""
    bits = np.asarray(bits); n = fixture['n_qubits']; shots = fixture['shots_per_replicate']
    require(bits.shape == (shots, n) and bits.dtype.kind in 'iub', 'Wrong native sample shape/type')
    require(np.isin(bits, [0, 1]).all(), 'Nonbinary native sample')
    logical = bits.astype(np.int64) @ (1 << np.arange(n, dtype=np.int64))
    counts = np.bincount(logical, minlength=1 << n).tolist()
    records = []
    for index, count in enumerate(counts):
        row = {'count': int(count)}
        for register, qubits in fixture['record_mapping'].items():
            row[register] = sum(((index >> q) & 1) << k for k, q in enumerate(qubits))
        records.append(row)
    return {'contexts': [{'context_id': 0, 'counts': counts, 'records': records}]}


def load_adapter(name):
    if name == 'qiskit':
        from .qiskit import QiskitAdapter
        return QiskitAdapter()
    if name == 'cirq':
        from .cirq import CirqAdapter
        return CirqAdapter()
    if name == 'flagquantum':
        from .flagquantum import FlagQuantumAdapter
        return FlagQuantumAdapter()
    raise ValueError('Unknown SDK')


class AdapterBase:
    """Each outcome builds one native template; each binding uses that template."""
    def execute(self, kind, fixture, seed):
        validate_fixture(kind, fixture)
        self.audit = {'native_program_builds': 0, 'native_bindings': 0, 'native_executions': 0}
        template, parameters = self.build(fixture, kind)
        self.audit['native_program_builds'] += 1
        if kind == 'sampling':return self.sample(template, fixture, seed)
        words = [local_word(name, fixture['n_qubits']) for name in fixture['observable_order']] if kind == 'parameter' else fixture['pauli_words']
        bindings = fixture['bindings'] if kind == 'parameter' else [fixture['parameters']]
        outputs = []
        for binding in bindings:
            bound = self.bind(template, parameters, binding)
            self.audit['native_bindings'] += 1
            values = real_values(self.expectations(bound, words, fixture['n_qubits']), len(words))
            self.audit['native_executions'] += 1
            outputs.append(values)
        if kind == 'parameter':
            return {'binding_ids': list(range(len(bindings))), 'observable_order': fixture['observable_order'],
                    'outputs': [dict(zip(fixture['observable_order'], row)) for row in outputs]}
        return {'expectations': outputs[0], 'weighted_sum': float(np.dot(fixture['coefficients'], outputs[0]))}
