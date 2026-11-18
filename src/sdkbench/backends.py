"""SDK adapters; optional SDKs are imported only when explicitly selected."""
from importlib.metadata import version
import importlib.util
import numpy as np
from .circuits import Circuit
from .reference import simulate

BACKENDS = ("reference", "qiskit", "cirq")


class BackendUnavailable(RuntimeError):
    pass


class ReferenceBackend:
    name = "reference"
    version = np.__version__
    compile_target = None

    def build(self, circuit):
        return Circuit(circuit.n_qubits, tuple(list(circuit.gates)))

    def inverse(self, circuit):
        return circuit.inverse()

    def compose(self, circuit):
        return circuit.compose(circuit)

    def simulate(self, circuit, n_qubits, initial_state=None):
        return simulate(circuit, initial_state)

    def compile(self, circuit, seed):
        raise NotImplementedError("Reference oracle does not implement compilation")

    def metrics(self, circuit):
        levels = [0]*circuit.n_qubits
        for gate in circuit.gates:
            depth = 1+max(levels[q] for q in gate.qubits)
            for q in gate.qubits:
                levels[q] = depth
        return {"gates":len(circuit.gates),"two_qubit_gates":sum(len(g.qubits)==2 for g in circuit.gates),"depth":max(levels)}


class QiskitBackend:
    name = "qiskit"
    compile_target = "all-to-all CZ plus arbitrary one-qubit U, optimization_level=2"

    def __init__(self):
        from qiskit import QuantumCircuit, transpile
        from qiskit.quantum_info import Statevector
        self.QuantumCircuit,self.transpile,self.Statevector = QuantumCircuit,transpile,Statevector
        self.version = version("qiskit")

    def build(self, circuit):
        native = self.QuantumCircuit(circuit.n_qubits)
        for gate in circuit.gates:
            operands = (gate.angle, *gate.qubits) if gate.name in ("ry","rz","cp") else gate.qubits
            getattr(native,gate.name)(*operands)
        return native

    def inverse(self, circuit):
        return circuit.inverse()

    def compose(self, circuit):
        return circuit.compose(circuit, inplace=False)

    def simulate(self, circuit, n_qubits, initial_state=None):
        if initial_state is None:
            return self.Statevector.from_instruction(circuit).data
        return self.Statevector(initial_state).evolve(circuit).data

    def compile(self, circuit, seed):
        return self.transpile(circuit, basis_gates=["u","cz"], optimization_level=2, seed_transpiler=seed)

    def metrics(self, circuit):
        return {"gates":len(circuit.data),"two_qubit_gates":sum(len(g.qubits)==2 for g in circuit.data),"depth":circuit.depth()}


class CirqBackend:
    name = "cirq"
    compile_target = "all-to-all CZ plus arbitrary one-qubit gates, CZTargetGateset"

    def __init__(self):
        import cirq
        self.cirq = cirq
        self.version = version("cirq-core")
        self.simulator = cirq.Simulator(dtype=np.complex128)

    def build(self, circuit):
        c = self.cirq
        qubits = c.LineQubit.range(circuit.n_qubits)
        ops = []
        for gate in circuit.gates:
            q = [qubits[i] for i in gate.qubits]
            if gate.name == "h": op = c.H(*q)
            elif gate.name == "x": op = c.X(*q)
            elif gate.name == "ry": op = c.ry(gate.angle)(*q)
            elif gate.name == "rz": op = c.rz(gate.angle)(*q)
            elif gate.name == "cx": op = c.CNOT(*q)
            else: op = c.CZPowGate(exponent=gate.angle/np.pi)(*q)
            ops.append(op)
        return c.Circuit(ops)

    def inverse(self, circuit):
        return self.cirq.inverse(circuit)

    def compose(self, circuit):
        return circuit + circuit

    def simulate(self, circuit, n_qubits, initial_state=None):
        # Reverse native qubit order to make logical qubit 0 the least significant bit.
        order = list(reversed(self.cirq.LineQubit.range(n_qubits)))
        state = 0 if initial_state is None else np.array(initial_state, copy=True)
        return self.simulator.simulate(circuit, qubit_order=order, initial_state=state).final_state_vector

    def compile(self, circuit, seed):
        return self.cirq.optimize_for_target_gateset(circuit, gateset=self.cirq.CZTargetGateset(allow_partial_czs=False))

    def metrics(self, circuit):
        ops = list(circuit.all_operations())
        return {"gates":len(ops),"two_qubit_gates":sum(len(op.qubits)==2 for op in ops),"depth":len(circuit)}


def available_backends():
    return {name:name=="reference" or importlib.util.find_spec(name) is not None for name in BACKENDS}


def get_backend(name):
    if name not in BACKENDS:
        raise ValueError("Unknown backend: " + str(name))
    if not available_backends()[name]:
        raise BackendUnavailable(f"Install optional SDK support with: pip install 'sdkbench[{name}]'")
    return {"reference":ReferenceBackend,"qiskit":QiskitBackend,"cirq":CirqBackend}[name]()
