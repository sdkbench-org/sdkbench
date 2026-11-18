"""Positive and adversarial qualification for every first-wave acceptance family."""
from copy import deepcopy
from dataclasses import replace
from pathlib import Path
import json
import math
import shutil
import numpy as np
import pytest
from sdkbench.p0 import Bundle, ContractError, ResultRecord, evaluate, evaluate_case
from sdkbench.p0.models import canonical_bytes, read_json
from sdkbench.p0.semantics import angle_expression, equivalent, propagate, qasm3_distribution
from sdkbench.p0.transport import OfflineTransport
from p0_cases import counts_for, legal_route, positive_payload, record

ROOT = Path(__file__).resolve().parents[1]
CASES = [c['id'] for c in json.loads((ROOT / 'docs/implementation/roadmap.json').read_text())['instances']]


@pytest.fixture(scope='module')
def bundle():return Bundle(ROOT / 'docs/implementation')


@pytest.mark.parametrize('instance', CASES)
def test_all_24_positive_references(bundle, instance):
    verdict = evaluate(bundle, record(bundle, instance))
    assert verdict.status == 'accepted', verdict


@pytest.mark.parametrize('instance', CASES)
def test_all_24_reject_missing_payload_fields(bundle, instance):
    r = record(bundle, instance); payload = deepcopy(r.payload); payload.pop(next(iter(payload)))
    assert evaluate(bundle, replace(r, payload=payload)).status == 'incorrect'


@pytest.mark.parametrize('fault', ['binding-order', 'stale-binding', 'y-sign', 'missing-value', 'extra-value', 'nan', 'inf', 'wrong-shape'])
def test_parameter_faults(bundle, fault):
    r = record(bundle, 'PARAM-04'); p = r.payload
    if fault == 'binding-order':p['binding_ids'][1:3] = [2, 1]
    elif fault == 'stale-binding':p['outputs'][2] = deepcopy(p['outputs'][1])
    elif fault == 'y-sign':p['outputs'][1]['Y0'] *= -1
    elif fault == 'missing-value':p['outputs'][0].pop('X0')
    elif fault == 'extra-value':p['outputs'][0]['unexpected'] = 0
    elif fault in ('nan', 'inf'):
        raw = r.to_dict(); raw['payload']['outputs'][0]['X0'] = float(fault)
        assert evaluate(bundle, raw).status == 'incorrect'; return
    else:p['outputs'][0]['X0'] = [0.]
    assert evaluate(bundle, r).status == 'incorrect'


@pytest.mark.parametrize('fault', ['single-term', 'weighted-sum', 'gradient', 'transpose', 'derivative-attribution', 'digital-only', 'physics-only'])
def test_scientific_faults(bundle, fault):
    id_ = 'OBS-04' if fault in ('single-term', 'weighted-sum') else 'GRAD-04' if fault in ('gradient', 'transpose', 'derivative-attribution') else 'DYN-04-S32'
    r = record(bundle, id_); p = r.payload
    if fault == 'single-term':p['expectations'][3] += .01
    elif fault == 'weighted-sum':p['weighted_sum'] += .01
    elif fault == 'gradient':p['jacobian'][0][0] *= .5
    elif fault == 'transpose':p['jacobian'] = np.array(p['jacobian']).T.tolist()
    elif fault == 'derivative-attribution':p['derivative']['method'] = ''
    elif fault == 'physics-only':p['moments'] = bundle.references[id_]['exact_physics']
    else:
        # This is neither physically nor digitally correct; a good digital
        # oracle with a deliberately tightened physics threshold tests both gates below.
        p['moments'][0] += .1
    assert evaluate(bundle, r).status == 'incorrect'


def test_dynamics_physics_gate_independent_of_digital_gate(bundle):
    b = deepcopy(bundle); b.cases['DYN-04-S32']['acceptance']['physics_max_abs_observable_error'] = 1e-8
    assert evaluate(b, record(b, 'DYN-04-S32')).status == 'incorrect'


@pytest.mark.parametrize('fault', ['total', 'negative', 'fractional', 'boolean', 'mapping', 'reordered-bits', 'duplicate', 'missing-category', 'law'])
def test_sampling_faults(bundle, fault):
    r = record(bundle, 'SAMPLE-05'); c = r.payload['contexts'][0]
    if fault == 'total':c['counts'][0] += 1
    elif fault == 'negative':c['counts'][0] = -1
    elif fault == 'fractional':c['counts'][0] = float(c['counts'][0])
    elif fault == 'boolean':c['counts'][0] = True
    elif fault == 'mapping':c['records'][0]['register_a'] = 3
    elif fault == 'reordered-bits':
        for row in c['records']:
            a = row['register_a']; row['register_a'] = ((a & 1) << 1) | (a >> 1)
    elif fault == 'duplicate':c['records'].append(deepcopy(c['records'][0]))
    elif fault == 'missing-category':c['counts'].pop()
    else:
        c['counts'] = [65536] + [0] * 31
        for row in c['records']:row['count'] = 65536 if row['register_a'] == row['register_b'] == 0 else 0
    assert evaluate(bundle, r).status == 'incorrect'


def teleport_law(inp, axis, fault):
    inputs = {'zero': [1, 0], 'one': [0, 1], 'plus': np.array([1, 1]) / math.sqrt(2), 'minus': np.array([1, -1]) / math.sqrt(2), 'plus-i': np.array([1, 1j]) / math.sqrt(2), 'minus-i': np.array([1, -1j]) / math.sqrt(2)}
    initial = np.zeros(8, complex); initial[:2] = inputs[inp]
    state = propagate(3, [{'name': 'h', 'qubits': [1]}, {'name': 'cx', 'qubits': [1, 2]}, {'name': 'cx', 'qubits': [0, 1]}, {'name': 'h', 'qubits': [0]}], initial)
    probabilities = [0.] * 8
    for m0 in (0, 1):
        for m1 in (0, 1):
            branch = state.copy(); ix = np.arange(8); branch[((ix & 1) != m0) | (((ix >> 1) & 1) != m1)] = 0
            ops = []
            if (m0 if fault == 'swapped-feedforward' else m1) and fault != 'missing-x':ops.append({'name': 'x', 'qubits': [2]})
            if (m1 if fault == 'swapped-feedforward' else m0) and fault != 'missing-z':ops.append({'name': 'z', 'qubits': [2]})
            if axis == 'Y':ops.append({'name': 'sdg', 'qubits': [2]})
            if axis != 'Z':ops.append({'name': 'h', 'qubits': [2]})
            branch = propagate(3, ops, branch)
            for out in (0, 1):
                a, b = (m1, m0) if fault == 'swapped-bits' else (m0, m1)
                probabilities[4 * a + 2 * b + out] = float(abs(branch[m0 + 2 * m1 + 4 * out])**2)
    return probabilities


@pytest.mark.parametrize('fault', ['missing-x', 'missing-z', 'swapped-feedforward', 'swapped-bits', 'missing-branch'])
def test_adaptive_teleportation_faults(bundle, fault):
    r = record(bundle, 'ADAPT-TELEPORT')
    for c, f in zip(r.payload['contexts'], bundle.fixtures['ADAPT-TELEPORT']['contexts']):
        p = teleport_law(f['input'], f['bob_basis'], fault)
        if fault == 'missing-branch':p = p[:4] + [0] * 4; p = np.array(p) / sum(p)
        c['counts'] = counts_for(p)
    # Swapping the two uniformly random teleportation measurement bits alone
    # preserves this ideal joint law; it is observationally indistinguishable.
    assert evaluate(bundle, r).status == ('accepted' if fault == 'swapped-bits' else 'incorrect')


@pytest.mark.parametrize('fault', ['missing-reset', 'cutoff', 'postselection'])
def test_bounded_loop_faults(bundle, fault):
    r = record(bundle, 'ADAPT-RESET-LOOP'); c = r.payload['contexts'][0]
    if fault == 'missing-reset':c['counts'][3] = c['counts'][2]; c['counts'][2] = 0
    elif fault == 'cutoff':c['counts'][10] += c['counts'][8]; c['counts'][8] = 0
    else:c['counts'][8] = 0
    assert evaluate(bundle, r).status == 'incorrect'


@pytest.mark.parametrize('fault', ['checkpoint', 'gradient', 'step-count', 'seed', 'test-loss', 'no-progress'])
def test_training_faults(bundle, fault):
    r = record(bundle, 'TRAIN-04-B16'); p = r.payload
    if fault == 'checkpoint':p['trace'][19]['theta'][1] += .1
    elif fault == 'gradient':p['gradients'][7]['weights'][0] += .1
    elif fault == 'step-count':p['trace'].pop()
    elif fault == 'seed':p['seed'] = 23
    elif fault == 'test-loss':p['trace'][-1]['test_loss'] += .1
    else:p['trace'][-1]['train_loss'] = p['trace'][0]['train_loss']
    assert evaluate(bundle, r).status == 'incorrect'


def test_every_training_initialization(bundle):
    r = record(bundle, 'TRAIN-08-B32'); records = [record(bundle, r.identity.instance_id, block=b) for b in range(10)]
    assert evaluate_case(bundle, r.identity, records).status == 'accepted'


@pytest.mark.parametrize('fault', ['nonedge', 'partial-cz', 'ancilla', 'rotation', 'nonunitary', 'layout', 'compile-cap'])
def test_routing_faults(bundle, fault):
    r = record(bundle, 'ROUTE-LINE-06'); p = r.payload
    if fault == 'nonedge':p['operations'].append({'name': 'cz', 'qubits': [0, 5]})
    elif fault == 'partial-cz':p['operations'].append({'name': 'cz', 'qubits': [0, 1], 'angle': .1})
    elif fault == 'ancilla':p['operations'].append({'name': 'h', 'qubits': [6]})
    elif fault == 'rotation':p['operations'][0]['angle'] += .1
    elif fault == 'nonunitary':p['operations'].append({'name': 'unitary', 'qubits': [0], 'matrix': [[[1, 0], [0, 0]], [[0, 0], [2, 0]]]})
    elif fault == 'layout':p['final_layout'][0:2] = [1, 0]
    else:p['compile_wall_seconds'] = 120.01
    assert evaluate(bundle, r).status == 'incorrect'


def test_layout_reconstruction_and_global_phase(bundle):
    r = record(bundle, 'ROUTE-LINE-06')
    # Three CXs make a physical SWAP; all CXs expanded into target-legal H/CZ.
    f = {'n_qubits': 6, 'target_edges': bundle.fixtures[r.identity.instance_id]['target_edges'], 'operations': [{'name': 'cx', 'qubits': [a, b]} for a, b in [(0, 1), (1, 0), (0, 1)]]}
    r.payload['operations'].extend(legal_route(f)); r.payload['final_layout'][:2] = [1, 0]
    r.payload['operations'].append({'name': 'unitary', 'qubits': [0], 'matrix': [[[0, 1], [0, 0]], [[0, 0], [0, 1]]]})
    assert evaluate(bundle, r).status == 'accepted'
    with pytest.raises(ContractError):equivalent(np.diag([1., -1.]), np.eye(2), 1e-8)


@pytest.mark.parametrize('fault', ['conditional', 'reset', 'register', 'angle', 'unknown', 'export-only'])
def test_interchange_faults(bundle, fault):
    id_ = 'ROUND-QASM3' if fault in ('conditional', 'reset', 'unknown') else 'ROUND-QASM2'
    r = record(bundle, id_); source = r.payload['exported_source']
    if fault == 'conditional':source = source.replace('if (c[1]) { x q[1]; }', '')
    elif fault == 'reset':source = source.replace('reset q[0];', '')
    elif fault == 'register':source = source.replace('q[0] -> c[2]', 'q[0] -> c[3]').replace('q[2] -> c[3]', 'q[2] -> c[2]')
    elif fault == 'angle':source = source.replace('0.37', '0.38')
    elif fault == 'unknown':source += 'opaque unsupported;'
    else:r.payload['reimported_source'] = source.replace('-0.81', '0.81')
    r.payload['exported_source'] = source
    assert evaluate(bundle, r).status == 'incorrect'


@pytest.mark.parametrize('fault', ['resubmit', 'identity', 'repeated-page', 'shots', 'cancelled', 'hidden-retry'])
def test_operational_faults(bundle, fault):
    id_ = 'JOB-LOST-ACK' if fault in ('resubmit', 'identity', 'hidden-retry') else 'JOB-PARTIAL-CANCEL'
    r = record(bundle, id_); p = r.payload
    if fault in ('resubmit', 'hidden-retry'):p['transport_trace'].append(deepcopy(p['transport_trace'][0]))
    elif fault == 'identity':p['client_result']['job_ids'] = ['job-002']
    elif fault == 'repeated-page':p['client_result']['records'].append(deepcopy(p['client_result']['records'][1]))
    elif fault == 'shots':p['client_result']['records'][1]['shots'] += 256
    else:p['client_result']['state'] = 'completed'
    assert evaluate(bundle, r).status == 'incorrect'


def test_offline_transport_does_not_reconcile_for_client(bundle):
    t = OfflineTransport(bundle.fixtures['JOB-LOST-ACK'])
    with pytest.raises(TimeoutError):t.submit('request-001')
    assert len(t.trace) == 1
    assert t.reconcile('request-001') == 'job-001'
    assert t.poll('job-001') == 'completed'
    r = record(bundle, 'JOB-LOST-ACK'); r.payload['transport_trace'] = t.trace
    assert evaluate(bundle, r).status == 'accepted'
    t = OfflineTransport(bundle.fixtures['JOB-PARTIAL-CANCEL'])
    assert len([t.next_event() for _ in range(4)]) == 4
    with pytest.raises(StopIteration):t.next_event()


def test_full_case_coverage_and_identity(bundle):
    identity = record(bundle, 'PARAM-04').identity
    records = [record(bundle, 'PARAM-04', b, r) for b in range(10) for r in range(3)]
    assert evaluate_case(bundle, identity, records).status == 'accepted'
    assert evaluate_case(bundle, identity, records[:-1]).status == 'not-measured'
    assert evaluate_case(bundle, identity, records + records[:1]).status == 'incorrect'
    mixed = records[:-1] + [replace(records[-1], identity=replace(identity, stack_id='another-stack'))]
    assert evaluate_case(bundle, identity, mixed).status == 'incorrect'
    assert evaluate(bundle, replace(records[0], identity=replace(identity, fixture_sha256='a' * 64))).status == 'incorrect'


@pytest.mark.parametrize('status', ['not-implemented', 'unsupported', 'install-failed', 'access-blocked', 'not-measured', 'timeout', 'out-of-memory', 'error'])
def test_failure_accounting(bundle, status):
    r = record(bundle, 'PARAM-04'); failure = replace(r, status=status, payload=None, reason='Qualification fault')
    assert evaluate(bundle, failure).status == status
    assert evaluate_case(bundle, r.identity, [failure]).status == status


@pytest.mark.parametrize('name', ['FlagQuantum', 'Qiskit', 'Cirq', 'unlisted-specialist'])
def test_no_identity_based_exceptions(bundle, name):
    r = record(bundle, 'PARAM-04', stack_id=name)
    assert evaluate(bundle, r).status == 'accepted'
    r.payload['outputs'][1]['Y0'] *= -1
    assert evaluate(bundle, r).status == 'incorrect'


def test_schema_strict_json_and_bundle_hashes(bundle, tmp_path):
    r = record(bundle, 'PARAM-04'); assert ResultRecord.from_dict(r.to_dict()) == r
    for text in ['{"x":1,"x":2}', '{"x":NaN}', '{"x":Infinity}', '{broken']:
        p = tmp_path / 'bad.json'; p.write_text(text)
        with pytest.raises(ContractError):read_json(p)
    with pytest.raises(ContractError):ResultRecord.from_dict({**r.to_dict(), 'winner': True})
    with pytest.raises(ContractError):replace(r, block=True)
    with pytest.raises(ContractError):replace(r, status='accepted')
    copy = tmp_path / 'bundle'; shutil.copytree(bundle.directory, copy)
    (copy / 'fixtures/PARAM-04.json').write_text('{}')
    with pytest.raises(ContractError, match='hash mismatch'):Bundle(copy)


def test_request_contains_inputs_not_gold(bundle):
    identity = record(bundle, 'PARAM-04').identity; request = bundle.request(identity)
    assert 'reference' not in request and 'outputs' not in request['fixture']
    request['fixture']['bindings'][0][0] = 1
    assert bundle.fixtures['PARAM-04']['bindings'][0][0] == 0
    assert bundle.request(identity)['sampling_seeds'] == bundle.request(identity)['sampling_seeds']
    assert bundle.request(identity, block=1)['sampling_seeds'] != bundle.request(identity)['sampling_seeds']


def test_primitive_semantic_anchors():
    bell = propagate(2, [{'name': 'h', 'qubits': [0]}, {'name': 'cx', 'qubits': [0, 1]}])
    np.testing.assert_allclose(bell, np.array([1, 0, 0, 1]) / math.sqrt(2), atol=1e-14)
    assert angle_expression('-pi/2 + 0.1') == -math.pi / 2 + .1
    with pytest.raises(ContractError):angle_expression('__import__("os")')
    with pytest.raises(ContractError):qasm3_distribution('not a program')


def test_registration_hashes_and_precision(bundle):
    from sdkbench.p0.registration import Registration
    registration = Registration('synthetic', [{'name': 'test-component', 'version': '1', 'role': 'qualification-only', 'artifact_sha256': 'a' * 64}],
                                {'profile': 'CPU1-FP64', 'precision': 'float64/complex128', 'threads': 1, 'options': {}},
                                {'python': 'test-only', 'os': 'test-only', 'image_sha256': 'b' * 64, 'dependency_lock_sha256': 'c' * 64, 'host': {'id': 'synthetic'}})
    identity = registration.identity(bundle, 'PARAM-04')
    bundle.verify_identity(identity)
    other = replace(registration, components=[{**registration.components[0], 'version': '2'}])
    assert other.configuration_sha256 != registration.configuration_sha256
    with pytest.raises(ContractError):replace(registration, configuration={**registration.configuration, 'precision': 'float32'})
    r = record(bundle, 'PARAM-04')
    assert evaluate(bundle, replace(r, identity=replace(r.identity, bundle_sha256='f' * 64))).status == 'incorrect'
    assert evaluate(bundle, replace(r, identity=replace(r.identity, reference_sha256='f' * 64))).status == 'incorrect'


def test_primitive_against_separate_dense_tensor_construction():
    from sdkbench.p0.semantics import rotation
    rng = np.random.default_rng(411)
    for n in (2, 3, 4):
        state = rng.normal(size=2**n) + 1j * rng.normal(size=2**n); state /= np.linalg.norm(state)
        expected = state.copy(); ops = []
        for i in range(16):
            q = i % n; angle = float(rng.uniform(-2, 2)); name = ('rx', 'ry', 'rz')[i % 3]
            op = {'name': name, 'qubits': [q], 'angle': angle}; ops.append(op)
            # Independent matrices: literal trigonometric entries, tensor multiplication.
            c, s = math.cos(angle / 2), math.sin(angle / 2)
            gate = {'rx': np.array([[c, -1j*s], [-1j*s, c]]), 'ry': np.array([[c, -s], [s, c]]), 'rz': np.diag([np.exp(-.5j*angle), np.exp(.5j*angle)])}[name]
            full = np.array([[1.]])
            for wire in reversed(range(n)):full = np.kron(full, gate if wire == q else np.eye(2))
            expected = full @ expected
            a, b = q, (q + 1) % n; ops.append({'name': 'cx', 'qubits': [a, b]})
            permutation = np.zeros((2**n, 2**n))
            for column in range(2**n):permutation[column ^ ((1 << b) if (column >> a) & 1 else 0), column] = 1
            expected = permutation @ expected
        np.testing.assert_allclose(propagate(n, ops, state), expected, atol=2e-14)


def test_workflow_completeness_and_registration(bundle):
    from sdkbench.p0 import evaluate_workflow
    records = [record(bundle, id_, b) for id_ in ('SAMPLE-03', 'SAMPLE-05') for b in range(10)]
    assert evaluate_workflow(bundle, 'W08', records).status == 'accepted'
    assert evaluate_workflow(bundle, 'W08', records[:10]).status == 'not-measured'
    assert evaluate_workflow(bundle, 'W08', records[:-1]).status == 'not-measured'
    assert evaluate_workflow(bundle, 'W08', records + records[:1]).status == 'incorrect'
    mixed = records[:-1] + [replace(records[-1], identity=replace(records[-1].identity, stack_id='other'))]
    assert evaluate_workflow(bundle, 'W08', mixed).status == 'incorrect'
    assert evaluate_workflow(bundle, 'W08', [record(bundle, 'PARAM-04')]).status == 'incorrect'
    assert evaluate_workflow(bundle, 'unknown', records).status == 'incorrect'
