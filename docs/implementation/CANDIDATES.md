# Candidate package snapshot

Observed from PyPI metadata on 2026-11-18. These are candidate versions, not resolved environments, verified installs, compatible component stacks or evidence of task support. Freeze full dependency locks and wheel/source hashes after eligibility review; a changed version requires an explicit protocol/environment amendment.

| Package | Observed version | Declared Python requirement | Metadata source |
| --- | --- | --- | --- |
| flagquantum | 0.3.1 | <3.13,>=3.10 | [PyPI](https://pypi.org/pypi/flagquantum/json) |
| qiskit | 2.6.2 | >=3.10 | [PyPI](https://pypi.org/pypi/qiskit/json) |
| qiskit-aer | 0.18.4 | >=3.11 | [PyPI](https://pypi.org/pypi/qiskit-aer/json) |
| cirq-core | 1.7.0 | >=3.11.0 | [PyPI](https://pypi.org/pypi/cirq-core/json) |
| pennylane | 0.45.1 | >=3.11 | [PyPI](https://pypi.org/pypi/pennylane/json) |
| pennylane-lightning | 0.45.0 | >=3.11 | [PyPI](https://pypi.org/pypi/pennylane-lightning/json) |
| cudaq | 0.17.0 | >=3.11 | [PyPI](https://pypi.org/pypi/cudaq/json) |
| pytket | 2.18.5 | >=3.10 | [PyPI](https://pypi.org/pypi/pytket/json) |
| qibo | 0.3.7 | <3.15,>=3.12 | [PyPI](https://pypi.org/pypi/qibo/json) |
| qibojit | 0.1.18 | <3.15,>=3.12 | [PyPI](https://pypi.org/pypi/qibojit/json) |
| qulacs | 0.6.14 | not declared | [PyPI](https://pypi.org/pypi/qulacs/json) |
| mindquantum | 0.12.0 | >=3.7 | [PyPI](https://pypi.org/pypi/mindquantum/json) |
| tensorcircuit-ng | 1.10.0 | >=3.9 | [PyPI](https://pypi.org/pypi/tensorcircuit-ng/json) |
| torchquantum | 0.1.8 | >=3.5 | [PyPI](https://pypi.org/pypi/torchquantum/json) |
| amazon-braket-sdk | 1.127.8 | >=3.11 | [PyPI](https://pypi.org/pypi/amazon-braket-sdk/json) |
| qiskit-ibm-runtime | 0.52.1 | >=3.10 | [PyPI](https://pypi.org/pypi/qiskit-ibm-runtime/json) |
| cirq-google | 1.7.0 | >=3.11.0 | [PyPI](https://pypi.org/pypi/cirq-google/json) |

## Proposed eligibility review by role

Package names identify components for investigation, not independent leaderboard entries. The actual registered unit is one declared SDK/component/backend stack.

### exact

Exact requested outputs and sampling on local CPU; numeric precision is a task constraint.

`flagquantum`, `qiskit`, `qiskit-aer`, `cirq-core`, `pennylane`, `pennylane-lightning`, `cudaq`, `qibo`, `qibojit`, `qulacs`, `mindquantum`, `tensorcircuit-ng`.

### adaptive

Native or registered execution of the specified adaptive programs; no benchmark-side implementation of missing feed-forward.

`flagquantum`, `qiskit`, `qiskit-aer`, `cirq-core`, `pennylane`, `cudaq`, `qibo`, `mindquantum`, `tensorcircuit-ng`.

### compiler

Target-legal all-to-all-to-constrained compilation with semantic checks.

`flagquantum`, `qiskit`, `cirq-core`, `pytket`, `pennylane`, `cudaq`, `qibo`, `mindquantum`, `tensorcircuit-ng`.

### derivative

Declared exact-expectation derivative workflows; external components and evaluations disclosed.

`flagquantum`, `pennylane`, `pennylane-lightning`, `tensorcircuit-ng`, `mindquantum`, `torchquantum`, `cudaq`, `qiskit`, `qibo`, `cirq-core`.

### learning

The fixed hybrid regression contract with a common explicit SGD recurrence.

`flagquantum`, `pennylane`, `tensorcircuit-ng`, `mindquantum`, `torchquantum`, `cudaq`, `qiskit`, `qibo`, `cirq-core`.

### orchestration

Recoverable provider-client or registered integrated-client workflow using offline transport stubs.

`amazon-braket-sdk`, `qiskit-ibm-runtime`, `cirq-google`, `flagquantum`, `qibo`.

### interchange

Declared QASM subset round trips; profile-specific missing support remains visible.

`flagquantum`, `qiskit`, `cirq-core`, `pytket`, `pennylane`, `cudaq`, `qibo`, `qulacs`, `mindquantum`, `tensorcircuit-ng`.
