"""Check committed native engineering evidence without importing participant SDKs."""
import gzip
import hashlib
import json
from pathlib import Path
from sdkbench.p0 import Bundle,evaluate

ROOT=Path(__file__).resolve().parents[1]


def test_native_evidence_hashes_scope_and_independent_acceptance():
    folder=ROOT/'docs/implementation/evidence'
    index=json.loads((folder/'index.json').read_text());bundle=Bundle(ROOT/'docs/implementation')
    assert index['publication_eligible'] is False
    for entry in index['archives']:
        encoded=(folder/entry['file']).read_bytes();assert hashlib.sha256(encoded).hexdigest()==entry['sha256']
        files=json.loads(gzip.decompress(encoded))['files']
        assert len(files)==entry['files_verified']+1
        for name,file in files.items():assert hashlib.sha256(file['utf8'].encode()).hexdigest()==file['sha256'],name
        manifest=json.loads(files['MANIFEST.json']['utf8'])
        assert set(manifest['files'])==set(files)-{'MANIFEST.json'}
        for name,sha in manifest['files'].items():assert sha==files[name]['sha256']
        context=json.loads(files['context.json']['utf8']);assert context['source_commit']==entry['source_commit']
        blocks=records=warmups=0
        for name,file in files.items():
            if not name.endswith('/evidence.json'):continue
            block=json.loads(file['utf8']);blocks+=1
            for raw,expected in zip(block['records'],block['record_verdicts']):
                assert evaluate(bundle,raw).status==expected['status'];records+=1
            response=block.get('response')
            if response:
                assert len(response['warmups'])==len(block['warmup_verdicts'])
                for raw,expected in zip(response['warmups'],block['warmup_verdicts']):
                    assert evaluate(bundle,raw).status==expected['status'];warmups+=1
        assert (blocks,records,warmups)==(entry['blocks'],entry['measured_records'],entry['warmups'])
