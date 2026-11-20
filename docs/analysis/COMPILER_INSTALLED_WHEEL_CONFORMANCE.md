# Compiler revision installed-wheel conformance

This workflow checks two immutable FlagQuantum source revisions through built,
installed wheels on Linux. It complements the earlier
[source conformance](COMPILER_OPTIONAL_DIAGNOSTICS.md). It does not execute a
benchmark, qualify a measurement host, draw study entropy or establish a ranking.

## Run the existing native acceptance against installations

Dispatch `Compiler revision installed-wheel conformance` with two distinct full
commit IDs already reachable from FlagQuantum main. The planned source control
uses first revision `df35fb74c2bab72ab3af5eb635e9a22774929688` and second revision
`846032c764f4b3c3228f96a906e3ddad7123ab98`. Neither role implies a winning result.
Record the actual SDKBench workflow commit and first-attempt run identity.

The workflow reuses `tools/build_compiler_candidate.py` for each source archive,
offline native build, command, log and wheel identity. Both builds use the same
Python 3.12.14/CPU PyTorch 2.10 build environment and 900-second build budget.
Build observations remain explicitly without independent attestation.

One resolved dependency wheelhouse is retained with an exact hash lock. It
contains the SDKBench wheel, CPU PyTorch 2.14, NumPy 2.5.5, Qiskit 2.6.2, Cirq
1.7.0 and test/install dependencies. Transitive versions are observed and retained;
this workflow is not a prospective target-platform dependency approval. No source
distribution or second dependency resolution is admitted during installation.

The common dependencies are installed once. Runtime steps clear `PYTHONPATH`
after the harness build so source-tree metadata cannot substitute for installing
the harness wheel. Two virtual environments with no
private pip installation add that common site-packages directory through an
explicit `.pth` file, and install only their own frontend wheel. Their invocation
paths differ while their interpreter executable bytes match. This retains the
same non-frontend distribution bytes and RECORD files, including generated
entry-point scripts. It avoids incorrectly describing separately rewritten
installation scripts as identical. The common environment contains no
FlagQuantum installation. The existing installed-wheel verifier checks each
frontend's complete package tree and import resolution; it rejects a source
checkout or a different installed wheel.

Development admissions use the existing source-build registration and runtime
verification. `verify_revision_control` then checks both ordinary and
target-artifact configurations, complete non-frontend dependency records,
registered component payloads, harness, interpreter and host observations. This
is an actual invocation of that compatibility check, not an invented substitute
or a relaxed comparison. These records are development admissions, not actual
campaign registrations or a joint freeze.

Both interpreters execute the identical command from the SDKBench checkout:

```bash
SDKBENCH_NATIVE_CANDIDATE_TESTS=1 OPENBLAS_NUM_THREADS=1 \
  OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONPATH= \
  /path/to/revision-environment/bin/python -m pytest \
  tests/test_candidate_native_adapters.py \
  -k 'flagquantum-ordinary-restored or flagquantum-target-artifact' -q
```

Expected on a conforming revision: twelve passes, covering the fixed six-qubit
routing case plus five application families, each through ordinary and
target-artifact compilation. The unchanged evaluator checks arbitrary-input
full operators and restored layouts. The target path must serialize its artifact.
Missing optional diagnostics remain unavailable rather than fabricated zeroes.
An unsupported workflow, compilation error or failed operator check remains a
failure; there is no skip or version-specific exemption in this selection.

## Evidence and limits

The artifact retains both source archives, build commands and logs, native wheels,
the common dependency wheels/hash lock, observed build/installed inventories,
development admissions, the joint compatibility check and each test's log/JUnit
result. Temporary expanded sources, object files and duplicate download staging
are excluded; their retained source archives, build logs, wheels and hashes remain
the authoritative inputs and outputs. Failure uploads run even when an earlier
step fails. A missing final
joint record or test result is incomplete evidence, not a success. The workflow
rejects rerun attempts; a new run is a separately identified observation and must
not erase an earlier failure.

These are six-qubit line correctness checks in a hosted Ubuntu 24.04 environment.
They do not demonstrate larger widths, different topologies, symbolic synthesis,
full artifact-schema security or publication-qualified memory/time. The hosted
machine does not satisfy the formal dedicated-host protocol. Per-step and job
timeouts bound this setup and conformance work; they do not replace the unchanged
campaign supervisor or its CPU, memory and elapsed-time admission.

Future formal studies still need target-platform artifact review, independent
attestation, a qualified dedicated host, actual environment/registration freeze,
one prospective draw per study, complete supervised outcomes and independent
replay. The workflow does not change any fixture, independent reference, compiler
option, acceptance tolerance, failure denominator or resource gate. It makes no
server configuration, kernel, driver, service or reboot change.

## Retained first-attempt setup failure

Run `44764569267`, attempt 1, used integrated harness
`39ff9929579b7efbc24444947f28a6920614170a`. Both fixed FlagQuantum source archives
built successfully. The following common wheel-lock step then failed before
installation, development admission or native semantic checks. This is a
SDKBench setup failure, not a failed FlagQuantum compilation result.

The wheel metadata selector matched every path ending in
`.dist-info/METADATA`. Setuptools 84.2.1 includes twelve nested vendored metadata
files in addition to its single canonical root metadata file. The original
thirteen matches triggered the ambiguity assertion. Select only the wheel-root
`<distribution>.dist-info/METADATA` path with exactly two components. Multiple
canonical roots and duplicate normalized distribution names still fail; nested
vendor metadata is neither a second wheel distribution nor discarded package
payload. Whole wheel bytes remain retained and hashed.

A separate local packaging reproduction found that source-tree
`src/sdkbench.egg-info`, exposed through `PYTHONPATH`, lets pip report SDKBench
already installed without placing its wheel in the requested virtual environment.
The first CI run did not reach that step. Clear the source override for actual
installation, development admission and native tests, and use the common
installed harness wheel. Build tools retain their source checkout override.

The [failure evidence index](evidence/compiler-wheel-conformance-failure-20261120.json)
records both successful builds, their verified archive/wheel/log hashes, the
original failed stage and its artifact identity. The complete 785,642,395-byte
original artifact was downloaded and verified against GitHub's SHA-256 digest.
Its source ZIP commit comments also match the declared revisions. The artifact
retention expiry is recorded explicitly; local retained bytes are not replaced
by a later successful run. No native acceptance result or performance comparison
was generated by this failed run. A corrected execution must have its own run
identity rather than rerunning or relabeling the original attempt.
