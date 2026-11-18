<!-- Generated from catalog.json by tools/requirements_docs.py. Do not edit directly. -->

# J07 - Train and differentiate a hybrid model

[All tasks](../TASK_CATALOG.md) | [Acceptance rules](../ACCEPTANCE.md) | [Traceability](../TRACEABILITY.md)

Status: requirements only. No task in this file is claimed as implemented or executed.

Workflow grounding: [S08](../SOURCES.md#s08). Sources inform context; they do not establish universal requirements or user-study validation.

<a id="t031"></a>

## T031 - Obtain trustworthy derivatives of a quantum model

**User need:** An optimizer user needs derivatives with correct shared-parameter and complex-output conventions.

**Target users:** [P05](../REQUIREMENTS_MAP.md#p05), [P02](../REQUIREMENTS_MAP.md#p02).

**Applicability tags:** gate, cv, analog, pulse. Instance selection and conditional edges must be frozen before participant evaluation.

**Workflow stages:** verify, optimize.

**Required input and constraints:** Small circuit, finite-mode and controlled-Hamiltonian fixtures with independent analytic/directional references, shared parameters, vector outputs and explicit units/complex-output conventions.

**Required output:** Gradients or derivative products with method, shape and cost provenance.

**Required capabilities:** [C02](../CAPABILITIES.md#c02), [C08](../CAPABILITIES.md#c08).

**Function traceability:**

- [F08.01](../CAPABILITIES.md#f08-01): Compute first derivatives. Required for every instance of this task family.
- [F08.02](../CAPABILITIES.md#f08-02): Compute Jacobians and derivative products. Required for every instance of this task family.
- [F08.05](../CAPABILITIES.md#f08-05): Disclose derivative method and cost. Required for every instance of this task family.
- [F02.03](../CAPABILITIES.md#f02-03): Bind and reuse parameters. Required for every instance of this task family.

**Acceptance profiles:** [A03](../ACCEPTANCE.md#a03), [A07](../ACCEPTANCE.md#a07), [A10](../ACCEPTANCE.md#a10).

**Task-specific acceptance:** Analytic cases and independent directional checks meet mixed absolute/relative tolerances, including near-zero components; parameter sharing is accumulated correctly.

**Measurements:** derivative error; forward/backward time; memory; evaluation calls.

**Required negative case:** A detached parameter, transposed Jacobian or conjugation error must fail even when optimization happens to improve the loss.

**Instance readiness:** Use the [instance specification template](../TASK_SPEC_TEMPLATE.md); bind fixtures, independent references, numerical/statistical thresholds, budgets, and attribution rules before execution.

<a id="t032"></a>

## T032 - Train a minibatched hybrid quantum/classical model

**User need:** A practitioner needs learning across a classical/quantum boundary with correct batching.

**Target users:** [P05](../REQUIREMENTS_MAP.md#p05).

**Applicability tags:** gate, cv. Instance selection and conditional edges must be frozen before participant evaluation.

**Workflow stages:** express, optimize, estimate.

**Required input and constraints:** A fixed dataset/split, model, initialization, objective and compute budget, with serial small-batch references.

**Required output:** Training traces, held-out evaluation and resource/call accounting.

**Required capabilities:** [C08](../CAPABILITIES.md#c08), [C09](../CAPABILITIES.md#c09), [C19](../CAPABILITIES.md#c19).

**Function traceability:**

- [F09.01](../CAPABILITIES.md#f09-01): Integrate quantum and classical models. Required for every instance of this task family.
- [F09.02](../CAPABILITIES.md#f09-02): Batch independent data and parameters. Required for every instance of this task family.
- [F09.03](../CAPABILITIES.md#f09-03): Optimize and evaluate reproducibly. Required for every instance of this task family.
- [F08.01](../CAPABILITIES.md#f08-01): Compute first derivatives. Required for every instance of this task family.
- [F19.03](../CAPABILITIES.md#f19-03): Parallelize independent work. Required for every instance of this task family.

**Acceptance profiles:** [A07](../ACCEPTANCE.md#a07), [A09](../ACCEPTANCE.md#a09).

**Task-specific acceptance:** Gradients cross every declared trainable boundary; batch outputs match serial references; the frozen convergence or quality target is met under the total budget.

**Measurements:** time to target; examples per second; memory; held-out quality.

**Required negative case:** Averaging all examples before the quantum layer or training on held-out data is rejected.

**Instance readiness:** Use the [instance specification template](../TASK_SPEC_TEMPLATE.md); bind fixtures, independent references, numerical/statistical thresholds, budgets, and attribution rules before execution.

<a id="t033"></a>

## T033 - Converge a variational objective under a fixed budget

**User need:** A researcher needs successful convergence, not merely fast optimizer iterations.

**Target users:** [P05](../REQUIREMENTS_MAP.md#p05), [P02](../REQUIREMENTS_MAP.md#p02).

**Applicability tags:** gate. Instance selection and conditional edges must be frozen before participant evaluation.

**Workflow stages:** optimize, estimate.

**Required input and constraints:** A declared cost operator, ansatz, parameter domain, initializations and target objective interval.

**Required output:** Independent-seed optimization outcomes and complete objective/gradient call traces.

**Required capabilities:** [C08](../CAPABILITIES.md#c08), [C09](../CAPABILITIES.md#c09), [C13](../CAPABILITIES.md#c13).

**Function traceability:**

- [F09.03](../CAPABILITIES.md#f09-03): Optimize and evaluate reproducibly. Required for every instance of this task family.
- [F09.05](../CAPABILITIES.md#f09-05): Budget training and adaptive search. Required for every instance of this task family.
- [F08.05](../CAPABILITIES.md#f08-05): Disclose derivative method and cost. Required for every instance of this task family.
- [F13.01](../CAPABILITIES.md#f13-01): Solve energy or spectral problems. Required for every instance of this task family.

**Acceptance profiles:** [A07](../ACCEPTANCE.md#a07), [A09](../ACCEPTANCE.md#a09).

**Task-specific acceptance:** Successful runs meet the frozen objective target within budget; seed failures and tuning cost remain in the success-rate and cost report.

**Measurements:** success probability; time/evaluations to target; final objective gap.

**Required negative case:** Changing optimizer stopping rules or retaining only the best initialization cannot change the primary cohort after results are seen.

**Instance readiness:** Use the [instance specification template](../TASK_SPEC_TEMPLATE.md); bind fixtures, independent references, numerical/statistical thresholds, budgets, and attribution rules before execution.

<a id="t034"></a>

## T034 - Use curvature or derivative products in a learning routine

**User need:** A researcher needs curvature-aware optimization or sensitivity analysis with a valid derivative graph.

**Target users:** [P05](../REQUIREMENTS_MAP.md#p05), [P02](../REQUIREMENTS_MAP.md#p02).

**Applicability tags:** gate, cv, analog, pulse. Instance selection and conditional edges must be frozen before participant evaluation.

**Workflow stages:** verify, optimize.

**Required input and constraints:** Small objectives with reference Hessians/JVPs/VJPs and a fixed outer optimization or sensitivity computation.

**Required output:** Derivative products and a correct enclosing workflow result.

**Required capabilities:** [C08](../CAPABILITIES.md#c08), [C09](../CAPABILITIES.md#c09).

**Function traceability:**

- [F08.02](../CAPABILITIES.md#f08-02): Compute Jacobians and derivative products. Required for every instance of this task family.
- [F08.03](../CAPABILITIES.md#f08-03): Compute higher-order derivatives. Required for every instance of this task family.
- [F08.05](../CAPABILITIES.md#f08-05): Disclose derivative method and cost. Required for every instance of this task family.
- [F09.01](../CAPABILITIES.md#f09-01): Integrate quantum and classical models. Required for every instance of this task family.

**Acceptance profiles:** [A03](../ACCEPTANCE.md#a03), [A07](../ACCEPTANCE.md#a07), [A10](../ACCEPTANCE.md#a10).

**Task-specific acceptance:** Independent small references and directional identities pass; unsupported derivative orders or backends are explicit instead of returning detached or zero values.

**Measurements:** product error; runtime; memory; outer convergence.

**Required negative case:** A first-derivative-only implementation cannot be presented as higher-order support through an unreported finite-difference wrapper.

**Instance readiness:** Use the [instance specification template](../TASK_SPEC_TEMPLATE.md); bind fixtures, independent references, numerical/statistical thresholds, budgets, and attribution rules before execution.

<a id="t035"></a>

## T035 - Optimize a noisy sampled model with a shot budget

**User need:** A user needs learning whose statistical cost is accounted for.

**Target users:** [P05](../REQUIREMENTS_MAP.md#p05), [P08](../REQUIREMENTS_MAP.md#p08).

**Applicability tags:** gate, adaptive, cv, analog. Instance selection and conditional edges must be frozen before participant evaluation.

**Workflow stages:** optimize, estimate.

**Required input and constraints:** A fixed sampled objective, noise/execution model, independent seeds, shot budget and target success criterion.

**Required output:** Training outcomes with derivative variance, total shots and all shifted evaluations.

**Required capabilities:** [C08](../CAPABILITIES.md#c08), [C09](../CAPABILITIES.md#c09), [C12](../CAPABILITIES.md#c12).

**Function traceability:**

- [F08.04](../CAPABILITIES.md#f08-04): Estimate derivatives with finite shots. Required for every instance of this task family.
- [F08.05](../CAPABILITIES.md#f08-05): Disclose derivative method and cost. Required for every instance of this task family.
- [F09.05](../CAPABILITIES.md#f09-05): Budget training and adaptive search. Required for every instance of this task family.
- [F12.02](../CAPABILITIES.md#f12-02): Estimate quantities with uncertainty. Required for every instance of this task family.
- [F12.03](../CAPABILITIES.md#f12-03): Plan and combine measurements. Required for every instance of this task family.

**Acceptance profiles:** [A04](../ACCEPTANCE.md#a04), [A07](../ACCEPTANCE.md#a07), [A09](../ACCEPTANCE.md#a09).

**Task-specific acceptance:** Declared estimator bias/variance and task success satisfy the frozen statistical contract; no analytic expectation is substituted for sampled calls.

**Measurements:** success probability; total shots; time to target; estimator variance.

**Required negative case:** Adaptive shot allocation and discarded trajectories must be charged and reproducible.

**Instance readiness:** Use the [instance specification template](../TASK_SPEC_TEMPLATE.md); bind fixtures, independent references, numerical/statistical thresholds, budgets, and attribution rules before execution.
