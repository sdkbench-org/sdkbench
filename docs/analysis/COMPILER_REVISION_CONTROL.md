# Joint compiler revision control

Status: execution infrastructure and preparation/reporting checks, not an
executed prospective study. No application nonce has been drawn for an actual
old/new comparison. Test fixtures and synthetic distributions provide no SDK
performance evidence. Publication eligibility remains false.

## Question and participants

Measure two immutable revisions of one complete compiler workflow on identical
prospectively generated inputs. This profile applies equally to FlagQuantum,
Qiskit and Cirq. It does not select participants or options after seeing results.
It does not attribute a whole-revision difference to an individual compiler pass.

The `revision-control` profile requires exactly two distinct stack IDs and
separate absolute interpreter paths. Both registrations must declare the same
SDK, frontend distribution, restored-layout workflow, compiler options, resource
profile, precision and thread count. Supported workflows are
`flagquantum-ordinary-restored`, `flagquantum-target-artifact`,
`qiskit-transpile-restored` and `cirq-route-cz-restored`.

Both participants must have distinct full source revisions or distinct published
release versions. Mixing source-build and release-download identity mechanisms
is refused. Each installed frontend retains its own verified wheel, installed
payload fingerprint, import resolution and build/release evidence. Different
frontend bytes and installation origins are expected; differences in other
registered configuration fields are rejected. Runtime admission still precedes
any SDK import.

## Environment matching

Capture a complete inventory with `sdkbench.p1a.provenance.capture_environment`
in each selected interpreter. Each inventory's full dependency digest must match
its registration. Normalize distribution names for matching and reject ambiguous
duplicates. All non-frontend dependency entries must match, including versions
and exact installed RECORD hashes. Match all registered non-frontend component
payload fingerprints, including the harness and numerical dependencies. Also
match Python, platform, image descriptor, implementation and stable host facts.
Retain the raw `/proc/cpuinfo` hash while excluding it from host equality because
CPU frequencies change between observations.

The bounded setup probe rechecks the supplied inventory inside its actual
selected interpreter, then repeats existing runtime admission. Merely supplying
a JSON file cannot substitute for this live check. A successful probe retains
the existing registration/interpreter binding; it is not independent attestation.

Installed RECORD hashes can differ because installers rewrite scripts, prefixes
or metadata even for identical wheel versions. This profile does not silently
strip those differences. A declared shared immutable dependency installation,
without either participant frontend installed, can support exact matching.
Keep reviewed locks, full retained wheelhouse hashes, source archives and build
records as external study evidence. RECORD inventories and selected component
fingerprints do not independently attest every transitive dependency byte or
establish a sealed environment. Additional dependencies or changed common
components are confounders and fail this matched control; separately declared
complete-stack experiments need their own interpretation.

## Freeze, draw and execute

Prepare both reviewed installations and registrations using the existing
[source-build or published-wheel workflow](../../src/sdkbench/candidates/README.md).
Capture inventories before requesting a draw, for example in each environment:

```bash
PYTHONPATH=src /environments/before/bin/python -c \
  'from sdkbench.p1a.provenance import capture_environment; from sdkbench.p0.models import canonical_bytes; print(canonical_bytes(capture_environment()).decode(), end="")' \
  > /evidence/before-environment.json
PYTHONPATH=src /environments/after/bin/python -c \
  'from sdkbench.p1a.provenance import capture_environment; from sdkbench.p0.models import canonical_bytes; print(canonical_bytes(capture_environment()).decode(), end="")' \
  > /evidence/after-environment.json
```

Use an immutable integrated harness checkout for the actual study. Once the
registrations, retained artifacts, environment locks, native conformance and
host qualification have been independently reviewed, explicitly invoke:

```bash
PYTHONPATH=src python tools/prepare_compiler_applications.py \
  --profile revision-control \
  --registration /evidence/before-registration.json \
  --registration /evidence/after-registration.json \
  --interpreter before-stack=/environments/before/bin/python \
  --interpreter after-stack=/environments/after/bin/python \
  --inventory before-stack=/evidence/before-environment.json \
  --inventory after-stack=/evidence/after-environment.json \
  --output /evidence/joint-preparation
PYTHONPATH=src python -m sdkbench.candidates.cli run \
  --registration /evidence/before-registration.json \
  --registration /evidence/after-registration.json \
  --interpreter before-stack=/environments/before/bin/python \
  --interpreter after-stack=/environments/after/bin/python \
  --bundle /evidence/joint-preparation/cohort \
  --directory /evidence/revision-campaign --cpu 0 \
  --cgroup-parent /sys/fs/cgroup/DELEGATED_SUBTREE
```

The stack names must match the registrations. The CPU and delegated cgroup are
operator-selected prerequisites on an already qualified dedicated Linux host.
No host setup, privilege escalation, kernel change or reboot is performed.
Use the existing 270-minute outer measurement and 360-minute job ceilings; the
manual commands do not provision those outer controls. Preserve an interrupted
campaign as incomplete rather than shortening case limits or drawing again.

Preparation checks both registrations, inventories and live environments before
requesting entropy. It exclusively creates the preparation directory and writes
one `freeze.json` retaining both registrations, inventories, interpreter identities
and successful probes. Only then does it request one OS-backed 32-byte draw.
Existing output directories are refused before probes or entropy. A failed draw
retains its directory and cannot silently redraw. Local event ordering is not an
independent timestamp or build attestation.

The existing generator and selection are reused: all five families, widths
6/8/12 and line/grid topology, totaling 30 cases. Each participant receives the
same fixture and reference bytes, compiler seeds, thresholds and limits. The
existing block-major rotation, supervisor and independent evaluators are
unchanged. A complete two-stack cohort has 60 case/stack pairs, 600 process
blocks, 1,200 warmups and 1,800 measured records. Cumulative case ceilings total
66,000 seconds; they are resource ceilings, not runtime estimates. Each process
retains one CPU, one numerical thread, 16 GiB and the existing per-compilation
and cumulative case bounds. Width 6 uses a full operator; widths 8/12 retain
three-probe-only semantics.

## Replay and paired report

```bash
PYTHONPATH=src python tools/compare_compiler_applications.py \
  --profile revision-control \
  --preparation /evidence/joint-preparation \
  --directory /evidence/revision-campaign \
  --bundle /evidence/joint-preparation/cohort \
  --output /evidence/revision-comparison.json
```

This invokes independent campaign replay, checks exact joint registration,
interpreter, freeze/draw/selection and bundle bindings, and requires all 30 cases
for both stack identities. An admitted campaign environment must reproduce its
frozen probe. If an environment becomes unavailable after the draw, its replayed
failures remain in the denominator. The report carries the joint evidence
hashes. Separately drawn campaigns cannot be substituted as paired evidence.

Rows group by stack identity, because both participants have the same workflow.
Each pair explicitly names `numerator_stack` and `denominator_stack` and retains
the actual workflow names. The existing accepted-pair calculation is shared
with ordinary, target-artifact and routing-policy reports. Only two fully
accepted cases with all 30 measured records and ten eligible blocks receive
ratios. A failed warmup or any full-case failure withholds all pair ratios.

CZ count and common dependency depth use independent accepted-record medians.
Timing compares each corresponding block's three-run median; memory compares
whole-block kernel peaks, including import, warmup and export. Zero, missing or
nonfinite inputs make the affected ratio undefined. Descriptive quartiles are
not confidence intervals or significance tests. No across-case winner, universal
SDK ranking or isolated-pass causal claim is produced.

## Verification and remaining gates

```bash
PYTHONPATH=src OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python -m pytest tests/test_revision_controls.py \
  tests/test_prepare_compiler_applications.py tests/test_application_comparison.py \
  tests/test_candidate_environments.py -q
```

Coverage includes neutral admission for every supported workflow, exact
non-frontend matching, freeze-before-entropy, refusal to redraw, live inventory
checks in actual separate interpreters, substituted evidence rejection, paired
metrics, and retained failures. Synthetic accepted numbers test calculations;
they are never evidence about a real SDK. The existing real Linux supervisor
and native SDK tests remain separate conformance checks.

An actual prospective comparison still requires reviewed source/wheel/lock
artifacts, native conformance against both selected revisions, a qualified
dedicated host and independent review. Hosted CI and this development machine
are not qualified measurement hosts. No server preparation is resumed by this
feature, and no formal improvement or publication claim follows from its tests.
