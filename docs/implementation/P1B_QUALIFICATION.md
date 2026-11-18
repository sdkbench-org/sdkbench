# P1b engineering qualification results

Date: 2026-11-18. Protocol: `sdkbench-first-wave / 0.1-candidate-1`. This is real native CPU engineering integration, with unchanged P0 acceptance and resource caps. It is not a global SDK ranking or an independently approved performance study.

## Complete frozen scope

The final-runtime campaign contains **240 fresh process blocks, 720 measured records and 480 warmup records**, covering all eight instances for all three registered stacks. Each case has ten blocks with two warmups and three measured outcomes per block.

| Frozen instance | FlagQuantum 0.3.1 + Torch CPU | Qiskit 2.6.2 + Algorithms 0.4.0 | Cirq-core 1.7.0 |
| --- | --- | --- | --- |
| ROUTE-LINE-06 | Accepted | Accepted | Accepted |
| ROUTE-GRID-08 | Accepted | Accepted | Accepted |
| ROUTE-LINE-12 | Accepted | Accepted | Accepted |
| GRAD-04 | Accepted | Accepted | Unsupported |
| GRAD-08 | Accepted | Accepted | Unsupported |
| GRAD-12 | Accepted | Accepted | Unsupported |
| DYN-04-S32 | Accepted | Accepted | Accepted |
| DYN-08-S64 | Accepted | Accepted | Accepted |

Case outcomes: **21 accepted**, **3 unsupported**. Workflow outcomes: 8 accepted, 1 unsupported.

Measured record outcomes: 630 accepted, 90 unsupported. Warmup record outcomes: 420 accepted, 60 unsupported. Unsupported attempts are retained as non-success, with reasons and no successful timing substitute. They are never credited as accepted zero-latency work.

Cirq-core does not provide the registered task through a general expectation-Jacobian API. TensorFlow Quantum 0.7.6 pins a different Cirq-core version and was not silently installed into this stack. This gap applies to the registered core stack, not every possible Cirq ecosystem combination. All participants remain subject to the same frozen derivative requirements.

## Native routing artifacts

The common evaluator computes the following ranges across the 30 measured artifacts in each case. The values describe these exact target/input/configuration combinations. They do not establish optimal routing, a hardware score or a general compiler ranking. FlagQuantum and Cirq expose no compiler seed argument in the selected APIs; identical outputs across blocks are not independent randomized searches.

| SDK | Instance | Full-CZ count range | Two-body dependency depth range |
| --- | --- | --- | --- |
| cirq | ROUTE-GRID-08 | 84 | 52 |
| cirq | ROUTE-LINE-06 | 68 | 65 |
| cirq | ROUTE-LINE-12 | 360 | 198 |
| flagquantum | ROUTE-GRID-08 | 218 | 165 |
| flagquantum | ROUTE-LINE-06 | 228 | 194 |
| flagquantum | ROUTE-LINE-12 | 1092 | 656 |
| qiskit | ROUTE-GRID-08 | 85 | 45–47 |
| qiskit | ROUTE-LINE-06 | 68 | 65 |
| qiskit | ROUTE-LINE-12 | 339–348 | 192–219 |

The six-qubit case checks the whole operator up to a single global phase. The larger two cases use the three frozen full-output probes and retain that limited-evidence label. Raw compilation latency, complete-outcome latency, semantic errors and memory telemetry are in the archive. No timing winner is inferred from an unsealed shared engineering host.

## Reproducible evidence

- Executed source: [`7037884603c75f3cd9e65ee35e247b60ccf04bec`](https://github.com/sdkbench-org/sdkbench/commit/7037884603c75f3cd9e65ee35e247b60ccf04bec).
- Full campaign: [completed Linux workflow](https://github.com/sdkbench-org/sdkbench/actions/runs/44268649442).
- Lossless raw archive: [p1b-full-7037884.json.gz](evidence/p1b-full-7037884.json.gz).
- Archive hashes, counts, component versions and limitations: [p1b-index.json](evidence/p1b-index.json).

All 728 retained evidence-file hashes were verified against the original manifest. Independent replay without participant imports checks every measured/warmup decision, all 24 complete cases, workflow completeness and registration bindings. The archive preserves original UTF-8 bytes and paths, including requests, native outputs, bounded stdout/stderr, environment and installed-component fingerprints, admissions, resource telemetry and verdicts.

The run uses one kernel-enforced CPU, one numerical thread and the frozen 16-GiB case memory caps. Complete-case wall budgets accumulate across blocks; every compilation additionally has a 120-second terminating kernel alarm. A separate supervised native-call test proves the alarm terminates code holding the GIL. Descendant cleanup is checked by CI. Kernel limits are ceilings, not a claim that the CI VM matches the dedicated publication host.

The final gradient records separately count native primal and derivative API calls. Forward-program invocation counts and expectation-request counts remain explicitly different units; unobserved internal bindings/evolutions are omitted. Earlier [diagnostic integration](https://github.com/sdkbench-org/sdkbench/actions/runs/44267511488) used source `c7f72b3`, before removal of an inapplicable inherited binding counter. Its numeric decisions were replayed, but its timings/audits are not pooled into the final-runtime dataset.

To replay after extracting the archive into an empty directory:

```sh
python tools/p1b_evidence.py --directory PATH --bundle docs/implementation
```

## Failure accounting and remaining gates

Real-adapter tests reject the same corrupted Jacobians, dynamics outputs, off-target interactions, wrong final layouts and over-cap compilations for every applicable SDK. Separate synthetic tests exercise unsupported features, installation failures, native exceptions, OOM, compiler timeouts, bad identity/PID/count evidence and changed registration bindings. Synthetic faults are harness tests and are not attributed to any participant.

Passing integration CI means declared outcomes were correctly retained, including known unsupported cases. It does not turn unsupported verdicts into task acceptance. The public CLI returns nonzero for any nonaccepted case. No participant-specific tolerance, hidden simulator/derivative/router fallback, SDK source patch or best-of retry was used.

All reports remain `publication_eligible: false`. Independent adapter review, dedicated sealed host/image qualification, wider SDK/extension registrations and broader requirements coverage remain open. No global position for any SDK follows from this phase.
