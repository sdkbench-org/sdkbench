# Neutrality, applicability and study governance

## Purpose

SDKBench exists to establish useful, reproducible evidence about quantum software. Its requirements and rules must allow any participant to perform poorly. Maintainer affiliation, implementation convenience, commercial interest or a desired winner cannot justify adding/removing tasks, changing thresholds or suppressing unfavorable results.

This baseline does not designate a favored participant, backend, programming language or national/vendor hardware stack. Official project documentation in [SOURCES.md](SOURCES.md) supplies workflow examples and conventions; it is not an authoritative feature shopping list for the benchmark.

## From a user need to a study

1. Record the user, real outcome and relevance rationale. Review alternatives and whether a task duplicates another outcome.
2. Specify inputs/outputs, scientific assumptions, required functions and acceptance. Use independent domain review and primary references where relevant.
3. Define the cohort by user role, computational model and measurement boundary before inspecting participant outcomes.
4. Freeze instances, references, tuning opportunities, resource budgets, metrics and statistical analysis.
5. Validate evaluators and thin adapters with positive, negative and convention-sensitive fixtures.
6. Execute, preserve failures/raw evidence and publish bounded conclusions. A software support claim needs executable evidence, not a catalog entry.

A task may be retained even when no current participant completes it. Record it as an unmet user need; do not implement a preferred SDK feature merely to justify a benchmark. Implementation priority follows user value, review readiness and evaluation feasibility, not a participant's likely advantage. Requirements breadth and runnable-study readiness are separate axes.

## Applicability and coverage

A cohort charter declares its target user, model/domain tags, outputs, required task set, conditional function edges and relevant environment. Broad and specialist tools have different responsibilities, which must be visible. A selected cohort cannot be narrowed after an unsupported feature or slow case is observed.

- `unsupported` is a missing applicable capability, not a fast result and not a missing row.
- `not_applicable` requires a prior scope rationale; maintainers cannot grant it merely because a participant lacks an implementation.
- `not_measured`, unavailable hardware, access denial, licensing limits and incomplete references are evidence gaps. They do not prove support or non-support.
- Conditional edges are selected from the instance's scientific representation or permitted solution path. They are not optional merely because a participant cannot implement them.
- At matched-application level, different representations/algorithms may be allowed, but the output, quality and total-budget contract must be shared. Matched-method diagnostics are a separate cohort.

Report the denominator, applicable task coverage and accepted-result fraction for each cohort. Show performance on the shared accepted subset only alongside full coverage and failure counts. Do not let selective failure improve an aggregate ranking. Do not give repeated microvariants more weight merely because they are easy to generate. Any aggregation requires published user-relevant weights and sensitivity analysis; the default is separate task/role/quality-resource reporting, not a universal SDK score.

## Equal implementation and tuning opportunities

Freeze participant selection and versions. A primary stable-release cohort uses the same published version-selection policy for all participants. Development branches, patches, alternative engines, precision changes and experimental configurations belong to explicitly identified cohorts. Disclose build and installation failures.

Adapters translate data and invoke documented capabilities. They may not solve a task for one participant using hidden benchmark-side algorithms or silently omit required work. Legitimate external components are permitted only under the declared task boundary, named in provenance and available under the same integration rules. Record native frontend, compiler, engine, differentiation method, runtime and service separately. The same underlying engine is not independent verification evidence merely because it is reached through different frontends.

Offer equivalent access to task definitions, configuration review and the declared tuning budget. Report documented-default and tuned settings separately where both are relevant. Charge autotuning, compilation, preprocessing, cache population and search according to the frozen boundary. Keep cold-start, warm execution, kernel-only and end-to-end measurements distinct. A participant may explain a failure; explanation does not erase it.

## Measurement and analysis

Freeze seeds, instance distributions, output/error requirements, clocks, synchronization, hardware/precision, process isolation, resource limits, measurement order and repetition rules. Use interleaved/randomized order and independent runs where appropriate. Preserve raw samples, not only best timings. Report effect size, uncertainty, completion and censored resource-limit outcomes. Do not claim equivalence from an underpowered non-significance test.

Define practical effect margins, stopping rules and multiplicity treatment before measurement. Parameter/seed choices used for tuning must be separated from held-out evaluation. If holdouts are later published, create new independent instances for future generalization checks; do not claim permanent secrecy or contamination immunity.

References need provenance, uncertainty and a scientific justification. Prefer analytic/exhaustive small fixtures and independently implemented checks. A shared engine or copied implementation is not an independent oracle. Large-instance probes, convergence studies and model-based bounds have explicitly limited verification strength. If the requested claim exceeds the available oracle, mark the evidence insufficient.

Software and physical hardware effects are distinct. Queue latency, calibration drift, QPU fidelity and device availability do not establish SDK compute efficiency. Cross-hardware results may support a deployment outcome but cannot attribute all differences to software. Live execution and any paid work require an explicit separate authorization/budget; no requirements check or CI job submits device work.

## Conflicts, reviews and corrections

Disclose relevant maintainer/author relationships to participants in each study. Participant maintainers may review and improve their adapters through the same public process. A person affiliated with an affected participant must not be the sole reviewer of disputed acceptance, applicability or scoring changes benefiting that participant. Until independent review is available, label the decision and conclusions provisional.

Record disputes as evaluator, reference, adapter, participant, environment or protocol issues. Publish minimal reproductions and the evidence needed to distinguish them. Correct genuine benchmark faults consistently for all affected participants, preserve previous artifacts and publish the impact. Re-execute the affected cohort as specified; do not silently delete one inconvenient result. Protect credentials/private acquisition data through declared redaction boundaries without pretending inaccessible evidence is publicly reproducible.

## Versioning and release gates

The requirements version is independent of the package and executable suite versions. Stable task/function IDs are never reused for different meanings. New tasks receive new IDs; deprecated tasks retain a rationale and history. Changes to outputs, semantics, thresholds, conditions, reference procedures or budgets require a new instance/protocol revision. Historical results remain attached to the old revision.

A study is ready only when its cohort charter, instance specifications, independent evaluators, adapter review, data rights, error budgets, resources, statistical analysis and limitations are recorded. A passing structural documentation check does not satisfy scientific review. The requirements baseline may be merged as a draft without claiming any study has passed these gates.

## Open review work

Before the first requirements-based release, obtain role/domain review of task relevance, review the conditional-edge policy with non-gate users, instantiate independently checkable small and realistic-size fixtures, choose role-specific cohorts and validate evaluators. Resolve unclear practical thresholds through preregistered pilot studies; pilots may inform a later frozen protocol but cannot be reported as unbiased evaluation under thresholds chosen from those same outcomes.
