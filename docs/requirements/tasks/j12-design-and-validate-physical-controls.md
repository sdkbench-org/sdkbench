<!-- Generated from catalog.json by tools/requirements_docs.py. Do not edit directly. -->

# J12 - Design and validate physical controls

[All tasks](../TASK_CATALOG.md) | [Acceptance rules](../ACCEPTANCE.md) | [Traceability](../TRACEABILITY.md)

Status: requirements only. No task in this file is claimed as implemented or executed.

Workflow grounding: [S01](../SOURCES.md#s01), [S09](../SOURCES.md#s09). Sources inform context; they do not establish universal requirements or user-study validation.

<a id="t056"></a>

## T056 - Express physical controls with explicit units and channels

**User need:** A control researcher needs an unambiguous representation of a physical experiment.

**Target users:** [P11](../REQUIREMENTS_MAP.md#p11).

**Applicability tags:** pulse. Instance selection and conditional edges must be frozen before participant evaluation.

**Workflow stages:** express, verify.

**Required input and constraints:** Waveforms, ports/frames, calibration references, sample rate, amplitude limits and channel assignments.

**Required output:** A validated control program and exported waveform/metadata artifact.

**Required capabilities:** [C15](../CAPABILITIES.md#c15), [C20](../CAPABILITIES.md#c20).

**Function traceability:**

- [F15.01](../CAPABILITIES.md#f15-01): Represent waveforms and channels. Required for every instance of this task family.
- [F15.05](../CAPABILITIES.md#f15-05): Preserve gate-to-control correspondence. Required for every instance of this task family.
- [F20.01](../CAPABILITIES.md#f20-01): Import and export declared formats. Required for every instance of this task family.

**Acceptance profiles:** [A02](../ACCEPTANCE.md#a02), [A10](../ACCEPTANCE.md#a10).

**Task-specific acceptance:** Units, frame changes, samples and channel associations survive inspection/export; constraints are independently checked.

**Measurements:** representation fidelity; construction/export time; payload size.

**Required negative case:** A frequency-unit mismatch, out-of-range sample or missing frame reference is rejected.

**Instance readiness:** Use the [instance specification template](../TASK_SPEC_TEMPLATE.md); bind fixtures, independent references, numerical/statistical thresholds, budgets, and attribution rules before execution.

<a id="t057"></a>

## T057 - Schedule simultaneous and feedback-dependent control

**User need:** An experimenter needs valid concurrent pulses and classical feedback timing.

**Target users:** [P11](../REQUIREMENTS_MAP.md#p11), [P06](../REQUIREMENTS_MAP.md#p06).

**Applicability tags:** pulse, adaptive. Instance selection and conditional edges must be frozen before participant evaluation.

**Workflow stages:** compile, verify.

**Required input and constraints:** A control program with channel conflicts, alignment, feedback latency and device timing constraints.

**Required output:** An executable schedule with conflict and dependency evidence.

**Required capabilities:** [C03](../CAPABILITIES.md#c03), [C06](../CAPABILITIES.md#c06), [C15](../CAPABILITIES.md#c15).

**Function traceability:**

- [F15.02](../CAPABILITIES.md#f15-02): Schedule physical controls. Required when the frozen instance includes the pulse applicability tag.
- [F06.05](../CAPABILITIES.md#f06-05): Schedule and account for resources. Required for every instance of this task family.
- [F03.02](../CAPABILITIES.md#f03-02): Condition on recorded outcomes. Required for every instance of this task family.
- [F06.01](../CAPABILITIES.md#f06-01): Describe an executable target. Required for every instance of this task family.

**Acceptance profiles:** [A05](../ACCEPTANCE.md#a05), [A10](../ACCEPTANCE.md#a10).

**Task-specific acceptance:** All constraints pass an independent schedule validator; effective rounded timings and any changed experiment are explicit.

**Measurements:** makespan; timing deviation; violations; compile time.

**Required negative case:** A feedback pulse cannot be scheduled before its measurement result exists.

**Instance readiness:** Use the [instance specification template](../TASK_SPEC_TEMPLATE.md); bind fixtures, independent references, numerical/statistical thresholds, budgets, and attribution rules before execution.

<a id="t058"></a>

## T058 - Predict a calibrated driven-system response

**User need:** A researcher needs response predictions in the intended physical frame.

**Target users:** [P11](../REQUIREMENTS_MAP.md#p11), [P08](../REQUIREMENTS_MAP.md#p08).

**Applicability tags:** pulse. Instance selection and conditional edges must be frozen before participant evaluation.

**Workflow stages:** formulate, execute, estimate.

**Required input and constraints:** A driven Hamiltonian, dissipators, control samples, rotating-frame convention and output times.

**Required output:** States or observable traces with solver tolerances and frame metadata.

**Required capabilities:** [C04](../CAPABILITIES.md#c04), [C10](../CAPABILITIES.md#c10), [C12](../CAPABILITIES.md#c12), [C15](../CAPABILITIES.md#c15).

**Function traceability:**

- [F15.03](../CAPABILITIES.md#f15-03): Simulate driven dynamics. Required for every instance of this task family.
- [F10.03](../CAPABILITIES.md#f10-03): Model time-dependent open systems. Required for every instance of this task family.
- [F04.01](../CAPABILITIES.md#f04-01): Represent states and linear operators. Required for every instance of this task family.
- [F12.05](../CAPABILITIES.md#f12-05): Export interpretable analysis. Required for every instance of this task family.

**Acceptance profiles:** [A03](../ACCEPTANCE.md#a03), [A06](../ACCEPTANCE.md#a06), [A10](../ACCEPTANCE.md#a10).

**Task-specific acceptance:** Analytic and independent small-system fixtures meet the observable/state budget; time-step refinement and frame conversion are checked.

**Measurements:** response error; time to tolerance; memory.

**Required negative case:** Dropping counter-rotating terms or changing frames requires an explicit approximation rather than a silent optimization.

**Instance readiness:** Use the [instance specification template](../TASK_SPEC_TEMPLATE.md); bind fixtures, independent references, numerical/statistical thresholds, budgets, and attribution rules before execution.

<a id="t059"></a>

## T059 - Optimize a pulse under physical and evaluation constraints

**User need:** A researcher needs a control solution that meets a physical objective without violating device limits.

**Target users:** [P11](../REQUIREMENTS_MAP.md#p11).

**Applicability tags:** pulse. Instance selection and conditional edges must be frozen before participant evaluation.

**Workflow stages:** optimize, verify.

**Required input and constraints:** A target operation/response, model or authorized device path, pulse constraints, initialization and evaluation budget.

**Required output:** A constrained control solution, objective trace and held-out validation.

**Required capabilities:** [C09](../CAPABILITIES.md#c09), [C15](../CAPABILITIES.md#c15).

**Function traceability:**

- [F15.04](../CAPABILITIES.md#f15-04): Calibrate or optimize controls. Required for every instance of this task family.
- [F15.01](../CAPABILITIES.md#f15-01): Represent waveforms and channels. Required for every instance of this task family.
- [F15.03](../CAPABILITIES.md#f15-03): Simulate driven dynamics. Required for every instance of this task family.
- [F09.05](../CAPABILITIES.md#f09-05): Budget training and adaptive search. Required for every instance of this task family.

**Acceptance profiles:** [A07](../ACCEPTANCE.md#a07), [A09](../ACCEPTANCE.md#a09), [A10](../ACCEPTANCE.md#a10).

**Task-specific acceptance:** The final control satisfies all physical constraints and the frozen quality target; all evaluations are counted and modeled versus measured evidence is distinct.

**Measurements:** time/evaluations to target; constraint violations; robustness over held-out parameters.

**Required negative case:** A high modeled fidelity outside allowed amplitudes or bandwidth is not a valid solution.

**Instance readiness:** Use the [instance specification template](../TASK_SPEC_TEMPLATE.md); bind fixtures, independent references, numerical/statistical thresholds, budgets, and attribution rules before execution.

<a id="t060"></a>

## T060 - Use the correct calibration for a gate-level experiment

**User need:** An experimenter needs calibrated controls associated with the correct gate, device and acquisition context.

**Target users:** [P11](../REQUIREMENTS_MAP.md#p11), [P09](../REQUIREMENTS_MAP.md#p09).

**Applicability tags:** pulse, gate. Instance selection and conditional edges must be frozen before participant evaluation.

**Workflow stages:** compile, execute, operate.

**Required input and constraints:** Versioned gate/control definitions, parameter domains, target IDs and stale or incompatible calibration fixtures.

**Required output:** A resolved gate-to-control binding and complete calibration provenance.

**Required capabilities:** [C06](../CAPABILITIES.md#c06), [C11](../CAPABILITIES.md#c11), [C15](../CAPABILITIES.md#c15), [C20](../CAPABILITIES.md#c20).

**Function traceability:**

- [F15.05](../CAPABILITIES.md#f15-05): Preserve gate-to-control correspondence. Required when the frozen instance includes the pulse applicability tag.
- [F06.01](../CAPABILITIES.md#f06-01): Describe an executable target. Required for every instance of this task family.
- [F11.05](../CAPABILITIES.md#f11-05): Preserve acquisition and result provenance. Required for every instance of this task family.
- [F20.04](../CAPABILITIES.md#f20-04): Package reproducible evidence. Required for every instance of this task family.

**Acceptance profiles:** [A05](../ACCEPTANCE.md#a05), [A08](../ACCEPTANCE.md#a08), [A10](../ACCEPTANCE.md#a10).

**Task-specific acceptance:** Compatible bindings preserve declared gate behavior on the small model; stale or mismatched definitions are rejected or explicitly flagged under a frozen policy.

**Measurements:** binding correctness; metadata completeness; validation overhead.

**Required negative case:** A calibration from a different device or clock cannot be treated as current without disclosure.

**Instance readiness:** Use the [instance specification template](../TASK_SPEC_TEMPLATE.md); bind fixtures, independent references, numerical/statistical thresholds, budgets, and attribution rules before execution.
