# External-program compiler qualification population

Status: population declaration before reading selected circuit contents or
compiler outcomes. This document does not admit an importer, execute a campaign,
claim an unseen-program result or change the acceptance protocol. The
[machine-readable population](COMPILER_EXTERNAL_PROGRAM_POPULATION_20261123.json)
retains all original path/blob identities and pre-inspection scope.

## User need and complete population

A developer receiving an existing scientific or application circuit needs a
correct native program for a connected device graph. Generated application
recipes are useful controls, but fresh parameters in already inspected recipes
do not establish unseen-program coverage. This next qualification uses a fixed
external source census rather than sampling convenient outcomes.

The source is [QASMBench](https://github.com/pnnl/QASMBench) at immutable revision
`357b942396d5c2b7cbc1c229c585a6ef5ccaebac`. Its repository tree metadata, top-level
LICENSE and NOTICE were inspected. None of the selected QASM files has been read
in this preparation. Selection is every original, non-transpiled `.qasm` with
logical width 6, 8 or 12 in `small/` and `medium/`; the basename matches the parent
program name. All seven matches are retained, including known algorithm families
and potentially unsupported or expensive files. There is no gate-count,
file-size, expected-quality, parser-success or family-based filter.

| Original program | Width | Git blob |
| --- | ---: | --- |
| `medium/cc_n12/cc_n12.qasm` | 12 | `d00b7347456b43f36cd384a31d251b4433998a02` |
| `small/bb84_n8/bb84_n8.qasm` | 8 | `379af7d98bd9189f0f4214c6310d0c77aff5fb9e` |
| `small/dnn_n8/dnn_n8.qasm` | 8 | `f25d5d1a0379f55c5cc7978b75a888ce9825a666` |
| `small/qaoa_n6/qaoa_n6.qasm` | 6 | `326787ca86e0a5aa716687345bcad583e1420c7f` |
| `small/simon_n6/simon_n6.qasm` | 6 | `4f3fbc26538ffa072aad76a0d37d5ca58476b25b` |
| `small/vqe_uccsd_n6/vqe_uccsd_n6.qasm` | 6 | `516adea7180da8f944235de92077338ef42a32ce` |
| `small/vqe_uccsd_n8/vqe_uccsd_n8.qasm` | 8 | `410ce5db21a65ba6af3f04cfe29c2567fb70e5f1` |

Use both line and 2-by-(n/2) grid targets for every source. Preserve every logical
wire, identity initial/output order, arbitrary-input semantics, no ancillas,
arbitrary one-qubit gates and full CZ target interactions. This yields fourteen
intended task instances and four separate existing delivered workflows:
`flagquantum-ordinary-restored`, `flagquantum-target-artifact`,
`qiskit-transpile-restored`, `cirq-route-cz-restored`. Do not select the better
FlagQuantum workflow after observing results. The artifact workflow includes
validation, provenance and serialization, so cross-workflow times do not isolate
one compiler pass. No hardware/native fidelity claim follows from abstract graphs.

## Importer admission before circuit inspection

An importer is a missing preparation capability; the current application builder
only emits its five implemented recipe families. Do not modify P0 semantics,
reference construction, evaluators, replay, adapters, thresholds or resource
supervision to make an external input pass. Do not introduce benchmark-specific
compiler changes. Develop and freeze a separate deterministic source converter
before reading this population's circuit bodies. Prefer an existing maintained
parser or repository importer over inventing another language implementation;
record its exact version, ownership and dependencies. A participant parser must
be clearly identified as preparation infrastructure, with no compiler pass,
transpilation, routing, optimization or simplification executed during import.
Every participant must receive the exact same canonical source operation list.

The task is compilation of the coherent unitary prefix, not sampled classical
output or dynamic execution. Record raw source bytes, SHA-256, all included gate
definitions, original register/wire order and a transformation trace. Terminal
measurements may be removed only when no subsequent quantum operation depends
on their outcomes or occurs afterward. Reset, classical feed-forward,
mid-circuit measurement, opaque/unknown gates, unresolved parameters and
unbounded expansion must refuse input admission. Report input-admission refusal
separately from participant unsupported/compile/resource/semantic failure; retain
all four intended participant rows for that source/target, with no fabricated
execution or timing. Do not replace a refused program.

Declare gate expansion rules, index/endian convention, scalar-angle handling,
global-phase scope, barrier treatment, structural limits and numerical checks
in the importer proposal before inspecting circuit contents. Preserve relative
phase. A global phase may be ignored only by the existing whole-program operator
contract. Changes needed after reading these programs require a separately
versioned proposal and reclassification as development; they cannot repair the
same prospective qualification silently.

Importer conformance must include independent analytic complete operators,
reversed operands, custom gate definitions, terminal-measurement boundaries,
register ordering and negative malformed/dynamic/budget inputs. Compare the
converted coherent prefix against a second independently implemented parser or
source interpreter before compiler execution. Cross-parser disagreement is an
input failure, not a reason to choose the parser favorable to a participant.
The independent SDKBench bit-block and dense references remain authoritative for
compiled-program acceptance.

## Novelty and execution freeze

Before any participant execution, audit raw source and canonical operation
fingerprints against previous SDKBench and FlagQuantum checked-in evidence,
retained archives and available campaign manifests. Record exact audit roots,
commands, source revisions, access gaps and all matches. A text search alone
cannot establish circuit novelty. Known matches remain controls, with their
prior exposure disclosed; no replacement draw or relabeling as held out.
If historical archives are unavailable, explicitly limit the novelty claim.
External origin does not prove an algorithm itself was unknown to developers.

The census requires no random draw. Probe preparation is copied unchanged from
the frozen width-specific W03 fixture. Program selection must not depend on a
probe, SDK result or compilation success. Genuinely unseen-program qualification
is conditional on importer admission, the novelty audit, publicly frozen compiler
source/wheel bytes, dependencies, registration options, complete bundle hash and
qualified environment before participant outcomes. If this population informs
compiler tuning, classify it as development for that later compiler revision.

For the first execution, use the same four wheel/configuration identities as the
November 23 Linux historical-control study, subject to reverified installed
payloads. FlagQuantum's wheel source is
`f88ebc88f8584cd580802cd219ba16d935fa6715`; Qiskit is 2.6.2 and Cirq Core is
1.7.0. Retain the exact registration bytes and complete installed dependency lock.
The separately frozen execution declaration must identify the final importer
and harness revision; this population document does not bind unknown code or
permit measuring before that declaration.

## Unchanged acceptance and budgets

Copy each width-specific W03 acceptance and resource object verbatim from the
existing frozen bundle. Six wires receive full-operator acceptance up to one
common global phase; widths eight/twelve receive three complete state probes,
explicitly not universal equivalence. Retain 1e-8 absolute semantic error,
1e-10 normalization error, zero illegal interactions, and independent count,
two-body dependency-depth, layout and full-CZ checks.

Retain ten process blocks, two warmups and three measured compilations per block,
compiler seeds 11/23/37/51/73 repeated twice, participant order rotation, one
CPU/thread, 16 GiB aggregate cgroup peak, no swap/network, descendant cleanup,
120-second compilation limit and 600/900/1800-second whole-case caps by width.
All fourteen admitted sources/targets would produce 560 blocks, 1680 measured
records and 1120 warmups over four registrations. Input refusals reduce actual
execution, not the denominator of intended cases. Preserve failed warmups and
all partial attempts. No budget increase, favorable rerun, reduced repetitions,
selected seed or post-inspection case removal is allowed.

The complete worst-case measurement ceiling is 50400 seconds (fourteen hours),
excluding preparation, reference construction and independent replay. Establish
separate bounded preparation/replay budgets before admission and refuse to start
unless the remaining exclusive window accommodates their sum and cleanup slack.
Large inputs can time out under the existing budget; that is a result to retain.
Use a dedicated Linux host with verified `memory.peak`, SMT sibling idleness,
pre/post baselines and full activity records. Reservation alone is insufficient.
Do not restart a machine/service, upgrade kernel/drivers or stop existing jobs.
Restore original runner scheduling labels after draining naturally and completing
or aborting the study.

Report every intended source/target/workflow row, all failure classes, gate-count
and dependency-depth ranges, process-block compile medians and distributions,
aggregate block-memory peaks and maximum numerical residuals. Keep input costs,
compiler costs, artifact obligations and independent evaluation costs separate.
Replay all retained outcomes without producer SDK imports before conclusions.
Publication eligibility stays false until separate publication/build/host review.
This study cannot establish global SDK ranking, molecular accuracy, algorithmic
advantage, dynamic execution, gradient support or scalability.

## Licensing and supported existing workflow

Preserve QASMBench's original LICENSE and NOTICE verbatim with every redistributed
source and derived fixture archive. Its custom Battelle license requires source
copyright/conditions/disclaimers and corresponding binary-distribution materials;
do not relabel external sources Apache-2.0. Record modified/converted forms and
source identities. Attribution and the required notices remain visible; no
endorsement is claimed.

The implemented execution surface remains:

```sh
PYTHONPATH=src python -m sdkbench.candidates.cli run --help
PYTHONPATH=src python -m sdkbench.candidates.cli replay --help
```

Expected: existing explicit bundle/registration/CPU/cgroup parameters and
producer-free replay. No external-source importer command is implemented or
advertised by this declaration. The ordinary supported application workflow is
still `python -m sdkbench.candidates.application_bundle --help`; its five recipe
families remain development inputs. This document changes no public API,
participant implementation, evaluator, threshold, protocol budget or installed
dependency. Importer implementation and scientific qualification remain pending.
