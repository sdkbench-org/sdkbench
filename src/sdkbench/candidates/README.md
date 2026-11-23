# Compiler candidate admission

This package identifies source-built and published-wheel compiler candidates without changing the historical
P1a/P1b release admissions. It owns build observations, installed-wheel checks
and their binding to the existing P0 `Registration`. It does not own quantum
semantics, acceptance thresholds, SDK compilation algorithms or resource limits.

Application generation and new W03 bundle construction are also owned here;
they use NumPy and the existing P0 semantics only for fixture auditing, never
participant performance or acceptance decisions. See the
[application protocol](../../../docs/analysis/COMPILER_APPLICATION_PROTOCOL.md).
Physics anchors independently check the meaning of the recipes.

External coherent OpenQASM preparation is a separate optional input path. It reuses
Qiskit/Cirq parsers for source conversion/conformance, never participant compilation
or W03 acceptance. See [conversion rules, bounds and synthetic tests](../../../docs/analysis/COMPILER_EXTERNAL_QASM_PREPARATION.md).
The frozen external population has completed input admission; see the
[complete decisions and exposure limits](../../../docs/analysis/COMPILER_EXTERNAL_INPUT_ADMISSION_20261123.md).
Participant execution has not started.
[Supervised preparation](../../../docs/analysis/COMPILER_EXTERNAL_BUNDLE_PREPARATION.md)
retains input refusals and the full intended denominator before constructing an
explicit bundle under unchanged W03 acceptance.
The [exact exposure audit](../../../docs/analysis/COMPILER_EXTERNAL_EXPOSURE_AUDIT.md)
compares retained inputs against explicit historical evidence and records coverage
gaps; absence of an exact match does not certify novelty.

Admission dependencies are the standard library and existing P0/P1a provenance code.
The explicit build command uses the repository's existing development dependency
`build`; its environment must already satisfy the candidate's build requirements.
It performs no dependency installation and inherits only recorded build controls.

Create a source archive and wheel from an immutable Git commit in a prepared
build environment:

```sh
PYTHONPATH=src python tools/build_compiler_candidate.py \
  --repository /path/to/sdk --revision FULL_COMMIT \
  --distribution qiskit --directory /tmp/qiskit-candidate-build
```

The command retains `source.zip`, the wheel, `build.log` and `build.json`. Failed
and timed-out builds retain their observations too; timed-out build process
groups are killed. Install the retained wheel in a separate measurement
environment, then register one of the declared workflows:

```sh
PYTHONPATH=src python -m sdkbench.candidates.cli register \
  --stack-id qiskit-source-transpile --workflow qiskit-transpile \
  --build-directory /tmp/qiskit-candidate-build \
  --output /tmp/qiskit-candidate-registration.json
```

Published comparator wheels can be admitted without pretending they were built
from source. Retain the exact wheel and its version-specific PyPI JSON response,
install the wheel in the measurement environment, then run:

```sh
PYTHONPATH=src python -m sdkbench.candidates.cli register-wheel \
  --stack-id qiskit-release-transpile --workflow qiskit-transpile \
  --wheel /tmp/qiskit-VERSION-PLATFORM.whl \
  --release-metadata /tmp/qiskit-release.json \
  --output /tmp/qiskit-release-registration.json
```

Admission checks the distribution, installed version, wheel filename, SHA-256,
size, non-yanked release status and PyPI file origin before checking every
installed payload byte. It retains the release metadata hash and labels the
origin `published_wheel`. Neither this observation nor source-build observation
is an independent publisher or build attestation.

Supported workflows are `flagquantum-ordinary`, `flagquantum-target-artifact`,
`qiskit-transpile` and `cirq-route-cz`. Three additional `-restored` workflows
apply the same timed final-layout postprocessing to the ordinary FlagQuantum,
Qiskit and Cirq outputs. All have distinct configurations. See the
[matched-layout control](../../../docs/analysis/COMPILER_MATCHED_LAYOUT_CONTROL.md). The
ordinary FlagQuantum path uses the current `compiler.lowering` module boundary;
the historical P1b adapter continues to use its pinned release boundary.

Run all three unchanged frozen routing tasks on a host with a delegated Linux
cgroup-v2 subtree and libseccomp. Repeat `--registration` to counterbalance more
than one candidate/configuration in the same measurement environment:

```sh
PYTHONPATH=src python -m sdkbench.candidates.cli run \
  --registration /tmp/qiskit-candidate-registration.json \
  --directory /tmp/compiler-campaign --cpu 0 \
  --cgroup-parent /sys/fs/cgroup/DELEGATED_SUBTREE
PYTHONPATH=src python -m sdkbench.candidates.cli replay \
  --directory /tmp/compiler-campaign
```

## Separate installed environments

Two revisions of one distribution cannot coexist in one Python installation.
Register each retained wheel using its own interpreter, with this same harness
source selected through `PYTHONPATH`. The runner can then select one interpreter
per stack, including for Qiskit, Cirq or any other admitted candidate; no SDK gets
a private execution path:

```sh
PYTHONPATH=src python -m sdkbench.candidates.cli run \
  --registration /evidence/before-registration.json \
  --registration /evidence/after-registration.json \
  --interpreter before-stack=/environments/before/bin/python \
  --interpreter after-stack=/environments/after/bin/python \
  --directory /evidence/revision-campaign --cpu 0 \
  --cgroup-parent /sys/fs/cgroup/DELEGATED_SUBTREE
PYTHONPATH=src python -m sdkbench.candidates.cli replay \
  --directory /evidence/revision-campaign
```

The names before `=` must exactly match the registrations' `stack_id` values.
Once interpreter selection is used, every stack needs an absolute path;
partial or duplicate selections fail before creating campaign evidence. The
invocation path preserves a virtual environment's prefix, rather than resolving
its Python symlink into the base interpreter. The executable bytes are hashed.

A bounded 120-second setup probe in each selected environment repeats the
existing installed-wheel/runtime admission without importing the SDK. Successful
probe output is retained in `admission.json`; failed probes retain a bounded
diagnostic reason. `interpreters.json` binds the
paths/hashes to the report. A missing environment or failed probe stays in the
denominator with all expected failure records. Probe costs are setup evidence,
not SDK compilation latency; setup elapsed time must be recorded separately by
the campaign operator. Each measured fresh worker checks its interpreter
and repeats runtime admission under the unchanged resource supervisor. Its
imports, validation and output work still consume the cumulative case budget.
The block-major participant rotation, fixtures, seeds, correctness tolerances,
memory and timeout limits are unchanged. No installations are switched between
blocks. Omit all `--interpreter` arguments to retain the single-environment path.

Replay verifies the setup admission's registration binding, selected executable,
actual supervised command and worker request/response bindings. It can replay
transferred evidence without the original environments. A content seal is not
independent attestation, and a Python executable hash alone does not identify a
complete environment; existing dependency, package and module-resolution checks
remain necessary.

This execution support alone does not preregister a prospective revision
comparison. Use the explicit [joint revision-control profile](../../../docs/analysis/COMPILER_REVISION_CONTROL.md)
for prospective preparation and paired reporting. It checks matched dependencies,
workflow options and host facts, rechecks full inventories in the selected
interpreters, and freezes both registrations before one shared draw. Existing
three-SDK profiles retain their own workflow sets. An actual old/new study still
needs reviewed artifacts, native conformance, a qualified dedicated host and
independent review.
Differences in dependencies or workflow options are confounders, not compiler
effects. Existing separately drawn campaigns are not matched old/new evidence.

```sh
PYTHONPATH=src python -m pytest -q tests/test_candidate_environments.py \
  tests/test_candidate_runner.py tests/test_candidate_resource_replay.py
```

The environment tests use real virtual environments with synthetic distributions
that raise on import. They prove environment admission and failure isolation,
not native SDK correctness or performance. Synthetic accepted lifecycle tests
exercise counterbalancing, unchanged limits, and resealed substitution rejection.
Real Linux-supervisor coverage remains an independently required CI check.

Produce a reproducible numerical summary outside the sealed campaign directory:

```sh
PYTHONPATH=src python tools/compiler_candidate_report.py \
  --directory /tmp/compiler-campaign --output /tmp/compiler-summary.json
```

The summary first replays the campaign, then recomputes accepted-record gate
counts and common depth. It retains failure denominators and reports timing
medians only for complete accepted blocks, excluding failed warmups. Kernel
memory peaks cover the entire supervised block. Conditional statistics from
failed cases never promote those cases to success. SDK-reported native baseline
counts are labeled separately from independently recomputed output counts.

The existing P1a/P1b runner supplies ten fresh process blocks, two warmups and
three measured outcomes, frozen seeds, independent P0 evaluators and unchanged
per-case budgets. Both the parent and worker revalidate each candidate before
SDK import. The existing Linux supervisor enforces the same CPU, memory and
network rules. Unsupported or rejected configurations remain explicit failures;
there is no execution fallback on hosts without the required isolation.
Target-artifact compilation includes serialization in its measured interval and
retains one compiler-evidence file per successful outcome. Filesystem export,
imports, admission and independent validation also consume the cumulative case
budget. The complete campaign is content-hashed for replay without SDK imports.

Replay checks complete case/block accounting, registration and request binding,
seeds, measured and warmup semantics, enforced resource fields, compiler-file
hashes and case/workflow verdicts. It verifies normalized circuit semantics;
retained SDK artifact envelopes are not promoted to independently verified
compiler provenance by this replay. Source-to-wheel attestation and qualified
publication-host evidence remain separate gates.

The admission check compares wheel files, installed distribution fingerprints,
the package tree and Python module resolution. It rejects shadowing, extra
package files, changed dependencies and changed harness source. Installer-written
`RECORD` is excluded from byte-for-byte wheel comparison but included in the
installed-distribution fingerprint. Wheels that require `.data` relocation are
explicitly unsupported pending a reviewed mapping. This is a build observation,
not an independent attestation of source-to-wheel reproducibility.

The `Compiler candidate qualification` GitHub Actions workflow builds its fixed
FlagQuantum commit with PyTorch 2.10, then installs that retained wheel alongside
published Qiskit 2.6.2 and Cirq 1.7.0 wheels in the common PyTorch 2.14 environment.
It registers four workflows, runs all frozen routing cases under Linux controls,
and independently replays the retained campaign. Failure does not discard
artifacts or permit a success-only rerun. The runner is an observed engineering
host; it is not a sealed publication host. A successful workflow run must still
be inspected before reporting complete campaign execution.

The first full native Linux campaign and local independent replay completed; see
[the result report](../../../docs/analysis/COMPILER_CANDIDATE_RESULTS.md). Independent
build attestation, publication-host qualification and the prospective held-out
campaign remain pending. Passing local adapter conformance or
synthetic runner tests does not establish measured SDK performance.

For a small change, modify the admission check and run:

```sh
PYTHONPATH=src python -m pytest -q \
  tests/test_candidate_provenance.py tests/test_candidate_build.py \
  tests/test_candidate_runner.py
```

Synthetic wheel tests exercise replacement at a fixed version, import shadowing,
configuration identity and worker revalidation. Build tests verify retained
input/output evidence and process-group cleanup. They do not replace native SDK
or Linux-supervisor tests.

Native adapter conformance is opt-in and checks the six-qubit full operator. Use
a prepared environment with the desired compiler revision already selected:

```sh
SDKBENCH_NATIVE_CANDIDATE_TESTS=1 PYTHONPATH=src \
  python -m pytest -q tests/test_candidate_native_adapters.py
```

These tests call the adapter directly. They intentionally do not claim the
wheel admission chain, ten-block campaign, Linux controls or timing ranking.

## Optional compiler observations

Target-artifact compilation and serialized evidence remain mandatory. An older
SDK may omit the optional native block-optimization result field. The adapter
then records `native_block_optimization_evidence_available=0` and omits the
unknown rewrite count, while applying the same independent acceptance. A present
but malformed result still fails. The independently replayed report distinguishes
missing observations from measured zero; neither contributes to acceptance or
paired performance ratios. See the
[diagnostic compatibility amendment](../../../docs/analysis/COMPILER_OPTIONAL_DIAGNOSTICS.md)
for retained before/after source checks and their limits. Historical campaign
records and the original frozen harness remain unchanged.
