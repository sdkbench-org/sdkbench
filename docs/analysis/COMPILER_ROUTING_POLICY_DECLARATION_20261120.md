# Native routing-policy qualification declaration

Declared on 2026-11-20 before dispatch, case generation or entropy for this
study. This is an auditable repository declaration, not independent timestamp
attestation. No result is claimed by implementing or declaring the profile.

## Requirement and question

Acceptance item 4 of FlagQuantum's approved
`docs/api-changes/FQ-COMPILER-AUTO-ROUTING-20261118.md` requires held-out
compile-time and memory comparisons against explicit routing policies under
unchanged SDKBench checks. Neither existing three-SDK application report
supplies this same-revision control. The original before-merge timing
requirement was not met; this is later qualification and cannot retroactively
establish that it was.

Compare the omitted default with explicit `restore_after_each_gate`,
`persistent_layout` and `sabre` on the same FlagQuantum source build, wheel,
host and freshly drawn application cohort. Gate count, dependency depth,
whole-workflow time, process memory and failures remain separate questions.
No policy is presumed to win. This study is not an SDK ranking.

## Sources and controlled input

Use immutable FlagQuantum commit
`858df9dbd5ba964e8e59b3383304547710a1dee5`, already integrated into main and used
in both earlier prospective campaigns. The new cohort must not influence
source selection or compiler options. Record the full integrated SDKBench
workflow revision in the delivery PR before dispatch, then freeze its actual
revision and source fingerprint through the existing workflow. Required
harness CI must pass first; unmerged implementation is insufficient.

| Workflow | Native routing keyword |
| --- | --- |
| `flagquantum-ordinary-restored` | Omitted |
| `flagquantum-restore-after-each-gate-restored` | `routing_strategy="restore_after_each_gate"` |
| `flagquantum-persistent-layout-restored` | `routing_strategy="persistent_layout"` |
| `flagquantum-sabre-restored` | `routing_strategy="sabre"` |

Only that keyword varies. Every control uses the same native circuit building,
ordinary `compiler.compile`, native gate legalization, normalization and timed
external identity restoration. No target-artifact or CZ block-optimization
stage is inserted. `sabre_layout` is excluded because nonidentity initial
placement changes this task contract. Default/explicit-`auto` functional
equivalence remains compiler conformance, not a measured timing result.

Admission and reporting both require identical source-build observations,
installed wheel information, dependency components and configuration after
normalizing the declared workflow and routing choice. Stable host facts must
match. Changing `/proc/cpuinfo` hashes are retained verbatim but excluded from
this equality because CPU frequencies vary between observations. Every other
environment field must match. Existing live installed-byte and source
admission still applies before the draw and each worker import.

## One execution, fixed scope and limits

Dispatch `.github/workflows/compiler-applications.yml` once with
`workflow_profile=routing-policies` and the fixed compiler commit. Do not rerun
the job, delete preparation records or redraw. Freeze all four actual
registrations and the same built wheel before the one OS-backed entropy draw.
Retain all failures and partial evidence, including failures before the draw.
A necessary source or harness repair requires a new declaration preserving
the earlier failure; it cannot silently replace this result.

Use the existing selection rule: QAOA, Ising, hopping, QFT and repetition;
widths 6/8/12; line/grid targets; 30 cases. Four workflows produce 120 complete
case/policy pairs, 1,200 process blocks, 2,400 warmups and 3,600 measured
compilations when complete. These are intended counts, not observations.

Retain one CPU, one numerical thread, 16 GiB, network isolation, ten blocks,
two warmups, three measurements, width-specific cumulative case limits and
120 seconds per compilation. Keep the 270-minute measurement and 360-minute
job ceilings despite the fourth participant. If interrupted, call the study
incomplete and retain partial artifacts. No threshold, budget, retry, case
filter or layout-permission changes to rescue a policy.

Reuse the existing block-order rotation. Ten blocks do not form a complete
multiple of four policies, so each position occurs two or three times per
policy. Preserve that ordering and report descriptive block variation; do not
claim exact position balance or infer significance from it.

The original independent references and acceptance remain authoritative:
absolute semantic error at most `1e-8`, normalization tolerance `1e-10`, zero
relative tolerance, zero topology violations, identity initial placement and
delivered identity final placement. Six-qubit cases use full-operator checks;
widths 8/12 retain three-probe scope. No hardware-fidelity or universal semantic
claim is inferred from those probes.

## Replay and reporting

Independently replay every retained block without participant SDK imports.
Retain the complete campaign, source/build/wheel identities, registrations,
requirements, both bundles, freeze/draw/selection records, warmups, measured
payloads, supervisor controls, failures, replay and descriptive comparisons.
A green exit, successful build or artifact upload is insufficient.

Report every case and all six unordered policy pairs: 180 pair rows. Ratios
require both complete cases to pass. Warmup, timeout, memory, unsupported and
correctness failures remain in coverage; partial passing measurements cannot
rescue the case. Preserve all ten paired block observations and descriptive
quartiles. Do not infer significance, a scalar score or an across-case winner.

Time includes complete adapter work and identity restoration. Process peak
memory includes imports, warmups, measurements and export, not isolated compiler
workspace. No stage cause is inferred without separate profiling. The earlier
three-SDK campaigns use different cohorts and hosts: retain them separately,
with no between-profile improvement ratios or favorable policy selection.
Publication eligibility remains false. Only a complete, independently replayed
and reported campaign can close this evidence gap; retain remaining limitations
even if every case passes.
