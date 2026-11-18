"""Independent acceptance rules for all 24 frozen first-wave instances."""
import math
import numpy as np
from .models import ContractError, ResultRecord, Verdict, finite, integer, keys, require
from .semantics import equivalent, operation, propagate, qasm3_distribution, parse_qasm2, real_array


def close(actual, expected, atol, rtol=0):
    expected = np.asarray(expected, dtype=float)
    actual = real_array(actual, expected.shape)
    error = abs(actual - expected)
    require(np.all(error <= atol + rtol * abs(expected)), 'Numeric tolerance exceeded')
    return float(np.max(error)) if error.size else 0.


def numeric(payload, fixture, reference, case, block):
    kind = case['kind']; a = case['acceptance']; metrics = {}
    if kind == 'parameter':
        keys(payload, ('binding_ids', 'observable_order', 'outputs'))
        require(isinstance(payload['binding_ids'], list), 'Binding IDs must be a list')
        for binding in payload['binding_ids']:integer(binding)
        require(payload['binding_ids'] == list(range(len(fixture['bindings']))), 'Binding identity/order mismatch')
        require(payload['observable_order'] == fixture['observable_order'], 'Observable identity/order mismatch')
        require(isinstance(payload['outputs'], list) and len(payload['outputs']) == len(reference['outputs']), 'Missing binding output')
        errors = []
        for actual, expected in zip(payload['outputs'], reference['outputs']):
            keys(actual, expected.keys())
            errors.append(close([actual[k] for k in fixture['observable_order']], [expected[k] for k in fixture['observable_order']], a['atol'], a['rtol']))
        metrics['max_abs_error'] = max(errors)
    elif kind == 'observable':
        keys(payload, ('expectations', 'weighted_sum'))
        metrics['max_abs_error'] = close(payload['expectations'], reference['expectations'], a['atol'], a['rtol'])
        close(payload['weighted_sum'], reference['weighted_sum'], a['atol'], a['rtol'])
        close(payload['weighted_sum'], float(np.dot(fixture['coefficients'], payload['expectations'])), a['atol'], a['rtol'])
    elif kind == 'gradient':
        keys(payload, ('outputs', 'jacobian', 'derivative'))
        keys(payload['derivative'], ('method', 'quantum_evaluations', 'components'))
        require(isinstance(payload['derivative']['method'], str) and payload['derivative']['method'].strip(), 'Missing derivative method')
        integer(payload['derivative']['quantum_evaluations'], 1)
        require(isinstance(payload['derivative']['components'], list) and all(isinstance(x, str) and x for x in payload['derivative']['components']), 'Malformed derivative attribution')
        metrics['output_max_abs_error'] = close(payload['outputs'], reference['outputs'], a['output_atol'], a['output_rtol'])
        metrics['jacobian_max_abs_error'] = close(payload['jacobian'], reference['jacobian'], a['jacobian_atol'], a['jacobian_rtol'])
    elif kind == 'dynamics':
        keys(payload, ('moments',))
        metrics['digital_max_abs_error'] = close(payload['moments'], reference['digital_ideal'], a['digital_ideal_atol'], a['digital_ideal_rtol'])
        metrics['physics_max_abs_error'] = close(payload['moments'], reference['exact_physics'], a['physics_max_abs_observable_error'])
    return metrics


def sampling(payload, fixture, reference, case, block):
    keys(payload, ('contexts',)); a = case['acceptance']
    expected = reference.get('contexts', [{'probabilities': reference.get('probabilities')}])
    require(isinstance(payload['contexts'], list) and len(payload['contexts']) == len(expected), 'Missing or extra sampling context')
    uppers = []; tvs = []
    for index, (context, target) in enumerate(zip(payload['contexts'], expected)):
        fields = ('context_id', 'counts', 'records') if case['kind'] == 'sampling' else ('context_id', 'counts')
        keys(context, fields)
        integer(context['context_id']); require(context['context_id'] == index, 'Context identity/order mismatch')
        probabilities = np.asarray(target['probabilities'], dtype=float); counts = context['counts']
        require(isinstance(counts, list) and len(counts) == len(probabilities), 'Missing count categories')
        for count in counts:integer(count)
        shots = a.get('shots_per_block', a.get('shots_per_context_per_block'))
        require(sum(counts) == shots, 'Incorrect shot total')
        require(np.isfinite(probabilities).all() and min(probabilities) >= 0 and abs(sum(probabilities) - 1) <= 1e-12, 'Invalid reference probability law')
        if case['kind'] == 'sampling':
            reconstructed = [0] * len(counts); seen = set()
            require(isinstance(context['records'], list), 'Missing register records')
            for row in context['records']:
                keys(row, ('register_a', 'register_b', 'count'))
                for v in row.values():integer(v)
                pair = (row['register_a'], row['register_b']); require(pair not in seen, 'Duplicate joint record'); seen.add(pair)
                output = 0
                for register, qubits in fixture['record_mapping'].items():
                    value = row[register]; require(value < 1 << len(qubits), 'Register value outside declared width')
                    for bit, q in enumerate(qubits):output |= ((value >> bit) & 1) << q
                reconstructed[output] += row['count']
            require(reconstructed == counts, 'Register/logical mapping mismatch')
        tv = float(.5 * np.sum(abs(np.asarray(counts) / shots - probabilities)))
        radius = math.sqrt((len(counts) * math.log(2) + math.log(a['workflow_total_decisions'] / a['workflow_family_error_probability'])) / (2 * shots))
        upper = tv + radius + 1e-10; tvs.append(tv); uppers.append(upper)
    require(max(uppers) <= a['total_variation_margin'], 'Distribution equivalence not established')
    return {'max_empirical_tv': max(tvs), 'max_upper_tv': max(uppers), 'contexts_checked': len(uppers)}


def training(payload, fixture, reference, case, block):
    keys(payload, ('seed', 'trace', 'gradients')); a = case['acceptance']; target = reference['runs'][block % 5]
    integer(payload['seed']); require(payload['seed'] == target['seed'], 'Wrong training initialization')
    require(isinstance(payload['trace'], list) and len(payload['trace']) == 49, 'Missing training checkpoints')
    require(isinstance(payload['gradients'], list) and len(payload['gradients']) == 48, 'Missing gradient audits')
    n = fixture['n_qubits']; batch = fixture['batch_size']; x = np.asarray(fixture['train_x']); y = np.asarray(fixture['train_y'])
    for step, (row, gold) in enumerate(zip(payload['trace'], target['trace'])):
        required = ('step', 'theta', 'weights', 'bias', 'train_loss') + (('test_loss',) if step in (0, 48) else ())
        keys(row, required, ('test_loss',)); integer(row['step']); require(row['step'] == step, 'Wrong checkpoint identity')
        for field in ('theta', 'weights', 'bias'):close(row[field], gold[field], a['parameter_atol'], a['parameter_rtol'])
        close(row['train_loss'], gold['train_loss'], a['loss_atol'], a['loss_rtol'])
        if 'test_loss' in row:close(row['test_loss'], gold['test_loss'], a['loss_atol'], a['loss_rtol'])
        theta = real_array(row['theta'], (n,)); weights = real_array(row['weights'], (n,)); bias = finite(row['bias'])
        prediction = np.cos(x + theta) @ weights / math.sqrt(n) + bias
        close(row['train_loss'], float(np.mean((prediction - y)**2)), a['loss_atol'], a['loss_rtol'])
        if step == 48:continue
        begin = (step % (len(x) // batch)) * batch; xb = x[begin:begin + batch]; error = prediction[begin:begin + batch] - y[begin:begin + batch]
        gradients = {'theta': np.mean(-2 * error[:, None] * np.sin(xb + theta) * weights / math.sqrt(n), axis=0),
                     'weights': np.mean(2 * error[:, None] * np.cos(xb + theta) / math.sqrt(n), axis=0),
                     'bias': float(np.mean(2 * error))}
        observed = payload['gradients'][step]; keys(observed, gradients.keys())
        for field, expected in gradients.items():
            close(observed[field], expected, a['gradient_atol'], a['gradient_rtol'])
            close(payload['trace'][step + 1][field], np.asarray(row[field]) - fixture['learning_rate'] * np.asarray(observed[field]), a['parameter_atol'], a['parameter_rtol'])
    require(payload['trace'][-1]['train_loss'] <= .95 * target['trace'][0]['train_loss'], 'Training progress target missed')
    return {'initial_train_loss': payload['trace'][0]['train_loss'], 'final_train_loss': payload['trace'][-1]['train_loss'], 'steps_checked': 48}


def routing(payload, fixture, reference, case, block):
    keys(payload, ('operations', 'final_layout', 'compile_wall_seconds'))
    a = case['acceptance']; n = fixture['n_qubits']; layout = payload['final_layout']
    require(isinstance(layout, list) and len(layout) == n, 'Missing final layout')
    for q in layout:integer(q)
    require(sorted(layout) == list(range(n)), 'Invalid final layout permutation')
    require(0 <= finite(payload['compile_wall_seconds']) <= a['per_compile_wall_limit_seconds'], 'Compile time exceeds cap')
    ops = payload['operations']; require(isinstance(ops, list) and len(ops) <= 20000, 'Invalid/oversized compiled artifact')
    edges = {frozenset(edge) for edge in fixture['target_edges']}; counters = [0] * n; interactions = 0
    for op in ops:
        name, qubits, _ = operation(op, n, target_edges=edges)
        if name == 'cz':
            depth = 1 + max(counters[q] for q in qubits)
            for q in qubits:counters[q] = depth
            interactions += 1
    order = np.array([sum(((logical >> q) & 1) << layout[q] for q in range(n)) for logical in range(1 << n)])
    if n == 6:
        initial = np.eye(1 << n, dtype=complex)
        target = propagate(n, fixture['operations'], initial)
        actual = propagate(n, ops, initial, target_edges=edges)[order]
        errors = [equivalent(actual, target, a['semantic_atol'], a['normalization_error_limit'])]
    else:
        errors = []
        for prep in fixture['probe_preparations']:
            initial = propagate(n, prep); target = propagate(n, fixture['operations'], initial)
            actual = propagate(n, ops, initial, target_edges=edges)[order]
            errors.append(equivalent(actual, target, a['semantic_atol'], a['normalization_error_limit']))
    return {'max_semantic_error': max(errors), 'full_cz_count': interactions, 'two_body_dependency_depth': max(counters),
            'verification': 'full-operator' if n == 6 else 'three-probes-only'}


def interchange(payload, fixture, reference, case, block):
    keys(payload, ('exported_source', 'reimported_source')); errors = []
    for source in payload.values():
        if case['id'] == 'ROUND-QASM2':
            ops, mapping = parse_qasm2(source)
            require(mapping == fixture['classical_bit_for_qubit'], 'Classical register permutation changed')
            initial = np.eye(16, dtype=complex)
            errors.append(equivalent(propagate(4, ops, initial), propagate(4, fixture['operations_before_measurement'], initial), case['acceptance']['numeric_atol']))
        else:
            probabilities, reset_zero = qasm3_distribution(source)
            errors.append(close(probabilities.tolist(), reference['probabilities'], case['acceptance']['numeric_atol']))
            close(reset_zero, reference['post_reset_q0_probability_zero'], case['acceptance']['numeric_atol'])
    return {'max_semantic_error': max(errors)}


def jobs(payload, fixture, reference, case, block):
    from .transport import expected_trace
    keys(payload, ('transport_trace', 'client_result'))
    require(payload['transport_trace'] == expected_trace(fixture), 'Missing, duplicate, reordered or hidden transport operations')
    result = payload['client_result']
    if case['id'] == 'JOB-LOST-ACK':
        keys(result, ('job_ids', 'state', 'submission_count', 'duplicate_jobs'))
        integer(result['submission_count']); integer(result['duplicate_jobs'])
        require(result == {'job_ids': reference['required_job_ids'], 'state': reference['required_terminal_state'],
                           'submission_count': 1, 'duplicate_jobs': 0}, 'Lost-ack reconciliation failed')
        return {'duplicate_jobs': 0, 'operational_study_status': 'completed'}
    keys(result, ('records', 'state', 'new_submissions'))
    integer(result['new_submissions']); require(result['new_submissions'] == 0, 'Unapproved submission')
    require(result['state'] == 'partial', 'Cancelled/partial work was erased')
    require(isinstance(result['records'], list) and len(result['records']) == 3, 'Missing/duplicate result records')
    by_id = {}
    for row in result['records']:
        keys(row, ('job_id', 'record', 'shots', 'state')); integer(row['shots'])
        require(isinstance(row['record'], str) and row['record'] not in by_id, 'Duplicate record identity')
        by_id[row['record']] = row
    gold = {record: {'job_id': job, 'record': record, 'shots': 0 if job == 'job-c' else 256,
                     'state': 'cancelled' if job == 'job-c' else 'completed'}
            for job, record in zip(fixture['submitted_job_ids'], fixture['planned_records'])}
    require(by_id == gold, 'Identity, status or shot accounting mismatch')
    return {'completed_shots': 512, 'cancelled_records': 1, 'operational_study_status': 'partial'}


EVALUATORS = {'parameter': numeric, 'observable': numeric, 'gradient': numeric, 'dynamics': numeric,
              'sampling': sampling, 'adaptive': sampling, 'training': training,
              'route': routing, 'roundtrip': interchange, 'job': jobs}


def evaluate(bundle, record, expected_identity=None):
    """Evaluate one measured repetition; no timing/SDK name influences thresholds."""
    try:
        if isinstance(record, dict):record = ResultRecord.from_dict(record)
        require(isinstance(record, ResultRecord), 'Expected a result record')
        bundle.verify_identity(record.identity)
        if expected_identity is not None:require(record.identity == expected_identity, 'Registered identity mismatch')
        if record.status != 'completed':return Verdict(record.status, (record.reason,))
        id_ = record.identity.instance_id; case = bundle.cases[id_]
        repetitions = 1 if case['kind'] in ('sampling', 'adaptive', 'training', 'job') else 3
        require(record.repetition < repetitions, 'Unexpected measured repetition')
        metrics = EVALUATORS[case['kind']](record.payload, bundle.fixtures[id_], bundle.references[id_], case, record.block)
        return Verdict('accepted', metrics=metrics)
    except (ContractError, KeyError, TypeError, ValueError, IndexError, OverflowError, RecursionError) as exc:
        return Verdict('incorrect', (str(exc),))


def evaluate_case(bundle, identity, records):
    """Require every block/repetition; partial evidence cannot become a case pass."""
    try:
        bundle.verify_identity(identity)
        kind = bundle.cases[identity.instance_id]['kind']; repetitions = 1 if kind in ('sampling', 'adaptive', 'training', 'job') else 3
        expected = {(b, r) for b in range(10) for r in range(repetitions)}; seen = set(); verdicts = []
        for item in records:
            record = ResultRecord.from_dict(item) if isinstance(item, dict) else item
            require(isinstance(record, ResultRecord), 'Expected a result record')
            require(record.identity == identity, 'Mixed stack/configuration/environment or task identity')
            key = (record.block, record.repetition); require(key not in seen and key in expected, 'Duplicate/unexpected repetition')
            seen.add(key); verdicts.append(evaluate(bundle, record, identity))
        bad = [v for v in verdicts if v.status != 'accepted']
        if bad:return Verdict(bad[0].status, tuple(reason for v in bad for reason in v.reasons), {'records': len(seen), 'required': len(expected)})
        if seen != expected:return Verdict('not-measured', ('Incomplete block/repetition coverage',), {'records': len(seen), 'required': len(expected)})
        return Verdict('accepted', metrics={'records': len(seen), 'required': len(expected)})
    except (ContractError, TypeError, ValueError, KeyError) as exc:return Verdict('incorrect', (str(exc),))


def evaluate_workflow(bundle, workflow_id, records):
    """Require every workflow case; statistical allocations are never recycled."""
    try:
        workflows = {w['id']: w for w in bundle.plan['workflows']}
        require(workflow_id in workflows, 'Unknown workflow')
        required = set(workflows[workflow_id]['instances']); groups = {}; fingerprint = None
        for item in records:
            record = ResultRecord.from_dict(item) if isinstance(item, dict) else item
            require(isinstance(record, ResultRecord), 'Expected a result record')
            id_ = record.identity.instance_id; require(id_ in required, 'Unexpected workflow instance')
            current = (record.identity.stack_id, record.identity.configuration_sha256,
                       record.identity.environment_sha256, record.identity.protocol_revision, record.identity.bundle_sha256)
            if fingerprint is None:fingerprint = current
            require(current == fingerprint, 'Mixed workflow registrations')
            groups.setdefault(id_, []).append(record)
        verdicts = {id_: evaluate_case(bundle, rows[0].identity, rows) for id_, rows in groups.items()}
        bad = [v for v in verdicts.values() if v.status != 'accepted']
        metrics = {'cases': {k: v.status for k, v in verdicts.items()}, 'missing_cases': sorted(required - groups.keys())}
        if bad:return Verdict(bad[0].status, tuple(reason for v in bad for reason in v.reasons), metrics)
        if set(groups) != required:return Verdict('not-measured', ('Incomplete workflow case coverage',), metrics)
        return Verdict('accepted', metrics=metrics)
    except (ContractError, TypeError, ValueError, KeyError, AttributeError) as exc:return Verdict('incorrect', (str(exc),))
