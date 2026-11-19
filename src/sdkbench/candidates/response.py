"""Validate candidate admission and retained compiler files independently of SDKs."""
from pathlib import Path

from ..p0.models import keys, read_json, require
from .provenance import file_sha256


def verify_response(registration, response, directory):
    completed = [(phase, index) for phase, records in
                 (('warmup', response['warmups']), ('measured', response['records']))
                 for index, record in enumerate(records) if record['status'] == 'completed']
    if completed:
        frontend = [c for c in registration.components if c['role'] == 'frontend']
        require(len(frontend) == 1 and response['sdk_version'] == frontend[0]['version'],
                'Worker SDK version differs from candidate registration')
        require(response['candidate_admission'] == {
            'configuration_sha256': registration.configuration_sha256,
            'environment_sha256': registration.environment_sha256,
            'independent_attestation': False}, 'Worker did not verify candidate admission')
    artifact_workflow = registration.configuration['options']['workflow'] == 'flagquantum-target-artifact'
    expected = set(completed) if artifact_workflow else set()
    files = response['compiler_evidence_files']
    require(isinstance(files, list), 'Compiler evidence files must be a list')
    seen = set()
    for item in files:
        keys(item, ('phase', 'repetition', 'filename', 'sha256'))
        key = (item['phase'], item['repetition'])
        require(key in expected and key not in seen, 'Unexpected or duplicate compiler evidence')
        expected_name = f'compiler-evidence-{key[0]}-{key[1]}.json'
        require(item['filename'] == expected_name, 'Compiler evidence path mismatch')
        path = Path(directory) / expected_name
        require(not path.is_symlink() and path.is_file(), 'Compiler evidence missing or symlinked')
        require(file_sha256(path) == item['sha256'], 'Compiler evidence file hash mismatch')
        evidence = read_json(path)
        keys(evidence, ('executable_artifact', 'target_snapshot_id'))
        require(isinstance(evidence['executable_artifact'], str) and evidence['executable_artifact'],
                'Missing serialized compiler artifact')
        require(isinstance(evidence['target_snapshot_id'], str) and len(evidence['target_snapshot_id']) == 64,
                'Missing compiler target snapshot identity')
        seen.add(key)
    require(seen == expected, 'Missing compiler evidence for completed outcomes')
