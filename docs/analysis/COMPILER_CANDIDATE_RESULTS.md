# Compiler candidate engineering results — 2026-11-19

All 12 workflow/case combinations passed the unchanged frozen routing acceptance.
The run contains 120 fresh process blocks, 240 warmups and 360 measured outputs.
Every measured output and warmup was retained; no failures, unsupported cases or
outliers were removed. GitHub run 44466785968 completed successfully, including
independent replay and cgroup cleanup. Local SDK-free replay independently
verified 515 campaign files and all 120 blocks.

The result is a bounded engineering study, not a global SDK ranking. FlagQuantum
still emits more CZ gates on these three workloads than the declared Qiskit and
Cirq workflows. Automatic target-aware rewriting reduces FlagQuantum's retained
baseline counts, but does not close that gap and carries substantial end-to-end
compilation overhead.

## Immutable inputs and participants

The frozen P0 bundle, evaluator, thresholds, seeds, ten-block protocol and
resource limits were unchanged. The complete source/configuration and
installed-file identities appear in [the machine-readable summary](compiler-candidate-summary.json).

- Harness: `1d52d14d2761d434a4fb5a34c120938d419e17b6`.
- FlagQuantum source: `5553fb3d2e186995c7fc27c0fa0859c38abd5a2a`, version 0.4.0,
  built with PyTorch 2.10 and installed as the retained Linux Stable ABI wheel.
  Wheel SHA-256: `89c791ebc7bc5c3d81862337db3498dbbd2fe5fb6a6f6a30c3a97668d8686fa5`.
- Qiskit 2.6.2 and cirq-core 1.7.0: published PyPI wheels, verified against
  retained release metadata and their installed payloads.
- Shared measurement environment: Python 3.12.14, PyTorch 2.14 CPU, NumPy 2.5.5,
  Ubuntu 24.04 runner, AMD EPYC 9V74; one pinned CPU, one numerical thread,
  16 GiB per block, seccomp network denial and cumulative case budgets.

FlagQuantum PR #1226 was integrated as
`5baf8d97d6575390c24cb8075ba629ecffb71786`. The source parent above is the
actual measured revision. A comparison against the integration commit found
only the intervening QEC changes and documentation, not compiler changes;
the two full repository trees are nevertheless different.

This hosted VM is an observed engineering environment. It is not the dedicated,
sealed publication host required by the measurement protocol. Timing values
below are descriptive observations on that VM, not certified speed rankings.
Build observations and release metadata checks are not independent attestations.

## Results

Each row has 30/30 accepted measured outputs and 20/20 accepted warmups.
CZ and depth ranges include every measured output. Time is the median across
ten block medians, each computed from all three measured compilations.
Peak memory is the maximum kernel cgroup peak across blocks and includes imports,
warmups, compilation and export; it is not isolated compiler workspace memory.

| Workflow | Task | CZ range | Depth range | Median compile (s) | Time IQR (s) | Peak block MiB |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| FlagQuantum ordinary | ROUTE-LINE-06 | 138 | 115 | 0.024560 | 0.000595 | 153.6 |
| FlagQuantum ordinary | ROUTE-GRID-08 | 146 | 82 | 0.029236 | 0.000538 | 154.0 |
| FlagQuantum ordinary | ROUTE-LINE-12 | 438 | 206 | 0.062441 | 0.001194 | 158.9 |
| FlagQuantum target artifact | ROUTE-LINE-06 | 124 | 101 | 0.740755 | 0.055406 | 158.0 |
| FlagQuantum target artifact | ROUTE-GRID-08 | 140 | 82 | 0.775635 | 0.031398 | 158.6 |
| FlagQuantum target artifact | ROUTE-LINE-12 | 422 | 192 | 2.586627 | 0.223563 | 172.8 |
| Qiskit transpile | ROUTE-LINE-06 | 68 | 65 | 0.008343 | 0.000626 | 66.5 |
| Qiskit transpile | ROUTE-GRID-08 | 85 | 45–47 | 0.009701 | 0.001258 | 66.6 |
| Qiskit transpile | ROUTE-LINE-12 | 339–348 | 192–219 | 0.022697 | 0.001389 | 81.4 |
| Cirq RouteCQC + CZ | ROUTE-LINE-06 | 68 | 65 | 0.124122 | 0.001974 | 145.5 |
| Cirq RouteCQC + CZ | ROUTE-GRID-08 | 84 | 52 | 0.158246 | 0.001647 | 146.8 |
| Cirq RouteCQC + CZ | ROUTE-LINE-12 | 360 | 198 | 0.563941 | 0.006995 | 161.6 |

## Interpretation and attribution limits

The target-artifact workflow reduced the native baseline from 138 to 124 CZ
on LINE-06, 146 to 140 on GRID-08 and 438 to 422 on LINE-12: reductions of
10.1%, 4.1% and 3.7%. Its common dependency depth was 101/82/192 versus the
ordinary path's 115/82/206. In particular, GRID-08's gate reduction did not
reduce this depth measure. Within the target-artifact invocation the compiler
retained and reported its native baseline; those baseline counts are labeled
SDK-reported, while the output counts are independently recomputed.

Both FlagQuantum workflows restore logical output placement. Qiskit and Cirq
may return a final permutation, which the independent evaluator reconstructs.
All satisfy the frozen task contract, but the layout obligations differ.
Their difference is a valid end-to-end user-workflow observation, not an
isolated estimate of routing or local-synthesis quality. The historical
108/96/375 expert counts used a free final layout and must not be substituted
for the restored baseline.

Qiskit/Cirq output fewer CZ gates in every case here. Depth is not uniformly
ordered: on LINE-12, FlagQuantum target depth 192 is lower than Cirq's 198 and
falls at the low end of Qiskit's 192–219 range, despite its higher CZ count.
A scalar claim that one workflow wins every objective would misstate this.
Qiskit exhibited seeded output variation on GRID-08 depth and LINE-12 counts
and depth; FlagQuantum and Cirq outputs were invariant over the requested seeds
because those workflows do not expose compiler seed control.

Target-artifact compilation took roughly 0.74/0.78/2.59 seconds here, versus
0.025/0.029/0.062 seconds for ordinary FlagQuantum compilation. It includes
native lowering, local synthesis, routing/evidence replay, verification,
artifact construction and serialization. This experiment does not isolate
which stage causes the overhead. It would be incorrect to attribute the entire
difference to KAK or SABRE, or to remove evidence work selectively from its timer.
Qiskit's observed medians were 0.0083/0.0097/0.0227 seconds and Cirq's were
0.124/0.158/0.564 seconds under their declared, different workflows.

Six-qubit acceptance checks every operator column up to one global phase.
Eight- and twelve-qubit acceptance checks three full-output probe states only;
those checks are not an arbitrary-input equivalence proof. Correctness on these
fixtures does not establish symbolic parameter preservation, dynamic control,
directed targets, arbitrary initial layouts, real hardware performance or
broad application coverage. Those require their own cases.

## Retained evidence and reproduction

[Evidence index](evidence/compiler-candidate-index.json) records hashes and the
original GitHub artifact. [The lossless archive](evidence/compiler-candidate-1d52d14.tar.gz)
contains every original campaign file, including normalized outputs, requests,
responses, warmups, execution telemetry, compiler artifact envelopes, manifests,
release metadata, build log/record and environment lock. Its 527 files were
compared byte-for-byte with the downloaded evidence. Large binary wheels and
source archives remain in the original GitHub artifact; their hashes are in
the index. The original artifact has finite retention, so reproduce builds from
the recorded revision or preserve that artifact for longer-term build auditing.

```sh
mkdir /tmp/sdkbench-candidate-replay
tar -xzf docs/analysis/evidence/compiler-candidate-1d52d14.tar.gz \
  -C /tmp/sdkbench-candidate-replay
PYTHONPATH=src OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 \
  python tools/compiler_candidate_report.py \
  --directory /tmp/sdkbench-candidate-replay/campaign \
  --output /tmp/sdkbench-candidate-summary.json
```

Expected: 12 cases, 120 verified blocks, 515 verified campaign files,
all cases accepted, and `publication_eligible=false`. Replay needs SDKBench and
NumPy, not any participant SDK. It validates normalized output semantics and
compiler-file hashes, not the internal semantics of serialized SDK envelopes.

## Next evidence and product work

1. Freeze prospective application generators and configurations before revealing
   cases, then run QAOA, dynamics, chemistry, QFT and coherent QEC families with
   broader topology coverage and explicit symbolic/unsupported cases.
2. Use separate controlled studies for final-layout restoration, routing/search,
   target lowering and synthesis/evidence cost. Keep the default workflow as its
   own result; do not silently replace it with expert settings.
3. Improve the ordinary native target workflow under an explicit approved API
   contract, and profile artifact-stage overhead before selecting optimizations.
4. Requalify any new compiler/configuration under the unchanged diagnostic bundle
   and a fresh prospective corpus. Keep this run as development evidence.

No parity or superiority claim is warranted by this campaign.


## Separate profiling diagnostic

A subsequent single warm cProfile invocation on macOS used the same FlagQuantum
source-built wheel and LINE-06 input. This is an instrumented local diagnostic,
not part of the Linux campaign or a cross-SDK timing comparison. Its metadata and
raw tables are under [source-probes](source-probes/compiler-profile-20261119.json).

The target-artifact invocation made approximately 5.72 million function calls.
Of its 0.720-second instrumented cumulative adapter time, 74 calls to
`CircuitIR.content_hash` accumulated about 0.425 seconds. Nested serialization
and `_encode_value` dominate this chain. `optimize_native_blocks` accumulated
0.191 seconds, and its independent verification accumulated 0.131 seconds.
These cumulative times overlap and must not be added. Only 0.056 seconds was
attributed to the 53 `_cz_blocks._candidate` calls. This directs investigation
toward repeated IR encoding and evidence/replay construction, not a conclusion
that numerical synthesis alone causes the overhead.

The ordinary invocation made approximately 226,000 function calls with four
content-hash calls. The profiles identify optimization opportunities, not
permission to skip validation, alter identities or cache hashes globally for
mutable nested IR data. Any performance change must preserve tamper rejection,
replay and serialization equivalence and be remeasured independently.

## Additional development reading

The [2026-11-19 application reading](COMPILER_DEVELOPMENT_20261119.md) records ten
six-qubit application cases across seven existing workflow configurations using
an unmerged FlagQuantum source revision. It includes complete-operator
acceptance and matched-restoration controls, but no resource qualification or
prospective draw. Its results are separate development observations and do not
replace the frozen Linux campaign above.
