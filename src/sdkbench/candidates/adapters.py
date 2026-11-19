"""Declared compiler workflows; numerical acceptance remains owned by P0."""
from copy import deepcopy
from datetime import datetime, timedelta, timezone
import math

from ..p0.models import digest, require
from ..p1a.common import UnsupportedCapability
from ..p1b.common import compile_deadline, matrix_payload, validate_fixture


WORKFLOWS = {
    'flagquantum-ordinary': {
        'sdk': 'flagquantum', 'entrypoint': 'compiler.compile; compiler.lowering.native_gate_legalization.legalize_native_gates',
        'options': {'routing': 'default', 'optimization_level': 'default',
                    'basis': ['h', 'x', 'y', 'z', 's', 'sdg', 'rx', 'ry', 'rz', 'cz'],
                    'max_added_operations': 20000, 'initial_layout': 'identity',
                    'final_layout': 'sdk-reported', 'compiler_seed_supported': False}},
    'flagquantum-target-artifact': {
        'sdk': 'flagquantum', 'entrypoint': 'compile_circuit_artifact_for_target',
        'options': {'basis': ['rx', 'rz', 'cz'], 'initial_layout': 'identity',
                    'final_layout': 'restored', 'routing': 'default',
                    'compiler_seed_supported': False, 'profile': 'openqasm-3.0',
                    'max_native_added_operations': 20000,
                    'max_routing_added_operations': 20000,
                    'maximum_program_operations': 20000,
                    'serialize_executable_artifact': True}},
    'qiskit-transpile': {
        'sdk': 'qiskit', 'entrypoint': 'qiskit.transpile',
        'options': {'basis': ['cz', 'u'], 'optimization_level': 2,
                    'approximation_degree': 1.0, 'qubits_initially_zero': False,
                    'num_processes': 1, 'initial_layout': 'identity',
                    'final_layout': 'sdk-reported', 'compiler_seed_supported': True}},
    'cirq-route-cz': {
        'sdk': 'cirq', 'entrypoint': 'RouteCQC; optimize_for_target_gateset',
        'options': {'basis': ['cz', 'arbitrary-one-qubit-unitary'],
                    'allow_partial_czs': False, 'synthesis_atol': 1e-12,
                    'initial_mapper': 'identity', 'initial_layout': 'identity',
                    'final_layout': 'sdk-reported', 'compiler_seed_supported': False}},
}


# Preserve the original open-output configurations; controls get new identities.
for _name in ('flagquantum-ordinary', 'qiskit-transpile', 'cirq-route-cz'):
    _control = deepcopy(WORKFLOWS[_name])
    _control['options']['postprocessing'] = {
        'final_layout': 'identity', 'algorithm': 'spanning-tree-leaf-token-restoration-v1',
        'tree_root': 0, 'neighbor_order': 'ascending', 'leaf_order': 'ascending',
        'swap_decomposition': 'H-CZ-H CNOT triple', 'optimization_after_restoration': False,
        'timed': True,
    }
    WORKFLOWS[_name + '-restored'] = _control


def workflow_configuration(name):
    """Return the complete supported configuration to bind before execution."""
    require(name in WORKFLOWS, 'Unknown candidate compiler workflow')
    return deepcopy(WORKFLOWS[name])


def _normalize_operations(program, basis):
    operations = []
    for op in program.instructions:
        require(op.matrix is None and op.name in basis, 'Non-target candidate instruction')
        item = {'name': op.name, 'qubits': list(op.wires)}
        if op.name in ('rx', 'ry', 'rz'):
            item['angle'] = float(op.params['theta'])
        operations.append(item)
    return operations


def _ordinary_flagquantum_route(adapter, fixture, seed):
    from flagquantum.compiler import CouplingMap, compile, final_layout
    from flagquantum.compiler.lowering.native_gate_legalization import legalize_native_gates
    from ..diagnostics.routing import target_snapshot
    circuit = adapter.fq.Circuit(fixture['n_qubits'], device='cpu', dtype=adapter.torch.complex128)
    for operation in fixture['operations']:
        params = ({'theta': adapter.torch.tensor(operation['angle'], dtype=adapter.torch.float64)}
                  if operation['name'] in ('rx', 'ry', 'rz', 'rzz') else {})
        circuit.gate(operation['name'], operation['qubits'], params=params)
    basis = WORKFLOWS['flagquantum-ordinary']['options']['basis']
    routed = compile(circuit, coupling_map=CouplingMap(fixture['n_qubits'], fixture['target_edges']),
                     config=circuit.runtime_config)
    require(list(routed.metadata['routing']['initial_logical_to_physical'])
            == list(range(fixture['n_qubits'])), 'Compiler changed initial layout')
    compiled = legalize_native_gates(routed, snapshot=target_snapshot(fixture, basis),
                                    max_added_operations=20000).program
    adapter.audit.update(native_program_builds=1, native_compilations=1, compiler_seed_supported=0)
    return {'operations': _normalize_operations(compiled, basis),
            'final_layout': list(final_layout(routed).logical_to_physical)}


def _qiskit_route(adapter, fixture, seed):
    from qiskit.quantum_info import Operator
    source = adapter.qiskit.QuantumCircuit(fixture['n_qubits'])
    for operation in fixture['operations']:
        arguments = list(operation['qubits'])
        if operation['name'] in ('rx', 'ry', 'rz', 'rzz'):
            arguments.insert(0, operation['angle'])
        getattr(source, operation['name'])(*arguments)
    n = fixture['n_qubits']
    compiled = adapter.qiskit.transpile(
        source, basis_gates=['cz', 'u'],
        coupling_map=[pair for a, b in fixture['target_edges'] for pair in ([a, b], [b, a])],
        initial_layout=list(range(n)), optimization_level=2,
        approximation_degree=1.0, qubits_initially_zero=False,
        seed_transpiler=seed, num_processes=1)
    require(compiled.num_qubits == n, 'Compiler introduced ancillas')
    require(compiled.layout is not None
            and [compiled.layout.initial_layout[q] for q in source.qubits] == list(range(n)),
            'Compiler changed initial layout')
    operations = []
    for item in compiled.data:
        qubits = [compiled.find_bit(q).index for q in item.qubits]
        if item.operation.name == 'cz':
            operations.append({'name': 'cz', 'qubits': qubits})
        else:
            require(len(qubits) == 1, 'Non-target compiler interaction')
            operations.append({'name': 'unitary', 'qubits': qubits,
                               'matrix': matrix_payload(Operator(item.operation).data)})
    adapter.audit.update(native_program_builds=1, native_compilations=1, compiler_seed_supported=1)
    return {'operations': operations,
            'final_layout': list(compiled.layout.final_index_layout(filter_ancillas=True))}


def _cirq_route(adapter, fixture, seed):
    import networkx as nx
    cirq = adapter.cirq
    n = fixture['n_qubits']
    qubits = cirq.LineQubit.range(n)
    graph = nx.Graph()
    graph.add_nodes_from(qubits)
    graph.add_edges_from((qubits[a], qubits[b]) for a, b in fixture['target_edges'])
    source_operations = []
    for operation in fixture['operations']:
        selected = [qubits[q] for q in operation['qubits']]
        name = operation['name']
        if name in ('rx', 'ry', 'rz'):
            source_operations.append(getattr(cirq, name)(operation['angle']).on(*selected))
        elif name == 'rzz':
            source_operations.append(cirq.ZZPowGate(exponent=operation['angle'] / math.pi,
                                                   global_shift=-0.5).on(*selected))
        else:
            source_operations.append({'h': cirq.H, 'x': cirq.X, 'cx': cirq.CNOT, 'cz': cirq.CZ}[name].on(*selected))
    source = cirq.Circuit(source_operations)
    routed, initial, final = cirq.RouteCQC(graph).route_circuit(
        source, initial_mapper=cirq.HardCodedInitialMapper({q: q for q in qubits}))
    require(all(initial[q] == q for q in qubits), 'Compiler changed initial layout')
    compiled = cirq.optimize_for_target_gateset(
        routed, gateset=cirq.CZTargetGateset(atol=1e-12, allow_partial_czs=False),
        ignore_failures=False)
    operations = []
    for op in compiled.all_operations():
        selected = [qubits.index(q) for q in op.qubits]
        if not selected:
            continue  # Frozen acceptance permits one global phase.
        if len(selected) == 1:
            operations.append({'name': 'unitary', 'qubits': selected,
                               'matrix': matrix_payload(cirq.unitary(op))})
        else:
            require(isinstance(op.gate, cirq.CZPowGate)
                    and abs(float(op.gate.exponent) % 2 - 1) < 1e-12,
                    'Non-full-CZ compiler interaction')
            operations.append({'name': 'cz', 'qubits': selected})
    adapter.audit.update(native_program_builds=1, native_compilations=1, compiler_seed_supported=0)
    return {'operations': operations,
            'final_layout': [qubits.index(final[initial[q]]) for q in qubits]}


def _target_artifact_route(adapter, fixture, seed):
    from flagquantum.compiler.artifacts.artifact_compilation import compile_circuit_artifact_for_target
    from flagquantum.compiler.routing import CouplingMap
    from flagquantum.core._artifacts import ProgramArtifactV2
    from flagquantum.core.ir import CircuitIR, Instruction, MeasurementNode
    from flagquantum.core.target_capabilities import (
        CapabilityFact, CapabilityScope, EvidenceLevel, EvidenceReference,
        FactExposure, FactSource, SupportStatus, TargetCapabilitySnapshot, TargetIdentity,
    )
    n = fixture['n_qubits']
    if any('parameter' in op for op in fixture['operations']):
        raise UnsupportedCapability('Target-artifact candidate requires fixed numeric routing fixtures')
    source = CircuitIR(n, tuple(
        Instruction(op['name'], tuple(op['qubits']),
                    params={'theta': op['angle']} if 'angle' in op else {})
        for op in fixture['operations']),
        measurements=(MeasurementNode('samples', tuple(range(n))),), dtype='complex128')
    now = datetime.now(timezone.utc)
    scope = CapabilityScope(device_ids=('sdkbench-abstract-cz',))
    facts = {'qubits.logical_capacity': n, 'limits.maximum_program_operations': 20000,
             'precision.effective_dtype': 'complex128', 'gates.native': ('rx', 'rz', 'cz'),
             'artifacts.profiles': ('openqasm-3.0',), 'measurements.results': ('samples',),
             'limits.maximum_shots': 1024}
    definition = {'facts': facts, 'edges': fixture['target_edges'],
                  'meaning': 'abstract compiler target; no hardware capability claim'}
    snapshot = TargetCapabilitySnapshot(
        target_identity=TargetIdentity('sdkbench-abstract-cz', 'abstract', 'sdkbench',
                                       '0.4.0', 'candidate', 'offline'),
        scope=scope, captured_at=now.isoformat(), valid_until=(now + timedelta(hours=1)).isoformat(),
        facts=tuple(CapabilityFact(name=key, value=value, support_status=SupportStatus.VERIFIED,
                                  fact_exposure=FactExposure.OBSERVED if key == 'precision.effective_dtype'
                                  else FactExposure.DECLARED,
                                  source=FactSource(kind='test', ref='abstract-definition'))
                    for key, value in facts.items()),
        evidence_refs=(EvidenceReference(evidence_id='abstract-definition', sha256=digest(definition),
                                         level=EvidenceLevel.OBSERVABLE, scope=scope),))
    result = compile_circuit_artifact_for_target(
        ProgramArtifactV2.from_circuit_ir(source, producer='sdkbench-candidate'),
        backend='qasm', profile='openqasm-3.0', producer='sdkbench-candidate',
        snapshot=snapshot, evaluated_at=now,
        coupling_map=CouplingMap(n, fixture['target_edges']),
        max_native_added_operations=20000, max_routing_added_operations=20000)
    # Serialization is part of the declared workflow and timed interval.
    serialized = result.executable_artifact.to_json()
    adapter.compiler_evidence = {'executable_artifact': serialized,
                                 'target_snapshot_id': snapshot.snapshot_id}
    operations = _normalize_operations(result.legalization.program, ('rx', 'rz', 'cz'))
    stage = result.legalization.native_block_optimization
    baseline = result.legalization.native_gate_legalization.program
    adapter.audit.update(native_program_builds=1, native_compilations=1,
                         compiler_seed_supported=0, native_baseline_cz_count=sum(
                             op.name == 'cz' for op in baseline.instructions),
                         accepted_block_rewrites=len(stage.rewrites) if stage is not None else 0,
                         serialized_artifact_bytes=len(serialized.encode('utf-8')))
    return {'operations': operations, 'final_layout': list(result.physical_plan.final_logical_to_physical)}


class CompilerAdapter:
    """Reuse native adapters; add only the explicitly registered artifact path."""
    def __init__(self, native, workflow):
        self.native = native
        self.workflow = workflow
        self.audit = {}

    def execute(self, kind, fixture, seed):
        import time
        require(kind == 'route', 'Candidate compiler adapter only supports routing tasks')
        validate_fixture(kind, fixture)
        if any('parameter' in operation for operation in fixture['operations']):
            raise UnsupportedCapability('Candidate routing workflows require explicit numeric bindings')
        with compile_deadline(120):
            started = time.perf_counter()
            self.native.audit = {'native_program_builds': 0, 'native_executions': 0}
            base_workflow = self.workflow.removesuffix('-restored')
            if base_workflow == 'flagquantum-target-artifact':
                payload = _target_artifact_route(self.native, fixture, seed)
            elif base_workflow == 'flagquantum-ordinary':
                payload = _ordinary_flagquantum_route(self.native, fixture, seed)
            elif base_workflow == 'qiskit-transpile':
                payload = _qiskit_route(self.native, fixture, seed)
            else:
                payload = _cirq_route(self.native, fixture, seed)
            if self.workflow.endswith('-restored'):
                from .layout import restore_payload
                self.native.audit.update(restore_payload(payload, fixture['target_edges']))
            payload['compile_wall_seconds'] = time.perf_counter() - started
        self.audit = dict(self.native.audit)
        return payload


def load_adapter(registration):
    """Load only a reviewed workflow whose entire configuration was registered."""
    options = registration.configuration['options']
    name = options['workflow']
    config = workflow_configuration(name)
    require(options['sdk'] == config['sdk'] and options['compiler_options'] == config,
            'Candidate workflow differs from its registered configuration')
    from ..p1b.common import load_adapter as load_native
    return CompilerAdapter(load_native(config['sdk']), name)
