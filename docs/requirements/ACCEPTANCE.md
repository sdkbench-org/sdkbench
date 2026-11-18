# Acceptance contracts

## Requirements versus executable instances

Task cards define family-level outcomes and acceptance criteria. They become runnable benchmarks only when an instance supplies immutable fixtures, an independent reference or reference procedure, concrete error/statistical thresholds, resource budgets and an evaluation procedure. A row containing the words "within budget" is not permission to select that budget after observing results.

Every executable instance must complete the [instance template](TASK_SPEC_TEMPLATE.md). Missing reference provenance, tolerance justification, applicability conditions or primary success criteria blocks instance readiness. All acceptance profiles used by a task apply together; selecting a faster implementation does not waive its output or scientific contract.

## Universal gates

1. **Identity and semantics:** Check input/output identity, dimensions, mappings, units, parameter bindings, initial-state assumptions and declared approximations.
2. **Correctness and validity:** Apply the appropriate independent oracle, statistical contract and target/application constraints. Do not time-rank incorrect outputs.
3. **Budget and provenance:** Record the actual execution chain and whether the complete output was obtained under the frozen budget.
4. **Quality and efficiency:** Compare accepted results with matched output/error contracts; retain failures and censored runs in completion reporting.

A result must have an explicit outcome such as `accepted`, `incorrect`, `unsupported`, `invalid_input`, `infeasible_target`, `timeout`, `out_of_memory`, `execution_error`, `inconclusive`, `not_measured` or `not_applicable`. These are proposed future study outcomes, not a change to the current runtime schema. Non-applicability needs a predeclared rationale. Inconclusive evidence is not acceptance. Failed/incomplete results cannot be encoded as a zero-cost successful output.

<a id="a01"></a>

## A01 - Reproducible environment and operational behavior

Freeze supported OS/architecture/interpreter, installation source, dependency resolution policy, documented steps and network/cache boundaries. Test a clean environment and explicit unsupported or broken environments. Require executable imports plus a checked result, not just successful package installation. Record logs, versions, interventions, bytes, disk use and elapsed time if measured.

For documentation/usability tasks, publish the script or participant procedure, prerequisites, assistance rules and completion rubric. Actual unassisted-success claims require a suitably designed user study; a maintainer replay only establishes procedural reproducibility. Configure dummy credentials and stubs for authorization tests, and require zero unauthorized submissions and zero dummy-secret disclosures in the declared artifact/log surface.

<a id="a02"></a>

## A02 - Exact semantics and algebraic correctness

Freeze basis/index order, dimensions, parameter identity, units, register mapping, control/target order and allowed global-phase rules. Use exhaustive truth tables, independent algebra or full small-instance operators where feasible. Include asymmetric, complex-valued and interference fixtures. A global phase that is irrelevant for an isolated unitary can become a relative phase when controlled; the enclosing task decides which equivalences are valid.

Dynamic and measurement-based programs require branch/instrument semantics, causal dependencies, reset and byproduct/correction handling. Observable probabilities from one input are not sufficient to establish a coherent operation's correctness. Arithmetic/oracle tasks also verify workspace cleanup, reversibility and the specified input domain. A claimed code distance or optimum needs a reference/proof for the evaluated fixture, not a label supplied by the participant.

<a id="a03"></a>

## A03 - Numerical equivalence and physical invariants

Each instance names an error metric, absolute/relative tolerances, precision and a reference whose uncertainty is smaller than the permitted discrepancy. Possible metrics include phase-aligned state error, trace distance, operator norm and observable error. Choose the metric from the output contract; do not require an exponential full-state output for a task asking only for local observables.

For mixed elementwise tolerances, explicitly define the rule, such as `abs(actual-reference) <= atol + rtol*abs(reference)`, including treatment of near-zero values. Separate reference uncertainty and approximation error from floating-point error. Check finite values, expected shape, norm/trace, and positivity or covariance physicality where the declared object requires them. Nonphysical algebraic maps are permitted only when labeled as such and not presented as channels.

Small exhaustive checks, larger random probes and analytic invariants provide different evidence strengths. Record the tested domain. Probe agreement is not a universal equivalence proof. Reject silent normalization, clipping, term dropping, approximation changes or output permutation that alters the requested task.

<a id="a04"></a>

## A04 - Statistical equivalence and uncertainty

Freeze distributions/estimands, discrepancy metric, equivalence margin, confidence/error level, power target, replication plan, sample budget and multiplicity/sequential-stopping treatment. A non-significant difference is not proof of equivalence: use an equivalence or interval-containment procedure suited to the estimand. Record inconclusive cases when power or reference precision is insufficient.

Validate an estimator on repeated known-distribution or independent synthetic fixtures before interpreting device counts. Account for correlated observations, calibration estimates, grouping, postselection and importance/quasi-probability weights. Preserve original and retained denominators and distinguish execution noise from fixture randomness. Zero observed events do not imply a zero event rate or zero uncertainty. Confidence, credible and heuristic intervals must be labeled accurately.

Hardware statistical success requires the actual acquisition protocol and relevant stationarity assumptions. Simulated, synthetic and hardware records must remain distinct, and caller-declared provenance is not an independent hardware attestation. Do not choose favorable seeds or observables after inspecting evaluation data.

<a id="a05"></a>

## A05 - Target legality, compilation quality and budgets

Freeze target operations, connectivity/direction, dimensions, durations/units, calibration snapshot, alignment, classical latency, shared resources and any ancilla restrictions. Independently validate emitted instructions, interaction legality, scheduling and final logical mapping. Check semantics under A02/A03/A04 as appropriate before comparing circuit quality.

Report compile time and quality together. Use either a fixed-budget quality comparison or time-to-quality contract, with all search/tuning cost charged. Declare native single-body representation and count comparable resources consistently; native depth and raw gate count from different representations are not automatically comparable. Record seeds, target violations, timeouts, memory limits and infeasibility. Missing target constraints cannot be replaced by an easier simulator's capabilities.

<a id="a06"></a>

## A06 - Approximation convergence and bounded claims

Freeze the requested outputs, approximation/error goal, exact comparison region, larger-instance evidence method, representation settings and total planning/execution budget. Distinguish truncation, discretization, tensor-contraction, solver and floating-point errors. Compare methods at the same output/error target, not merely the same internal bond dimension, cutoff or solver knob.

Require independent exact checks where feasible and prescribed refinement/convergence evidence elsewhere. A discarded weight, state norm, small local residual or local-observable match is not automatically a certified global fidelity/error bound. If the task requires a global certificate and none is available, return insufficient evidence. Charge contraction planning, representation selection and output gathering. Report approximation breakdown rather than only the largest nominal problem size.

<a id="a07"></a>

## A07 - Derivatives and training outcomes

Freeze parameter domains, complex-gradient convention, shared-parameter semantics, output shapes, derivative order and method attribution. Check analytic fixtures and independent directional derivatives, including near-zero components; use a justified finite-difference step/convergence procedure when it is the reference. Check the full classical/quantum derivative chain and distinguish finite-shot estimators from analytic derivatives.

For learning, freeze datasets, splits, preprocessing, objective, initialization distribution, optimizer/search policy, stopping rule, total calls/shots and quality target. Report independent-run success distributions, time/evaluations to target, final quality and held-out evaluation. Include compilation, input encoding, preprocessing, hyperparameter search and classical work in the specified end-to-end boundary. Check that batching matches serial semantics. Higher-order support must be demonstrated for the selected path; no blanket claim follows from first derivatives.

A checkpoint continuation must preserve the declared model, optimizer, scheduler, random state, parameter bindings and relevant distributed state. Deterministic or statistical continuation equivalence must be defined in advance.

<a id="a08"></a>

## A08 - Job lifecycle, provenance and failure recovery

Use stubs or replay fixtures for repeatable operational acceptance, plus separately authorized device instances when available. Freeze program hashes, bindings, target, budgets, authorization, retry/idempotency policy, result ordering and provenance requirements. Include lost acknowledgments, partial results, provider errors, cancellation and expired access.

Require zero unapproved submissions, an auditable payload/authorization match, stable experiment identities and exact shot/result reconciliation. A client timeout does not prove that a server rejected the job. An unknown submission state must not automatically cause a duplicate paid task. Preserve provider records and explicit unresolved states. Separate software collection/processing latency from queue delay, QPU duration and calibration drift; mock acceptance alone does not prove live-provider compatibility.

<a id="a09"></a>

## A09 - Application validity and time to target

Freeze the physical/application problem and desired output before choosing implementations. Chemistry must retain geometry, basis, active space, spin/charge, constants and the ground/excited-state target. Dynamics must retain initial state, boundaries, units and time/observable grid. Optimization must decode and validate feasibility/objectives in original variables. Inference and linear algebra must include input preparation, conditioning, oracle construction/query cost, readout and postselection. Kernel/predictive studies must retain splits and account for regularization/search and any matrix repair.

Require an independent reference or defensible bound with declared uncertainty. Define time/resources to an accepted output and retain unsuccessful seeds. A successful toy application does not establish practical utility or quantum advantage; such claims need an appropriate classical comparison and complete cost boundary. Physical resource estimates must expose the model and assumptions rather than appear as measured hardware performance.

<a id="a10"></a>

## A10 - Modality-specific units and physical constraints

Pulse instances specify waveform samples, frames, ports, bandwidth/amplitude limits, clocks and calibrated definitions. Analog instances specify geometry, interactions, interpolation, fields, initialization, device limits and loading/loss rules. Photonic/CV instances specify mode/quadrature/hbar conventions, Gaussian/non-Gaussian semantics, Fock cutoff, detector models and postselection. Annealing instances specify variable domains, coefficient offsets/scaling, embedding/chains, schedules, gauge transforms and repair rules.

Validate physical/program constraints independently and retain any rounding, discretization or approximation. Lowering to another model is allowed only when the task permits it, the semantic/error contract survives and all overhead is attributed. No participant receives a free pass by changing the physical problem, allowable controls, detector definition or desired output type.

<a id="a11"></a>

## A11 - Distributed correctness and resource accounting

Freeze hardware/software environment, device allocation, threads, precision, communication fabric, partitions, random streams, output location and the timing boundary. Synchronize asynchronous work before stopping timers. Distinguish replicated independent work, data parallelism, state sharding and contraction slicing. A larger allocated register or repeated small state is not demonstrated useful state capacity.

Strong scaling keeps the computational task fixed; capacity/weak-scaling experiments specify how work, error and per-worker resources change. Include communication, requested output gathering and relevant setup/checkpoint costs in their declared boundaries. Record host/device memory, timeouts, out-of-memory failures and incomplete/censored results. Cross-device comparisons must not assign differences in hardware to software efficiency without a controlled matched-device experiment.

## Evaluator readiness checklist

Before publishing accepted results, require an independently reviewed fixture/reference, frozen thresholds and budgets, positive and negative cases, evaluator checks, complete measurement/provenance fields and a declared uncertainty treatment. Review both the scientific task and the evaluator, including errors in adapters or references. Store raw evidence sufficient for reanalysis. Templates and structural checks are preparation for this gate, not evidence that it has been passed.
