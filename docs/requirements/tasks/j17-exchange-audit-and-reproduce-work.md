<!-- Generated from catalog.json by tools/requirements_docs.py. Do not edit directly. -->

# J17 - Exchange, audit and reproduce work

[All tasks](../TASK_CATALOG.md) | [Acceptance rules](../ACCEPTANCE.md) | [Traceability](../TRACEABILITY.md)

Status: requirements only. No task in this file is claimed as implemented or executed.

Workflow grounding: [S01](../SOURCES.md#s01), [S02](../SOURCES.md#s02), [S03](../SOURCES.md#s03). Sources inform context; they do not establish universal requirements or user-study validation.

<a id="t081"></a>

## T081 - Exchange a program through a declared standard/profile

**User need:** An engineer needs another tool to understand the intended program.

**Target users:** [P16](../REQUIREMENTS_MAP.md#p16), [P02](../REQUIREMENTS_MAP.md#p02).

**Applicability tags:** gate, adaptive, pulse. Instance selection and conditional edges must be frozen before participant evaluation.

**Workflow stages:** exchange, verify.

**Required input and constraints:** Versioned interchange fixtures, parameters, classical records, timing features and an explicit supported profile.

**Required output:** Imported/exported programs and feature-level conversion diagnostics.

**Required capabilities:** [C03](../CAPABILITIES.md#c03), [C06](../CAPABILITIES.md#c06), [C20](../CAPABILITIES.md#c20).

**Function traceability:**

- [F20.01](../CAPABILITIES.md#f20-01): Import and export declared formats. Required for every instance of this task family.
- [F20.02](../CAPABILITIES.md#f20-02): Normalize conventions across boundaries. Required for every instance of this task family.
- [F03.05](../CAPABILITIES.md#f03-05): Assess execution-profile compatibility. Required for every instance of this task family.
- [F06.01](../CAPABILITIES.md#f06-01): Describe an executable target. Required for every instance of this task family.

**Acceptance profiles:** [A02](../ACCEPTANCE.md#a02), [A03](../ACCEPTANCE.md#a03), [A05](../ACCEPTANCE.md#a05).

**Task-specific acceptance:** Supported fixtures retain required semantics on independent bounded references; unsupported syntax/features are rejected with a precise profile boundary.

**Measurements:** semantic retention; parse/export time; diagnostic completeness.

**Required negative case:** Successful parsing of a program with dropped control or calibration blocks is not successful interchange.

**Instance readiness:** Use the [instance specification template](../TASK_SPEC_TEMPLATE.md); bind fixtures, independent references, numerical/statistical thresholds, budgets, and attribution rules before execution.

<a id="t082"></a>

## T082 - Round-trip an artifact across different conventions

**User need:** A user needs portability without hidden changes to wire, variable, unit or output meaning.

**Target users:** [P16](../REQUIREMENTS_MAP.md#p16), [P02](../REQUIREMENTS_MAP.md#p02).

**Applicability tags:** gate, adaptive, qudit, cv, annealing. Instance selection and conditional edges must be frozen before participant evaluation.

**Workflow stages:** exchange, verify.

**Required input and constraints:** Asymmetric convention-sensitive fixtures, source/target maps and the required preservable metadata.

**Required output:** Round-trip artifacts plus an explicit preservation/loss report.

**Required capabilities:** [C04](../CAPABILITIES.md#c04), [C12](../CAPABILITIES.md#c12), [C20](../CAPABILITIES.md#c20).

**Function traceability:**

- [F20.02](../CAPABILITIES.md#f20-02): Normalize conventions across boundaries. Required for every instance of this task family.
- [F20.03](../CAPABILITIES.md#f20-03): Round-trip artifacts without hidden loss. Required for every instance of this task family.
- [F12.01](../CAPABILITIES.md#f12-01): Validate and normalize result records. Required for every instance of this task family.
- [F04.01](../CAPABILITIES.md#f04-01): Represent states and linear operators. Required for every instance of this task family.

**Acceptance profiles:** [A02](../ACCEPTANCE.md#a02), [A03](../ACCEPTANCE.md#a03), [A10](../ACCEPTANCE.md#a10).

**Task-specific acceptance:** Small reference outputs and required metadata agree after declared conversions; irrecoverable information loss is rejected or explicitly outside the round-trip contract.

**Measurements:** round-trip pass rate; conversion time; retained metadata.

**Required negative case:** Byte equality alone is insufficient, while semantic equality cannot excuse losing required calibration or result provenance.

**Instance readiness:** Use the [instance specification template](../TASK_SPEC_TEMPLATE.md); bind fixtures, independent references, numerical/statistical thresholds, budgets, and attribution rules before execution.

<a id="t083"></a>

## T083 - Reproduce a published software result from its evidence bundle

**User need:** A reviewer needs to reproduce a claim without the original workstation or undisclosed settings.

**Target users:** [P16](../REQUIREMENTS_MAP.md#p16), [P01](../REQUIREMENTS_MAP.md#p01).

**Applicability tags:** common. Instance selection and conditional edges must be frozen before participant evaluation.

**Workflow stages:** setup, execute, exchange.

**Required input and constraints:** An immutable evidence bundle with input/reference hashes, environment lock, commands, seeds, outputs and restrictions.

**Required output:** A replayed run, environment differences and checked result comparison.

**Required capabilities:** [C01](../CAPABILITIES.md#c01), [C05](../CAPABILITIES.md#c05), [C12](../CAPABILITIES.md#c12), [C20](../CAPABILITIES.md#c20).

**Function traceability:**

- [F20.04](../CAPABILITIES.md#f20-04): Package reproducible evidence. Required for every instance of this task family.
- [F01.01](../CAPABILITIES.md#f01-01): Install a reproducible environment. Required for every instance of this task family.
- [F05.05](../CAPABILITIES.md#f05-05): Select and disclose execution implementation. Required for every instance of this task family.
- [F12.05](../CAPABILITIES.md#f12-05): Export interpretable analysis. Required for every instance of this task family.

**Acceptance profiles:** [A01](../ACCEPTANCE.md#a01), [A03](../ACCEPTANCE.md#a03), [A04](../ACCEPTANCE.md#a04).

**Task-specific acceptance:** The declared reference and numerical/statistical contract can be checked from the bundle; missing access or artifacts are explicit and prevent a reproducible label.

**Measurements:** reproduction success; setup/replay time; missing artifacts; result discrepancy.

**Required negative case:** A screenshot, best runtime or mutable notebook link alone is not a replayable result.

**Instance readiness:** Use the [instance specification template](../TASK_SPEC_TEMPLATE.md); bind fixtures, independent references, numerical/statistical thresholds, budgets, and attribution rules before execution.

<a id="t084"></a>

## T084 - Identify which components actually performed the work

**User need:** A reviewer needs to attribute frontend, compiler, engine and external-service contributions accurately.

**Target users:** [P16](../REQUIREMENTS_MAP.md#p16), [P07](../REQUIREMENTS_MAP.md#p07).

**Applicability tags:** common. Instance selection and conditional edges must be frozen before participant evaluation.

**Workflow stages:** verify, operate, exchange.

**Required input and constraints:** A workflow containing optional engines, derivative methods, compilation caches and intentional fallback conditions.

**Required output:** A component/version dependency chain and stage-level execution/cost evidence.

**Required capabilities:** [C05](../CAPABILITIES.md#c05), [C08](../CAPABILITIES.md#c08), [C20](../CAPABILITIES.md#c20).

**Function traceability:**

- [F05.05](../CAPABILITIES.md#f05-05): Select and disclose execution implementation. Required for every instance of this task family.
- [F08.05](../CAPABILITIES.md#f08-05): Disclose derivative method and cost. Required for every instance of this task family.
- [F20.04](../CAPABILITIES.md#f20-04): Package reproducible evidence. Required for every instance of this task family.
- [F20.05](../CAPABILITIES.md#f20-05): Expose inspectable errors and traces. Required for every instance of this task family.

**Acceptance profiles:** [A01](../ACCEPTANCE.md#a01), [A11](../ACCEPTANCE.md#a11).

**Task-specific acceptance:** Actual execution and fallback match telemetry/probes; all externally supplied work and cached setup costs are disclosed under the chosen measurement boundary.

**Measurements:** provenance completeness; unreported fallback count; stage overhead.

**Required negative case:** Two frontends using the same engine cannot be presented as independent engine implementations or independent numerical oracles.

**Instance readiness:** Use the [instance specification template](../TASK_SPEC_TEMPLATE.md); bind fixtures, independent references, numerical/statistical thresholds, budgets, and attribution rules before execution.

<a id="t085"></a>

## T085 - Detect semantic or operational regressions after an upgrade

**User need:** A maintainer needs to know whether upgrading preserves an existing study.

**Target users:** [P16](../REQUIREMENTS_MAP.md#p16).

**Applicability tags:** common, gate. Instance selection and conditional edges must be frozen before participant evaluation.

**Workflow stages:** setup, verify, operate.

**Required input and constraints:** Frozen task/fixture versions, old/new dependency locks and declared compatibility promises.

**Required output:** A regression report separating changed semantics, environment failures and performance changes.

**Required capabilities:** [C01](../CAPABILITIES.md#c01), [C20](../CAPABILITIES.md#c20).

**Function traceability:**

- [F20.04](../CAPABILITIES.md#f20-04): Package reproducible evidence. Required for every instance of this task family.
- [F20.05](../CAPABILITIES.md#f20-05): Expose inspectable errors and traces. Required for every instance of this task family.
- [F01.02](../CAPABILITIES.md#f01-02): Discover capabilities and limits. Required for every instance of this task family.
- [F20.03](../CAPABILITIES.md#f20-03): Round-trip artifacts without hidden loss. Required for every instance of this task family.

**Acceptance profiles:** [A01](../ACCEPTANCE.md#a01), [A03](../ACCEPTANCE.md#a03), [A08](../ACCEPTANCE.md#a08).

**Task-specific acceptance:** The same frozen acceptance contracts are evaluated for both environments; migration requirements and intentional breaking changes remain visible.

**Measurements:** regression count; compatible task coverage; performance change; diagnostic quality.

**Required negative case:** Changing the test inputs or dropping failed tasks during an upgrade invalidates a direct regression claim.

**Instance readiness:** Use the [instance specification template](../TASK_SPEC_TEMPLATE.md); bind fixtures, independent references, numerical/statistical thresholds, budgets, and attribution rules before execution.
