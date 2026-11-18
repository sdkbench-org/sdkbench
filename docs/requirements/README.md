# SDKBench requirements baseline

**Status:** Draft requirements baseline 0.1, dated 2026-11-18. This is a structured user-needs specification. It does not claim that the catalog is an executable suite, that any participant supports these tasks, or that stakeholder review is complete.

SDKBench starts with the work users need to complete. The traceability chain is:

**Target user -> real task -> required capability -> functional contract -> frozen benchmark instance -> observed evidence.**

No participant's present implementation defines the perimeter. Task relevance and acceptance rules must be established before participant support or performance is measured. A specialist component and an integrated development kit can both be evaluated, but their responsibilities and comparison cohorts must be explicit.

## Read in this order

1. [Requirements map](REQUIREMENTS_MAP.md): target users, boundaries, computing models and workflow stages.
2. [Task catalog](TASK_CATALOG.md): user outcomes, inputs, required capabilities, acceptance criteria, measurements and negative cases.
3. [Capability and function dictionary](CAPABILITIES.md): implementation-neutral behavioral contracts and reverse task references.
4. [Task-capability-function matrix](TRACEABILITY.md): complete task-level mapping, including conditional requirements.
5. [Acceptance rules](ACCEPTANCE.md): numerical, statistical, operational and scientific validation contracts.
6. [Neutrality and governance](GOVERNANCE.md): applicability, attribution, comparison, disclosure and change control.
7. [Coverage audit](COVERAGE.md): structural checks and the human review still required.
8. [Instance specification template](TASK_SPEC_TEMPLATE.md): requirements for making a family measurable.
9. [Primary sources](SOURCES.md): workflow context, standards and scientific grounding.

The [machine-readable catalog](catalog.json) is the source of truth for personas, capabilities, functions, journeys and task cards. The [long-form matrix CSV](matrix.csv) contains one row per task/function edge, with the condition, acceptance profiles and task-specific acceptance text. There is no SDK-versus-feature support table in this requirements baseline.

## What is specified

The baseline covers 16 user roles, 18 user journeys, 20 capability domains, 101 functional contracts and 92 task families. It includes static/adaptive gate programs, mixed-dimensional systems, measurement-based computation, physical controls, analog models, photonic/continuous-variable workflows, annealing, and error-corrected computation. Cross-cutting needs include installation, scientific modeling, resource constraints, uncertainty, recovery, provenance and interoperability.

Counts describe requirements structure, not benchmark instance count, test coverage or scientific completeness. A nonempty matrix cell is a requirement edge, not a passed test. The catalog is broad by design and remains open to justified new user needs.

## Relationship to the released package

The existing 0.1.0 implementation offers a small ideal-circuit timing harness and optional adapters. It does not implement this requirements baseline. Existing operation checks may become components of future task instances only after their user outcome, acceptance criteria and evidence boundary are specified. This documentation does not change the runtime suite, its scores, version or performance claims.

## Maintain the documents

Edit `catalog.json` for task/dictionary changes, then run from the repository root:

```bash
python tools/requirements_docs.py
python tools/requirements_docs.py --check
```

The tool renders the catalog, journey task cards, capability dictionary, traceability table, matrix CSV, source list and coverage audit. It checks identifiers, references, orphan functions, unused user/model/profile/stage entries, generated-file consistency, local links/anchors and English-only content. Generated files carry a header; edit the source instead. The explanatory requirements map, acceptance rules, governance and instance template are maintained by hand.

Structural validation cannot establish stakeholder demand, scientific correctness of future evaluators or completeness of every function variant. Those remain explicit review gates. Additions and corrections need a user-need rationale and the review process in [GOVERNANCE.md](GOVERNANCE.md).
