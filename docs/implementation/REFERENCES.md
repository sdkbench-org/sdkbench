# Independent references and fixture provenance

## Construction and independence

[roadmap_reference.py](../../tools/roadmap_reference.py) constructs fixtures and expected outputs using NumPy and mathematical definitions. It imports no evaluated SDK, compiler, autodiff engine or provider client and makes no network/device calls. “Independent” here means independent of participants, not an assertion of external certification: authorship and domain review must still be disclosed, and independent reviewer approval remains a P0 gate.

[artifacts.json](artifacts.json) records content SHA256 hashes, the generator hash and the actual Python/NumPy generation versions. The requirements catalog hash is pinned in [roadmap.json](roadmap.json). All 24 input and reference artifacts are versioned. Explicit parameter, coefficient, dataset, initialization and operation values are stored in fixtures, so a participant does not need the generator's random implementation. Generator parameters use a SHA256 counter, not an unspecified library RNG. Logical q0 is index bit 0; Pauli-word character j refers to logical qj; rotations are `exp(-i*angle*Pauli/2)` and angles are radians.

## Reference methods by workflow

| Workflow | Oracle and independent check | Limits |
| --- | --- | --- |
| W01 | Analytic local X/Y/Z and adjacent ZZ moments for RY/RZ rotations followed by a CZ chain; dense Kronecker validation at n=4, all seven bindings | Structured graph-state family only; n=24 reference does not allocate a 24-qubit state |
| W02 | Teleportation identity for six Pauli input states and 18 Bob measurement contexts, including both classical bits; dense projected-branch density checks; bounded geometric stopping law and exact reset | Ideal joint distributions, not feedback latency or noisy device modeling |
| W03 | Explicit ideal block-state propagation and full small operator comparison against dense Kronecker/permutation construction; independently checked target constraints required in future evaluator | n=6 full operator, n=8/12 three probe states; no optimal-route claim; stored rounded probe hashes are audit markers, never floating-point acceptance thresholds |
| W04 | Exact ideal state propagation followed by independent Pauli-index permutation sums for 64 requested terms and weighted sum; small dense state/convention anchors | Finite float64 numerics; no shot allocation or chemistry model validity claim |
| W05 | Analytic rotation derivative matrices and tangent propagation for all shared occurrences; independent five-point dense finite differences at n=3/4 | Small finite-difference audit is not full production gradient implementation; no participant autograd output used as gold |
| W06 | Closed-form quantum moments, explicit classical chain rule and plain-SGD recurrence; small quantum-feature dense check and independent finite-difference joint-gradient audit | Structured non-entangled feature regression; all 49 states per initialization stored; no general ML/application advantage claim |
| W07 | Dense independently assembled TFIM Hamiltonian and spectral evolution; separate block-state S2 digital-program reference; both physical and digital outputs stored | n=4/8 closed system, finite numerical reference and fixed Trotter schedule; not general analog/device fidelity |
| W08 | Product rotation probabilities plus inverse-CNOT permutation; small dense probability audit; all categories stored | Assumes independent ideal shots at the declared law |
| W09 | Explicit finite-state transition and deduplicated event-ledger postconditions independent of client code | Offline protocol fixture, not evidence a real client supports the contract; transport bindings remain to implement/review |
| W10 | Explicit QASM text and separately defined small matrix behavior/classical permutation; exact adaptive branch/reset identity | Declared subsets only; independent parser/evaluator and rejection mutation tests remain to implement |

For a statevector reference, block updates and the small dense construction share rotation definitions but use different application algorithms. Analytic RY, Bell and complex-Y anchors catch convention errors; this is useful corroboration, not fully independent implementations of every mathematical primitive. Before release, an independent reviewer must audit definitions and add a separately authored evaluator or higher-precision checks wherever residual bounds warrant it. Do not treat fixture hashes as proof that their contents are correct.

`--verify-small` checks analytic/dense/derivative/branch identities and regenerates 12 small reference artifacts for tolerant numeric comparison. It avoids asserting byte-identical cross-platform eigensolver output. Reference generation also checks the dynamics physical error target and all five training-start improvement criteria. Probability totals, finite outputs, numerical residuals and every required negative control must additionally pass the production evaluator before participant timings. The sampling upper bound and its derivation are specified in the [measurement protocol](MEASUREMENT_PROTOCOL.md), not borrowed as a participant-specific threshold.

## Primary workflow/specification sources

The [requirements source register](../requirements/SOURCES.md) grounds the user workflows across domains. These sources provide semantic context; no vendor's API or feature inventory defines the scope. Pin applicable specification/source revisions in the eventual execution manifest.

- [OpenQASM language specification](https://openqasm.com/): interchange/control semantics; first-wave subsets are explicitly narrower than whole-language conformance.
- [NumPy linear algebra documentation](https://numpy.org/doc/stable/reference/generated/numpy.linalg.eigh.html): Hermitian eigensolver interface used for small reference evolution; source/environment hashes belong in execution evidence.
- [CUDA-Q simulator backend documentation](https://nvidia.github.io/cuda-quantum/latest/using/backends/sims/svsims.html): illustrates why backend and precision attribution matter; no performance comparison is inferred from its description.
- [TensorCircuit-NG upstream repository](https://github.com/tensorcircuit/tensorcircuit-ng): identifies the maintained candidate project; metadata and registration are still separately reviewed.
- [Candidate package snapshot](CANDIDATES.md): exact observed versions and primary PyPI metadata URLs, dated 2026-11-18; these do not establish tested compatibility or task support.

## Changes and reproducibility

To change a fixture/reference, review the need and mathematical contract first, increment the protocol revision, update explicit inputs and provenance, regenerate using `--freeze`, inspect output differences and record the review. Invalidate affected participant results and rerun all affected stacks. Never update references to agree with a favored participant. Retain prior released artifacts and amendments so external readers can reconstruct which answer and thresholds applied to each result.
