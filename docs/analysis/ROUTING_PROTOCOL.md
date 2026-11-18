# Routing attribution protocol

This follow-up investigates the P1b routing counts without changing the frozen tasks, acceptance rules, production adapters or original results. It separates a registered default pipeline from the SDK's available nondefault configurations. It is an exploratory mechanism study, not a blinded performance study or an optimized global SDK ranking. Local public-API probes preceded this controlled campaign.

## Questions and controls

The machine-readable [profile](routing-profile.json) declares every arm before the controlled Linux execution. All arms, including failures and regressions, must be retained. No best-of result replaces a baseline.

- FlagQuantum: the complete 4 x 2 x 2 factorial of `restore_after_each_gate`, `persistent_layout`, `auto` and `sabre`; retain/remove the final restore through the public `remove_layout_restore`; no extra pass/add native optimization plus native legalization after the first basis lowering. All use native optimization level 2. Additional controls use default routing at native levels 0 and 1, and the universal RX/RZ one-qubit basis instead of the original larger named one-qubit basis. These are 19 configurations.
- Qiskit: default, explicitly requested SABRE, basic and lookahead routing at level 2, plus the default pipeline at level 0. Every configuration uses all ten frozen compiler seeds. Numeric optimization levels are SDK-specific labels, not equal optimization effort across SDKs.
- Cirq: the registered RouteCQC and full-CZ target-synthesis baseline. It exposes no seed argument in this API. No alternative optimizer is invented for this analysis.

Each configuration/input pair retains the frozen identity initial placement, width, undirected edges, no-ancilla rule, full-CZ/one-qubit output family, allowed final permutation and original independent P0 tolerances. `sabre_layout` is excluded because it searches a nonidentity initial layout. This exclusion is a task constraint, not a failure or a missing SDK capability. Public runtime/deployment compilation services are distinct entry points and are not silently substituted into this expert-compiler cohort.

The design has 210 frozen-instance diagnostic outcomes: 19 deterministic FlagQuantum configurations x 3 cases, 5 Qiskit configurations x 3 cases x 10 seeds, and 1 deterministic Cirq configuration x 3 cases. Deterministic configurations are not repeated to create artificial independent searches. The different search spaces mean this study cannot establish a fair best-tuned SDK ranking. It can establish causal within-SDK effects and reproduce the registered configuration comparison.

## Independent microprobes

Six six-qubit line microprobes isolate local native lowering, cancellation, reuse of a remote interaction, and a native SWAP followed by a CNOT with the same or reversed operand order. Nonzero one-qubit rotations make every wire active. The profile selects seven FlagQuantum controls and the Qiskit/Cirq baselines, producing another 54 outcomes. All are checked as complete operators, up to one global phase, using the unchanged P0 routing validator and six-qubit acceptance thresholds.

The two SWAP/CNOT probes build the SDK's native SWAP instruction. Their independent P0 reference input spells SWAP as three CNOTs because P0's original input interpreter has no SWAP opcode. This reference-only definition is not used to compile or lower participant output. Both input representations, their digest and the exact generator source are retained. These synthetic diagnostic inputs have their own IDs; they are never represented as the original frozen fixtures or credited as full P1b cases.

A compiler may absorb a logical SWAP into its final permutation. This is permitted by the task, but must be distinguished from reducing the entangling cost while retaining an identity final layout. Every output permutation is retained and independently reconstructed.

## Native stage evidence

FlagQuantum execution calls public `compile`, `remove_layout_restore`, `optimize` and `legalize_native_gates`. A read-only Python profiler observes the released implementation's pre-routing optimizer, routing and post-routing optimizer returns. It records opcode counts, routed SWAP phases, source instruction indices and native metadata. Native basis-lowering records identify each source instruction and emitted opcodes. No SDK function, source or IR is patched, and no benchmark-side routing, matrix-block optimizer or synthesis fallback is used.

Qiskit's public transpiler callback records pass names and intermediate opcode counts; original initial and final layout mappings are retained. Cirq retains native operation counts before routing, after RouteCQC and after target synthesis. The primary cross-SDK metrics remain the common independent full-CZ count and two-body dependency depth, not SDK-specific depth counters.

Profiling, callbacks and trace materialization perturb wall time. Their cost is inside the diagnostic compilation bound. The resulting times must not be used for speed rankings or pooled with the uninstrumented P1b timing records.

## Lifecycle, resource limits and evidence

Every outcome runs in a fresh process with zero warmups and one measured compilation. This is diagnostic qualification, not ten-block full-case acceptance. The existing P0 supervisor enforces a single CPU, one numerical thread, 16 GiB, no sockets, bounded files/output and descendant cleanup. The original 600/900/1800-second complete-case wall ceilings accumulate across diagnostic outcomes for each registered configuration/input. Every instrumented compilation additionally has the same terminating 120-second kernel alarm as P1b. No participant receives an increased ceiling or an unrestricted fallback.

The driver records package-content hashes, observed environment, configuration registrations, diagnostic source fingerprint, exact requests, worker PID/request binding, native traces, final artifacts, independent verdicts, bounded process streams and kernel telemetry. Import errors, native errors, unsupported options, incorrect outputs, timeouts and OOM remain non-successes. The workflow retains artifacts on failure. The host is an unsealed engineering CI host and every report has `publication_eligible: false`.

Use the [analysis workflow](../../.github/workflows/routing-analysis.yml) or, from a checkout with the pinned P1b dependencies and a delegated Linux cgroup subtree:

```sh
python tools/routing_attribution.py --directory routing-evidence \
  --cgroup-parent /sys/fs/cgroup/sdkbench-routing-study
```

The frozen P1b archives remain immutable. Any future production adapter change must receive a new explicit registration and fresh qualification; this analysis does not retroactively replace their scores.
