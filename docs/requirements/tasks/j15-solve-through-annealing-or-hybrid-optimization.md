<!-- Generated from catalog.json by tools/requirements_docs.py. Do not edit directly. -->

# J15 - Solve through annealing or hybrid optimization

[All tasks](../TASK_CATALOG.md) | [Acceptance rules](../ACCEPTANCE.md) | [Traceability](../TRACEABILITY.md)

Status: requirements only. No task in this file is claimed as implemented or executed.

Workflow grounding: [S06](../SOURCES.md#s06). Sources inform context; they do not establish universal requirements or user-study validation.

<a id="t071"></a>

## T071 - Translate an application into a quadratic or constrained model

**User need:** A practitioner needs the solver model to represent the original objective and constraints.

**Target users:** [P14](../REQUIREMENTS_MAP.md#p14).

**Applicability tags:** annealing. Instance selection and conditional edges must be frozen before participant evaluation.

**Workflow stages:** formulate, verify.

**Required input and constraints:** Small exhaustive binary/spin/constrained instances, penalty construction and coefficient/offset conventions.

**Required output:** A model and a reversible variable/objective map.

**Required capabilities:** [C04](../CAPABILITIES.md#c04), [C13](../CAPABILITIES.md#c13), [C18](../CAPABILITIES.md#c18).

**Function traceability:**

- [F18.01](../CAPABILITIES.md#f18-01): Represent quadratic and constrained models. Required for every instance of this task family.
- [F04.05](../CAPABILITIES.md#f04-05): Formulate objectives and constraints. Required for every instance of this task family.
- [F13.03](../CAPABILITIES.md#f13-03): Solve optimization instances. Required for every instance of this task family.

**Acceptance profiles:** [A02](../ACCEPTANCE.md#a02), [A09](../ACCEPTANCE.md#a09).

**Task-specific acceptance:** Exhaustive small assignments reconcile energies, offsets and feasibility; domain conversions and penalty assumptions are explicit.

**Measurements:** formulation time; model size; mapping correctness.

**Required negative case:** A sign convention, missing offset or insufficient penalty cannot be ignored when claiming the original problem was solved.

**Instance readiness:** Use the [instance specification template](../TASK_SPEC_TEMPLATE.md); bind fixtures, independent references, numerical/statistical thresholds, budgets, and attribution rules before execution.

<a id="t072"></a>

## T072 - Embed a logical model onto a physical topology

**User need:** A user needs a legal embedding and interpretable decoded samples.

**Target users:** [P14](../REQUIREMENTS_MAP.md#p14), [P09](../REQUIREMENTS_MAP.md#p09).

**Applicability tags:** annealing. Instance selection and conditional edges must be frozen before participant evaluation.

**Workflow stages:** compile, verify.

**Required input and constraints:** A logical model, physical graph, coefficient bounds, chain policy and embedding budget.

**Required output:** A valid embedded/scaled model, chains and inverse mapping.

**Required capabilities:** [C06](../CAPABILITIES.md#c06), [C18](../CAPABILITIES.md#c18).

**Function traceability:**

- [F18.02](../CAPABILITIES.md#f18-02): Embed and scale for a target. Required for every instance of this task family.
- [F18.01](../CAPABILITIES.md#f18-01): Represent quadratic and constrained models. Required for every instance of this task family.
- [F06.01](../CAPABILITIES.md#f06-01): Describe an executable target. Required for every instance of this task family.
- [F18.04](../CAPABILITIES.md#f18-04): Decode and validate candidate solutions. Required for every instance of this task family.

**Acceptance profiles:** [A02](../ACCEPTANCE.md#a02), [A05](../ACCEPTANCE.md#a05), [A10](../ACCEPTANCE.md#a10).

**Task-specific acceptance:** All interactions fit the target and unbroken-chain small assignments preserve logical energy up to disclosed scaling/offset; embedding failure remains explicit.

**Measurements:** embedding time; physical resources; chain length; valid embedding rate.

**Required negative case:** Breaking a logical interaction or omitting coefficient clipping cannot improve embedding success invisibly.

**Instance readiness:** Use the [instance specification template](../TASK_SPEC_TEMPLATE.md); bind fixtures, independent references, numerical/statistical thresholds, budgets, and attribution rules before execution.

<a id="t073"></a>

## T073 - Run a controlled annealing sampling study

**User need:** A practitioner needs results tied to the actual schedule, gauge and sampler type.

**Target users:** [P14](../REQUIREMENTS_MAP.md#p14), [P09](../REQUIREMENTS_MAP.md#p09).

**Applicability tags:** annealing. Instance selection and conditional edges must be frozen before participant evaluation.

**Workflow stages:** execute, estimate.

**Required input and constraints:** A model, solver type, reads, schedules, gauges and execution authorization or local stub.

**Required output:** Samples with timing, occurrences, schedule and decoding provenance.

**Required capabilities:** [C11](../CAPABILITIES.md#c11), [C12](../CAPABILITIES.md#c12), [C18](../CAPABILITIES.md#c18).

**Function traceability:**

- [F18.03](../CAPABILITIES.md#f18-03): Execute declared sampling schedules. Required for every instance of this task family.
- [F18.04](../CAPABILITIES.md#f18-04): Decode and validate candidate solutions. Required for every instance of this task family.
- [F11.05](../CAPABILITIES.md#f11-05): Preserve acquisition and result provenance. Required for every instance of this task family.
- [F12.02](../CAPABILITIES.md#f12-02): Estimate quantities with uncertainty. Required for every instance of this task family.

**Acceptance profiles:** [A04](../ACCEPTANCE.md#a04), [A08](../ACCEPTANCE.md#a08), [A10](../ACCEPTANCE.md#a10).

**Task-specific acceptance:** Read totals and variable mappings reconcile; known small-model results satisfy the declared statistical/quality contract without assuming thermal sampling unless that is the task.

**Measurements:** feasible-solution probability; objective distribution; total reads; wall/device time.

**Required negative case:** A classical sampler or repaired sample cannot be relabeled as raw quantum output.

**Instance readiness:** Use the [instance specification template](../TASK_SPEC_TEMPLATE.md); bind fixtures, independent references, numerical/statistical thresholds, budgets, and attribution rules before execution.

<a id="t074"></a>

## T074 - Evaluate feasibility and postprocessing honestly

**User need:** A user needs to understand whether chain decoding or repair actually yields valid application solutions.

**Target users:** [P14](../REQUIREMENTS_MAP.md#p14).

**Applicability tags:** annealing. Instance selection and conditional edges must be frozen before participant evaluation.

**Workflow stages:** estimate, optimize.

**Required input and constraints:** Raw samples including broken chains/infeasible points, a fixed decoding/repair rule and original problem.

**Required output:** Raw and repaired solutions with independently recomputed objectives, feasibility and costs.

**Required capabilities:** [C12](../CAPABILITIES.md#c12), [C13](../CAPABILITIES.md#c13), [C18](../CAPABILITIES.md#c18).

**Function traceability:**

- [F18.04](../CAPABILITIES.md#f18-04): Decode and validate candidate solutions. Required for every instance of this task family.
- [F18.01](../CAPABILITIES.md#f18-01): Represent quadratic and constrained models. Required for every instance of this task family.
- [F13.03](../CAPABILITIES.md#f13-03): Solve optimization instances. Required for every instance of this task family.
- [F12.05](../CAPABILITIES.md#f12-05): Export interpretable analysis. Required for every instance of this task family.

**Acceptance profiles:** [A02](../ACCEPTANCE.md#a02), [A09](../ACCEPTANCE.md#a09).

**Task-specific acceptance:** Every claimed solution is valid in original variables; raw failures, repair changes and repair compute are separately retained.

**Measurements:** raw/repaired feasibility; quality gap; repair time; discarded sample rate.

**Required negative case:** Dropping infeasible samples or reporting repaired objectives as raw solver outcomes is a reporting failure.

**Instance readiness:** Use the [instance specification template](../TASK_SPEC_TEMPLATE.md); bind fixtures, independent references, numerical/statistical thresholds, budgets, and attribution rules before execution.

<a id="t075"></a>

## T075 - Compare hybrid optimization at a matched end-to-end budget

**User need:** A practitioner needs a defensible quality/cost comparison for a solver that mixes resources.

**Target users:** [P14](../REQUIREMENTS_MAP.md#p14).

**Applicability tags:** annealing. Instance selection and conditional edges must be frozen before participant evaluation.

**Workflow stages:** optimize, estimate.

**Required input and constraints:** Frozen instances, classical baseline/bounds, all preprocessing/repair, solver settings and total budget.

**Required output:** Feasibility/quality success curves and a complete resource-accounting boundary.

**Required capabilities:** [C09](../CAPABILITIES.md#c09), [C13](../CAPABILITIES.md#c13), [C18](../CAPABILITIES.md#c18), [C19](../CAPABILITIES.md#c19).

**Function traceability:**

- [F18.05](../CAPABILITIES.md#f18-05): Account for hybrid optimization cost. Required for every instance of this task family.
- [F09.05](../CAPABILITIES.md#f09-05): Budget training and adaptive search. Required for every instance of this task family.
- [F13.03](../CAPABILITIES.md#f13-03): Solve optimization instances. Required for every instance of this task family.
- [F19.04](../CAPABILITIES.md#f19-04): Measure and enforce execution budgets. Required for every instance of this task family.

**Acceptance profiles:** [A09](../ACCEPTANCE.md#a09).

**Task-specific acceptance:** The output contract and budget are shared; inaccessible internal QPU/classical breakdown is labeled unknown, while observable end-to-end cost and failures remain reported.

**Measurements:** time to feasible target; success probability; objective gap; known/unknown resource cost.

**Required negative case:** A hidden classical search or unknown internal QPU time cannot support a claimed quantum speedup or per-QPU efficiency.

**Instance readiness:** Use the [instance specification template](../TASK_SPEC_TEMPLATE.md); bind fixtures, independent references, numerical/statistical thresholds, budgets, and attribution rules before execution.
