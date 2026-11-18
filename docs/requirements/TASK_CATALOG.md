<!-- Generated from catalog.json by tools/requirements_docs.py. Do not edit directly. -->

# Task catalog

Requirements baseline 0.1. These are user-task requirements, not implemented benchmarks, executed evidence, or participant support claims. Read [the requirements map](REQUIREMENTS_MAP.md) and [acceptance rules](ACCEPTANCE.md) before using them.

92 task families across 18 user journeys. Each family requires a frozen executable instance specification before measurement.

| Journey | User objective | Task count |
| --- | --- | --- |
| J01 | [Start and maintain a usable project](tasks/j01-start-and-maintain-a-usable-project.md) | 5 |
| J02 | [Express an algorithm faithfully](tasks/j02-express-an-algorithm-faithfully.md) | 6 |
| J03 | [Establish program correctness](tasks/j03-establish-program-correctness.md) | 5 |
| J04 | [Make a program executable on a target](tasks/j04-make-a-program-executable-on-a-target.md) | 5 |
| J05 | [Compute the quantities a study needs](tasks/j05-compute-the-quantities-a-study-needs.md) | 5 |
| J06 | [Compute beyond dense-state limits](tasks/j06-compute-beyond-dense-state-limits.md) | 5 |
| J07 | [Train and differentiate a hybrid model](tasks/j07-train-and-differentiate-a-hybrid-model.md) | 5 |
| J08 | [Answer a scientific or application question](tasks/j08-answer-a-scientific-or-application-question.md) | 6 |
| J09 | [Understand and reduce execution error](tasks/j09-understand-and-reduce-execution-error.md) | 5 |
| J10 | [Run a recoverable device experiment](tasks/j10-run-a-recoverable-device-experiment.md) | 5 |
| J11 | [Study error-corrected computation](tasks/j11-study-error-corrected-computation.md) | 5 |
| J12 | [Design and validate physical controls](tasks/j12-design-and-validate-physical-controls.md) | 5 |
| J13 | [Run a native analog study](tasks/j13-run-a-native-analog-study.md) | 5 |
| J14 | [Run a photonic or continuous-variable study](tasks/j14-run-a-photonic-or-continuous-variable-study.md) | 5 |
| J15 | [Solve through annealing or hybrid optimization](tasks/j15-solve-through-annealing-or-hybrid-optimization.md) | 5 |
| J16 | [Scale and operate a computational study](tasks/j16-scale-and-operate-a-computational-study.md) | 5 |
| J17 | [Exchange, audit and reproduce work](tasks/j17-exchange-audit-and-reproduce-work.md) | 5 |
| J18 | [Turn observations into defensible conclusions](tasks/j18-turn-observations-into-defensible-conclusions.md) | 5 |

## All tasks

| Task | User outcome | Users | Applicability tags |
| --- | --- | --- | --- |
| [T001](tasks/j01-start-and-maintain-a-usable-project.md#t001) | Start a working project in a clean environment | P01, P16 | common |
| [T002](tasks/j01-start-and-maintain-a-usable-project.md#t002) | Determine whether a planned study is supported | P02, P09, P16 | common |
| [T003](tasks/j01-start-and-maintain-a-usable-project.md#t003) | Learn a complete workflow from documentation | P01, P16 | gate, common |
| [T004](tasks/j01-start-and-maintain-a-usable-project.md#t004) | Configure local and remote execution deliberately | P09, P16 | common |
| [T005](tasks/j01-start-and-maintain-a-usable-project.md#t005) | Integrate a new provider or computation component | P16 | common |
| [T006](tasks/j02-express-an-algorithm-faithfully.md#t006) | Build and reuse a parameterized algorithm | P02, P05 | gate |
| [T007](tasks/j02-express-an-algorithm-faithfully.md#t007) | Compose controlled and inverted subroutines with clean workspace | P02 | gate |
| [T008](tasks/j02-express-an-algorithm-faithfully.md#t008) | Prepare a declared input state or data encoding | P02, P05 | gate |
| [T009](tasks/j02-express-an-algorithm-faithfully.md#t009) | Express a measurement-dependent algorithm | P02, P09 | adaptive |
| [T010](tasks/j02-express-an-algorithm-faithfully.md#t010) | Express a mixed-dimensional quantum experiment | P02, P07 | qudit |
| [T011](tasks/j03-establish-program-correctness.md#t011) | Verify an ideal algorithm against an independent oracle | P02, P07 | gate, qudit |
| [T012](tasks/j03-establish-program-correctness.md#t012) | Verify sampling and register interpretation | P01, P02, P08 | gate, adaptive |
| [T013](tasks/j03-establish-program-correctness.md#t013) | Check that a program rewrite preserves intended behavior | P02, P06 | gate, adaptive |
| [T014](tasks/j03-establish-program-correctness.md#t014) | Validate a declared quantum channel or state transformation | P08, P07 | gate, cv |
| [T015](tasks/j03-establish-program-correctness.md#t015) | Locate the stage and cause of an invalid experiment | P16, P02 | common |
| [T016](tasks/j04-make-a-program-executable-on-a-target.md#t016) | Lower an algorithm into an executable instruction set | P06, P09 | gate |
| [T017](tasks/j04-make-a-program-executable-on-a-target.md#t017) | Map a logical algorithm to constrained connectivity | P06, P09 | gate |
| [T018](tasks/j04-make-a-program-executable-on-a-target.md#t018) | Schedule a program under timing and shared-resource constraints | P06, P11 | gate, pulse |
| [T019](tasks/j04-make-a-program-executable-on-a-target.md#t019) | Choose a compiler configuration under a practical budget | P06, P14 | gate |
| [T020](tasks/j04-make-a-program-executable-on-a-target.md#t020) | Determine feasibility before executing a target-incompatible program | P06, P09 | gate, adaptive, pulse |
| [T021](tasks/j05-compute-the-quantities-a-study-needs.md#t021) | Compute only the amplitudes or probabilities needed by a study | P02, P07 | gate, qudit |
| [T022](tasks/j05-compute-the-quantities-a-study-needs.md#t022) | Evaluate a large observable collection correctly | P03, P04, P05 | gate |
| [T023](tasks/j05-compute-the-quantities-a-study-needs.md#t023) | Compute subsystem information without changing subsystem identity | P04, P08 | gate, qudit |
| [T024](tasks/j05-compute-the-quantities-a-study-needs.md#t024) | Work with a Hamiltonian without unnecessary dense expansion | P03, P04, P07 | gate |
| [T025](tasks/j05-compute-the-quantities-a-study-needs.md#t025) | Evaluate a parameter sweep without cross-run contamination | P02, P05, P07 | gate |
| [T026](tasks/j06-compute-beyond-dense-state-limits.md#t026) | Simulate an extended low-entanglement system | P04, P07 | gate |
| [T027](tasks/j06-compute-beyond-dense-state-limits.md#t027) | Determine where an approximate representation stops being reliable | P04, P07 | gate |
| [T028](tasks/j06-compute-beyond-dense-state-limits.md#t028) | Compute a tensor-network output within a memory ceiling | P07, P15 | gate, analog |
| [T029](tasks/j06-compute-beyond-dense-state-limits.md#t029) | Evolve a many-body state with controlled discretization and truncation | P04 | gate, analog |
| [T030](tasks/j06-compute-beyond-dense-state-limits.md#t030) | Select a representation for a requested scientific output | P04, P07 | gate, analog |
| [T031](tasks/j07-train-and-differentiate-a-hybrid-model.md#t031) | Obtain trustworthy derivatives of a quantum model | P05, P02 | gate, cv, analog, pulse |
| [T032](tasks/j07-train-and-differentiate-a-hybrid-model.md#t032) | Train a minibatched hybrid quantum/classical model | P05 | gate, cv |
| [T033](tasks/j07-train-and-differentiate-a-hybrid-model.md#t033) | Converge a variational objective under a fixed budget | P05, P02 | gate |
| [T034](tasks/j07-train-and-differentiate-a-hybrid-model.md#t034) | Use curvature or derivative products in a learning routine | P05, P02 | gate, cv, analog, pulse |
| [T035](tasks/j07-train-and-differentiate-a-hybrid-model.md#t035) | Optimize a noisy sampled model with a shot budget | P05, P08 | gate, adaptive, cv, analog |
| [T036](tasks/j08-answer-a-scientific-or-application-question.md#t036) | Estimate molecular ground or excited-state energies | P03 | gate |
| [T037](tasks/j08-answer-a-scientific-or-application-question.md#t037) | Predict a many-body dynamics or correlation study | P04 | gate, analog, qudit, cv |
| [T038](tasks/j08-answer-a-scientific-or-application-question.md#t038) | Solve a constrained optimization instance and decode the answer | P14 | gate, annealing |
| [T039](tasks/j08-answer-a-scientific-or-application-question.md#t039) | Estimate a phase or amplitude with complete oracle accounting | P02 | gate, adaptive |
| [T040](tasks/j08-answer-a-scientific-or-application-question.md#t040) | Extract a useful observable from a quantum linear-algebra routine | P02, P04 | gate |
| [T041](tasks/j09-understand-and-reduce-execution-error.md#t041) | Predict outputs of a declared noisy experiment | P08, P07 | gate |
| [T042](tasks/j09-understand-and-reduce-execution-error.md#t042) | Integrate a time-dependent open quantum system | P08, P04 | gate, analog, pulse |
| [T043](tasks/j09-understand-and-reduce-execution-error.md#t043) | Correct measurement bias with accounted calibration uncertainty | P08, P09 | gate |
| [T044](tasks/j09-understand-and-reduce-execution-error.md#t044) | Assess extrapolation or cancellation at matched total cost | P08, P09 | gate |
| [T045](tasks/j09-understand-and-reduce-execution-error.md#t045) | Validate a frozen device or noise model on unseen experiments | P08, P09 | gate, analog, pulse |
| [T046](tasks/j10-run-a-recoverable-device-experiment.md#t046) | Select a device capable of a planned experiment | P09, P16 | gate, adaptive, analog, pulse, cv, annealing |
| [T047](tasks/j10-run-a-recoverable-device-experiment.md#t047) | Prepare and submit an explicitly authorized experiment batch | P09 | gate, adaptive, analog, pulse, cv, annealing |
| [T048](tasks/j10-run-a-recoverable-device-experiment.md#t048) | Recover asynchronous or partially completed work | P09, P16 | common |
| [T049](tasks/j10-run-a-recoverable-device-experiment.md#t049) | Recover logical observations from compiled device results | P09, P08 | gate, adaptive |
| [T050](tasks/j10-run-a-recoverable-device-experiment.md#t050) | Repeat an experiment while retaining acquisition context | P09, P08 | gate, analog, pulse, cv, annealing |
| [T051](tasks/j11-study-error-corrected-computation.md#t051) | Construct and validate a code with named logical observables | P10 | qec |
| [T052](tasks/j11-study-error-corrected-computation.md#t052) | Run repeated syndrome-extraction memory experiments | P10 | qec, adaptive |
| [T053](tasks/j11-study-error-corrected-computation.md#t053) | Build and sample an explicitly scoped detector error model | P10 | qec |
| [T054](tasks/j11-study-error-corrected-computation.md#t054) | Evaluate a decoder on held-out detector events | P10 | qec |
| [T055](tasks/j11-study-error-corrected-computation.md#t055) | Estimate resources for a specified logical computation | P10, P02 | qec |
| [T056](tasks/j12-design-and-validate-physical-controls.md#t056) | Express physical controls with explicit units and channels | P11 | pulse |
| [T057](tasks/j12-design-and-validate-physical-controls.md#t057) | Schedule simultaneous and feedback-dependent control | P11, P06 | pulse, adaptive |
| [T058](tasks/j12-design-and-validate-physical-controls.md#t058) | Predict a calibrated driven-system response | P11, P08 | pulse |
| [T059](tasks/j12-design-and-validate-physical-controls.md#t059) | Optimize a pulse under physical and evaluation constraints | P11 | pulse |
| [T060](tasks/j12-design-and-validate-physical-controls.md#t060) | Use the correct calibration for a gate-level experiment | P11, P09 | pulse, gate |
| [T061](tasks/j13-run-a-native-analog-study.md#t061) | Describe a native analog experiment | P12, P04 | analog |
| [T062](tasks/j13-run-a-native-analog-study.md#t062) | Compute observables of a native analog evolution | P12, P04 | analog |
| [T063](tasks/j13-run-a-native-analog-study.md#t063) | Prepare an analog program for a constrained device | P12, P09 | analog |
| [T064](tasks/j13-run-a-native-analog-study.md#t064) | Interpret analog measurements with loading and loss records | P12, P08, P09 | analog |
| [T065](tasks/j13-run-a-native-analog-study.md#t065) | Compare analog schedules for the same physical objective | P12, P14 | analog |
| [T066](tasks/j14-run-a-photonic-or-continuous-variable-study.md#t066) | Prepare and transform a mode-based input state | P13 | cv |
| [T067](tasks/j14-run-a-photonic-or-continuous-variable-study.md#t067) | Compute Gaussian optical transformations and correlations | P13 | cv |
| [T068](tasks/j14-run-a-photonic-or-continuous-variable-study.md#t068) | Compute a non-Gaussian process with controlled Fock truncation | P13 | cv |
| [T069](tasks/j14-run-a-photonic-or-continuous-variable-study.md#t069) | Analyze photon-counting or quadrature observations | P13, P08 | cv |
| [T070](tasks/j14-run-a-photonic-or-continuous-variable-study.md#t070) | Transfer a mode program to another execution boundary | P13, P16 | cv, adaptive |
| [T071](tasks/j15-solve-through-annealing-or-hybrid-optimization.md#t071) | Translate an application into a quadratic or constrained model | P14 | annealing |
| [T072](tasks/j15-solve-through-annealing-or-hybrid-optimization.md#t072) | Embed a logical model onto a physical topology | P14, P09 | annealing |
| [T073](tasks/j15-solve-through-annealing-or-hybrid-optimization.md#t073) | Run a controlled annealing sampling study | P14, P09 | annealing |
| [T074](tasks/j15-solve-through-annealing-or-hybrid-optimization.md#t074) | Evaluate feasibility and postprocessing honestly | P14 | annealing |
| [T075](tasks/j15-solve-through-annealing-or-hybrid-optimization.md#t075) | Compare hybrid optimization at a matched end-to-end budget | P14 | annealing |
| [T076](tasks/j16-scale-and-operate-a-computational-study.md#t076) | Run the same output contract on supported compute devices | P15, P07 | gate, analog, cv |
| [T077](tasks/j16-scale-and-operate-a-computational-study.md#t077) | Expand a single computation through distributed state or tensor partitioning | P15, P07 | gate, analog |
| [T078](tasks/j16-scale-and-operate-a-computational-study.md#t078) | Increase throughput of independent experiments or training examples | P15, P05 | common, gate |
| [T079](tasks/j16-scale-and-operate-a-computational-study.md#t079) | Resume a computation or training run after interruption | P15, P05 | common, gate |
| [T080](tasks/j16-scale-and-operate-a-computational-study.md#t080) | Determine the largest completed study under real resource limits | P15, P07 | gate, analog, cv |
| [T081](tasks/j17-exchange-audit-and-reproduce-work.md#t081) | Exchange a program through a declared standard/profile | P16, P02 | gate, adaptive, pulse |
| [T082](tasks/j17-exchange-audit-and-reproduce-work.md#t082) | Round-trip an artifact across different conventions | P16, P02 | gate, adaptive, qudit, cv, annealing |
| [T083](tasks/j17-exchange-audit-and-reproduce-work.md#t083) | Reproduce a published software result from its evidence bundle | P16, P01 | common |
| [T084](tasks/j17-exchange-audit-and-reproduce-work.md#t084) | Identify which components actually performed the work | P16, P07 | common |
| [T085](tasks/j17-exchange-audit-and-reproduce-work.md#t085) | Detect semantic or operational regressions after an upgrade | P16 | common, gate |
| [T086](tasks/j18-turn-observations-into-defensible-conclusions.md#t086) | Estimate an observable with a specified uncertainty target | P08, P04 | gate, analog, cv |
| [T087](tasks/j18-turn-observations-into-defensible-conclusions.md#t087) | Plan measurements for an energy or correlation target | P03, P08 | gate |
| [T088](tasks/j18-turn-observations-into-defensible-conclusions.md#t088) | Reconstruct a state or process with validation beyond the fitted data | P08, P09 | gate, cv |
| [T089](tasks/j18-turn-observations-into-defensible-conclusions.md#t089) | Estimate a predefined observable family from reusable measurement records | P08, P04 | gate |
| [T090](tasks/j18-turn-observations-into-defensible-conclusions.md#t090) | Produce a scientific report that retains model failures and uncertainty | P08, P09, P16 | common |
| [T091](tasks/j08-answer-a-scientific-or-application-question.md#t091) | Train and evaluate a quantum-kernel predictor | P05 | gate |
| [T092](tasks/j02-express-an-algorithm-faithfully.md#t092) | Execute a measurement-based computation pattern | P02, P10 | mbqc, adaptive |
