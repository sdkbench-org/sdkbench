# Matched final-layout control

Status: implemented control and semantic conformance; no resource-qualified
comparative result is claimed here.

## User need and output obligation

A caller may need logical wire q returned to physical wire q so that subsequent
calibration, measurement or a separately compiled circuit has a fixed interface.
This obligation differs from permitting a free final permutation with classical
reconstruction. Both workflows are useful and must retain separate results.

Existing candidate configurations remain unchanged. New workflow identities are
`flagquantum-ordinary-restored`, `qiskit-transpile-restored` and
`cirq-route-cz-restored`. Each runs its existing ordinary compiler and appends
the same participant-independent restoration. The existing FlagQuantum target
artifact workflow already promises identity final layout, retains its native
restoration, and also includes packaging/serialization. It remains a distinct
workflow rather than a pure routing comparator.

## Exact policy

Read `final_layout[logical]` as the physical position of that logical wire.
Build a breadth-first spanning tree of the connected target graph rooted at
physical zero, visiting neighbors in ascending order. Repeatedly choose the
smallest active leaf, route its desired token along the unique active tree path
to that leaf, and freeze the leaf. Each swap exchanges both token positions.
The last token is then home. At most n(n-1)/2 swaps are appended.

Each physical SWAP is three CNOTs, each CNOT is H(target), CZ(control,target),
H(target). These exact gates use only declared edges and target operations.
There is no optimization after restoration for any participant. Identity input
layouts append no operations. Malformed permutations and disconnected targets
fail explicitly. The algorithm is deterministic, SDK-independent and bounded;
it is not claimed to minimize token swapping, depth or CZ count.

Program construction, native compilation, output normalization and restoration
all run inside the existing 120-second compilation alarm and timed interval.
The parent resource limits and independent P0 semantics are unchanged. Audit
fields `restoration_swaps`, `restoration_cz_count` and `restoration_operations`
expose appended cost separately. Total output CZ and common dependency depth
are recomputed by the independent evaluator/report, including restoration.

## Registration and execution

Prepare an immutable installed wheel and retain the release metadata as in the
existing candidate admission protocol. Register a new control explicitly:

```sh
PYTHONPATH=src python -m sdkbench.candidates.cli register-wheel \
  --stack-id qiskit-restored-control --workflow qiskit-transpile-restored \
  --wheel /tmp/qiskit-VERSION-PLATFORM.whl \
  --release-metadata /tmp/qiskit-release.json \
  --output /tmp/qiskit-restored-control.json
```

Expected: a new configuration-bound registration. Use `flagquantum-ordinary-restored`
and `cirq-route-cz-restored` for the corresponding candidates, and the existing
run/replay commands with an explicitly selected bundle on a qualified Linux host.
Source-build registration supports the same workflow names.

## What this controls and what it does not

The result compares complete delivered programs with the same fixed output
obligation. Appended cost is attributable to the chosen common restoration
policy. A compiler that already restores internally may retain avoidable swaps;
a compiler with free layout may benefit from an ordering that a native fixed-layout
optimizer would choose differently. Native optimizers do not see the common
suffix. Therefore this control cannot isolate synthesis quality, identify an
optimal constrained-layout compiler, or justify subtracting suffix costs and
calling the remainder a matched-layout comparison.

Report both original open-output and restored-output cohorts. Retain native
layout contracts, original compiler configuration, appended costs, compilation
time, memory, output counts, depth and failures. Do not combine artifact
serialization time with ordinary compilation time without stating the distinction.
A future native fixed-layout cohort requires separately reviewed configurations
and new registrations; it must not silently replace this control.

## Verification

```sh
PYTHONPATH=src python -m pytest tests/test_candidate_layout.py -q
SDKBENCH_NATIVE_CANDIDATE_TESTS=1 PYTHONPATH=src \
  python -m pytest tests/test_candidate_native_adapters.py -k restored -q
```

The independent tests cover every four-wire permutation on line, star and cycle
graphs using complete permutation operators, target legality, no-op identity,
invalid input rejection, configuration identity separation and inclusion of the
restoration in the compile timer. Native tests exercise all five application
families and the frozen six-wire routing circuit for all three controls through
unchanged complete-operator acceptance. These are conformance tests, not
resource-qualified performance evidence.
