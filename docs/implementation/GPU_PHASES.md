# GPU phase protocol v2

This engineering protocol supplements `gpu-statevector-v1`; it does not revise
sealed measurements, metric weights or the existing v1 worker. The v1
`evolution_seconds` interval includes initialization and internal execution
preparation. It is not a GPU kernel measurement.

## Independent experiments

`tools/gpu_phases.py` runs one participant/scenario/gradient-mode/track in a fresh
worker process. Repetitions within that process remain paired observations, not
independent process blocks. A confirmatory campaign must predeclare process
blocks, balanced participant order, resource/version constraints and analysis.
This collector alone does not qualify a host or establish a ranking.

| Scenario | Request and reuse contract |
| --- | --- |
| `first_request` | First complete request after imports/context; no warmup. Construction and disposal included. Interpreter launch is separately observed by the supervisor. |
| `repeated_fixed` | Retain a circuit or native handle, matrices and workspace. Recompute a fresh state on every request; never return a cached state. First construction is in warmup if warmups are requested. Final retained-resource disposal is outside request timing. |
| `parameter_update` | Change all rotation angles by `0.007 * repetition`; rebuild through the declared public adapter on each request. This is **not** native parameter-binding reuse. |
| `differentiable_forward` | Construct leaf parameters with `requires_grad=True`; return full state and scalar `<Z_0>` with graph recording, without backward. |
| `gradient` | Above plus backward of the same real scalar loss with respect to every rotation angle. |
| `training_step` | Above plus one explicitly implemented plain SGD update, learning rate 0.01, no momentum, weight decay or optimizer state. Each request starts at the same initial parameters. |

The first three scenarios support FlagQuantum `default`, `no_grad` and
`inference` contexts with **requires_grad=False**. They are controlled ablations;
they must not be described as equivalent to graph-recording forward. Gradient
scenarios force enabled autograd. cuStateVec has no Torch gradient context;
gradient scenarios are not applicable to this primitive adapter. A future
cuStateVec-plus-differentiation stack requires a separate participant identity,
algorithm and execution-count disclosure.

For a matched graph-recording ablation, `differentiable_forward` accepts
`--forward-context enabled|no_grad|inference`. All three keep leaf parameters
with requires_grad=True and return the same full state, scalar loss and parameter
vector. Only graph-recording context changes; backward is absent in all three.
This is separate from ordinary forward requests with requires_grad=False.

`--oracle-cache` can supply precomputed independent NumPy fixtures keyed by the
SHA-256 of qubit count and the complete operation/angle list. Each fixture's
bytes and SHA-256 are checked before use outside request timing. Generation and
the complete index must be retained with the study. Identical reference inputs
are reused within a worker; changed parameters use distinct keys. Every actual
GPU output is still checked and retained independently.

## Two timing tracks

* **primary:** host wall time around the complete request, synchronized at entry
  and completion only. No phase barriers or CUDA event measurements are inserted.
  Primary stage values stay null. This is the performance-comparison track.
* **diagnostic:** separate process/run with synchronization at each observable
  public stage. Stage durations include host dispatch and GPU completion wait;
  they are not CUDA kernel times. Synchronization changes execution, so these
  values cannot be subtracted from, pooled with or stacked into primary timings.

Startup imports/context, supervisor process wall time and request time are
distinct. Supervisor time also includes verification and serialization; it is
not a cold-request latency estimate. The collector imports Torch and CuPy for
both participants as shared synchronization infrastructure; these startup costs
are not a minimal participant installation comparison. No clock-domain mixing.
Runtime build identifiers and native library versions are retained separately
from Python distribution metadata. The complete distribution inventory preserves
duplicate dist-info entries; a dictionary alone can hide conflicting metadata.

## Phase semantics and observability

The protocol defines construction/binding, execution preparation, device-state
initialization, H2D, forward, output production, D2H, backward, optimizer, cleanup.
All rows include status, nullable seconds, and a reason when unmeasured.
Measured diagnostic rows declare `clock=host_wall_completed, additive=false`.
Unmeasured is never zero; `not_observable`, `not_applicable`, `not_measured` and
execution errors have different meanings.

cuStateVec preparation covers native handle, uploaded matrices and workspace;
its public state initialization and apply-matrix loop are separately observable.
It has no SDK frontend. FlagQuantum public `Circuit.state(refresh=True)` includes
initialization, internal planning and gate execution, so the `forward` interval
is a **composite public call**. Internal preparation/initialization are explicitly
`not_observable`. H2D matrix/parameter traffic remains within preparation or
construction and is not separately timed. No unsupported pure-kernel claim is
inferred from these rows. State output requires no extra production step; scalar
loss production is separately observed for gradient scenarios. Cleanup measures
explicit resource release within this adapter, not complete allocator teardown
or Python process destruction.

## Correctness and evidence

The circuit family, MSB qubit order and independent NumPy state oracle are reused
from v1 without editing it. Every warmup and measurement retains full state
output, scalar loss, gradients and post-update parameters as applicable. Absolute
state, normalization, loss, gradient and SGD-update errors are individually
checked at 1e-10 in complex128/float64. Outputs and timings before an error remain
on disk and supervisor stderr/timeout status is retained; errors are not zeros.

Gradient correctness uses an independent NumPy two-term parameter-shift oracle
for each RY/RZ angle. Oracle evaluations are outside timings. Because this costs
two reference evolutions per parameter, gradient/training verification is bounded
to at most 12 qubits. One forward circuit execution is explicit; autograd's
internal backward execution count is `null/not_observable`, not an invented
count of one or zero. This prevents an unjustified algorithmic-work comparison.

Example (new output directory required):

```sh
python tools/gpu_phases.py --participant flagquantum --scenario training_step \
  --track primary --qubits 4 --output /private/results/new-run/primary
python tools/gpu_phases.py --participant flagquantum --scenario training_step \
  --track diagnostic --qubits 4 --output /private/results/new-run/diagnostic
```

The method and CPU-only tests belong in the public engine repository. Environment
facts, smoke outputs, failures and confirmatory data belong in private
`sdkbench-results`, with source hashes, exact execution revision and predeclared
study identity. No smoke result should be exported as a comparative campaign.
