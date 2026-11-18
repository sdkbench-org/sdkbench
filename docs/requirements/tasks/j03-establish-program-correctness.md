<!-- Generated from catalog.json by tools/requirements_docs.py. Do not edit directly. -->

# J03 - Establish program correctness

[All tasks](../TASK_CATALOG.md) | [Acceptance rules](../ACCEPTANCE.md) | [Traceability](../TRACEABILITY.md)

Status: requirements only. No task in this file is claimed as implemented or executed.

Workflow grounding: [S01](../SOURCES.md#s01), [S02](../SOURCES.md#s02). Sources inform context; they do not establish universal requirements or user-study validation.

<a id="t011"></a>

## T011 - Verify an ideal algorithm against an independent oracle

**User need:** A developer needs to distinguish numerical implementation faults from algorithm design faults.

**Target users:** [P02](../REQUIREMENTS_MAP.md#p02), [P07](../REQUIREMENTS_MAP.md#p07).

**Applicability tags:** gate, qudit. Instance selection and conditional edges must be frozen before participant evaluation.

**Workflow stages:** verify, execute.

**Required input and constraints:** Small circuits with complex amplitudes, nonlocal controls, permutations and declared global-phase rules.

**Required output:** Output states and a verification certificate identifying the tested input space.

**Required capabilities:** [C05](../CAPABILITIES.md#c05), [C20](../CAPABILITIES.md#c20).

**Function traceability:**

- [F05.01](../CAPABILITIES.md#f05-01): Evolve a state from an explicit input. Required for every instance of this task family.
- [F05.03](../CAPABILITIES.md#f05-03): Compute exact observables and reduced states. Required for every instance of this task family.
- [F20.02](../CAPABILITIES.md#f20-02): Normalize conventions across boundaries. Required for every instance of this task family.
- [F20.04](../CAPABILITIES.md#f20-04): Package reproducible evidence. Required for every instance of this task family.

**Acceptance profiles:** [A02](../ACCEPTANCE.md#a02), [A03](../ACCEPTANCE.md#a03).

**Task-specific acceptance:** Exhaustive basis plus interference tests or full small-unitary comparison meet the frozen error budget; any larger probe-only evidence is labeled as such.

**Measurements:** verification pass rate; maximum state error; runtime.

**Required negative case:** A relative phase or control/target reversal must fail even when one initial-state probability distribution happens to agree.

**Instance readiness:** Use the [instance specification template](../TASK_SPEC_TEMPLATE.md); bind fixtures, independent references, numerical/statistical thresholds, budgets, and attribution rules before execution.

<a id="t012"></a>

## T012 - Verify sampling and register interpretation

**User need:** A user needs samples that represent the declared measurement rather than a convenient output encoding.

**Target users:** [P01](../REQUIREMENTS_MAP.md#p01), [P02](../REQUIREMENTS_MAP.md#p02), [P08](../REQUIREMENTS_MAP.md#p08).

**Applicability tags:** gate, adaptive. Instance selection and conditional edges must be frozen before participant evaluation.

**Workflow stages:** verify, execute, estimate.

**Required input and constraints:** Known discrete distributions with sparse support, multiple registers and nontrivial measurement maps.

**Required output:** Samples or counts with exact shot totals and explicit register conventions.

**Required capabilities:** [C03](../CAPABILITIES.md#c03), [C05](../CAPABILITIES.md#c05), [C12](../CAPABILITIES.md#c12).

**Function traceability:**

- [F05.02](../CAPABILITIES.md#f05-02): Sample declared measurements. Required for every instance of this task family.
- [F03.02](../CAPABILITIES.md#f03-02): Condition on recorded outcomes. Required for every instance of this task family.
- [F12.01](../CAPABILITIES.md#f12-01): Validate and normalize result records. Required for every instance of this task family.
- [F12.02](../CAPABILITIES.md#f12-02): Estimate quantities with uncertainty. Required for every instance of this task family.

**Acceptance profiles:** [A04](../ACCEPTANCE.md#a04).

**Task-specific acceptance:** Frozen equivalence tests meet the distribution tolerance with declared power and multiplicity control; shot conservation and mapping are exact.

**Measurements:** distribution discrepancy; sampling throughput; shots; inconclusive rate.

**Required negative case:** Counts, quasi-probabilities and postselected samples cannot be interchanged without type and denominator disclosure.

**Instance readiness:** Use the [instance specification template](../TASK_SPEC_TEMPLATE.md); bind fixtures, independent references, numerical/statistical thresholds, budgets, and attribution rules before execution.

<a id="t013"></a>

## T013 - Check that a program rewrite preserves intended behavior

**User need:** A compiler or algorithm developer needs evidence that an optimization preserves more than a single test output.

**Target users:** [P02](../REQUIREMENTS_MAP.md#p02), [P06](../REQUIREMENTS_MAP.md#p06).

**Applicability tags:** gate, adaptive. Instance selection and conditional edges must be frozen before participant evaluation.

**Workflow stages:** verify, compile.

**Required input and constraints:** Original and transformed programs, permitted approximation, logical permutation and dynamic execution profile.

**Required output:** A comparison artifact stating exact, bounded numerical or sampled verification scope.

**Required capabilities:** [C03](../CAPABILITIES.md#c03), [C06](../CAPABILITIES.md#c06), [C20](../CAPABILITIES.md#c20).

**Function traceability:**

- [F06.03](../CAPABILITIES.md#f06-03): Optimize while preserving semantics. Required for every instance of this task family.
- [F03.02](../CAPABILITIES.md#f03-02): Condition on recorded outcomes. Required for every instance of this task family.
- [F20.03](../CAPABILITIES.md#f20-03): Round-trip artifacts without hidden loss. Required for every instance of this task family.
- [F20.05](../CAPABILITIES.md#f20-05): Expose inspectable errors and traces. Required for every instance of this task family.

**Acceptance profiles:** [A02](../ACCEPTANCE.md#a02), [A03](../ACCEPTANCE.md#a03), [A04](../ACCEPTANCE.md#a04).

**Task-specific acceptance:** For the prescribed small oracle domain, states or branch instruments match after only declared mapping/phase corrections; approximate changes remain within budget.

**Measurements:** semantic pass rate; verification cost; unverified domains.

**Required negative case:** An optimizer cannot erase terminal measurements, change branch probabilities or rely on an undisclosed initial-state assumption.

**Instance readiness:** Use the [instance specification template](../TASK_SPEC_TEMPLATE.md); bind fixtures, independent references, numerical/statistical thresholds, budgets, and attribution rules before execution.

<a id="t014"></a>

## T014 - Validate a declared quantum channel or state transformation

**User need:** A user needs valid mixed-state operations, including when errors are subtle.

**Target users:** [P08](../REQUIREMENTS_MAP.md#p08), [P07](../REQUIREMENTS_MAP.md#p07).

**Applicability tags:** gate, cv. Instance selection and conditional edges must be frozen before participant evaluation.

**Workflow stages:** verify, execute.

**Required input and constraints:** Small channels with a declared representation and physicality contract, including entangled reference inputs.

**Required output:** Evolved states plus trace, positivity and representation checks.

**Required capabilities:** [C04](../CAPABILITIES.md#c04), [C05](../CAPABILITIES.md#c05), [C10](../CAPABILITIES.md#c10).

**Function traceability:**

- [F04.01](../CAPABILITIES.md#f04-01): Represent states and linear operators. Required for every instance of this task family.
- [F10.01](../CAPABILITIES.md#f10-01): Specify channels and readout models. Required for every instance of this task family.
- [F10.02](../CAPABILITIES.md#f10-02): Execute noisy density or trajectory evolution. Required for every instance of this task family.
- [F05.03](../CAPABILITIES.md#f05-03): Compute exact observables and reduced states. Required for every instance of this task family.

**Acceptance profiles:** [A03](../ACCEPTANCE.md#a03).

**Task-specific acceptance:** Declared physical channels preserve trace and positivity within budget and agree with a direct small channel oracle; nonphysical algebraic maps are labeled separately.

**Measurements:** channel error; trace error; positivity violation; execution time.

**Required negative case:** A trace-changing map cannot be made valid by silent renormalization, and an invalid physical-channel declaration must fail.

**Instance readiness:** Use the [instance specification template](../TASK_SPEC_TEMPLATE.md); bind fixtures, independent references, numerical/statistical thresholds, budgets, and attribution rules before execution.

<a id="t015"></a>

## T015 - Locate the stage and cause of an invalid experiment

**User need:** A user needs actionable failure evidence to repair a workflow.

**Target users:** [P16](../REQUIREMENTS_MAP.md#p16), [P02](../REQUIREMENTS_MAP.md#p02).

**Applicability tags:** common. Instance selection and conditional edges must be frozen before participant evaluation.

**Workflow stages:** verify, operate.

**Required input and constraints:** Invalid dimensions, bindings, unsupported operations, resource limits and injected execution/result faults.

**Required output:** A stage-specific failure record with reproducible input and redacted context.

**Required capabilities:** [C01](../CAPABILITIES.md#c01), [C03](../CAPABILITIES.md#c03), [C11](../CAPABILITIES.md#c11), [C20](../CAPABILITIES.md#c20).

**Function traceability:**

- [F01.03](../CAPABILITIES.md#f01-03): Learn and diagnose a workflow. Required for every instance of this task family.
- [F20.05](../CAPABILITIES.md#f20-05): Expose inspectable errors and traces. Required for every instance of this task family.
- [F03.05](../CAPABILITIES.md#f03-05): Assess execution-profile compatibility. Required for every instance of this task family.
- [F11.04](../CAPABILITIES.md#f11-04): Recover and reconcile partial work. Required for every instance of this task family.

**Acceptance profiles:** [A01](../ACCEPTANCE.md#a01), [A08](../ACCEPTANCE.md#a08).

**Task-specific acceptance:** Each injected fault is classified at the correct boundary; no failure is represented as an empty successful result or silent fallback.

**Measurements:** diagnostic completeness; fault detection rate; time to failure.

**Required negative case:** A provider outage or missing dependency must remain distinguishable from an incorrect computed result.

**Instance readiness:** Use the [instance specification template](../TASK_SPEC_TEMPLATE.md); bind fixtures, independent references, numerical/statistical thresholds, budgets, and attribution rules before execution.
