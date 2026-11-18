<!-- Generated from catalog.json by tools/requirements_docs.py. Do not edit directly. -->

# J04 - Make a program executable on a target

[All tasks](../TASK_CATALOG.md) | [Acceptance rules](../ACCEPTANCE.md) | [Traceability](../TRACEABILITY.md)

Status: requirements only. No task in this file is claimed as implemented or executed.

Workflow grounding: [S01](../SOURCES.md#s01), [S02](../SOURCES.md#s02). Sources inform context; they do not establish universal requirements or user-study validation.

<a id="t016"></a>

## T016 - Lower an algorithm into an executable instruction set

**User need:** A device user needs every operation expressed in a target-supported form.

**Target users:** [P06](../REQUIREMENTS_MAP.md#p06), [P09](../REQUIREMENTS_MAP.md#p09).

**Applicability tags:** gate. Instance selection and conditional edges must be frozen before participant evaluation.

**Workflow stages:** compile, verify.

**Required input and constraints:** A fixed target basis, symbolic and numeric programs, synthesis tolerance and ancilla budget.

**Required output:** A legal lowered program with preserved semantics and resource counts.

**Required capabilities:** [C06](../CAPABILITIES.md#c06), [C20](../CAPABILITIES.md#c20).

**Function traceability:**

- [F06.01](../CAPABILITIES.md#f06-01): Describe an executable target. Required for every instance of this task family.
- [F06.02](../CAPABILITIES.md#f06-02): Synthesize and decompose operations. Required for every instance of this task family.
- [F06.03](../CAPABILITIES.md#f06-03): Optimize while preserving semantics. Required for every instance of this task family.
- [F20.02](../CAPABILITIES.md#f20-02): Normalize conventions across boundaries. Required for every instance of this task family.

**Acceptance profiles:** [A02](../ACCEPTANCE.md#a02), [A03](../ACCEPTANCE.md#a03), [A05](../ACCEPTANCE.md#a05).

**Task-specific acceptance:** Every emitted operation satisfies the target contract; small-instance semantics and synthesis error pass; symbolic parameters and global-phase conventions are preserved.

**Measurements:** lowering time; two-body operations; workspace; approximation error.

**Required negative case:** An unsupported gate cannot pass merely because an external simulator can execute it.

**Instance readiness:** Use the [instance specification template](../TASK_SPEC_TEMPLATE.md); bind fixtures, independent references, numerical/statistical thresholds, budgets, and attribution rules before execution.

<a id="t017"></a>

## T017 - Map a logical algorithm to constrained connectivity

**User need:** A user needs executable interactions with correct final logical results.

**Target users:** [P06](../REQUIREMENTS_MAP.md#p06), [P09](../REQUIREMENTS_MAP.md#p09).

**Applicability tags:** gate. Instance selection and conditional edges must be frozen before participant evaluation.

**Workflow stages:** compile, verify.

**Required input and constraints:** Frozen line, grid, irregular and all-to-all graphs; nonlocal circuits; placement policy and compile budget.

**Required output:** A routed program, initial/final mappings and logical result reconstruction.

**Required capabilities:** [C06](../CAPABILITIES.md#c06), [C12](../CAPABILITIES.md#c12).

**Function traceability:**

- [F06.01](../CAPABILITIES.md#f06-01): Describe an executable target. Required for every instance of this task family.
- [F06.04](../CAPABILITIES.md#f06-04): Place, route and recover logical outputs. Required for every instance of this task family.
- [F06.03](../CAPABILITIES.md#f06-03): Optimize while preserving semantics. Required for every instance of this task family.
- [F12.01](../CAPABILITIES.md#f12-01): Validate and normalize result records. Required for every instance of this task family.

**Acceptance profiles:** [A03](../ACCEPTANCE.md#a03), [A05](../ACCEPTANCE.md#a05).

**Task-specific acceptance:** Every interaction is legal and reconstructed small-instance outputs match the original; routing quality is evaluated only after these gates pass.

**Measurements:** compile time; added interactions; two-body depth; budget completion.

**Required negative case:** A final permutation, direction constraint or disconnected target cannot be ignored.

**Instance readiness:** Use the [instance specification template](../TASK_SPEC_TEMPLATE.md); bind fixtures, independent references, numerical/statistical thresholds, budgets, and attribution rules before execution.

<a id="t018"></a>

## T018 - Schedule a program under timing and shared-resource constraints

**User need:** An experimenter needs a schedule that can actually run on the declared device.

**Target users:** [P06](../REQUIREMENTS_MAP.md#p06), [P11](../REQUIREMENTS_MAP.md#p11).

**Applicability tags:** gate, pulse. Instance selection and conditional edges must be frozen before participant evaluation.

**Workflow stages:** compile, verify.

**Required input and constraints:** Instruction durations, alignment, conflicts, classical latency, dependencies and a frozen calibration snapshot.

**Required output:** A schedule with unit-tagged durations and conflict/critical-path evidence.

**Required capabilities:** [C06](../CAPABILITIES.md#c06), [C15](../CAPABILITIES.md#c15), [C20](../CAPABILITIES.md#c20).

**Function traceability:**

- [F06.01](../CAPABILITIES.md#f06-01): Describe an executable target. Required for every instance of this task family.
- [F06.05](../CAPABILITIES.md#f06-05): Schedule and account for resources. Required for every instance of this task family.
- [F15.02](../CAPABILITIES.md#f15-02): Schedule physical controls. Required when the frozen instance includes the pulse applicability tag.
- [F20.04](../CAPABILITIES.md#f20-04): Package reproducible evidence. Required for every instance of this task family.

**Acceptance profiles:** [A05](../ACCEPTANCE.md#a05), [A10](../ACCEPTANCE.md#a10).

**Task-specific acceptance:** All dependency, alignment and shared-resource constraints hold; duration accounting matches an independent schedule validator.

**Measurements:** makespan; idle exposure; compile time; constraint violations.

**Required negative case:** Illegal overlaps and incompatible time units cannot be repaired silently or excluded from reported duration.

**Instance readiness:** Use the [instance specification template](../TASK_SPEC_TEMPLATE.md); bind fixtures, independent references, numerical/statistical thresholds, budgets, and attribution rules before execution.

<a id="t019"></a>

## T019 - Choose a compiler configuration under a practical budget

**User need:** A user needs a useful quality-versus-latency choice rather than the smallest circuit at unlimited cost.

**Target users:** [P06](../REQUIREMENTS_MAP.md#p06), [P14](../REQUIREMENTS_MAP.md#p14).

**Applicability tags:** gate. Instance selection and conditional edges must be frozen before participant evaluation.

**Workflow stages:** compile, optimize.

**Required input and constraints:** A frozen circuit distribution, target, seed set, wall-time/memory budgets and common quality metrics.

**Required output:** Feasible compile results and a quality/time Pareto surface including failed and censored runs.

**Required capabilities:** [C06](../CAPABILITIES.md#c06), [C19](../CAPABILITIES.md#c19).

**Function traceability:**

- [F06.03](../CAPABILITIES.md#f06-03): Optimize while preserving semantics. Required for every instance of this task family.
- [F06.04](../CAPABILITIES.md#f06-04): Place, route and recover logical outputs. Required for every instance of this task family.
- [F06.06](../CAPABILITIES.md#f06-06): Expose compile tradeoffs and diagnostics. Required for every instance of this task family.
- [F19.04](../CAPABILITIES.md#f19-04): Measure and enforce execution budgets. Required for every instance of this task family.

**Acceptance profiles:** [A05](../ACCEPTANCE.md#a05).

**Task-specific acceptance:** Semantic and target checks pass first; all tuning and search cost is recorded; only results within the predeclared budget enter that budget cohort.

**Measurements:** time to target quality; interaction count at fixed budget; memory; failure rate.

**Required negative case:** A timeout, best-of-many hidden seed search or target-specific gate-count convention cannot be presented as a fair win.

**Instance readiness:** Use the [instance specification template](../TASK_SPEC_TEMPLATE.md); bind fixtures, independent references, numerical/statistical thresholds, budgets, and attribution rules before execution.

<a id="t020"></a>

## T020 - Determine feasibility before executing a target-incompatible program

**User need:** A user needs an explicit explanation when a chosen device cannot carry the experiment.

**Target users:** [P06](../REQUIREMENTS_MAP.md#p06), [P09](../REQUIREMENTS_MAP.md#p09).

**Applicability tags:** gate, adaptive, pulse. Instance selection and conditional edges must be frozen before participant evaluation.

**Workflow stages:** formulate, compile.

**Required input and constraints:** Targets with insufficient wires, unsupported control flow, forbidden operations or incompatible timing.

**Required output:** A feasibility decision, constraint diagnostics and any explicitly authorized transformation proposal.

**Required capabilities:** [C01](../CAPABILITIES.md#c01), [C03](../CAPABILITIES.md#c03), [C06](../CAPABILITIES.md#c06).

**Function traceability:**

- [F01.02](../CAPABILITIES.md#f01-02): Discover capabilities and limits. Required for every instance of this task family.
- [F03.05](../CAPABILITIES.md#f03-05): Assess execution-profile compatibility. Required for every instance of this task family.
- [F06.01](../CAPABILITIES.md#f06-01): Describe an executable target. Required for every instance of this task family.
- [F06.06](../CAPABILITIES.md#f06-06): Expose compile tradeoffs and diagnostics. Required for every instance of this task family.

**Acceptance profiles:** [A01](../ACCEPTANCE.md#a01), [A05](../ACCEPTANCE.md#a05).

**Task-specific acceptance:** Feasible fixtures compile legally; infeasible fixtures identify the violated constraints before execution; emulation or changed semantics require disclosure and cohort separation.

**Measurements:** decision accuracy; assessment time; false-feasible rate.

**Required negative case:** A compiler must not silently switch provider, discard control flow or increase the requested error budget.

**Instance readiness:** Use the [instance specification template](../TASK_SPEC_TEMPLATE.md); bind fixtures, independent references, numerical/statistical thresholds, budgets, and attribution rules before execution.
