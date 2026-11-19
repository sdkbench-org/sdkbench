# Compiler candidate admission

This package identifies source-built and published-wheel compiler candidates without changing the historical
P1a/P1b release admissions. It owns build observations, installed-wheel checks
and their binding to the existing P0 `Registration`. It does not own quantum
semantics, acceptance thresholds, SDK compilation algorithms or resource limits.

Dependencies are the standard library and the existing P0/P1a provenance code.
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
`qiskit-transpile` and `cirq-route-cz`. They have distinct configurations. The
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
