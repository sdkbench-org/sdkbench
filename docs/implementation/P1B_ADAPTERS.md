# P1b: shared-parameter gradients, dynamics and constrained routing

SDKBench 0.4.0 implements W05, W07 and W03 for the registered FlagQuantum 0.3.1, Qiskit 2.6.2 and Cirq-core 1.7.0 stacks. The [profile](p1b-profile.json) declares methods, dependencies and known capability gaps before the Linux campaign. All eight frozen instances are in scope. The [P0 contracts](P0_FOUNDATION.md), input/reference hashes, numerical thresholds and complete-case resource caps are unchanged. Passing integration does not establish a global SDK ranking.

## Tasks and acceptance

| Workflow | Frozen instances | Independent acceptance | Complete-case cap |
| --- | --- | --- | --- |
| W05, three-output Jacobian with each of 3n parameters shared by two rotations | GRAD-04, GRAD-08, GRAD-12 | Primal atol 1e-9, rtol 1e-8; Jacobian atol 2e-7, rtol 2e-5, including zero and near-zero parameters | 180 / 600 / 1800 seconds; 16 GiB |
| W07, fixed second-order digital TFIM evolution from a Neel state | DYN-04-S32, DYN-08-S64 | Every local X/Z and neighboring ZZ moment agrees with digital ideal at atol 1e-9, rtol 1e-8 and exact physical evolution within absolute 0.002 | 600 / 1800 seconds; 16 GiB |
| W03, identity initial layout, line/grid full-CZ target, no ancillas | ROUTE-LINE-06, ROUTE-GRID-08, ROUTE-LINE-12 | Edges, full-CZ basis, final logical-to-physical permutation and original semantics; atol 1e-8, rtol 0, norm error 1e-10 | 600 / 900 / 1800 seconds; 16 GiB; additionally 120 seconds per native compilation |

The six-qubit route is checked as a complete operator, allowing one global phase for the whole operator. The eight- and twelve-qubit routes use the three frozen full-output probes and provide limited evidence rather than an equivalence proof. The common evaluator computes actual full-CZ count and two-body dependency depth. No optimality claim follows from those values.

## Public native methods and component attribution

| Registered stack | Gradient | Dynamics | Routing and target synthesis |
| --- | --- | --- | --- |
| FlagQuantum + Torch 2.14 CPU | `fq.jacobian` with native PyTorch autograd; shared Tensor bindings preserve the computation graph | Native `Circuit` RX/RZZ and `fq.run` expectations at complex128 | `flagquantum.compiler.compile`, default level 2 and restore-after-each-gate routing, then the SDK's exported `legalize_native_gates` pass |
| Qiskit + Qiskit Algorithms 0.4.0 | `ReverseEstimatorGradient`, with `StatevectorEstimator` for the primal | Native RX/RZZ and Statevector expectations | `transpile` level 2, basis CZ/U, exact synthesis, identity layout, `qubits_initially_zero=False`, one process, frozen compiler seed |
| Cirq-core | `unsupported` for this registered stack | Native RX and `ZZPowGate(theta/pi, global_shift=-0.5)`, complex128 Simulator | `RouteCQC`, identity `HardCodedInitialMapper`, followed by `CZTargetGateset(allow_partial_czs=False, atol=1e-12)` |

The gradient configuration targets exact local CPU derivatives. Qiskit's native reverse-mode extension and FlagQuantum's native autograd are selected by that role before the controlled campaign. Neither adapter implements finite differences, parameter shifts, an adjoint solver or derivative rules in benchmark code. Qiskit Algorithms is an explicit installed, version-checked, content-fingerprinted gradient component; its results are not attributed to Qiskit core alone.

Cirq-core 1.7.0 exposes no general expectation-Jacobian API. TensorFlow Quantum 0.7.6 is a separately installable ecosystem stack whose published metadata pins Cirq-core 1.5.0. It is not silently installed into this 1.7.0 registration. All three Cirq gradient instances remain `unsupported`, with no successful timings or fabricated gradients. This says nothing about all possible Cirq ecosystem configurations; a compatible extension stack requires its own future registration and qualification. The same extension and non-substitution policy applies to every participant.

Structured `native_primal_calls` and `native_derivative_calls` record public API calls separately (one each per successful gradient outcome). Unobserved internal parameter bindings are omitted, never reported as zero. Derivative audit counts have explicitly different units: FlagQuantum counts native forward-program invocations (primal plus Jacobian callback); Qiskit counts three primal expectation requests plus three native reverse-gradient requests. Internal state evolutions/backward sweeps are not exposed as comparable counts. These audit values must not be compared as physical circuit executions or a speed score. The primary wall timer includes all primal and derivative work and output materialization.

Dynamics executes the exact frozen S2 sequence, including the initial logical basis state and the RX/RZZ angle conventions. Adapters do not read reference values, diagonalize the Hamiltonian or substitute exact spectral evolution. P0 checks both digital implementation error and physical approximation error separately.

Routing uses public SDK routing and synthesis passes, never a benchmark-side router or decomposition fallback. FlagQuantum's target capability snapshot describes the **abstract benchmark target definition**, not observed hardware capabilities: its static source points to a content-hashed definition of the common full-CZ/one-qubit basis. The SDK native legalizer's expansion bound is 20,000 added operations, matching the common evaluator's existing total-artifact ceiling; the final artifact still must satisfy that total ceiling. No compiler precision, memory or time allowance is relaxed. Runtime configuration is explicitly complex128. Qiskit and Cirq normalize native one-qubit matrices; global phase is permitted only as specified by P0. Final-layout metadata is reconstructed through SDK-native mappings and checked independently.

Qiskit consumes the frozen per-block compiler seed. The FlagQuantum and Cirq compiler entry points used here expose no seed argument; their audit explicitly records this limitation rather than pretending the requested seed was consumed. Identical compiler output across blocks is not ten independent randomized searches. No participant receives seed hunting or repeated best-of selection.

## Shared lifecycle and limits

P1b reuses the P1a campaign/worker lifecycle with an explicit suite selector. Default P1a behavior remains available. Each numeric case runs ten fresh process blocks, two validated warmups and three measured outcomes per block. Every repetition builds a fresh native program. SDK/gradient-extension imports are outside the primary outcome timer and inside the complete-case wall budget. Construction, binding, compilation, native computation, derivative work and output normalization are inside the outcome timer.

The strict P0 Linux cgroup-v2 supervisor enforces one CPU, one numerical thread, the frozen memory/case-time caps, no sockets, bounded output and descendant cleanup. Budgets accumulate only work attributable to that SDK/instance, including import, validation and evidence export, and never reset between blocks. There is no unrestricted local fallback.

Each routing outcome additionally arms a POSIX kernel timer for 120 seconds around native construction, route/synthesis and artifact normalization. SIGALRM uses its default process-termination action, so native code holding the Python GIL cannot postpone enforcement. The parent preserves raw execution evidence and maps this signal to `timeout`; it cannot count a successful stdout as acceptance. A separate shortened test-only alarm verifies native-call termination locally and inside the Linux supervisor. The production cap remains 120 seconds.

The runner retains installation/version mismatches, missing capabilities, exceptions, malformed responses, semantic failures, timeouts and OOM. Failed warmups prevent case acceptance. Every selected case appears in the report and every omitted case is listed. Admission/component/configuration hashes include the P1b runtime sources and the native gradient extension. Prior P1a archives remain immutable and identify their original source commits.

## Running and verifying

Use Python 3.12 and install from this checkout. The PyPI release is separate from this implementation:

```sh
python -m pip install 'torch==2.14.0+cpu' --index-url https://download.pytorch.org/whl/cpu
python -m pip install '.[p1b,dev]'
SDKBENCH_REQUIRE_P1B=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 \
  python -m pytest tests/test_p1b_adapters.py tests/test_p1b_runner.py -q
```

With an operator-delegated Linux cgroup subtree and the operator inside its operator leaf:

```sh
sdkbench-p1b --bundle docs/implementation --directory evidence/p1b \
  --cgroup-parent /sys/fs/cgroup/sdkbench-study --cpu 2
python tools/p1b_integration.py --directory evidence/p1b-ci \
  --cgroup-parent /sys/fs/cgroup/sdkbench-study --scope all-protocol
python tools/p1b_evidence.py --directory evidence/p1b-ci --bundle docs/implementation \
  --archive evidence/p1b-raw.json.gz --summary evidence/p1b-replay.json
```

The CLI returns nonzero for **any** nonaccepted case, including `unsupported`. Integration CI separately checks whether observed statuses match the declared capability profile; a correctly retained known gap can pass an accounting test but remains non-success in every result/report. Unexpected failure in any SDK fails CI. No SDK name is special-cased by the evaluator.

Routine [P1b CI](../../.github/workflows/p1b.yml) runs all adapter sizes and the complete small-instance protocol. Manual dispatch with `extended=true` runs the complete protocol for every size, 240 process blocks, 720 measured records and 480 warmups. Evidence is retained even when CI fails. The [archive/replay tool](../../tools/p1b_evidence.py) verifies the manifest and independently re-evaluates records without importing SDKs. [Qualification evidence](P1B_QUALIFICATION.md) records actual runs and their scope.

The observed CI host/image is unsealed. Reports remain `publication_eligible: false`; dedicated host review, independent adapter review, broader model/task coverage and reviewed environment registration are still required before comparative publication.

Public sources checked on 2026-11-18: [FlagQuantum 0.3.1 distribution](https://pypi.org/project/flagquantum/0.3.1/), [Qiskit reverse estimator gradient](https://qiskit-community.github.io/qiskit-algorithms/stubs/qiskit_algorithms.gradients.ReverseEstimatorGradient.html), [Qiskit transpile](https://quantum.cloud.ibm.com/docs/en/api/qiskit/compiler), [Cirq RouteCQC](https://quantumai.google/reference/python/cirq/RouteCQC), [Cirq CZTargetGateset](https://quantumai.google/reference/python/cirq/CZTargetGateset), and [TensorFlow Quantum 0.7.6 metadata](https://pypi.org/pypi/tensorflow-quantum/0.7.6/json). FlagQuantum native compiler/target APIs are verified against the installed, unmodified published wheel; they are not private benchmark implementations.
