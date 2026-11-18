import math
import numpy as np
import pytest
from sdkbench import Circuit, Gate, make_workload
from sdkbench.circuits import WORKLOADS
from sdkbench.reference import equivalent, simulate


def test_seeded_workloads():
    assert make_workload('brickwork',4,3,7) == make_workload('brickwork',4,3,7)
    assert make_workload('brickwork',4,3,7) != make_workload('brickwork',4,3,8)
    assert len(make_workload('ghz',5).gates)==5
    assert len(make_workload('qft',5).gates)==15


@pytest.mark.parametrize('name',WORKLOADS)
def test_inverse_and_composition_on_random_input(name):
    circuit=make_workload(name,4,2,3)
    rng=np.random.default_rng(7)
    initial=rng.normal(size=16)+1j*rng.normal(size=16); initial/=np.linalg.norm(initial)
    result=simulate(circuit.compose(circuit.inverse()),initial)
    assert equivalent(result,initial)
    assert equivalent(simulate(circuit.compose(circuit),initial),simulate(circuit,simulate(circuit,initial)))
    assert circuit.inverse().inverse()==circuit


def test_ghz_and_little_endian_gates():
    result=simulate(make_workload('ghz',4))
    expected=np.zeros(16,dtype=complex); expected[[0,15]]=1/math.sqrt(2)
    assert equivalent(result,expected)
    assert np.argmax(abs(simulate(Circuit(3,(Gate('x',(0,)),)))))==1
    assert np.argmax(abs(simulate(Circuit(3,(Gate('x',(2,)),)))))==4
    circuit=Circuit(3,(Gate('x',(0,)),Gate('cx',(0,2))))
    assert np.argmax(abs(simulate(circuit)))==5


def test_qft_against_dense_fourier_matrix():
    n=3; size=1<<n
    circuit=make_workload('qft',n)
    reverse=[int(f'{x:0{n}b}'[::-1],2) for x in range(size)]
    for x in range(size):
        initial=np.eye(size,dtype=complex)[x]
        expected=np.exp(2j*np.pi*x*np.arange(size)/size)/np.sqrt(size)
        assert equivalent(simulate(circuit,initial)[reverse],expected)


def test_echo_is_identity():
    initial=np.ones(8,dtype=complex)/np.sqrt(8)
    assert equivalent(simulate(make_workload('echo',3,3),initial),initial)


def test_single_qubit_rotation_conventions():
    assert equivalent(simulate(Circuit(1,(Gate('ry',(0,),math.pi),))),np.array([0.,1.]))
    initial=np.array([1.,1.])/np.sqrt(2)
    expected=np.array([np.exp(-.25j),np.exp(.25j)])/np.sqrt(2)
    assert equivalent(simulate(Circuit(1,(Gate('rz',(0,),.5),)),initial),expected)
    initial=np.ones(4)/2
    expected=np.array([1,1,1,np.exp(.3j)])/2
    assert equivalent(simulate(Circuit(2,(Gate('cp',(0,1),.3),)),initial),expected)


@pytest.mark.parametrize('actual',[np.array([1,1]),np.array([0.,0.]),np.array([float('nan'),0]),np.ones(3),np.array([[1,0]])])
def test_bad_states_rejected(actual):
    assert not equivalent(actual,np.array([1.,0.]))


def test_global_phase_and_relative_phase():
    a=np.array([1.,1.])/np.sqrt(2)
    assert equivalent(1j*a,a)
    assert not equivalent(a*np.array([1,-1]),a)
    with pytest.raises(ValueError): simulate(Circuit(1,()),[1,1])
    with pytest.raises(ValueError): simulate(Circuit(1,()),[1,0,0])


@pytest.mark.parametrize('factory',[
    lambda:Gate('h',[0]),lambda:Gate('ry',(0,),'bad'),lambda:make_workload('ghz',2,1,-1),
    lambda:Gate('bad',(0,)),lambda:Gate('cx',(0,0)),lambda:Gate('h',(-1,)),
    lambda:Gate('ry',(0,),float('nan')),lambda:Gate('h',(0,),1),
    lambda:Circuit(0,()),lambda:Circuit(2,(Gate('h',(2,)),)),lambda:Circuit(2,[]),
    lambda:make_workload('bad'),lambda:make_workload('ghz',17),lambda:make_workload('ghz',2,0),
    lambda:make_workload('ghz',True),lambda:Circuit(2,()).compose(Circuit(3,())),
])
def test_invalid_circuits_and_parameters(factory):
    with pytest.raises(ValueError): factory()
