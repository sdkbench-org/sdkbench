# External scientific-program compiler results

This report retains the complete population of seven external QASMBench programs,
both target graphs and all four frozen workflows. Input-admission refusals,
operator execution failures and participant outcomes are separate observations.
No participant, compiler option, evaluator, threshold, repetition or resource
budget was changed after outcomes. No comparative result was rerun.

## Frozen scope and denominator

See the [source population](COMPILER_EXTERNAL_PROGRAM_QUALIFICATION_20261123.md),
[input decisions](COMPILER_EXTERNAL_INPUT_ADMISSION_20261123.md) and
[prospective execution and operational corrections](COMPILER_EXTERNAL_EXECUTION_FREEZE_20261123.md).
The population contains 56 intended source/target/workflow rows. Three admitted
programs yield six tasks and 24 executable rows; four refused source inputs retain
32 input-not-admitted rows. CC and BB84 contain quantum operations after a
measurement; both VQE sources fail syntax admission because `q` is undefined.
Those preparation refusals are not SDK failures. No twelve-wire source was admitted.

The exact exposure audit compared 8662 historical files, found no exact source or
canonical operation match and retained 242 gaps. It covers materialized declared
roots, not all history, private campaigns or developer knowledge.
`novelty_certified=false`; external source origin does not certify unseen
algorithmic knowledge. The publicly frozen population was not used to tune this
measured compiler revision. Future tuning against these inputs is development.

## Independent acceptance and workflow obligations

The complete installed dependency inventory and four candidate registrations
remain frozen. FlagQuantum uses source `f88ebc88f8584cd580802cd219ba16d935fa6715`;
Qiskit is 2.6.2 and Cirq Core is 1.7.0. The measured interpreter is Python 3.12.14
with CPU Torch 2.14.0. The native execution path is one CPU/thread per worker,
complex128/float64, 16 GiB aggregate cgroup peak, no swap and denied external
sockets. This is static exact compilation within numerical tolerances; there
is no gradient method, QPU, accelerator or distributed workload.

Each task retains ten independent process blocks, two warmups and three measured
positions per block, requested seeds 11/23/37/51/73 repeated twice, and participant
order rotation. All four workflows receive the identical canonical ordered gate
sequence, arbitrary-input semantics, identity initial layout, full CZ and arbitrary
one-qubit target operations, no ancillas and restored logical output order.
Qiskit uses level 2, exact synthesis and `qubits_initially_zero=False`; Cirq uses
RouteCQC and full-CZ synthesis. Ordinary paths include the same timed deterministic
layout restoration. FlagQuantum's artifact path also includes native validation,
provenance, restoration and executable serialization; timing across these
workflows does not isolate one optimization pass.

The unchanged evaluator independently recomputes CZ count and two-body dependency
depth and checks topology/layout, absolute semantic error <= 1e-8, zero relative
tolerance and normalization error <= 1e-10. Six-wire tasks use the complete
operator up to one common phase. Eight-wire DNN uses three complete output-state
probes; this is not universal equivalence proof. All observations remain
`publication_eligible=false` and `scalability_claim_allowed=false`.


## Complete measured outcomes

Twenty of 24 executable cases were accepted; four retained `error`. Across all
56 intended rows this is 20 accepted, four participant errors and 32
input-not-admitted. The 240 blocks retain 720 measured positions (600 accepted,
120 error) and 480 warmup positions. Maximum accepted numerical residual is
1.1072e-14. Producer-free replay verified 240 blocks and 825 campaign files.
The campaign returned 1 in 1019.991 seconds because of the four failed cases;
independent replay returned 0 in 163.212 seconds; the unchanged report tool's
second replay and summary returned 0 in 208.111 seconds. None exceeded its
prospective phase ceiling. These evaluation costs are separate from compile time.

The table uses independently recomputed CZ/dependency-depth ranges over accepted
records. Timing is the median of ten block medians, each based on three accepted
measurements after two warmups. The machine-readable summary retains every
sample, inclusive quartiles and block-median range. Memory is the maximum
aggregate cgroup peak for a complete block including imports, warmups, measured
work, export and descendants. Memory for a failed case is diagnostic only and
not evidence of a faster or smaller successful compilation.

| Instance | Workflow | Status | Accepted / 30 | CZ range | Two-body depth | Median ms | Maximum block MiB |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| EXT-02-LINE-08 | `cirq-release-restored` | accepted | 30 | 197 | 84 | 457.591 | 153.04 |
| EXT-02-GRID-08 | `cirq-release-restored` | accepted | 30 | 103 | 47 | 317.330 | 149.36 |
| EXT-03-LINE-06 | `cirq-release-restored` | accepted | 30 | 100 | 73 | 170.090 | 145.73 |
| EXT-03-GRID-06 | `cirq-release-restored` | accepted | 30 | 72 | 51 | 131.151 | 143.77 |
| EXT-04-LINE-06 | `cirq-release-restored` | accepted | 30 | 32 | 32 | 51.043 | 141.36 |
| EXT-04-GRID-06 | `cirq-release-restored` | accepted | 30 | 50 | 45 | 69.463 | 142.33 |
| EXT-02-LINE-08 | `fq-integrated-artifact` | error | 0 | — | — | — | 158.33 |
| EXT-02-GRID-08 | `fq-integrated-artifact` | error | 0 | — | — | — | 158.17 |
| EXT-03-LINE-06 | `fq-integrated-artifact` | error | 0 | — | — | — | 153.43 |
| EXT-03-GRID-06 | `fq-integrated-artifact` | error | 0 | — | — | — | 153.46 |
| EXT-04-LINE-06 | `fq-integrated-artifact` | accepted | 30 | 34 | 31 | 174.505 | 154.52 |
| EXT-04-GRID-06 | `fq-integrated-artifact` | accepted | 30 | 36 | 33 | 178.035 | 154.78 |
| EXT-02-LINE-08 | `fq-integrated-ordinary` | accepted | 30 | 270 | 114 | 318.118 | 164.11 |
| EXT-02-GRID-08 | `fq-integrated-ordinary` | accepted | 30 | 264 | 111 | 317.957 | 164.44 |
| EXT-03-LINE-06 | `fq-integrated-ordinary` | accepted | 30 | 108 | 72 | 80.168 | 156.25 |
| EXT-03-GRID-06 | `fq-integrated-ordinary` | accepted | 30 | 84 | 51 | 88.907 | 155.82 |
| EXT-04-LINE-06 | `fq-integrated-ordinary` | accepted | 30 | 32 | 30 | 16.342 | 152.76 |
| EXT-04-GRID-06 | `fq-integrated-ordinary` | accepted | 30 | 44 | 43 | 17.276 | 152.98 |
| EXT-02-LINE-08 | `qiskit-release-restored` | accepted | 30 | 136–142 | 47–65 | 19.952 | 81.28 |
| EXT-02-GRID-08 | `qiskit-release-restored` | accepted | 30 | 124–130 | 52–72 | 19.079 | 83.17 |
| EXT-03-LINE-06 | `qiskit-release-restored` | accepted | 30 | 94–104 | 61–77 | 11.424 | 70.13 |
| EXT-03-GRID-06 | `qiskit-release-restored` | accepted | 30 | 70–82 | 50–57 | 9.985 | 66.57 |
| EXT-04-LINE-06 | `qiskit-release-restored` | accepted | 30 | 28–32 | 26–32 | 6.295 | 64.54 |
| EXT-04-GRID-06 | `qiskit-release-restored` | accepted | 30 | 40–50 | 34–44 | 6.637 | 65.03 |

FlagQuantum's ordinary workflow was slower than Qiskit on every admitted task:
15.94/16.67 times on DNN line/grid, 7.02/8.90 on QAOA and 2.60/2.60 on Simon.
It used more CZs than every Qiskit observed seed on DNN and QAOA. On Simon its
counts overlap Qiskit's ranges. Its maximum block-memory peak was larger than
Qiskit's in all six cases. It was faster than Cirq in five tasks and slightly
slower on DNN grid (317.957 versus 317.330 ms); these short observations do not
establish statistical significance or an SDK-wide ranking.

The artifact workflow succeeded only on Simon. On the line it emitted 34 CZs
and depth 31, versus the ordinary workflow's 32 and 30: a quality regression,
in addition to higher latency. On the grid it reduced those measures to 36/33
from 44/43, but cost 178.035 ms versus 17.276 ms. Both artifact cases were slower
than the compared Qiskit and Cirq workflows and had larger block-memory peaks.
The native block optimizer's local strict-reduction rule does not guarantee an
improvement over a separately optimized ordinary whole workflow.

These observations supersede any suggestion from the three historical controls
that artifact gate counts are uniformly better or ordinary performance is close
to Qiskit. No universal superiority, confidence interval, optimality, device
fidelity, dynamic-circuit, symbolic-gradient or twelve-wire external claim is made.

## Host closure and next engineering decision

Fresh admission used CPU 96 with idle SMT sibling 288; the observer stayed on
CPU 0. Pre/post OS package and stable-file baselines matched; no foreign CI worker
was observed in the retained heartbeats, and no worker cgroup remained. The
original sixteen scheduling label sets were restored after both the blocked
first attempt and the completed second attempt. No machine/service restart,
kernel/driver change or unrelated process termination occurred. Directly
administered snapshots are not independent immutable-host attestation.

Keep production code and the comparison protocol unchanged by this report.
Priorities are the protected source-artifact capacity inconsistency, ordinary
whole-workflow latency and DNN/QAOA target-CZ quality. Profile development inputs
and inspect existing/upstream passes before selecting an implementation. Source
normalization, routing, native synthesis and evidence/serialization costs require
separate attribution. This population is now development data for subsequent
changes; a new prospective population is needed for new unseen-program claims.

## Artifact input-envelope failure

The four DNN/QAOA line/grid artifact cases retain `error`, specifically
`ValueError: circuit payload exceeds maximum entry count 4096`. The adapter's
`ProgramArtifactV2.from_circuit_ir` fails before calling target compilation.
The 20000-operation target allowance does not override the source envelope's
separate mapping/list entry limit. All error records and failed warmups remain
retained; no successful timing or valid output quality is assigned to these cases.

A separate post-observation local diagnostic using the identical measured
`_artifacts.py` implementation constructed the same source envelopes without
routing or target compilation. DNN has 2640 operations, 21143 mapping/list entries
and 232657 payload bytes; QAOA has 702 operations, 5637 entries and 61926 bytes.
Simon has 104 operations, 853 entries and 8992 bytes and its envelope constructs.
This explains the entry-bound refusal, distinct from the 16-MiB byte bound.
Nine unchanged FlagQuantum artifact-v2 candidate tests passed. This diagnostic is
not Linux performance evidence. The protected bound was not relaxed.

## Failed operational attempts

Initial admission refused selected-core activity before campaign/cgroup creation.
Its observer was pinned to the selected CPU and could contaminate the observation;
missing retained after-sample prevents exact attribution. The next driver placed
the observer on CPU 0 but its campaign supervisor inherited that restriction.
Campaign attempt 1 completed all 240 blocks as `access-blocked`, with 720
placeholder records and zero supervised participant executions or responses.
Producer-free replay and summary preserved the failure; it is not SDK performance.

Attempt 2 was separately published before any compiler outcome. It kept the
observer on CPU 0 and explicitly launched the unchanged CLI on CPU 96. A launch
control and the original fifteen resource controls passed. A new directory and
separate records preserve the failed attempt. All protocol limits and the original
reservation end remain unchanged. There were no compiler outcomes to select or
repeat in that prerequisite recovery.

## Supported reproduction entry points

```sh
PYTHONPATH=src python -m sdkbench.candidates.cli run --help
PYTHONPATH=src python -m sdkbench.candidates.cli replay --help
```

Use the exact frozen bundle, registrations and admitted cgroup/CPU environment.
The first command retains every candidate case and failure; producer-free replay
checks the retained complete manifest and independent verdicts. These commands
do not reserve a host or certify publication. Source/derived fixtures must retain
the original QASMBench LICENSE and NOTICE, unchanged; no upstream endorsement is
claimed.

The [complete intended-row ledger](COMPILER_EXTERNAL_RESULTS_20261123.json) embeds
the unchanged independent numerical summary, including every block sample.
The [public numerical evidence release](https://github.com/FlagQuantum/FlagQuantum-evidence/releases/tag/evidence-compiler-external-2026-11-23.1)
retains both operational attempts and the complete measured campaign. The archive
is 21,904,135 bytes with SHA-256
`2062cab0857de6088abe402d05ea7722dad8d37cc5cb13206a478f79e07428d8`.
Its per-file manifest has SHA-256
`596c3e69fe89f46b12730a07a1cadc4c4982f3f037597c078b445d30f519e201`.
Both identities were verified against downloaded draft assets before publication
on November 23, 2026. The release also includes checksums and the credential-scan
receipt; detailed private host/process snapshots are excluded. Disclosure changes
accessibility only, not the retained outcomes or claim eligibility.

## Repository verification

The exact executable harness head passed all fourteen CI checks before execution.
Fresh local preparation/audit tests passed 37 tests and skipped 21 tests in
12.37 seconds because optional parser/preparation SDK dependencies are absent
from this local environment. An initial invocation omitted `PYTHONPATH=src` and
failed collection; the corrected invocation is the reported run. This local
subset does not replace the exact-harness CI or the completed Linux controls.
The Linux launch resource controls passed all fifteen tests. The independent
measured campaign and producer-free replay are separate evidence.
