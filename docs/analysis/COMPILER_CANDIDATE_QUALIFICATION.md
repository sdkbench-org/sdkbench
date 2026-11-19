# Compiler candidate qualification protocol

Status: source-build and published-wheel observation, registration admission, four compiler adapters,
the frozen campaign runner and independent replay are implemented. Full native
campaign execution and publication qualification are pending. This document specifies the next
engineering campaign; it is not a result or a ranking. See
[`candidates/README.md`](../../src/sdkbench/candidates/README.md) for the implemented
entry points, limits and focused verification. The historical P1b and
routing-attribution registrations, fixtures, thresholds, resources and archives
remain the baseline. No development checkout is admitted as an old release.

## Users and question

A circuit developer needs a correct executable circuit for a specified device
connectivity and gate family, without selecting undocumented expert passes.
A compiler developer also needs controlled configurations to locate overhead.
These are distinct questions: measure the documented ordinary workflow and
explicit expert configurations as separate, content-addressed registrations.
Any supported SDK may register either workflow under the same requirements.

The question is whether an identified new compiler/configuration improves the
accepted output or resource tradeoffs for those users. An algorithm name, a
small reproducer, or one lower gate count does not answer that question.

## Source and configuration admission

Each participant/configuration must record:

- SDK distribution name and actual installed version; immutable source commit
  when built from source; source archive and built wheel SHA-256; build command
  and build environment. A version string alone cannot identify a checkout.
- Installed non-bytecode file fingerprint, complete dependency/environment
  observations and SDKBench source fingerprint, including the new adapter and
  runner. Published release comparators retain the exact wheel, version-specific
  PyPI JSON response, its hash and declared file origin instead of fabricated
  source-build evidence. Keep observed engineering hosts labeled as unsealed.
- Public entry point, all explicit options and remaining defaults, target basis,
  precision, initial and final layout obligations, seed support, search/trial
  effort, permitted ancillas, compiler objective and stage ordering.
- Native versus external compiler ownership. An external Qiskit/Cirq compiler
  backend must be attributed as such, regardless of its caller's package name.

Use the existing `Registration` and identity mechanism. Bind these facts into
its configuration/component hashes rather than creating a parallel identity
schema. Parent and worker must verify the admitted implementation before SDK
execution. A missing, changed or mismatched component produces a retained
non-success outcome. Do not replace a pinned-version check with a permissive
check in a historical worker.

## First campaign: unchanged frozen routing tasks

Run ROUTE-LINE-06, ROUTE-GRID-08 and ROUTE-LINE-12 from the existing P0 bundle
through its unchanged record, case and workflow evaluators. Preserve their
fixture and bundle hashes, semantic thresholds, normalization, seeds, warmups,
repetitions and complete-case accounting.

| Requirement | Evidence |
| --- | --- |
| Identity initial placement, no ancillas | Verify the returned initial map and physical width; reject violations. |
| Full CZ interactions on target edges | Feed normalized artifacts to the existing independent routing evaluator. Arbitrary one-qubit unitaries remain subject to its existing checks. |
| Final permutation allowed | Submit the actual final map. Restoring it is valid but its cost remains part of that configuration. Never compare restored and free-layout outputs as an isolated synthesis experiment. |
| Arbitrary input semantics | Keep full-operator verification for six qubits and the explicitly limited three-probe verification for the larger frozen cases. Do not relabel probes as a full proof. |
| Complete timing protocol | Ten fresh process blocks; two warmups and three measured compilations per block. Retain and validate warmups. Preserve the ten frozen compiler seeds even for deterministic participants. |
| Per-compilation bound | Existing terminating 120-second kernel alarm, including normalization inside the registered compile interval. |
| Cumulative case budgets | Existing 600/900/1800-second limits, including this case's imports, warmups, measurements, independent validation and evidence export; exclude other participants' work. |
| CPU and memory | Existing Linux cgroup/seccomp supervisor: one CPU, one numerical thread, 16 GiB, no sockets, no memory-swap allowance, descendant cleanup and peak-memory evidence. |

Keep all SDKs/configurations serial and counterbalance their order by block.
Changing an SDK's version or pipeline creates a new registration, never a
replacement for historical outcomes. Installation failures, unsupported
capabilities, errors, OOMs and timeouts remain in the denominator. No best-of
retries or successful timing substitutes are permitted.

The first new FlagQuantum registrations should distinguish the ordinary
`compiler.compile` plus native legalization workflow from the target-artifact
workflow. The automatic native CZ block stage belongs to the latter. Its
current admission requires RX/RZ/full-CZ, an absent or undirected unallocated
topology and identity initial placement; its artifact workflow restores final
layout. These limits must appear in the registration. Do not imply that the
existing ordinary compiler entry calls the new stage. Qiskit and Cirq use their
own declared public workflows; no participant receives a special tolerance,
resource budget or hidden helper compiler.

## Attribution controls

Choose controls before examining their results. Record one-factor contrasts
where the product exposes them: routing selection, layout restoration,
post-routing optimization, native basis, local synthesis and search effort.
Keep the input, target, initial state contract and acceptance fixed. A compound
pipeline comparison is useful but cannot identify the contribution of one pass.
Do not add an implementation switch solely to make an ablation convenient.

The new target-artifact stage has a retained native baseline, so record both
baseline and accepted-output costs within that invocation. Include replay,
verification, artifact creation and serialization in its declared wall time.
Keep compiler-native depth separate from the independent evaluator's common
two-body dependency depth.

## Prospective held-out extension

The three frozen inputs are development diagnostics and cannot support a global
SDK ranking. A separate task bundle must cover actual application families:

| Family | User requirement | Topology variation |
| --- | --- | --- |
| MaxCut/QAOA circuits | Repeated cost/mixer layers with shared symbolic and fixed numeric parameters | Line, ring, rectangular grid, bounded-degree irregular graphs |
| Product-formula dynamics | Noncommuting Pauli evolution with repeated physical interactions | Same graph families, including mismatched interaction graphs |
| Small quantum-chemistry ansatz circuits | Jordan-Wigner parity chains and particle-conserving excitation patterns | Line, grid and sparse irregular targets |
| QFT/phase-estimation subcircuits | Controlled rotations with long-range interactions | Line, ring and grid |
| Coherent error-correction subcircuits | Stabilizer-extraction interactions and explicit ancilla roles | Declared code connectivity and mismatched sparse targets |

These families specify compilation workloads, not claims of algorithmic
advantage, chemistry accuracy or error-correction performance. Dynamic
measurement/reset variants and disconnected-target failures need explicit
contracts and separate negative cases. Symbolic/shared/trainable parameters
must remain symbolic, be supported through a declared binding workflow, or
produce an explicit unsupported result. Never silently bind them numerically.

Freeze the generator, semantic conventions, widths, layers, graph generation,
acceptance, total budgets and registration policy before revealing held-out
realizations. Freeze compiler defaults before generating those realizations.
Store generator revision, seed derivation, input hashes and all generated
cases. If any held-out result informs a compiler change, move that corpus to
development and generate a new prospective set. Label published fixed fixtures
as fixed regression cases rather than permanently unseen data.

The extension is a new bundle revision. Reuse existing independent semantics
and limits where applicable, but do not pretend that new fixtures or additional
operator checks ran under the unchanged historical bundle. Small instances
need all input columns checked up to one global phase; larger probes retain
their limited-evidence label. Include inverse/round-trip, reversed operands,
nontrivial final maps, arbitrary-state, unsupported and exhausted-budget cases.

## Report and completion gates

Publish a matrix per SDK/version/configuration, case family, width and topology:
acceptance and failure counts; semantic evidence/error; full-CZ count and common
dependency depth; compilation wall time and peak memory; seed spread and all
regressions. Retain raw normalized artifacts, requests, responses, supervisor
telemetry, warnings and manifests for independent replay without SDK imports.
Separate a complete engineering campaign from publication-host qualification.

Before any parity or superiority claim, require:

1. Integrated immutable compiler revisions and verified build/install chains.
2. The complete unchanged frozen campaign, with independent replay of every
   record, warmup, case, registration binding and resource outcome.
3. A preregistered prospective held-out campaign and its complete evidence.
4. Honest treatment of restored-layout overhead, unsupported targets, symbolic
   boundaries, compile-time/memory costs and objective conflicts.
5. Independent adapter review and the publication environment gates required by
   the existing measurement protocol.

These gates are outstanding. No local development probe, formatting check or
compiler unit suite substitutes for them.
