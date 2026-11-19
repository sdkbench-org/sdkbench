# Compiler candidate admission

This package identifies newly built compilers without changing the historical
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
environment before calling `create_registration`. Supply a unique stack ID,
public workflow and explicit compiler options. Call `verify_runtime` in each
fresh worker before importing the SDK. For example, after installing the wheel:

```python
from pathlib import Path
from sdkbench.candidates.provenance import create_registration, verify_runtime
from sdkbench.p0.models import canonical_bytes

registration = create_registration(
    stack_id="qiskit-source-transpile",
    sdk="qiskit",
    workflow="qiskit.transpile",
    options={"optimization_level": 2, "basis_gates": ["cz", "u"],
             "initial_layout": "identity", "final_layout": "permutation-allowed"},
    build_directory="/tmp/qiskit-candidate-build",
)
verify_runtime(registration)
with Path("candidate-registration.json").open("xb") as output:
    output.write(canonical_bytes(registration.to_dict()))
```

The options above illustrate registration, not an implemented runner or a
complete option set for the frozen campaign. Neither function compiles a task or
claims complete-case qualification.

The admission check compares wheel files, installed distribution fingerprints,
the package tree and Python module resolution. It rejects shadowing, extra
package files, changed dependencies and changed harness source. Installer-written
`RECORD` is excluded from byte-for-byte wheel comparison but included in the
installed-distribution fingerprint. Wheels that require `.data` relocation are
explicitly unsupported pending a reviewed mapping. This is a build observation,
not an independent attestation of source-to-wheel reproducibility.

The campaign runner, candidate adapters and full independent campaign replay
are still pending. Do not use these helpers as evidence that the frozen routing
campaign or its strict Linux controls have executed.

For a small change, modify the admission check and run:

```sh
PYTHONPATH=src python -m pytest -q \
  tests/test_candidate_provenance.py tests/test_candidate_build.py
```

Synthetic wheel tests exercise replacement at a fixed version, import shadowing,
configuration identity and worker revalidation. Build tests verify retained
input/output evidence and process-group cleanup. They do not replace native SDK
or Linux-supervisor tests.
