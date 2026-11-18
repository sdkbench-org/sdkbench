<!-- Generated from catalog.json by tools/requirements_docs.py. Do not edit directly. -->

# J16 - Scale and operate a computational study

[All tasks](../TASK_CATALOG.md) | [Acceptance rules](../ACCEPTANCE.md) | [Traceability](../TRACEABILITY.md)

Status: requirements only. No task in this file is claimed as implemented or executed.

Workflow grounding: [S10](../SOURCES.md#s10). Sources inform context; they do not establish universal requirements or user-study validation.

<a id="t076"></a>

## T076 - Run the same output contract on supported compute devices

**User need:** An operator needs to know which devices and precisions actually complete a study.

**Target users:** [P15](../REQUIREMENTS_MAP.md#p15), [P07](../REQUIREMENTS_MAP.md#p07).

**Applicability tags:** gate, analog, cv. Instance selection and conditional edges must be frozen before participant evaluation.

**Workflow stages:** setup, execute, verify.

**Required input and constraints:** Frozen outputs/accuracy targets, CPU/accelerator configurations and supported precision combinations.

**Required output:** Per-device correctness, actual execution path, memory and timing records.

**Required capabilities:** [C05](../CAPABILITIES.md#c05), [C19](../CAPABILITIES.md#c19), [C20](../CAPABILITIES.md#c20).

**Function traceability:**

- [F19.01](../CAPABILITIES.md#f19-01): Select and measure compute resources. Required for every instance of this task family.
- [F05.05](../CAPABILITIES.md#f05-05): Select and disclose execution implementation. Required for every instance of this task family.
- [F20.04](../CAPABILITIES.md#f20-04): Package reproducible evidence. Required for every instance of this task family.
- [F19.04](../CAPABILITIES.md#f19-04): Measure and enforce execution budgets. Required for every instance of this task family.

**Acceptance profiles:** [A03](../ACCEPTANCE.md#a03), [A11](../ACCEPTANCE.md#a11).

**Task-specific acceptance:** The same output/accuracy contract passes; device execution is verified, asynchronous work is synchronized and any host fallback is explicit.

**Measurements:** time to accuracy; peak memory; capacity; fallback count.

**Required negative case:** A GPU label with CPU execution or a lower-precision result outside tolerance cannot count as successful acceleration.

**Instance readiness:** Use the [instance specification template](../TASK_SPEC_TEMPLATE.md); bind fixtures, independent references, numerical/statistical thresholds, budgets, and attribution rules before execution.

<a id="t077"></a>

## T077 - Expand a single computation through distributed state or tensor partitioning

**User need:** A user needs a larger single problem to fit across multiple resources.

**Target users:** [P15](../REQUIREMENTS_MAP.md#p15), [P07](../REQUIREMENTS_MAP.md#p07).

**Applicability tags:** gate, analog. Instance selection and conditional edges must be frozen before participant evaluation.

**Workflow stages:** execute, operate, verify.

**Required input and constraints:** Fixed strong-scaling and separately defined capacity/weak-scaling workloads, partition policy and output contract.

**Required output:** Validated distributed outputs with partition and communication evidence.

**Required capabilities:** [C05](../CAPABILITIES.md#c05), [C07](../CAPABILITIES.md#c07), [C19](../CAPABILITIES.md#c19).

**Function traceability:**

- [F19.02](../CAPABILITIES.md#f19-02): Partition states or tensor computations. Required for every instance of this task family.
- [F19.04](../CAPABILITIES.md#f19-04): Measure and enforce execution budgets. Required for every instance of this task family.
- [F07.02](../CAPABILITIES.md#f07-02): Plan contractions and memory use. Required for every instance of this task family.
- [F05.03](../CAPABILITIES.md#f05-03): Compute exact observables and reduced states. Required for every instance of this task family.

**Acceptance profiles:** [A03](../ACCEPTANCE.md#a03), [A11](../ACCEPTANCE.md#a11).

**Task-specific acceptance:** Small overlaps match an independent reference; shards or slices jointly represent one computation and resource/communication measurements include gathering the requested output.

**Measurements:** strong-scaling efficiency; capacity at accuracy; communication cost; peak per-worker memory.

**Required negative case:** Replicated copies of a small state are not evidence of larger distributed-state capacity.

**Instance readiness:** Use the [instance specification template](../TASK_SPEC_TEMPLATE.md); bind fixtures, independent references, numerical/statistical thresholds, budgets, and attribution rules before execution.

<a id="t078"></a>

## T078 - Increase throughput of independent experiments or training examples

**User need:** A study needs higher throughput without changing individual outputs.

**Target users:** [P15](../REQUIREMENTS_MAP.md#p15), [P05](../REQUIREMENTS_MAP.md#p05).

**Applicability tags:** common, gate. Instance selection and conditional edges must be frozen before participant evaluation.

**Workflow stages:** execute, operate.

**Required input and constraints:** Independent circuits, seeds, parameter batches or shot partitions with a frozen serial reference.

**Required output:** An ordered reconciled result set and total-work/resource ledger.

**Required capabilities:** [C05](../CAPABILITIES.md#c05), [C09](../CAPABILITIES.md#c09), [C19](../CAPABILITIES.md#c19).

**Function traceability:**

- [F19.03](../CAPABILITIES.md#f19-03): Parallelize independent work. Required for every instance of this task family.
- [F09.02](../CAPABILITIES.md#f09-02): Batch independent data and parameters. Required for every instance of this task family.
- [F05.05](../CAPABILITIES.md#f05-05): Select and disclose execution implementation. Required for every instance of this task family.
- [F19.04](../CAPABILITIES.md#f19-04): Measure and enforce execution budgets. Required for every instance of this task family.

**Acceptance profiles:** [A03](../ACCEPTANCE.md#a03), [A11](../ACCEPTANCE.md#a11).

**Task-specific acceptance:** All independent outputs match their serial contracts; random streams, work assignment and result ordering are correct and throughput is not described as single-state capacity.

**Measurements:** completed outputs per second; scaling efficiency; memory; load imbalance.

**Required negative case:** Dropped, duplicated or accidentally correlated work units must fail accounting or statistical checks.

**Instance readiness:** Use the [instance specification template](../TASK_SPEC_TEMPLATE.md); bind fixtures, independent references, numerical/statistical thresholds, budgets, and attribution rules before execution.

<a id="t079"></a>

## T079 - Resume a computation or training run after interruption

**User need:** An operator needs a long-running study to survive interruption without changing its meaning.

**Target users:** [P15](../REQUIREMENTS_MAP.md#p15), [P05](../REQUIREMENTS_MAP.md#p05).

**Applicability tags:** common, gate. Instance selection and conditional edges must be frozen before participant evaluation.

**Workflow stages:** operate, verify.

**Required input and constraints:** A fixed checkpoint point, model/optimizer/RNG state, partition configuration and declared failure injections.

**Required output:** A resumed run and comparison against an uninterrupted control.

**Required capabilities:** [C09](../CAPABILITIES.md#c09), [C19](../CAPABILITIES.md#c19), [C20](../CAPABILITIES.md#c20).

**Function traceability:**

- [F19.05](../CAPABILITIES.md#f19-05): Recover long-running execution. Required for every instance of this task family.
- [F09.04](../CAPABILITIES.md#f09-04): Checkpoint and resume training. Required for every instance of this task family.
- [F20.04](../CAPABILITIES.md#f20-04): Package reproducible evidence. Required for every instance of this task family.
- [F20.05](../CAPABILITIES.md#f20-05): Expose inspectable errors and traces. Required for every instance of this task family.

**Acceptance profiles:** [A01](../ACCEPTANCE.md#a01), [A07](../ACCEPTANCE.md#a07), [A11](../ACCEPTANCE.md#a11).

**Task-specific acceptance:** Required state is restored and final outputs/continuation match the frozen deterministic or statistical contract; replayed work and recovery cost are counted.

**Measurements:** recovery time; lost/replayed work; checkpoint size; continuation error.

**Required negative case:** Restoring weights while losing optimizer, random or parameter-binding state is not full training recovery.

**Instance readiness:** Use the [instance specification template](../TASK_SPEC_TEMPLATE.md); bind fixtures, independent references, numerical/statistical thresholds, budgets, and attribution rules before execution.

<a id="t080"></a>

## T080 - Determine the largest completed study under real resource limits

**User need:** A user needs a capacity boundary tied to meaningful outputs and acceptable error.

**Target users:** [P15](../REQUIREMENTS_MAP.md#p15), [P07](../REQUIREMENTS_MAP.md#p07).

**Applicability tags:** gate, analog, cv. Instance selection and conditional edges must be frozen before participant evaluation.

**Workflow stages:** execute, operate, estimate.

**Required input and constraints:** A predefined scale ladder, error target, memory/wall-time budget and stop policy.

**Required output:** Completed, timed-out, out-of-memory and inaccurate outcomes with telemetry.

**Required capabilities:** [C05](../CAPABILITIES.md#c05), [C07](../CAPABILITIES.md#c07), [C19](../CAPABILITIES.md#c19).

**Function traceability:**

- [F19.01](../CAPABILITIES.md#f19-01): Select and measure compute resources. Required for every instance of this task family.
- [F19.04](../CAPABILITIES.md#f19-04): Measure and enforce execution budgets. Required for every instance of this task family.
- [F05.05](../CAPABILITIES.md#f05-05): Select and disclose execution implementation. Required for every instance of this task family.
- [F07.03](../CAPABILITIES.md#f07-03): Track numerical and approximation error. Required for every instance of this task family.

**Acceptance profiles:** [A06](../ACCEPTANCE.md#a06), [A09](../ACCEPTANCE.md#a09), [A11](../ACCEPTANCE.md#a11).

**Task-specific acceptance:** Capacity is the largest instance completing the same output/error contract within budget; resource-limit outcomes remain censored failures rather than missing rows.

**Measurements:** largest valid instance; time to target; peak host/device memory; failure boundary.

**Required negative case:** A large allocation, trivial initial state or omitted requested output cannot establish useful computational capacity.

**Instance readiness:** Use the [instance specification template](../TASK_SPEC_TEMPLATE.md); bind fixtures, independent references, numerical/statistical thresholds, budgets, and attribution rules before execution.
