"""One isolated native routing diagnostic, with no reference output in its request."""
import contextlib
from importlib import metadata
import os
import sys
import time
import traceback
from ..p0.models import canonical_bytes,digest,read_json,require
from ..p1a.common import DISTRIBUTIONS,VERSIONS,load_adapter
from ..p1a.worker import exception_status
from .routing import compile_variant


def run(request):
    adapter=None;started=time.perf_counter()
    response={'schema_version':1,'request_sha256':digest(request),'worker_pid':os.getpid()}
    with contextlib.redirect_stdout(sys.stderr):
        try:
            sdk=request['config']['sdk'];actual=metadata.version(DISTRIBUTIONS[sdk])
            require(actual==VERSIONS[sdk],'Pinned SDK version mismatch')
            adapter=load_adapter(sdk);response['import_wall_seconds']=time.perf_counter()-started
            payload,trace=compile_variant(adapter,request['fixture'],request['config'],request['seed'])
            response.update(status='completed',payload=payload,trace=trace,reason=None)
        except Exception as exc:
            traceback.print_exc(file=sys.stderr)
            response.update(status=exception_status(exc),payload=None,reason=f'{type(exc).__name__}: {exc}',
                            trace=getattr(adapter,'diagnostic_trace',None))
    return response


if __name__=='__main__':print(canonical_bytes(run(read_json(sys.argv[1]))).decode(),end='')
