# Contributing

Propose new SDKs, operations or workload families through an issue. Keep adapters small and keep optional dependencies optional.

Workloads must be independently authored or carry the required license and attribution. Record gate conventions, units, seeds, expected semantics and validation limits. Never remove attribution required by a dependency or copied asset.

A new adapter must preserve the shared circuit's semantics, handle the little-endian statevector convention, use complex128 simulation, declare compiler targets and expose failures explicitly. Include independent correctness tests, unused-qubit tests and a complete benchmark run. Do not report a missing SDK as a successful measurement.

Performance claims must include environment details, SDK versions, raw samples, correctness results and equivalent experiment configurations. Avoid comparing compiler quality using incompatible target gates or native depth definitions without qualification. Keep setup, validation and reporting outside timing intervals.

Run `python -m pytest -q` and the build checks before submitting changes. A changed workload or timing methodology requires a version change; do not silently compare different input fingerprints.
