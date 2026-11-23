# Prospective external-program execution freeze

This [final manifest](COMPILER_EXTERNAL_EXECUTION_FREEZE_20261123.json) is frozen
before the first participant outcome. It supersedes the explicitly pending
execution preparation record. The exact harness revision
`3e4d6ed0ad024e81da4fc55a6051bfff64e8e647` passed all fourteen required checks;
the [retained CI receipt](evidence/external-execution-20261123/ci-gate.json)
binds their names, workflows, URLs and completion observations to that head.
This does not claim that the separate documentation-head CI has completed.

The [operator driver](evidence/external-execution-20261123/run-frozen-external.py)
uses the existing reviewed phase helper, bound by hash, and unchanged candidate
CLI. Its [negative control](evidence/external-execution-20261123/missing-ci-admission-control.json)
confirms that absent CI evidence refuses admission before creating a campaign
or cgroup. Interruption handling enters owned-descendant cleanup; optimized
Python is refused so admission assertions cannot silently disappear.

The four registered workflows retain the exact historical candidate wheels,
dependencies and compiler options. All 49 existing Python runtime files remain
byte-identical to the historical harness; only the converter, preparation and
exposure modules were added. The manifest binds new harness-specific
registrations, input/bundle/evaluator hashes, case acceptance, phase budgets and
preliminary host/control observations. Actual baseline and selected-core/sibling
idleness must be checked again immediately before execution.

All seven original sources and 56 intended workflow rows remain accounted for.
Three admitted sources yield six line/grid tasks and 24 executable workflow rows;
32 rows remain input-not-admitted. No source repair, replacement, repetition
reduction, selected seed, private participant allowance or favorable rerun is
permitted. There is no admitted twelve-qubit source in this population. The
limited exact-match exposure audit does not certify novelty. Eight-qubit
semantics retain the original three-probe scope, not universal equivalence.

The original reservation ends at `2026-11-24T05:36:41Z`. Require at least 71100
seconds remaining and admit no later than `2026-11-23T09:51:41Z`, even though
some preparation phases have completed. Retain the 50400-second campaign,
10800-second independent replay, 900-second numerical summary and 900-second
cleanup ceilings. The summary's own replay consumes its summary ceiling. A
phase timeout is an incomplete/failing observation, never permission to extend
another budget or erase partial results. Restore original scheduling labels on
completion, failure or abandonment; do not restart services or machines.

The outer driver disabled bytecode writes, but the source supervisor deliberately
uses an explicit environment and does not inherit that flag. Therefore the outer
flag alone does not establish worker cache immutability. The
[read-only metadata observation](evidence/external-execution-20261123/retained-env-bytecode-observation.json)
found no `.pyc` mtime newer than the historical study's completion across 12410
retained environment files and 5733 base-interpreter files. This is metadata
evidence, not cache-content attestation. Installed non-bytecode candidate
payloads and dependency inventories were separately reverified. No package,
interpreter, compiler option or resource-control implementation changed.

After publishing and independently checking these exact manifest bytes, stage
the same file as `public-external-freeze.json` in the declared study root and run:

```sh
env PYTHONDONTWRITEBYTECODE=1 PYTHONOPTIMIZE=0   /data/sdkbench-compiler-qualification-20261123/python-complete/bin/python3.12   -u /data/sdkbench-external-inputs-staged-20261123/run-frozen-external.py
```

Expected: one attempt through the existing candidate `run`, producer-free `replay`
and existing report tool, with live phase/resource observations and all failures
retained. The prepared missing-CI check ran no external participant. This freeze
reports no external compiler result, comparative ranking or publication-host
certification. Detailed raw host/process inventories remain private; this record
publishes identities and compact controls only. Preserve original external
LICENSE/NOTICE with every redistributed source/derived fixture archive.

## Observer placement correction before participant execution

The first admission was refused before campaign/cgroup creation or any SDK
execution. The [retained refusal](evidence/external-execution-20261123/admission-attempt-1.json)
binds the original published driver and manifest. The observer had been pinned
to measured CPU 96 before checking that CPU's idleness. Observer activity can
contaminate that check; the original after-sample was not retained, so exact
attribution is unavailable.

The [amended manifest](COMPILER_EXTERNAL_OBSERVER_FREEZE_20261123.json) binds
the [corrected operator driver](evidence/external-execution-20261123/run-frozen-external-observer.py).
It keeps the observer on housekeeping CPU 0, outside measured CPU 96 and its
SMT sibling 288, for admission and phase monitoring. It captures a fresh
selected-core interval and writes both samples and all deltas before asserting
the unchanged zero-busy-tick requirement. Participant workers still explicitly
use CPU 96. No evaluator, participant, input, repetition, budget or original
reservation deadline changes. The original freeze remains retained unchanged.

Publish and independently verify this amended manifest before staging it as
`public-external-observer-freeze.json` and executing the corrected driver as
`run-frozen-external-observer.py`. This authorizes one first participant campaign,
not a repeat of participant outcomes. If admission fails again, retain the full
samples and diagnose them before any further action.
