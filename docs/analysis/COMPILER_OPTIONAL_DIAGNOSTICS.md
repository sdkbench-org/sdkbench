# Optional compiler diagnostics across revisions

Status: explicit adapter amendment implementation with local source conformance;
full CI and integration are recorded in the pull request. This is not a formal
performance campaign or installed-wheel qualification. It does not change the
compiler tasks, participant options, payloads, acceptance or resource limits.

## Observed adapter incompatibility

SDKBench harness `8299c6043c00303419ef9cd3d41f412a3fd21535` unconditionally read
`result.legalization.native_block_optimization` after the target-artifact
workflow had compiled and serialized its output. FlagQuantum baseline
`df35fb74c2bab72ab3af5eb635e9a22774929688` has no such result field. Candidate
`846032c764f4b3c3228f96a906e3ddad7123ab98` exposes it. This is an adapter
assumption about an optional diagnostic, not evidence that the old compiler
cannot compile the target or satisfy the independent semantic checks.

The unchanged local source-conformance selection comprised the frozen six-qubit
routing case and all five existing six-qubit application families on a line.
For each revision it exercised both `flagquantum-ordinary-restored` and
`flagquantum-target-artifact`, with the existing independent arbitrary-input
full-operator check and restored output-layout assertion.

| Source revision | Original adapter | Amended adapter |
| --- | --- | --- |
| Pre-default baseline `df35fb74c2ba` | 6 ordinary passes; 6 target-artifact failures | 12 passes |
| Integrated candidate `846032c764f4` | 12 passes | 12 passes |

The [retained evidence index](evidence/compiler-optional-diagnostics-20261120.json)
binds compressed raw logs and JUnit results for both before/after selections.
All six original baseline target-artifact failures were `AttributeError` for
`native_block_optimization`. The earlier failed outcomes remain retained. The
amendment does not relabel them as historical passes. A new harness identity,
new actual registrations and a new reviewed freeze are required for future
studies; separately drawn campaigns remain unpaired.

## Amendment and observability

The adapter continues to invoke the identical target compilation API, with the
same target, routing/native-operation budgets and serialized artifact costs.
The required compiled program, final layout, native-legalization result,
serialized executable artifact and target snapshot evidence remain mandatory.
Their failure is not treated as an absent diagnostic.

Only the optional SDK-reported block-optimization observation changes:

| Observed SDK result | Availability measurement | Rewrite measurement |
| --- | --- | --- |
| Field absent | `native_block_optimization_evidence_available=0` | Omitted; unknown |
| Field present and `None` | `native_block_optimization_evidence_available=1` | `accepted_block_rewrites=0` |
| Field present with rewrite evidence | `native_block_optimization_evidence_available=1` | Number of returned rewrites |
| Field present but malformed | Execution fails | No fabricated success |

This is capability observation, with no revision checks, no version-specific
routing branches and no injected optimization. It does not claim the SDK exposes
an optimization stage merely because a compiled program is correct. An absent
field is not zero observed rewrites and is not a basis for attributing any gate
count difference to a pass.

The independently replayed summary exposes the availability distribution as
`sdk_reported_native_block_optimization_evidence_available`. The existing
`sdk_reported_accepted_block_rewrites` remains `null` when no accepted record
supplied that observation. It retains a real zero when every observed stage
reported zero rewrites. Both remain SDK-reported diagnostics. The paired
comparison continues to use only independently recomputed CZ count/dependency
depth and the unchanged eligible timing/memory observations. These diagnostics
cannot turn a failed case into an accepted case or qualify a performance ratio.

## Reproduce the source checks

Use separate fixed source roots and a shared development dependency installation.
Confirm the imported `flagquantum.__file__` points inside the selected source
root. Run from the SDKBench checkout so another current directory cannot shadow
`PYTHONPATH`.

```bash
SDKBENCH_NATIVE_CANDIDATE_TESTS=1 OPENBLAS_NUM_THREADS=1 \
  OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  PYTHONPATH=src:/path/to/selected-FlagQuantum-source \
  python -m pytest tests/test_candidate_native_adapters.py \
  -k 'flagquantum-ordinary-restored or flagquantum-target-artifact' -q
PYTHONPATH=src OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python -m pytest tests/test_candidate_optional_evidence.py \
  tests/test_candidate_runner.py tests/test_application_comparison.py \
  tests/test_revision_controls.py -q
```

The synthetic target compiler tests require the actual adapter to preserve its
artifact, layout and budgets with absent, zero and populated diagnostics. They
also preserve failures from compilation, serialization and malformed present
evidence. A sealed synthetic campaign independently replays every block of the
fixed three-case/two-stack scope and proves that the report distinguishes
missing observations from zero; these synthetic numbers are not SDK results.

The local source checks used macOS ARM64, Python 3.12.14 and PyTorch 2.14.0.
The amended source also passed all 60 existing opt-in candidate adapter tests,
covering the three SDKs and their registered workflows over the same six inputs.
Source selection did not modify installed distributions. There was no wheel
build/admission, strict Linux supervisor, study nonce draw, qualified dedicated
host, complete prospective campaign, comparative timing/memory result or global
SDK rank. Six-qubit line conformance does not prove larger widths, other
topologies, symbolic inputs or artifact schema security. The existing full
protocol, native-wheel and independent review gates remain required.

## Local validation record

The amended adapter passed the 24 selected old/new source checks and all 60
existing native workflow checks across FlagQuantum, Qiskit and Cirq. Focused
optional-evidence, candidate-report, paired-comparison and revision-control
coverage passed 69 tests in 86.63 seconds. Source/wheel builds, strict Twine,
scoped Ruff and whitespace checks passed. A broader runner-inclusive local
selection reached its unchanged 240-second outer budget and was terminated;
that interrupted run is not reported as passing. Complete CI remains required
before integration. No test, tolerance or resource limit was weakened.
