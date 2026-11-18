"""Synthetic qualification evidence, never an SDK adapter or performance result."""
from copy import deepcopy
from collections import deque
import math
import numpy as np
from sdkbench.p0.models import ResultRecord
from sdkbench.p0.transport import expected_trace


def counts_for(probabilities, shots=65536):
    real = np.asarray(probabilities) * shots; counts = np.floor(real).astype(int)
    for i in np.argsort(-(real - counts))[:shots - sum(counts)]:counts[i] += 1
    return counts.tolist()


def legal_route(fixture):
    adjacency = {q: [] for q in range(fixture['n_qubits'])}
    for a, b in fixture['target_edges']:adjacency[a].append(b); adjacency[b].append(a)
    out = []
    def cx(a, b):out.extend([{'name': 'h', 'qubits': [b]}, {'name': 'cz', 'qubits': [a, b]}, {'name': 'h', 'qubits': [b]}])
    def swap(a, b):cx(a, b); cx(b, a); cx(a, b)
    for op in fixture['operations']:
        if op['name'] != 'cx':out.append(deepcopy(op)); continue
        a, b = op['qubits']; queue = deque([[a]])
        while queue:
            path = queue.popleft()
            if path[-1] == b:break
            queue.extend(path + [q] for q in adjacency[path[-1]] if q not in path)
        moves = list(zip(path[:-2], path[1:-1]))
        for edge in moves:swap(*edge)
        cx(path[-2], b)
        for edge in reversed(moves):swap(*edge)
    return out


def positive_payload(bundle, instance, block=0):
    case = bundle.cases[instance]; f = bundle.fixtures[instance]; r = bundle.references[instance]; kind = case['kind']
    if kind == 'parameter':return {'binding_ids': list(range(7)), 'observable_order': f['observable_order'], 'outputs': deepcopy(r['outputs'])}
    if kind == 'observable':return {k: deepcopy(r[k]) for k in ('expectations', 'weighted_sum')}
    if kind == 'gradient':return {'outputs': r['outputs'], 'jacobian': deepcopy(r['jacobian']), 'derivative': {'method': 'qualification-oracle', 'quantum_evaluations': 1, 'components': ['synthetic-test-only']}}
    if kind == 'dynamics':return {'moments': deepcopy(r['digital_ideal'])}
    if kind in ('sampling', 'adaptive'):
        laws = [c['probabilities'] for c in r['contexts']] if 'contexts' in r else [r['probabilities']]
        contexts = []
        for i, probabilities in enumerate(laws):
            counts = counts_for(probabilities); context = {'context_id': i, 'counts': counts}
            if kind == 'sampling':
                records = []
                for output, count in enumerate(counts):
                    row = {'count': count}
                    for name, qubits in f['record_mapping'].items():row[name] = sum(((output >> q) & 1) << k for k, q in enumerate(qubits))
                    records.append(row)
                context['records'] = records
            contexts.append(context)
        return {'contexts': contexts}
    if kind == 'training':
        run = r['runs'][block % 5]; trace = deepcopy(run['trace']); gradients = []; n = f['n_qubits']; batch = f['batch_size']; x = np.array(f['train_x']); y = np.array(f['train_y'])
        for step, row in enumerate(trace[:-1]):
            start = step % 4 * batch; xb = x[start:start + batch]; target = y[start:start + batch]
            theta = np.array(row['theta']); w = np.array(row['weights']); error = np.cos(xb + theta) @ w / math.sqrt(n) + row['bias'] - target
            gradients.append({'theta': np.mean(2 * error[:, None] * -np.sin(xb + theta) * w / math.sqrt(n), axis=0).tolist(),
                              'weights': np.mean(2 * error[:, None] * np.cos(xb + theta) / math.sqrt(n), axis=0).tolist(), 'bias': float(np.mean(2 * error))})
        return {'seed': run['seed'], 'trace': trace, 'gradients': gradients}
    if kind == 'route':return {'operations': legal_route(f), 'final_layout': list(range(f['n_qubits'])), 'compile_wall_seconds': .001}
    if kind == 'roundtrip':return {'exported_source': f['source'], 'reimported_source': f['source']}
    if instance == 'JOB-LOST-ACK':
        result = {'job_ids': ['job-001'], 'state': 'completed', 'submission_count': 1, 'duplicate_jobs': 0}
    else:
        result = {'state': 'partial', 'new_submissions': 0,
                  'records': [{'job_id': job, 'record': record, 'shots': 0 if job == 'job-c' else 256, 'state': 'cancelled' if job == 'job-c' else 'completed'} for job, record in zip(f['submitted_job_ids'], f['planned_records'])]}
    return {'transport_trace': expected_trace(f), 'client_result': result}


def record(bundle, instance, block=0, repetition=0, stack_id='synthetic-qualification'):
    identity = bundle.identity(instance, stack_id, '1' * 64, '2' * 64)
    return ResultRecord(identity, block, repetition, 'completed', positive_payload(bundle, instance, block), measurements={'outcome_wall_seconds': 1e-6})
