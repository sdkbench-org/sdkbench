# Compiler application development reading: 2026-11-19

Status: development-only local reading. This is not a prospective draw, a
resource-qualified campaign, a release gate, or a global SDK ranking. Historical
fixtures, adapters, budgets and acceptance thresholds were not changed.

## Question and scope

How do the current compiler workflows behave on small application circuits when
output-layout obligations are reported explicitly? The cohort contains ten
six-qubit circuits: QAOA, Ising, hopping, QFT and coherent repetition correction,
each on a line and a two-row grid. Recipes and application limitations are in
[the application protocol](COMPILER_APPLICATION_PROTOCOL.md).

The public development nonce is 32 repetitions of byte `01`. This same input
family is available for compiler development and must not become a blind test.
The seven workflows are the existing ordinary and target-artifact FlagQuantum
paths, ordinary Qiskit and Cirq paths, and the three existing matched-restoration
controls. Options and file hashes are retained in
[metadata](evidence/compiler-development-20261119/metadata.json).

The harness is SDKBench `d18c53e19134311d61e0c74012503e76941b4795`. Its generator,
adapters, restoration and independent evaluator match the files used for this
reading. FlagQuantum is the unmerged development revision
`338f9bb5051f37a9b8ee9c604d70e166db2a1f2a`, including bounded routing trials.
This does not establish an integrated or released FlagQuantum result. Qiskit
2.6.2 and Cirq Core 1.7.0 are the installed comparators.

## Correctness and observed counts

All 70 compilations passed the existing independent six-qubit acceptance: the
complete 64-by-64 operator, one common global phase, normalization, target gates,
coupling legality and final-layout reconstruction. There were no unsupported or
failed outcomes in this cohort. Raw output rows retain each numerical residual
and the adapter audit fields.

The following are sums over ten separate cases, not the width or depth of a
single executable:

| Workflow | Full CZ count | Two-body dependency depth |
| --- | ---: | ---: |
| FlagQuantum ordinary | 738 | 559 |
| FlagQuantum target artifact | 684 | 519 |
| Qiskit transpile | 538 | 407 |
| Cirq route and CZ optimization | 536 | 399 |
| FlagQuantum ordinary, restored control | 738 | 559 |
| Qiskit transpile, restored control | 700 | 526 |
| Cirq route and CZ optimization, restored control | 692 | 526 |

The ordinary Qiskit and Cirq workflows permit reported final permutations;
FlagQuantum already restores its output. Those original rows therefore measure
different delivered-layout obligations. They must not be presented as an
isolated synthesis comparison. The restored controls append the same independent
restoration policy to each ordinary workflow, including no operations for an
identity layout. That controls the output interface, but it is not an optimal
native fixed-layout compiler comparison: optimizers do not see the appended
suffix. See [the matched-layout control](COMPILER_MATCHED_LAYOUT_CONTROL.md).

Family totals across line and grid expose important differences hidden by the
aggregate:

| Family | FQ ordinary restored | FQ target artifact | Qiskit restored | Cirq restored |
| --- | ---: | ---: | ---: | ---: |
| QAOA | 114 | 110 | 122 | 126 |
| Ising | 96 | 96 | 106 | 106 |
| Hopping | 162 | 148 | 168 | 150 |
| QFT | 192 | 168 | 174 | 176 |
| Coherent repetition correction | 174 | 162 | 130 | 134 |

FlagQuantum's ordinary path remains behind both restored comparators in total
CZ count, with a particularly clear gap on coherent correction. Its target
artifact path has a smaller total in this cohort, but combines different
optimization and serialization work. Neither fact establishes superiority or
identifies a unique cause. Report each workflow and each family rather than
choosing the table that favors a participant.

## Measurement limits

The execution environment was macOS CPU, complex128 and one numerical thread,
with a shared host, no warmup and one compilation at seed zero for each workflow.
Seed zero is passed only through the existing declared adapter contracts;
deterministic SDKs do not gain a special tuning knob. Individual compilation
wall times are retained as diagnostic observations, not performance rankings.
There is no repeated seed/block distribution, confidence interval or reliable
peak-memory measurement.

The existing per-compilation 120-second alarm remained active. An additional
240-second outer process bound covered this reading, and all rows completed.
Linux cgroup, seccomp, pinned single-CPU isolation, immutable candidate admission
and the standard multi-block campaign were not run. Passing numerical
acceptance on this host does not satisfy those resource and provenance gates.

## Retained artifacts and next gate

- [Raw outcomes](evidence/compiler-development-20261119/outcomes.jsonl): all
  seventy rows, counts, residuals, diagnostic wall times and adapter audit fields.
- [Metadata](evidence/compiler-development-20261119/metadata.json): cohort,
  revisions, environment, unchanged options, acceptance and content hashes.

To reproduce the numerical reading, use `applications.fixture(6, family,
topology, "01" * 32)`, the frozen `CompilerAdapter` workflow names recorded in
metadata, compiler seed zero, and `p0.evaluators.routing` with the original
six-qubit W03 acceptance. This describes a source-development check; replay of
an admitted immutable campaign still requires the standard candidate CLI and
retained wheels/build records.

Before a comparative claim, integrate and freeze the intended compiler builds,
freeze the harness/configurations and cohort, then draw fresh prospective inputs
and run the complete resource-qualified campaign. Publish every failure,
unsupported case and regression, including cases that reverse these local
aggregate results. This reading must remain labeled development evidence after
that campaign exists.
