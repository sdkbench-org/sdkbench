# Native compiler integration proposal for FlagQuantum

This engineering plan is informed by the [routing attribution study](FLAGQUANTUM_ROUTING_ANALYSIS.md). The implementation status below distinguishes delivered native changes from outstanding product and comparative qualification work. The intended destination is FlagQuantum's own IR, target model and pass pipeline. Mature algorithms and necessary implementation should become native passes with explicit contracts and provenance. SDKBench remains an independent consumer and evaluator.

## Architecture and ownership

The proposed flow is: FlagQuantum IR validation and normalization; dependency/frontier analysis; contract-aware placement and routing; target gate lowering; local target-aware resynthesis and cleanup; final topology, basis and layout validation. Analysis results and layout maps belong to the native compilation context. Stage ordering and bounded iteration belong to the pass manager. The public ordinary compilation entry point should construct this pipeline from the target and requested objective.

Each pass must preserve instruction semantics, symbolic parameter identity, operand order and phase information, or explicitly reject the unsupported domain. Layout is an output contract: record both maps, compose them across passes, propagate measurement mappings and restore only when requested by the caller or required by an external interface. Arbitrary-input compilation must never assume unused wires start in zero. Existing target-independent optimization should retain its own contract; target-dependent synthesis belongs in a target-aware stage.

## Delivery sequence

The immediate priorities are (A) routing/layout orchestration using existing SABRE, especially automatic selection and the ordinary default workflow, and (B) target-gate optimization of local two-qubit blocks, including reversed operands and final-permutation tracking. Additional routing algorithms come after these two deliverables and require evidence of a remaining need. SABRE means SWAP-based BidiREctional heuristic search; see the [original mapping paper](https://arxiv.org/abs/1809.02573).

| Stage | Native work | Acceptance gate |
| --- | --- | --- |
| 1. Make existing capability reachable | Reuse the existing SABRE implementation, layout metadata/removal and native legalization/optimization in an explicit target-aware pipeline. Expose final-layout policy, objective, seed and budget through a coherent public API. | Ordinary documented invocation reproduces the explicit expert pipeline's semantics and records the actual stages. No workload IDs or circuit-size thresholds selecting benchmark answers. |
| 2. Integrate local synthesis | Reuse existing FlagQuantum two-qubit synthesis where appropriate. Collect safe blocks on a physical qubit pair, preserve each instruction's operand-to-local-basis mapping and resynthesize for the actual target CZ cost. Consider direction, gate availability, declared error and final permutation. | Full-operator tests include both SWAP/CX operand orders, generic two-qubit unitaries, singular/near-singular decompositions and parameter boundaries. Never replace a block with a higher-cost candidate under the same declared scalar objective. |
| 3. Improve routing on native IR when justified | Add or improve dependency frontiers, future-interaction scoring, bounded candidate SWAP evaluation, decay and deterministic tie-breaking. Keep initial-placement search separate from routing. | Fixed-initial and free-initial tests are separate. All routes obey edges, preserve bijective mappings and finish within the declared global search budget. |
| 4. Stabilize defaults | Select a bounded policy using a broad development corpus and a held-out evaluation corpus. Choose a declared cost objective; report count/depth alternatives when objectives conflict. | Regressions, seed spread, compile time, memory, unsupported cases and provenance are published. SDKBench registers a new version/configuration and reruns the unchanged external acceptance checks. |

Stage 1 is likely the fastest route to usable improvement because the measured native controls already close much of the count gap. Simply changing one routing string is insufficient: persistent layout with restoration regresses on two of the three inputs, and synthesis after basis lowering has different opportunities from target-independent optimization.

Initial placement must remain identity for the current frozen tasks. A future workload allowing placement search needs a distinct contract and registration; a native compiler may support both. Native multi-trial search is legitimate only within an explicit total CPU/wall/memory budget. Candidate selection must use the user's objective and retain the best valid incumbent so budget exhaustion has a defined outcome.

## What to learn or reuse from other compilers

The measured implementations are related but not identical:

| Participant version | Routing implementation in this study | Consequence |
| --- | --- | --- |
| FlagQuantum 0.3.1 | Native SABRE-style frontier/lookahead planner is available; deterministic lexicographic tie-breaking. The registered baseline instead uses per-gate restoration. | First fix automatic selection and layout orchestration; the presence of a SABRE implementation does not establish parity with another implementation. |
| Qiskit 2.6.2 | `SabreSwap` documents SABRE with LightSABRE modifications and multiple seeded trials. | Search effort, tie-breaking and surrounding passes differ from FlagQuantum even when both request SABRE. Distinguish external experiment seeds from internal trials. |
| cirq-core 1.7.0 | `RouteCQC` processes disjoint two-qubit timesteps and scores candidate SWAPs using lookahead. | Shared frontier/lookahead ideas do not make it the same SABRE implementation. The benchmark explicitly supplies identity placement rather than its default mapper. |

These implementation observations were checked against the installed cohort sources `flagquantum/compiler/sabre.py`, `qiskit/transpiler/passes/routing/sabre_swap.py` and `cirq/transformers/routing/route_circuit_cqc.py`. Algorithm labels alone do not specify a compiler: placement, routing, final-layout obligations, target lowering and resynthesis all affect the output. Compare their full declared pipelines and search budgets.

Qiskit's [transpiler documentation](https://quantum.cloud.ibm.com/docs/en/api/qiskit/transpiler) describes DAG-based passes, shared analysis properties and configurable staged pipelines. These provide useful design references for dependencies, layout state and pass contracts. Qiskit passes are coupled to its IR, analysis context and accelerated implementation; transferring a few Python files is not a self-contained migration. Choose individual algorithms or implementation kernels, pin their source revision and map their inputs/outputs explicitly to FlagQuantum types.

Cirq's [RouteCQC description](https://quantumai.google/cirq/transform/routing_transformer) explains timestep/frontier processing, executable-operation draining and scored candidate SWAP insertion. These ideas can be implemented over native FlagQuantum instruction dependencies without adopting Cirq's circuit or qubit classes. Its full-CZ synthesis behavior is a useful differential reference. Any reused implementation needs its actual protocol and numerical dependencies audited before porting.

The first decision should be whether existing native capability is adequate, then whether a missing part warrants algorithm reimplementation, source adaptation or a narrow reusable kernel. An external Qiskit/Cirq compiler backend can serve as an explicitly labeled optional interoperability path and a differential test reference. Results using that path must name the external compiler and version. Such a backend does not constitute the native integration proposed here.

Qiskit and Cirq publish Apache-2.0 license texts in the [Qiskit repository](https://github.com/Qiskit/qiskit/blob/main/LICENSE.txt) and [Cirq repository](https://github.com/quantumlib/Cirq/blob/main/LICENSE). Before copying code, inspect the exact pinned files and their dependencies, preserve applicable copyright/license/NOTICE material, identify modifications and record upstream origin. Algorithm reimplementation should cite its source publications and describe differences. Attribution belongs in source and developer documentation even when end-user package branding remains independent.

## Required validation

Use independent matrix/operator references for small circuits and contract-appropriate probes at larger sizes. Differential comparisons with Qiskit or Cirq supplement independent correctness checks; matching their output or counts is not a correctness oracle. Cover reversed operands, global phase, disconnected/directed graphs, zero gates, repeated remote interactions, arbitrary initial states, output permutations, measurements, symbolic shared parameters, unsupported instructions and budget exhaustion. Unsupported domains must be explicit, with no silent numerical binding or dropped operations.

The reversed two-qubit SWAP/CX reproducer should reach at most two full CZs when identity final layout and that basis are required, while satisfying the original tolerances. This is a local regression target supported by a known equivalent circuit, not a gate-count target for all circuits. The historical 108/96/375 CZ counts belong to expert configurations allowing a free final layout. They must not be compared with restored-layout artifact outputs as an isolated synthesis improvement. The corresponding restored-layout native baseline was 138/146/438 CZ; local target-stage probes produced 124/140/422 CZ. These local diagnostics are not full protocol measurements, universal targets or proofs of optimality.

Evaluate generated families, application circuits and held-out topologies in addition to the three frozen SDKBench inputs. Separate target-aware product defaults from tuned expert searches. For each, report entangling count, common dependency depth, compile time, memory, seeds, failure rates and the exact layout/basis/error obligations. The default policy should be chosen by user objectives and general workloads, never by passing SDKBench specifically.

## Proposed implementation boundary

FlagQuantum should own the IR analyses, target-dependent passes, orchestration and public API. SDKBench should own the neutral task specification, independent acceptance, resource enforcement and transparent adapter registration. Improvements go upstream and are then measured as a new participant version. This document does not modify FlagQuantum, claim that either compiler has been ported, or replace historical results.

## Candidate qualification follow-through

The [compiler candidate qualification protocol](COMPILER_CANDIDATE_QUALIFICATION.md)
specifies separate source/configuration registration, unchanged frozen routing
acceptance and resource limits, layout-aware attribution, and prospective
held-out gates. Its admission, adapters, runner and replay are implemented; positive Linux
campaign evidence is retained in [the result report](COMPILER_CANDIDATE_RESULTS.md);
prospective held-out qualification remains pending. It
does not replace the historical routing results.


## Delivered implementation and remaining scope (2026-11-19)

FlagQuantum PR #1219 introduced native automatic routing selection and bounded
CZ resynthesis. PR #1226 integrated the automatic full-CZ block stage into the
qualifying target-artifact pipeline and was merged as
`5baf8d97d6575390c24cb8075ba629ecffb71786`. Its measured source parent is
`5553fb3d2e186995c7fc27c0fa0859c38abd5a2a`. All 239 non-skipped PR checks passed;
three conditional checks skipped. The separately bounded local full runtime
suite timed out and is not counted as passing.

The automatic artifact stage preserves a native baseline, checks complete
local operators, accepts only strict CZ reduction and writes the approved v4
many-to-many evidence. It currently requires RX/RZ/full-CZ, absent or undirected
unallocated topology and identity initial placement. Symbolic, trainable and
batched values are collection boundaries. The artifact layout is restored.
Read-only Runtime and offline Deployment consume the evidence. These statements
concern local compilation and evidence, not hardware execution or SDK ranking.

The ordinary `compiler.compile` path already selects routing automatically;
it does not call the target-artifact block stage. A coherent ordinary
user-facing target workflow, broader target/layout admission and any additional
routing search remain separately scoped product work. Existing protected API
and serialization changes require their approved proposals; the artifact
implementation does not implicitly authorize them.

The source-build/published-wheel campaign compares four explicitly different
workflows under the same frozen task acceptance and Linux resource limits.
The first complete campaign and independent replay are recorded. Prospective
application-family coverage, parameter preservation, further resource tradeoffs
and publication qualification remain necessary
before claiming parity or superiority. Local gate-count examples do not close
those gates.
