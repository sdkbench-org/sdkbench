"""SDK-independent first-wave reference construction. No participant imports or cloud calls.

Logical q0 is index bit 0. Rx/Ry/Rz use exp(-i angle Pauli/2).
The primary state oracle applies 2x2 blocks; a separate small dense Kronecker
oracle and analytic anchors check conventions. These are fixture references,
not participant benchmark implementations or a general SDK.
"""
import hashlib
import math
import numpy as np


def u01(seed, label, index):
    raw = hashlib.sha256(f'{seed}:{label}:{index}'.encode('ascii')).digest()
    return (int.from_bytes(raw[:8], 'big') >> 11) / 2**53


def angles(seed, label, count, scale=math.pi):
    return [scale*(2*u01(seed, label, i)-1) for i in range(count)]


def gate(name, *qubits, angle=None, parameter=None):
    op = {'name':name, 'qubits':list(qubits)}
    if angle is not None: op['angle'] = float(angle)
    if parameter is not None: op['parameter'] = parameter
    return op


def matrix(name, angle=0., derivative=False):
    c,s = math.cos(angle/2),math.sin(angle/2)
    if name == 'h': return np.array([[1,1],[1,-1]],dtype=complex)/math.sqrt(2)
    if name == 'x': return np.array([[0,1],[1,0]],dtype=complex)
    if name == 'rx':
        return np.array([[-s,-1j*c],[-1j*c,-s]],dtype=complex)/2 if derivative else np.array([[c,-1j*s],[-1j*s,c]])
    if name == 'ry':
        return np.array([[-s,-c],[c,-s]],dtype=complex)/2 if derivative else np.array([[c,-s],[s,c]],dtype=complex)
    if name == 'rz':
        m = np.diag([np.exp(-.5j*angle),np.exp(.5j*angle)])
        return np.diag([-.5j,.5j])@m if derivative else m
    raise ValueError(name)


def apply(state, op, params=None, derivative=False):
    name=op['name']; q=op['qubits']; a=op.get('angle',0.)
    if 'parameter' in op: a=params[op['parameter']]
    index=np.arange(len(state),dtype=np.int64)
    out=state.copy()
    if name in ('cx','cz','rzz'):
        if derivative: raise ValueError('Only rotation gates have reference derivatives')
        if name=='cx':
            low=index[(((index>>q[0])&1)==1)&(((index>>q[1])&1)==0)];high=low|(1<<q[1])
            out[low],out[high]=state[high],state[low]
        elif name=='cz': out[(((index>>q[0])&1)&((index>>q[1])&1)).astype(bool)] *= -1
        else:
            parity=((index>>q[0])^(index>>q[1]))&1
            out *= np.exp(-.5j*a*(1-2*parity))
        return out
    low=index[((index>>q[0])&1)==0];high=low|(1<<q[0]);m=matrix(name,a,derivative)
    out[low]=m[0,0]*state[low]+m[0,1]*state[high]
    out[high]=m[1,0]*state[low]+m[1,1]*state[high]
    return out


def statevector(n, ops, params=None, initial=None):
    state=np.zeros(1<<n,dtype=np.complex128) if initial is None else np.array(initial,dtype=np.complex128,copy=True)
    if initial is None:state[0]=1
    for op in ops: state=apply(state,op,params)
    return state


def pauli_action(state, word):
    # word[j] is the operator on logical qj, independent of string significance.
    index=np.arange(len(state),dtype=np.int64);dest=index.copy();phase=np.ones(len(state),dtype=complex)
    for q,op in enumerate(word):
        bit=(index>>q)&1
        if op in 'XY':dest ^= 1<<q
        if op=='Z':phase *= 1-2*bit
        if op=='Y':phase *= 1j*(1-2*bit)
    out=np.empty_like(state);out[dest]=phase*state
    return out


def expectations(state, words):
    return [float(np.vdot(state,pauli_action(state,w)).real) for w in words]


def variational_program(n):
    ops=[gate('h',0),gate('x',n-1)]
    for layer in range(3):
        for q in range(n):
            ops.extend([gate('ry',q,parameter=layer*n+q),gate('rz',q,parameter=layer*n+(q+1)%n)])
        ops.extend(gate('cx',q,q+1) for q in range(layer%2,n-1,2))
    return ops


def derivative_reference(n,ops,params,words):
    state=np.zeros(1<<n,dtype=complex);state[0]=1
    tangent=np.zeros((len(params),1<<n),dtype=complex)
    for op in ops:
        before=state;state=apply(before,op,params)
        tangent=np.stack([apply(v,op,params) for v in tangent])
        if 'parameter' in op:tangent[op['parameter']]+=apply(before,op,params,derivative=True)
    jac=np.array([[2*np.vdot(pauli_action(state,w),t).real for t in tangent] for w in words])
    return expectations(state,words),jac


def parameter_fixture(n):
    ops=[gate('ry',q,parameter=q) for q in range(n)]+[gate('rz',q,parameter=n+q) for q in range(n)]
    edges=[[q,q+1] for q in range(n-1)];ops += [gate('cz',*e) for e in edges]
    bindings=[[0.]*(2*n)]+[angles(1701,f'bind-{n}-{b}',2*n,1.3) for b in range(1,7)]
    outputs=[]
    for p in bindings:
        row={}
        for q in range(n):
            factor=math.prod(math.cos(p[j]) for j in [q-1,q+1] if 0<=j<n)
            row[f'Z{q}']=math.cos(p[q]);row[f'X{q}']=math.sin(p[q])*math.cos(p[n+q])*factor
            row[f'Y{q}']=math.sin(p[q])*math.sin(p[n+q])*factor
        for a,b in edges:row[f'Z{a}Z{b}']=math.cos(p[a])*math.cos(p[b])
        outputs.append(row)
    return {'n_qubits':n,'operations':ops,'bindings':bindings,'observable_order':list(outputs[0])}, {'method':'analytic graph-state local moments','outputs':outputs}


def observable_fixture(n):
    ops=variational_program(n);params=angles(1901,f'observables-{n}',3*n)
    words=['Z'+'I'*(n-1),'X'*n,'Z'*(n-1)+'X']
    for i in range(61):
        word=''.join('IXYZ'[int(4*u01(1901,f'pauli-{n}-{i}',q))] for q in range(n))
        words.append(word)
    coefficients=angles(1901,f'coeff-{n}',len(words),.25)
    state=statevector(n,ops,params);values=expectations(state,words)
    return {'n_qubits':n,'operations':ops,'parameters':params,'pauli_words':words,'coefficients':coefficients}, {'method':'independent block state propagation and Pauli permutation sums','expectations':values,'weighted_sum':float(np.dot(coefficients,values))}


def gradient_fixture(n):
    ops=variational_program(n);params=angles(2201,f'gradient-{n}',3*n,.9)
    params[0]=0.;params[1]=1e-7
    words=['Z'+'I'*(n-1),'X'*n,'Z'+'I'*(n-2)+'Z']
    values,jac=derivative_reference(n,ops,params,words)
    return {'n_qubits':n,'operations':ops,'parameters':params,'pauli_words':words,'shared_occurrences_per_parameter':2}, {'method':'analytic gate derivatives with tangent propagation; five-point independent finite-difference check','outputs':values,'jacobian':jac.tolist()}


def training_fixture(n,batch):
    # Deliberately structured analytic hybrid regression; no application advantage claim.
    m=4*batch;test=2*batch
    x=np.array([angles(2301,f'train-x-{n}-{i}',n,1.1) for i in range(m)])
    xt=np.array([angles(2301,f'test-x-{n}-{i}',n,1.1) for i in range(test)])
    teacher_theta=np.array(angles(2301,f'teacher-theta-{n}',n,.7))
    teacher_w=np.array(angles(2301,f'teacher-w-{n}',n,.8));teacher_b=.17
    y=np.cos(x+teacher_theta)@teacher_w/math.sqrt(n)+teacher_b
    yt=np.cos(xt+teacher_theta)@teacher_w/math.sqrt(n)+teacher_b
    runs=[];starts=[]
    for seed in [11,23,37,51,73]:
        theta=np.array(angles(seed,f'init-theta-{n}',n,.2));w=np.array(angles(seed,f'init-w-{n}',n,.2));b=0.
        starts.append({'seed':seed,'theta':theta.tolist(),'weights':w.tolist(),'bias':b})
        trace=[]
        def loss(a,target):return float(np.mean((np.cos(a+theta)@w/math.sqrt(n)+b-target)**2))
        initial=loss(x,y)
        for step in range(49):
            trace.append({'step':step,'train_loss':loss(x,y),'test_loss':loss(xt,yt),'theta':theta.tolist(),'weights':w.tolist(),'bias':b})
            if step==48:break
            begin=(step%(m//batch))*batch;xb=x[begin:begin+batch];yb=y[begin:begin+batch]
            z=np.cos(xb+theta);error=z@w/math.sqrt(n)+b-yb
            dtheta=np.mean(2*error[:,None]*(-np.sin(xb+theta))*w/math.sqrt(n),axis=0)
            dw=np.mean(2*error[:,None]*z/math.sqrt(n),axis=0);db=float(np.mean(2*error))
            theta-=.03*dtheta;w-=.03*dw;b-=.03*db
        assert trace[-1]['train_loss']<=.95*initial
        runs.append({'seed':seed,'trace':trace,'progress_target':.95*initial})
    return {'n_qubits':n,'batch_size':batch,'train_x':x.tolist(),'train_y':y.tolist(),'test_x':xt.tolist(),'test_y':yt.tolist(),'initializations':starts,'steps':48,'learning_rate':.03,'model':'z_j=cos(x_j+theta_j) from Ry(x_j) then Ry(theta_j); prediction=sum_j(w_j*z_j)/sqrt(n)+b; mean squared error; plain SGD, all parameters trainable'}, {'method':'closed-form moments and chain-rule SGD, not quantum SDK/autograd output','runs':runs}


def route_fixture(n,topology):
    if topology=='grid-2x4':edges=[[r*4+c,r*4+c+1] for r in range(2) for c in range(3)]+[[c,c+4] for c in range(4)]
    else:edges=[[q,q+1] for q in range(n-1)]
    ops=[gate('ry',q,angle=angles(2401,f'route-in-{n}',n)[q]) for q in range(n)]
    for i in range(4*n):
        a=(5*i+1)%n;b=(a+1+(i%(n-1)))%n
        ops += [gate('cx',a,b),gate('rz',b,angle=angles(2401,f'route-angle-{n}',4*n)[i])]
    probes=[];digests=[]
    for p in range(3):
        initial_ops=[]
        for q in range(n):initial_ops += [gate('ry',q,angle=angles(2401,f'probe-a-{n}-{p}',n)[q]),gate('rz',q,angle=angles(2401,f'probe-b-{n}-{p}',n)[q])]
        state=statevector(n,ops,initial=statevector(n,initial_ops));probes.append(initial_ops)
        representation=[[round(float(v.real),11),round(float(v.imag),11)] for v in state]
        digests.append(hashlib.sha256(json_bytes(representation)).hexdigest())
    return {'n_qubits':n,'operations':ops,'target_edges':edges,'target_basis':'arbitrary one-qubit unitaries and full CZ only','ancillas_allowed':0,'initial_layout':'identity','final_layout':'permitted only with explicit logical reconstruction','probe_preparations':probes,'verification':'full small operator at n=6; three full-output probe states at n=8,12'}, {'method':'independent full-state propagation; dense small-operator audit','probe_state_audit_sha256':digests,'digest_role':'artifact audit only, never a floating-point acceptance test'}


def dynamics_fixture(n,steps):
    size=1<<n;h=np.zeros((size,size),dtype=float);index=np.arange(size)
    for q in range(n):h[index^(1<<q),index]-=.7
    for q in range(n-1):h[index,index]-=1-2*(((index>>q)^(index>>(q+1)))&1)
    eigen,vectors=np.linalg.eigh(h);initial_index=sum(1<<q for q in range(n) if q%2)
    initial=np.zeros(size,dtype=complex);initial[initial_index]=1
    exact=vectors@(np.exp(-.7j*eigen)*(vectors.T@initial))
    dt=.7/steps;ops=[]
    for _ in range(steps):
        ops += [gate('rzz',q,q+1,angle=-dt) for q in range(n-1)]
        ops += [gate('rx',q,angle=-1.4*dt) for q in range(n)]
        ops += [gate('rzz',q,q+1,angle=-dt) for q in range(n-1)]
    digital=statevector(n,ops,initial=initial)
    words=[]
    for q in range(n):words += ['I'*q+'Z'+'I'*(n-q-1),'I'*q+'X'+'I'*(n-q-1)]
    for q in range(n-1):words.append('I'*q+'ZZ'+'I'*(n-q-2))
    a=expectations(exact,words);b=expectations(digital,words)
    assert max(abs(x-y) for x,y in zip(a,b))<.002
    return {'n_qubits':n,'time':.7,'steps':steps,'initial_basis_index':initial_index,'hamiltonian':'-sum_{q=0}^{n-2} Zq Z(q+1) - 0.7 sum_q Xq; open boundary; hbar=1; J=1','operations':ops,'pauli_words':words}, {'method':'independent dense spectral evolution; separate digital product-formula oracle','exact_physics':a,'digital_ideal':b,'product_formula_error':max(abs(x-y) for x,y in zip(a,b))}


def sampling_fixture(n):
    rotation=[.31,.83,1.19,.57,.97][:n]
    ops=[gate('ry',q,angle=a) for q,a in enumerate(rotation)]+[gate('cx',0,n-1)]
    p=[]
    for output in range(1<<n):
        before=output^((1<<(n-1)) if output&1 else 0)
        p.append(math.prod((math.sin(rotation[q]/2)**2 if (before>>q)&1 else math.cos(rotation[q]/2)**2) for q in range(n)))
    return {'n_qubits':n,'operations':ops,'record_mapping':{'register_a':[n-1,0],'register_b':list(range(1,n-1))},'category_encoding':'all n logical bits; integer index=sum(bit(q)*2**q); register normalization is mandatory','shots_per_replicate':65536,'independent_blocks':10,'seed_rule':'roadmap.json execution_profile.stochastic_seed_rule'}, {'method':'analytic independent rotation probabilities with a deterministic CNOT permutation','probabilities':p}


def adaptive_fixture(kind):
    if kind=='teleport':
        states={'zero':[0.,0.,1.],'one':[0.,0.,-1.],'plus':[1.,0.,0.],'minus':[-1.,0.,0.],'plus-i':[0.,1.,0.],'minus-i':[0.,-1.,0.]}
        contexts=[]
        for name,bloch in states.items():
            for axis,value in zip('XYZ',bloch):
                probs=[.25*(1+((-1)**out)*value)/2 for m0 in range(2) for m1 in range(2) for out in range(2)]
                contexts.append({'input':name,'bob_basis':axis,'probabilities':probs})
        return {'n_qubits':3,'protocol':'input on q0; H(q1), CX(q1,q2), CX(q0,q1), H(q0); measure q0->m0,q1->m1; X(q2) iff m1; Z(q2) iff m0; measure q2 in requested X/Y/Z basis','inputs_bloch':states,'contexts':[{'input':c['input'],'bob_basis':c['bob_basis']} for c in contexts],'category_encoding':'index=4*m0+2*m1+bob_outcome; 8 categories, including zero-probability outcomes','shots_per_context_per_replicate':65536,'independent_blocks':10,'seed_rule':'roadmap.json execution_profile.stochastic_seed_rule'}, {'method':'teleportation identity and branch-wise analytic probabilities','contexts':contexts}
    p=[0.]*12
    for trial,success,probability in [(1,1,.5),(2,1,.25),(3,1,.125),(3,0,.125)]:p[(trial-1)*4+2*success]=probability
    return {'n_qubits':1,'protocol':'start |0>; for trial in 1..3: H, measure; stop on 1, else continue; retain trial count and success flag; after stopping reset qubit and terminal Z-measure; no postselection','category_encoding':'index=4*(trial-1)+2*success+terminal_Z; 12 categories, including impossible records','shots_per_context_per_replicate':65536,'independent_blocks':10,'seed_rule':'roadmap.json execution_profile.stochastic_seed_rule'}, {'method':'bounded geometric stopping law plus exact reset postcondition','probabilities':p}


def job_fixture(kind):
    if kind=='lost-ack':
        return {'transport':'offline deterministic provider stub; no network or credentials','plan_id':'job-plan-a','operations':[{'operation':'submit','request_key':'request-001','server':'accept job-001 and persist payload hash; lose client acknowledgment'},{'operation':'reconcile','request_key':'request-001','server':'return original job-001'},{'operation':'poll','job_id':'job-001','server':'completed; all planned records'}],'policy':'one authorized submission; zero additional submissions; unresolved is permitted until reconciliation, not a successful duplicate'}, {'method':'independent finite-state transition table','required_submission_count':1,'required_job_ids':['job-001'],'required_terminal_state':'completed','duplicate_jobs_allowed':0}
    return {'transport':'offline deterministic provider stub; no network or credentials','plan_id':'job-plan-b','submitted_job_ids':['job-a','job-b','job-c'],'planned_records':['circuit-a/binding-0','circuit-a/binding-1','circuit-b/binding-0'],'events':[{'job_id':'job-b','status':'partial','record':'circuit-a/binding-1','shots':256},{'job_id':'job-a','status':'completed','record':'circuit-a/binding-0','shots':256},{'job_id':'job-b','status':'completed','record':'circuit-a/binding-1','shots':256,'duplicate_page':True},{'job_id':'job-c','status':'cancelled','record':'circuit-b/binding-0','shots':0}],'policy':'deduplicate provider pages by stable identity; retain cancelled record; no automatic resubmission'}, {'method':'independent event-ledger reconciliation','unique_completed_records':2,'completed_shots':512,'cancelled_records':1,'new_submissions_allowed':0,'study_status':'partial, not accepted complete'}


def roundtrip_fixture(kind):
    if kind=='qasm2':
        source='OPENQASM 2.0;\ninclude "qelib1.inc";\nqreg q[4];\ncreg c[4];\nx q[3];\nry(0.37) q[0];\nrz(-0.81) q[0];\nh q[1];\ncx q[0],q[2];\ncz q[1],q[3];\nmeasure q[0] -> c[2];\nmeasure q[1] -> c[0];\nmeasure q[2] -> c[3];\nmeasure q[3] -> c[1];\n'
        ops=[gate('x',3),gate('ry',0,angle=.37),gate('rz',0,angle=-.81),gate('h',1),gate('cx',0,2),gate('cz',1,3)]
        state=statevector(4,ops)
        return {'format':'OpenQASM 2.0','source':source,'n_qubits':4,'operations_before_measurement':ops,'classical_bit_for_qubit':[2,0,3,1],'required_roundtrip':'source -> native -> exported program -> reimport; preserve declared behavior, register mapping and numeric angles'}, {'method':'independent matrix semantics and explicit bit permutation','logical_probabilities':(abs(state)**2).tolist(),'premeasurement_state':[[float(v.real),float(v.imag)] for v in state]}
    source='OPENQASM 3.0;\ninclude "stdgates.inc";\nqubit[2] q;\nbit[2] c;\nh q[0];\ncx q[0],q[1];\nc[1] = measure q[0];\nif (c[1]) { x q[1]; }\nreset q[0];\nc[0] = measure q[1];\n'
    return {'format':'OpenQASM 3.0 static plus measurement/reset/if subset','source':source,'n_qubits':2,'required_roundtrip':'preserve measured c[1], conditional X, reset and terminal c[0]; no postselection'}, {'method':'independent branch enumeration','classical_category_encoding':'index=2*c[1]+c[0]','probabilities':[.5,0.,.5,0.],'post_reset_q0_probability_zero':1.}


def dense_state(n,ops,params=None,initial=None):
    state=np.zeros(1<<n,dtype=complex) if initial is None else np.array(initial,copy=True)
    if initial is None:state[0]=1
    for op in ops:
        if len(op['qubits'])==1:
            value=params[op['parameter']] if 'parameter' in op else op.get('angle',0.)
            full=np.array([[1.]],dtype=complex)
            for q in reversed(range(n)):full=np.kron(full,matrix(op['name'],value) if q==op['qubits'][0] else np.eye(2))
        else:
            full=np.eye(1<<n,dtype=complex);a,b=op['qubits']
            if op['name']=='cx':
                full[:]=0
                for col in range(1<<n):full[col^((1<<b) if (col>>a)&1 else 0),col]=1
            elif op['name']=='cz':
                for col in range(1<<n):full[col,col]=-1 if (col>>a)&1 and (col>>b)&1 else 1
            else:
                angle=op['angle']
                for col in range(1<<n):full[col,col]=np.exp(-.5j*angle*((-1)**(((col>>a)^(col>>b))&1)))
        state=full@state
    return state


def json_bytes(value):
    import json
    return (json.dumps(value,sort_keys=True,indent=2,allow_nan=False)+'\n').encode('ascii')


def verify_anchors():
    from numpy.testing import assert_allclose
    assert_allclose(statevector(1,[gate('ry',0,angle=math.pi/2)]),[1/math.sqrt(2)]*2,atol=1e-14)
    assert_allclose(statevector(2,[gate('h',0),gate('cx',0,1)]),[1/math.sqrt(2),0,0,1/math.sqrt(2)],atol=1e-14)
    assert_allclose(expectations(np.array([1,1j])/math.sqrt(2),['Y']),[1.],atol=1e-14)
    for n in [3,4]:
        ops=variational_program(n);params=angles(33,'anchor',3*n)
        assert_allclose(statevector(n,ops,params),dense_state(n,ops,params),atol=1e-12)
        words=['X'*n,'Z'+'I'*(n-1)];_,jac=derivative_reference(n,ops,params,words)
        h=1e-4;numeric=[]
        for k in range(len(params)):
            samples=[]
            for delta in [-2*h,-h,h,2*h]:
                p=list(params);p[k]+=delta;samples.append(np.array(expectations(dense_state(n,ops,p),words)))
            numeric.append((samples[0]-8*samples[1]+8*samples[2]-samples[3])/(12*h))
        assert_allclose(jac,np.array(numeric).T,atol=2e-9,rtol=2e-8)
    fixture,reference=parameter_fixture(4)
    words=[]
    for name in reference['outputs'][0]:
        word=['I']*4
        import re
        for op,q in re.findall(r'([XYZ])(\d+)',name):word[int(q)]=op
        words.append(''.join(word))
    for p,row in zip(fixture['bindings'],reference['outputs']):
        assert_allclose(expectations(dense_state(4,fixture['operations'],p),words),list(row.values()),atol=1e-12)
    fixture,reference=sampling_fixture(3)
    assert_allclose(abs(dense_state(3,fixture['operations']))**2,reference['probabilities'],atol=1e-12)
    # Family-wide sampling confidence radius: union bound over all subsets + Hoeffding.
    for alphabet,decisions in [(32,20),(12,190),(8,190)]:
        radius=math.sqrt((alphabet*math.log(2)+math.log(decisions/.01))/(2*65536))
        assert 2*radius+1e-10<.04

    # Teleportation: enumerate projected branches using the dense construction.
    input_states = [np.array([1,0]),np.array([0,1]),np.array([1,1])/math.sqrt(2),np.array([1,-1])/math.sqrt(2),np.array([1,1j])/math.sqrt(2),np.array([1,-1j])/math.sqrt(2)]
    for inp in input_states:
        initial=np.zeros(8,dtype=complex);initial[:2]=inp
        state=dense_state(3,[gate('h',1),gate('cx',1,2),gate('cx',0,1),gate('h',0)],initial=initial)
        for m0 in range(2):
            for m1 in range(2):
                branch=np.array([state[m0+2*m1+4*b] for b in range(2)])
                if m1:branch=matrix('x')@branch
                if m0:branch=np.diag([1,-1])@branch
                assert_allclose(np.outer(branch,branch.conj()),.25*np.outer(inp,inp.conj()),atol=1e-12)
    # Every column of the smallest routing operator, not only its zero input.
    fixture,_=route_fixture(6,'line')
    for column in range(64):
        basis=np.eye(64,dtype=complex)[:,column]
        assert_allclose(statevector(6,fixture['operations'],initial=basis),dense_state(6,fixture['operations'],initial=basis),atol=1e-12)
    # Quantum feature and classical/quantum chain-rule derivatives are independent of autograd.
    x=np.array([.2,-.4]);theta=np.array([.1,.3]);w=np.array([.6,-.2]);target=.17;b=.02
    def loss(t,weights,bias):return (np.dot(weights,np.cos(x+t))/math.sqrt(2)+bias-target)**2
    error=np.dot(w,np.cos(x+theta))/math.sqrt(2)+b-target
    analytic=np.r_[2*error*(-np.sin(x+theta))*w/math.sqrt(2),2*error*np.cos(x+theta)/math.sqrt(2),2*error]
    p=np.r_[theta,w,b];numeric=[]
    for k in range(5):
        plus=p.copy();minus=p.copy();plus[k]+=1e-6;minus[k]-=1e-6
        numeric.append((loss(plus[:2],plus[2:4],plus[4])-loss(minus[:2],minus[2:4],minus[4]))/2e-6)
    assert_allclose(analytic,numeric,atol=1e-10)
    for q in range(2):
        z=expectations(dense_state(1,[gate('ry',0,angle=x[q]),gate('ry',0,angle=theta[q])]),['Z'])[0]
        assert_allclose(z,np.cos(x[q]+theta[q]),atol=1e-12)
