"""Real SDK execution against the frozen independent P0 acceptance rules."""
from copy import deepcopy
from dataclasses import replace
from pathlib import Path
import importlib.util
import os
import pytest
from sdkbench.p0 import Bundle, ResultRecord, evaluate
from sdkbench.p0.models import ContractError
from sdkbench.p1a.common import load_adapter, validate_fixture

ROOT = Path(__file__).resolve().parents[1]
SDKS = ('flagquantum', 'qiskit', 'cirq')


@pytest.fixture(scope='module')
def bundle():return Bundle(ROOT / 'docs/implementation')


@pytest.fixture(scope='module', params=SDKS)
def adapter(request):
    if importlib.util.find_spec(request.param) is None:
        if os.environ.get('SDKBENCH_REQUIRE_P1A'):pytest.fail('Required SDK missing: ' + request.param)
        pytest.skip('Optional SDK not installed: ' + request.param)
    return request.param, load_adapter(request.param)


@pytest.mark.parametrize('instance', ['PARAM-04', 'SAMPLE-03', 'SAMPLE-05', 'OBS-04'])
def test_native_outputs_pass_frozen_acceptance(bundle, adapter, instance):
    sdk, native = adapter; fixture = deepcopy(bundle.fixtures[instance]); kind = bundle.cases[instance]['kind']
    identity = bundle.identity(instance, sdk, '1' * 64, '2' * 64)
    payload = native.execute(kind, fixture, bundle.request(identity)['sampling_seeds'][0])
    result = ResultRecord(identity, 0, 0, 'completed', payload)
    verdict = evaluate(bundle, result, identity)
    assert verdict.status == 'accepted', verdict
    assert fixture == bundle.fixtures[instance]
    assert native.audit['native_program_builds'] == 1
    assert native.audit['native_executions'] == (7 if kind == 'parameter' else 1)
    if kind == 'parameter':assert native.audit['native_bindings'] == 7
    # The same negative output mutation must fail for every SDK.
    corrupted = deepcopy(payload)
    if kind == 'parameter':corrupted['outputs'][1]['Y0'] *= -1
    elif kind == 'observable':corrupted['expectations'][0] += .1
    else:corrupted['contexts'][0]['counts'][0] += 1
    assert evaluate(bundle, replace(result, payload=corrupted), identity).status != 'accepted'


def test_parameter_template_is_reusable_and_does_not_leak_binding(bundle, adapter):
    sdk, native = adapter; fixture = bundle.fixtures['PARAM-04']; template, parameters = native.build(fixture, 'parameter')
    words = ['XIII', 'YIII', 'ZIII', 'ZZII']
    first = native.expectations(native.bind(template, parameters, fixture['bindings'][1]), words, 4)
    changed = native.expectations(native.bind(template, parameters, fixture['bindings'][2]), words, 4)
    again = native.expectations(native.bind(template, parameters, fixture['bindings'][1]), words, 4)
    import numpy as np
    np.testing.assert_allclose(again, first, atol=1e-12)
    assert not np.allclose(first, changed)


@pytest.mark.parametrize('fault', ['missing', 'extra', 'nested', 'nonfinite'])
def test_bad_bindings_fail_uniformly_before_execution(bundle, adapter, fault):
    _, native = adapter; fixture = deepcopy(bundle.fixtures['PARAM-04'])
    if fault == 'missing':fixture['bindings'][1].pop()
    elif fault == 'extra':fixture['bindings'][1].append(0.)
    elif fault == 'nested':fixture['bindings'][1][0] = [0.]
    else:fixture['bindings'][1][0] = float('nan')
    with pytest.raises(ContractError):native.execute('parameter', fixture, 11)
