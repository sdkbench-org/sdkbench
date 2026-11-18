"""Native diagnostic controls and independent semantic checks, not timing scores."""
from copy import deepcopy
import importlib.util
import json
import os
from pathlib import Path
import pytest
from sdkbench.p0 import Bundle
from sdkbench.p0.evaluators import routing
from sdkbench.p0.models import ContractError
from sdkbench.p1a.common import load_adapter
from sdkbench.diagnostics.routing import variants,micro_fixtures,compile_variant

ROOT=Path(__file__).resolve().parents[1]


@pytest.fixture(scope='module')
def bundle():return Bundle(ROOT/'docs/implementation')


@pytest.fixture(scope='module',params=('flagquantum','qiskit','cirq'))
def adapter(request):
    if importlib.util.find_spec(request.param) is None:
        if os.environ.get('SDKBENCH_REQUIRE_ROUTING'):pytest.fail('Required SDK missing: '+request.param)
        pytest.skip('Optional SDK missing: '+request.param)
    return request.param,load_adapter(request.param)


@pytest.mark.parametrize('instance',('ROUTE-LINE-06','ROUTE-GRID-08','ROUTE-LINE-12'))
def test_baseline_reproduction_and_bad_layout(bundle,adapter,instance):
    sdk,native=adapter;id_={'flagquantum':'fq-default','qiskit':'qiskit-default','cirq':'cirq-default'}[sdk]
    config=next(v for v in variants() if v['id']==id_);fixture=deepcopy(bundle.fixtures[instance])
    payload,trace=compile_variant(native,fixture,config,bundle.plan['execution_profile']['compiler_seeds'][0])
    metrics=routing(payload,fixture,None,bundle.cases[instance],0)
    assert metrics['full_cz_count']>0 and trace and fixture==bundle.fixtures[instance]
    bad=deepcopy(payload);bad['final_layout']=[0]*fixture['n_qubits']
    with pytest.raises(ContractError):routing(bad,fixture,None,bundle.cases[instance],0)


@pytest.mark.parametrize('name',('MICRO-LOCAL-CX','MICRO-LOCAL-CANCEL','MICRO-LOCAL-SWAP','MICRO-REMOTE-REUSE','MICRO-SWAP-CX-SAME','MICRO-SWAP-CX-REVERSED'))
def test_microprobe_full_operator(bundle,adapter,name):
    sdk,native=adapter;id_={'flagquantum':'fq-default','qiskit':'qiskit-default','cirq':'cirq-default'}[sdk]
    fixture=micro_fixtures(bundle.fixtures['ROUTE-LINE-06'])[name]
    payload,_=compile_variant(native,fixture,next(v for v in variants() if v['id']==id_),17)
    metrics=routing(payload,fixture,None,bundle.cases['ROUTE-LINE-06'],0)
    assert metrics['verification']=='full-operator'
    if name=='MICRO-LOCAL-CX':assert metrics['full_cz_count']==1
    if name=='MICRO-LOCAL-CANCEL':assert metrics['full_cz_count']==0


def test_factorial_scope_and_excluded_initial_layout_search():
    profile=json.loads((ROOT/'docs/analysis/routing-profile.json').read_text())
    assert profile['variants']==variants() and len(variants())==25
    factor=[v for v in variants() if v['sdk']=='flagquantum' and v['level']==2 and len(v['basis'])==10]
    assert len(factor)==16
    assert len({(v['strategy'],v['drop_restore'],v['post_basis']) for v in factor})==16
    assert all(v.get('strategy')!='sabre_layout' for v in variants())
    assert profile['scope_exclusions'][0]['strategy']=='sabre_layout'
    assert not profile['publication_eligible']


def test_native_error_retains_partial_trace(monkeypatch):
    from sdkbench.diagnostics import worker
    monkeypatch.setattr(worker.metadata,'version',lambda _:'0.3.1')
    class Native:diagnostic_trace={'stage':'partial-native-compilation'}
    monkeypatch.setattr(worker,'load_adapter',lambda _:Native())
    def fail(*args):raise NotImplementedError('Declared native option unavailable')
    monkeypatch.setattr(worker,'compile_variant',fail)
    result=worker.run({'config':{'sdk':'flagquantum'},'fixture':{},'seed':17})
    assert result['status']=='unsupported' and result['payload'] is None
    assert result['trace']==Native.diagnostic_trace and result['reason']
