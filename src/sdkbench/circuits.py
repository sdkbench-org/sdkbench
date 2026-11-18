"""Deterministic circuit workloads and an explicit little-endian circuit IR."""
from dataclasses import dataclass
import math
import random

WORKLOADS = ("ghz", "qft", "brickwork", "echo")
GATES = {"h": 1, "x": 1, "ry": 1, "rz": 1, "cx": 2, "cp": 2}


@dataclass(frozen=True)
class Gate:
    name: str
    qubits: tuple[int, ...]
    angle: float = 0.0

    def __post_init__(self):
        if not isinstance(self.name, str) or self.name not in GATES:
            raise ValueError("Unsupported gate")
        if not isinstance(self.qubits, tuple) or len(self.qubits) != GATES[self.name]:
            raise ValueError("Unsupported gate or incorrect arity")
        if len(set(self.qubits)) != len(self.qubits):
            raise ValueError("Gate operands must be distinct")
        if any(type(q) is not int or q < 0 for q in self.qubits):
            raise ValueError("Qubit indices must be nonnegative integers")
        if type(self.angle) not in (int, float) or not math.isfinite(self.angle):
            raise ValueError("Angle must be finite")
        if self.name not in ("ry", "rz", "cp") and self.angle != 0:
            raise ValueError("Nonparameterized gates require angle=0")


@dataclass(frozen=True)
class Circuit:
    n_qubits: int
    gates: tuple[Gate, ...]

    def __post_init__(self):
        if type(self.n_qubits) is not int or not 1 <= self.n_qubits <= 16:
            raise ValueError("Circuit n_qubits must be an integer in 1..16")
        if not isinstance(self.gates, tuple) or any(not isinstance(g, Gate) for g in self.gates):
            raise ValueError("gates must be a tuple of Gate objects")
        if any(q >= self.n_qubits for g in self.gates for q in g.qubits):
            raise ValueError("Gate refers to a qubit outside the circuit")

    def inverse(self):
        return Circuit(self.n_qubits, tuple(
            Gate(g.name, g.qubits, -g.angle) for g in reversed(self.gates)))

    def compose(self, other):
        if self.n_qubits != other.n_qubits:
            raise ValueError("Cannot compose circuits of different widths")
        return Circuit(self.n_qubits, self.gates + other.gates)


def make_workload(name, n_qubits=8, depth=4, seed=0):
    """Generate a shared gate sequence. depth applies only to brickwork and echo."""
    if name not in WORKLOADS:
        raise ValueError("Unknown workload: " + str(name))
    if type(n_qubits) is not int or not 2 <= n_qubits <= 16:
        raise ValueError("n_qubits must be an integer in 2..16")
    if type(depth) is not int or not 1 <= depth <= 256:
        raise ValueError("depth must be an integer in 1..256")
    if type(seed) is not int or not 0 <= seed < 2**32:
        raise ValueError("seed must be an integer in 0..2**32-1")
    gates = []
    if name == "ghz":
        gates = [Gate("h", (0,))] + [Gate("cx", (q-1, q)) for q in range(1, n_qubits)]
    elif name == "qft":
        # Forward QFT, with no final swaps. Its exact ordered gate sequence is the workload.
        for q in reversed(range(n_qubits)):
            gates.append(Gate("h", (q,)))
            for control in reversed(range(q)):
                gates.append(Gate("cp", (control, q), math.pi / 2**(q-control)))
    else:
        rng = random.Random(seed)
        for layer in range(depth):
            for q in range(n_qubits):
                gates.extend([Gate("ry", (q,), rng.uniform(-math.pi, math.pi)),
                              Gate("rz", (q,), rng.uniform(-math.pi, math.pi))])
            gates.extend(Gate("cx", (q, q+1)) for q in range(layer % 2, n_qubits-1, 2))
    circuit = Circuit(n_qubits, tuple(gates))
    return circuit.compose(circuit.inverse()) if name == "echo" else circuit
