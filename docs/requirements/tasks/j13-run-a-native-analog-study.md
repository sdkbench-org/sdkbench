<!-- Generated from catalog.json by tools/requirements_docs.py. Do not edit directly. -->

# J13 - Run a native analog study

[All tasks](../TASK_CATALOG.md) | [Acceptance rules](../ACCEPTANCE.md) | [Traceability](../TRACEABILITY.md)

Status: requirements only. No task in this file is claimed as implemented or executed.

Workflow grounding: [S04](../SOURCES.md#s04). Sources inform context; they do not establish universal requirements or user-study validation.

<a id="t061"></a>

## T061 - Describe a native analog experiment

**User need:** A researcher needs to specify geometry and time-dependent interactions directly.

**Target users:** [P12](../REQUIREMENTS_MAP.md#p12), [P04](../REQUIREMENTS_MAP.md#p04).

**Applicability tags:** analog. Instance selection and conditional edges must be frozen before participant evaluation.

**Workflow stages:** formulate, express.

**Required input and constraints:** Sites, species, initial configuration, coupling law, boundaries, fields and physical units.

**Required output:** An inspectable analog program with explicit interpolation and control semantics.

**Required capabilities:** [C04](../CAPABILITIES.md#c04), [C16](../CAPABILITIES.md#c16).

**Function traceability:**

- [F16.01](../CAPABILITIES.md#f16-01): Describe geometry and interactions. Required for every instance of this task family.
- [F16.02](../CAPABILITIES.md#f16-02): Define time-dependent controls. Required for every instance of this task family.
- [F04.04](../CAPABILITIES.md#f04-04): Specify scientific problem inputs. Required for every instance of this task family.

**Acceptance profiles:** [A02](../ACCEPTANCE.md#a02), [A10](../ACCEPTANCE.md#a10).

**Task-specific acceptance:** Geometry, interactions, units and schedule endpoints match independent small fixtures; no gate-model discretization is imposed without an explicit method declaration.

**Measurements:** model fidelity; construction time; validation cost.

**Required negative case:** Changing lattice boundaries or silently converting a piecewise schedule to a different interpolation changes the task.

**Instance readiness:** Use the [instance specification template](../TASK_SPEC_TEMPLATE.md); bind fixtures, independent references, numerical/statistical thresholds, budgets, and attribution rules before execution.

<a id="t062"></a>

## T062 - Compute observables of a native analog evolution

**User need:** A scientist needs predicted observables or samples for an analog study.

**Target users:** [P12](../REQUIREMENTS_MAP.md#p12), [P04](../REQUIREMENTS_MAP.md#p04).

**Applicability tags:** analog. Instance selection and conditional edges must be frozen before participant evaluation.

**Workflow stages:** execute, estimate.

**Required input and constraints:** A fixed analog program, initial state, observable/time grid and solver/error budget.

**Required output:** Observable trajectories or samples with method and uncertainty metadata.

**Required capabilities:** [C07](../CAPABILITIES.md#c07), [C12](../CAPABILITIES.md#c12), [C16](../CAPABILITIES.md#c16).

**Function traceability:**

- [F16.03](../CAPABILITIES.md#f16-03): Simulate and measure analog evolution. Required for every instance of this task family.
- [F16.01](../CAPABILITIES.md#f16-01): Describe geometry and interactions. Required for every instance of this task family.
- [F07.04](../CAPABILITIES.md#f07-04): Simulate structured evolution. Required for every instance of this task family.
- [F12.02](../CAPABILITIES.md#f12-02): Estimate quantities with uncertainty. Required for every instance of this task family.

**Acceptance profiles:** [A03](../ACCEPTANCE.md#a03), [A04](../ACCEPTANCE.md#a04), [A06](../ACCEPTANCE.md#a06), [A10](../ACCEPTANCE.md#a10).

**Task-specific acceptance:** Small direct-Hamiltonian references and larger declared convergence checks pass; approximation, loss and sampling assumptions remain explicit.

**Measurements:** time to observable accuracy; memory; distribution error.

**Required negative case:** An easier gate approximation cannot replace the requested evolution outside the agreed discretization budget.

**Instance readiness:** Use the [instance specification template](../TASK_SPEC_TEMPLATE.md); bind fixtures, independent references, numerical/statistical thresholds, budgets, and attribution rules before execution.

<a id="t063"></a>

## T063 - Prepare an analog program for a constrained device

**User need:** A device user needs physical geometry and controls that the target can implement.

**Target users:** [P12](../REQUIREMENTS_MAP.md#p12), [P09](../REQUIREMENTS_MAP.md#p09).

**Applicability tags:** analog. Instance selection and conditional edges must be frozen before participant evaluation.

**Workflow stages:** compile, verify.

**Required input and constraints:** A program plus spacing, placement, field, slew-rate, clock and local/global control limits.

**Required output:** A legal target program with a record of rounding, discretization and unsupported requirements.

**Required capabilities:** [C06](../CAPABILITIES.md#c06), [C11](../CAPABILITIES.md#c11), [C16](../CAPABILITIES.md#c16).

**Function traceability:**

- [F16.04](../CAPABILITIES.md#f16-04): Translate to a compatible analog device. Required for every instance of this task family.
- [F16.02](../CAPABILITIES.md#f16-02): Define time-dependent controls. Required for every instance of this task family.
- [F11.01](../CAPABILITIES.md#f11-01): Discover and select execution targets. Required for every instance of this task family.
- [F06.01](../CAPABILITIES.md#f06-01): Describe an executable target. Required for every instance of this task family.

**Acceptance profiles:** [A05](../ACCEPTANCE.md#a05), [A10](../ACCEPTANCE.md#a10).

**Task-specific acceptance:** Independent target checks pass and the induced program change remains inside the declared tolerance; infeasible programs are diagnosed before submission.

**Measurements:** constraint pass rate; rounding error; compile time.

**Required negative case:** Unavailable local addressing cannot silently become a global field.

**Instance readiness:** Use the [instance specification template](../TASK_SPEC_TEMPLATE.md); bind fixtures, independent references, numerical/statistical thresholds, budgets, and attribution rules before execution.

<a id="t064"></a>

## T064 - Interpret analog measurements with loading and loss records

**User need:** A user needs an honest denominator when particles are absent or lost.

**Target users:** [P12](../REQUIREMENTS_MAP.md#p12), [P08](../REQUIREMENTS_MAP.md#p08), [P09](../REQUIREMENTS_MAP.md#p09).

**Applicability tags:** analog. Instance selection and conditional edges must be frozen before participant evaluation.

**Workflow stages:** execute, estimate.

**Required input and constraints:** Raw loading/pre/post-measurement records, a frozen postselection rule and desired correlations.

**Required output:** Raw and conditional estimates, loss fractions, acceptance denominators and uncertainty.

**Required capabilities:** [C11](../CAPABILITIES.md#c11), [C12](../CAPABILITIES.md#c12), [C16](../CAPABILITIES.md#c16).

**Function traceability:**

- [F16.05](../CAPABILITIES.md#f16-05): Track losses and analog experiment context. Required for every instance of this task family.
- [F12.01](../CAPABILITIES.md#f12-01): Validate and normalize result records. Required for every instance of this task family.
- [F12.02](../CAPABILITIES.md#f12-02): Estimate quantities with uncertainty. Required for every instance of this task family.
- [F11.05](../CAPABILITIES.md#f11-05): Preserve acquisition and result provenance. Required for every instance of this task family.

**Acceptance profiles:** [A04](../ACCEPTANCE.md#a04), [A08](../ACCEPTANCE.md#a08), [A10](../ACCEPTANCE.md#a10).

**Task-specific acceptance:** Counts reconcile across loading, loss and selection; both unconditional and conditional meanings are explicit and the estimator follows the frozen rule.

**Measurements:** retained fraction; loss rate; estimation error; total shots.

**Required negative case:** Discarding loss events without reporting them cannot improve a success metric invisibly.

**Instance readiness:** Use the [instance specification template](../TASK_SPEC_TEMPLATE.md); bind fixtures, independent references, numerical/statistical thresholds, budgets, and attribution rules before execution.

<a id="t065"></a>

## T065 - Compare analog schedules for the same physical objective

**User need:** A researcher needs a schedule comparison tied to an unchanged physical problem.

**Target users:** [P12](../REQUIREMENTS_MAP.md#p12), [P14](../REQUIREMENTS_MAP.md#p14).

**Applicability tags:** analog. Instance selection and conditional edges must be frozen before participant evaluation.

**Workflow stages:** optimize, estimate.

**Required input and constraints:** A physical objective, admissible schedule class, model/target constraints and tuning/evaluation budget.

**Required output:** Schedules, objective/feasibility distributions and total cost.

**Required capabilities:** [C09](../CAPABILITIES.md#c09), [C13](../CAPABILITIES.md#c13), [C16](../CAPABILITIES.md#c16).

**Function traceability:**

- [F16.01](../CAPABILITIES.md#f16-01): Describe geometry and interactions. Required for every instance of this task family.
- [F16.02](../CAPABILITIES.md#f16-02): Define time-dependent controls. Required for every instance of this task family.
- [F16.03](../CAPABILITIES.md#f16-03): Simulate and measure analog evolution. Required for every instance of this task family.
- [F09.05](../CAPABILITIES.md#f09-05): Budget training and adaptive search. Required for every instance of this task family.
- [F13.03](../CAPABILITIES.md#f13-03): Solve optimization instances. Required for every instance of this task family.

**Acceptance profiles:** [A06](../ACCEPTANCE.md#a06), [A09](../ACCEPTANCE.md#a09), [A10](../ACCEPTANCE.md#a10).

**Task-specific acceptance:** All compared schedules solve the same objective and satisfy identical constraints; selection cost, solver approximation and held-out evaluation are disclosed.

**Measurements:** time/evaluations to target; objective gap; physical duration.

**Required negative case:** Changing interaction strength or allowed controls to make one schedule easier is a different cohort.

**Instance readiness:** Use the [instance specification template](../TASK_SPEC_TEMPLATE.md); bind fixtures, independent references, numerical/statistical thresholds, budgets, and attribution rules before execution.
