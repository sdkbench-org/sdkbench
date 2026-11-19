# Application compiler corpus and prospective qualification

Status: numeric recipes, a content-addressed 60-case development bundle builder,
independent physics anchors and opt-in native adapter conformance are implemented.
No prospective draw or resource-qualified application campaign is claimed here.
The original frozen bundle, historical adapters, acceptance thresholds and
measurement budgets remain unchanged.

## Users and application scope

A circuit developer needs a correct executable for a device topology. Targets
here are abstract connected undirected graphs with arbitrary local unitaries,
full CZ interactions, identity initial placement and no additional physical
ancillas. Application work qubits are explicit within the logical width. Final
permutations must be reported and reconstructed during acceptance.

| Family | Exact workload | Independent application anchor |
| --- | --- | --- |
| `qaoa` | Two weighted MaxCut cost/mixer layers after H preparation; permuted ring plus matching interaction graph; weights in [0.5,1.5), gamma/beta in [-pi,pi) | Direct diagonal cut-cost Hamiltonian and dense transverse-X mixer exponentials |
| `ising` | Three symmetric product-formula steps with dt=0.2 on a permuted open interaction chain; positive transverse fields and ZZ couplings in [0.5,1.5) | Ordered dense exponentials of the specified factors |
| `hopping` | Half-filled initial occupation and two layers of disjoint orbital-pair hopping rotations with Jordan-Wigner parity strings | Fock-space creation/annihilation matrices, complete operator and particle-number checks |
| `qft` | Complete positive-sign QFT including terminal bit reversal; controlled phases decomposed into RZ and RZZ | Analytic DFT matrix, all input columns and one common global phase |
| `repetition` | Coherent three-data-qubit bit-flip correction, two explicit syndrome qubits, one selected X error and phase-bearing spectator operations | Complete Toffoli permutation, recovered logical amplitudes and retained syndrome |

These are bounded application slices. Hopping is not a complete UCCSD ansatz or
molecular energy calculation. QFT is a phase-estimation component. Digital Ising
equivalence does not certify continuous-time Trotter error. Repetition correction
retains its syndrome; it does not claim reset, feed-forward, fault tolerance or
a QEC threshold. Other requirements remain in the requirements map.

Every family has widths 6, 8 and 12 and four target types: line, ring,
2-by-(n/2) grid and connected sparse graph (spanning path plus matching).
The same family/width source is reused across targets. Domain-separated SHA-256
draws determine parameters, labels, interaction order, target chords and three
input probes. QFT application structure is fixed; its probes and sparse target
vary. The generator and physics references import no participant SDK.

Conventions: q0 is the least significant bit; R(P,theta)=exp(-i theta P/2).
Hopping is exp(-i theta H) with
H=a†p aq+a†q ap=(Xp Xq+Yp Yq) Z(parity)/2. MaxCut uses
C=sum w(1-Za Zb)/2 and exp(-i gamma C), up to one common global phase.
The Clifford+T Toffoli decomposition retains relative phases.

## Acceptance, resources and identity

The new builder copies the frozen width-specific W03 acceptance and resource
objects verbatim, retains the execution profile and changes protocol/fixture
identities. Existing bundle hashing, request isolation, supervisor, campaign and
independent replay remain authoritative. Both generator source hashes and the
base bundle hash are retained. Candidate registrations bind the actual harness
fingerprint.

- Width 6: complete 64-by-64 operator comparison, one global phase.
- Widths 8 and 12: three complete output probes, explicitly labeled
  `three-probes-only`; these do not prove universal equivalence.
- Absolute semantic tolerance 1e-8; normalization bound 1e-10; zero illegal
  interactions; terminating 120-second per-compilation alarm.
- Cumulative case caps 600/900/1800 seconds by width; one CPU, one numerical
  thread, 16 GiB, Linux cgroup/seccomp, no sockets, memory-swap restriction and
  descendant cleanup.
- Ten fresh-process blocks, two retained warmups and three measured compilations
  per block; retain the existing compiler seeds even for deterministic SDKs.

A complete registration has a 66,000-second cumulative case ceiling (20 cases
per width); four registrations have a 264,000-second ceiling, excluding external
installation/build overhead. These are worst-case ceilings, not runtime
estimates. Record host wall time separately. A reduced cohort must be selected
before execution and cannot be called the complete study. Never remove failed
or expensive cases after inspection.

## Candidate and layout controls

Use the existing source/wheel admission protocol for immutable FlagQuantum,
Qiskit and Cirq builds. Ordinary, target-artifact and expert workflows remain
distinct registrations. Candidate numeric builders now handle all existing W03
operations, including RX and RZZ. Historical P1a/P1b builders remain unchanged.
Symbolic candidate inputs explicitly report unsupported rather than silently
binding or ignoring angles.

Report open-layout output as complete workflow cost. FlagQuantum's restored
artifact layout differs from the Qiskit/Cirq free final layouts, so that
comparison cannot isolate synthesis. A separately registered matched-restoration
cohort uses the separately registered `flagquantum-ordinary-restored`,
`qiskit-transpile-restored` and `cirq-route-cz-restored` workflows. See the
[matched-layout control](COMPILER_MATCHED_LAYOUT_CONTROL.md) for its exact
obligation, timing, cost accounting and limitations. The generator does not
select workflows or establish a prospective draw.

## Prospective draw procedure

1. Merge and freeze recipes, topology rules, widths, layers, acceptance, budgets
   and cohort before examining candidate results. Retain the integrated
   generator/harness revision, source hashes and review record.
2. Freeze all compiler builds, dependencies, registration options and environment,
   including layout/search controls. Retain the exact registration bytes/hashes.
3. After both freezes, draw one 32-byte OS-random nonce. Retain its value,
   timestamp and already-frozen selection hashes in an append-only draw record.
   Never redraw, filter cases or search seeds. Public test nonces are development.
4. Generate every case; retain the complete hash-manifested bundle. Run the
   preregistered cohort serially with counterbalanced SDK order and the existing
   supervisor. Preserve unsupported, install/compile/semantic failures, timeouts
   and OOMs.
5. Independently replay every outcome and publish cases, metrics and regressions.
   If results inform compiler tuning, reclassify the corpus as development and
   obtain fresh prospective inputs only after freezing the next candidates.

The builder labels every output `development`. A nonce does not prove event
ordering, and changing that label cannot establish prospectivity. An audited
draw record and execution history are still required; no automated draw service
or prospective result is introduced here.

## Reproduction and remaining gates

```bash
PYTHONPATH=src python -m sdkbench.candidates.application_bundle \
  --base docs/implementation --output /tmp/sdkbench-app-development \
  --nonce 0101010101010101010101010101010101010101010101010101010101010101
PYTHONPATH=src python -m pytest tests/test_candidate_applications.py \
  tests/test_candidate_application_bundle.py -q
```

Expected: a new verified 60-case bundle, deterministic identity, unchanged frozen
files and passing physics anchors. Existing output paths are refused. The
existing candidate CLI accepts this directory through `run --bundle` and
`replay --bundle`, with required registrations and Linux resource delegation.
Set `SDKBENCH_NATIVE_CANDIDATE_TESTS=1` to opt into native semantic conformance;
those tests are not resource-qualified performance measurements.

Standard QAOA is described by
[Farhi et al. (2014)](https://arxiv.org/abs/1411.4028). The formulas above,
Jordan-Wigner Fock-space anchors and analytic QFT matrix are the executable
specification, rather than a participant serving as gold implementation.

Before comparative claims: integrated immutable candidates, matched-layout
attribution controls, recorded prospective draw, complete outcomes including
compile time/memory/full-CZ/common-depth metrics, independent replay, adapter
review and publication-host qualification remain required. No generator or local
test result establishes a global ranking or superiority.

The first reduced matched-layout run is specified in
[the application campaign](COMPILER_APPLICATION_CAMPAIGN.md). Its workflow and
preparation record do not themselves establish an executed prospective result.
