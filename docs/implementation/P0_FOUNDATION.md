# P0 foundation: implemented contracts, evaluators and execution controls

## Status and scope

SDKBench 0.2.0 implements the technical foundation for the frozen `sdkbench-first-wave / 0.1-candidate-1` bundle. All 24 first-wave instances have independent semantic evaluators and synthetic positive/negative qualification tests. The candidate fixtures, thresholds and numerical references are unchanged. No participant SDK adapter, SDK support claim, performance comparison or live-device execution is added here.

This is technical P0 implementation, not a claim that all P0 release gates are satisfied. Stakeholder review, independently signed mathematical/adapter reviews, a sealed study host/image and resolved participant environments remain required before publishing participant performance. CI validates software and kernel controls; it is not an independent scientific review or a qualified study machine.

## Code and boundaries

| Component | Implementation | Responsibility |
| --- | --- | --- |
| Result and adapter contracts | [models.py](../../src/sdkbench/p0/models.py) | Versioned identity, explicit completion/failure states, finite JSON, raw measurements and semantic verdicts |
| Registered stack | [registration.py](../../src/sdkbench/p0/registration.py) | Component attribution and content-addressed configuration/environment manifests |
| Protocol bundle | [bundle.py](../../src/sdkbench/p0/bundle.py) | Verify all frozen artifact hashes, bind result identity and provide input-only adapter requests |
| Acceptance rules | [evaluators.py](../../src/sdkbench/p0/evaluators.py) | Numerical, statistical, trajectory, program and ledger decisions without participant imports |
| Small-program semantics | [semantics.py](../../src/sdkbench/p0/semantics.py) | Independent program propagation and restricted QASM interpretation |
| Offline transport | [transport.py](../../src/sdkbench/p0/transport.py) | Supply recorded provider events, without implementing client reconciliation |
| Resource supervisor | [supervisor.py](../../src/sdkbench/p0/supervisor.py), [_isolate.py](../../src/sdkbench/p0/_isolate.py) | Enforce memory/CPU/process/wall/output limits and deny socket networking before participant execution |
| Invocation bridge | [execution.py](../../src/sdkbench/p0/execution.py) | Send a request to a reviewed adapter, retain execution evidence and validate its returned record |
| CLI | [cli.py](../../src/sdkbench/p0/cli.py) | Inspect bundles, validate records and execute one bounded invocation |

The new code imports neither evaluated SDKs nor the fixture-generation tool. Numerical gold values come only from the verified, explicitly selected bundle. Program artifacts are independently interpreted rather than trusting a participant's self-reported semantic fidelity. Reference derivation and limitations remain in [REFERENCES.md](REFERENCES.md).

The legacy `sdkbench run` harness remains separate. The new `sdkbench-p0` entry point does not turn the legacy adapters into first-wave adapters or claim the full ten-block study is implemented.

## Result schema and provenance

`ResultRecord` schema version 1 contains:

- `identity`: protocol revision, instance ID, input-fixture SHA256, numerical-reference SHA256, complete bundle-manifest SHA256, stack ID, configuration SHA256 and environment SHA256.
- `block` in 0..9 and `repetition`, checked against the task's required measured repetitions.
- `status`: `completed` or an explicit noncompletion status; `payload` is required only for completion, and a nonempty `reason` only for noncompletion.
- `measurements`: finite, nonnegative named values, retained separately from semantic acceptance. Participant-reported timings are not trusted as independently measured latency.

The identity binds changes to thresholds/references as well as inputs. Serialized verdicts additionally identify the SDKBench version and SHA256 fingerprint of the actual P0 implementation source. `Registration` hashes component identities plus configuration options separately from environment facts. It requires component names, versions, roles and artifact hashes, FP64/complex128 and single-thread declarations, an image hash, dependency-lock hash and host facts. These are declared facts; structural validation cannot prove the operator installed those bits, uses a dedicated physical core or obtained independent review. Verify them when sealing a study environment.

All participant names use the same rules. The package snapshot is not an execution allowlist. No conditional threshold, hidden fallback, adapter or evaluator path refers to a favored SDK.

`evaluate()` checks one measured repetition. `evaluate_case()` additionally requires exactly ten blocks and the prescribed one or three measured repetitions in each, with one identical registered identity. Missing blocks remain `not-measured`; duplicate or mixed records are rejected. `evaluate_workflow()` additionally requires every constituent instance and an identical stack/configuration/environment across them, including complete sampling/adaptive confidence families. No aggregate ranking or accepted latency is produced by these functions.

An `accepted` verdict is explicitly scoped to semantic evidence. It is not independent review approval or permission to publish a performance result. Failure statuses remain visible; unsupported, inaccessible, unimplemented, incorrect, timed-out and out-of-memory outcomes never become zero-latency successes. The partial-job case may pass its recovery contract while its operational study status correctly remains `partial`.

## Adapter payload contracts

Fields below are exact; unknown/missing fields, nonfinite values and incorrect shapes are rejected. Matrix complex entries are encoded as `[real, imaginary]`. Full examples are generated as synthetic qualification data in [p0_cases.py](../../tests/p0_cases.py); that helper is test-only and must never be registered as a participant adapter.

| Kind | Required payload | Independent decision |
| --- | --- | --- |
| Parameter reuse | `binding_ids`, `observable_order`, seven `outputs` dictionaries | Exact binding/output identities and every requested moment at frozen tolerances |
| Observables | `expectations`, `weighted_sum` | All 64 values, weighted gold total and internal sum consistency |
| Jacobian | `outputs`, `jacobian`, `derivative` with method, quantum evaluation count and component attribution | All outputs and all shared-parameter derivatives, not an average error |
| Dynamics | `moments` | Both fixed digital-program tolerances and separate physical-error ceiling |
| Sampling | `contexts`, each with zero-based `context_id`, full `counts` vector and joint `records` | Integer totals, complete alphabet, independently reconstructed register mapping and conservative equivalence upper bound |
| Adaptation | `contexts`, each with `context_id` and full `counts` vector | All 18 teleportation contexts or the bounded-reset-loop joint law, no postselection |
| Training | `seed`, all 49 `trace` checkpoints, all 48 `gradients` | Frozen trajectory, direct chain-rule gradient audit, SGD recurrence, per-initialization progress and held-out endpoints |
| Compilation | `operations`, `final_layout`, `compile_wall_seconds` | Legal topology/basis, no ancillas, full n=6 operator or three n=8/12 probes, one global phase and explicit wire reconstruction |
| Interchange | `exported_source`, `reimported_source` | Interpret both text artifacts independently, preserving unitary/register or branch/reset behavior |
| Job recovery | `transport_trace`, `client_result` | Actual offline-call sequence, unique identity/record/shot ledger and correct completed/partial state |

Sampling records are `{register_a, register_b, count}` integers. Bit k of a register maps to qubit k of that register's `record_mapping` list; the evaluator reconstructs logical integer indices independently. Duplicate joint records, out-of-width values or disagreement between records and the normalized counts fail before statistics. Adaptive category encodings and context ordering are fixed by their fixtures. The confidence allocation is never recycled across missing cases or blocks.

A training row contains `step`, `theta`, `weights`, `bias`, `train_loss`, and `test_loss` at least at steps 0 and 48. Optional intermediate test losses are checked if supplied. Each gradient row contains `theta`, `weights` and `bias`; the evaluator recomputes the exact chain-rule minibatch gradient using the reported parameters and frozen data. Native/autodiff/other derivative methods remain participant responsibilities; audit math is not an adapter-side substitute.

Compiler target operations are full `cz` on a declared edge or a one-qubit `h/x/y/z/s/sdg/rx/ry/rz/unitary` operation. A `unitary` must be a finite unitary 2x2 complex matrix. `final_layout[q]` gives the physical output wire for logical q. The evaluator recomputes quality and depth from the artifact; no optimality score is invented. `compile_wall_seconds` remains participant-reported diagnostic evidence; enforce each actual compilation stage using `Limits.for_case(..., stage='compile')` when integrating it.

QASM support is deliberately limited to the specified four-qubit QASM2 static/register subset and two-qubit QASM3 measurement/reset/if subset. Unknown syntax is rejected, not silently ignored. Angle expressions permit finite numbers, pi and simple arithmetic, never Python execution. This is not a whole-language parser or SDK conformance claim.

## Strict Linux execution

`run_command()` requires an explicitly delegated, non-root cgroup-v2 subtree with memory, CPU, cpuset and pids controllers, `memory.peak`, `cgroup.kill`, and `libseccomp.so.2`. The operator prepares this subtree and runs the supervisor in a separate operator leaf under it, so worker migration stays within the delegated common ancestor; SDKBench never silently changes host-wide controls or requests elevated privileges itself. macOS and hosts without these controls can inspect/validate artifacts but strict execution refuses to launch a participant command.

For each invocation, the supervisor creates a fresh leaf cgroup. Before executing the participant command, the private standard-library launcher, started with site initialization disabled, joins it, pins its CPU, disables core files, sets a per-file size limit and installs inherited syscall filters. The worker environment contains explicit values only (including any required pinned `LD_LIBRARY_PATH`, supplied through the API or CLI `--environment` JSON), with numerical-library thread controls forced to one and no operator-shell credential inheritance.

Kernel controls include:

- `memory.max`, `memory.swap.max=0`, and `memory.oom.group=1` for aggregate descendant memory and group OOM handling. Kernel-accounted memory includes charged cache and is a conservative ceiling relative to RSS-only accounting; report both kernel peak and sampled summed RSS.
- A one-CPU cpuset and CPU quota, plus a process/thread-count ceiling. Numerical thread settings are declared and recorded; the cpuset enforces one available execution CPU even if a library ignores a setting. The operator must still seal SMT sibling and competing-host-load policy.
- Inherited seccomp rules denying socket creation/use for IPv4, IPv6 and Unix sockets, plus io_uring network bypass and namespace/process-control routes. No user-space Python socket monkeypatch is used. Denial is unchanged in descendants after exec.
- A monotonic wall deadline, bounded stdout/stderr capture and per-file size limits. Timeout/output overflow kills the cgroup. Descendants remain members after `setsid()`; leftover children after the worker exits are classified as `child-leak` and killed. OOM evidence comes from kernel counters, not an inferred exit code alone.

This is a resource runner for reviewed adapters on a clean host, not a filesystem/hostile-code security sandbox. It does not hide host files, prove truthful SDK output, apply an installation-disk quota, reserve a dedicated physical core, or qualify a machine image. Do not run unreviewed hostile code or place credentials on the study host. Whole-environment disk limits and host sealing remain operator/P1 campaign responsibilities.

## Invocation and evidence

A future adapter command receives the absolute request JSON path as its last argument. It writes exactly one `ResultRecord` to stdout and diagnostics to stderr. Requests contain the frozen input fixture, identity, block/repetition and prescribed sampling/compiler/training seeds; no gold output is passed. Construction, JIT, synchronization and output materialization belong inside the adapter's execution boundary.

`execute_once()` combines strict execution and independent checking. A timeout/OOM/crash cannot be overridden by a success-shaped stdout payload. Invalid JSON, duplicate keys, nonfinite constants, wrong invocation identity and incomplete results fail. The evidence directory retains the request, raw bounded stdout/stderr, limits, timestamps, kernel counters, observed host facts and semantic verdict. It never overwrites an existing evidence bundle. Output hashes cover captured bytes; truncation is explicit.

Create a `CaseBudget` before case setup and share it across invocations/stages/warmups/blocks to enforce the complete case wall budget. A compile stage is additionally bounded at 120 seconds. This API is a foundation for the P1 scheduler; `execute_once()` alone runs one invocation, not the protocol's full warmup/repetition lifecycle. Its external wall time includes launch/import and is separately labeled, not misreported as primary warm outcome latency. Do not reset a case budget to rescue a slow participant.

## Commands

Install the repository checkout or source archive to obtain `sdkbench-p0`:

```sh
python -m pip install '.[dev]'
sdkbench-p0 --bundle docs/implementation inspect
sdkbench-p0 --bundle docs/implementation validate result.json
sdkbench-p0 --bundle docs/implementation validate --full-case case-records.json
sdkbench-p0 --bundle docs/implementation validate --workflow W08 workflow-records.json
```

For a registered identity and an operator-prepared Linux subtree, run one adapter invocation:

```sh
sdkbench-p0 --bundle docs/implementation execute \
  --identity identity.json --cgroup-parent /sys/fs/cgroup/sdkbench-study \
  --cpu 2 --directory evidence/invocation-001 -- \
  /absolute/path/to/python /absolute/path/to/reviewed_adapter.py
```

The complete frozen bundle is stored in the repository and source distribution, not implicitly discovered from the installed wheel. Supply its path explicitly. Identity/configuration/environment files must be sealed by the operator; accepting their JSON structure is not certification of their contents.

## Qualification evidence and remaining gates

Run:

```sh
python tools/requirements_docs.py --check
python tools/roadmap_docs.py --check --verify-small
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python -m pytest -q
```

The dedicated Linux CI job delegates a disposable cgroup subtree on its ephemeral VM, places the test runner in its operator leaf and sets `SDKBENCH_TEST_CGROUP`. With this variable set, real-kernel tests are mandatory: no control-unavailable skip is allowed. They exercise aggregate child OOM, timeout, detached-child cleanup, CPU affinity/thread environment, elapsed clocks/telemetry, IPv4/IPv6/Unix-socket denial in parent and exec descendants, output overflow, crash and worker JSON faults. Other platforms run semantic/schema tests and explicitly skip those Linux-only integration tests.

Every instance has a positive expected-output test and missing-output negative test. Family-specific mutations cover stale/wrong bindings, phase-sensitive Y signs, wrong numeric terms, transposed/shared gradients, independent digital/physical gates, malformed counts and mappings, omitted feed-forward/reset/branches, loop cutoff, checkpoint/gradient/seed/progress errors, illegal target edges/bases/ancillas, wrong layouts/global phases, lossy/unsupported QASM and duplicate/lost/cancelled operational work. Name-substitution tests apply the same accepted/incorrect decisions to several participant identities. These synthetic outcomes are qualification fixtures, not SDK results.

One explicit sensitivity limit remains: swapping only the reported teleportation measurement-bit labels preserves this ideal fixture's joint distribution because both bits are uniform and corrected Bob outputs are independent of them. The test records that observational equivalence rather than claiming it detects the swap. Swapping the feed-forward controls, removing either correction, or dropping branches is detected. Future register-label certification needs an additional asymmetric diagnostic instance and a reviewed protocol amendment; the current fixture is not silently changed.

Remaining release gates include independent user/mathematical review records, adapter review, actual environment locks, dedicated-host sealing, the complete ten-block/warmup campaign scheduler and provider transport bindings. No SDK comparison may be published as qualified P1 evidence until the [roadmap gates](ROADMAP.md) are satisfied.

Kernel design references: [cgroup v2](https://docs.kernel.org/admin-guide/cgroup-v2.html), [seccomp filters](https://docs.kernel.org/userspace-api/seccomp_filter.html), and [libseccomp rule API](https://github.com/seccomp/libseccomp/blob/main/doc/man/man3/seccomp_rule_add.3).
