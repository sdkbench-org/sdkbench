"""P1b contracts and artifact normalization; no derivative, simulation or routing solver."""
from contextlib import contextmanager
import signal
import time
import numpy as np
from ..p0.models import finite, integer, require
from ..p1a.common import SDKS,DISTRIBUTIONS,VERSIONS,UnsupportedCapability

WORKFLOWS=('W03','W05','W07')
KINDS=('gradient','dynamics','route')
EXTENSIONS={'qiskit-algorithms':'0.4.0'}
CONFIGURATIONS={
    'flagquantum': {'gradient': 'fq.jacobian/autograd', 'routing': 'compiler.compile default level 2; native_gate_legalization',
                    'basis': ['h','x','y','z','s','sdg','rx','ry','rz','cz'], 'compiler_seed_supported': False,
                    'native_legalizer_max_added_operations': 20000},
    'qiskit': {'gradient': 'qiskit-algorithms==0.4.0 ReverseEstimatorGradient', 'routing': 'transpile',
               'optimization_level': 2, 'approximation_degree': 1.0, 'qubits_initially_zero': False,
               'basis': ['cz','u'], 'num_processes': 1, 'compiler_seed_supported': True},
    'cirq': {'gradient': 'unsupported in cirq-core==1.7.0', 'routing': 'RouteCQC; CZTargetGateset',
             'allow_partial_czs': False, 'synthesis_atol': 1e-12, 'initial_mapper': 'identity', 'compiler_seed_supported': False}}



def validate_fixture(kind,fixture):
    require(kind in KINDS,'Task kind is outside P1b')
    n=integer(fixture['n_qubits'],1)
    for op in fixture['operations']:
        name=op['name'];require(name in ('h','x','rx','ry','rz','rzz','cx','cz'),'Unknown frozen operation')
        require(len(op['qubits'])==(2 if name in ('rzz','cx','cz') else 1),'Invalid operation arity')
        for q in op['qubits']:integer(q);require(q<n,'Operation outside declared width')
        require(len(set(op['qubits']))==len(op['qubits']),'Repeated operation wire')
        if name in ('rx','ry','rz','rzz'):
            require(('angle' in op)!=('parameter' in op),'Rotation requires one angle source')
            if 'angle' in op:finite(op['angle'])
            else:integer(op['parameter']);require(op['parameter']<len(fixture['parameters']),'Unbound parameter')
    if kind=='gradient':
        for value in fixture['parameters']:finite(value)
        require(len(fixture['parameters'])==3*n,'Wrong shared parameter count')
    if kind=='dynamics':
        integer(fixture['initial_basis_index']);require(fixture['initial_basis_index']<1<<n,'Bad initial basis index')
    if kind=='route':
        require(fixture['initial_layout']=='identity' and fixture['ancillas_allowed']==0,'Unsupported target contract')


def matrix_payload(value):
    array=np.asarray(value,dtype=np.complex128)
    require(array.shape==(2,2) and np.isfinite(array).all(),'Invalid native one-qubit matrix')
    return np.stack([array.real,array.imag],axis=-1).tolist()


@contextmanager
def compile_deadline(seconds=120):
    """The default SIGALRM action terminates even a GIL-holding native compiler.

    This is a POSIX worker-stage bound, additional to the parent cgroup wall cap.
    No Python exception handler waits for a native call to return.
    """
    require(hasattr(signal,'setitimer'),'A kernel per-compile timer is required')
    old_handler=signal.getsignal(signal.SIGALRM);old_timer=signal.getitimer(signal.ITIMER_REAL)
    require(old_timer[0]==0,'An active timer would conflict with the compile stage')
    signal.signal(signal.SIGALRM,signal.SIG_DFL)
    signal.setitimer(signal.ITIMER_REAL,seconds)
    try:yield
    finally:
        signal.setitimer(signal.ITIMER_REAL,0);signal.signal(signal.SIGALRM,old_handler)


def load_adapter(name):
    if name=='flagquantum':
        from .flagquantum import FlagQuantumP1b
        return FlagQuantumP1b()
    if name=='qiskit':
        from .qiskit import QiskitP1b
        return QiskitP1b()
    if name=='cirq':
        from .cirq import CirqP1b
        return CirqP1b()
    raise ValueError('Unknown SDK')


class P1bBase:
    def execute(self,kind,fixture,seed):
        validate_fixture(kind,fixture)
        self.audit={'native_program_builds':0,'native_executions':0}
        if kind=='gradient':return self.gradient(fixture)
        if kind=='dynamics':return self.dynamics(fixture)
        with compile_deadline(120):
            start=time.perf_counter();payload=self.route(fixture,seed)
            payload['compile_wall_seconds']=time.perf_counter()-start
        return payload
