# User-need priorities and selection rationale

## Separate importance from deliverability

The requirements personas describe intended users, not completed interviews or measured market demand. Priority judgments therefore remain provisional and auditable. No package's current features, performance, sponsorship or maintainer relationship is an input to a need score. FlagQuantum receives the same rules, missing-support status and failure criteria as every participant.

The ordinal planning score is `4 * outcome_impact + 3 * wrong_answer_consequence + 2 * cross_journey_reuse`, with each dimension in 1..3. The coefficients express policy, not a validated quantitative demand model. There is no score precision beyond those judgments and no SDK score derives from them.

| Dimension | 1 | 2 | 3 |
| --- | --- | --- | --- |
| Outcome impact | Convenience or optional diagnostic | Important supporting outcome | Direct scientific, experimental or operational outcome |
| Wrong-answer consequence | Easily noticed/local rework | Misleading local interpretation or wasted compute | Invalid scientific conclusion, silent semantic loss or incorrect/costly operation |
| Cross-journey reuse | Mainly specialist/local | Several related workflows | Measurement-wide or broad integration dependency |

The [register](priorities.csv) records all 92 task judgments and delivery rationale. Current scores use coarse journey-level defaults with explicit foundational exceptions; they are not individually validated stakeholder estimates. Review individual scores with users before a protocol release. Sensitivity to alternative weights must be reported if a future selection claims to be score-driven. The first portfolio is constrained by outcome coverage and trustworthy bounded references, so sorting this score alone does not recreate phase order.

Delivery readiness is a separate gate: independently checkable outputs, bounded costs, semantic translation review and infrastructure availability. A high-value need stays high-value when a reference or device is difficult to obtain. P2 specialist lanes can advance as soon as those gates pass. Missing participant support never makes a user need out of scope.

## Why the first ten workflows

| Workflow | Need and selection reason | Intentional limitation / follow-on |
| --- | --- | --- |
| W01 parameter reuse | Avoid incorrect parameter binding and leaked state in repeated experiments; broadly reused by optimization and sweeps | A structured graph circuit with analytic moments, not a generic worst-case statevector test; extra/missing binding and shape diagnostics remain required |
| W08 sampling | Users consume mapped shot records, so output order and sampling uncertainty must be trusted early | Small asymmetric distributions; later correlated noise, large alphabets and rare-event studies |
| W04 observables | Scientific users need many local/nonlocal moments and weighted energies, not only state throughput | Fixed exact circuits/Pauli requests, not full chemistry performance or statistical measurement allocation |
| W05 derivatives | A wrong shared-parameter Jacobian invalidates an optimizer even if forward outputs are correct | Exact first derivatives; later higher-order, stochastic, nonunitary and simulator-specific methods |
| W07 dynamics | Compare physical predictions at a stated Hamiltonian/time and distinguish software from discretization error | Two open TFIM instances; later convergence studies, other Hamiltonians and requested-error algorithm freedom |
| W03 compilation | Users need hardware-legal algorithms with preserved logical meaning and visible compilation cost | Abstract line/grid full-CZ targets, not calibrated hardware, optimal routing or all basis sets |
| W06 training | Catch errors across quantum/classical boundaries and account for an entire learning trajectory | Structured analytic regression diagnostic; no entangled ML, real-dataset generalization or quantum advantage claim |
| W02 adaptive protocols | Feed-forward, measurement, stopping and reset are real computational semantics | Teleportation and bounded loop; later general control, latency, QEC and live feedback |
| W10 interchange | An executable artifact must survive tool boundaries without dropped features | Two explicitly declared QASM subsets; not whole-language conformance or general portability certification |
| W09 recovery | Users cannot tolerate silently duplicated work or erased partial results | Offline client/event contract; no device reliability, provider queue or payment performance claim |

These tasks deliberately span scientists, algorithm/ML researchers, compiler/device users, experiment operators and integration engineers. They do not fully represent all 16 personas. Teachers, specialist-model researchers, control/calibration engineers, QEC architects, large-system operators and other users retain explicit requirements and later lanes in the [roadmap](ROADMAP.md). A first-wave-only report must state these representation gaps.

## Deferred needs and review controls

Noise, mitigation, chemistry/optimization, QEC, pulses, analog, photonics, annealing, qudits, measurement-based computation, large-scale resources and prospective live-device work remain required directions. They need additional physical/error references, expert review or resource authorization; their omission from this first local study says nothing about their user value or any SDK's importance.

Before releasing a protocol, record stakeholder reviews across personas and model lanes, disagreements, conflicts of interest and a rationale for every exclusion or deferred variant. Revisit scores when new evidence changes a need, not when a participant performs poorly. Freeze task selection, thresholds, environments and public reporting policy before participant timings. Correct a benchmark defect transparently, invalidate affected results and rerun every affected stack under the amended revision.
