"""Native P1b outputs and uniform negative mutations against frozen P0 references."""
from copy import deepcopy
from dataclasses import replace
import importlib.util
import os
from pathlib import Path
import pytest
from sdkbench.p0 import Bundle, ResultRecord, evaluate
from sdkbench.p1b.common import load_adapter, UnsupportedCapability, WORKFLOWS

ROOT = Path(__file__).resolve().parents[1]
INSTANCES = ('GRAD-04', 'GRAD-08', 'GRAD-12', 'DYN-04-S32', 'DYN-08-S64',
             'ROUTE-LINE-06', 'ROUTE-GRID-08', 'ROUTE-LINE-12')


@pytest.fixture(scope='module')
def bundle():return Bundle(ROOT / 'docs/implementation')


@pytest.fixture(scope='module', params=('flagquantum', 'qiskit', 'cirq'))
def adapter(request):
    if importlib.util.find_spec(request.param) is None:
        if os.environ.get('SDKBENCH_REQUIRE_P1B'):pytest.fail('Required SDK missing: ' + request.param)
        pytest.skip('Optional SDK missing: ' + request.param)
    return request.param, load_adapter(request.param)


@pytest.mark.parametrize('instance', INSTANCES)
def test_all_native_instances_and_adversarial_outputs(bundle, adapter, instance):
    sdk, native = adapter; kind = bundle.cases[instance]['kind']
    fixture = deepcopy(bundle.fixtures[instance])
    if sdk == 'cirq' and kind == 'gradient':
        with pytest.raises(UnsupportedCapability, match='No benchmark-side derivative'):
            native.execute(kind, fixture, 17)
        assert native.audit['native_executions'] == 0
        return
    if sdk == 'qiskit' and kind == 'gradient' and importlib.util.find_spec('qiskit_algorithms') is None:
        if os.environ.get('SDKBENCH_REQUIRE_P1B'):pytest.fail('Required gradient extension missing')
        pytest.skip('Optional qiskit-algorithms extension missing')
    identity = bundle.identity(instance, sdk, '1' * 64, '2' * 64)
    payload = native.execute(kind, fixture, bundle.request(identity)['compiler_seed'])
    result = ResultRecord(identity, 0, 0, 'completed', payload)
    verdict = evaluate(bundle, result, identity)
    assert verdict.status == 'accepted', verdict
    assert fixture == bundle.fixtures[instance]
    assert native.audit['native_program_builds'] == 1
    bad = deepcopy(payload)
    if kind == 'gradient':
        # Shared-parameter chains, including zero/near-zero parameters, cannot be dropped.
        assert fixture['parameters'][:2] == [0., 1e-7]
        bad['jacobian'][0][0] += .1
        assert payload['derivative']['quantum_evaluations'] >= 1
        assert payload['derivative']['components']
    elif kind == 'dynamics':bad['moments'][0] += .1
    else:
        assert payload['compile_wall_seconds'] <= 120
        assert len(payload['final_layout']) == fixture['n_qubits']
        assert native.audit['native_compilations'] == 1
        bad['operations'].append({'name': 'x', 'qubits': [0]})
    assert evaluate(bundle, replace(result, payload=bad), identity).status != 'accepted'
    if kind == 'route':
        bad = deepcopy(payload);bad['final_layout'] = [0] * fixture['n_qubits']
        assert evaluate(bundle, replace(result, payload=bad), identity).status != 'accepted'
        bad = deepcopy(payload);bad['compile_wall_seconds'] = 120.01
        assert evaluate(bundle, replace(result, payload=bad), identity).status != 'accepted'
        bad = deepcopy(payload);bad['operations'].append({'name': 'cz', 'qubits': [0, fixture['n_qubits'] - 1]})
        assert evaluate(bundle, replace(result, payload=bad), identity).status != 'accepted'


def test_exact_frozen_scope(bundle):
    assert set(INSTANCES) == {i for i,c in bundle.cases.items() if c['workflow'] in WORKFLOWS}
