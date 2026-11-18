"""Replay committed real P1b evidence without importing participant SDKs."""
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path
from sdkbench.p0 import Bundle, Registration, evaluate, evaluate_case, evaluate_workflow

ROOT = Path(__file__).resolve().parents[1]


def test_archived_native_full_protocol_and_capability_gaps():
    folder = ROOT/'docs/implementation/evidence';bundle = Bundle(ROOT/'docs/implementation')
    index = json.loads((folder/'p1b-index.json').read_text())
    assert index['publication_eligible'] is False
    for entry in index['archives']:
        encoded = (folder/entry['file']).read_bytes()
        assert hashlib.sha256(encoded).hexdigest() == entry['sha256']
        files = json.loads(gzip.decompress(encoded))['files']
        for name, file in files.items():
            assert hashlib.sha256(file['utf8'].encode()).hexdigest() == file['sha256'], name
        manifest = json.loads(files['MANIFEST.json']['utf8'])
        assert set(manifest['files']) == set(files) - {'MANIFEST.json'}
        assert len(manifest['files']) == entry['files_verified']
        for name, sha in manifest['files'].items():assert sha == files[name]['sha256']
        def read(name):return json.loads(files[name]['utf8'])
        context = read('context.json');assert context['source_commit'] == entry['source_commit']
        assert context['scope'] == 'all-protocol'
        report = read('all-protocol/report.json')
        registrations = {sdk: Registration(**raw) for sdk,raw in read('all-protocol/registrations.json').items()}
        assert set(report['sdks']) == {'flagquantum','qiskit','cirq'}
        assert len(report['instances']) == 8 and not report['unselected_instances']
        blocks = measured = warmups = 0;groups = {};statuses = Counter()
        for name in files:
            if not name.endswith('/evidence.json'):continue
            evidence = read(name);blocks += 1;sdk = evidence['sdk'];instance = evidence['instance']
            identity = registrations[sdk].identity(bundle, instance)
            assert len(evidence['records']) == len(evidence['record_verdicts']) == 3
            for record, stored in zip(evidence['records'], evidence['record_verdicts']):
                assert evaluate(bundle, record, identity).status == stored['status'];measured += 1
                groups.setdefault((sdk,instance), []).append(record)
                if instance.startswith('GRAD') and record['status'] == 'completed':
                    assert 'native_bindings' not in record['measurements']
                    assert record['measurements']['native_primal_calls'] == record['measurements']['native_derivative_calls'] == 1
                if record['status'] != 'completed':assert record['payload'] is None and not record['measurements']
            response = evidence.get('response')
            if response:
                assert len(response['warmups']) == len(evidence['warmup_verdicts']) == 2
                for record, stored in zip(response['warmups'], evidence['warmup_verdicts']):
                    assert evaluate(bundle, record, identity).status == stored['status'];warmups += 1
            execution = evidence.get('execution')
            if execution:
                assert execution['limits']['memory_bytes'] == 16 * 1024**3
                assert 0 < execution['limits']['wall_seconds'] <= bundle.cases[instance]['case_wall_limit_seconds']
                assert execution['network_policy'] == 'seccomp-deny-sockets-and-io-uring'
        for row in report['outcomes']:
            sdk = row['sdk'];instance = row['instance'];records = groups[sdk,instance]
            assert len(records) == 30
            verdict = evaluate_case(bundle, registrations[sdk].identity(bundle, instance), records)
            assert verdict.status == row['case_verdict']['status']
            statuses[verdict.status] += 1
        for sdk in registrations:
            for workflow, stored in report['workflows'][sdk].items():
                records = [r for (s,i), rows in groups.items() if s == sdk and bundle.cases[i]['workflow'] == workflow for r in rows]
                assert evaluate_workflow(bundle, workflow, records).status == stored['status']
        assert (blocks, measured, warmups) == (entry['blocks'], entry['measured_records'], entry['warmups'])
        assert dict(statuses) == entry['case_status_counts']
        assert blocks == 240 and measured == 720
        alarm = read('compile-deadline-check.json')
        assert alarm['returncode'] == -14 and alarm['execution_status'] == 'error'
        assert alarm['network_policy'] == 'seccomp-deny-sockets-and-io-uring'
