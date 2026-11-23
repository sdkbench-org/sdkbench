#!/usr/bin/env python3
"""GPU phase protocol v2. Engineering collector, independent of the sealed v1 runner."""
from __future__ import annotations

import argparse
from contextlib import nullcontext
import importlib.metadata
import json
import math
from pathlib import Path
import subprocess
import sys
import time

from gpu_statevector import CuStateVec, operations, reference, sha, write

PROTOCOL = 'gpu-phases-v2'
SCENARIOS = ('first_request', 'repeated_fixed', 'parameter_update',
             'differentiable_forward', 'gradient', 'training_step')
GRAD_SCENARIOS = SCENARIOS[3:]
STAGES = ('construction_binding', 'execution_preparation', 'state_initialization',
          'h2d', 'forward', 'output', 'd2h', 'backward', 'optimizer', 'cleanup')


def unavailable(status, reason):
    return dict(status=status, seconds=None, reason=reason)


def loss(state):
    """<Z_0>, qubit zero is the most significant bit; real scalar output."""
    import numpy as np
    probabilities = np.abs(state.reshape(-1)) ** 2
    half = probabilities.size // 2
    return float(probabilities[:half].sum() - probabilities[half:].sum())


def shifted_ops(ops, offset):
    return [[name, wires[:], None if angle is None else angle + offset]
            for name, wires, angle in ops]


def gradient_reference(n, ops):
    """Independent two-term parameter-shift oracle, one angle per rotation."""
    import numpy as np
    result = []
    for i, (_, _, angle) in enumerate(ops):
        if angle is None:
            continue
        plus, minus = shifted_ops(ops, 0), shifted_ops(ops, 0)
        plus[i][2] += math.pi / 2
        minus[i][2] -= math.pi / 2
        result.append((loss(reference(n, plus)) - loss(reference(n, minus))) / 2)
    return np.array(result, dtype=np.float64)


class Recorder:
    """Diagnostic barriers are never inserted into the primary request track."""
    def __init__(self, track, sync, clock=time.perf_counter):
        self.track, self.sync, self.clock = track, sync, clock
        self.stages = {key: unavailable('not_measured', 'Primary track has no stage barriers')
                       for key in STAGES}

    def call(self, key, function):
        if self.track == 'primary':
            return function()
        self.sync()
        start = self.clock()
        result = function()
        self.sync()
        self.stages[key] = dict(status='measured', seconds=self.clock() - start,
                                clock='host_wall_completed', additive=False)
        return result


def check_record(record):
    """Reject missing/zero substitutions and incomplete or mislabelled timings."""
    if record['protocol'] != PROTOCOL or set(record['stages']) != set(STAGES):
        raise ValueError('Invalid protocol/stage set')
    if record['track'] not in ('primary', 'diagnostic'):
        raise ValueError('Invalid track')
    statuses = {'measured', 'not_measured', 'not_observable', 'not_applicable', 'error'}
    for stage in record['stages'].values():
        status, value = stage['status'], stage['seconds']
        if status not in statuses:
            raise ValueError('Invalid stage status')
        if status == 'measured':
            if (record['track'] != 'diagnostic' or isinstance(value, bool)
                    or not isinstance(value, (int, float)) or not math.isfinite(value)
                    or value < 0 or stage.get('additive') is not False
                    or stage.get('clock') != 'host_wall_completed'):
                raise ValueError('Invalid measured stage')
        elif value is not None or not stage.get('reason'):
            raise ValueError('Unmeasured stage must be null with a reason')
    total = record['request_wall_seconds']
    if isinstance(total, bool) or not isinstance(total, (int, float)) or not math.isfinite(total) or total < 0:
        raise ValueError('Invalid complete request timing')


class Adapter:
    def __init__(self, participant, n, torch, cp, fq=None):
        self.participant, self.n = participant, n
        self.torch, self.cp, self.fq = torch, cp, fq
        self.executor = self.circuit = self.theta = self.state = self.objective = None

    def build(self, ops, grad=False):
        self.ops = ops
        if self.participant == 'custatevec':
            self.executor = CuStateVec(self.n, ops)
            return
        torch = self.torch
        angles = [angle for _, _, angle in ops if angle is not None]
        # Independent scalar leaf parameters; no hidden binding/reuse claim.
        self.theta = [torch.tensor(a, device='cuda', dtype=torch.float64,
                                   requires_grad=grad) for a in angles]
        self.circuit = self.fq.Circuit(self.n, device='cuda', dtype=torch.complex128)
        index = 0
        for name, wires, angle in ops:
            if angle is None:
                self.circuit.cx(*wires)
            else:
                getattr(self.circuit, name)(wires[0], self.theta[index])
                index += 1

    def forward(self):
        if self.executor:
            executor = self.executor
            for matrix, target, controls in executor.items:
                executor.cv.apply_matrix(executor.handle, self.state.data.ptr, 5, self.n,
                    matrix.data.ptr, 5, executor.cv.MatrixLayout.ROW, 0, [target], 1,
                    controls, [1] * len(controls), len(controls),
                    executor.cv.ComputeType.COMPUTE_64F,
                    executor.workspace.ptr if executor.workspace else 0, executor.workspace_bytes)
        else:
            self.state = self.circuit.state(refresh=True)

    def initialize(self):
        self.state = self.cp.zeros(1 << self.n, dtype=self.cp.complex128)
        self.state[0] = 1

    def output(self, grad):
        if grad:
            values = self.state.reshape(-1)
            half = values.numel() // 2
            probabilities = values.abs().square()
            self.objective = probabilities[:half].sum() - probabilities[half:].sum()

    def backward(self):
        self.objective.backward()

    def optimize(self, rate):
        with self.torch.no_grad():
            for parameter in self.theta:
                parameter.add_(parameter.grad, alpha=-rate)

    def download(self, grad):
        if self.executor:
            state = self.cp.asnumpy(self.state).reshape(-1)
        else:
            state = self.state.detach().cpu().numpy().reshape(-1).copy()
        self.host = dict(state=state)
        if grad:
            import numpy as np
            self.host['loss'] = self.objective.detach().cpu().numpy().copy()
            self.host['parameters'] = np.array([p.detach().item() for p in self.theta])
            if self.theta[0].grad is not None:
                self.host['gradient'] = np.array([p.grad.item() for p in self.theta])

    def close(self):
        if self.executor:
            self.executor.close()
        self.executor = self.circuit = self.theta = self.state = self.objective = None


def worker(args):
    startup = time.perf_counter()
    import numpy as np
    import torch
    import cupy as cp
    fq = None
    cv = None
    if args.participant == 'flagquantum':
        import flagquantum as fq
    else:
        from cuquantum.bindings import custatevec as cv
    if not torch.cuda.is_available() or torch.cuda.device_count() != 1:
        raise RuntimeError('Exactly one visible CUDA GPU required; no fallback')
    torch.set_num_threads(1)
    torch.set_num_interop_threads(1)

    def sync():
        torch.cuda.synchronize()
        cp.cuda.Stream.null.synchronize()

    sync()
    startup_seconds = time.perf_counter() - startup
    adapter = Adapter(args.participant, args.qubits, torch, cp, fq)
    base_ops = operations(args.qubits, args.layers, args.seed)
    grad = args.scenario in GRAD_SCENARIOS
    reusable = args.scenario == 'repeated_fixed'
    context = (torch.enable_grad if grad else {'default': nullcontext,
               'no_grad': torch.no_grad, 'inference': torch.inference_mode}[args.grad_mode])
    count = 1 if args.scenario == 'first_request' else args.warmups + args.measured
    records = []
    args.output.mkdir(parents=True, exist_ok=False)
    write(args.output / 'environment.json', dict(
        protocol=PROTOCOL, startup_import_context_seconds=startup_seconds,
        startup_scope='worker imports (NumPy, Torch, CuPy, participant) and CUDA context; excludes interpreter launch',
        python=sys.version, device=torch.cuda.get_device_name(0), cuda=torch.version.cuda,
        torch_runtime=torch.__version__,
        custatevec_native_version=cv.get_version() if cv is not None else None,
        # Multiple dist-info directories can coexist. Preserve that fact rather
        # than silently letting enumeration order choose a reported version.
        versions={name: importlib.metadata.version(name) for name in
                  {d.metadata['Name'] for d in importlib.metadata.distributions()}},
        distribution_inventory=sorted(
            [dict(name=d.metadata['Name'], version=d.version)
             for d in importlib.metadata.distributions()], key=lambda d: (d['name'], d['version'])),
        source_files={Path(__file__).name: sha(Path(__file__)),
                      'gpu_statevector.py': sha(Path(__file__).with_name('gpu_statevector.py'))}))
    for repetition in range(count):
        phase = 'measured' if args.scenario == 'first_request' or repetition >= args.warmups else 'warmup'
        offset = .007 * repetition if args.scenario == 'parameter_update' else 0
        ops = shifted_ops(base_ops, offset)
        recorder = Recorder(args.track, sync)
        # Initial/terminal barriers only in primary. Verification and serialization excluded.
        sync()
        start = time.perf_counter()
        with context():
            if not reusable or repetition == 0:
                recorder.call('execution_preparation' if args.participant == 'custatevec'
                              else 'construction_binding', lambda: adapter.build(ops, grad))
            else:
                recorder.stages['construction_binding'] = unavailable('not_applicable', 'Retained fixed circuit/handle; state always recomputed')
            if args.participant == 'custatevec':
                recorder.call('state_initialization', adapter.initialize)
            recorder.call('forward', adapter.forward)
            recorder.call('output', lambda: adapter.output(grad)) if grad else None
            if args.scenario in ('gradient', 'training_step'):
                recorder.call('backward', adapter.backward)
            if args.scenario == 'training_step':
                recorder.call('optimizer', lambda: adapter.optimize(args.learning_rate))
            recorder.call('d2h', lambda: adapter.download(grad))
            if not reusable:
                recorder.call('cleanup', adapter.close)
        sync()
        total = time.perf_counter() - start
        for key in (('execution_preparation', 'state_initialization', 'h2d')
                    if args.participant == 'flagquantum' else ('h2d',)):
            recorder.stages[key] = unavailable('not_observable',
                'Contained in construction_binding or public forward call; no isolated public boundary in this adapter')
        if args.participant == 'custatevec':
            recorder.stages['construction_binding'] = unavailable('not_applicable', 'Primitive adapter has no SDK frontend')
            if reusable and repetition:
                recorder.stages['execution_preparation'] = unavailable('not_applicable', 'Retained handle, matrices and workspace')
        if not grad:
            recorder.stages['output'] = unavailable('not_applicable', 'Full state is the forward output')
        for key, applicable in [('backward', args.scenario in ('gradient', 'training_step')),
                                ('optimizer', args.scenario == 'training_step'), ('cleanup', not reusable)]:
            if not applicable:
                recorder.stages[key] = unavailable('not_applicable', 'Not part of this request contract')
        expected = reference(args.qubits, ops)
        host = adapter.host
        errors = dict(state=float(np.max(np.abs(host['state'] - expected))),
                      norm=float(abs(np.vdot(host['state'], host['state']).real - 1)))
        if grad:
            errors['loss'] = abs(float(host['loss']) - loss(expected))
        if args.scenario in ('gradient', 'training_step'):
            expected_gradient = gradient_reference(args.qubits, ops)
            errors['gradient'] = float(np.max(np.abs(host['gradient'] - expected_gradient)))
            initial = np.array([a for _, _, a in ops if a is not None])
            expected_parameters = initial - (args.learning_rate * expected_gradient if args.scenario == 'training_step' else 0)
            errors['parameters'] = float(np.max(np.abs(host['parameters'] - expected_parameters)))
        artifact = args.output / f'{phase}-{repetition}.npz'
        np.savez(artifact, **host)
        record = dict(protocol=PROTOCOL, participant=args.participant,
            scope='component_request' if args.participant == 'custatevec' else 'sdk_request',
            scenario=args.scenario, track=args.track,
            grad_mode=('not_applicable' if args.participant == 'custatevec' else 'enabled' if grad else args.grad_mode),
            requires_grad=grad, parameter_policy='rebuild' if not reusable else 'retained_fixed',
            qubits=args.qubits, repetition=repetition, phase=phase, parameter_offset=offset,
            request_wall_seconds=total, stages=recorder.stages, status='completed',
            semantic_status='accepted' if all(math.isfinite(v) and v <= args.tolerance for v in errors.values()) else 'rejected',
            errors=errors, tolerance=args.tolerance, output=dict(path=artifact.name, sha256=sha(artifact), bytes=artifact.stat().st_size),
            forward_circuit_executions=1, gradient_method='torch_autograd' if grad else None,
            backward_circuit_executions=None if args.scenario in ('gradient', 'training_step') else 0,
            backward_execution_count_status='not_observable' if args.scenario in ('gradient', 'training_step') else 'not_applicable')
        check_record(record)
        records.append(record)
        write(args.output / 'records.json', records)
    if reusable:
        adapter.close()  # Retained resource release is outside repeated request timing.
        sync()
    return int(any(r['semantic_status'] != 'accepted' for r in records))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--participant', choices=('custatevec', 'flagquantum'), required=True)
    parser.add_argument('--scenario', choices=SCENARIOS, required=True)
    parser.add_argument('--track', choices=('primary', 'diagnostic'), default='primary')
    parser.add_argument('--grad-mode', choices=('default', 'no_grad', 'inference'), default='no_grad')
    parser.add_argument('--qubits', type=int, default=4)
    parser.add_argument('--layers', type=int, default=4)
    parser.add_argument('--seed', type=int, default=41)
    parser.add_argument('--warmups', type=int, default=2)
    parser.add_argument('--measured', type=int, default=3)
    parser.add_argument('--learning-rate', type=float, default=.01)
    parser.add_argument('--tolerance', type=float, default=1e-10)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--worker', action='store_true', help=argparse.SUPPRESS)
    parser.add_argument('--timeout', type=int, default=300)
    args = parser.parse_args()
    if (not 1 <= args.qubits <= 24 or args.layers < 1 or args.warmups < 0
            or args.measured < 1 or not math.isfinite(args.learning_rate)
            or not math.isfinite(args.tolerance) or args.tolerance <= 0):
        parser.error('Invalid size, repetition count, learning rate or tolerance')
    if args.participant == 'custatevec' and args.scenario in GRAD_SCENARIOS:
        parser.error('Gradient scenarios need an independently declared differentiable stack; primitive is not applicable')
    if args.scenario in ('gradient', 'training_step') and args.qubits > 12:
        parser.error('Independent parameter-shift verification is bounded to <=12 qubits')
    if args.output.exists():
        parser.error('Output exists; append-only run requires a new path')
    if args.worker:
        return worker(args)
    start = time.perf_counter()
    try:
        result = subprocess.run([sys.executable, str(Path(__file__).resolve()),
                                 *sys.argv[1:], '--worker'], capture_output=True,
                                text=True, timeout=args.timeout)
        execution = dict(status='completed' if result.returncode == 0 else 'error',
                         returncode=result.returncode, stdout=result.stdout, stderr=result.stderr)
    except subprocess.TimeoutExpired as exc:
        execution = dict(status='timeout', returncode=None,
                         stdout=str(exc.stdout), stderr=str(exc.stderr))
    execution['process_wall_seconds'] = time.perf_counter() - start
    execution['command'] = sys.argv
    execution['publication_eligible'] = False
    args.output.mkdir(parents=True, exist_ok=True)
    write(args.output / 'execution.json', execution)
    return int(execution['status'] != 'completed')


if __name__ == '__main__':
    raise SystemExit(main())
