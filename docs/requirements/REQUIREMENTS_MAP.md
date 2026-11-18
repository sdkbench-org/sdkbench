# Requirements map

## Purpose and intended decisions

SDKBench evaluates how effectively quantum software helps users finish meaningful work. It must answer which tasks are supported, whether outputs are correct, what quality and uncertainty are obtained, what resources are consumed, and where users encounter limitations. It must enable improvement of every participant, including projects affiliated with benchmark maintainers.

The unit of assessment is a frozen task instance with a user outcome and verifiable output contract. An operation-level benchmark is useful when it explains a task bottleneck; its existence or speed alone does not establish user value. An algorithm demonstration may be useful for education or verification without providing practical quantum advantage. Those purposes must not be conflated.

## Objects under assessment

| Object | Responsibility | Appropriate evidence |
| --- | --- | --- |
| Integrated quantum development kit | Connect formulation, program expression, compilation/execution and interpretation | Role-specific workflow completion, coverage, quality and total cost |
| Language, frontend or interchange tool | Preserve intended program semantics and expose diagnostics | Expressiveness, valid lowering, conversion fidelity and frontend overhead |
| Compiler or synthesis component | Produce a legal equivalent implementation under target constraints | Semantic checks, target legality and quality/time/resource tradeoffs |
| Simulation or numerical engine | Produce requested quantum outputs within error and resource budgets | Correctness, error-cost curves, useful capacity and scaling |
| Differentiation or hybrid-learning component | Support mathematically correct learning/sensitivity workflows | Derivative validation, convergence, predictive evaluation and total training cost |
| Domain tool | Help complete a scientific, optimization, control or QEC task | Domain-specific validity, provenance and time/resources to the requested result |
| Provider or orchestration layer | Prepare, manage and recover executable experiments | Payload fidelity, authorization, lifecycle behavior, result identity and recovery |

These categories can overlap. A pipeline may use multiple independently supplied components. Integrated usability and native-component performance are separate claims. External engines are allowed where the task contract permits them; attribution and costs must remain visible. A comparison must not quietly credit one frontend with the work of an external engine while measuring another participant's native implementation under a different boundary.

## Target users

These role descriptions are design hypotheses grounded in established workflows, not the results of completed interviews. Users may hold more than one role. No role is defined by a preferred SDK, programming language or hardware vendor.

| ID | Target user | Real outcome sought |
| --- | --- | --- |
| <a id="p01"></a>P01 | Learner and educator | Learn, reproduce and explain a correct quantum computation without hidden setup or conventions |
| <a id="p02"></a>P02 | Algorithm researcher | Express, compose and validate algorithms, adaptive routines and their resource requirements |
| <a id="p03"></a>P03 | Chemistry and materials researcher | Obtain scientifically specified energies or spectra with reproducible physical-model inputs |
| <a id="p04"></a>P04 | Many-body and dynamics researcher | Compute states, correlations and time-dependent quantities with controlled numerical errors |
| <a id="p05"></a>P05 | Machine-learning researcher | Train and evaluate quantum/hybrid or kernel models under data and compute budgets |
| <a id="p06"></a>P06 | Compiler researcher | Produce valid target programs with defensible quality and compilation costs |
| <a id="p07"></a>P07 | Simulation developer and user | Obtain requested outputs at useful scale, accuracy and memory cost |
| <a id="p08"></a>P08 | Noise and estimation researcher | Model errors, analyze observations and quantify uncertainty or mitigation benefit |
| <a id="p09"></a>P09 | Device experimenter | Execute a traceable experiment and correctly interpret or recover its results |
| <a id="p10"></a>P10 | Error-correction and fault-tolerance researcher | Evaluate code, detector, decoder, logical-operation and resource assumptions |
| <a id="p11"></a>P11 | Control and calibration researcher | Express physical controls and obtain valid response, calibration or optimization results |
| <a id="p12"></a>P12 | Analog-computing researcher | Specify geometry/interactions and analyze native continuous-time experiments |
| <a id="p13"></a>P13 | Photonic and continuous-variable researcher | Study mode-based processes with explicit conventions, losses and truncation |
| <a id="p14"></a>P14 | Optimization practitioner | Obtain feasible decoded solutions and quantify solution quality and total cost |
| <a id="p15"></a>P15 | HPC and platform operator | Allocate resources, scale independent or partitioned work and recover studies |
| <a id="p16"></a>P16 | Application and integration engineer | Install, extend, integrate, deploy, debug, exchange and reproduce workflows |

Journey-level requirements and detailed acceptance criteria are in the [task catalog](TASK_CATALOG.md). A task may serve several roles; duplicate role membership must not multiply its statistical weight.

## Computing models and applicability

The map deliberately extends beyond currently implemented gate-circuit tests. Applicability tags distinguish computing models, control levels and workflow domains; they are not mutually exclusive and must not be treated as a single qubit-count ladder.

| Tag | Boundary and user intent |
| --- | --- |
| `common` | Environment, evidence, analysis or operational behavior that can apply across models; not a requirement that every tool implement every common task |
| `gate` | Static discrete gate programs on qubits |
| `adaptive` | Measurement/reset and classical dependence, including bounded feedback workflows |
| `qudit` | Explicit finite local dimensions beyond qubits or mixed-dimensional registers |
| `mbqc` | Graph states, measurement patterns, causal dependencies and byproduct/frame corrections |
| `analog` | Native Hamiltonians, geometry and continuous-time schedules rather than an implicitly preferred gate lowering |
| `pulse` | Physical control waveforms, channels, frames and timing constraints |
| `cv` | Bosonic/photonic modes, quadratures, Gaussian/non-Gaussian evolution and explicit finite-cutoff approximations |
| `annealing` | Quadratic/constrained models, embedding, schedules, sampling and logical solution decoding |
| `qec` | A workflow domain: checks, repeated syndrome extraction, detector models, decoding, logical programs and resource assumptions |

Task tags list the allowed model/domain contexts, not a demand that each participant support every tag. Some tags can be combined: a QEC experiment may use adaptive gate execution; a photonic program may implement measurement-based computation. A frozen instance must name its actual context and required edges. The matrix marks conditional functions explicitly. For example, annealing embedding/decoding requirements belong to an annealing-backed optimization path, not automatically to a gate-based optimizer solving the same application problem.

Unsupported functions in an applicable cohort remain unsupported. Non-applicability requires a predeclared scientific/role boundary, not a new exception created after an SDK fails. A specialist decoder does not owe photonic simulation, but it does owe the decoder task contract in a decoder cohort. A broad tool claiming a user role must disclose applicable missing tasks.

## Full workflow lifecycle

| Stage | User question | Required connection to a later outcome |
| --- | --- | --- |
| `setup` | Can I obtain and configure a usable environment? | Reproducible, documented prerequisites and an independently checked first result |
| `formulate` | Does this model represent my question? | Preserved physical/application semantics, units, domains and assumptions |
| `express` | Can I represent the intended computation? | An inspectable program, input and output contract |
| `verify` | What evidence shows the behavior is correct? | Independent oracles, invariant checks and explicit validation limits |
| `compile` | Can this target execute the program legally? | Preserved semantics, legal instructions/mapping/timing and accounted compilation cost |
| `execute` | Can I obtain the requested result within budget? | Actual execution provenance, resources, output identity and failures |
| `estimate` | What can I conclude from the outputs? | Valid estimators, uncertainty, denominators and scientific interpretation |
| `optimize` | Can I reach an objective or quality target? | Convergence/success distributions and complete search/evaluation costs |
| `operate` | Can I scale, monitor, interrupt and recover it? | Reconciled work, preserved state and resource/fault evidence |
| `exchange` | Can another person or tool reproduce or consume it? | Semantic retention, evidence bundles, formats and explicit losses |

Cross-cutting requirements include deterministic/stochastic semantics, units, wire/mode/variable order, parameter identity, initial-state assumptions, precision, approximation, target context, resource bounds, observability, result provenance and failure classification. They must be instantiated where relevant rather than awarded as independent feature-count points.

## Three assessment levels

| Level | Purpose | Example |
| --- | --- | --- |
| User task | Establish whether meaningful work is completed | Obtain a molecular energy within a specified total error and resource budget |
| Capability | Explain which required abilities enable or block that work | Model construction, state preparation, estimation and optimization |
| Function/operation | Locate a concrete semantic or performance bottleneck | Preserve an energy offset, bind parameters or evaluate a Pauli sum |

Task outcomes are primary. Function microbenchmarks remain linked diagnostic evidence. An implementation should not score well overall merely by exposing many fast methods while failing the user outcome. Conversely, a complete workflow can legitimately use reusable components if the task allows them and costs/provenance are disclosed.

## Scope boundaries

- SDKBench measures software correctness, capabilities, operational behavior and resource efficiency. Physical QPU quality is a separate experimental property. Device results may support a controlled software workflow comparison only with acquisition/drift context.
- Classical preprocessing, simulation, optimization, repair, postprocessing and externally supplied work are included or excluded according to an explicit measurement boundary, never silently omitted.
- Domain packages, proprietary services and inaccessible devices remain in the requirements map. Access limitations restrict evidence, not the definition of user need.
- Energy, financial-cost or environmental-impact claims require a separately specified measurement boundary and direct measurements or dated price assumptions. No such claim follows automatically from wall time.
- Popularity, organization size, number of APIs, lines of code and maintainer preference are not substitutes for task acceptance. Usability claims require a structured procedure and, for user-success claims, actual user evidence.
- This baseline does not claim practical quantum advantage, universal applicability of one algorithm, all-purpose production readiness or compliance with every external specification.

## How completeness is reviewed

Completeness is a maintained argument, not an absolute claim about a permanently closed field. Review the Cartesian axes conceptually: user role, workflow stage, computing model, output type, execution setting, error regime and failure mode. A full Cartesian execution grid would be wasteful and scientifically invalid for many combinations.

Reviewers must identify meaningful intersections, document intentional non-intersections and propose missing user tasks. Every function must trace back to at least one task, and each task must state its need, output and independent acceptance rule. [COVERAGE.md](COVERAGE.md) shows structural coverage; [GOVERNANCE.md](GOVERNANCE.md) defines review and revision. Domain review remains pending for this first baseline and must be recorded before the affected cohort is frozen.
