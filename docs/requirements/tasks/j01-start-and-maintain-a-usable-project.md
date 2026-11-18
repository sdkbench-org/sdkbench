<!-- Generated from catalog.json by tools/requirements_docs.py. Do not edit directly. -->

# J01 - Start and maintain a usable project

[All tasks](../TASK_CATALOG.md) | [Acceptance rules](../ACCEPTANCE.md) | [Traceability](../TRACEABILITY.md)

Status: requirements only. No task in this file is claimed as implemented or executed.

Workflow grounding: [S01](../SOURCES.md#s01), [S08](../SOURCES.md#s08). Sources inform context; they do not establish universal requirements or user-study validation.

<a id="t001"></a>

## T001 - Start a working project in a clean environment

**User need:** A new user must reach a first valid result without undocumented setup.

**Target users:** [P01](../REQUIREMENTS_MAP.md#p01), [P16](../REQUIREMENTS_MAP.md#p16).

**Applicability tags:** common. Instance selection and conditional edges must be frozen before participant evaluation.

**Workflow stages:** setup, verify.

**Required input and constraints:** A frozen supported OS, interpreter, package source and documented installation procedure.

**Required output:** An environment manifest, complete install log and a checked example result.

**Required capabilities:** [C01](../CAPABILITIES.md#c01), [C20](../CAPABILITIES.md#c20).

**Function traceability:**

- [F01.01](../CAPABILITIES.md#f01-01): Install a reproducible environment. Required for every instance of this task family.
- [F01.03](../CAPABILITIES.md#f01-03): Learn and diagnose a workflow. Required for every instance of this task family.
- [F20.04](../CAPABILITIES.md#f20-04): Package reproducible evidence. Required for every instance of this task family.

**Acceptance profiles:** [A01](../ACCEPTANCE.md#a01).

**Task-specific acceptance:** Installation and the example complete without undeclared manual steps; resolved versions match the manifest and the example meets its independent oracle.

**Measurements:** install wall time; download bytes; disk footprint; success rate.

**Required negative case:** An unsupported interpreter or missing binary dependency produces an actionable diagnosis rather than a successful import claim.

**Instance readiness:** Use the [instance specification template](../TASK_SPEC_TEMPLATE.md); bind fixtures, independent references, numerical/statistical thresholds, budgets, and attribution rules before execution.

<a id="t002"></a>

## T002 - Determine whether a planned study is supported

**User need:** A user must know execution limits before investing in an experiment.

**Target users:** [P02](../REQUIREMENTS_MAP.md#p02), [P09](../REQUIREMENTS_MAP.md#p09), [P16](../REQUIREMENTS_MAP.md#p16).

**Applicability tags:** common. Instance selection and conditional edges must be frozen before participant evaluation.

**Workflow stages:** setup, formulate.

**Required input and constraints:** Queries for supported models, operations, precision, derivatives, devices and known limits.

**Required output:** Machine-readable capability answers with version, scope and fallback policy.

**Required capabilities:** [C01](../CAPABILITIES.md#c01), [C03](../CAPABILITIES.md#c03), [C05](../CAPABILITIES.md#c05), [C20](../CAPABILITIES.md#c20).

**Function traceability:**

- [F01.02](../CAPABILITIES.md#f01-02): Discover capabilities and limits. Required for every instance of this task family.
- [F03.05](../CAPABILITIES.md#f03-05): Assess execution-profile compatibility. Required for every instance of this task family.
- [F05.05](../CAPABILITIES.md#f05-05): Select and disclose execution implementation. Required for every instance of this task family.
- [F20.05](../CAPABILITIES.md#f20-05): Expose inspectable errors and traces. Required for every instance of this task family.

**Acceptance profiles:** [A01](../ACCEPTANCE.md#a01).

**Task-specific acceptance:** Answers agree with executable positive and negative probes; unknown support is explicit and no unavailable device is reported as tested.

**Measurements:** discovery latency; answer/probe agreement; missing declarations.

**Required negative case:** A requested feature absent from a selected backend is rejected or explicitly transformed before execution.

**Instance readiness:** Use the [instance specification template](../TASK_SPEC_TEMPLATE.md); bind fixtures, independent references, numerical/statistical thresholds, budgets, and attribution rules before execution.

<a id="t003"></a>

## T003 - Learn a complete workflow from documentation

**User need:** A learner needs a correct mental model and an executable example.

**Target users:** [P01](../REQUIREMENTS_MAP.md#p01), [P16](../REQUIREMENTS_MAP.md#p16).

**Applicability tags:** gate, common. Instance selection and conditional edges must be frozen before participant evaluation.

**Workflow stages:** setup, express, execute, estimate.

**Required input and constraints:** A frozen tutorial with specified prerequisites, wire order, parameters and expected outputs.

**Required output:** A reproduced artifact and a structured record of setup or interpretation obstacles.

**Required capabilities:** [C01](../CAPABILITIES.md#c01), [C02](../CAPABILITIES.md#c02), [C05](../CAPABILITIES.md#c05), [C12](../CAPABILITIES.md#c12).

**Function traceability:**

- [F01.03](../CAPABILITIES.md#f01-03): Learn and diagnose a workflow. Required for every instance of this task family.
- [F02.01](../CAPABILITIES.md#f02-01): Construct and inspect programs. Required for every instance of this task family.
- [F05.02](../CAPABILITIES.md#f05-02): Sample declared measurements. Required for every instance of this task family.
- [F12.05](../CAPABILITIES.md#f12-05): Export interpretable analysis. Required for every instance of this task family.

**Acceptance profiles:** [A01](../ACCEPTANCE.md#a01), [A03](../ACCEPTANCE.md#a03).

**Task-specific acceptance:** A reviewer following only the declared instructions reproduces the expected result; documentation states conventions and all required dependencies.

**Measurements:** documented-step completion; unassisted success rate; recorded interventions.

**Required negative case:** A convention-sensitive example distinguishes control/target and wire significance rather than relying only on a symmetric Bell state.

**Instance readiness:** Use the [instance specification template](../TASK_SPEC_TEMPLATE.md); bind fixtures, independent references, numerical/statistical thresholds, budgets, and attribution rules before execution.

<a id="t004"></a>

## T004 - Configure local and remote execution deliberately

**User need:** An engineer needs to choose an account and target without accidental submissions or credential exposure.

**Target users:** [P09](../REQUIREMENTS_MAP.md#p09), [P16](../REQUIREMENTS_MAP.md#p16).

**Applicability tags:** common. Instance selection and conditional edges must be frozen before participant evaluation.

**Workflow stages:** setup, execute, operate.

**Required input and constraints:** Dummy credentials, mocked accounts, target settings, denied permissions and an explicit submission authorization policy.

**Required output:** A configuration or dry-run artifact, redacted diagnostics and an auditable submission decision.

**Required capabilities:** [C01](../CAPABILITIES.md#c01), [C11](../CAPABILITIES.md#c11), [C20](../CAPABILITIES.md#c20).

**Function traceability:**

- [F01.04](../CAPABILITIES.md#f01-04): Configure execution without exposing secrets. Required for every instance of this task family.
- [F11.01](../CAPABILITIES.md#f11-01): Discover and select execution targets. Required for every instance of this task family.
- [F11.02](../CAPABILITIES.md#f11-02): Prepare a budgeted experiment. Required for every instance of this task family.
- [F11.03](../CAPABILITIES.md#f11-03): Submit and manage asynchronous jobs. Required for every instance of this task family.
- [F20.05](../CAPABILITIES.md#f20-05): Expose inspectable errors and traces. Required for every instance of this task family.

**Acceptance profiles:** [A01](../ACCEPTANCE.md#a01), [A08](../ACCEPTANCE.md#a08).

**Task-specific acceptance:** Dry-run and import paths make no execution submission; unauthorized paths fail; dummy secrets never appear in declared logs or persisted artifacts.

**Measurements:** configuration success rate; unauthorized submission count; secret exposure count.

**Required negative case:** Invalid credentials and a missing authorization flag cannot trigger an automatic paid retry.

**Instance readiness:** Use the [instance specification template](../TASK_SPEC_TEMPLATE.md); bind fixtures, independent references, numerical/statistical thresholds, budgets, and attribution rules before execution.

<a id="t005"></a>

## T005 - Integrate a new provider or computation component

**User need:** An integration engineer needs a supported extension path without modifying core internals.

**Target users:** [P16](../REQUIREMENTS_MAP.md#p16).

**Applicability tags:** common. Instance selection and conditional edges must be frozen before participant evaluation.

**Workflow stages:** setup, express, execute, operate.

**Required input and constraints:** A minimal contract-conforming stub plus malformed operations, outputs and provider errors.

**Required output:** An extension, boundary diagnostics and a result carrying component provenance.

**Required capabilities:** [C01](../CAPABILITIES.md#c01), [C11](../CAPABILITIES.md#c11), [C20](../CAPABILITIES.md#c20).

**Function traceability:**

- [F01.05](../CAPABILITIES.md#f01-05): Extend an execution path. Required for every instance of this task family.
- [F11.05](../CAPABILITIES.md#f11-05): Preserve acquisition and result provenance. Required for every instance of this task family.
- [F20.02](../CAPABILITIES.md#f20-02): Normalize conventions across boundaries. Required for every instance of this task family.
- [F20.05](../CAPABILITIES.md#f20-05): Expose inspectable errors and traces. Required for every instance of this task family.

**Acceptance profiles:** [A01](../ACCEPTANCE.md#a01), [A08](../ACCEPTANCE.md#a08).

**Task-specific acceptance:** The documented extension interface accepts the valid component, rejects malformed records and preserves program/result conventions and structured failures.

**Measurements:** integration steps; boundary overhead; contract pass rate.

**Required negative case:** A plugin returning a different wire order or truncated output is detected, not accepted as a successful result.

**Instance readiness:** Use the [instance specification template](../TASK_SPEC_TEMPLATE.md); bind fixtures, independent references, numerical/statistical thresholds, budgets, and attribution rules before execution.
