"""Independently replay saved local issue-reproducer outputs without any SDK imports."""
import json
from pathlib import Path
import numpy as np
from sdkbench.p0 import Bundle
from sdkbench.p0.evaluators import routing
from sdkbench.p0.semantics import propagate,equivalent
from sdkbench.diagnostics.routing import micro_fixtures

ROOT=Path(__file__).resolve().parents[1]


def test_local_pair_reproducer_saved_full_operators():
    reference=[{'name':'cx','qubits':q} for q in ([0,1],[1,0],[0,1],[1,0])]
    target=propagate(2,reference,np.eye(4,dtype=complex))
    for filename in ('local-pair-release.json','local-pair-upstream.json'):
        data=json.loads((ROOT/'docs/analysis/source-probes'/filename).read_text())
        assert data['post_basis_optimization'] and 'no cgroup' in data['scope']
        assert [r['full_cz_count'] for r in data['outcomes']]==[4,2]
        for row in data['outcomes']:
            assert row['final_layout']==[0,1]
            actual=propagate(2,row['output_operations'],np.eye(4,dtype=complex),target_edges={frozenset([0,1])})
            equivalent(actual,target,1e-8,1e-10)
            assert row['full_cz_count']==sum(op['name']=='cz' for op in row['output_operations'])


def test_upstream_six_qubit_probe_is_separate_and_correct():
    data=json.loads((ROOT/'docs/analysis/source-probes/upstream-full-operator.json').read_text())
    inspected=json.loads((ROOT/'docs/analysis/source-probes/inspection.json').read_text())
    assert data['git_sha']==inspected['upstream_commit']
    assert data['sdk_version']==inspected['upstream_version']=='0.4.0'
    assert 'not the registered' in data['scope']
    bundle=Bundle(ROOT/'docs/implementation');fixtures=micro_fixtures(bundle.fixtures['ROUTE-LINE-06'])
    for row in data['outcomes']:
        actual=routing(row['payload'],fixtures[row['input_id']],None,bundle.cases['ROUTE-LINE-06'],0)
        assert actual['full_cz_count']==row['validation']['full_cz_count']
        assert actual['verification']=='full-operator'
