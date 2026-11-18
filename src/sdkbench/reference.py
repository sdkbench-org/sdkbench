"""Small NumPy statevector oracle, independent of third-party quantum SDKs."""
import math
import numpy as np
from .circuits import Circuit


def simulate(circuit: Circuit, initial_state=None):
    size = 1 << circuit.n_qubits
    if initial_state is None:
        state = np.zeros(size, dtype=np.complex128)
        state[0] = 1
    else:
        state = np.array(initial_state, dtype=np.complex128, copy=True)
        if state.shape != (size,) or not np.isfinite(state).all():
            raise ValueError("Initial state must be a finite vector of length 2**n_qubits")
        if not np.isclose(np.vdot(state, state).real, 1, atol=1e-10, rtol=0):
            raise ValueError("Initial state must be normalized")
    indices = np.arange(size)
    for gate in circuit.gates:
        if gate.name == "cp":
            a,b = gate.qubits
            mask = ((indices >> a) & 1).astype(bool) & ((indices >> b) & 1).astype(bool)
            state[mask] *= np.exp(1j*gate.angle)
            continue
        if gate.name == "cx":
            control,target = gate.qubits
            low = indices[(((indices >> control)&1)==1) & (((indices >> target)&1)==0)]
            high = low | (1 << target)
            state[low],state[high] = state[high].copy(),state[low].copy()
            continue
        q = gate.qubits[0]
        low = indices[((indices >> q)&1)==0]
        high = low | (1 << q)
        if gate.name == "h":
            matrix = np.array([[1,1],[1,-1]]) / math.sqrt(2)
        elif gate.name == "x":
            matrix = np.array([[0,1],[1,0]])
        elif gate.name == "ry":
            c,s = math.cos(gate.angle/2),math.sin(gate.angle/2)
            matrix = np.array([[c,-s],[s,c]])
        elif gate.name == "rz":
            matrix = np.diag([np.exp(-.5j*gate.angle),np.exp(.5j*gate.angle)])
        else:
            raise ValueError("Unsupported gate: " + gate.name)
        a,b = state[low].copy(),state[high].copy()
        state[low] = matrix[0,0]*a + matrix[0,1]*b
        state[high] = matrix[1,0]*a + matrix[1,1]*b
    return state


def equivalent(actual, expected, atol=1e-8):
    """Check finite normalized vectors for agreement up to one global phase."""
    a,b = np.asarray(actual),np.asarray(expected)
    if a.shape != b.shape or a.ndim != 1 or not np.isfinite(a).all() or not np.isfinite(b).all():
        return False
    if not np.isclose(np.linalg.norm(a), 1, atol=atol, rtol=0):
        return False
    if not np.isclose(np.linalg.norm(b), 1, atol=atol, rtol=0):
        return False
    overlap = np.vdot(b, a)
    return bool(abs(overlap)>0 and np.allclose(a, b*overlap/abs(overlap), atol=atol, rtol=0))
