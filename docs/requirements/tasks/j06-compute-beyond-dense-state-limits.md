<!-- Generated from catalog.json by tools/requirements_docs.py. Do not edit directly. -->

# J06 - Compute beyond dense-state limits

[All tasks](../TASK_CATALOG.md) | [Acceptance rules](../ACCEPTANCE.md) | [Traceability](../TRACEABILITY.md)

Status: requirements only. No task in this file is claimed as implemented or executed.

Workflow grounding: [S10](../SOURCES.md#s10). Sources inform context; they do not establish universal requirements or user-study validation.

<a id="t026"></a>

## T026 - Simulate an extended low-entanglement system

**User need:** A researcher needs large-system local observables that do not require a full dense state.

**Target users:** [P04](../REQUIREMENTS_MAP.md#p04), [P07](../REQUIREMENTS_MAP.md#p07).

**Applicability tags:** gate. Instance selection and conditional edges must be frozen before participant evaluation.

**Workflow stages:** execute, verify.

**Required input and constraints:** A low-entanglement circuit family, requested observables and a prescribed error/resource budget.

**Required output:** Local results and representation/truncation diagnostics.

**Required capabilities:** [C05](../CAPABILITIES.md#c05), [C07](../CAPABILITIES.md#c07).

**Function traceability:**

- [F07.01](../CAPABILITIES.md#f07-01): Control representation and truncation. Required for every instance of this task family.
- [F07.03](../CAPABILITIES.md#f07-03): Track numerical and approximation error. Required for every instance of this task family.
- [F07.05](../CAPABILITIES.md#f07-05): Return outputs without accidental densification. Required for every instance of this task family.
- [F05.03](../CAPABILITIES.md#f05-03): Compute exact observables and reduced states. Required for every instance of this task family.

**Acceptance profiles:** [A03](../ACCEPTANCE.md#a03), [A06](../ACCEPTANCE.md#a06).

**Task-specific acceptance:** Small overlaps agree with exact references; larger results meet the declared observable or certified-bound contract, and no unrequested dense state is materialized.

**Measurements:** time at matched error; memory; maximum completed size.

**Required negative case:** A large wire count with an uncontrolled observable error is not a successful capacity result.

**Instance readiness:** Use the [instance specification template](../TASK_SPEC_TEMPLATE.md); bind fixtures, independent references, numerical/statistical thresholds, budgets, and attribution rules before execution.

<a id="t027"></a>

## T027 - Determine where an approximate representation stops being reliable

**User need:** A user needs to recognize approximation failure rather than receive plausible-looking numbers.

**Target users:** [P04](../REQUIREMENTS_MAP.md#p04), [P07](../REQUIREMENTS_MAP.md#p07).

**Applicability tags:** gate. Instance selection and conditional edges must be frozen before participant evaluation.

**Workflow stages:** verify, execute, estimate.

**Required input and constraints:** Matched low/high-entanglement families, escalating depth and truncation budgets.

**Required output:** Accuracy/resource curves with explicit failure or uncertainty boundaries.

**Required capabilities:** [C07](../CAPABILITIES.md#c07), [C19](../CAPABILITIES.md#c19), [C20](../CAPABILITIES.md#c20).

**Function traceability:**

- [F07.01](../CAPABILITIES.md#f07-01): Control representation and truncation. Required for every instance of this task family.
- [F07.03](../CAPABILITIES.md#f07-03): Track numerical and approximation error. Required for every instance of this task family.
- [F19.04](../CAPABILITIES.md#f19-04): Measure and enforce execution budgets. Required for every instance of this task family.
- [F20.05](../CAPABILITIES.md#f20-05): Expose inspectable errors and traces. Required for every instance of this task family.

**Acceptance profiles:** [A06](../ACCEPTANCE.md#a06).

**Task-specific acceptance:** Measured reference errors stay within the accepted region; outside it, violations remain visible; discarded weight is not treated as a universal observable-error certificate.

**Measurements:** error versus resources; budget completion; invalid-success rate.

**Required negative case:** Renormalization alone cannot turn a strongly truncated state into evidence of a correct computation.

**Instance readiness:** Use the [instance specification template](../TASK_SPEC_TEMPLATE.md); bind fixtures, independent references, numerical/statistical thresholds, budgets, and attribution rules before execution.

<a id="t028"></a>

## T028 - Compute a tensor-network output within a memory ceiling

**User need:** A simulator user needs a feasible contraction strategy whose planning cost is known.

**Target users:** [P07](../REQUIREMENTS_MAP.md#p07), [P15](../REQUIREMENTS_MAP.md#p15).

**Applicability tags:** gate, analog. Instance selection and conditional edges must be frozen before participant evaluation.

**Workflow stages:** compile, execute, operate.

**Required input and constraints:** Network families, requested outputs, contraction-search budget and memory ceiling.

**Required output:** A contraction/slicing plan, planning log and validated output.

**Required capabilities:** [C07](../CAPABILITIES.md#c07), [C19](../CAPABILITIES.md#c19).

**Function traceability:**

- [F07.02](../CAPABILITIES.md#f07-02): Plan contractions and memory use. Required for every instance of this task family.
- [F07.05](../CAPABILITIES.md#f07-05): Return outputs without accidental densification. Required for every instance of this task family.
- [F19.02](../CAPABILITIES.md#f19-02): Partition states or tensor computations. Required for every instance of this task family.
- [F19.04](../CAPABILITIES.md#f19-04): Measure and enforce execution budgets. Required for every instance of this task family.

**Acceptance profiles:** [A03](../ACCEPTANCE.md#a03), [A06](../ACCEPTANCE.md#a06), [A11](../ACCEPTANCE.md#a11).

**Task-specific acceptance:** Planning plus execution stays within its cohort budget; output passes the independent feasible-size oracle and all slices are combined with the correct weights.

**Measurements:** planning time; execution time; peak memory; slice count.

**Required negative case:** A cached plan from another topology or omitted slices must not produce a successful result.

**Instance readiness:** Use the [instance specification template](../TASK_SPEC_TEMPLATE.md); bind fixtures, independent references, numerical/statistical thresholds, budgets, and attribution rules before execution.

<a id="t029"></a>

## T029 - Evolve a many-body state with controlled discretization and truncation

**User need:** A scientist needs physically meaningful time-series outputs with both integration and representation errors controlled.

**Target users:** [P04](../REQUIREMENTS_MAP.md#p04).

**Applicability tags:** gate, analog. Instance selection and conditional edges must be frozen before participant evaluation.

**Workflow stages:** execute, estimate.

**Required input and constraints:** A Hamiltonian, initial state, time grid, boundary conditions and error budget.

**Required output:** Observable trajectories with step-size and truncation diagnostics.

**Required capabilities:** [C04](../CAPABILITIES.md#c04), [C07](../CAPABILITIES.md#c07), [C13](../CAPABILITIES.md#c13).

**Function traceability:**

- [F07.03](../CAPABILITIES.md#f07-03): Track numerical and approximation error. Required for every instance of this task family.
- [F07.04](../CAPABILITIES.md#f07-04): Simulate structured evolution. Required for every instance of this task family.
- [F04.02](../CAPABILITIES.md#f04-02): Manipulate structured observables. Required for every instance of this task family.
- [F13.02](../CAPABILITIES.md#f13-02): Study dynamics and correlations. Required for every instance of this task family.

**Acceptance profiles:** [A03](../ACCEPTANCE.md#a03), [A06](../ACCEPTANCE.md#a06).

**Task-specific acceptance:** Small cases agree with exact evolution; refinement studies separate time-discretization and representation effects and satisfy the requested observable tolerance.

**Measurements:** time to accuracy; memory; conservation error.

**Required negative case:** Changing boundaries or the time unit cannot be used to obtain an easier but different evolution.

**Instance readiness:** Use the [instance specification template](../TASK_SPEC_TEMPLATE.md); bind fixtures, independent references, numerical/statistical thresholds, budgets, and attribution rules before execution.

<a id="t030"></a>

## T030 - Select a representation for a requested scientific output

**User need:** A user needs a practical answer at target accuracy, not the same internal algorithm in every implementation.

**Target users:** [P04](../REQUIREMENTS_MAP.md#p04), [P07](../REQUIREMENTS_MAP.md#p07).

**Applicability tags:** gate, analog. Instance selection and conditional edges must be frozen before participant evaluation.

**Workflow stages:** formulate, execute, estimate.

**Required input and constraints:** A fixed problem/output contract, candidate representation policies and total selection budget.

**Required output:** A validated output with method choice, selection cost and approximation provenance.

**Required capabilities:** [C05](../CAPABILITIES.md#c05), [C07](../CAPABILITIES.md#c07), [C19](../CAPABILITIES.md#c19).

**Function traceability:**

- [F05.05](../CAPABILITIES.md#f05-05): Select and disclose execution implementation. Required for every instance of this task family.
- [F07.01](../CAPABILITIES.md#f07-01): Control representation and truncation. Required for every instance of this task family.
- [F07.03](../CAPABILITIES.md#f07-03): Track numerical and approximation error. Required for every instance of this task family.
- [F07.05](../CAPABILITIES.md#f07-05): Return outputs without accidental densification. Required for every instance of this task family.
- [F19.04](../CAPABILITIES.md#f19-04): Measure and enforce execution budgets. Required for every instance of this task family.

**Acceptance profiles:** [A06](../ACCEPTANCE.md#a06), [A09](../ACCEPTANCE.md#a09).

**Task-specific acceptance:** The output meets the common error target; all method-selection runs are counted and comparisons distinguish matched-method from best-available workflows.

**Measurements:** total time to target; memory; selection overhead.

**Required negative case:** An automatic fallback to a different precision or approximation cannot remain undisclosed.

**Instance readiness:** Use the [instance specification template](../TASK_SPEC_TEMPLATE.md); bind fixtures, independent references, numerical/statistical thresholds, budgets, and attribution rules before execution.
