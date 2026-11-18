# First-wave instance contracts

Generated from [roadmap.json](roadmap.json). Candidate specification only: no participant adapter, result or support claim is implied. All thresholds must pass before reporting accepted timing. These bounded instances do not certify the entire parent task family.

See [measurement rules](MEASUREMENT_PROTOCOL.md), [references](REFERENCES.md) and [comparison scope](COHORTS.md). Each fixture contains explicit input values, operations, datasets or events; each reference artifact contains the independent expected outputs.

## W01 - Reuse a parameterized experiment

A researcher evaluates a reusable experiment at seven parameter bindings and obtains all requested local moments, without leaking a previous binding or state.

Primary requirement: [T006](../requirements/tasks/j02-express-an-algorithm-faithfully.md#t006); cohort: `exact`. All parent personas, capability/function edges and acceptance profiles remain in the linked requirements baseline.

### PARAM-04

Inputs: [fixture](fixtures/PARAM-04.json); expected outputs: [reference](references/PARAM-04.json). Construction arguments: `{"n": 4}`.

Budget: 120 seconds for the complete case, 16 GiB aggregate participant memory.

Independent reference: Closed-form graph-state local moments; dense Kronecker validation at n=4.

| Acceptance field | Required value |
| --- | --- |
| precision | float64 real / complex128 state arithmetic |
| atol | 1e-09 |
| rtol | 1e-08 |
| rule | Every requested finite scalar must satisfy abs(actual-reference) <= atol + rtol*abs(reference); no dropped outputs. |

Required negative control: Swap one binding, drop a repeated binding update, or change a Y sign.

Record: complete seven-binding latency, binding/setup split, peak host memory, all-output maximum error.

### PARAM-12

Inputs: [fixture](fixtures/PARAM-12.json); expected outputs: [reference](references/PARAM-12.json). Construction arguments: `{"n": 12}`.

Budget: 600 seconds for the complete case, 16 GiB aggregate participant memory.

Independent reference: Closed-form graph-state local moments; dense Kronecker validation at n=4.

| Acceptance field | Required value |
| --- | --- |
| precision | float64 real / complex128 state arithmetic |
| atol | 1e-09 |
| rtol | 1e-08 |
| rule | Every requested finite scalar must satisfy abs(actual-reference) <= atol + rtol*abs(reference); no dropped outputs. |

Required negative control: Swap one binding, drop a repeated binding update, or change a Y sign.

Record: complete seven-binding latency, binding/setup split, peak host memory, all-output maximum error.

### PARAM-24

Inputs: [fixture](fixtures/PARAM-24.json); expected outputs: [reference](references/PARAM-24.json). Construction arguments: `{"n": 24}`.

Budget: 3600 seconds for the complete case, 16 GiB aggregate participant memory.

Independent reference: Closed-form graph-state local moments; dense Kronecker validation at n=4.

| Acceptance field | Required value |
| --- | --- |
| precision | float64 real / complex128 state arithmetic |
| atol | 1e-09 |
| rtol | 1e-08 |
| rule | Every requested finite scalar must satisfy abs(actual-reference) <= atol + rtol*abs(reference); no dropped outputs. |

Required negative control: Swap one binding, drop a repeated binding update, or change a Y sign.

Record: complete seven-binding latency, binding/setup split, peak host memory, all-output maximum error.

## W02 - Run an adaptive measurement protocol

An experimenter needs classical feed-forward, bounded stopping and reset semantics to survive execution and result mapping.

Primary requirement: [T009](../requirements/tasks/j02-express-an-algorithm-faithfully.md#t009); cohort: `adaptive`. All parent personas, capability/function edges and acceptance profiles remain in the linked requirements baseline.

### ADAPT-TELEPORT

Inputs: [fixture](fixtures/ADAPT-TELEPORT.json); expected outputs: [reference](references/ADAPT-TELEPORT.json). Construction arguments: `{"kind": "teleport"}`.

Budget: 1800 seconds for the complete case, 8 GiB aggregate participant memory.

Independent reference: Teleportation identity for every joint branch; independent dense branch-projection density audit for six input states.

| Acceptance field | Required value |
| --- | --- |
| shots_per_context_per_block | 65536 |
| independent_process_blocks | 10 |
| total_variation_margin | 0.04 |
| workflow_family_error_probability | 0.01 |
| workflow_total_decisions | 190 |
| confidence_rule | upper_TV = empirical_TV + sqrt((K*ln(2)+ln(190/0.01))/(2*N)) + 1e-10; accept each decision only if upper_TV <= 0.04; N=65536; K=8 teleport or 12 reset-loop. All 190 decisions across 18+1 contexts and ten blocks must pass; unused allocation is not recycled. |

Required negative control: Remove conditional Z, remove conditional X, swap m0/m1, or omit a measured branch.

Record: protocol completion, all-context distribution discrepancy, complete context acquisition time, logical shot/branch accounting.

### ADAPT-RESET-LOOP

Inputs: [fixture](fixtures/ADAPT-RESET-LOOP.json); expected outputs: [reference](references/ADAPT-RESET-LOOP.json). Construction arguments: `{"kind": "reset-loop"}`.

Budget: 900 seconds for the complete case, 8 GiB aggregate participant memory.

Independent reference: Bounded geometric stopping law with exact reset postcondition and all twelve record categories.

| Acceptance field | Required value |
| --- | --- |
| shots_per_context_per_block | 65536 |
| independent_process_blocks | 10 |
| total_variation_margin | 0.04 |
| workflow_family_error_probability | 0.01 |
| workflow_total_decisions | 190 |
| confidence_rule | upper_TV = empirical_TV + sqrt((K*ln(2)+ln(190/0.01))/(2*N)) + 1e-10; accept each decision only if upper_TV <= 0.04; N=65536; K=8 teleport or 12 reset-loop. All 190 decisions across 18+1 contexts and ten blocks must pass; unused allocation is not recycled. |

Required negative control: Fail to reset after success, ignore the third-try cutoff, or drop unsuccessful records.

Record: protocol completion, all-context distribution discrepancy, complete context acquisition time, logical shot/branch accounting.

## W03 - Route an algorithm to legal connectivity

A device user needs a legal compiled program and correctly reconstructed logical outputs, with compile latency and interaction cost exposed.

Primary requirement: [T017](../requirements/tasks/j04-make-a-program-executable-on-a-target.md#t017); cohort: `compiler`. All parent personas, capability/function edges and acceptance profiles remain in the linked requirements baseline.

### ROUTE-LINE-06

Inputs: [fixture](fixtures/ROUTE-LINE-06.json); expected outputs: [reference](references/ROUTE-LINE-06.json). Construction arguments: `{"n": 6, "topology": "line"}`.

Budget: 600 seconds for the complete case, 16 GiB aggregate participant memory.

Independent reference: Independent bit-block propagation and separate dense-Kronecker/gate-permutation construction; no optimal-routing oracle is claimed.

| Acceptance field | Required value |
| --- | --- |
| per_compile_wall_limit_seconds | 120 |
| target | full CZ and arbitrary one-qubit unitaries on listed undirected edges; no ancillas |
| initial_layout | identity |
| final_layout | allowed only with explicit logical reconstruction |
| semantic_atol | 1e-08 |
| semantic_rtol | 0.0 |
| normalization_error_limit | 1e-10 |
| verification | n=6: full operator up to one global phase; n=8,12: three complete output probe states up to one global phase per probe; probe checks are not a universal equivalence proof |
| target_violations_allowed | 0 |
| primary_quality | number of physical full CZ interactions; report compile-time/interaction-count Pareto points; no scalar winner |

Required negative control: Ignore final layout, emit a nonedge CZ, emit a partial CZ, or erase a noncommuting rotation.

Record: compile wall time, full-CZ count, two-body dependency depth from common scheduling rule, target/semantic failures.

### ROUTE-GRID-08

Inputs: [fixture](fixtures/ROUTE-GRID-08.json); expected outputs: [reference](references/ROUTE-GRID-08.json). Construction arguments: `{"n": 8, "topology": "grid-2x4"}`.

Budget: 900 seconds for the complete case, 16 GiB aggregate participant memory.

Independent reference: Independent bit-block propagation and separate dense-Kronecker/gate-permutation construction; no optimal-routing oracle is claimed.

| Acceptance field | Required value |
| --- | --- |
| per_compile_wall_limit_seconds | 120 |
| target | full CZ and arbitrary one-qubit unitaries on listed undirected edges; no ancillas |
| initial_layout | identity |
| final_layout | allowed only with explicit logical reconstruction |
| semantic_atol | 1e-08 |
| semantic_rtol | 0.0 |
| normalization_error_limit | 1e-10 |
| verification | n=6: full operator up to one global phase; n=8,12: three complete output probe states up to one global phase per probe; probe checks are not a universal equivalence proof |
| target_violations_allowed | 0 |
| primary_quality | number of physical full CZ interactions; report compile-time/interaction-count Pareto points; no scalar winner |

Required negative control: Ignore final layout, emit a nonedge CZ, emit a partial CZ, or erase a noncommuting rotation.

Record: compile wall time, full-CZ count, two-body dependency depth from common scheduling rule, target/semantic failures.

### ROUTE-LINE-12

Inputs: [fixture](fixtures/ROUTE-LINE-12.json); expected outputs: [reference](references/ROUTE-LINE-12.json). Construction arguments: `{"n": 12, "topology": "line"}`.

Budget: 1800 seconds for the complete case, 16 GiB aggregate participant memory.

Independent reference: Independent bit-block propagation and separate dense-Kronecker/gate-permutation construction; no optimal-routing oracle is claimed.

| Acceptance field | Required value |
| --- | --- |
| per_compile_wall_limit_seconds | 120 |
| target | full CZ and arbitrary one-qubit unitaries on listed undirected edges; no ancillas |
| initial_layout | identity |
| final_layout | allowed only with explicit logical reconstruction |
| semantic_atol | 1e-08 |
| semantic_rtol | 0.0 |
| normalization_error_limit | 1e-10 |
| verification | n=6: full operator up to one global phase; n=8,12: three complete output probe states up to one global phase per probe; probe checks are not a universal equivalence proof |
| target_violations_allowed | 0 |
| primary_quality | number of physical full CZ interactions; report compile-time/interaction-count Pareto points; no scalar winner |

Required negative control: Ignore final layout, emit a nonedge CZ, emit a partial CZ, or erase a noncommuting rotation.

Record: compile wall time, full-CZ count, two-body dependency depth from common scheduling rule, target/semantic failures.

## W04 - Evaluate a many-term observable

A scientist needs every requested expectation and their weighted total at controlled numerical error, including nonlocal and complex-phase-sensitive terms.

Primary requirement: [T022](../requirements/tasks/j05-compute-the-quantities-a-study-needs.md#t022); cohort: `exact`. All parent personas, capability/function edges and acceptance profiles remain in the linked requirements baseline.

### OBS-04

Inputs: [fixture](fixtures/OBS-04.json); expected outputs: [reference](references/OBS-04.json). Construction arguments: `{"n": 4}`.

Budget: 120 seconds for the complete case, 16 GiB aggregate participant memory.

Independent reference: Independent complex state propagation and Pauli permutation sums, cross-checked against small dense Pauli matrices.

| Acceptance field | Required value |
| --- | --- |
| precision | float64 real / complex128 state arithmetic |
| atol | 1e-09 |
| rtol | 1e-08 |
| rule | Every requested finite scalar must satisfy abs(actual-reference) <= atol + rtol*abs(reference); no dropped outputs. |

Required negative control: Drop a coefficient/observable, conjugate a Y term incorrectly, or silently switch to sampled expectations.

Record: complete 64-term and weighted-sum latency, peak memory, maximum per-output error, state-preparation calls.

### OBS-12

Inputs: [fixture](fixtures/OBS-12.json); expected outputs: [reference](references/OBS-12.json). Construction arguments: `{"n": 12}`.

Budget: 600 seconds for the complete case, 16 GiB aggregate participant memory.

Independent reference: Independent complex state propagation and Pauli permutation sums, cross-checked against small dense Pauli matrices.

| Acceptance field | Required value |
| --- | --- |
| precision | float64 real / complex128 state arithmetic |
| atol | 1e-09 |
| rtol | 1e-08 |
| rule | Every requested finite scalar must satisfy abs(actual-reference) <= atol + rtol*abs(reference); no dropped outputs. |

Required negative control: Drop a coefficient/observable, conjugate a Y term incorrectly, or silently switch to sampled expectations.

Record: complete 64-term and weighted-sum latency, peak memory, maximum per-output error, state-preparation calls.

### OBS-20

Inputs: [fixture](fixtures/OBS-20.json); expected outputs: [reference](references/OBS-20.json). Construction arguments: `{"n": 20}`.

Budget: 3600 seconds for the complete case, 16 GiB aggregate participant memory.

Independent reference: Independent complex state propagation and Pauli permutation sums, cross-checked against small dense Pauli matrices.

| Acceptance field | Required value |
| --- | --- |
| precision | float64 real / complex128 state arithmetic |
| atol | 1e-09 |
| rtol | 1e-08 |
| rule | Every requested finite scalar must satisfy abs(actual-reference) <= atol + rtol*abs(reference); no dropped outputs. |

Required negative control: Drop a coefficient/observable, conjugate a Y term incorrectly, or silently switch to sampled expectations.

Record: complete 64-term and weighted-sum latency, peak memory, maximum per-output error, state-preparation calls.

## W05 - Differentiate a shared-parameter model

An optimizer needs a trustworthy multi-output Jacobian with repeated parameter occurrences before it can rely on learning results.

Primary requirement: [T031](../requirements/tasks/j07-train-and-differentiate-a-hybrid-model.md#t031); cohort: `derivative`. All parent personas, capability/function edges and acceptance profiles remain in the linked requirements baseline.

### GRAD-04

Inputs: [fixture](fixtures/GRAD-04.json); expected outputs: [reference](references/GRAD-04.json). Construction arguments: `{"n": 4}`.

Budget: 180 seconds for the complete case, 16 GiB aggregate participant memory.

Independent reference: Analytic gate-derivative tangent propagation; small dense five-point stencil with h=1e-4 checked at atol=2e-9, rtol=2e-8.

| Acceptance field | Required value |
| --- | --- |
| output_atol | 1e-09 |
| output_rtol | 1e-08 |
| jacobian_atol | 2e-07 |
| jacobian_rtol | 2e-05 |
| shape | 3 outputs by 3*n shared real parameters |
| primary_mode | Exact expectations. Derivative method must be declared; every shifted/objective evaluation and any external derivative component is charged. |
| nonfinite_values_allowed | 0 |

Required negative control: Treat shared occurrences as separate independent parameters, return a transposed Jacobian, or detach a parameter.

Record: full-Jacobian latency, primal/derivative call counts, peak memory, componentwise derivative error.

### GRAD-08

Inputs: [fixture](fixtures/GRAD-08.json); expected outputs: [reference](references/GRAD-08.json). Construction arguments: `{"n": 8}`.

Budget: 600 seconds for the complete case, 16 GiB aggregate participant memory.

Independent reference: Analytic gate-derivative tangent propagation; small dense five-point stencil with h=1e-4 checked at atol=2e-9, rtol=2e-8.

| Acceptance field | Required value |
| --- | --- |
| output_atol | 1e-09 |
| output_rtol | 1e-08 |
| jacobian_atol | 2e-07 |
| jacobian_rtol | 2e-05 |
| shape | 3 outputs by 3*n shared real parameters |
| primary_mode | Exact expectations. Derivative method must be declared; every shifted/objective evaluation and any external derivative component is charged. |
| nonfinite_values_allowed | 0 |

Required negative control: Treat shared occurrences as separate independent parameters, return a transposed Jacobian, or detach a parameter.

Record: full-Jacobian latency, primal/derivative call counts, peak memory, componentwise derivative error.

### GRAD-12

Inputs: [fixture](fixtures/GRAD-12.json); expected outputs: [reference](references/GRAD-12.json). Construction arguments: `{"n": 12}`.

Budget: 1800 seconds for the complete case, 16 GiB aggregate participant memory.

Independent reference: Analytic gate-derivative tangent propagation; small dense five-point stencil with h=1e-4 checked at atol=2e-9, rtol=2e-8.

| Acceptance field | Required value |
| --- | --- |
| output_atol | 1e-09 |
| output_rtol | 1e-08 |
| jacobian_atol | 2e-07 |
| jacobian_rtol | 2e-05 |
| shape | 3 outputs by 3*n shared real parameters |
| primary_mode | Exact expectations. Derivative method must be declared; every shifted/objective evaluation and any external derivative component is charged. |
| nonfinite_values_allowed | 0 |

Required negative control: Treat shared occurrences as separate independent parameters, return a transposed Jacobian, or detach a parameter.

Record: full-Jacobian latency, primal/derivative call counts, peak memory, componentwise derivative error.

## W06 - Train a hybrid regression model

A practitioner needs correct minibatch gradients across the quantum/classical boundary and a reproducible training trajectory under a complete evaluation budget.

Primary requirement: [T032](../requirements/tasks/j07-train-and-differentiate-a-hybrid-model.md#t032); cohort: `learning`. All parent personas, capability/function edges and acceptance profiles remain in the linked requirements baseline.

### TRAIN-04-B16

Inputs: [fixture](fixtures/TRAIN-04-B16.json); expected outputs: [reference](references/TRAIN-04-B16.json). Construction arguments: `{"batch": 16, "n": 4}`.

Budget: 900 seconds for the complete case, 16 GiB aggregate participant memory.

Independent reference: Closed-form quantum moments cos(x+theta), independently differentiated classical head and explicit SGD recurrence; full trace stored.

| Acceptance field | Required value |
| --- | --- |
| steps | 48 |
| learning_rate | 0.03 |
| optimizer | plain SGD, no momentum, clipping, regularization or hidden averaging |
| loss_atol | 1e-07 |
| loss_rtol | 1e-05 |
| parameter_atol | 1e-06 |
| parameter_rtol | 1e-05 |
| gradient_atol | 2e-07 |
| gradient_rtol | 2e-05 |
| progress_target | train MSE <= 0.95 * own frozen initial train MSE, separately for all five fixed initializations |
| trajectory | Validate every step against the corresponding stored reference trajectory; report held-out MSE at steps 0 and 48; no tuning on held-out rows. |
| complete_budget | Ten independent process blocks; initializations cycle [11,23,37,51,73] twice; one complete 48-step run per block. |

Required negative control: Collapse the batch before its quantum layer, break the classical/quantum derivative chain, change MSE normalization, or skip/reset optimizer steps.

Record: time to 5% progress, complete 48-step wall time, held-out MSE, calls and peak memory.

### TRAIN-08-B32

Inputs: [fixture](fixtures/TRAIN-08-B32.json); expected outputs: [reference](references/TRAIN-08-B32.json). Construction arguments: `{"batch": 32, "n": 8}`.

Budget: 1800 seconds for the complete case, 16 GiB aggregate participant memory.

Independent reference: Closed-form quantum moments cos(x+theta), independently differentiated classical head and explicit SGD recurrence; full trace stored.

| Acceptance field | Required value |
| --- | --- |
| steps | 48 |
| learning_rate | 0.03 |
| optimizer | plain SGD, no momentum, clipping, regularization or hidden averaging |
| loss_atol | 1e-07 |
| loss_rtol | 1e-05 |
| parameter_atol | 1e-06 |
| parameter_rtol | 1e-05 |
| gradient_atol | 2e-07 |
| gradient_rtol | 2e-05 |
| progress_target | train MSE <= 0.95 * own frozen initial train MSE, separately for all five fixed initializations |
| trajectory | Validate every step against the corresponding stored reference trajectory; report held-out MSE at steps 0 and 48; no tuning on held-out rows. |
| complete_budget | Ten independent process blocks; initializations cycle [11,23,37,51,73] twice; one complete 48-step run per block. |

Required negative control: Collapse the batch before its quantum layer, break the classical/quantum derivative chain, change MSE normalization, or skip/reset optimizer steps.

Record: time to 5% progress, complete 48-step wall time, held-out MSE, calls and peak memory.

## W07 - Predict physical dynamics observables

A many-body researcher needs observable predictions for a fixed Hamiltonian and physical time, with software and discretization errors distinguished.

Primary requirement: [T037](../requirements/tasks/j08-answer-a-scientific-or-application-question.md#t037); cohort: `exact`. All parent personas, capability/function edges and acceptance profiles remain in the linked requirements baseline.

### DYN-04-S32

Inputs: [fixture](fixtures/DYN-04-S32.json); expected outputs: [reference](references/DYN-04-S32.json). Construction arguments: `{"n": 4, "steps": 32}`.

Budget: 600 seconds for the complete case, 16 GiB aggregate participant memory.

Independent reference: Dense spectral evolution of an independently assembled TFIM matrix; separate circuit-propagation reference records product-formula bias.

| Acceptance field | Required value |
| --- | --- |
| physics_max_abs_observable_error | 0.002 |
| digital_ideal_atol | 1e-09 |
| digital_ideal_rtol | 1e-08 |
| mode | Matched second-order product formula, given step count and operation sequence; exact spectral reference is the physical target. Best-available solver selection is a later separate cohort. |
| requested_outputs | all local Z/X moments and all nearest-neighbor ZZ moments at t=0.7; open chain; hbar=1 |

Required negative control: Change sign/time/boundary, omit outputs, or compare to the digital ideal alone without checking the physical error.

Record: complete evolution-plus-observable time, physical error, software error against digital ideal, memory.

### DYN-08-S64

Inputs: [fixture](fixtures/DYN-08-S64.json); expected outputs: [reference](references/DYN-08-S64.json). Construction arguments: `{"n": 8, "steps": 64}`.

Budget: 1800 seconds for the complete case, 16 GiB aggregate participant memory.

Independent reference: Dense spectral evolution of an independently assembled TFIM matrix; separate circuit-propagation reference records product-formula bias.

| Acceptance field | Required value |
| --- | --- |
| physics_max_abs_observable_error | 0.002 |
| digital_ideal_atol | 1e-09 |
| digital_ideal_rtol | 1e-08 |
| mode | Matched second-order product formula, given step count and operation sequence; exact spectral reference is the physical target. Best-available solver selection is a later separate cohort. |
| requested_outputs | all local Z/X moments and all nearest-neighbor ZZ moments at t=0.7; open chain; hbar=1 |

Required negative control: Change sign/time/boundary, omit outputs, or compare to the digital ideal alone without checking the physical error.

Record: complete evolution-plus-observable time, physical error, software error against digital ideal, memory.

## W08 - Sample an asymmetric measurement distribution

A user needs correctly mapped counts whose distribution is equivalent to the requested measurement law, not merely a total shot count.

Primary requirement: [T012](../requirements/tasks/j03-establish-program-correctness.md#t012); cohort: `exact`. All parent personas, capability/function edges and acceptance profiles remain in the linked requirements baseline.

### SAMPLE-03

Inputs: [fixture](fixtures/SAMPLE-03.json); expected outputs: [reference](references/SAMPLE-03.json). Construction arguments: `{"n": 3}`.

Budget: 300 seconds for the complete case, 8 GiB aggregate participant memory.

Independent reference: Analytic product-rotation probabilities and invertible CNOT permutation; exact small dense check.

| Acceptance field | Required value |
| --- | --- |
| shots_per_block | 65536 |
| independent_process_blocks | 10 |
| total_variation_margin | 0.04 |
| workflow_family_error_probability | 0.01 |
| workflow_total_decisions | 20 |
| confidence_rule | upper_TV = empirical_TV + sqrt((K*ln(2)+ln(20/0.01))/(2*N)) + 1e-10; accept each decision only if upper_TV <= 0.04; K=2**n including impossible outcomes; all twenty decisions must pass. |
| type_rule | Nonnegative integer counts with exact total shots and exact register/logical mapping; malformed records fail before statistics. |

Required negative control: Swap measured registers, alter shot totals, supply probabilities as counts, or inject out-of-alphabet outcomes.

Record: sampling-and-normalization time, distribution upper bound, shots per second, invalid/inconclusive outcomes.

### SAMPLE-05

Inputs: [fixture](fixtures/SAMPLE-05.json); expected outputs: [reference](references/SAMPLE-05.json). Construction arguments: `{"n": 5}`.

Budget: 600 seconds for the complete case, 8 GiB aggregate participant memory.

Independent reference: Analytic product-rotation probabilities and invertible CNOT permutation; exact small dense check.

| Acceptance field | Required value |
| --- | --- |
| shots_per_block | 65536 |
| independent_process_blocks | 10 |
| total_variation_margin | 0.04 |
| workflow_family_error_probability | 0.01 |
| workflow_total_decisions | 20 |
| confidence_rule | upper_TV = empirical_TV + sqrt((K*ln(2)+ln(20/0.01))/(2*N)) + 1e-10; accept each decision only if upper_TV <= 0.04; K=2**n including impossible outcomes; all twenty decisions must pass. |
| type_rule | Nonnegative integer counts with exact total shots and exact register/logical mapping; malformed records fail before statistics. |

Required negative control: Swap measured registers, alter shot totals, supply probabilities as counts, or inject out-of-alphabet outcomes.

Record: sampling-and-normalization time, distribution upper bound, shots per second, invalid/inconclusive outcomes.

## W09 - Recover work without duplicate submission

An experimenter needs to reconcile interrupted work without silently losing records or duplicating paid execution.

Primary requirement: [T048](../requirements/tasks/j10-run-a-recoverable-device-experiment.md#t048); cohort: `orchestration`. All parent personas, capability/function edges and acceptance profiles remain in the linked requirements baseline.

### JOB-LOST-ACK

Inputs: [fixture](fixtures/JOB-LOST-ACK.json); expected outputs: [reference](references/JOB-LOST-ACK.json). Construction arguments: `{"kind": "lost-ack"}`.

Budget: 120 seconds for the complete case, 8 GiB aggregate participant memory.

Independent reference: Explicit finite-state/event-ledger tables; positive and fault transitions are fixture data, independent of any client.

| Acceptance field | Required value |
| --- | --- |
| unapproved_or_duplicate_submissions_allowed | 0 |
| identity_or_shot_accounting_errors_allowed | 0 |
| hidden_retries_allowed | 0 |
| transport | Offline deterministic event stub only; no external network, credentials or paid device requests. |
| decision | Required ledger/postconditions must match exactly; partial/cancelled work must remain partial rather than successful completion. |
| adapter_rule | The stub supplies provider events, not missing client reconciliation logic. A participant-specific transport binding must be reviewed before this case is executable. |

Required negative control: Resubmit after an accepted but unacknowledged request, double-count a repeated result page, or erase cancelled work.

Record: correct reconciliation and classification, duplicate count, handling latency as diagnostic only, not a performance ranking.

### JOB-PARTIAL-CANCEL

Inputs: [fixture](fixtures/JOB-PARTIAL-CANCEL.json); expected outputs: [reference](references/JOB-PARTIAL-CANCEL.json). Construction arguments: `{"kind": "partial-cancel"}`.

Budget: 120 seconds for the complete case, 8 GiB aggregate participant memory.

Independent reference: Explicit finite-state/event-ledger tables; positive and fault transitions are fixture data, independent of any client.

| Acceptance field | Required value |
| --- | --- |
| unapproved_or_duplicate_submissions_allowed | 0 |
| identity_or_shot_accounting_errors_allowed | 0 |
| hidden_retries_allowed | 0 |
| transport | Offline deterministic event stub only; no external network, credentials or paid device requests. |
| decision | Required ledger/postconditions must match exactly; partial/cancelled work must remain partial rather than successful completion. |
| adapter_rule | The stub supplies provider events, not missing client reconciliation logic. A participant-specific transport binding must be reviewed before this case is executable. |

Required negative control: Resubmit after an accepted but unacknowledged request, double-count a repeated result page, or erase cancelled work.

Record: correct reconciliation and classification, duplicate count, handling latency as diagnostic only, not a performance ranking.

## W10 - Round-trip an executable program

An integration engineer needs another tool or environment to preserve program, register and adaptive semantics through interchange.

Primary requirement: [T082](../requirements/tasks/j17-exchange-audit-and-reproduce-work.md#t082); cohort: `interchange`. Supporting requirements: T081. All parent personas, capability/function edges and acceptance profiles remain in the linked requirements baseline.

### ROUND-QASM2

Inputs: [fixture](fixtures/ROUND-QASM2.json); expected outputs: [reference](references/ROUND-QASM2.json). Construction arguments: `{"kind": "qasm2"}`.

Budget: 300 seconds for the complete case, 8 GiB aggregate participant memory.

Independent reference: Published small text fixture, independent matrix interpretation for QASM2 and exact branch enumeration for QASM3.

| Acceptance field | Required value |
| --- | --- |
| required_format | OpenQASM 2.0 static subset |
| numeric_atol | 1e-08 |
| numeric_rtol | 0.0 |
| register_or_feature_loss_allowed | 0 |
| verification | Compare small full premeasurement semantics and exact register permutation for QASM2; enumerate every reachable branch and reset postcondition for QASM3. |
| fallback_rule | Unsupported syntax/profile is unsupported, never a successful parse with omitted features. Conversion work must be performed by registered participant components. |

Required negative control: Drop a conditional/reset, reorder classical outputs, erase an angle or report parser success despite unsupported constructs.

Record: semantic/metadata retention, complete parse-export-reimport latency, loss/rejection diagnostics, artifact bytes.

### ROUND-QASM3

Inputs: [fixture](fixtures/ROUND-QASM3.json); expected outputs: [reference](references/ROUND-QASM3.json). Construction arguments: `{"kind": "qasm3"}`.

Budget: 300 seconds for the complete case, 8 GiB aggregate participant memory.

Independent reference: Published small text fixture, independent matrix interpretation for QASM2 and exact branch enumeration for QASM3.

| Acceptance field | Required value |
| --- | --- |
| required_format | OpenQASM 3.0 declared measurement/reset/if subset |
| numeric_atol | 1e-08 |
| numeric_rtol | 0.0 |
| register_or_feature_loss_allowed | 0 |
| verification | Compare small full premeasurement semantics and exact register permutation for QASM2; enumerate every reachable branch and reset postcondition for QASM3. |
| fallback_rule | Unsupported syntax/profile is unsupported, never a successful parse with omitted features. Conversion work must be performed by registered participant components. |

Required negative control: Drop a conditional/reset, reorder classical outputs, erase an angle or report parser success despite unsupported constructs.

Record: semantic/metadata retention, complete parse-export-reimport latency, loss/rejection diagnostics, artifact bytes.
