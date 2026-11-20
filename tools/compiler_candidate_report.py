"""Summarize independently replayed candidate evidence without ranking SDKs."""
import argparse
from collections import Counter
from pathlib import Path
from statistics import median, quantiles

from sdkbench.candidates.replay import replay
from sdkbench.p0 import Bundle, Registration, ResultRecord, evaluate
from sdkbench.p0.models import canonical_bytes, read_json


def spread(values):
    if not values:
        return None
    q1, _, q3 = quantiles(values, n=4, method='inclusive') if len(values) > 1 else values * 3
    return {'count': len(values), 'minimum': min(values), 'median': median(values),
            'maximum': max(values), 'q1': q1, 'q3': q3, 'interquartile_range': q3 - q1}


def summarize(directory, bundle):
    root = Path(directory)
    verified = replay(root, bundle)
    registrations = {name: Registration(**raw) for name, raw in
                     read_json(root / 'registrations.json').items()}
    rows = []
    for case in verified['cases']:
        name, instance = case['sdk'], case['instance']
        registration = registrations[name]
        identity = registration.identity(bundle, instance)
        statuses = Counter()
        metrics = []
        baseline_counts, rewrite_counts, optimization_evidence = [], [], []
        block_times, memory, blocks = [], [], []
        for path in sorted((root / name / instance).glob('*/evidence.json')):
            evidence = read_json(path)
            times = []
            for raw in evidence['records']:
                record = ResultRecord.from_dict(raw)
                verdict = evaluate(bundle, record, identity)
                statuses[verdict.status] += 1
                if verdict.status == 'accepted':
                    metrics.append(verdict.metrics)
                    times.append(record.payload['compile_wall_seconds'])
                    if 'native_baseline_cz_count' in record.measurements:
                        baseline_counts.append(record.measurements['native_baseline_cz_count'])
                    if 'accepted_block_rewrites' in record.measurements:
                        rewrite_counts.append(record.measurements['accepted_block_rewrites'])
                    if 'native_block_optimization_evidence_available' in record.measurements:
                        optimization_evidence.append(record.measurements['native_block_optimization_evidence_available'])
            # A failed warmup or case-budget overrun must not contribute a
            # timing block even when all three measured payloads are correct.
            eligible = len(times) == 3 and evidence['block_verdict']['status'] == 'accepted'
            if eligible:
                block_times.append(median(times))
            execution = evidence.get('execution')
            peak = execution.get('kernel_memory_peak_bytes') if execution else None
            if peak is not None:
                memory.append(peak)
            blocks.append({'block': len(blocks), 'status': evidence['block_verdict']['status'],
                           'accepted_records': len(times), 'timing_eligible': eligible,
                           'compile_wall_seconds': times, 'kernel_memory_peak_bytes': peak})
        rows.append({**case, 'workflow': registration.configuration['options']['workflow'],
                     'measured_record_statuses': dict(statuses),
                     'expected_records': 30, 'accepted_records': statuses['accepted'],
                     'full_cz_count_for_accepted_records': spread([m['full_cz_count'] for m in metrics]),
                     'dependency_depth_for_accepted_records': spread([m['two_body_dependency_depth'] for m in metrics]),
                     'maximum_semantic_error': max((m['max_semantic_error'] for m in metrics), default=None),
                     'verification': sorted({m['verification'] for m in metrics}),
                     'complete_block_compile_medians_seconds': spread(block_times),
                     'kernel_block_memory_peak_bytes': spread(memory), 'blocks': blocks})
        rows[-1]['sdk_reported_native_baseline_cz_count'] = spread(baseline_counts)
        rows[-1]['sdk_reported_accepted_block_rewrites'] = spread(rewrite_counts)
        rows[-1]['sdk_reported_native_block_optimization_evidence_available'] = spread(optimization_evidence)
    return {'schema_version': 1, 'bundle_sha256': bundle.sha256,
            'scope': 'Observed engineering campaign; conditional metrics do not erase failures',
            'publication_eligible': False, 'independent_replay': verified, 'cases': rows,
            'registrations': {name: reg.to_dict() for name, reg in registrations.items()},
            'metric_notes': [
                'Counts and dependency depth are recomputed by the independent evaluator.',
                'Timing uses the median of three accepted measurements within each accepted block.',
                'Quartiles use inclusive linear interpolation across observed values.',
                'Incomplete or warmup-failed blocks contribute no timing median; all records remain counted.',
                'Memory includes the whole supervised block: imports, warmups, measurements and export.',
                'Accepted-record statistics in a failed case are conditional diagnostics, not case success.',
                'Six-qubit semantics use the full operator; larger frozen cases use only three probes.',
                'Restored-layout and free-final-layout workflows are different end-to-end contracts.',
                'No optimality, global ranking or qualified publication-host claim is made.',
            ]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--directory', type=Path, required=True)
    parser.add_argument('--bundle', type=Path, default=Path('docs/implementation'))
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = summarize(args.directory, Bundle(args.bundle))
    with args.output.open('xb') as output:
        output.write(canonical_bytes(result))
    print(f"Summarized {len(result['cases'])} complete case records; publication_eligible=false")


if __name__ == '__main__':
    main()
