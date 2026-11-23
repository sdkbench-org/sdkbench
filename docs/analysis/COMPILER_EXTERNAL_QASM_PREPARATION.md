# External OpenQASM preparation

Status: synthetic converter conformance only. No frozen external source bodies
or participant outcomes have been inspected. The separately published
[population declaration](COMPILER_EXTERNAL_PROGRAM_QUALIFICATION_20261123.md)
fixes the seven external programs and all intended outcomes. Converter admission
and a separately frozen execution declaration are required before those programs
can be called a prospective qualification.

## Responsibility and dependency boundary

`src/sdkbench/candidates/external_qasm.py` prepares one common numeric coherent
prefix for all participants. It does not compile, optimize, route, select a
participant, change a target or decide W03 acceptance. Qiskit `qasm2.loads`
provides the maintained parser and public gate definitions. Cirq's contrib QASM
parser independently reads the source and supplies a second source-meaning
check. No participant compiler, transpiler or target optimizer runs during
conversion. The unchanged SDKBench bit-block propagation, independent dense
references and W03 evaluator still decide compiled-output acceptance.

The inspected parser versions are Qiskit 2.6.2 and Cirq Core 1.7.0. They already
belong to the compiler comparison environment. Cirq declares PLY as an optional
`contrib` dependency; preparation additionally uses PLY 3.11 (BSD-3-Clause),
verified wheel SHA-256
`096f9b8350b65ebd2fd1346b12452efe5b9607f7482813ffca50c22722a807ce`.
This is an isolated preparation dependency, not a new required SDKBench runtime
or participant measurement dependency. Preserve wheel/license metadata when
redistributing its bytes. Candidate preparation owns this use. Its replacement
boundary is source text to the recorded numeric rotation/CX list; the independent
source checks and frozen compiled-output checks survive parser replacement.
Remove the optional use when another admitted source parser supplies the same
conversion/conformance without changing participant consumers. No parser types
leave the preparation module and no implementation is vendored.

The initial local installation attempt found no pip module in the existing venv;
it installed nothing. Synthetic verification instead zip-imported the exact
hash-verified pure-Python PLY wheel from a separate temporary path. Measurement
environments and the project dependency manifest were unchanged. A production
preparation run must record its own actual parser/wheel identities and import
origins, including optional dependencies; these local paths are not a portable
installation recipe.

The existing SDKBench QASM2 semantics parser is restricted to one declared
four-qubit import task. FlagQuantum's importer requires its emitter's canonical
subset. Neither is widened for these external programs. No new language grammar
or duplicate quantum reference is introduced.

## Frozen conversion rules

- Source is at most 1 MiB of UTF-8 text. Before parsing, bound every declared
  quantum/classical register and each total to twelve bits. Only the built-in
  `qelib1.inc` include is allowed; external filesystem/network includes refuse.
  Parse strict OpenQASM 2 with an empty include search path and no custom parser
  instructions or classical functions.
- Preserve all declared quantum wires, including idle wires, in source register
  declaration order. SDKBench q0 is the least significant basis index bit.
  Cross-check Cirq wire names and explicitly reverse the declared order for its
  big-endian simulation/matrix interface.
- The task is the coherent prefix before terminal measurements. Keep a trace of
  every removed terminal measurement and its quantum/classical indices. Any
  quantum operation after a measurement, reset, classical control, unresolved
  angle, nongate instruction or opaque gate refuses admission. This is not
  dynamic execution or sampled-output qualification.
- Barriers are annotations excluded from this unitary-only task, never a claimed
  scheduling constraint. Record top-level barriers and the number encountered
  inside definitions. Cirq does not accept barriers, so remove these annotations
  from its source text only after strict primary parsing. No quantum operation
  is deleted from that source projection. Measurement parsing remains independent.
- Recursively expand public gate definitions without calling synthesis,
  transpilation, optimization or matrix-to-Euler routines. Stop at genuine
  Qiskit U/CX gate objects rather than trusting their names. Emit CX with its
  original ordered operands. Emit U(theta,phi,lambda) in circuit order as
  RZ(lambda), RY(theta), RZ(phi); retain even zero rotations. Every participant
  receives this same expanded source, rather than its own preferred input form.
- Ignore only scalar whole-program/definition/U phases permitted by the existing
  operator contract. Record the program phase, nonzero definition phases and each
  primitive expansion's phase. Keep controlled-gate definition operations, so
  relative phase cannot be discarded as a local global phase. Check every angle
  and phase for finiteness.
- Bound source/definition traversal to 200000 nodes, definition path depth to 64,
  and the common canonical operation list to 20000 entries. Detect cycles and
  inconsistent definition arity. Budget refusal is an input-admission result,
  never permission to truncate, optimize, replace the program or raise its limit.

Call conversion under a bounded preparation supervisor: these structural limits
are not a process sandbox or a proof that native parser code cannot fail.
Before actual input admission, freeze preparation timeout, aggregate cgroup
memory and cleanup alongside the complete measurement/replay wall budget. Keep
raw parser crashes, dependency failures and partial preparation separate from
participant unsupported/compile/resource/semantic outcomes.

## Source-meaning conformance

At widths one through six, compare the complete converted operator with both
Qiskit's original coherent-prefix operator and Cirq's independently parsed
operator. Use the unchanged SDKBench phase-aware equivalence checker, 1e-8
absolute semantic tolerance and 1e-10 unitarity/normalization bound. One global
phase is compared across the whole operator, not independently per input column.

At widths eight/twelve, require exactly the three frozen W03 probe preparations
and compare complete output states against both original-source parsers. The
converter accepts other widths up to twelve for development, with the same
three-probe requirement above six; the frozen population remains 6/8/12.
Three-probe agreement does not prove universal equivalence or independently
certify the scientific algorithm. A parser disagreement or unsupported construct
refuses input admission; no alternate parser, case or tolerance is selected to
repair it after inspection. All fourteen intended source/target rows and four
workflow outcomes remain accounted for even when conversion refuses.

Return raw source SHA-256/size, register order, numeric operations, projection
trace, primitive definition paths and canonical index ranges, phase accounting,
expansion work counts, parser versions and maximum source-conformance residual.
These observations are preparation evidence; they are not a W03 verdict. Freeze
source files, converter/harness revision, all parser/dependency payloads and the
resulting bundle before measuring. Novelty auditing, required external notices,
independent campaign replay and publication/host qualification remain separate.

## Executable development path

In a preparation environment with the declared optional parsers installed:

```python
from sdkbench.candidates.external_qasm import convert_source

source = '''OPENQASM 2.0;
include "qelib1.inc";
qreg q[2];
h q[0];
cx q[0],q[1];
'''
prepared = convert_source(source)
assert prepared["n_qubits"] == 2
assert prepared["source_conformance"]["verification"] == "full-operator"
```

Expected: one common rotation/CX program with recorded definition expansion and
agreement with two original-source parsers. This example submits no remote job
and imports no FlagQuantum implementation. Run synthetic conformance with:

```sh
PYTHONPATH=src python -m pytest tests/test_external_qasm_preparation.py -q
```

Optional native-parser tests skip when their dependencies are absent; that is
not a native conformance pass. The tests cover analytic U/CX order, reversed
operands, multiple registers/idle wires, custom definitions, Toffoli's complete
basis permutation, phase traces, terminal measurement/barrier projection,
dynamic/opaque/malformed/budget refusals, three-probe scope, deliberate conversion
corruption, secondary-parser disagreement and forbidden compiler invocation.
No QASMBench circuit body is used as a test fixture.

## Local verification record

All eighteen synthetic converter checks pass with the declared native parsers.
The final focused run, including existing resource-replay and independent P0
evaluator checks, passed 158 tests in 48.38 seconds.
The first full local repository suite reached its 300-second external supervisor
limit before completion (progress output reached 23 percent); it is not a full
suite pass. The timed-out pytest process exited and a process inspection found
no remaining matching test processes. No frozen external source was inspected
or compiled during these tests. Full exact-head CI remains required.
