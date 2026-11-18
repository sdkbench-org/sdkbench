"""Replay native artifacts independently and reject resealed provenance tampering."""
import gzip
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

import pytest

from sdkbench.p0 import Bundle
from sdkbench.p0.models import canonical_bytes, digest

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope='module')
def evidence(tmp_path_factory):
    root = tmp_path_factory.mktemp('routing-archive')
    index = json.loads((ROOT/'docs/analysis/evidence/index.json').read_text())['archives'][0]
    encoded = (ROOT/'docs/analysis/evidence'/index['file']).read_bytes()
    assert hashlib.sha256(encoded).hexdigest() == index['sha256']
    files = json.loads(gzip.decompress(encoded))['files']
    for name, entry in files.items():
        path = (root/name).resolve()
        assert path.is_relative_to(root)
        content = entry['utf8'].encode()
        assert hashlib.sha256(content).hexdigest() == entry['sha256']
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
    return root


@pytest.fixture(scope='module')
def replay():
    sys.path.insert(0, str(ROOT/'tools'))
    try:
        spec = importlib.util.spec_from_file_location('routing_replay', ROOT/'tools/routing_evidence.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        yield module
    finally:
        sys.path.remove(str(ROOT/'tools'))


def test_full_independent_archive_replay(evidence, replay):
    actual = replay.verify(evidence, Bundle(ROOT/'docs/implementation'))
    assert actual['files_verified'] == 798
    assert actual['outcomes_verified'] == 264
    assert actual['status_counts'] == {'accepted': 264}
    assert not actual['publication_eligible']
    summary = json.loads((ROOT/'docs/analysis/routing-summary.json').read_text())
    profile = json.loads((evidence/'profile.json').read_text())
    assert digest(profile) == summary['profile_sha256']
    assert len(summary['baseline_reproduction']) == 36
    assert all(row['matches'] for row in summary['baseline_reproduction'])
    for row in summary['default_route_derivation']:
        assert row['retained_swaps'] == 2 * row['sum_distance_minus_one']
        assert row['input_cx'] + 3 * row['retained_swaps'] == row['observed_cz']
        native = next(r for r in actual['flagquantum_lowering_arithmetic']
                      if r['variant'] == 'fq-default' and r['input_id'] == row['input_id'])
        assert native['swap'] == row['retained_swaps']
        assert native['first_basis_cz'] == row['observed_cz']


@pytest.mark.parametrize('tamper', ['hash', 'registration', 'frozen-layout'])
def test_reject_changed_evidence_even_with_resealed_hashes(evidence, replay, tamper):
    manifest_path = evidence/'MANIFEST.json'
    old_manifest = manifest_path.read_bytes()
    name = ('registrations.json' if tamper != 'frozen-layout' else
            'runs/cirq-default/ROUTE-LINE-06/seed-00/request.json')
    path = evidence/name
    original = path.read_bytes()
    try:
        value = json.loads(original)
        if tamper == 'frozen-layout':
            value['fixture']['initial_layout'] = 'free'
            value['fixture_sha256'] = digest(value['fixture'])
        else:
            value['cirq-default']['configuration']['options']['variant']['level'] = 99
        path.write_bytes(canonical_bytes(value))
        if tamper != 'hash':
            manifest = json.loads(old_manifest)
            manifest['files'][name] = hashlib.sha256(path.read_bytes()).hexdigest()
            manifest_path.write_bytes(canonical_bytes(manifest))
        message = {'hash': 'File hash mismatch', 'registration': 'Registration configuration mismatch',
                   'frozen-layout': 'Frozen input modified'}[tamper]
        with pytest.raises(ValueError, match=message):
            replay.verify(evidence, Bundle(ROOT/'docs/implementation'))
    finally:
        path.write_bytes(original)
        manifest_path.write_bytes(old_manifest)
