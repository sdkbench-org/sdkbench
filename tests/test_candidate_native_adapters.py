"""Opt-in native adapter conformance, not a resource-qualified campaign."""
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest

from sdkbench.candidates.adapters import WORKFLOWS
from sdkbench.p0 import Bundle
from sdkbench.p0.evaluators import routing

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.skipif(os.environ.get('SDKBENCH_NATIVE_CANDIDATE_TESTS') != '1',
                    reason='Explicit native candidate environment required')
@pytest.mark.parametrize('workflow', tuple(WORKFLOWS))
def test_native_workflow_satisfies_independent_arbitrary_input_semantics(workflow):
    script = r'''
import json
from types import SimpleNamespace
from pathlib import Path
from sdkbench.candidates.adapters import load_adapter, workflow_configuration
from sdkbench.p0 import Bundle
import sys
workflow = sys.argv[1]
config = workflow_configuration(workflow)
registration = SimpleNamespace(configuration={'options': {
    'sdk': config['sdk'], 'workflow': workflow, 'compiler_options': config}})
bundle = Bundle(sys.argv[2])
adapter = load_adapter(registration)
payload = adapter.execute('route', bundle.fixtures['ROUTE-LINE-06'],
                          bundle.plan['execution_profile']['compiler_seeds'][0])
print(json.dumps({'payload': payload, 'audit': adapter.audit}))
'''
    result = subprocess.run([sys.executable, '-c', script, workflow, str(ROOT / 'docs/implementation')],
                            capture_output=True, text=True, timeout=150)
    assert result.returncode == 0, result.stderr
    output = json.loads(result.stdout)
    bundle = Bundle(ROOT / 'docs/implementation')
    metrics = routing(output['payload'], bundle.fixtures['ROUTE-LINE-06'],
                      None, bundle.cases['ROUTE-LINE-06'], 0)
    assert metrics['max_semantic_error'] <= bundle.cases['ROUTE-LINE-06']['acceptance']['semantic_atol']
    assert output['audit']['native_compilations'] == 1
    if workflow == 'flagquantum-target-artifact':
        assert output['payload']['final_layout'] == list(range(6))
        assert output['audit']['serialized_artifact_bytes'] > 0
        assert output['audit']['native_baseline_cz_count'] >= sum(
            op['name'] == 'cz' for op in output['payload']['operations'])
