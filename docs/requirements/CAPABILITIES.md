<!-- Generated from catalog.json by tools/requirements_docs.py. Do not edit directly. -->

# Capability and function dictionary

Requirements baseline 0.1. These are user-task requirements, not implemented benchmarks, executed evidence, or participant support claims. Read [the requirements map](REQUIREMENTS_MAP.md) and [acceptance rules](ACCEPTANCE.md) before using them.

Function IDs describe required behavior, not named API methods or preferred implementations. Conditional requirements are explicit on task edges.

<a id="c01"></a>

## C01 - Environment and usability

<a id="f01-01"></a>

### F01.01 - Install a reproducible environment

Resolve documented dependencies and verify executable imports in a clean supported environment.

**Required by:** [T001](tasks/j01-start-and-maintain-a-usable-project.md#t001), [T083](tasks/j17-exchange-audit-and-reproduce-work.md#t083).

<a id="f01-02"></a>

### F01.02 - Discover capabilities and limits

Query supported models, devices, operations, precision and explicit rejection conditions.

**Required by:** [T002](tasks/j01-start-and-maintain-a-usable-project.md#t002), [T020](tasks/j04-make-a-program-executable-on-a-target.md#t020), [T046](tasks/j10-run-a-recoverable-device-experiment.md#t046), [T085](tasks/j17-exchange-audit-and-reproduce-work.md#t085).

<a id="f01-03"></a>

### F01.03 - Learn and diagnose a workflow

Execute documented examples and surface actionable input, installation and runtime errors.

**Required by:** [T001](tasks/j01-start-and-maintain-a-usable-project.md#t001), [T003](tasks/j01-start-and-maintain-a-usable-project.md#t003), [T015](tasks/j03-establish-program-correctness.md#t015).

<a id="f01-04"></a>

### F01.04 - Configure execution without exposing secrets

Select accounts and execution settings while keeping credentials out of artifacts and diagnostics.

**Required by:** [T004](tasks/j01-start-and-maintain-a-usable-project.md#t004), [T047](tasks/j10-run-a-recoverable-device-experiment.md#t047).

<a id="f01-05"></a>

### F01.05 - Extend an execution path

Register a provider or computation component through a documented boundary with validated errors.

**Required by:** [T005](tasks/j01-start-and-maintain-a-usable-project.md#t005).

<a id="c02"></a>

## C02 - Static program representation

<a id="f02-01"></a>

### F02.01 - Construct and inspect programs

Represent ordered operations or structured graphs, wires/modes, registers, parameters and declared semantics.

**Required by:** [T003](tasks/j01-start-and-maintain-a-usable-project.md#t003), [T006](tasks/j02-express-an-algorithm-faithfully.md#t006), [T092](tasks/j02-express-an-algorithm-faithfully.md#t092).

<a id="f02-02"></a>

### F02.02 - Compose, invert and control subprograms

Preserve operation order, global-phase conventions and workspace contracts during program construction.

**Required by:** [T007](tasks/j02-express-an-algorithm-faithfully.md#t007), [T039](tasks/j08-answer-a-scientific-or-application-question.md#t039).

<a id="f02-03"></a>

### F02.03 - Bind and reuse parameters

Support symbolic or deferred parameters, shared occurrences, binding and repeated execution.

**Required by:** [T006](tasks/j02-express-an-algorithm-faithfully.md#t006), [T025](tasks/j05-compute-the-quantities-a-study-needs.md#t025), [T031](tasks/j07-train-and-differentiate-a-hybrid-model.md#t031).

<a id="f02-04"></a>

### F02.04 - Prepare states and encode inputs

Represent input states, isometries, encodings and associated normalization or approximation contracts.

**Required by:** [T008](tasks/j02-express-an-algorithm-faithfully.md#t008), [T040](tasks/j08-answer-a-scientific-or-application-question.md#t040), [T092](tasks/j02-express-an-algorithm-faithfully.md#t092).

<a id="f02-05"></a>

### F02.05 - Represent mixed-dimensional systems

Declare wire dimensions and reject invalid operations rather than silently treating every subsystem as a qubit.

**Required by:** [T010](tasks/j02-express-an-algorithm-faithfully.md#t010).

<a id="c03"></a>

## C03 - Classical control and adaptive execution

<a id="f03-01"></a>

### F03.01 - Measure and reset during execution

Represent destructive or nondestructive measurement and reset with explicit state semantics.

**Required by:** [T009](tasks/j02-express-an-algorithm-faithfully.md#t009), [T052](tasks/j11-study-error-corrected-computation.md#t052), [T092](tasks/j02-express-an-algorithm-faithfully.md#t092).

<a id="f03-02"></a>

### F03.02 - Condition on recorded outcomes

Preserve classical registers, predicates, branches and output mappings.

**Required by:** [T009](tasks/j02-express-an-algorithm-faithfully.md#t009), [T012](tasks/j03-establish-program-correctness.md#t012), [T013](tasks/j03-establish-program-correctness.md#t013), [T052](tasks/j11-study-error-corrected-computation.md#t052), [T057](tasks/j12-design-and-validate-physical-controls.md#t057), [T070](tasks/j14-run-a-photonic-or-continuous-variable-study.md#t070), [T092](tasks/j02-express-an-algorithm-faithfully.md#t092).

<a id="f03-03"></a>

### F03.03 - Execute bounded loops and adaptive routines

Apply declared iteration, termination and feed-forward semantics.

**Required by:** [T009](tasks/j02-express-an-algorithm-faithfully.md#t009), [T039](tasks/j08-answer-a-scientific-or-application-question.md#t039), [T092](tasks/j02-express-an-algorithm-faithfully.md#t092).

<a id="f03-04"></a>

### F03.04 - Track workspace and classical state

Allocate, reuse and release resources without leaking quantum or classical state.

**Required by:** [T007](tasks/j02-express-an-algorithm-faithfully.md#t007).

<a id="f03-05"></a>

### F03.05 - Assess execution-profile compatibility

Reject unsupported dynamic features before execution and identify any transformation or emulation.

**Required by:** [T002](tasks/j01-start-and-maintain-a-usable-project.md#t002), [T009](tasks/j02-express-an-algorithm-faithfully.md#t009), [T015](tasks/j03-establish-program-correctness.md#t015), [T020](tasks/j04-make-a-program-executable-on-a-target.md#t020), [T046](tasks/j10-run-a-recoverable-device-experiment.md#t046), [T081](tasks/j17-exchange-audit-and-reproduce-work.md#t081).

<a id="c04"></a>

## C04 - Problem and operator models

<a id="f04-01"></a>

### F04.01 - Represent states and linear operators

Specify basis, dimensions, units, Hermiticity and dense or sparse data without implicit changes.

**Required by:** [T008](tasks/j02-express-an-algorithm-faithfully.md#t008), [T010](tasks/j02-express-an-algorithm-faithfully.md#t010), [T014](tasks/j03-establish-program-correctness.md#t014), [T023](tasks/j05-compute-the-quantities-a-study-needs.md#t023), [T024](tasks/j05-compute-the-quantities-a-study-needs.md#t024), [T040](tasks/j08-answer-a-scientific-or-application-question.md#t040), [T042](tasks/j09-understand-and-reduce-execution-error.md#t042), [T058](tasks/j12-design-and-validate-physical-controls.md#t058), [T066](tasks/j14-run-a-photonic-or-continuous-variable-study.md#t066), [T082](tasks/j17-exchange-audit-and-reproduce-work.md#t082), [T088](tasks/j18-turn-observations-into-defensible-conclusions.md#t088).

<a id="f04-02"></a>

### F04.02 - Manipulate structured observables

Compose, simplify and act with Pauli sums, sparse operators and symmetry sectors.

**Required by:** [T022](tasks/j05-compute-the-quantities-a-study-needs.md#t022), [T024](tasks/j05-compute-the-quantities-a-study-needs.md#t024), [T029](tasks/j06-compute-beyond-dense-state-limits.md#t029), [T037](tasks/j08-answer-a-scientific-or-application-question.md#t037), [T051](tasks/j11-study-error-corrected-computation.md#t051), [T087](tasks/j18-turn-observations-into-defensible-conclusions.md#t087), [T091](tasks/j08-answer-a-scientific-or-application-question.md#t091).

<a id="f04-03"></a>

### F04.03 - Map fermionic and bosonic models

Preserve algebra, particle or mode ordering, encoding and truncation metadata.

**Required by:** [T036](tasks/j08-answer-a-scientific-or-application-question.md#t036), [T037](tasks/j08-answer-a-scientific-or-application-question.md#t037).

<a id="f04-04"></a>

### F04.04 - Specify scientific problem inputs

Record geometry, basis, charge, spin, boundary conditions and constants needed to reproduce a model.

**Required by:** [T036](tasks/j08-answer-a-scientific-or-application-question.md#t036), [T037](tasks/j08-answer-a-scientific-or-application-question.md#t037), [T061](tasks/j13-run-a-native-analog-study.md#t061).

<a id="f04-05"></a>

### F04.05 - Formulate objectives and constraints

Translate application variables, constraints and objectives with reversible interpretation of outputs.

**Required by:** [T038](tasks/j08-answer-a-scientific-or-application-question.md#t038), [T071](tasks/j15-solve-through-annealing-or-hybrid-optimization.md#t071).

<a id="c05"></a>

## C05 - Exact and sampled execution

<a id="f05-01"></a>

### F05.01 - Evolve a state from an explicit input

Compute ideal evolution without changing initial-state, wire-order or precision semantics.

**Required by:** [T006](tasks/j02-express-an-algorithm-faithfully.md#t006), [T010](tasks/j02-express-an-algorithm-faithfully.md#t010), [T011](tasks/j03-establish-program-correctness.md#t011), [T021](tasks/j05-compute-the-quantities-a-study-needs.md#t021).

<a id="f05-02"></a>

### F05.02 - Sample declared measurements

Return shots, outcomes and register mappings from the declared measurement process.

**Required by:** [T003](tasks/j01-start-and-maintain-a-usable-project.md#t003), [T012](tasks/j03-establish-program-correctness.md#t012), [T086](tasks/j18-turn-observations-into-defensible-conclusions.md#t086).

<a id="f05-03"></a>

### F05.03 - Compute exact observables and reduced states

Return specified amplitudes, probabilities, expectations, correlations or partial traces.

**Required by:** [T011](tasks/j03-establish-program-correctness.md#t011), [T014](tasks/j03-establish-program-correctness.md#t014), [T021](tasks/j05-compute-the-quantities-a-study-needs.md#t021), [T022](tasks/j05-compute-the-quantities-a-study-needs.md#t022), [T023](tasks/j05-compute-the-quantities-a-study-needs.md#t023), [T024](tasks/j05-compute-the-quantities-a-study-needs.md#t024), [T026](tasks/j06-compute-beyond-dense-state-limits.md#t026), [T041](tasks/j09-understand-and-reduce-execution-error.md#t041), [T067](tasks/j14-run-a-photonic-or-continuous-variable-study.md#t067), [T077](tasks/j16-scale-and-operate-a-computational-study.md#t077).

<a id="f05-04"></a>

### F05.04 - Execute adaptive and nonunitary semantics

Handle permitted measurements, reset and branches consistently with the execution profile.

**Required by:** [T009](tasks/j02-express-an-algorithm-faithfully.md#t009).

<a id="f05-05"></a>

### F05.05 - Select and disclose execution implementation

Expose actual method, device, numeric precision, batching, synchronization and fallback provenance.

**Required by:** [T002](tasks/j01-start-and-maintain-a-usable-project.md#t002), [T025](tasks/j05-compute-the-quantities-a-study-needs.md#t025), [T030](tasks/j06-compute-beyond-dense-state-limits.md#t030), [T076](tasks/j16-scale-and-operate-a-computational-study.md#t076), [T078](tasks/j16-scale-and-operate-a-computational-study.md#t078), [T080](tasks/j16-scale-and-operate-a-computational-study.md#t080), [T083](tasks/j17-exchange-audit-and-reproduce-work.md#t083), [T084](tasks/j17-exchange-audit-and-reproduce-work.md#t084).

<a id="c06"></a>

## C06 - Compilation and target constraints

<a id="f06-01"></a>

### F06.01 - Describe an executable target

Represent supported operations, connectivity, timing, calibration snapshot and target limits.

**Required by:** [T016](tasks/j04-make-a-program-executable-on-a-target.md#t016), [T017](tasks/j04-make-a-program-executable-on-a-target.md#t017), [T018](tasks/j04-make-a-program-executable-on-a-target.md#t018), [T020](tasks/j04-make-a-program-executable-on-a-target.md#t020), [T046](tasks/j10-run-a-recoverable-device-experiment.md#t046), [T057](tasks/j12-design-and-validate-physical-controls.md#t057), [T060](tasks/j12-design-and-validate-physical-controls.md#t060), [T063](tasks/j13-run-a-native-analog-study.md#t063), [T072](tasks/j15-solve-through-annealing-or-hybrid-optimization.md#t072), [T081](tasks/j17-exchange-audit-and-reproduce-work.md#t081).

<a id="f06-02"></a>

### F06.02 - Synthesize and decompose operations

Lower unitary, state-preparation and structured operations within declared error and workspace bounds.

**Required by:** [T007](tasks/j02-express-an-algorithm-faithfully.md#t007), [T008](tasks/j02-express-an-algorithm-faithfully.md#t008), [T016](tasks/j04-make-a-program-executable-on-a-target.md#t016).

<a id="f06-03"></a>

### F06.03 - Optimize while preserving semantics

Rewrite a program with verified ordering, phase, parameters and classical behavior.

**Required by:** [T013](tasks/j03-establish-program-correctness.md#t013), [T016](tasks/j04-make-a-program-executable-on-a-target.md#t016), [T017](tasks/j04-make-a-program-executable-on-a-target.md#t017), [T019](tasks/j04-make-a-program-executable-on-a-target.md#t019), [T092](tasks/j02-express-an-algorithm-faithfully.md#t092).

<a id="f06-04"></a>

### F06.04 - Place, route and recover logical outputs

Respect connectivity and track initial/final logical-to-physical permutations.

**Required by:** [T017](tasks/j04-make-a-program-executable-on-a-target.md#t017), [T019](tasks/j04-make-a-program-executable-on-a-target.md#t019), [T049](tasks/j10-run-a-recoverable-device-experiment.md#t049).

<a id="f06-05"></a>

### F06.05 - Schedule and account for resources

Respect declared durations, alignments, dependencies and resource conflicts.

**Required by:** [T018](tasks/j04-make-a-program-executable-on-a-target.md#t018), [T055](tasks/j11-study-error-corrected-computation.md#t055), [T057](tasks/j12-design-and-validate-physical-controls.md#t057).

<a id="f06-06"></a>

### F06.06 - Expose compile tradeoffs and diagnostics

Record budgets, seeds, failed constraints and quality/time tradeoffs without substituting an unrelated task.

**Required by:** [T019](tasks/j04-make-a-program-executable-on-a-target.md#t019), [T020](tasks/j04-make-a-program-executable-on-a-target.md#t020).

<a id="c07"></a>

## C07 - Approximate and structured simulation

<a id="f07-01"></a>

### F07.01 - Control representation and truncation

Select MPS, tensor networks or other structured methods with explicit approximation settings.

**Required by:** [T026](tasks/j06-compute-beyond-dense-state-limits.md#t026), [T027](tasks/j06-compute-beyond-dense-state-limits.md#t027), [T030](tasks/j06-compute-beyond-dense-state-limits.md#t030).

<a id="f07-02"></a>

### F07.02 - Plan contractions and memory use

Search, cache and execute contraction or slicing plans under a declared resource budget.

**Required by:** [T028](tasks/j06-compute-beyond-dense-state-limits.md#t028), [T077](tasks/j16-scale-and-operate-a-computational-study.md#t077).

<a id="f07-03"></a>

### F07.03 - Track numerical and approximation error

Preserve normalization, discarded weights, truncation and observable-error evidence.

**Required by:** [T026](tasks/j06-compute-beyond-dense-state-limits.md#t026), [T027](tasks/j06-compute-beyond-dense-state-limits.md#t027), [T029](tasks/j06-compute-beyond-dense-state-limits.md#t029), [T030](tasks/j06-compute-beyond-dense-state-limits.md#t030), [T068](tasks/j14-run-a-photonic-or-continuous-variable-study.md#t068), [T080](tasks/j16-scale-and-operate-a-computational-study.md#t080).

<a id="f07-04"></a>

### F07.04 - Simulate structured evolution

Evolve low-entanglement, symmetry-restricted or time-dependent systems with declared discretization.

**Required by:** [T029](tasks/j06-compute-beyond-dense-state-limits.md#t029), [T037](tasks/j08-answer-a-scientific-or-application-question.md#t037), [T062](tasks/j13-run-a-native-analog-study.md#t062).

<a id="f07-05"></a>

### F07.05 - Return outputs without accidental densification

Compute specified local or sampled outputs without materializing an unnecessary exponential state.

**Required by:** [T026](tasks/j06-compute-beyond-dense-state-limits.md#t026), [T028](tasks/j06-compute-beyond-dense-state-limits.md#t028), [T030](tasks/j06-compute-beyond-dense-state-limits.md#t030).

<a id="c08"></a>

## C08 - Differentiation

<a id="f08-01"></a>

### F08.01 - Compute first derivatives

Differentiate declared outputs with respect to real parameters with explicit complex-value conventions.

**Required by:** [T031](tasks/j07-train-and-differentiate-a-hybrid-model.md#t031), [T032](tasks/j07-train-and-differentiate-a-hybrid-model.md#t032).

<a id="f08-02"></a>

### F08.02 - Compute Jacobians and derivative products

Support vector outputs, JVPs or VJPs with documented shapes and parameter sharing.

**Required by:** [T031](tasks/j07-train-and-differentiate-a-hybrid-model.md#t031), [T034](tasks/j07-train-and-differentiate-a-hybrid-model.md#t034).

<a id="f08-03"></a>

### F08.03 - Compute higher-order derivatives

Expose supported Hessians or Hessian-vector products and reject unsupported paths.

**Required by:** [T034](tasks/j07-train-and-differentiate-a-hybrid-model.md#t034).

<a id="f08-04"></a>

### F08.04 - Estimate derivatives with finite shots

Account for sampling variance, bias, shifted evaluations and shot allocation.

**Required by:** [T035](tasks/j07-train-and-differentiate-a-hybrid-model.md#t035).

<a id="f08-05"></a>

### F08.05 - Disclose derivative method and cost

Record analytic, automatic, adjoint, shift or finite-difference method, calls, memory and fallback.

**Required by:** [T031](tasks/j07-train-and-differentiate-a-hybrid-model.md#t031), [T033](tasks/j07-train-and-differentiate-a-hybrid-model.md#t033), [T034](tasks/j07-train-and-differentiate-a-hybrid-model.md#t034), [T035](tasks/j07-train-and-differentiate-a-hybrid-model.md#t035), [T084](tasks/j17-exchange-audit-and-reproduce-work.md#t084).

<a id="c09"></a>

## C09 - Hybrid training

<a id="f09-01"></a>

### F09.01 - Integrate quantum and classical models

Preserve gradients, dtype, device and parameter ownership through a hybrid computation.

**Required by:** [T032](tasks/j07-train-and-differentiate-a-hybrid-model.md#t032), [T034](tasks/j07-train-and-differentiate-a-hybrid-model.md#t034).

<a id="f09-02"></a>

### F09.02 - Batch independent data and parameters

Define broadcasting, minibatches, multiple observables and distinct parameter sets.

**Required by:** [T025](tasks/j05-compute-the-quantities-a-study-needs.md#t025), [T032](tasks/j07-train-and-differentiate-a-hybrid-model.md#t032), [T078](tasks/j16-scale-and-operate-a-computational-study.md#t078).

<a id="f09-03"></a>

### F09.03 - Optimize and evaluate reproducibly

Track objectives, constraints, seeds, datasets, convergence and held-out evaluation.

**Required by:** [T032](tasks/j07-train-and-differentiate-a-hybrid-model.md#t032), [T033](tasks/j07-train-and-differentiate-a-hybrid-model.md#t033), [T091](tasks/j08-answer-a-scientific-or-application-question.md#t091).

<a id="f09-04"></a>

### F09.04 - Checkpoint and resume training

Save model, optimizer, random state and relevant execution state for a controlled continuation.

**Required by:** [T079](tasks/j16-scale-and-operate-a-computational-study.md#t079).

<a id="f09-05"></a>

### F09.05 - Budget training and adaptive search

Account for all objective/gradient calls, shots, preprocessing and parameter-search cost.

**Required by:** [T033](tasks/j07-train-and-differentiate-a-hybrid-model.md#t033), [T035](tasks/j07-train-and-differentiate-a-hybrid-model.md#t035), [T036](tasks/j08-answer-a-scientific-or-application-question.md#t036), [T038](tasks/j08-answer-a-scientific-or-application-question.md#t038), [T059](tasks/j12-design-and-validate-physical-controls.md#t059), [T065](tasks/j13-run-a-native-analog-study.md#t065), [T075](tasks/j15-solve-through-annealing-or-hybrid-optimization.md#t075), [T091](tasks/j08-answer-a-scientific-or-application-question.md#t091).

<a id="c10"></a>

## C10 - Noise and open-system modeling

<a id="f10-01"></a>

### F10.01 - Specify channels and readout models

Represent noise ordering, locality, units, physical constraints and classical confusion.

**Required by:** [T014](tasks/j03-establish-program-correctness.md#t014), [T041](tasks/j09-understand-and-reduce-execution-error.md#t041), [T043](tasks/j09-understand-and-reduce-execution-error.md#t043).

<a id="f10-02"></a>

### F10.02 - Execute noisy density or trajectory evolution

Compute mixed-state evolution with explicit integration or trajectory settings.

**Required by:** [T014](tasks/j03-establish-program-correctness.md#t014), [T041](tasks/j09-understand-and-reduce-execution-error.md#t041).

<a id="f10-03"></a>

### F10.03 - Model time-dependent open systems

Represent Hamiltonians, dissipators, frames, units and solver tolerances.

**Required by:** [T042](tasks/j09-understand-and-reduce-execution-error.md#t042), [T058](tasks/j12-design-and-validate-physical-controls.md#t058).

<a id="f10-04"></a>

### F10.04 - Apply and assess error mitigation

Track calibration, assumptions, raw/mitigated outputs, variance and extra executions.

**Required by:** [T043](tasks/j09-understand-and-reduce-execution-error.md#t043), [T044](tasks/j09-understand-and-reduce-execution-error.md#t044).

<a id="f10-05"></a>

### F10.05 - Validate noise predictions out of sample

Evaluate a frozen noise or device model against held-out measurements with drift and validity limits.

**Required by:** [T045](tasks/j09-understand-and-reduce-execution-error.md#t045), [T050](tasks/j10-run-a-recoverable-device-experiment.md#t050).

<a id="c11"></a>

## C11 - Job and experiment orchestration

<a id="f11-01"></a>

### F11.01 - Discover and select execution targets

Inspect availability and supported execution profiles without claiming device access from an adapter alone.

**Required by:** [T004](tasks/j01-start-and-maintain-a-usable-project.md#t004), [T046](tasks/j10-run-a-recoverable-device-experiment.md#t046), [T063](tasks/j13-run-a-native-analog-study.md#t063).

<a id="f11-02"></a>

### F11.02 - Prepare a budgeted experiment

Construct circuit or program batches with shot, cost, time and resource estimates or explicit unknowns.

**Required by:** [T004](tasks/j01-start-and-maintain-a-usable-project.md#t004), [T044](tasks/j09-understand-and-reduce-execution-error.md#t044), [T047](tasks/j10-run-a-recoverable-device-experiment.md#t047), [T087](tasks/j18-turn-observations-into-defensible-conclusions.md#t087).

<a id="f11-03"></a>

### F11.03 - Submit and manage asynchronous jobs

Submit only with explicit authorization and retain identities, status, cancellation and provider errors.

**Required by:** [T004](tasks/j01-start-and-maintain-a-usable-project.md#t004), [T047](tasks/j10-run-a-recoverable-device-experiment.md#t047), [T048](tasks/j10-run-a-recoverable-device-experiment.md#t048).

<a id="f11-04"></a>

### F11.04 - Recover and reconcile partial work

Retrieve prior jobs and handle retries, partial failures and duplicate-submission hazards.

**Required by:** [T015](tasks/j03-establish-program-correctness.md#t015), [T048](tasks/j10-run-a-recoverable-device-experiment.md#t048).

<a id="f11-05"></a>

### F11.05 - Preserve acquisition and result provenance

Bind results to programs, parameter bindings, mappings, shots, acquisition times and target metadata.

**Required by:** [T005](tasks/j01-start-and-maintain-a-usable-project.md#t005), [T045](tasks/j09-understand-and-reduce-execution-error.md#t045), [T047](tasks/j10-run-a-recoverable-device-experiment.md#t047), [T048](tasks/j10-run-a-recoverable-device-experiment.md#t048), [T049](tasks/j10-run-a-recoverable-device-experiment.md#t049), [T050](tasks/j10-run-a-recoverable-device-experiment.md#t050), [T052](tasks/j11-study-error-corrected-computation.md#t052), [T060](tasks/j12-design-and-validate-physical-controls.md#t060), [T064](tasks/j13-run-a-native-analog-study.md#t064), [T073](tasks/j15-solve-through-annealing-or-hybrid-optimization.md#t073).

<a id="c12"></a>

## C12 - Estimation and result analysis

<a id="f12-01"></a>

### F12.01 - Validate and normalize result records

Distinguish counts, samples, probabilities, quasi-probabilities and missing outcomes with explicit bit/mode mappings.

**Required by:** [T012](tasks/j03-establish-program-correctness.md#t012), [T017](tasks/j04-make-a-program-executable-on-a-target.md#t017), [T043](tasks/j09-understand-and-reduce-execution-error.md#t043), [T049](tasks/j10-run-a-recoverable-device-experiment.md#t049), [T053](tasks/j11-study-error-corrected-computation.md#t053), [T064](tasks/j13-run-a-native-analog-study.md#t064), [T069](tasks/j14-run-a-photonic-or-continuous-variable-study.md#t069), [T082](tasks/j17-exchange-audit-and-reproduce-work.md#t082), [T086](tasks/j18-turn-observations-into-defensible-conclusions.md#t086), [T089](tasks/j18-turn-observations-into-defensible-conclusions.md#t089).

<a id="f12-02"></a>

### F12.02 - Estimate quantities with uncertainty

Use declared estimators, confidence or credible intervals and finite-sample assumptions.

**Required by:** [T012](tasks/j03-establish-program-correctness.md#t012), [T035](tasks/j07-train-and-differentiate-a-hybrid-model.md#t035), [T036](tasks/j08-answer-a-scientific-or-application-question.md#t036), [T039](tasks/j08-answer-a-scientific-or-application-question.md#t039), [T040](tasks/j08-answer-a-scientific-or-application-question.md#t040), [T041](tasks/j09-understand-and-reduce-execution-error.md#t041), [T043](tasks/j09-understand-and-reduce-execution-error.md#t043), [T044](tasks/j09-understand-and-reduce-execution-error.md#t044), [T045](tasks/j09-understand-and-reduce-execution-error.md#t045), [T050](tasks/j10-run-a-recoverable-device-experiment.md#t050), [T054](tasks/j11-study-error-corrected-computation.md#t054), [T062](tasks/j13-run-a-native-analog-study.md#t062), [T064](tasks/j13-run-a-native-analog-study.md#t064), [T067](tasks/j14-run-a-photonic-or-continuous-variable-study.md#t067), [T069](tasks/j14-run-a-photonic-or-continuous-variable-study.md#t069), [T073](tasks/j15-solve-through-annealing-or-hybrid-optimization.md#t073), [T086](tasks/j18-turn-observations-into-defensible-conclusions.md#t086), [T087](tasks/j18-turn-observations-into-defensible-conclusions.md#t087), [T088](tasks/j18-turn-observations-into-defensible-conclusions.md#t088), [T089](tasks/j18-turn-observations-into-defensible-conclusions.md#t089), [T091](tasks/j08-answer-a-scientific-or-application-question.md#t091).

<a id="f12-03"></a>

### F12.03 - Plan and combine measurements

Group compatible observables and allocate shots while preserving correlations and total cost.

**Required by:** [T022](tasks/j05-compute-the-quantities-a-study-needs.md#t022), [T035](tasks/j07-train-and-differentiate-a-hybrid-model.md#t035), [T044](tasks/j09-understand-and-reduce-execution-error.md#t044), [T087](tasks/j18-turn-observations-into-defensible-conclusions.md#t087), [T089](tasks/j18-turn-observations-into-defensible-conclusions.md#t089).

<a id="f12-04"></a>

### F12.04 - Reconstruct and diagnose states or processes

Evaluate tomography, shadows or fitted models under declared identifiability and validation assumptions.

**Required by:** [T088](tasks/j18-turn-observations-into-defensible-conclusions.md#t088), [T089](tasks/j18-turn-observations-into-defensible-conclusions.md#t089), [T090](tasks/j18-turn-observations-into-defensible-conclusions.md#t090).

<a id="f12-05"></a>

### F12.05 - Export interpretable analysis

Preserve units, uncertainty, failed fits, raw data, transformations and machine-readable diagnostics.

**Required by:** [T003](tasks/j01-start-and-maintain-a-usable-project.md#t003), [T023](tasks/j05-compute-the-quantities-a-study-needs.md#t023), [T037](tasks/j08-answer-a-scientific-or-application-question.md#t037), [T058](tasks/j12-design-and-validate-physical-controls.md#t058), [T069](tasks/j14-run-a-photonic-or-continuous-variable-study.md#t069), [T074](tasks/j15-solve-through-annealing-or-hybrid-optimization.md#t074), [T083](tasks/j17-exchange-audit-and-reproduce-work.md#t083), [T086](tasks/j18-turn-observations-into-defensible-conclusions.md#t086), [T088](tasks/j18-turn-observations-into-defensible-conclusions.md#t088), [T090](tasks/j18-turn-observations-into-defensible-conclusions.md#t090).

<a id="c13"></a>

## C13 - Scientific and application workflows

<a id="f13-01"></a>

### F13.01 - Solve energy or spectral problems

Compute a declared ground/excited-state or spectral target with a specified reference and total energy convention.

**Required by:** [T033](tasks/j07-train-and-differentiate-a-hybrid-model.md#t033), [T036](tasks/j08-answer-a-scientific-or-application-question.md#t036).

<a id="f13-02"></a>

### F13.02 - Study dynamics and correlations

Compute time-dependent observables of a fixed physical model with controlled errors.

**Required by:** [T029](tasks/j06-compute-beyond-dense-state-limits.md#t029), [T037](tasks/j08-answer-a-scientific-or-application-question.md#t037), [T042](tasks/j09-understand-and-reduce-execution-error.md#t042).

<a id="f13-03"></a>

### F13.03 - Solve optimization instances

Return feasible decoded solutions, objective values and a declared optimality or quality reference.

**Required by:** [T038](tasks/j08-answer-a-scientific-or-application-question.md#t038), [T065](tasks/j13-run-a-native-analog-study.md#t065), [T071](tasks/j15-solve-through-annealing-or-hybrid-optimization.md#t071), [T074](tasks/j15-solve-through-annealing-or-hybrid-optimization.md#t074), [T075](tasks/j15-solve-through-annealing-or-hybrid-optimization.md#t075).

<a id="f13-04"></a>

### F13.04 - Estimate algorithmic quantities

Implement phase, amplitude or linear-algebra workflows with complete oracle and state-preparation costs.

**Required by:** [T039](tasks/j08-answer-a-scientific-or-application-question.md#t039), [T040](tasks/j08-answer-a-scientific-or-application-question.md#t040), [T055](tasks/j11-study-error-corrected-computation.md#t055).

<a id="f13-05"></a>

### F13.05 - Evaluate predictive or kernel methods

Use fixed datasets, splits, preprocessing, regularization and classical comparison protocols.

**Required by:** [T091](tasks/j08-answer-a-scientific-or-application-question.md#t091).

<a id="c14"></a>

## C14 - Error correction and fault tolerance

<a id="f14-01"></a>

### F14.01 - Specify codes and logical observables

Record checks, logical operators, geometry, boundary and commutation conventions.

**Required by:** [T051](tasks/j11-study-error-corrected-computation.md#t051).

<a id="f14-02"></a>

### F14.02 - Build repeated error-correction experiments

Preserve syndrome rounds, reset, noise locations, detector events and observable labels.

**Required by:** [T052](tasks/j11-study-error-corrected-computation.md#t052), [T053](tasks/j11-study-error-corrected-computation.md#t053).

<a id="f14-03"></a>

### F14.03 - Construct and sample detector error models

Declare approximation, correlation handling and event-to-observable relationships.

**Required by:** [T053](tasks/j11-study-error-corrected-computation.md#t053), [T054](tasks/j11-study-error-corrected-computation.md#t054).

<a id="f14-04"></a>

### F14.04 - Decode and estimate logical outcomes

Track decoder assumptions, latency, failure probabilities, confidence and unmatched syndromes.

**Required by:** [T054](tasks/j11-study-error-corrected-computation.md#t054).

<a id="f14-05"></a>

### F14.05 - Compile logical operations and estimate resources

State logical protocol, error budget, code assumptions, physical resources and extrapolation boundaries.

**Required by:** [T055](tasks/j11-study-error-corrected-computation.md#t055).

<a id="c15"></a>

## C15 - Pulse and control

<a id="f15-01"></a>

### F15.01 - Represent waveforms and channels

Define samples, units, frames, ports, amplitude limits and device calibration associations.

**Required by:** [T056](tasks/j12-design-and-validate-physical-controls.md#t056), [T059](tasks/j12-design-and-validate-physical-controls.md#t059).

<a id="f15-02"></a>

### F15.02 - Schedule physical controls

Respect clock, alignment, channel conflicts and simultaneous-control constraints.

**Required by:** [T018](tasks/j04-make-a-program-executable-on-a-target.md#t018), [T057](tasks/j12-design-and-validate-physical-controls.md#t057).

<a id="f15-03"></a>

### F15.03 - Simulate driven dynamics

Represent rotating frames, Hamiltonians and dissipators with controlled time integration.

**Required by:** [T042](tasks/j09-understand-and-reduce-execution-error.md#t042), [T058](tasks/j12-design-and-validate-physical-controls.md#t058), [T059](tasks/j12-design-and-validate-physical-controls.md#t059).

<a id="f15-04"></a>

### F15.04 - Calibrate or optimize controls

Use a fixed objective, evaluation budget, held-out validation and explicit model/device execution provenance.

**Required by:** [T059](tasks/j12-design-and-validate-physical-controls.md#t059).

<a id="f15-05"></a>

### F15.05 - Preserve gate-to-control correspondence

Track calibrated gate realizations and reject stale or incompatible pulse definitions.

**Required by:** [T056](tasks/j12-design-and-validate-physical-controls.md#t056), [T060](tasks/j12-design-and-validate-physical-controls.md#t060).

<a id="c16"></a>

## C16 - Analog quantum programs

<a id="f16-01"></a>

### F16.01 - Describe geometry and interactions

Define sites, species, boundaries, interactions, units and initialization.

**Required by:** [T061](tasks/j13-run-a-native-analog-study.md#t061), [T062](tasks/j13-run-a-native-analog-study.md#t062), [T065](tasks/j13-run-a-native-analog-study.md#t065).

<a id="f16-02"></a>

### F16.02 - Define time-dependent controls

Represent schedules, fields, interpolation, local/global control and hardware limits.

**Required by:** [T061](tasks/j13-run-a-native-analog-study.md#t061), [T063](tasks/j13-run-a-native-analog-study.md#t063), [T065](tasks/j13-run-a-native-analog-study.md#t065).

<a id="f16-03"></a>

### F16.03 - Simulate and measure analog evolution

Return specified observables or samples with disclosed approximation and solver settings.

**Required by:** [T062](tasks/j13-run-a-native-analog-study.md#t062), [T065](tasks/j13-run-a-native-analog-study.md#t065).

<a id="f16-04"></a>

### F16.04 - Translate to a compatible analog device

Validate geometry and control constraints and report rounding or unsupported features.

**Required by:** [T063](tasks/j13-run-a-native-analog-study.md#t063).

<a id="f16-05"></a>

### F16.05 - Track losses and analog experiment context

Retain loading, atom loss, postselection, denominators and acquisition provenance.

**Required by:** [T064](tasks/j13-run-a-native-analog-study.md#t064).

<a id="c17"></a>

## C17 - Photonic and continuous-variable programs

<a id="f17-01"></a>

### F17.01 - Represent modes and conventions

Declare mode order, commutation and quadrature conventions, units and input states.

**Required by:** [T066](tasks/j14-run-a-photonic-or-continuous-variable-study.md#t066), [T067](tasks/j14-run-a-photonic-or-continuous-variable-study.md#t067).

<a id="f17-02"></a>

### F17.02 - Evolve Gaussian and non-Gaussian processes

Represent Gaussian transformations and required non-Gaussian operations without silent substitution.

**Required by:** [T066](tasks/j14-run-a-photonic-or-continuous-variable-study.md#t066), [T067](tasks/j14-run-a-photonic-or-continuous-variable-study.md#t067), [T068](tasks/j14-run-a-photonic-or-continuous-variable-study.md#t068).

<a id="f17-03"></a>

### F17.03 - Control Fock-space approximation

Declare cutoff, discarded probability, normalization and convergence evidence.

**Required by:** [T068](tasks/j14-run-a-photonic-or-continuous-variable-study.md#t068).

<a id="f17-04"></a>

### F17.04 - Sample photonic measurements

Define homodyne, heterodyne or photon-counting outcomes, losses and postselection.

**Required by:** [T069](tasks/j14-run-a-photonic-or-continuous-variable-study.md#t069).

<a id="f17-05"></a>

### F17.05 - Compile or adapt mode programs

Preserve interferometer, feed-forward, target constraints and observable semantics.

**Required by:** [T070](tasks/j14-run-a-photonic-or-continuous-variable-study.md#t070).

<a id="c18"></a>

## C18 - Annealing and optimization models

<a id="f18-01"></a>

### F18.01 - Represent quadratic and constrained models

Declare binary/spin domains, coefficients, offsets, constraints and penalty construction.

**Required by:** [T071](tasks/j15-solve-through-annealing-or-hybrid-optimization.md#t071), [T072](tasks/j15-solve-through-annealing-or-hybrid-optimization.md#t072), [T074](tasks/j15-solve-through-annealing-or-hybrid-optimization.md#t074).

<a id="f18-02"></a>

### F18.02 - Embed and scale for a target

Track chains, coefficient scaling, topology and decoding back to logical variables.

**Required by:** [T072](tasks/j15-solve-through-annealing-or-hybrid-optimization.md#t072).

<a id="f18-03"></a>

### F18.03 - Execute declared sampling schedules

Record anneal schedules, gauges, reads, initialization and solver type.

**Required by:** [T073](tasks/j15-solve-through-annealing-or-hybrid-optimization.md#t073).

<a id="f18-04"></a>

### F18.04 - Decode and validate candidate solutions

Report feasibility, chain breaks, objective reconstruction and any repair or postprocessing.

**Required by:** [T038](tasks/j08-answer-a-scientific-or-application-question.md#t038), [T072](tasks/j15-solve-through-annealing-or-hybrid-optimization.md#t072), [T073](tasks/j15-solve-through-annealing-or-hybrid-optimization.md#t073), [T074](tasks/j15-solve-through-annealing-or-hybrid-optimization.md#t074).

<a id="f18-05"></a>

### F18.05 - Account for hybrid optimization cost

Distinguish classical, quantum and hybrid work and state access to reference optima.

**Required by:** [T075](tasks/j15-solve-through-annealing-or-hybrid-optimization.md#t075).

<a id="c19"></a>

## C19 - Resource scaling and operations

<a id="f19-01"></a>

### F19.01 - Select and measure compute resources

Record CPU/GPU/accelerator allocation, threads, precision, memory and device synchronization.

**Required by:** [T076](tasks/j16-scale-and-operate-a-computational-study.md#t076), [T080](tasks/j16-scale-and-operate-a-computational-study.md#t080).

<a id="f19-02"></a>

### F19.02 - Partition states or tensor computations

Specify sharding, replication, contraction slicing, communication and output gathering.

**Required by:** [T028](tasks/j06-compute-beyond-dense-state-limits.md#t028), [T077](tasks/j16-scale-and-operate-a-computational-study.md#t077).

<a id="f19-03"></a>

### F19.03 - Parallelize independent work

Batch data, shots, observables or parameter points without confusing throughput with state capacity.

**Required by:** [T022](tasks/j05-compute-the-quantities-a-study-needs.md#t022), [T025](tasks/j05-compute-the-quantities-a-study-needs.md#t025), [T032](tasks/j07-train-and-differentiate-a-hybrid-model.md#t032), [T078](tasks/j16-scale-and-operate-a-computational-study.md#t078).

<a id="f19-04"></a>

### F19.04 - Measure and enforce execution budgets

Track wall time, memory, device time, communication and censored resource-limit outcomes.

**Required by:** [T019](tasks/j04-make-a-program-executable-on-a-target.md#t019), [T021](tasks/j05-compute-the-quantities-a-study-needs.md#t021), [T024](tasks/j05-compute-the-quantities-a-study-needs.md#t024), [T027](tasks/j06-compute-beyond-dense-state-limits.md#t027), [T028](tasks/j06-compute-beyond-dense-state-limits.md#t028), [T030](tasks/j06-compute-beyond-dense-state-limits.md#t030), [T039](tasks/j08-answer-a-scientific-or-application-question.md#t039), [T054](tasks/j11-study-error-corrected-computation.md#t054), [T068](tasks/j14-run-a-photonic-or-continuous-variable-study.md#t068), [T075](tasks/j15-solve-through-annealing-or-hybrid-optimization.md#t075), [T076](tasks/j16-scale-and-operate-a-computational-study.md#t076), [T077](tasks/j16-scale-and-operate-a-computational-study.md#t077), [T078](tasks/j16-scale-and-operate-a-computational-study.md#t078), [T080](tasks/j16-scale-and-operate-a-computational-study.md#t080).

<a id="f19-05"></a>

### F19.05 - Recover long-running execution

Record checkpoints, failure injection, recovery state and correctness after restart.

**Required by:** [T079](tasks/j16-scale-and-operate-a-computational-study.md#t079).

<a id="c20"></a>

## C20 - Interoperability and reproducibility

<a id="f20-01"></a>

### F20.01 - Import and export declared formats

Declare format versions and preserve or explicitly reject program features and metadata.

**Required by:** [T056](tasks/j12-design-and-validate-physical-controls.md#t056), [T070](tasks/j14-run-a-photonic-or-continuous-variable-study.md#t070), [T081](tasks/j17-exchange-audit-and-reproduce-work.md#t081).

<a id="f20-02"></a>

### F20.02 - Normalize conventions across boundaries

Convert wire order, dimensions, measurement mapping, units and phase/parameter conventions explicitly.

**Required by:** [T005](tasks/j01-start-and-maintain-a-usable-project.md#t005), [T006](tasks/j02-express-an-algorithm-faithfully.md#t006), [T007](tasks/j02-express-an-algorithm-faithfully.md#t007), [T008](tasks/j02-express-an-algorithm-faithfully.md#t008), [T010](tasks/j02-express-an-algorithm-faithfully.md#t010), [T011](tasks/j03-establish-program-correctness.md#t011), [T016](tasks/j04-make-a-program-executable-on-a-target.md#t016), [T049](tasks/j10-run-a-recoverable-device-experiment.md#t049), [T051](tasks/j11-study-error-corrected-computation.md#t051), [T066](tasks/j14-run-a-photonic-or-continuous-variable-study.md#t066), [T070](tasks/j14-run-a-photonic-or-continuous-variable-study.md#t070), [T081](tasks/j17-exchange-audit-and-reproduce-work.md#t081), [T082](tasks/j17-exchange-audit-and-reproduce-work.md#t082), [T092](tasks/j02-express-an-algorithm-faithfully.md#t092).

<a id="f20-03"></a>

### F20.03 - Round-trip artifacts without hidden loss

Compare semantics, retain conversion diagnostics and identify irrecoverable information loss.

**Required by:** [T013](tasks/j03-establish-program-correctness.md#t013), [T053](tasks/j11-study-error-corrected-computation.md#t053), [T070](tasks/j14-run-a-photonic-or-continuous-variable-study.md#t070), [T082](tasks/j17-exchange-audit-and-reproduce-work.md#t082), [T085](tasks/j17-exchange-audit-and-reproduce-work.md#t085).

<a id="f20-04"></a>

### F20.04 - Package reproducible evidence

Hash inputs and retain environment, versions, seeds, raw results, settings and execution dependency chains.

**Required by:** [T001](tasks/j01-start-and-maintain-a-usable-project.md#t001), [T011](tasks/j03-establish-program-correctness.md#t011), [T018](tasks/j04-make-a-program-executable-on-a-target.md#t018), [T045](tasks/j09-understand-and-reduce-execution-error.md#t045), [T050](tasks/j10-run-a-recoverable-device-experiment.md#t050), [T055](tasks/j11-study-error-corrected-computation.md#t055), [T060](tasks/j12-design-and-validate-physical-controls.md#t060), [T076](tasks/j16-scale-and-operate-a-computational-study.md#t076), [T079](tasks/j16-scale-and-operate-a-computational-study.md#t079), [T083](tasks/j17-exchange-audit-and-reproduce-work.md#t083), [T084](tasks/j17-exchange-audit-and-reproduce-work.md#t084), [T085](tasks/j17-exchange-audit-and-reproduce-work.md#t085), [T090](tasks/j18-turn-observations-into-defensible-conclusions.md#t090).

<a id="f20-05"></a>

### F20.05 - Expose inspectable errors and traces

Retain stage-specific diagnostics and prevent silent fallback, hidden postselection or successful-looking partial results.

**Required by:** [T002](tasks/j01-start-and-maintain-a-usable-project.md#t002), [T004](tasks/j01-start-and-maintain-a-usable-project.md#t004), [T005](tasks/j01-start-and-maintain-a-usable-project.md#t005), [T013](tasks/j03-establish-program-correctness.md#t013), [T015](tasks/j03-establish-program-correctness.md#t015), [T027](tasks/j06-compute-beyond-dense-state-limits.md#t027), [T048](tasks/j10-run-a-recoverable-device-experiment.md#t048), [T079](tasks/j16-scale-and-operate-a-computational-study.md#t079), [T084](tasks/j17-exchange-audit-and-reproduce-work.md#t084), [T085](tasks/j17-exchange-audit-and-reproduce-work.md#t085), [T090](tasks/j18-turn-observations-into-defensible-conclusions.md#t090).
