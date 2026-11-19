"""One source-registered compiler block, with admission before SDK import."""
import argparse
import contextlib
from importlib import metadata
import os
from pathlib import Path
import sys
import time
import traceback
import warnings

from ..p0.models import Identity, ResultRecord, canonical_bytes, digest, read_json, require
from ..p0.registration import Registration
from ..p1a.common import DISTRIBUTIONS
from ..p1a.worker import exception_status, failure
from .adapters import load_adapter
from .provenance import file_sha256, verify_runtime


def execute_block(sdk, request):
    require(request['suite'] == 'compiler-candidate' and request['kind'] == 'route',
            'Candidate worker requires a routing request')
    require(request['execution_mode'] in ('protocol', 'qualification'), 'Unknown execution mode')
    registration = Registration(**request['candidate_registration'])
    identity = Identity(**request['identity'])
    require(identity.stack_id == sdk == registration.stack_id
            and identity.configuration_sha256 == registration.configuration_sha256
            and identity.environment_sha256 == registration.environment_sha256,
            'Candidate registration does not match request identity')
    block = request['block']
    protocol = request['execution_mode'] == 'protocol'
    measured, warmups, audits, evidence_files = [], [], [], []
    adapter = None
    admission_error = None
    admission = None
    actual = None
    started = time.perf_counter()
    with warnings.catch_warnings(record=True) as caught, contextlib.redirect_stdout(sys.stderr):
        warnings.simplefilter('always')
        try:
            admission = verify_runtime(registration)
            native_sdk = registration.configuration['options']['sdk']
            actual = metadata.version(DISTRIBUTIONS[native_sdk])
            adapter = load_adapter(registration)
        except Exception as exc:
            admission_error = exc
            traceback.print_exc(file=sys.stderr)
        import_seconds = time.perf_counter() - started
        for phase, count, records in [('warmup', 2 if protocol else 0, warmups),
                                      ('measured', 3 if protocol else 1, measured)]:
            for repetition in range(count):
                if admission_error is not None:
                    records.append(failure(identity, block, repetition,
                                           exception_status(admission_error), admission_error))
                    continue
                started = time.perf_counter()
                try:
                    adapter.native.compiler_evidence = None
                    payload = adapter.execute('route', request['fixture'], request['compiler_seed'])
                    elapsed = time.perf_counter() - started
                    record = ResultRecord(identity, block, repetition, 'completed', payload,
                                          measurements={'outcome_wall_seconds': elapsed, **adapter.audit})
                    evidence = getattr(adapter.native, 'compiler_evidence', None)
                    if evidence is not None:
                        path = Path(f'compiler-evidence-{phase}-{repetition}.json')
                        with path.open('xb') as output:
                            output.write(canonical_bytes(evidence))
                        evidence_files.append({'phase': phase, 'repetition': repetition,
                                               'filename': path.name, 'sha256': file_sha256(path)})
                    records.append(record.to_dict())
                    audits.append({'phase': phase, 'repetition': repetition, **adapter.audit})
                except Exception as exc:
                    traceback.print_exc(file=sys.stderr)
                    records.append(failure(identity, block, repetition, exception_status(exc), exc))
    return {'schema_version': 1, 'request_sha256': digest(request), 'sdk': sdk,
            'sdk_version': actual, 'worker_pid': os.getpid(), 'sdk_import_wall_seconds': import_seconds,
            'warmups': warmups, 'records': measured, 'native_audit': audits,
            'candidate_admission': admission, 'compiler_evidence_files': evidence_files,
            'warnings': [{'category': item.category.__name__, 'message': str(item.message)} for item in caught]}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sdk', required=True)
    parser.add_argument('request')
    args = parser.parse_args(argv)
    response = execute_block(args.sdk, read_json(args.request))
    print(canonical_bytes(response).decode(), end='')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
