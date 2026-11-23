"""CPU-only protocol tests. GPU adapter coverage is a separate smoke experiment."""
import copy
import importlib.util
import json
from pathlib import Path
import sys

import numpy as np
import pytest

TOOLS = Path(__file__).resolve().parents[1] / 'tools'
sys.path.insert(0, str(TOOLS))
spec = importlib.util.spec_from_file_location('gpu_phases', TOOLS / 'gpu_phases.py')
phases = importlib.util.module_from_spec(spec)
spec.loader.exec_module(phases)


def test_primary_has_no_per_stage_barriers():
    calls = []
    rec = phases.Recorder('primary', lambda: calls.append('sync'))
    assert rec.call('forward', lambda: 42) == 42
    assert calls == []
    assert rec.stages['forward']['seconds'] is None


def test_diagnostic_completed_wall_interval():
    calls, ticks = [], iter([5., 7.])
    rec = phases.Recorder('diagnostic', lambda: calls.append('sync'), lambda: next(ticks))
    rec.call('forward', lambda: calls.append('forward'))
    assert calls == ['sync', 'forward', 'sync']
    assert rec.stages['forward'] == dict(status='measured', seconds=2.,
                                       clock='host_wall_completed', additive=False)


def test_failure_does_not_manufacture_a_completed_stage():
    rec = phases.Recorder('diagnostic', lambda: None)
    with pytest.raises(RuntimeError):
        rec.call('forward', lambda: (_ for _ in ()).throw(RuntimeError('failure')))
    assert rec.stages['forward']['seconds'] is None


def valid_record():
    return dict(protocol=phases.PROTOCOL, track='primary', request_wall_seconds=.1,
                stages=phases.Recorder('primary', lambda: None).stages)


@pytest.mark.parametrize('value', [0, float('nan'), False])
def test_missing_stage_cannot_be_replaced_by_number(value):
    record = valid_record()
    record['stages']['forward']['seconds'] = value
    with pytest.raises(ValueError):
        phases.check_record(record)


def test_complete_schema_and_primary_track_separation():
    record = valid_record()
    phases.check_record(record)
    record['stages']['forward'] = dict(status='measured', seconds=.01,
                                      clock='host_wall_completed', additive=False)
    with pytest.raises(ValueError):
        phases.check_record(record)
    record['track'] = 'diagnostic'
    phases.check_record(record)
    bad = copy.deepcopy(record)
    bad['stages']['forward']['additive'] = True
    with pytest.raises(ValueError):
        phases.check_record(bad)
    record['stages'].pop('h2d')
    with pytest.raises(ValueError):
        phases.check_record(record)


def test_parameter_shift_against_finite_difference():
    ops = phases.operations(2, 2, 41)
    actual = phases.gradient_reference(2, ops)
    finite_difference = []
    for index, (_, _, angle) in enumerate(ops):
        if angle is None:
            continue
        plus, minus = phases.shifted_ops(ops, 0), phases.shifted_ops(ops, 0)
        plus[index][2] += 1e-5
        minus[index][2] -= 1e-5
        finite_difference.append((phases.loss(phases.reference(2, plus)) -
                                  phases.loss(phases.reference(2, minus))) / 2e-5)
    np.testing.assert_allclose(actual, finite_difference, atol=1e-9, rtol=1e-8)


def test_z0_loss_uses_most_significant_qubit():
    assert phases.loss(np.array([0, 1, 0, 0], dtype=complex)) == 1
    assert phases.loss(np.array([0, 0, 1, 0], dtype=complex)) == -1


def test_published_catalog_matches_collector_without_measurements():
    catalog = json.loads((TOOLS.parent / 'docs/implementation/gpu-phases-protocol.json').read_text())
    assert catalog['protocol'] == phases.PROTOCOL
    assert {s['id'] for s in catalog['stages']} == set(phases.STAGES) | {'startup'}
    assert tuple(s['id'] for s in catalog['scenarios']) == phases.SCENARIOS
    assert all(s['results'] is None and s['status'] == 'not_run' for s in catalog['scenarios'])
    assert all(s['seconds'] is None for s in catalog['stages'])


def test_oracle_cache_pins_input_bytes_and_detects_corruption(tmp_path):
    ops = phases.operations(2, 1, 41)
    key = phases.oracle_key(2, ops)
    assert key != phases.oracle_key(2, phases.shifted_ops(ops, .007))
    assert key != phases.oracle_key(3, ops)
    path = tmp_path / (key + '.npz')
    state, gradient = phases.reference(2, ops), phases.gradient_reference(2, ops)
    np.savez(path, state=state, gradient=gradient)
    (tmp_path / 'index.json').write_text(json.dumps({key:dict(sha256=phases.sha(path),bytes=path.stat().st_size)}))
    actual, deriv = phases.cached_oracle(tmp_path, 2, ops, True)
    np.testing.assert_array_equal(actual, state)
    np.testing.assert_array_equal(deriv, gradient)
    path.write_bytes(path.read_bytes() + b'changed')
    with pytest.raises(ValueError, match='integrity'):
        phases.cached_oracle(tmp_path, 2, ops, True)
