# P1a: native parameter reuse, sampling and observable workflows

## Implementation status

SDKBench 0.3.0 adds public-API adapters for FlagQuantum 0.3.1, Qiskit 2.6.2 and Cirq 1.7.0, plus a serial process-block runner using the P0 kernel supervisor and independent evaluators. The scope is W01, W04 and W08: PARAM-04/12/24, OBS-04/12/20 and SAMPLE-03/05, eight instances per SDK. Input artifacts, reference values, numerical/statistical thresholds and per-case resource caps remain the frozen candidate protocol's values.

The [machine-readable binding](p1a-profile.json) records the initial package/profile choices. These are engineering integrations, not independently reviewed SDK rankings. P0 review and sealed-host/environment gates remain open. No participant name changes an evaluator, tolerance, seed allocation or resource ceiling.

## Native APIs and attribution

| Stack | Parameter reuse | Requested expectations | Joint sampling |
| --- | --- | --- | --- |
| FlagQuantum 0.3.1 + Torch 2.14 CPU | `Circuit`, `Parameter`, `bind_parameters` | `fq.run` with public `fq.expectation` outputs | `fq.run` with one full-register `fq.samples` output |
| Qiskit 2.6.2 | `QuantumCircuit`, `ParameterVector`, `assign_parameters` | `Statevector.from_instruction` and native Pauli expectations | `StatevectorSampler`, paired classical-register BitArray outputs |
| Cirq 1.7.0 | Symbolic circuit and `resolve_parameters` | `Simulator.simulate_expectation_values` | `Simulator.run`, paired measurement-key bit arrays |

Each repetition constructs one native symbolic template and evaluates the seven complete bindings in fixture order. The template is reused within that outcome; binding never rewrites it in place. Each repetition constructs its own program, so previous participant outputs are not cached. The same SDK instance may retain legitimate runtime/import caches within a block.

All circuits execute on CPU at complex128/float64. Cirq's default complex64 is explicitly overridden. FlagQuantum requests statevector/PyTorch CPU execution with gradients, approximation and backend fallback disabled; literals and bindings use float64 tensors. Qiskit uses its own exact Statevector APIs, without Aer. These fixed choices are declared before measurement; no participant-specific tuning or SDK source patch is supplied.

The adapters implement input translation and classical output normalization only. They import no reference generator, expected-output artifact, P0 program simulator or benchmark-side sampler. Weighted observable totals use the same classical dot product for all SDKs. Quantum propagation, expectations and random shot generation are native SDK operations. Missing SDK functionality is never filled by another SDK or an analytic graph-state solution.

## Register and precision conventions

Logical q0 is bit 0. Pauli word character j denotes logical qj. Qiskit's displayed Pauli labels are reversed at the API boundary. Cirq receives explicit qubit ordering for expectations. FlagQuantum observables use explicit logical indices. All requested values must pass P0 finite/shape/order checks and the unchanged numerical thresholds.

Sampling uses the SDK's actual joint shots. Qiskit's two native register `BitArray.to_bool_array(order='little')` outputs are paired by shot index; independent marginal histograms are never combined into invented joint data. Cirq's measurement-key columns are mapped to the declared register bits. FlagQuantum produces one full joint sample array, then projects the requested registers from the same rows. The common normalizer only counts observed bit rows; it never evaluates a probability law or draws additional samples.

Every context uses 65,536 native shots and the prescribed block/context seed. The evaluator reconstructs logical counts from joint register records and applies the unchanged family-wide confidence allocation. A one-block sampling qualification does not establish the complete W08 confidence family or full-case acceptance.

## Lifecycle and resource accounting

The default `protocol` mode executes ten fresh worker processes per SDK/instance. Numeric blocks run two warmups and three measured outcomes in the same process. Sampling blocks run zero warmups and one measured acquisition. Warmups are independently checked and retained separately; a bad warmup prevents a successful block verdict even if later outputs are correct.

The worker imports one SDK and records its import time separately. The primary monotonic timer surrounds native construction, binding, execution, synchronization/materialization and normalization for one complete outcome. Registration, file capture and independent validation are outside that primary timer. External supervisor wall time includes process launch/import and is separately recorded. Native program-build/binding/execution counts and warnings are retained as audit evidence, not speed scores.

The P0 supervisor enforces the same single-CPU, numerical-thread environment, memory, socket-network, child cleanup and output policies for every SDK. Memory caps remain 16 GiB for numerical cases and 8 GiB for sampling. Original complete-case wall caps remain in [FIRST_WAVE.md](FIRST_WAVE.md); no per-SDK override is exposed. All worker descendants count toward the same kernel cap.

SDK order rotates by block. The cumulative case budget charges only elapsed work attributable to that SDK/instance, including its setup, validation and evidence export; it pauses while other cases or SDKs run. This resolves the interaction between counterbalanced blocks and complete-case caps without charging one SDK for another's work. The budget never resets to the original cap between blocks. Every block is attempted or explicitly recorded as budget-exhausted; a slow case is not silently dropped.

`qualification` mode is an explicit engineering smoke scope: one fresh process and one measured outcome, with no warmups, for every selected case. It retains the original instance inputs, thresholds and resource caps. Its successful outcomes remain `not-measured` at full-case level because ten blocks are absent. It must not be described as the full P1a performance study.

## Evidence and failures

[Campaign code](../../src/sdkbench/p1a/campaign.py) writes an immutable evidence directory containing observed environment/dependency facts, registered component content hashes, admission decisions, each input request, response, raw bounded stdout/stderr, resource telemetry, warmup/measured records and P0 verdicts. The SDK version, request digest, block/repetition identity and supervised process PID are checked. Import/setup failure, missing distributions, version mismatch, unsupported capabilities, native exceptions, malformed evidence, timeouts and OOM remain visible. A success-shaped stdout cannot override a failed supervisor outcome.

Component fingerprints hash actual installed non-pyc files, rather than asserting an unverified wheel hash. The environment includes dependency versions and RECORD fingerprints. The image descriptor is explicitly marked unsealed: its hash identifies observed platform facts, not an immutable boot image or a completed host review. Actual SDK/version/host information must be inspected before any comparative interpretation.

`report.json` lists all requested SDK/instance outcomes and every unselected P1a case. Missing capabilities and failed outputs receive no zero-latency or successful timing substitute. `evaluate_case` and `evaluate_workflow` remain the completeness checks; a partial selected case list cannot establish its missing workflow variants. Every report has `publication_eligible: false`; signed independent reviews and sealed study infrastructure are not inferred from passing engineering tests.

The result schema separates participant execution status from semantic acceptance. A distribution-equivalence failure means its confidence criterion was not established; it is not automatically proof of a wrong underlying sampling distribution. Detailed P0 reasons remain in the evidence, without retries or seed hunting.

## Running

Install all three pinned adapters on Python 3.12. On Linux, select the published CPU Torch wheel first:

```sh
python -m pip install 'torch==2.14.0+cpu' --index-url https://download.pytorch.org/whl/cpu
python -m pip install '.[p1a,dev]'
```

FlagQuantum's published package declares Python <3.13. Selecting a Python environment without a compatible installed distribution is recorded as an installation/access gap; it is not erased from the requested cohort. The legacy `all` extra remains the legacy Qiskit/Cirq environment; use `p1a` explicitly for this cohort.

With an operator-prepared Linux cgroup subtree and the operator process inside its delegated operator leaf:

```sh
sdkbench-p1a --bundle docs/implementation --directory evidence/p1a \
  --cgroup-parent /sys/fs/cgroup/sdkbench-study --cpu 2
```

Use `--mode qualification` for the explicit one-block engineering scope. `--sdk` and `--instance` may select a declared partial campaign; the report lists omitted cases. `--environment runtime.json` supplies explicit runtime loader paths when required. Existing evidence directories are never overwritten. Missing kernel controls refuse execution; there is no unbounded local-process fallback.

These commands do not qualify a machine automatically. The dedicated CI runner is an engineering host; its resource/SMT/image facts are retained and it is not represented as the sealed 8-core/64-GiB study host in the candidate roadmap.

## Testing and reproducibility

[Adapter tests](../../tests/test_p1a_adapters.py) execute real public SDK APIs against frozen P0 references, test first/second/first binding reuse, and reject identical bad outputs for every SDK. [Runner tests](../../tests/test_p1a_runner.py) use clearly synthetic records to test lifecycle counts, order rotation, budget carryover, malformed/mismatched responses and retained failures. They are not participant evidence.

The [P1a CI workflow](../../.github/workflows/p1a.yml) installs the pinned CPU stack, requires all three SDKs, prepares a disposable cgroup subtree and runs [the integration driver](../../tools/p1a_integration.py). Routine push/PR CI runs the complete ten-block lifecycle for PARAM-04, OBS-04, SAMPLE-03 and SAMPLE-05. Manual dispatch with `extended=true` additionally attempts all eight frozen sizes for each SDK in qualification mode; this is the required extended check for a cohort release. Large-instance qualification and complete small-instance checks are explicitly separate, and no omitted case is represented as passed. All native outcomes and failures, not only successful timing samples, are retained in a hashed artifact manifest.

[Evidence replay and archive tooling](../../tools/p1a_evidence.py) verifies every retained file hash and independently replays measured/warmup decisions without importing SDKs. It can write a lossless compressed JSON archive with the exact original UTF-8 evidence bytes, paths and hashes. An archive records its actual source commit; results from different adapter implementations must not be silently mixed into a performance claim.

```sh
SDKBENCH_REQUIRE_P1A=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 \
  python -m pytest tests/test_p1a_adapters.py tests/test_p1a_runner.py -q
python tools/requirements_docs.py --check
python tools/roadmap_docs.py --check --verify-small
```

No global SDK rank follows from these integrations. Full large-instance ten-block campaigns, independent adapter review, model breadth and a sealed publication environment remain explicit next steps.

Public API sources checked on 2026-11-18: [FlagQuantum published package](https://pypi.org/project/flagquantum/0.3.1/), [Qiskit Statevector](https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.quantum_info.Statevector), [Qiskit StatevectorSampler](https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.primitives.StatevectorSampler), [Cirq simulation and precision](https://quantumai.google/cirq/simulate/simulation), and the [official Torch CPU index](https://download.pytorch.org/whl/cpu/torch/).
