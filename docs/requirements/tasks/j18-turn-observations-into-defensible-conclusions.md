<!-- Generated from catalog.json by tools/requirements_docs.py. Do not edit directly. -->

# J18 - Turn observations into defensible conclusions

[All tasks](../TASK_CATALOG.md) | [Acceptance rules](../ACCEPTANCE.md) | [Traceability](../TRACEABILITY.md)

Status: requirements only. No task in this file is claimed as implemented or executed.

Workflow grounding: [S09](../SOURCES.md#s09), [S11](../SOURCES.md#s11). Sources inform context; they do not establish universal requirements or user-study validation.

<a id="t086"></a>

## T086 - Estimate an observable with a specified uncertainty target

**User need:** A scientist needs an estimate whose stated uncertainty is meaningful at finite sample size.

**Target users:** [P08](../REQUIREMENTS_MAP.md#p08), [P04](../REQUIREMENTS_MAP.md#p04).

**Applicability tags:** gate, analog, cv. Instance selection and conditional edges must be frozen before participant evaluation.

**Workflow stages:** estimate, execute.

**Required input and constraints:** Typed raw observations, a fixed estimator, target error/confidence, independent seeds and a stopping policy.

**Required output:** An estimate, interval, denominator and a complete shot/call ledger.

**Required capabilities:** [C05](../CAPABILITIES.md#c05), [C12](../CAPABILITIES.md#c12).

**Function traceability:**

- [F12.01](../CAPABILITIES.md#f12-01): Validate and normalize result records. Required for every instance of this task family.
- [F12.02](../CAPABILITIES.md#f12-02): Estimate quantities with uncertainty. Required for every instance of this task family.
- [F12.05](../CAPABILITIES.md#f12-05): Export interpretable analysis. Required for every instance of this task family.
- [F05.02](../CAPABILITIES.md#f05-02): Sample declared measurements. Required for every instance of this task family.

**Acceptance profiles:** [A04](../ACCEPTANCE.md#a04).

**Task-specific acceptance:** Known-distribution coverage and equivalence/power fixtures pass; zero counts and rare events receive valid uncertainty handling and sequential stopping follows the frozen protocol.

**Measurements:** shots/time to target; coverage; bias; inconclusive rate.

**Required negative case:** A narrow plug-in interval at zero observed failures or an uncorrected repeated significance test must not pass.

**Instance readiness:** Use the [instance specification template](../TASK_SPEC_TEMPLATE.md); bind fixtures, independent references, numerical/statistical thresholds, budgets, and attribution rules before execution.

<a id="t087"></a>

## T087 - Plan measurements for an energy or correlation target

**User need:** A user needs an accurate many-term estimate at limited measurement cost.

**Target users:** [P03](../REQUIREMENTS_MAP.md#p03), [P08](../REQUIREMENTS_MAP.md#p08).

**Applicability tags:** gate. Instance selection and conditional edges must be frozen before participant evaluation.

**Workflow stages:** express, execute, estimate.

**Required input and constraints:** An observable collection, allowed compatible-measurement groups, allocation policy and total shot budget.

**Required output:** Measurement programs, grouped outcomes, final estimates and covariance/cost accounting.

**Required capabilities:** [C04](../CAPABILITIES.md#c04), [C11](../CAPABILITIES.md#c11), [C12](../CAPABILITIES.md#c12).

**Function traceability:**

- [F12.03](../CAPABILITIES.md#f12-03): Plan and combine measurements. Required for every instance of this task family.
- [F04.02](../CAPABILITIES.md#f04-02): Manipulate structured observables. Required for every instance of this task family.
- [F12.02](../CAPABILITIES.md#f12-02): Estimate quantities with uncertainty. Required for every instance of this task family.
- [F11.02](../CAPABILITIES.md#f11-02): Prepare a budgeted experiment. Required for every instance of this task family.

**Acceptance profiles:** [A04](../ACCEPTANCE.md#a04), [A09](../ACCEPTANCE.md#a09).

**Task-specific acceptance:** The requested observable is unchanged; grouped-estimator bias/uncertainty satisfies the frozen contract and all pilot, calibration and evaluation shots are charged.

**Measurements:** error at fixed shots; state preparations; total time; variance.

**Required negative case:** Assuming grouped observables are statistically independent without justification can invalidate the uncertainty claim.

**Instance readiness:** Use the [instance specification template](../TASK_SPEC_TEMPLATE.md); bind fixtures, independent references, numerical/statistical thresholds, budgets, and attribution rules before execution.

<a id="t088"></a>

## T088 - Reconstruct a state or process with validation beyond the fitted data

**User need:** A researcher needs a reconstruction whose apparent fit is not confused with predictive validity.

**Target users:** [P08](../REQUIREMENTS_MAP.md#p08), [P09](../REQUIREMENTS_MAP.md#p09).

**Applicability tags:** gate, cv. Instance selection and conditional edges must be frozen before participant evaluation.

**Workflow stages:** estimate, verify.

**Required input and constraints:** Informationally specified measurements, physicality/model assumptions, noise and held-out validation fixtures.

**Required output:** A reconstruction, identifiability diagnostics, uncertainty and held-out predictions.

**Required capabilities:** [C04](../CAPABILITIES.md#c04), [C12](../CAPABILITIES.md#c12).

**Function traceability:**

- [F12.04](../CAPABILITIES.md#f12-04): Reconstruct and diagnose states or processes. Required for every instance of this task family.
- [F12.02](../CAPABILITIES.md#f12-02): Estimate quantities with uncertainty. Required for every instance of this task family.
- [F04.01](../CAPABILITIES.md#f04-01): Represent states and linear operators. Required for every instance of this task family.
- [F12.05](../CAPABILITIES.md#f12-05): Export interpretable analysis. Required for every instance of this task family.

**Acceptance profiles:** [A03](../ACCEPTANCE.md#a03), [A04](../ACCEPTANCE.md#a04).

**Task-specific acceptance:** Analytic/small references and held-out prediction criteria pass; underdetermined or nonidentifiable cases are explicit and physicality constraints are disclosed.

**Measurements:** reconstruction/prediction error; coverage; fit time; measurement cost.

**Required negative case:** A good in-sample fit cannot certify a unique state, process or global fidelity when the observations do not identify it.

**Instance readiness:** Use the [instance specification template](../TASK_SPEC_TEMPLATE.md); bind fixtures, independent references, numerical/statistical thresholds, budgets, and attribution rules before execution.

<a id="t089"></a>

## T089 - Estimate a predefined observable family from reusable measurement records

**User need:** A researcher needs a controlled way to reuse randomized measurements for multiple quantities.

**Target users:** [P08](../REQUIREMENTS_MAP.md#p08), [P04](../REQUIREMENTS_MAP.md#p04).

**Applicability tags:** gate. Instance selection and conditional edges must be frozen before participant evaluation.

**Workflow stages:** execute, estimate.

**Required input and constraints:** A frozen randomized measurement scheme, observable family, reconstruction rule, seed and sample budget.

**Required output:** Per-observable estimates, simultaneous uncertainty and measurement provenance.

**Required capabilities:** [C12](../CAPABILITIES.md#c12).

**Function traceability:**

- [F12.03](../CAPABILITIES.md#f12-03): Plan and combine measurements. Required for every instance of this task family.
- [F12.04](../CAPABILITIES.md#f12-04): Reconstruct and diagnose states or processes. Required for every instance of this task family.
- [F12.02](../CAPABILITIES.md#f12-02): Estimate quantities with uncertainty. Required for every instance of this task family.
- [F12.01](../CAPABILITIES.md#f12-01): Validate and normalize result records. Required for every instance of this task family.

**Acceptance profiles:** [A04](../ACCEPTANCE.md#a04), [A09](../ACCEPTANCE.md#a09).

**Task-specific acceptance:** Known small cases and repeated-seed coverage tests meet the family-wise error contract; observable selection and all measurement overhead are disclosed.

**Measurements:** family error; coverage; shots/time to target; memory.

**Required negative case:** Choosing only observables with favorable estimates after viewing the data cannot support the preregistered family claim.

**Instance readiness:** Use the [instance specification template](../TASK_SPEC_TEMPLATE.md); bind fixtures, independent references, numerical/statistical thresholds, budgets, and attribution rules before execution.

<a id="t090"></a>

## T090 - Produce a scientific report that retains model failures and uncertainty

**User need:** A user needs a report that communicates what the experiment does and does not establish.

**Target users:** [P08](../REQUIREMENTS_MAP.md#p08), [P09](../REQUIREMENTS_MAP.md#p09), [P16](../REQUIREMENTS_MAP.md#p16).

**Applicability tags:** common. Instance selection and conditional edges must be frozen before participant evaluation.

**Workflow stages:** estimate, exchange.

**Required input and constraints:** Known identifiable and nonidentifiable fit fixtures, raw records, units, model assumptions and report schema.

**Required output:** Machine-readable and human-readable results retaining raw estimates, diagnostics and provenance.

**Required capabilities:** [C12](../CAPABILITIES.md#c12), [C20](../CAPABILITIES.md#c20).

**Function traceability:**

- [F12.04](../CAPABILITIES.md#f12-04): Reconstruct and diagnose states or processes. Required for every instance of this task family.
- [F12.05](../CAPABILITIES.md#f12-05): Export interpretable analysis. Required for every instance of this task family.
- [F20.04](../CAPABILITIES.md#f20-04): Package reproducible evidence. Required for every instance of this task family.
- [F20.05](../CAPABILITIES.md#f20-05): Expose inspectable errors and traces. Required for every instance of this task family.

**Acceptance profiles:** [A04](../ACCEPTANCE.md#a04), [A09](../ACCEPTANCE.md#a09).

**Task-specific acceptance:** Units, uncertainty and raw-data links reconcile; unidentifiable fits and model mismatch are explicit; generated examples cannot be labeled as device measurements.

**Measurements:** report completeness; fit error; failure classification; export round-trip fidelity.

**Required negative case:** Clipping a failed fit into a plausible parameter or dropping missing outcomes is a reporting failure.

**Instance readiness:** Use the [instance specification template](../TASK_SPEC_TEMPLATE.md); bind fixtures, independent references, numerical/statistical thresholds, budgets, and attribution rules before execution.
