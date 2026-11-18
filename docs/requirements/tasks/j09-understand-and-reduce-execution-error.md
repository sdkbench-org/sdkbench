<!-- Generated from catalog.json by tools/requirements_docs.py. Do not edit directly. -->

# J09 - Understand and reduce execution error

[All tasks](../TASK_CATALOG.md) | [Acceptance rules](../ACCEPTANCE.md) | [Traceability](../TRACEABILITY.md)

Status: requirements only. No task in this file is claimed as implemented or executed.

Workflow grounding: [S09](../SOURCES.md#s09), [S11](../SOURCES.md#s11). Sources inform context; they do not establish universal requirements or user-study validation.

<a id="t041"></a>

## T041 - Predict outputs of a declared noisy experiment

**User need:** A noise researcher needs consistent channel placement and sampled or exact outputs.

**Target users:** [P08](../REQUIREMENTS_MAP.md#p08), [P07](../REQUIREMENTS_MAP.md#p07).

**Applicability tags:** gate. Instance selection and conditional edges must be frozen before participant evaluation.

**Workflow stages:** formulate, execute, estimate.

**Required input and constraints:** Frozen channel locations/order, noise parameters, input program, measurement and trajectory/shot policy.

**Required output:** Mixed-state observables or distributions with solver/sampling metadata.

**Required capabilities:** [C05](../CAPABILITIES.md#c05), [C10](../CAPABILITIES.md#c10), [C12](../CAPABILITIES.md#c12).

**Function traceability:**

- [F10.01](../CAPABILITIES.md#f10-01): Specify channels and readout models. Required for every instance of this task family.
- [F10.02](../CAPABILITIES.md#f10-02): Execute noisy density or trajectory evolution. Required for every instance of this task family.
- [F12.02](../CAPABILITIES.md#f12-02): Estimate quantities with uncertainty. Required for every instance of this task family.
- [F05.03](../CAPABILITIES.md#f05-03): Compute exact observables and reduced states. Required for every instance of this task family.

**Acceptance profiles:** [A03](../ACCEPTANCE.md#a03), [A04](../ACCEPTANCE.md#a04).

**Task-specific acceptance:** Small density-matrix references and trajectory equivalence tests pass; finite-sampling uncertainty and exact-versus-sampled cohorts are distinct.

**Measurements:** observable/distribution error; time at accuracy; memory; trajectories.

**Required negative case:** Moving noise before rather than after a noncommuting gate is a changed experiment and must fail.

**Instance readiness:** Use the [instance specification template](../TASK_SPEC_TEMPLATE.md); bind fixtures, independent references, numerical/statistical thresholds, budgets, and attribution rules before execution.

<a id="t042"></a>

## T042 - Integrate a time-dependent open quantum system

**User need:** A researcher needs driven/dissipative dynamics with interpretable physical units and solver error.

**Target users:** [P08](../REQUIREMENTS_MAP.md#p08), [P04](../REQUIREMENTS_MAP.md#p04).

**Applicability tags:** gate, analog, pulse. Instance selection and conditional edges must be frozen before participant evaluation.

**Workflow stages:** formulate, execute, estimate.

**Required input and constraints:** Hamiltonian/dissipators, units, frame, initial density matrix, output times and tolerances.

**Required output:** State or observable trajectories with integration diagnostics.

**Required capabilities:** [C04](../CAPABILITIES.md#c04), [C10](../CAPABILITIES.md#c10), [C13](../CAPABILITIES.md#c13), [C15](../CAPABILITIES.md#c15).

**Function traceability:**

- [F10.03](../CAPABILITIES.md#f10-03): Model time-dependent open systems. Required for every instance of this task family.
- [F04.01](../CAPABILITIES.md#f04-01): Represent states and linear operators. Required for every instance of this task family.
- [F15.03](../CAPABILITIES.md#f15-03): Simulate driven dynamics. Required when the frozen instance includes the pulse applicability tag.
- [F13.02](../CAPABILITIES.md#f13-02): Study dynamics and correlations. Required for every instance of this task family.

**Acceptance profiles:** [A03](../ACCEPTANCE.md#a03), [A06](../ACCEPTANCE.md#a06), [A10](../ACCEPTANCE.md#a10).

**Task-specific acceptance:** Analytically solvable and independent small-solver fixtures satisfy error budgets; trace/physicality checks and refinement tests expose integration failure.

**Measurements:** time to tolerance; state/observable error; step count; memory.

**Required negative case:** A frame, rate-unit or collapse-operator normalization mismatch cannot be hidden by rescaling the final curve.

**Instance readiness:** Use the [instance specification template](../TASK_SPEC_TEMPLATE.md); bind fixtures, independent references, numerical/statistical thresholds, budgets, and attribution rules before execution.

<a id="t043"></a>

## T043 - Correct measurement bias with accounted calibration uncertainty

**User need:** An experimenter needs to know whether readout correction improves the requested estimate.

**Target users:** [P08](../REQUIREMENTS_MAP.md#p08), [P09](../REQUIREMENTS_MAP.md#p09).

**Applicability tags:** gate. Instance selection and conditional edges must be frozen before participant evaluation.

**Workflow stages:** execute, estimate.

**Required input and constraints:** Calibration and evaluation datasets kept separate, an estimator, target observable and total shot budget.

**Required output:** Raw and mitigated estimates, uncertainty, conditioning diagnostics and calibration cost.

**Required capabilities:** [C10](../CAPABILITIES.md#c10), [C12](../CAPABILITIES.md#c12).

**Function traceability:**

- [F10.04](../CAPABILITIES.md#f10-04): Apply and assess error mitigation. Required for every instance of this task family.
- [F10.01](../CAPABILITIES.md#f10-01): Specify channels and readout models. Required for every instance of this task family.
- [F12.01](../CAPABILITIES.md#f12-01): Validate and normalize result records. Required for every instance of this task family.
- [F12.02](../CAPABILITIES.md#f12-02): Estimate quantities with uncertainty. Required for every instance of this task family.

**Acceptance profiles:** [A04](../ACCEPTANCE.md#a04).

**Task-specific acceptance:** Known-channel fixtures satisfy the declared bias/coverage target; calibration uncertainty and any negative quasi-probabilities are handled explicitly.

**Measurements:** error reduction; variance; total calibration/evaluation shots; failure rate.

**Required negative case:** Clipping negative weights and silently renormalizing them cannot be claimed as an unbiased correction.

**Instance readiness:** Use the [instance specification template](../TASK_SPEC_TEMPLATE.md); bind fixtures, independent references, numerical/statistical thresholds, budgets, and attribution rules before execution.

<a id="t044"></a>

## T044 - Assess extrapolation or cancellation at matched total cost

**User need:** A user needs evidence of practical mitigation benefit after its statistical overhead.

**Target users:** [P08](../REQUIREMENTS_MAP.md#p08), [P09](../REQUIREMENTS_MAP.md#p09).

**Applicability tags:** gate. Instance selection and conditional edges must be frozen before participant evaluation.

**Workflow stages:** express, execute, estimate.

**Required input and constraints:** A declared mitigation method, scaling/quasi-probability assumptions, raw baseline, held-out fixtures and total budget.

**Required output:** Raw/mitigated errors, intervals, failure cases and all additional programs/shots.

**Required capabilities:** [C10](../CAPABILITIES.md#c10), [C11](../CAPABILITIES.md#c11), [C12](../CAPABILITIES.md#c12).

**Function traceability:**

- [F10.04](../CAPABILITIES.md#f10-04): Apply and assess error mitigation. Required for every instance of this task family.
- [F12.02](../CAPABILITIES.md#f12-02): Estimate quantities with uncertainty. Required for every instance of this task family.
- [F12.03](../CAPABILITIES.md#f12-03): Plan and combine measurements. Required for every instance of this task family.
- [F11.02](../CAPABILITIES.md#f11-02): Prepare a budgeted experiment. Required for every instance of this task family.

**Acceptance profiles:** [A04](../ACCEPTANCE.md#a04), [A09](../ACCEPTANCE.md#a09).

**Task-specific acceptance:** At matched total cost the predeclared quality criterion is evaluated with appropriate uncertainty; scaling and cancellation assumptions are independently checked.

**Measurements:** error versus cost; variance amplification; extra circuits; coverage.

**Required negative case:** A zero-noise reference used in fitting cannot also be presented as unseen validation evidence.

**Instance readiness:** Use the [instance specification template](../TASK_SPEC_TEMPLATE.md); bind fixtures, independent references, numerical/statistical thresholds, budgets, and attribution rules before execution.

<a id="t045"></a>

## T045 - Validate a frozen device or noise model on unseen experiments

**User need:** A user needs to know where a predictive model generalizes beyond calibration data.

**Target users:** [P08](../REQUIREMENTS_MAP.md#p08), [P09](../REQUIREMENTS_MAP.md#p09).

**Applicability tags:** gate, analog, pulse. Instance selection and conditional edges must be frozen before participant evaluation.

**Workflow stages:** formulate, execute, estimate.

**Required input and constraints:** Versioned calibration/training data, a frozen model, disjoint circuits/settings and acquisition windows.

**Required output:** Predictions, held-out residuals, uncertainty and a declared validity region.

**Required capabilities:** [C10](../CAPABILITIES.md#c10), [C11](../CAPABILITIES.md#c11), [C12](../CAPABILITIES.md#c12), [C20](../CAPABILITIES.md#c20).

**Function traceability:**

- [F10.05](../CAPABILITIES.md#f10-05): Validate noise predictions out of sample. Required for every instance of this task family.
- [F11.05](../CAPABILITIES.md#f11-05): Preserve acquisition and result provenance. Required for every instance of this task family.
- [F12.02](../CAPABILITIES.md#f12-02): Estimate quantities with uncertainty. Required for every instance of this task family.
- [F20.04](../CAPABILITIES.md#f20-04): Package reproducible evidence. Required for every instance of this task family.

**Acceptance profiles:** [A04](../ACCEPTANCE.md#a04), [A09](../ACCEPTANCE.md#a09).

**Task-specific acceptance:** The frozen predictive contract is evaluated only on held-out data; calibration age, drift and unsupported regions are retained, with failures reported.

**Measurements:** held-out prediction error; coverage; validity-region completion; calibration cost.

**Required negative case:** Retrospective fitting on evaluation counts cannot be labeled prospective validation.

**Instance readiness:** Use the [instance specification template](../TASK_SPEC_TEMPLATE.md); bind fixtures, independent references, numerical/statistical thresholds, budgets, and attribution rules before execution.
