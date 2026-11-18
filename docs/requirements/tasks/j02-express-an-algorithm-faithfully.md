<!-- Generated from catalog.json by tools/requirements_docs.py. Do not edit directly. -->

# J02 - Express an algorithm faithfully

[All tasks](../TASK_CATALOG.md) | [Acceptance rules](../ACCEPTANCE.md) | [Traceability](../TRACEABILITY.md)

Status: requirements only. No task in this file is claimed as implemented or executed.

Workflow grounding: [S01](../SOURCES.md#s01), [S02](../SOURCES.md#s02), [S12](../SOURCES.md#s12). Sources inform context; they do not establish universal requirements or user-study validation.

<a id="t006"></a>

## T006 - Build and reuse a parameterized algorithm

**User need:** An algorithm researcher needs one program evaluated at many parameter points without semantic changes.

**Target users:** [P02](../REQUIREMENTS_MAP.md#p02), [P05](../REQUIREMENTS_MAP.md#p05).

**Applicability tags:** gate. Instance selection and conditional edges must be frozen before participant evaluation.

**Workflow stages:** express, verify, execute.

**Required input and constraints:** A generated program with shared parameters, noncommuting gates, unused wires and several complete bindings.

**Required output:** An inspectable reusable program and correctly ordered outputs for each binding.

**Required capabilities:** [C02](../CAPABILITIES.md#c02), [C05](../CAPABILITIES.md#c05), [C20](../CAPABILITIES.md#c20).

**Function traceability:**

- [F02.01](../CAPABILITIES.md#f02-01): Construct and inspect programs. Required for every instance of this task family.
- [F02.03](../CAPABILITIES.md#f02-03): Bind and reuse parameters. Required for every instance of this task family.
- [F05.01](../CAPABILITIES.md#f05-01): Evolve a state from an explicit input. Required for every instance of this task family.
- [F20.02](../CAPABILITIES.md#f20-02): Normalize conventions across boundaries. Required for every instance of this task family.

**Acceptance profiles:** [A02](../ACCEPTANCE.md#a02), [A03](../ACCEPTANCE.md#a03).

**Task-specific acceptance:** All parameter occurrences use the specified binding; outputs match independent small-instance references and reusing a program does not leak state between runs.

**Measurements:** construction time; binding time; repeat execution time; peak memory.

**Required negative case:** Missing, extra or shape-incompatible bindings are diagnosed explicitly.

**Instance readiness:** Use the [instance specification template](../TASK_SPEC_TEMPLATE.md); bind fixtures, independent references, numerical/statistical thresholds, budgets, and attribution rules before execution.

<a id="t007"></a>

## T007 - Compose controlled and inverted subroutines with clean workspace

**User need:** A researcher needs arithmetic or an oracle usable coherently inside a larger algorithm.

**Target users:** [P02](../REQUIREMENTS_MAP.md#p02).

**Applicability tags:** gate. Instance selection and conditional edges must be frozen before participant evaluation.

**Workflow stages:** express, verify.

**Required input and constraints:** A bounded arithmetic/predicate specification, allowed ancillas, control conditions and promised workspace postcondition.

**Required output:** A controlled composable subroutine and workspace/resource report.

**Required capabilities:** [C02](../CAPABILITIES.md#c02), [C03](../CAPABILITIES.md#c03), [C06](../CAPABILITIES.md#c06), [C20](../CAPABILITIES.md#c20).

**Function traceability:**

- [F02.02](../CAPABILITIES.md#f02-02): Compose, invert and control subprograms. Required for every instance of this task family.
- [F03.04](../CAPABILITIES.md#f03-04): Track workspace and classical state. Required for every instance of this task family.
- [F06.02](../CAPABILITIES.md#f06-02): Synthesize and decompose operations. Required for every instance of this task family.
- [F20.02](../CAPABILITIES.md#f20-02): Normalize conventions across boundaries. Required for every instance of this task family.

**Acceptance profiles:** [A02](../ACCEPTANCE.md#a02), [A03](../ACCEPTANCE.md#a03).

**Task-specific acceptance:** For exhaustive bounded basis inputs and superposition checks, the action, phase and control behavior match the specification and clean ancillas are restored within the declared tolerance.

**Measurements:** construction/synthesis time; gate count; workspace qubits.

**Required negative case:** Dirty ancillas, control-dependent phase errors and out-of-domain inputs are not hidden by checking only output probabilities.

**Instance readiness:** Use the [instance specification template](../TASK_SPEC_TEMPLATE.md); bind fixtures, independent references, numerical/statistical thresholds, budgets, and attribution rules before execution.

<a id="t008"></a>

## T008 - Prepare a declared input state or data encoding

**User need:** A user needs state preparation whose normalization, approximation and cost are explicit.

**Target users:** [P02](../REQUIREMENTS_MAP.md#p02), [P05](../REQUIREMENTS_MAP.md#p05).

**Applicability tags:** gate. Instance selection and conditional edges must be frozen before participant evaluation.

**Workflow stages:** formulate, express, verify.

**Required input and constraints:** Basis, sparse and dense amplitude inputs plus an encoding convention, resource limit and approximation budget.

**Required output:** A prepared state or executable preparation routine with its cost and error disclosure.

**Required capabilities:** [C02](../CAPABILITIES.md#c02), [C04](../CAPABILITIES.md#c04), [C06](../CAPABILITIES.md#c06), [C20](../CAPABILITIES.md#c20).

**Function traceability:**

- [F02.04](../CAPABILITIES.md#f02-04): Prepare states and encode inputs. Required for every instance of this task family.
- [F04.01](../CAPABILITIES.md#f04-01): Represent states and linear operators. Required for every instance of this task family.
- [F06.02](../CAPABILITIES.md#f06-02): Synthesize and decompose operations. Required for every instance of this task family.
- [F20.02](../CAPABILITIES.md#f20-02): Normalize conventions across boundaries. Required for every instance of this task family.

**Acceptance profiles:** [A02](../ACCEPTANCE.md#a02), [A03](../ACCEPTANCE.md#a03).

**Task-specific acceptance:** Small cases agree with independent amplitudes up to a single permitted global phase; normalization and approximation bounds are met and preparation cost is included.

**Measurements:** state error; preparation time; compiled resources; memory.

**Required negative case:** Zero-norm, nonfinite or dimensionally inconsistent input is rejected without silent normalization that changes the task.

**Instance readiness:** Use the [instance specification template](../TASK_SPEC_TEMPLATE.md); bind fixtures, independent references, numerical/statistical thresholds, budgets, and attribution rules before execution.

<a id="t009"></a>

## T009 - Express a measurement-dependent algorithm

**User need:** A researcher needs feed-forward, reset and bounded iterative behavior rather than static terminal measurement only.

**Target users:** [P02](../REQUIREMENTS_MAP.md#p02), [P09](../REQUIREMENTS_MAP.md#p09).

**Applicability tags:** adaptive. Instance selection and conditional edges must be frozen before participant evaluation.

**Workflow stages:** express, verify, execute.

**Required input and constraints:** Teleportation, repeat-until-success or phase-estimation fixtures with branch tables, register mapping and termination budget.

**Required output:** Execution traces and joint classical/quantum outcome statistics.

**Required capabilities:** [C03](../CAPABILITIES.md#c03), [C05](../CAPABILITIES.md#c05).

**Function traceability:**

- [F03.01](../CAPABILITIES.md#f03-01): Measure and reset during execution. Required for every instance of this task family.
- [F03.02](../CAPABILITIES.md#f03-02): Condition on recorded outcomes. Required for every instance of this task family.
- [F03.03](../CAPABILITIES.md#f03-03): Execute bounded loops and adaptive routines. Required for every instance of this task family.
- [F03.05](../CAPABILITIES.md#f03-05): Assess execution-profile compatibility. Required for every instance of this task family.
- [F05.04](../CAPABILITIES.md#f05-04): Execute adaptive and nonunitary semantics. Required for every instance of this task family.

**Acceptance profiles:** [A02](../ACCEPTANCE.md#a02), [A04](../ACCEPTANCE.md#a04).

**Task-specific acceptance:** Reachable branches match an independently enumerated small model; reset and termination semantics hold; unsupported target profiles are identified before submission.

**Measurements:** branch correctness; distribution error; termination rate; execution cost.

**Required negative case:** Reordered classical bits, an unbounded loop and an unsupported conditional operation cannot silently become a static circuit.

**Instance readiness:** Use the [instance specification template](../TASK_SPEC_TEMPLATE.md); bind fixtures, independent references, numerical/statistical thresholds, budgets, and attribution rules before execution.

<a id="t010"></a>

## T010 - Express a mixed-dimensional quantum experiment

**User need:** A researcher studying higher-dimensional systems needs dimensions preserved throughout execution.

**Target users:** [P02](../REQUIREMENTS_MAP.md#p02), [P07](../REQUIREMENTS_MAP.md#p07).

**Applicability tags:** qudit. Instance selection and conditional edges must be frozen before participant evaluation.

**Workflow stages:** express, verify, execute.

**Required input and constraints:** A mixed qubit/qutrit register, level-selective gates and an explicit basis-index mapping.

**Required output:** An inspectable program and amplitudes or probabilities in the declared product basis.

**Required capabilities:** [C02](../CAPABILITIES.md#c02), [C04](../CAPABILITIES.md#c04), [C05](../CAPABILITIES.md#c05), [C20](../CAPABILITIES.md#c20).

**Function traceability:**

- [F02.05](../CAPABILITIES.md#f02-05): Represent mixed-dimensional systems. Required for every instance of this task family.
- [F04.01](../CAPABILITIES.md#f04-01): Represent states and linear operators. Required for every instance of this task family.
- [F05.01](../CAPABILITIES.md#f05-01): Evolve a state from an explicit input. Required for every instance of this task family.
- [F20.02](../CAPABILITIES.md#f20-02): Normalize conventions across boundaries. Required for every instance of this task family.

**Acceptance profiles:** [A02](../ACCEPTANCE.md#a02), [A03](../ACCEPTANCE.md#a03).

**Task-specific acceptance:** Dimensions, operation arity and indexing match a direct small-matrix oracle and normalization is preserved.

**Measurements:** dimension coverage; execution time; state error.

**Required negative case:** An operation addressing a nonexistent level or a qubit-only backend is rejected rather than padded or relabeled silently.

**Instance readiness:** Use the [instance specification template](../TASK_SPEC_TEMPLATE.md); bind fixtures, independent references, numerical/statistical thresholds, budgets, and attribution rules before execution.

<a id="t092"></a>

## T092 - Execute a measurement-based computation pattern

**User need:** A researcher needs graph-state preparation, dependent measurement angles and byproduct corrections to implement a specified computation.

**Target users:** [P02](../REQUIREMENTS_MAP.md#p02), [P10](../REQUIREMENTS_MAP.md#p10).

**Applicability tags:** mbqc, adaptive. Instance selection and conditional edges must be frozen before participant evaluation.

**Workflow stages:** express, verify, compile, execute.

**Required input and constraints:** A bounded graph/measurement pattern, input/output vertices, measurement planes and angles, causal dependencies and correction/frame rules.

**Required output:** An executable pattern or semantics-preserving lowering, measurement histories and corrected logical outputs with resource accounting.

**Required capabilities:** [C02](../CAPABILITIES.md#c02), [C03](../CAPABILITIES.md#c03), [C06](../CAPABILITIES.md#c06), [C20](../CAPABILITIES.md#c20).

**Function traceability:**

- [F02.01](../CAPABILITIES.md#f02-01): Construct and inspect programs. Required for every instance of this task family.
- [F02.04](../CAPABILITIES.md#f02-04): Prepare states and encode inputs. Required for every instance of this task family.
- [F03.01](../CAPABILITIES.md#f03-01): Measure and reset during execution. Required for every instance of this task family.
- [F03.02](../CAPABILITIES.md#f03-02): Condition on recorded outcomes. Required for every instance of this task family.
- [F03.03](../CAPABILITIES.md#f03-03): Execute bounded loops and adaptive routines. Required for every instance of this task family.
- [F06.03](../CAPABILITIES.md#f06-03): Optimize while preserving semantics. Required for every instance of this task family.
- [F20.02](../CAPABILITIES.md#f20-02): Normalize conventions across boundaries. Required for every instance of this task family.

**Acceptance profiles:** [A02](../ACCEPTANCE.md#a02), [A03](../ACCEPTANCE.md#a03), [A04](../ACCEPTANCE.md#a04).

**Task-specific acceptance:** All bounded reachable branches obey causality and produce the specified corrected logical map against an independent oracle; any postselection probability and lowering overhead are reported.

**Measurements:** corrected-output error; pattern construction/compile time; resource count; measurement/feedback cost.

**Required negative case:** Ignoring byproduct corrections, measuring before a dependency is available or silently postselecting successful branches must fail.

**Instance readiness:** Use the [instance specification template](../TASK_SPEC_TEMPLATE.md); bind fixtures, independent references, numerical/statistical thresholds, budgets, and attribution rules before execution.
