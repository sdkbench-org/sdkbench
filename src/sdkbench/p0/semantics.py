"""SDK-independent small-program semantics. No participant or gold-generator imports."""
import ast
import math
import re
import numpy as np
from .models import ContractError, finite, integer, keys, require


def real_array(value, shape):
    try:
        def check_leaves(item):
            if isinstance(item, (list, tuple)):
                for child in item:check_leaves(child)
            else:finite(item)
        check_leaves(value)
        raw = np.asarray(value)
        require(raw.dtype.kind in 'iuf' and raw.shape == tuple(shape), 'Wrong numeric type or shape')
        out = raw.astype(np.float64)
    except (ValueError, TypeError, OverflowError) as exc:
        raise ContractError('Malformed numeric array') from exc
    require(np.isfinite(out).all(), 'Nonfinite numeric output')
    return out


def rotation(name, angle):
    if name == 'h':return np.array([[1, 1], [1, -1]], complex) / math.sqrt(2)
    if name == 'x':return np.array([[0, 1], [1, 0]], complex)
    if name == 'y':return np.array([[0, -1j], [1j, 0]], complex)
    if name == 'z':return np.diag([1, -1]).astype(complex)
    if name in ('s', 'sdg'):return np.diag([1, 1j if name == 's' else -1j])
    require(name in ('rx', 'ry', 'rz'), 'Unknown one-qubit gate')
    pauli = rotation(name[-1], 0)
    return math.cos(angle / 2) * np.eye(2) - 1j * math.sin(angle / 2) * pauli


def operation(op, n, parameters=None, target_edges=None):
    require(isinstance(op, dict) and 'name' in op and 'qubits' in op, 'Malformed operation')
    name = op['name']; qubits = op['qubits']
    require(isinstance(qubits, list), 'Qubits must be a list')
    for q in qubits:integer(q); require(q < n, 'Wire outside program')
    require(len(set(qubits)) == len(qubits), 'Repeated operation wire')
    if name in ('cx', 'cz', 'rzz'):
        keys(op, ('name', 'qubits', 'angle') if name == 'rzz' else ('name', 'qubits'))
        require(len(qubits) == 2, 'Invalid two-qubit arity')
        if target_edges is not None:
            require(name == 'cz' and frozenset(qubits) in target_edges, 'Illegal target interaction/basis')
        angle = finite(op['angle']) if name == 'rzz' else 0
        return name, qubits, angle
    if name == 'unitary':
        keys(op, ('name', 'qubits', 'matrix'))
        require(len(qubits) == 1, 'Only one-qubit matrix operations are target-legal')
        parts = real_array(op['matrix'], (2, 2, 2)); matrix = parts[..., 0] + 1j * parts[..., 1]
        require(np.max(abs(matrix.conj().T @ matrix - np.eye(2))) <= 1e-10, 'Nonunitary gate matrix')
    else:
        require(name in ('h', 'x', 'y', 'z', 's', 'sdg', 'rx', 'ry', 'rz'), 'Unsupported gate')
        fields = ['name', 'qubits']
        angle = 0
        if name in ('rx', 'ry', 'rz'):
            require(('angle' in op) != ('parameter' in op), 'Rotation needs one angle source')
            fields.append('parameter' if 'parameter' in op else 'angle')
            if 'parameter' in op:
                integer(op['parameter']); require(parameters is not None and op['parameter'] < len(parameters), 'Unbound parameter')
                angle = finite(parameters[op['parameter']])
            else:angle = finite(op['angle'])
        keys(op, fields); require(len(qubits) == 1, 'Invalid one-qubit arity')
        matrix = rotation(name, angle)
    return 'matrix', qubits, matrix


def propagate(n, operations, initial=None, parameters=None, target_edges=None):
    state = np.zeros(1 << n, complex) if initial is None else np.array(initial, dtype=complex, copy=True)
    if initial is None:state[0] = 1
    require(state.shape[0] == 1 << n, 'Invalid state dimension')
    indices = np.arange(1 << n)
    for op in operations:
        name, qubits, arg = operation(op, n, parameters, target_edges)
        if name == 'matrix':
            stride = 1 << qubits[0]
            view = state.reshape((-1, 2, stride) + state.shape[1:])
            a = view[:, 0].copy(); b = view[:, 1].copy()
            view[:, 0] = arg[0, 0] * a + arg[0, 1] * b
            view[:, 1] = arg[1, 0] * a + arg[1, 1] * b
        else:
            a, b = qubits
            if name == 'cx':state = state[indices ^ (((indices >> a) & 1) << b)].copy()
            else:
                phase = (1 - 2 * (((indices >> a) & 1) & ((indices >> b) & 1))) if name == 'cz' else np.exp(-.5j * arg * (1 - 2 * (((indices >> a) ^ (indices >> b)) & 1)))
                state *= phase.reshape((-1,) + (1,) * (state.ndim - 1))
    return state


def equivalent(actual, expected, atol, norm_limit=1e-10):
    require(actual.shape == expected.shape, 'Semantic shape mismatch')
    if actual.ndim == 1:
        require(abs(np.vdot(actual, actual).real - 1) <= norm_limit, 'State normalization error')
    else:
        require(np.max(abs(actual.conj().T @ actual - np.eye(actual.shape[1]))) <= norm_limit, 'Operator unitarity error')
    pivot = np.unravel_index(np.argmax(abs(expected)), expected.shape)
    require(abs(actual[pivot]) > 0, 'Missing phase pivot')
    phase = actual[pivot] / expected[pivot]; phase /= abs(phase)
    error = float(np.max(abs(actual / phase - expected)))
    require(error <= atol, 'Program semantics differ')
    return error


def angle_expression(text):
    require(len(text) <= 100, 'Angle expression too long')
    try:node = ast.parse(text, mode='eval').body
    except SyntaxError as exc:raise ContractError('Invalid angle expression') from exc
    def visit(node):
        if isinstance(node, ast.Constant):return finite(node.value)
        if isinstance(node, ast.Name) and node.id == 'pi':return math.pi
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
            return (1 if isinstance(node.op, ast.UAdd) else -1) * visit(node.operand)
        if isinstance(node, ast.BinOp) and isinstance(node.op, (ast.Add, ast.Sub, ast.Mult, ast.Div)):
            a, b = visit(node.left), visit(node.right)
            if isinstance(node.op, ast.Add):return a + b
            if isinstance(node.op, ast.Sub):return a - b
            if isinstance(node.op, ast.Mult):return a * b
            require(b != 0, 'Zero angle divisor'); return a / b
        raise ContractError('Unsupported angle expression')
    return finite(visit(node))


def parse_qasm2(source):
    require(isinstance(source, str) and len(source) <= 100000, 'Invalid QASM source')
    source = re.sub(r'//[^\n]*', '', source)
    require(source.strip().endswith(';'), 'Missing QASM2 terminal semicolon')
    statements = [s.strip() for s in source.split(';') if s.strip()]
    require(len(statements) >= 4 and statements[0] == 'OPENQASM 2.0' and statements[1] == 'include "qelib1.inc"', 'Unsupported QASM2 header')
    require(statements[2] == 'qreg q[4]' and statements[3] == 'creg c[4]', 'Register declaration mismatch')
    ops = []; mapping = {}; measuring = False
    for text in statements[4:]:
        match = re.fullmatch(r'measure\s+q\[(\d+)\]\s*->\s*c\[(\d+)\]', text)
        if match:
            q, c = map(int, match.groups()); require(q < 4 and c < 4 and q not in mapping and c not in mapping.values(), 'Invalid measurement mapping')
            mapping[q] = c; measuring = True; continue
        require(not measuring, 'Gate after measurement is outside QASM2 subset')
        match = re.fullmatch(r'(h|x|y|z|s|sdg|rx|ry|rz|cx|cz)(?:\(([^()]+)\))?\s+q\[(\d+)\](?:\s*,\s*q\[(\d+)\])?', text)
        require(match is not None, 'Unsupported QASM2 syntax')
        name, angle, a, b = match.groups(); op = {'name': name, 'qubits': [int(a)] + ([int(b)] if b is not None else [])}
        require((angle is not None) == (name in ('rx', 'ry', 'rz')), 'Unexpected/missing angle')
        if angle is not None:op['angle'] = angle_expression(angle)
        operation(op, 4); ops.append(op)
    require(set(mapping) == set(range(4)), 'Missing measurement/register output')
    return ops, [mapping[q] for q in range(4)]


def qasm3_distribution(source):
    """Interpret the declared two-qubit measurement/reset/if subset branch by branch."""
    require(isinstance(source, str) and len(source) <= 100000, 'Invalid QASM source')
    source = re.sub(r'//[^\n]*', '', source)
    header = r'\s*OPENQASM\s+3\.0\s*;\s*include\s+"stdgates.inc"\s*;\s*qubit\[2\]\s+q\s*;\s*bit\[2\]\s+c\s*;'
    match = re.match(header, source); require(match is not None, 'Unsupported QASM3 header/registers')
    source = source[match.end():]; branches = [(0, np.array([1, 0, 0, 0], complex))]
    patterns = [
        ('if', r'if\s*\(c\[(\d+)\]\)\s*\{\s*x\s+q\[(\d+)\]\s*;\s*\}'),
        ('measure', r'c\[(\d+)\]\s*=\s*measure\s+q\[(\d+)\]\s*;'),
        ('reset', r'reset\s+q\[(\d+)\]\s*;'),
        ('gate', r'(h|x|z|cx|cz)\s+q\[(\d+)\](?:\s*,\s*q\[(\d+)\])?\s*;'),
    ]
    while source.strip():
        source = source.lstrip(); found = False
        for kind, pattern in patterns:
            match = re.match(pattern, source)
            if match is None:continue
            found = True; source = source[match.end():]; args = match.groups()
            if kind == 'gate':
                name, a, b = args; op = {'name': name, 'qubits': [int(a)] + ([int(b)] if b else [])}
                branches = [(bits, propagate(2, [op], state)) for bits, state in branches]
            elif kind == 'if':
                c, q = map(int, args); require(c < 2 and q < 2, 'Out-of-range conditional')
                branches = [(bits, propagate(2, [{'name': 'x', 'qubits': [q]}], state) if bits & (1 << c) else state) for bits, state in branches]
            else:
                c, q = map(int, args) if kind == 'measure' else (None, int(args[0]))
                require(q < 2 and (c is None or c < 2), 'Out-of-range measurement/reset')
                projected = []
                for bits, state in branches:
                    for outcome in (0, 1):
                        part = state.copy(); part[((np.arange(4) >> q) & 1) != outcome] = 0
                        if np.vdot(part, part).real < 1e-28:continue
                        if kind == 'reset' and outcome:part = propagate(2, [{'name': 'x', 'qubits': [q]}], part)
                        new_bits = bits if c is None else (bits & ~(1 << c)) | (outcome << c)
                        projected.append((new_bits, part))
                branches = projected
                require(len(branches) <= 4096, 'Too many QASM branches')
            break
        require(found, 'Unsupported QASM3 syntax')
    probabilities = np.zeros(4); q0_zero = 0.
    for bits, state in branches:
        probabilities[bits] += np.vdot(state, state).real; q0_zero += float(np.sum(abs(state[[0, 2]])**2))
    return probabilities, q0_zero
