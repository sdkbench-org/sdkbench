<!-- Generated from catalog.json by tools/requirements_docs.py. Do not edit directly. -->

# J05 - Compute the quantities a study needs

[All tasks](../TASK_CATALOG.md) | [Acceptance rules](../ACCEPTANCE.md) | [Traceability](../TRACEABILITY.md)

Status: requirements only. No task in this file is claimed as implemented or executed.

Workflow grounding: [S09](../SOURCES.md#s09). Sources inform context; they do not establish universal requirements or user-study validation.

<a id="t021"></a>

## T021 - Compute only the amplitudes or probabilities needed by a study

**User need:** A researcher needs selected outputs without paying for unnecessary output materialization.

**Target users:** [P02](../REQUIREMENTS_MAP.md#p02), [P07](../REQUIREMENTS_MAP.md#p07).

**Applicability tags:** gate, qudit. Instance selection and conditional edges must be frozen before participant evaluation.

**Workflow stages:** execute, estimate.

**Required input and constraints:** A program, nonzero initial state and selected basis indices with a fixed representation/precision contract.

**Required output:** Indexed amplitudes or probabilities with execution and output costs separated.

**Required capabilities:** [C05](../CAPABILITIES.md#c05), [C19](../CAPABILITIES.md#c19).

**Function traceability:**

- [F05.01](../CAPABILITIES.md#f05-01): Evolve a state from an explicit input. Required for every instance of this task family.
- [F05.03](../CAPABILITIES.md#f05-03): Compute exact observables and reduced states. Required for every instance of this task family.
- [F19.04](../CAPABILITIES.md#f19-04): Measure and enforce execution budgets. Required for every instance of this task family.

**Acceptance profiles:** [A03](../ACCEPTANCE.md#a03).

**Task-specific acceptance:** Values match the small reference and indexing contract; output volume and any full-state materialization are disclosed.

**Measurements:** time to requested output; peak memory; output bytes; error.

**Required negative case:** Selected-index order and an unused-wire permutation cannot change the interpreted answer.

**Instance readiness:** Use the [instance specification template](../TASK_SPEC_TEMPLATE.md); bind fixtures, independent references, numerical/statistical thresholds, budgets, and attribution rules before execution.

<a id="t022"></a>

## T022 - Evaluate a large observable collection correctly

**User need:** A scientist needs energies and correlations containing many terms, often sharing a state.

**Target users:** [P03](../REQUIREMENTS_MAP.md#p03), [P04](../REQUIREMENTS_MAP.md#p04), [P05](../REQUIREMENTS_MAP.md#p05).

**Applicability tags:** gate. Instance selection and conditional edges must be frozen before participant evaluation.

**Workflow stages:** execute, estimate.

**Required input and constraints:** Pauli or sparse observable sums with coefficients, support patterns and exact or shot-based execution mode.

**Required output:** All requested expectations with correct coefficient, basis and covariance handling.

**Required capabilities:** [C04](../CAPABILITIES.md#c04), [C05](../CAPABILITIES.md#c05), [C12](../CAPABILITIES.md#c12), [C19](../CAPABILITIES.md#c19).

**Function traceability:**

- [F04.02](../CAPABILITIES.md#f04-02): Manipulate structured observables. Required for every instance of this task family.
- [F05.03](../CAPABILITIES.md#f05-03): Compute exact observables and reduced states. Required for every instance of this task family.
- [F12.03](../CAPABILITIES.md#f12-03): Plan and combine measurements. Required for every instance of this task family.
- [F19.03](../CAPABILITIES.md#f19-03): Parallelize independent work. Required for every instance of this task family.

**Acceptance profiles:** [A03](../ACCEPTANCE.md#a03), [A04](../ACCEPTANCE.md#a04).

**Task-specific acceptance:** Exact outputs meet the numerical oracle; sampled outputs meet the specified statistical equivalence contract; all state preparations and shots are charged.

**Measurements:** total evaluation time; observable throughput; state preparations; estimation error.

**Required negative case:** Dropping small terms or independently normalizing coefficients requires an explicit approximation contract.

**Instance readiness:** Use the [instance specification template](../TASK_SPEC_TEMPLATE.md); bind fixtures, independent references, numerical/statistical thresholds, budgets, and attribution rules before execution.

<a id="t023"></a>

## T023 - Compute subsystem information without changing subsystem identity

**User need:** A researcher needs entanglement or local-state information on explicitly selected subsystems.

**Target users:** [P04](../REQUIREMENTS_MAP.md#p04), [P08](../REQUIREMENTS_MAP.md#p08).

**Applicability tags:** gate, qudit. Instance selection and conditional edges must be frozen before participant evaluation.

**Workflow stages:** execute, estimate.

**Required input and constraints:** Entangled pure/mixed fixtures, noncontiguous subsystem lists and a basis-order convention.

**Required output:** Reduced states, correlations or entropy under specified conventions.

**Required capabilities:** [C04](../CAPABILITIES.md#c04), [C05](../CAPABILITIES.md#c05), [C12](../CAPABILITIES.md#c12).

**Function traceability:**

- [F04.01](../CAPABILITIES.md#f04-01): Represent states and linear operators. Required for every instance of this task family.
- [F05.03](../CAPABILITIES.md#f05-03): Compute exact observables and reduced states. Required for every instance of this task family.
- [F12.05](../CAPABILITIES.md#f12-05): Export interpretable analysis. Required for every instance of this task family.

**Acceptance profiles:** [A03](../ACCEPTANCE.md#a03).

**Task-specific acceptance:** Partial traces and derived quantities match independent small references; trace, dimensions and eigenvalue handling satisfy the contract.

**Measurements:** subsystem error; runtime; memory.

**Required negative case:** A subsystem permutation or entropy unit mismatch must be detected rather than hidden by a symmetric test state.

**Instance readiness:** Use the [instance specification template](../TASK_SPEC_TEMPLATE.md); bind fixtures, independent references, numerical/statistical thresholds, budgets, and attribution rules before execution.

<a id="t024"></a>

## T024 - Work with a Hamiltonian without unnecessary dense expansion

**User need:** A user needs algebra and action on large structured operators within memory limits.

**Target users:** [P03](../REQUIREMENTS_MAP.md#p03), [P04](../REQUIREMENTS_MAP.md#p04), [P07](../REQUIREMENTS_MAP.md#p07).

**Applicability tags:** gate. Instance selection and conditional edges must be frozen before participant evaluation.

**Workflow stages:** formulate, execute.

**Required input and constraints:** Sparse or Pauli-sum Hamiltonians, symmetry sectors, coefficient scales and memory budgets.

**Required output:** Operator action, expectations or simplified representations with equivalent semantics.

**Required capabilities:** [C04](../CAPABILITIES.md#c04), [C05](../CAPABILITIES.md#c05), [C19](../CAPABILITIES.md#c19).

**Function traceability:**

- [F04.01](../CAPABILITIES.md#f04-01): Represent states and linear operators. Required for every instance of this task family.
- [F04.02](../CAPABILITIES.md#f04-02): Manipulate structured observables. Required for every instance of this task family.
- [F05.03](../CAPABILITIES.md#f05-03): Compute exact observables and reduced states. Required for every instance of this task family.
- [F19.04](../CAPABILITIES.md#f19-04): Measure and enforce execution budgets. Required for every instance of this task family.

**Acceptance profiles:** [A02](../ACCEPTANCE.md#a02), [A03](../ACCEPTANCE.md#a03).

**Task-specific acceptance:** Small cases match dense algebra; declared sparsity and memory limits are respected, and transformations retain coefficients and constants.

**Measurements:** operator action time; peak memory; term count; error.

**Required negative case:** A constant energy offset, canceled term or symmetry-sector restriction cannot be lost.

**Instance readiness:** Use the [instance specification template](../TASK_SPEC_TEMPLATE.md); bind fixtures, independent references, numerical/statistical thresholds, budgets, and attribution rules before execution.

<a id="t025"></a>

## T025 - Evaluate a parameter sweep without cross-run contamination

**User need:** A study needs many parameter points or initial states with predictable ordering and reuse.

**Target users:** [P02](../REQUIREMENTS_MAP.md#p02), [P05](../REQUIREMENTS_MAP.md#p05), [P07](../REQUIREMENTS_MAP.md#p07).

**Applicability tags:** gate. Instance selection and conditional edges must be frozen before participant evaluation.

**Workflow stages:** execute, operate.

**Required input and constraints:** Distinct parameter/initial-state batches, repeated execution and serial reference cases.

**Required output:** Ordered outputs with explicit cache/compilation reuse and batch semantics.

**Required capabilities:** [C02](../CAPABILITIES.md#c02), [C05](../CAPABILITIES.md#c05), [C09](../CAPABILITIES.md#c09), [C19](../CAPABILITIES.md#c19).

**Function traceability:**

- [F02.03](../CAPABILITIES.md#f02-03): Bind and reuse parameters. Required for every instance of this task family.
- [F05.05](../CAPABILITIES.md#f05-05): Select and disclose execution implementation. Required for every instance of this task family.
- [F09.02](../CAPABILITIES.md#f09-02): Batch independent data and parameters. Required for every instance of this task family.
- [F19.03](../CAPABILITIES.md#f19-03): Parallelize independent work. Required for every instance of this task family.

**Acceptance profiles:** [A03](../ACCEPTANCE.md#a03), [A11](../ACCEPTANCE.md#a11).

**Task-specific acceptance:** Every output matches its corresponding serial reference; cache invalidation works after changed parameters, program or device.

**Measurements:** end-to-end sweep time; throughput; memory; reuse overhead.

**Required negative case:** Broadcasting one parameter vector into all samples or reusing a stale compiled binding must fail.

**Instance readiness:** Use the [instance specification template](../TASK_SPEC_TEMPLATE.md); bind fixtures, independent references, numerical/statistical thresholds, budgets, and attribution rules before execution.
