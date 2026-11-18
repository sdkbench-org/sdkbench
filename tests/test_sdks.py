"""Real optional SDK integration tests, skipped if that SDK is not installed."""
import numpy as np
import pytest
from sdkbench import Circuit,Gate,make_workload,run_benchmarks
from sdkbench.backends import get_backend,available_backends
from sdkbench.circuits import WORKLOADS
from sdkbench.reference import equivalent,simulate


@pytest.mark.parametrize('sdk',['qiskit','cirq'])
@pytest.mark.parametrize('workload',WORKLOADS)
def test_native_circuit_unitary_on_every_basis_state(sdk,workload):
    if not available_backends()[sdk]: pytest.skip(sdk+' is optional')
    backend=get_backend(sdk); spec=make_workload(workload,3,2,11); native=backend.build(spec)
    for initial in np.eye(8,dtype=complex):
        assert equivalent(backend.simulate(native,3,initial),simulate(spec,initial))
    inverse=backend.inverse(native)
    composed=backend.compose(native)
    # Exhaustive basis checks for transformations as well as the original circuit.
    for initial in np.eye(8,dtype=complex):
        assert equivalent(backend.simulate(inverse,3,initial),simulate(spec.inverse(),initial))
        assert equivalent(backend.simulate(composed,3,initial),simulate(spec.compose(spec),initial))


@pytest.mark.parametrize('sdk',['qiskit','cirq'])
def test_sdk_run_all_workloads_and_operations(sdk):
    if not available_backends()[sdk]: pytest.skip(sdk+' is optional')
    report=run_benchmarks(sdks=[sdk],n_qubits=3,depth=2,repeats=1,warmups=0)
    assert report['summary']=={'passed':20,'failed':0,'skipped':0,'error':0},report


@pytest.mark.parametrize('sdk',['qiskit','cirq'])
def test_unused_qubits_and_compile_target(sdk):
    if not available_backends()[sdk]: pytest.skip(sdk+' is optional')
    backend=get_backend(sdk)
    spec=Circuit(3,(Gate('h',(0,)),Gate('cx',(0,2))))
    native=backend.build(spec); compiled=backend.compile(native,3)
    assert equivalent(backend.simulate(compiled,3),simulate(spec))
    assert backend.metrics(compiled)['two_qubit_gates']>=1
    if sdk=='qiskit':
        assert set(compiled.count_ops()) <= {'u','cz'}
    else:
        import cirq
        for op in compiled.all_operations():
            assert len(op.qubits)<=2
            if len(op.qubits)==2:
                assert isinstance(op.gate,cirq.CZPowGate)
                assert float(op.gate.exponent)%2 == pytest.approx(1)
