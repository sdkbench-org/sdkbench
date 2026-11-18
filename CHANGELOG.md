# Changelog

## 0.3.0

- Added public native FlagQuantum, Qiskit and Cirq adapters for parameter reuse, joint sampling and multi-term observable tasks.
- Added the strict `sdkbench-p1a` process-block runner with warmups, measured repetitions, seeds, cumulative case budgets and complete failure evidence.
- Added pinned CPU integration CI, real-adapter tests and synthetic lifecycle/adverse-case tests; engineering qualification remains separate from a reviewed performance study.
- Added observed environment and installed-component content provenance, with explicit unsealed-image status.

## 0.2.0

- Added SDK-neutral P0 result, registration and content-addressed protocol-bundle contracts.
- Added independent semantic evaluators for all 24 candidate first-wave instances, including complete-case accounting.
- Added a fail-closed Linux cgroup-v2/seccomp execution supervisor and a bounded adapter invocation protocol.
- Added positive, adversarial and real-kernel resource/fault qualification tests plus the `sdkbench-p0` CLI.
- Kept candidate-protocol acceptance separate from participant support, independent review and performance publication.

## 0.1.0

- Added deterministic GHZ, QFT, brickwork and echo circuit generators.
- Added Qiskit/Cirq adapters and a NumPy reference statevector oracle.
- Added construction, inversion, composition, statevector and CZ-target compilation benchmarks.
- Added warmups, raw timings, statistical summaries, correctness checks and explicit failure reporting.
- Added environment metadata, circuit fingerprints, JSON/CSV export and matched-report comparisons.
