<!-- Generated from catalog.json by tools/requirements_docs.py. Do not edit directly. -->

# J10 - Run a recoverable device experiment

[All tasks](../TASK_CATALOG.md) | [Acceptance rules](../ACCEPTANCE.md) | [Traceability](../TRACEABILITY.md)

Status: requirements only. No task in this file is claimed as implemented or executed.

Workflow grounding: [S11](../SOURCES.md#s11), [S02](../SOURCES.md#s02). Sources inform context; they do not establish universal requirements or user-study validation.

<a id="t046"></a>

## T046 - Select a device capable of a planned experiment

**User need:** An experimenter needs to choose an accessible target whose actual profile matches the program.

**Target users:** [P09](../REQUIREMENTS_MAP.md#p09), [P16](../REQUIREMENTS_MAP.md#p16).

**Applicability tags:** gate, adaptive, analog, pulse, cv, annealing. Instance selection and conditional edges must be frozen before participant evaluation.

**Workflow stages:** formulate, compile.

**Required input and constraints:** Mocked target rosters, availability/access responses and programs with model/timing/control requirements.

**Required output:** A target decision and compatibility evidence without a submission.

**Required capabilities:** [C01](../CAPABILITIES.md#c01), [C03](../CAPABILITIES.md#c03), [C06](../CAPABILITIES.md#c06), [C11](../CAPABILITIES.md#c11).

**Function traceability:**

- [F11.01](../CAPABILITIES.md#f11-01): Discover and select execution targets. Required for every instance of this task family.
- [F01.02](../CAPABILITIES.md#f01-02): Discover capabilities and limits. Required for every instance of this task family.
- [F06.01](../CAPABILITIES.md#f06-01): Describe an executable target. Required for every instance of this task family.
- [F03.05](../CAPABILITIES.md#f03-05): Assess execution-profile compatibility. Required for every instance of this task family.

**Acceptance profiles:** [A01](../ACCEPTANCE.md#a01), [A05](../ACCEPTANCE.md#a05), [A08](../ACCEPTANCE.md#a08).

**Task-specific acceptance:** Declared capabilities match validation fixtures; unavailable, inaccessible or incompatible targets are distinguished and do not trigger substitute execution.

**Measurements:** selection correctness; assessment latency; false-compatible rate.

**Required negative case:** A provider adapter being installed is not evidence that the user has hardware access.

**Instance readiness:** Use the [instance specification template](../TASK_SPEC_TEMPLATE.md); bind fixtures, independent references, numerical/statistical thresholds, budgets, and attribution rules before execution.

<a id="t047"></a>

## T047 - Prepare and submit an explicitly authorized experiment batch

**User need:** A user needs predictable submission scope and a traceable acquisition request.

**Target users:** [P09](../REQUIREMENTS_MAP.md#p09).

**Applicability tags:** gate, adaptive, analog, pulse, cv, annealing. Instance selection and conditional edges must be frozen before participant evaluation.

**Workflow stages:** compile, execute.

**Required input and constraints:** A frozen plan, target snapshot, parameter bindings, shot limits and explicit authorization.

**Required output:** A validated preview and, only when authorized, job identities bound to the exact submitted payloads.

**Required capabilities:** [C01](../CAPABILITIES.md#c01), [C11](../CAPABILITIES.md#c11).

**Function traceability:**

- [F11.02](../CAPABILITIES.md#f11-02): Prepare a budgeted experiment. Required for every instance of this task family.
- [F11.03](../CAPABILITIES.md#f11-03): Submit and manage asynchronous jobs. Required for every instance of this task family.
- [F11.05](../CAPABILITIES.md#f11-05): Preserve acquisition and result provenance. Required for every instance of this task family.
- [F01.04](../CAPABILITIES.md#f01-04): Configure execution without exposing secrets. Required for every instance of this task family.

**Acceptance profiles:** [A08](../ACCEPTANCE.md#a08).

**Task-specific acceptance:** The submitted payload, bindings and budgets match the approved preview; uncertainty in provider cost is explicit and a stub verifies zero unapproved submissions.

**Measurements:** payload agreement; submission overhead; budget adherence.

**Required negative case:** Changed shots, extra calibration circuits or retries beyond the approved policy require a new explicit decision.

**Instance readiness:** Use the [instance specification template](../TASK_SPEC_TEMPLATE.md); bind fixtures, independent references, numerical/statistical thresholds, budgets, and attribution rules before execution.

<a id="t048"></a>

## T048 - Recover asynchronous or partially completed work

**User need:** A user needs to resume a study after interruption without losing or duplicating paid work.

**Target users:** [P09](../REQUIREMENTS_MAP.md#p09), [P16](../REQUIREMENTS_MAP.md#p16).

**Applicability tags:** common. Instance selection and conditional edges must be frozen before participant evaluation.

**Workflow stages:** execute, operate.

**Required input and constraints:** Recorded job IDs, partial result pages, timeouts, cancellation states and ambiguous submission acknowledgments.

**Required output:** A reconciled job ledger and complete/partial results with explicit unresolved states.

**Required capabilities:** [C11](../CAPABILITIES.md#c11), [C20](../CAPABILITIES.md#c20).

**Function traceability:**

- [F11.03](../CAPABILITIES.md#f11-03): Submit and manage asynchronous jobs. Required for every instance of this task family.
- [F11.04](../CAPABILITIES.md#f11-04): Recover and reconcile partial work. Required for every instance of this task family.
- [F11.05](../CAPABILITIES.md#f11-05): Preserve acquisition and result provenance. Required for every instance of this task family.
- [F20.05](../CAPABILITIES.md#f20-05): Expose inspectable errors and traces. Required for every instance of this task family.

**Acceptance profiles:** [A08](../ACCEPTANCE.md#a08).

**Task-specific acceptance:** Retrieval reconstructs available results and distinguishes unknown submission from failure; no duplicate job is created outside the predeclared retry/authorization policy.

**Measurements:** recovery success; duplicate submissions; recovery time; unresolved jobs.

**Required negative case:** A client timeout after server acceptance cannot automatically become a second paid submission.

**Instance readiness:** Use the [instance specification template](../TASK_SPEC_TEMPLATE.md); bind fixtures, independent references, numerical/statistical thresholds, budgets, and attribution rules before execution.

<a id="t049"></a>

## T049 - Recover logical observations from compiled device results

**User need:** A scientist needs counts attributed to the right program, binding and logical subsystem.

**Target users:** [P09](../REQUIREMENTS_MAP.md#p09), [P08](../REQUIREMENTS_MAP.md#p08).

**Applicability tags:** gate, adaptive. Instance selection and conditional edges must be frozen before participant evaluation.

**Workflow stages:** execute, estimate.

**Required input and constraints:** Batches with distinct IDs, unused wires, final layout permutations, multiple registers and provider result order changes.

**Required output:** Canonical logical result records plus the original provider records and mappings.

**Required capabilities:** [C06](../CAPABILITIES.md#c06), [C11](../CAPABILITIES.md#c11), [C12](../CAPABILITIES.md#c12), [C20](../CAPABILITIES.md#c20).

**Function traceability:**

- [F11.05](../CAPABILITIES.md#f11-05): Preserve acquisition and result provenance. Required for every instance of this task family.
- [F06.04](../CAPABILITIES.md#f06-04): Place, route and recover logical outputs. Required for every instance of this task family.
- [F12.01](../CAPABILITIES.md#f12-01): Validate and normalize result records. Required for every instance of this task family.
- [F20.02](../CAPABILITIES.md#f20-02): Normalize conventions across boundaries. Required for every instance of this task family.

**Acceptance profiles:** [A02](../ACCEPTANCE.md#a02), [A08](../ACCEPTANCE.md#a08).

**Task-specific acceptance:** Every result is matched to its exact program/binding and logical bits; all shot totals and partial/missing records reconcile without positional guesses.

**Measurements:** mapping accuracy; collection overhead; missing-record detection.

**Required negative case:** Reordered publications or provider-endian strings must not silently swap experiment identities.

**Instance readiness:** Use the [instance specification template](../TASK_SPEC_TEMPLATE.md); bind fixtures, independent references, numerical/statistical thresholds, budgets, and attribution rules before execution.

<a id="t050"></a>

## T050 - Repeat an experiment while retaining acquisition context

**User need:** A user needs to distinguish software differences from device drift and acquisition conditions.

**Target users:** [P09](../REQUIREMENTS_MAP.md#p09), [P08](../REQUIREMENTS_MAP.md#p08).

**Applicability tags:** gate, analog, pulse, cv, annealing. Instance selection and conditional edges must be frozen before participant evaluation.

**Workflow stages:** execute, estimate, operate.

**Required input and constraints:** A repeated protocol with acquisition windows, calibration snapshots, interleaved ordering and frozen software settings.

**Required output:** A run series with time/device context and separately reported software and acquisition effects.

**Required capabilities:** [C10](../CAPABILITIES.md#c10), [C11](../CAPABILITIES.md#c11), [C12](../CAPABILITIES.md#c12), [C20](../CAPABILITIES.md#c20).

**Function traceability:**

- [F11.05](../CAPABILITIES.md#f11-05): Preserve acquisition and result provenance. Required for every instance of this task family.
- [F12.02](../CAPABILITIES.md#f12-02): Estimate quantities with uncertainty. Required for every instance of this task family.
- [F20.04](../CAPABILITIES.md#f20-04): Package reproducible evidence. Required for every instance of this task family.
- [F10.05](../CAPABILITIES.md#f10-05): Validate noise predictions out of sample. Required for every instance of this task family.

**Acceptance profiles:** [A04](../ACCEPTANCE.md#a04), [A08](../ACCEPTANCE.md#a08).

**Task-specific acceptance:** The same task/budget is preserved; timestamp and calibration provenance are retained and any missing context limits the permitted comparison claim.

**Measurements:** protocol completion; metadata completeness; between-run variation.

**Required negative case:** Queue time or a hardware fidelity change cannot be assigned to SDK computation speed without a controlled software measurement.

**Instance readiness:** Use the [instance specification template](../TASK_SPEC_TEMPLATE.md); bind fixtures, independent references, numerical/statistical thresholds, budgets, and attribution rules before execution.
