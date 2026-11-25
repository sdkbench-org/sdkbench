"""Scope selection must not substitute qualification for full-case measurement."""
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('p1a_integration_driver', ROOT / 'tools/p1a_integration.py')
driver = importlib.util.module_from_spec(spec)
spec.loader.exec_module(driver)


def invoke(monkeypatch, tmp_path, scope, verdict='accepted'):
    calls = []
    def campaign(bundle, **kwargs):
        calls.append(kwargs)
        return dict(mode=kwargs['mode'], outcomes=[dict(qualification_status='accepted',
                    case_verdict=dict(status=verdict))], workflows={}, scope='engineering', unselected_instances=[])
    monkeypatch.setattr(driver, 'run_campaign', campaign)
    monkeypatch.setattr(driver.os, 'sched_getaffinity', lambda _: {0}, raising=False)
    code = driver.main(['--bundle', str(ROOT / 'docs/implementation'), '--directory', str(tmp_path / 'evidence'),
                        '--cgroup-parent', str(tmp_path / 'cgroups'), '--scope', scope])
    return code, calls, json.loads((tmp_path / 'evidence/context.json').read_text())


def test_all_protocol_does_not_run_qualification_or_limit_instances(monkeypatch, tmp_path):
    code, calls, context = invoke(monkeypatch, tmp_path, 'all-protocol')
    assert code == 0 and len(calls) == 1
    assert calls[0]['mode'] == 'protocol' and 'instances' not in calls[0]
    assert context['scope'] == 'all-protocol' and context['publication_eligible'] is False


def test_legacy_all_retains_two_distinct_scopes(monkeypatch, tmp_path):
    code, calls, _ = invoke(monkeypatch, tmp_path, 'all')
    assert code == 0 and [c['mode'] for c in calls] == ['qualification', 'protocol']
    assert calls[1]['instances'] == ['PARAM-04','OBS-04','SAMPLE-03','SAMPLE-05']


def test_failed_full_case_exits_unsuccessfully_even_with_accepted_qualification(monkeypatch, tmp_path):
    code, _, _ = invoke(monkeypatch, tmp_path, 'all-protocol', verdict='not-measured')
    assert code == 1
