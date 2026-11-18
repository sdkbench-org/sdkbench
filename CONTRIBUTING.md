# Contributing

Propose new SDKs, operations or workload families through an issue. Keep adapters small and keep optional dependencies optional.

New benchmark tasks and evaluation-protocol changes must start from a user need in the [requirements baseline](docs/requirements/README.md). Provide task/function traceability, an independent acceptance rule, explicit applicability and a complete measurement boundary. Add a justified missing need to the catalog instead of tailoring requirements to a participant. Follow the [neutrality and change-control rules](docs/requirements/GOVERNANCE.md).

For catalog changes, edit `docs/requirements/catalog.json`, run `python tools/requirements_docs.py`, and verify `python tools/requirements_docs.py --check`. Requirements-only task cards do not establish implementation or participant support.

Workloads must be independently authored or carry the required license and attribution. Record gate conventions, units, seeds, expected semantics and validation limits. Never remove attribution required by a dependency or copied asset.

Adapters for the existing 0.1.0 ideal-circuit harness must preserve its shared circuit semantics, handle its little-endian statevector convention, use complex128 simulation, declare compiler targets and expose failures explicitly. Include independent correctness tests, unused-qubit tests and a complete harness run. For new task families or computing models, define the appropriate output, precision and convention contracts instead of imposing this legacy statevector interface. Do not report a missing SDK as a successful measurement.

Performance claims must include environment details, SDK versions, raw samples, correctness results and equivalent experiment configurations. Avoid comparing compiler quality using incompatible target gates or native depth definitions without qualification. For the existing 0.1.0 harness, keep setup, validation and reporting outside timing intervals. Future task protocols must declare their own complete outcome boundary; the candidate first-wave protocol includes native program construction and JIT while separating independent oracle validation and reporting.

Run `python -m pytest -q` and the build checks before submitting changes. A changed workload or timing methodology requires a version change; do not silently compare different input fingerprints.

Implementation planning is maintained in [docs/implementation](docs/implementation/README.md). Edit `roadmap.json` for case/phase/threshold changes; run `python tools/roadmap_docs.py` for generated tables and `python tools/roadmap_docs.py --check --verify-small` to validate. Reviewed fixture/reference changes require a protocol revision and explicit `--freeze`, with independent review and invalidation of affected results. Preserve the participant-neutral cohort and attribution rules; reference tooling is not a participant adapter.
