<!-- Generated from catalog.json by tools/requirements_docs.py. Do not edit directly. -->

# Workflow grounding and primary sources

Reviewed on 2026-11-18. These standards, primary research and official workflow descriptions are context, not a popularity-based task-selection rule. A project documenting a workflow does not make its API mandatory, establish that all SDKs support it, or prove stakeholder demand. The task requirements and acceptance rules are independently specified here.

Live documentation can change. Executable studies must pin relevant specification revisions, source commits, fixtures and references in their manifests. No performance claim or vendor ranking is inferred from these sources.

<a id="s01"></a>

## S01 - OpenQASM language specification

[OpenQASM language specification](https://openqasm.com/intro.html). Program semantics, classical control, timing and calibration boundaries; a language standard is not a mandate that every target support every feature.

<a id="s02"></a>

## S02 - QIR specification and execution profiles

[QIR specification and execution profiles](https://github.com/qir-alliance/qir-spec/blob/main/specification/README.md). Interchange and explicit execution-profile boundaries; no universal target gate set is assumed.

<a id="s03"></a>

## S03 - MolSSI QCSchema components

[MolSSI QCSchema components](https://github.com/MolSSI/QCSchema/blob/master/docs/source/spec_components.rst). Scientific input/output metadata, model and basis conventions needed for reproducible chemistry tasks.

<a id="s04"></a>

## S04 - Analog Hamiltonian simulation terminology

[Analog Hamiltonian simulation terminology](https://docs.aws.amazon.com/braket/latest/developerguide/braket-terms.html). Evidence that native analog users specify time-dependent Hamiltonians; vendor-specific limits are not universal requirements.

<a id="s05"></a>

## S05 - Strawberry Fields research paper

[Strawberry Fields research paper](https://arxiv.org/abs/1804.03159). Primary research describing photonic/CV workflows; motivates mode, Gaussian/Fock and measurement requirements without prescribing an implementation.

<a id="s06"></a>

## S06 - Formulation and sampling workflow

[Formulation and sampling workflow](https://docs.dwavequantum.com/en/latest/ocean/workflow.html). Evidence of optimization-model, sampler and hybrid-solver user journeys; particular APIs are not required.

<a id="s07"></a>

## S07 - Stabilizer and QEC circuit workflows

[Stabilizer and QEC circuit workflows](https://github.com/quantumlib/Stim). Concrete QEC workload context for detector events and logical observables; no preferred simulator or decoder is designated.

<a id="s08"></a>

## S08 - Differentiable hybrid interfaces

[Differentiable hybrid interfaces](https://docs.pennylane.ai/en/stable/introduction/interfaces.html). Evidence of quantum/classical derivative boundaries; no classical framework or derivative method is privileged.

<a id="s09"></a>

## S09 - Open-system dynamics workflow

[Open-system dynamics workflow](https://qutip.readthedocs.io/en/latest/guide/dynamics/dynamics-master.html). Hamiltonian, dissipator and solver conventions for dynamics studies; no solver implementation is prescribed.

<a id="s10"></a>

## S10 - MPI Forum standards

[MPI Forum standards](https://www.mpi-forum.org/docs/). Communication semantics and explicit runtime versions; this source does not establish that any SDK recovers from failures.

<a id="s11"></a>

## S11 - Sampler execution and result interface

[Sampler execution and result interface](https://quantum.cloud.ibm.com/docs/api/qiskit-ibm-runtime/sampler-v2). Concrete hardware job/result workflow context; neither this provider nor its API is a universal interface requirement.

<a id="s12"></a>

## S12 - Measurement-based computation patterns

[Measurement-based computation patterns](https://graphix.readthedocs.io/en/latest/). Primary project documentation for graph-state patterns, dependent measurements and corrections; motivates a distinct user task, not a required implementation or frontend.
