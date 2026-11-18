"""Synthetic adverse evidence tests for the independent P1b replay tool."""
from dataclasses import asdict
import hashlib
import json
from pathlib import Path
import pytest
from sdkbench.p0 import Bundle
from sdkbench.p0.models import ContractError, canonical_bytes, read_json
from sdkbench.p1a import campaign
from test_p1a_runner import synthetic_setup

ROOT = Path(__file__).resolve().parents[1]


def seal(root):
    files = {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
             for p in root.rglob('*') if p.is_file() and p.name != 'MANIFEST.json'}
    (root/'MANIFEST.json').write_bytes(canonical_bytes({'files': files}))


def test_replay_preserves_unsupported_and_rejects_false_registration(monkeypatch, tmp_path):
    monkeypatch.syspath_prepend(str(ROOT/'tools'))
    from p1b_evidence import verify_cases
    bundle = Bundle(ROOT/'docs/implementation');synthetic_setup(monkeypatch, bundle)
    original = campaign.run_command
    def synthetic_run(argv, **kwargs):
        execution = original(argv, **kwargs)
        execution.update(limits=asdict(kwargs['limits']), network_policy='seccomp-deny-sockets-and-io-uring')
        response = json.loads(execution['stdout'])
        if read_json(argv[-1])['kind'] == 'gradient':
            for record in response['records'] + response['warmups']:
                record.update(status='unsupported', payload=None, measurements={}, reason='Synthetic missing feature')
            execution['stdout'] = json.dumps(response)
        return execution
    monkeypatch.setattr(campaign, 'run_command', synthetic_run)
    root = tmp_path/'raw';root.mkdir()
    (root/'context.json').write_bytes(canonical_bytes({'source_commit': 'synthetic-only'}))
    campaign.run_campaign(bundle, directory=root/'small-protocol', cgroup_parent=tmp_path, cpu=0, suite='p1b',
                          sdks=('cirq',), instances=['GRAD-04','DYN-04-S32','ROUTE-LINE-06'])
    seal(root);summary = verify_cases(root, bundle)
    assert summary['blocks_verified'] == 30
    assert [c['status'] for c in summary['cases_verified']] == ['unsupported','accepted','accepted']
    registrations_path = root/'small-protocol/registrations.json'
    registrations = read_json(registrations_path)
    registrations['cirq']['configuration']['options']['tampered'] = True
    registrations_path.write_bytes(canonical_bytes(registrations));seal(root)
    with pytest.raises(ContractError, match='registration binding mismatch'):verify_cases(root, bundle)
