# Executable task-instance specification template

This is a template, not a ready-to-run instance. Replace every placeholder and resolve every conditional field before freezing an instance. Unspecified tolerances, references or budgets block readiness. Do not infer missing settings from a participant's defaults.

## Identity and user outcome

- Task family ID and requirements version: `<Txxx, version>`
- Instance/protocol ID, revision and immutable fixture hash: `<identifiers>`
- Target user(s), role and real decision or scientific outcome: `<who and why>`
- Intended output and why it is useful: `<output contract>`
- Task relevance evidence and domain review: `<sources/review records; distinguish hypotheses from user studies>`
- Computing-model/domain tags and workflow stages: `<tags/stages>`
- Cohort charter and participant-selection/version policy: `<frozen charter>`
- Required capabilities/functions: `<IDs>`
- Each conditional edge and its resolved applicability: `<scientific condition and decision>`

## Inputs and semantics

- Input fixture/generator, distribution, seed policy and data license: `<artifact/version>`
- Model geometry, basis, dimensions, boundary conditions, constants and units: `<values or justified N/A>`
- Wire/mode/variable significance, control/target order and output mapping: `<explicit conventions>`
- Parameters, shared occurrences, domains, binding and broadcasting semantics: `<contract>`
- Initial states, workspace, allowed global/relative phase and reset assumptions: `<contract>`
- Dynamic branch, loop, measurement-pattern and termination semantics: `<contract or N/A>`
- Noise, calibration, trajectory or acquisition assumptions: `<contract or N/A>`
- Modality-specific controls, quadrature conventions, schedules, embedding and cutoff: `<contract or N/A>`
- Invalid/unsupported inputs and independently checked negative fixtures: `<list>`

## Required outputs

- Artifact/data types, dimensions, ordering, units and identifiers: `<schema>`
- Raw results, shot totals, postselection/loss/repair denominators: `<records>`
- Requested observables, solution validity or scientific quantity: `<values to compute>`
- Approximation, provenance, derivative method and execution-chain disclosures: `<fields>`
- Diagnostics and explicit incomplete/failed outcomes: `<schema>`
- Allowed external components and required cost/attribution boundary: `<policy>`

## Independent acceptance

- Acceptance profile IDs and task-specific criteria: `<Axx references>`
- Reference implementation/proof/data, revision and provenance: `<independent artifact>`
- Reference uncertainty and limits of verification: `<quantified scope>`
- Exact/algebraic and physical-invariant checks: `<procedure>`
- Numerical error metric, `atol`, `rtol` or other concrete bound with justification: `<frozen values>`
- Approximation/refinement criteria and evidence required at large scale: `<procedure>`
- Statistical estimand, discrepancy/equivalence margin and interval/test procedure: `<procedure>`
- Confidence/error level, power, replication, multiplicity and stopping policy: `<frozen values>`
- Application target and feasibility/oracle/energy convention: `<contract>`
- Target legality and resource/timing validator: `<independent validator>`
- Success, failure and inconclusive decision rules: `<machine-checkable logic>`
- Evaluator positive/negative cases and independent review: `<evidence>`

## Measurement boundary and resources

- Primary metric, direction, units, secondary diagnostics and quality constraints: `<definitions>`
- Requested scales and realism/relevance rationale: `<ladder; avoid an unjustified full Cartesian grid>`
- CPU/device/node count, memory limits, threads, precision and communication settings: `<resources>`
- Wall-time, calls, shots, search and any authorized device-spend budget: `<limits>`
- Exact work included/excluded: `<setup, import, compilation, preprocessing, encoding, synchronization, output, optimization, repair, postprocessing>`
- Cold/warm/cache/JIT/autotuning policy and output-materialization location: `<rules>`
- Timing clocks, synchronization and peak-memory collection procedure: `<procedure>`
- Matched-method versus matched-quality/best-available mode: `<cohort>`
- Tuning access, algorithm search space and held-out split: `<rules>`
- Run ordering, independent processes/seeds and censored-limit policy: `<rules>`
- Checkpoint/fault/retry policy and expected recovery semantics: `<procedure or N/A>`

## Reporting and reproducibility

- Source, SDK, compiler, engine, derivative, library, OS and driver versions: `<manifest>`
- Actual backend and fallback verification: `<probe/telemetry>`
- Data origin: `<synthetic / simulator / hardware; identification and attestation limits>`
- Job IDs, acquisition windows and target/calibration snapshots: `<records or justified N/A>`
- Raw observations, timings, intermediate validation and failure records: `<artifacts>`
- End-to-end and component-cost attribution: `<ledger>`
- Coverage denominator, unsupported/access-limited cases and any aggregation weights: `<rules>`
- Uncertainty/effect-size analysis and result-selection policy: `<procedure>`
- Reproduction commands, hashes, access/data-rights limits and safe redaction: `<bundle>`
- Maintainer conflicts, reviews, limitations and permitted claim wording: `<disclosures>`
- Frozen approval/revision date and change-control record: `<record>`

## Readiness decision

- `<not ready / ready for controlled execution>`
- Outstanding requirements: `<none or explicit blockers>`
- Independent scientific/evaluator review: `<records>`
- Dry-run and no-unapproved-submission checks: `<evidence>`
- Authorized execution scope: `<local resources or separately approved device budget>`

No participant support or accepted result is inferred merely by completing this form.
