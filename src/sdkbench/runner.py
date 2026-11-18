"""Serial timing harness with untimed correctness checks and raw measurements."""
from datetime import datetime, timezone
import hashlib
import json
import math
import os
import platform
import statistics
import time

import numpy as np
from .backends import BACKENDS, BackendUnavailable, get_backend
from .circuits import WORKLOADS, make_workload
from .reference import equivalent, simulate

OPERATIONS = ("build", "inverse", "compose", "simulate", "compile")


def summarize(samples):
    """Summarize positive integer nanosecond samples (linear-interpolated p95)."""
    if not samples or any(type(x) is not int or x < 0 for x in samples):
        raise ValueError("Timing samples must be a nonempty list of nonnegative integer nanoseconds")
    ordered = sorted(samples)
    index = .95*(len(ordered)-1)
    low,high = math.floor(index), math.ceil(index)
    p95 = ordered[low] + (ordered[high]-ordered[low])*(index-low)
    return {"min_ns":min(samples), "median_ns":statistics.median(samples),
            "mean_ns":statistics.mean(samples), "max_ns":max(samples),
            "stdev_ns":statistics.stdev(samples) if len(samples)>1 else 0.0, "p95_ns":p95}


def measure(operation, repeats, warmups):
    for _ in range(warmups):
        operation()
    samples = []
    for _ in range(repeats):
        start = time.perf_counter_ns()
        result = operation()
        # Stop before releasing the previous result to avoid timing its destruction.
        elapsed = time.perf_counter_ns()-start
        samples.append(elapsed)
        last = result
        del result
    return last, samples


def _fingerprint(circuit):
    data = [circuit.n_qubits, [[g.name,list(g.qubits),g.angle] for g in circuit.gates]]
    return hashlib.sha256(json.dumps(data,separators=(",", ":")).encode()).hexdigest()


def _probes(n, seed):
    zero = np.zeros(1<<n, dtype=np.complex128); zero[0] = 1
    basis = np.zeros_like(zero); basis[(1<<n)-1] = 1
    rng = np.random.default_rng(seed)
    random_state = rng.normal(size=len(zero)) + 1j*rng.normal(size=len(zero))
    random_state /= np.linalg.norm(random_state)
    return [zero, basis, random_state]


def run_benchmarks(sdks=("reference",), workloads=WORKLOADS, operations=OPERATIONS,
                   n_qubits=8, depth=4, seed=0, repeats=5, warmups=1):
    """Return a JSON-serializable report; never silently discard failed or skipped cases."""
    sdks,workloads,operations = list(sdks),list(workloads),list(operations)
    for values,allowed,label in [(sdks,BACKENDS,"SDK"),(workloads,WORKLOADS,"workload"),(operations,OPERATIONS,"operation")]:
        if not values or len(values)!=len(set(values)) or any(v not in allowed for v in values):
            raise ValueError(f"Select nonempty, unique, supported {label} names")
    if type(repeats) is not int or not 1 <= repeats <= 10000:
        raise ValueError("repeats must be an integer in 1..10000")
    if type(warmups) is not int or not 0 <= warmups <= 1000:
        raise ValueError("warmups must be an integer in 0..1000")
    if type(seed) is not int or not 0 <= seed < 2**32:
        raise ValueError("seed must be an integer in 0..2**32-1")
    circuits = {name:make_workload(name,n_qubits,depth,seed) for name in workloads}
    probes = _probes(n_qubits,seed)
    config = dict(sdks=sdks,workloads=workloads,operations=operations,n_qubits=n_qubits,
                  depth=depth,seed=seed,repeats=repeats,warmups=warmups)
    rows, sdk_info = [], {}
    for name in sdks:
        try:
            backend = get_backend(name)
            sdk_info[name] = {"version":backend.version,"compile_target":backend.compile_target,
                              "role":"oracle" if name=="reference" else "sdk"}
        except Exception as exc:
            status = "skipped" if isinstance(exc,BackendUnavailable) else "error"
            rows.extend({"sdk":name,"workload":w,"operation":op,"status":status,
                         "reason":str(exc)} for w in workloads for op in operations)
            continue
        for workload,spec in circuits.items():
            try:
                native = backend.build(spec)
            except Exception as exc:
                rows.extend({"sdk":name,"workload":workload,"operation":op,"status":"error",
                             "reason":"Initial circuit construction failed: "+str(exc)} for op in operations)
                continue
            for op in operations:
                row = {"sdk":name,"workload":workload,"operation":op,"n_qubits":n_qubits,
                       "circuit_sha256":_fingerprint(spec),"input_gates":len(spec.gates)}
                try:
                    if op == "build": operation = lambda: backend.build(spec)
                    elif op == "inverse": operation = lambda: backend.inverse(native)
                    elif op == "compose": operation = lambda: backend.compose(native)
                    elif op == "simulate": operation = lambda: backend.simulate(native,n_qubits)
                    else: operation = lambda: backend.compile(native,seed)
                    result,samples = measure(operation,repeats,warmups)
                    row["samples_ns"],row["timing"] = samples,summarize(samples)
                    expected_spec = spec.inverse() if op=="inverse" else spec.compose(spec) if op=="compose" else spec
                    valid = True
                    for i,probe in enumerate(probes):
                        actual = result if op=="simulate" and i==0 else backend.simulate(
                            native if op=="simulate" else result,n_qubits,probe)
                        valid = equivalent(actual,simulate(expected_spec,probe)) and valid
                    row["status"] = "passed" if valid else "failed"
                    row["validation"] = {"passed":valid,"probe_count":len(probes),"atol":1e-8,
                                         "method":"statevector agreement up to global phase"}
                    if op != "simulate": row["output_metrics"] = backend.metrics(result)
                    if not valid: row["reason"] = "Output disagrees with the reference oracle"
                except NotImplementedError as exc:
                    row.update(status="skipped",reason=str(exc))
                except Exception as exc:
                    row.update(status="error",reason=type(exc).__name__+": "+str(exc))
                rows.append(row)
    from . import __version__
    return {"schema_version":1,"sdkbench_version":__version__,
            "created_at":datetime.now(timezone.utc).isoformat(),"config":config,
            "environment":{"python":platform.python_version(),"platform":platform.platform(),
                           "machine":platform.machine(),"processor":platform.processor(),
                           "logical_cpus":os.cpu_count(),"numpy":np.__version__,
                           "thread_environment":{k:os.environ[k] for k in
                            ("OMP_NUM_THREADS","OPENBLAS_NUM_THREADS","MKL_NUM_THREADS","RAYON_NUM_THREADS") if k in os.environ}},
            "sdks":sdk_info,"results":rows,
            "summary":{s:sum(row["status"]==s for row in rows) for s in ("passed","failed","skipped","error")}}
