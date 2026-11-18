<!-- Generated from catalog.json by tools/requirements_docs.py. Do not edit directly. -->

# J08 - Answer a scientific or application question

[All tasks](../TASK_CATALOG.md) | [Acceptance rules](../ACCEPTANCE.md) | [Traceability](../TRACEABILITY.md)

Status: requirements only. No task in this file is claimed as implemented or executed.

Workflow grounding: [S03](../SOURCES.md#s03), [S06](../SOURCES.md#s06), [S09](../SOURCES.md#s09). Sources inform context; they do not establish universal requirements or user-study validation.

<a id="t036"></a>

## T036 - Estimate molecular ground or excited-state energies

**User need:** A chemistry researcher needs energies for the same molecular problem, with all conventions explicit.

**Target users:** [P03](../REQUIREMENTS_MAP.md#p03).

**Applicability tags:** gate. Instance selection and conditional edges must be frozen before participant evaluation.

**Workflow stages:** formulate, express, optimize, estimate.

**Required input and constraints:** Frozen geometry/units, basis, charge/spin, active space, Hamiltonian constants, state/spectral target and reference uncertainty.

**Required output:** Energies, state/optimization evidence and end-to-end preparation/evaluation costs.

**Required capabilities:** [C04](../CAPABILITIES.md#c04), [C09](../CAPABILITIES.md#c09), [C12](../CAPABILITIES.md#c12), [C13](../CAPABILITIES.md#c13).

**Function traceability:**

- [F04.03](../CAPABILITIES.md#f04-03): Map fermionic and bosonic models. Required for every instance of this task family.
- [F04.04](../CAPABILITIES.md#f04-04): Specify scientific problem inputs. Required for every instance of this task family.
- [F13.01](../CAPABILITIES.md#f13-01): Solve energy or spectral problems. Required for every instance of this task family.
- [F09.05](../CAPABILITIES.md#f09-05): Budget training and adaptive search. Required for every instance of this task family.
- [F12.02](../CAPABILITIES.md#f12-02): Estimate quantities with uncertainty. Required for every instance of this task family.

**Acceptance profiles:** [A03](../ACCEPTANCE.md#a03), [A04](../ACCEPTANCE.md#a04), [A09](../ACCEPTANCE.md#a09).

**Task-specific acceptance:** The requested total or electronic-energy convention and state target match the reference; error plus reference uncertainty fits the budget and all preprocessing/calls are recorded.

**Measurements:** energy error; time to target; shots; peak memory.

**Required negative case:** A different active space, omitted nuclear constant or ground-state answer to an excited-state request is a different task, not a speedup.

**Instance readiness:** Use the [instance specification template](../TASK_SPEC_TEMPLATE.md); bind fixtures, independent references, numerical/statistical thresholds, budgets, and attribution rules before execution.

<a id="t037"></a>

## T037 - Predict a many-body dynamics or correlation study

**User need:** A scientist needs a physically specified trajectory rather than a circuit-runtime number.

**Target users:** [P04](../REQUIREMENTS_MAP.md#p04).

**Applicability tags:** gate, analog, qudit, cv. Instance selection and conditional edges must be frozen before participant evaluation.

**Workflow stages:** formulate, execute, estimate.

**Required input and constraints:** Lattice/graph, local Hilbert dimensions, spin/fermion/boson encoding, couplings, units, boundaries, initial state, output times and selected correlations.

**Required output:** A time series and an auditable total error/resource account.

**Required capabilities:** [C04](../CAPABILITIES.md#c04), [C07](../CAPABILITIES.md#c07), [C12](../CAPABILITIES.md#c12), [C13](../CAPABILITIES.md#c13).

**Function traceability:**

- [F04.02](../CAPABILITIES.md#f04-02): Manipulate structured observables. Required for every instance of this task family.
- [F04.04](../CAPABILITIES.md#f04-04): Specify scientific problem inputs. Required for every instance of this task family.
- [F13.02](../CAPABILITIES.md#f13-02): Study dynamics and correlations. Required for every instance of this task family.
- [F07.04](../CAPABILITIES.md#f07-04): Simulate structured evolution. Required for every instance of this task family.
- [F12.05](../CAPABILITIES.md#f12-05): Export interpretable analysis. Required for every instance of this task family.
- [F04.03](../CAPABILITIES.md#f04-03): Map fermionic and bosonic models. Required for every instance of this task family.

**Acceptance profiles:** [A03](../ACCEPTANCE.md#a03), [A06](../ACCEPTANCE.md#a06), [A09](../ACCEPTANCE.md#a09).

**Task-specific acceptance:** Small reference and larger convergence cases meet the prescribed observable error; constants, boundary conditions and time grids are identical across compared workflows.

**Measurements:** observable error; time to accuracy; memory; completed time horizon.

**Required negative case:** Selecting only easy early-time points or omitting correlation terms must remain a failed/incomplete study.

**Instance readiness:** Use the [instance specification template](../TASK_SPEC_TEMPLATE.md); bind fixtures, independent references, numerical/statistical thresholds, budgets, and attribution rules before execution.

<a id="t038"></a>

## T038 - Solve a constrained optimization instance and decode the answer

**User need:** A practitioner needs feasible solutions in the original application variables.

**Target users:** [P14](../REQUIREMENTS_MAP.md#p14).

**Applicability tags:** gate, annealing. Instance selection and conditional edges must be frozen before participant evaluation.

**Workflow stages:** formulate, optimize, estimate.

**Required input and constraints:** Frozen instance distribution, constraints, objective, classical reference or bound and resource budget.

**Required output:** Decoded solutions, independently recomputed objectives, feasibility and success distributions.

**Required capabilities:** [C04](../CAPABILITIES.md#c04), [C09](../CAPABILITIES.md#c09), [C13](../CAPABILITIES.md#c13), [C18](../CAPABILITIES.md#c18).

**Function traceability:**

- [F04.05](../CAPABILITIES.md#f04-05): Formulate objectives and constraints. Required for every instance of this task family.
- [F13.03](../CAPABILITIES.md#f13-03): Solve optimization instances. Required for every instance of this task family.
- [F18.04](../CAPABILITIES.md#f18-04): Decode and validate candidate solutions. Required when the frozen instance includes the annealing applicability tag.
- [F09.05](../CAPABILITIES.md#f09-05): Budget training and adaptive search. Required for every instance of this task family.

**Acceptance profiles:** [A09](../ACCEPTANCE.md#a09).

**Task-specific acceptance:** Every claimed solution is checked in the original problem; success meets the predeclared quality/feasibility target and includes formulation, search and repair costs.

**Measurements:** feasible-solution rate; objective gap; time to target; total evaluations.

**Required negative case:** A low penalized energy is not evidence of original-problem feasibility; classical repair cannot be hidden.

**Instance readiness:** Use the [instance specification template](../TASK_SPEC_TEMPLATE.md); bind fixtures, independent references, numerical/statistical thresholds, budgets, and attribution rules before execution.

<a id="t039"></a>

## T039 - Estimate a phase or amplitude with complete oracle accounting

**User need:** An algorithm researcher needs an inference result at specified accuracy and confidence.

**Target users:** [P02](../REQUIREMENTS_MAP.md#p02).

**Applicability tags:** gate, adaptive. Instance selection and conditional edges must be frozen before participant evaluation.

**Workflow stages:** express, execute, estimate.

**Required input and constraints:** A declared oracle and construction, input preparation, target parameter, precision/confidence and query/time budget.

**Required output:** An estimate, interval and full controlled-oracle/preparation/measurement cost.

**Required capabilities:** [C02](../CAPABILITIES.md#c02), [C03](../CAPABILITIES.md#c03), [C12](../CAPABILITIES.md#c12), [C13](../CAPABILITIES.md#c13), [C19](../CAPABILITIES.md#c19).

**Function traceability:**

- [F13.04](../CAPABILITIES.md#f13-04): Estimate algorithmic quantities. Required for every instance of this task family.
- [F02.02](../CAPABILITIES.md#f02-02): Compose, invert and control subprograms. Required for every instance of this task family.
- [F03.03](../CAPABILITIES.md#f03-03): Execute bounded loops and adaptive routines. Required for every instance of this task family.
- [F12.02](../CAPABILITIES.md#f12-02): Estimate quantities with uncertainty. Required for every instance of this task family.
- [F19.04](../CAPABILITIES.md#f19-04): Measure and enforce execution budgets. Required for every instance of this task family.

**Acceptance profiles:** [A03](../ACCEPTANCE.md#a03), [A04](../ACCEPTANCE.md#a04), [A09](../ACCEPTANCE.md#a09).

**Task-specific acceptance:** The inference error and interval coverage meet the frozen contract over the prescribed instance ensemble; oracle and classical postprocessing costs are included.

**Measurements:** queries to target; success probability; wall time; workspace.

**Required negative case:** Counting a controlled high-power oracle as one free elementary operation cannot support an end-to-end efficiency claim.

**Instance readiness:** Use the [instance specification template](../TASK_SPEC_TEMPLATE.md); bind fixtures, independent references, numerical/statistical thresholds, budgets, and attribution rules before execution.

<a id="t040"></a>

## T040 - Extract a useful observable from a quantum linear-algebra routine

**User need:** A user needs an interpretable answer, not only a normalized state encoding an unknown solution.

**Target users:** [P02](../REQUIREMENTS_MAP.md#p02), [P04](../REQUIREMENTS_MAP.md#p04).

**Applicability tags:** gate. Instance selection and conditional edges must be frozen before participant evaluation.

**Workflow stages:** formulate, express, execute, estimate.

**Required input and constraints:** A bounded matrix problem, conditioning promise, preparation/block-encoding contract and explicitly requested observable or solution output.

**Required output:** The requested classical quantity or declared quantum-state output with all success probabilities.

**Required capabilities:** [C02](../CAPABILITIES.md#c02), [C04](../CAPABILITIES.md#c04), [C12](../CAPABILITIES.md#c12), [C13](../CAPABILITIES.md#c13).

**Function traceability:**

- [F04.01](../CAPABILITIES.md#f04-01): Represent states and linear operators. Required for every instance of this task family.
- [F02.04](../CAPABILITIES.md#f02-04): Prepare states and encode inputs. Required for every instance of this task family.
- [F13.04](../CAPABILITIES.md#f13-04): Estimate algorithmic quantities. Required for every instance of this task family.
- [F12.02](../CAPABILITIES.md#f12-02): Estimate quantities with uncertainty. Required for every instance of this task family.

**Acceptance profiles:** [A03](../ACCEPTANCE.md#a03), [A04](../ACCEPTANCE.md#a04), [A09](../ACCEPTANCE.md#a09).

**Task-specific acceptance:** The specified output matches the independent reference within budget; conditioning, postselection, preparation and readout costs are disclosed.

**Measurements:** output error; success probability; total time; oracle calls.

**Required negative case:** Comparing quantum-state preparation time to a full classical-vector output is disallowed unless the output contracts are made identical.

**Instance readiness:** Use the [instance specification template](../TASK_SPEC_TEMPLATE.md); bind fixtures, independent references, numerical/statistical thresholds, budgets, and attribution rules before execution.

<a id="t091"></a>

## T091 - Train and evaluate a quantum-kernel predictor

**User need:** A researcher needs predictive utility of a quantum kernel measured on unseen data under a complete computation budget.

**Target users:** [P05](../REQUIREMENTS_MAP.md#p05).

**Applicability tags:** gate. Instance selection and conditional edges must be frozen before participant evaluation.

**Workflow stages:** formulate, execute, optimize, estimate.

**Required input and constraints:** A frozen dataset/split, encoding, kernel definition, sampled or exact evaluation policy, regularization search space and classical comparison protocol.

**Required output:** Kernel matrices or predictions, train/validation/test results, conditioning diagnostics and all kernel/search costs.

**Required capabilities:** [C04](../CAPABILITIES.md#c04), [C09](../CAPABILITIES.md#c09), [C12](../CAPABILITIES.md#c12), [C13](../CAPABILITIES.md#c13).

**Function traceability:**

- [F13.05](../CAPABILITIES.md#f13-05): Evaluate predictive or kernel methods. Required for every instance of this task family.
- [F09.03](../CAPABILITIES.md#f09-03): Optimize and evaluate reproducibly. Required for every instance of this task family.
- [F09.05](../CAPABILITIES.md#f09-05): Budget training and adaptive search. Required for every instance of this task family.
- [F12.02](../CAPABILITIES.md#f12-02): Estimate quantities with uncertainty. Required for every instance of this task family.
- [F04.02](../CAPABILITIES.md#f04-02): Manipulate structured observables. Required for every instance of this task family.

**Acceptance profiles:** [A03](../ACCEPTANCE.md#a03), [A04](../ACCEPTANCE.md#a04), [A09](../ACCEPTANCE.md#a09).

**Task-specific acceptance:** Small exact kernels match independent references; finite-shot uncertainty and any matrix repair are disclosed; the frozen held-out quality target is evaluated without test-set tuning and with all preprocessing and hyperparameter search charged.

**Measurements:** held-out predictive quality; total time to target; kernel/shot evaluations; matrix conditioning.

**Required negative case:** Repairing a sampled kernel, tuning on test labels or omitting classical training/search cost cannot improve the reported result invisibly.

**Instance readiness:** Use the [instance specification template](../TASK_SPEC_TEMPLATE.md); bind fixtures, independent references, numerical/statistical thresholds, budgets, and attribution rules before execution.
