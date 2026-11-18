"""One fresh process block: import one SDK, then warmups and measured outcomes."""
import argparse
import contextlib
from importlib import metadata
import sys
import time
import traceback
import warnings
from ..p0.models import Identity, ResultRecord, canonical_bytes, digest, read_json, require
from .common import DISTRIBUTIONS, VERSIONS, UnsupportedCapability, load_adapter


def failure(identity, block, repetition, status, exc):
    return ResultRecord(identity, block, repetition, status, reason=f'{type(exc).__name__}: {exc}').to_dict()


def exception_status(exc):
    if isinstance(exc, (ModuleNotFoundError, ImportError, metadata.PackageNotFoundError)):return 'install-failed'
    if isinstance(exc, UnsupportedCapability):return 'unsupported'
    if isinstance(exc, NotImplementedError):return 'unsupported'
    if isinstance(exc, MemoryError):return 'out-of-memory'
    return 'error'


def execute_block(sdk, request):
    require(sdk in DISTRIBUTIONS, 'Unknown SDK')
    identity = Identity(**request['identity']); block = request['block']; mode = request['execution_mode']
    require(identity.stack_id == sdk and mode in ('protocol', 'qualification'), 'Worker registration/mode mismatch')
    kind = request['kind']; stochastic = kind == 'sampling'
    warmup_count = 2 if mode == 'protocol' and not stochastic else 0
    repetition_count = 3 if mode == 'protocol' and not stochastic else 1
    measured = []; warmups = []; audits = []; import_started = time.perf_counter(); import_error = None; adapter = None
    with warnings.catch_warnings(record=True) as caught, contextlib.redirect_stdout(sys.stderr):
        warnings.simplefilter('always')
        try:
            actual = metadata.version(DISTRIBUTIONS[sdk])
            require(actual == VERSIONS[sdk], f'Pinned SDK version mismatch: expected {VERSIONS[sdk]}, found {actual}')
            adapter = load_adapter(sdk)
        except Exception as exc:
            import_error = exc; traceback.print_exc(file=sys.stderr)
        import_seconds = time.perf_counter() - import_started
        for phase, count, records in [('warmup', warmup_count, warmups), ('measured', repetition_count, measured)]:
            for repetition in range(count):
                if import_error is not None:
                    records.append(failure(identity, block, repetition, exception_status(import_error), import_error)); continue
                started = time.perf_counter()
                try:
                    payload = adapter.execute(kind, request['fixture'], request['sampling_seeds'][0])
                    elapsed = time.perf_counter() - started
                    result = ResultRecord(identity, block, repetition, 'completed', payload,
                                          measurements={'outcome_wall_seconds': elapsed, **adapter.audit})
                    records.append(result.to_dict()); audits.append({'phase': phase, 'repetition': repetition, **adapter.audit})
                except Exception as exc:
                    traceback.print_exc(file=sys.stderr)
                    records.append(failure(identity, block, repetition, exception_status(exc), exc))
    return {'schema_version': 1, 'request_sha256': digest(request), 'sdk': sdk, 'sdk_version': actual if 'actual' in locals() else None,
            'worker_pid': __import__('os').getpid(), 'sdk_import_wall_seconds': import_seconds,
            'warmups': warmups, 'records': measured, 'native_audit': audits,
            'warnings': [{'category': x.category.__name__, 'message': str(x.message)} for x in caught]}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument('--sdk', required=True, choices=tuple(DISTRIBUTIONS))
    parser.add_argument('request'); args = parser.parse_args(argv)
    try:
        response = execute_block(args.sdk, read_json(args.request))
        print(canonical_bytes(response).decode(), end=''); return 0
    except Exception:
        traceback.print_exc(file=sys.stderr); return 2


if __name__ == '__main__':raise SystemExit(main())
