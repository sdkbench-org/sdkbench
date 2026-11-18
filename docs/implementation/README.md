# SDKBench implementation plan

This candidate plan translates the [requirements baseline](../requirements/README.md) into a delivery sequence. It preserves all 92 task families and selects ten user workflows with 24 concrete first-wave instances. The documents, reference fixtures and [P0 technical foundation](P0_FOUNDATION.md) are implemented: result contracts, independent evaluators, a strict Linux resource runner and qualification tests. Participant adapters, independent reviewer approval, resolved participant environments and study results are not. The existing SDKBench 0.1 timing harness does not execute this protocol.

| Document | Decision it supports |
| --- | --- |
| [P1a adapters](P1A_ADAPTERS.md) | Native SDK APIs, lifecycle, strict execution, evidence and test scope |
| [P0 foundation](P0_FOUNDATION.md) | Implemented contracts, evaluators, resource controls, tests and remaining review gates |
| [Roadmap](ROADMAP.md) | Phase goals, dependencies, deliverables and exit gates |
| [Priorities](PRIORITIES.md) | Why these needs come first and which needs remain deferred |
| [Phase assignments](PHASE_ASSIGNMENTS.md) / [priority register](priorities.csv) | Every task's phase, need judgment and links to user/capability requirements |
| [First wave](FIRST_WAVE.md) | Concrete inputs, expected outputs, thresholds, negative controls and per-case budgets |
| [Measurement protocol](MEASUREMENT_PROTOCOL.md) | Timing boundaries, statistical decisions, precision, resources and reporting |
| [Comparison scope](COHORTS.md) / [candidate snapshot](CANDIDATES.md) | Eligible roles, initial packages and fair stack attribution |
| [References](REFERENCES.md) | Independent oracle methods, audits and limitations |
| [Machine-readable plan](roadmap.json) / [artifact manifest](artifacts.json) | Reproducible specifications and content hashes |

Protocol: `sdkbench-first-wave`, revision `0.1-candidate-1`, dated 2026-11-18. This is a reviewable candidate freeze, not a released measurement standard. Amendments require review, a new revision, regenerated artifacts and disclosed rationale before participant measurement. No performance conclusion about FlagQuantum or any other SDK follows from this plan.

The first execution study is deliberately bounded to local CPU/offline workflows. Model-specific and hardware-dependent needs remain explicit roadmap commitments; first-wave results cannot establish a global quantum SDK ranking. No live QPU jobs, credentials or device spending are needed to construct or check these artifacts.

Run from the repository root:

```sh
python tools/requirements_docs.py --check
python tools/roadmap_docs.py --check --verify-small
```

Reference generation needs NumPy; integrity and documentation checks use the standard library. `python tools/roadmap_docs.py --freeze` intentionally replaces reference artifacts and their hashes: use it only after reviewing a specification or generator change. `python tools/roadmap_docs.py` updates generated tables. CI checks stored artifacts without requiring cross-platform floating-point files to be byte-identical to regenerated results.
