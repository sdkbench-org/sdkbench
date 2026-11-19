"""Opt-in native adapter conformance, not a resource-qualified campaign."""
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from sdkbench.candidates.adapters import WORKFLOWS
from sdkbench.candidates.applications import FAMILIES, fixture
from sdkbench.p0 import Bundle
from sdkbench.p0.evaluators import routing

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.skipif(os.environ.get('SDKBENCH_NATIVE_CANDIDATE_TESTS') != '1',
                    reason='Explicit native candidate environment required')
@pytest.mark.parametrize('workflow', tuple(WORKFLOWS))
@pytest.mark.parametrize('family', ('frozen', *FAMILIES))
def test_native_workflow_satisfies_independent_arbitrary_input_semantics(workflow, family):
    script = r'''
import json
from contextlib import nullcontext
from types import SimpleNamespace
from pathlib import Path
from unittest.mock import patch
from sdkbench.candidates.adapters import load_adapter, workflow_configuration
from sdkbench.p0 import Bundle
from sdkbench.candidates.applications import fixture
import sys
workflow = sys.argv[1]
config = workflow_configuration(workflow)
registration = SimpleNamespace(configuration={'options': {
    'sdk': config['sdk'], 'workflow': workflow, 'compiler_options': config}})
bundle = Bundle(sys.argv[2])
adapter = load_adapter(registration)
selected = (bundle.fixtures['ROUTE-LINE-06'] if sys.argv[3] == 'frozen'
            else fixture(6, sys.argv[3], 'line', '01' * 32))
ordinary_native = config['sdk'] == 'flagquantum' and workflow != 'flagquantum-target-artifact'
if ordinary_native:
    from flagquantum.compiler import compile as native_compile
    context = patch('flagquantum.compiler.compile', wraps=native_compile)
else:
    context = nullcontext()
with context as compiler:
    payload = adapter.execute('route', selected,
                              bundle.plan['execution_profile']['compiler_seeds'][0])
    routing_arguments = ([
        {key: value for key, value in call.kwargs.items() if key == 'routing_strategy'}
        for call in compiler.call_args_list
    ] if ordinary_native else None)
print(json.dumps({'payload': payload, 'audit': adapter.audit, 'routing_arguments': routing_arguments}))
'''
    result = subprocess.run([sys.executable, '-c', script, workflow, str(ROOT / 'docs/implementation'), family],
                            capture_output=True, text=True, timeout=150, check=False)
    assert result.returncode == 0, result.stderr
    output = json.loads(result.stdout)
    bundle = Bundle(ROOT / 'docs/implementation')
    selected = bundle.fixtures['ROUTE-LINE-06'] if family == 'frozen' else fixture(6, family, 'line', '01' * 32)
    metrics = routing(output['payload'], selected,
                      None, bundle.cases['ROUTE-LINE-06'], 0)
    assert metrics['max_semantic_error'] <= bundle.cases['ROUTE-LINE-06']['acceptance']['semantic_atol']
    assert output['audit']['native_compilations'] == 1
    if output['routing_arguments'] is not None:
        strategy = WORKFLOWS[workflow]['options']['routing']
        assert output['routing_arguments'] == [
            {} if strategy == 'default' else {'routing_strategy': strategy}
        ]
    if workflow.endswith('-restored'):
        assert output['payload']['final_layout'] == list(range(6))
        assert output['audit']['restoration_cz_count'] % 3 == 0
    if workflow == 'flagquantum-target-artifact':
        assert output['payload']['final_layout'] == list(range(6))
        assert output['audit']['serialized_artifact_bytes'] > 0
        assert output['audit']['native_baseline_cz_count'] >= sum(
            op['name'] == 'cz' for op in output['payload']['operations'])
