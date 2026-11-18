# Phased implementation roadmap

## Delivery principles

Start from the user outcome and an independently checkable answer. Establish semantic correctness before comparing speed, and report complete workflows alongside component diagnostics. Requirements are not dropped when an SDK lacks support. [All 92 families](PHASE_ASSIGNMENTS.md) retain a delivery assignment; a phase assignment promises neither full family implementation nor participant coverage.

The phases are dependency gates, not calendar deadlines or a ranking of computing models. Specialist P2 lanes may qualify alongside P1 once their own P0 foundations pass. Actual delivery estimates require named maintainers, reviewer availability and access approvals; those are not claimed here. Roles below are responsibilities to assign, not fictional completed appointments.

## P0 - Qualify the measurement system

**Need:** a user must trust answers, task applicability and resource accounting before using a comparison to choose a tool. Owner roles: protocol maintainer, independent reference reviewer and measurement reviewer. Scope includes environment/provenance, precision, output normalization, validation, safe operational boundaries and result evidence; see the P0 register for corresponding families.

Deliver in dependency order:

1. Review the ten first-wave user outcomes with intended users, especially operational and specialist users. Record missing needs, scope objections and conflicts of interest. Review thresholds without participant timing data.
2. Review the parameter-complete fixtures and independent oracle derivations; check seeds, bit/register conventions, global phase, branches, shared parameters, gradients and error budgets. Store signed review records and amendment history alongside fixture hashes.
3. Implement separate evaluators for deterministic values, distribution equivalence, compilation legality, training trajectories and operational ledgers. Add every required negative control from the instance contracts. A validator must reject a deliberately wrong result even when it is very fast.
4. Implement a process supervisor enforcing wall/RSS/thread/network restrictions and complete raw evidence capture. Test timeout, out-of-memory, nonfinite output, missing records, unsupported syntax and child-process leakage. Validate clocks and telemetry against controlled workloads.
5. Register adapter interfaces, attribution rules and result schemas; resolve and hash actual component environments on the sealed host. Independently review adapter semantic translations, especially adaptive execution and offline job transport bindings.

**Exit gate:** independent review records exist; all 24 positive fixture checks and required negative controls pass through the evaluators; supervisor fault tests pass; exact host/image/dependency manifests are sealed; every attempted stack has an eligibility/status record. Candidate fixture generation alone does not satisfy this gate. No participant timing publication before it passes.

## P1 - Publish a bounded local workflow study

**Need:** researchers and integration engineers need correct reusable experiments, numerical results, derivatives, training, compiled programs and recoverable execution. Ten workflows and 24 instances are specified in [FIRST_WAVE.md](FIRST_WAVE.md). Owner roles: adapter maintainers, independent adapter reviewers and study operator.

Implementation batches follow data dependencies:

| Batch | Workflows | Why this order | Required evidence |
| --- | --- | --- | --- |
| P1a | W01 parameter reuse, W08 mapped sampling, W04 observables | Establish reusable inputs, numerical conventions and count semantics needed by later workflows | Correct outputs and negatives; binding/order isolation; raw moments/counts; precision and resource manifests |
| P1b | W05 Jacobians, W07 dynamics, W03 routing | Test scientific and device-facing correctness with independent mathematical references | Full Jacobians; separate digital/physical error; target legality, layout reconstruction and compilation artifacts |
| P1c | W06 training, W02 adaptation, W10 interchange, W09 recovery | Validate complete outcomes beyond a numerical kernel | Every training checkpoint; joint branch records; exported/reimported programs; reconciled ledgers and explicit partial status |

These batches are implementation sequencing, not publication selection. The primary report covers all registered attempts in the complete first wave, including failures and missing capabilities. A smaller pilot may be released only as a clearly labeled pilot with all intended-but-unimplemented instances listed; it is not the P1 exit gate.

**Exit gate:** P0 complete; ten blocks per attempted case under the frozen protocol; raw artifacts and failure records published; correctness decisions independently reproduced; at least two independently maintained eligible stacks in a role for a comparative claim (otherwise descriptive evidence only). Complete budget/censoring disclosures, reviewer objections and role-specific coverage tables are mandatory. No combined universal leaderboard.

## P2 - Expand scientific and computing-model coverage

**Need:** real applications require more than exact small gate programs. Scientific breadth and alternative models are first-class requirements. Owner roles: domain user plus independent domain-reference reviewer for each lane. No lane waits for another SDK to add a feature. All unselected families remain visible in the register.

| Lane | Next needs and representative instances to specify | Independent reference / qualification gate |
| --- | --- | --- |
| Noise and approximation | Channels, correlated/readout errors, trajectories, mitigation, approximate tensor outputs; vary requested error and shots | Small density/Kraus propagation and analytic channels; uncertainty coverage and bias tests; matched achieved error, not identical truncation knobs |
| Algorithms and scientific applications | Ground-state/chemistry energies, excited states, optimization, estimation, Hamiltonian dynamics beyond the first TFIM, state preparation | Exact diagonalization or independently converged classical calculations with pinned Hamiltonians, units and geometry; physical residual/error and total budget; no unqualified application advantage claim |
| Learning and differentiation | Entangled feature models, higher derivatives, stochastic gradients, structured data and optimizer choice | Analytic small cases plus independent classical derivative checks; data splits, optimizer/search cost and uncertainty; first-wave regression is insufficient coverage |
| QEC and fault tolerance | Stabilizer extraction, decoding, logical error, feed-forward, lattice surgery and resource estimation | Enumerated small codes/noise and independent syndrome/logical checks; confidence bounds for rare errors and explicit decoder/resource attribution |
| Pulse and calibration | Waveforms, frames, timing constraints, schedule semantics and calibration fitting | Analytic/Rabi small systems plus independently converged differential-equation references; units, hardware constraints and uncertainty reviewed before control claims |
| Analog and neutral atom | Geometry, interactions, ramps, constraints and observable prediction | Small independent Hamiltonian/spectral solutions; geometry/units and evolution-error checks; simulator and live-device outcomes separated |
| Photonic and continuous variable | Gaussian/non-Gaussian programs, Fock truncation, loss and detection | Analytic Gaussian moments/small Fock reference; explicit energy/cutoff convergence and tail-error budget |
| Annealing and optimization models | QUBO/Ising formulation, embedding, constraints, schedules and solution quality | Enumerate small objectives and constraint satisfaction; time-to-quality distribution including formulation/embedding/sampling cost |
| Qudits and measurement-based computation | Mixed local dimensions, resource graphs, measurement dependencies and byproducts | Small dense mixed-radix operators and exhaustive measurement branches; no silent qubit encoding or ignored byproduct |
| Interoperability, reliability and developer workflows | Additional formats/versions, remote schemas, exceptions, installation, documentation-guided completion and reproducible environments | Round-trip semantic references, fault injection and blinded user task protocols; preserve unsupported and inaccessible outcomes |

**Entry gate per lane:** a real user outcome, domain review and the same specification fields as P1, including concrete inputs, independent reference, numeric/statistical tolerances, adverse cases, resource ceiling and eligible roles. Freeze actual sizes and budgets before selecting or timing implementations. No numeric budgets for unspecified future experiments are fabricated here.

**Exit gate per released lane:** independent semantic/physical review, validator mutation tests, eligible stack manifests and a complete evidence bundle at the declared error/quality target. Preserve separate model-specific views; do not translate missing model coverage into an irrelevant speed score.

## P3 - Measure useful capacity and scaling

**Need:** practitioners need to know which useful workload fits their compute budget and how throughput, capacity and recovery change with resources. J16 families lead this phase; the applicable P1/P2 tasks are scaled again rather than assumed to scale.

Deliver matched-device CPU parallel, single-GPU, multi-GPU and multi-node profiles, each with independently sealed hardware/software manifests. Separate independent-experiment batching from partitioning one state or tensor network. Grow tasks on preregistered size ladders until correctness, time, memory or monetary limits; report the boundary and censoring rather than extrapolating beyond it. Measure compile/JIT/startup, transfers, communication, peak host/device memory, energy where calibrated and recovery after interruption.

**Entry gate:** verified small semantics plus resource-specific references/error certificates, device access and a preapproved compute budget. **Exit gate:** strong/weak scaling and time-to-quality curves with complete resource/cost accounting, explicit out-of-memory/timeouts and independent replication on a second host. Accelerator results are not mixed into the CPU1-FP64 table. Fair algorithmic freedom at matched error is a separate study from matched-method comparisons.

## P4 - Controlled live workflows and replication

**Need:** reliable offline behavior must eventually predict useful behavior under real device noise, queues, calibration drift and cost constraints. The field acquisition/model-validation/drift families have P4 assignments. Independent replication is desirable from P0 onward; P4 requires prospective field replication rather than postponing all review until this phase.

Deliver separately authorized provider/device studies with job reconciliation, calibration snapshots, dated availability, prospective predictions, shot/cost limits and drift-aware repetitions. Separate SDK overhead from queue latency and physical-device quality. Use matched devices and access conditions wherever possible; otherwise report noncomparability. Account for failed/cancelled work and no-refund costs. Do not infer SDK superiority from a better QPU or privileged queue.

**Entry gate:** P0 operational fault tests; relevant scientific lane validated; named device, access authorization, spending/shot/job limits and stopping rules approved before submission. **Exit gate:** independently reproduced raw results with timestamped device metadata, uncertainty and cost, and an explicit scope statement for what the result cannot generalize to. This planning change authorizes no device requests or spending.

## Immediate implementation backlog

The next code change should implement the result schema, deterministic evaluator and supervisor before adding participant adapters. Then implement W01/W08/W04 adapter contracts against at least two independently maintained eligible stacks; deliberately inject bad angles, swapped outputs, incorrect counts and suppressed errors. Continue through P1b/P1c, with adaptive and orchestration contracts reviewed independently rather than emulated by benchmark glue. Publish implementation/readiness status separately from measured support. A maintainer who contributes to an evaluated SDK cannot be the sole approver of its adapter or the protocol thresholds.
