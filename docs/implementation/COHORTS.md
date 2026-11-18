# Comparison scope and neutral attribution

## First-study question

For each specified user outcome, which registered SDK stacks can complete it correctly under the same CPU1-FP64 resource envelope, and what latency, memory, compilation quality or reliability behavior do they exhibit? This answers a bounded procurement/development question. It does not establish which quantum SDK is globally best.

The [candidate snapshot](CANDIDATES.md) lists 17 observed packages and seven proposed role cohorts: exact computation/sampling, adaptive execution, compilation, derivatives, learning, orchestration and interchange. Their inclusion is an invitation to eligibility review, not a claim of support, successful installation or equal API scope. Candidate versions were read from PyPI on 2026-11-18; no live package-version assumptions are used as benchmark results.

Initial scope includes FlagQuantum, Qiskit/Aer, Cirq, PennyLane/Lightning, CUDA-Q, tket, Qibo/qibojit, Qulacs, MindQuantum, TensorCircuit-NG, TorchQuantum and provider-client components where relevant. This finite initial investigation is not a claim to enumerate every SDK worldwide. Accept additional eligible open or proprietary stacks under the same access, attribution, validation and resource rules before the cohort freeze; publish exclusions and access gaps. Do not choose candidates by expected relative performance.

## Register stacks, not overlapping brand entries

A registration identifies frontend, provider/client, compiler, simulator/device plugin, differentiation engine, numerical libraries and versions, and exact options. For example, a Qiskit frontend with Aer is one stack, not two independent votes. A PennyLane frontend using another simulator reports both components; a CUDA-Q CPU run must identify its actual CPU backend, not imply GPU performance. Provider clients are compared as clients for the offline recovery contract, not as if they were universal local simulators.

Distinguish frontend-only behavior from integrated-stack outcome. Native, plugin-assisted and externally integrated configurations are legitimate separate declared configurations when they satisfy the same user contract. Do not credit a frontend with a backend speed result without attribution. Limit primary configuration count equally by role: one documented default compliant configuration per registered frontend/role; additional configurations go into a separate disclosed configuration study, not extra weight in a ranking. Declare the selected backend by review before observing timings.

A numerical backend is eligible for numerical tasks if it can express/execute the required program through a supported public interface. A specialist compiler may enter compilation without a local simulator; its output is independently evaluated. A learning stack must execute requested quantum features and its declared derivative mechanism; analytic benchmark-side substitution is not support. For adaptive cases, host-orchestrated execution is permitted only as an actual supported declared participant workflow, preserving every branch with its cost included. Replacing missing control semantics with a special-purpose harness simulator is forbidden.

The offline job transport contract requires a reviewed binding to a real participant client interface. If the existing client cannot reconcile accepted-but-unacknowledged work, report that limitation; do not implement reconciliation in its benchmark wrapper. If no safe transport binding exists, record not-implemented/access-blocked with rationale, not accepted. No network, credentials or paid jobs are needed or allowed in those cases.

## Eligibility and fairness checklist for release

1. Freeze role applicability from user contracts, not candidate feature lists. Use per-instance declared subsets, not a general language/model support claim.
2. Independently review that every registered configuration meets precision, thread, resource and output constraints. Lock and hash full environments; the Python metadata snapshot alone does not establish resolution or OS compatibility.
3. Record license, installation/access constraints and required proprietary/hardware components. Lack of access is an evidence gap, not demonstrated poor capability. Do not silently downgrade a package to make a result available.
4. Apply identical case caps, default/tuning policy, negative controls and rerun rules to FlagQuantum and all peers. Publish unsuccessful attempts and unsupported outcomes. No maintainer is sole reviewer of their own evaluated adapter.
5. Require at least two independent eligible stacks per role before making a comparison. A one-stack result is descriptive. A specialist's intentionally different model is not a numerical zero in another model's cohort.
6. Publish separate correctness, coverage, resources, latency and quality views. Do not combine provider queue/device quality with SDK overhead, nor CPU/GPU or precision profiles, nor specialist model results into an arbitrary overall score.

The first-wave exact programs include structured analytic cases and small entangled cases; they do not by themselves establish generic simulator capacity, realistic chemistry performance, general QML usefulness or all-model completeness. Those questions have explicit later roadmap lanes. Report this scope beside every first-wave comparison, including any statement about FlagQuantum's position.
