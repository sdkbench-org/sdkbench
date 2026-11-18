<!-- Generated from catalog.json by tools/requirements_docs.py. Do not edit directly. -->

# J11 - Study error-corrected computation

[All tasks](../TASK_CATALOG.md) | [Acceptance rules](../ACCEPTANCE.md) | [Traceability](../TRACEABILITY.md)

Status: requirements only. No task in this file is claimed as implemented or executed.

Workflow grounding: [S07](../SOURCES.md#s07). Sources inform context; they do not establish universal requirements or user-study validation.

<a id="t051"></a>

## T051 - Construct and validate a code with named logical observables

**User need:** A researcher needs code definitions whose algebra and logical conventions can be checked.

**Target users:** [P10](../REQUIREMENTS_MAP.md#p10).

**Applicability tags:** qec. Instance selection and conditional edges must be frozen before participant evaluation.

**Workflow stages:** formulate, express, verify.

**Required input and constraints:** Check matrices or geometric code specifications, boundaries and named logical operators.

**Required output:** A code object or equivalent artifact with checks, labels and validation evidence.

**Required capabilities:** [C04](../CAPABILITIES.md#c04), [C14](../CAPABILITIES.md#c14), [C20](../CAPABILITIES.md#c20).

**Function traceability:**

- [F14.01](../CAPABILITIES.md#f14-01): Specify codes and logical observables. Required for every instance of this task family.
- [F04.02](../CAPABILITIES.md#f04-02): Manipulate structured observables. Required for every instance of this task family.
- [F20.02](../CAPABILITIES.md#f20-02): Normalize conventions across boundaries. Required for every instance of this task family.

**Acceptance profiles:** [A02](../ACCEPTANCE.md#a02).

**Task-specific acceptance:** Commutation, dimensions, declared logical relations and small enumerated fixtures agree; a claimed distance is proved for the bounded fixture or explicitly left unverified.

**Measurements:** construction time; algebra pass rate; resource size.

**Required negative case:** A noncommuting check set or an unsupported subsystem-code assumption must not be silently repaired.

**Instance readiness:** Use the [instance specification template](../TASK_SPEC_TEMPLATE.md); bind fixtures, independent references, numerical/statistical thresholds, budgets, and attribution rules before execution.

<a id="t052"></a>

## T052 - Run repeated syndrome-extraction memory experiments

**User need:** A researcher needs the full round/measurement history for logical-memory analysis.

**Target users:** [P10](../REQUIREMENTS_MAP.md#p10).

**Applicability tags:** qec, adaptive. Instance selection and conditional edges must be frozen before participant evaluation.

**Workflow stages:** express, execute, estimate.

**Required input and constraints:** A code, extraction schedule, round count, noise locations and detector/logical definitions.

**Required output:** Syndrome histories, detection events and logical-observable records.

**Required capabilities:** [C03](../CAPABILITIES.md#c03), [C11](../CAPABILITIES.md#c11), [C14](../CAPABILITIES.md#c14).

**Function traceability:**

- [F14.02](../CAPABILITIES.md#f14-02): Build repeated error-correction experiments. Required when the frozen instance includes the qec applicability tag.
- [F03.01](../CAPABILITIES.md#f03-01): Measure and reset during execution. Required for every instance of this task family.
- [F03.02](../CAPABILITIES.md#f03-02): Condition on recorded outcomes. Required for every instance of this task family.
- [F11.05](../CAPABILITIES.md#f11-05): Preserve acquisition and result provenance. Required for every instance of this task family.

**Acceptance profiles:** [A02](../ACCEPTANCE.md#a02), [A04](../ACCEPTANCE.md#a04).

**Task-specific acceptance:** Noiseless and injected single-fault small fixtures match independent expected histories; measurement/reset order and round labels are preserved.

**Measurements:** construction/execution time; history correctness; samples per second.

**Required negative case:** Dropping an initial/final boundary event or shifting a measurement by one round must fail.

**Instance readiness:** Use the [instance specification template](../TASK_SPEC_TEMPLATE.md); bind fixtures, independent references, numerical/statistical thresholds, budgets, and attribution rules before execution.

<a id="t053"></a>

## T053 - Build and sample an explicitly scoped detector error model

**User need:** A decoder study needs a model that matches the declared circuit/noise assumptions.

**Target users:** [P10](../REQUIREMENTS_MAP.md#p10).

**Applicability tags:** qec. Instance selection and conditional edges must be frozen before participant evaluation.

**Workflow stages:** formulate, execute, verify.

**Required input and constraints:** A small extraction experiment, supported noise model, correlation policy and event/observable mapping.

**Required output:** A detector model, interchange artifact and sampled events with provenance.

**Required capabilities:** [C12](../CAPABILITIES.md#c12), [C14](../CAPABILITIES.md#c14), [C20](../CAPABILITIES.md#c20).

**Function traceability:**

- [F14.03](../CAPABILITIES.md#f14-03): Construct and sample detector error models. Required for every instance of this task family.
- [F14.02](../CAPABILITIES.md#f14-02): Build repeated error-correction experiments. Required for every instance of this task family.
- [F12.01](../CAPABILITIES.md#f12-01): Validate and normalize result records. Required for every instance of this task family.
- [F20.03](../CAPABILITIES.md#f20-03): Round-trip artifacts without hidden loss. Required for every instance of this task family.

**Acceptance profiles:** [A02](../ACCEPTANCE.md#a02), [A04](../ACCEPTANCE.md#a04).

**Task-specific acceptance:** Independent enumerated faults and sampled distributions agree within contract; approximation and discarded correlations are explicit and round-trip semantics hold.

**Measurements:** model error; construction time; sample throughput; approximation scope.

**Required negative case:** An unsupported correlated error cannot be split into independent edges without a declared approximation.

**Instance readiness:** Use the [instance specification template](../TASK_SPEC_TEMPLATE.md); bind fixtures, independent references, numerical/statistical thresholds, budgets, and attribution rules before execution.

<a id="t054"></a>

## T054 - Evaluate a decoder on held-out detector events

**User need:** A researcher needs a logical error/latency tradeoff with the same underlying decoding problem.

**Target users:** [P10](../REQUIREMENTS_MAP.md#p10).

**Applicability tags:** qec. Instance selection and conditional edges must be frozen before participant evaluation.

**Workflow stages:** execute, estimate.

**Required input and constraints:** Frozen detector events, logical labels, model, noise rate, training/tuning separation and latency budget.

**Required output:** Predictions, logical failure intervals, latency distribution and unmatched-case records.

**Required capabilities:** [C12](../CAPABILITIES.md#c12), [C14](../CAPABILITIES.md#c14), [C19](../CAPABILITIES.md#c19).

**Function traceability:**

- [F14.04](../CAPABILITIES.md#f14-04): Decode and estimate logical outcomes. Required for every instance of this task family.
- [F14.03](../CAPABILITIES.md#f14-03): Construct and sample detector error models. Required for every instance of this task family.
- [F12.02](../CAPABILITIES.md#f12-02): Estimate quantities with uncertainty. Required for every instance of this task family.
- [F19.04](../CAPABILITIES.md#f19-04): Measure and enforce execution budgets. Required for every instance of this task family.

**Acceptance profiles:** [A04](../ACCEPTANCE.md#a04), [A09](../ACCEPTANCE.md#a09).

**Task-specific acceptance:** Predictions are scored on held-out events; latency includes specified preprocessing boundaries, and zero observed failures still receive a nonzero uncertainty bound.

**Measurements:** logical failure rate; tail latency; throughput; memory.

**Required negative case:** Decoder training/tuning samples cannot leak into evaluation, and unmatched syndromes cannot be dropped.

**Instance readiness:** Use the [instance specification template](../TASK_SPEC_TEMPLATE.md); bind fixtures, independent references, numerical/statistical thresholds, budgets, and attribution rules before execution.

<a id="t055"></a>

## T055 - Estimate resources for a specified logical computation

**User need:** A user needs transparent fault-tolerant resource assumptions rather than an unexplained qubit number.

**Target users:** [P10](../REQUIREMENTS_MAP.md#p10), [P02](../REQUIREMENTS_MAP.md#p02).

**Applicability tags:** qec. Instance selection and conditional edges must be frozen before participant evaluation.

**Workflow stages:** formulate, compile, estimate.

**Required input and constraints:** A logical program, synthesis precision, error budget, code/cycle assumptions and magic-state/resource model.

**Required output:** A resource ledger separating logical counts, synthesis, factories, physical assumptions and extrapolation.

**Required capabilities:** [C06](../CAPABILITIES.md#c06), [C13](../CAPABILITIES.md#c13), [C14](../CAPABILITIES.md#c14), [C20](../CAPABILITIES.md#c20).

**Function traceability:**

- [F14.05](../CAPABILITIES.md#f14-05): Compile logical operations and estimate resources. Required for every instance of this task family.
- [F06.05](../CAPABILITIES.md#f06-05): Schedule and account for resources. Required for every instance of this task family.
- [F13.04](../CAPABILITIES.md#f13-04): Estimate algorithmic quantities. Required for every instance of this task family.
- [F20.04](../CAPABILITIES.md#f20-04): Package reproducible evidence. Required for every instance of this task family.

**Acceptance profiles:** [A02](../ACCEPTANCE.md#a02), [A09](../ACCEPTANCE.md#a09).

**Task-specific acceptance:** Small ledgers independently reconcile counts and budgets; all claimed physical resources follow the frozen model and no estimate is presented as demonstrated hardware performance.

**Measurements:** logical operations; physical-resource estimate; runtime estimate; assumption sensitivity.

**Required negative case:** A logical T-count alone cannot be reported as total physical resource cost.

**Instance readiness:** Use the [instance specification template](../TASK_SPEC_TEMPLATE.md); bind fixtures, independent references, numerical/statistical thresholds, budgets, and attribution rules before execution.
