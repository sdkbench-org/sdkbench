#!/usr/bin/env python3
"""Verify hashes, native request bindings, routing semantics and complete diagnostic scope."""
import argparse
from collections import Counter
from dataclasses import asdict
import hashlib
import json
from pathlib import Path
import signal
from sdkbench.p0 import Bundle,Registration,ResultRecord,evaluate
from sdkbench.p0.evaluators import routing
from sdkbench.p0.models import canonical_bytes,digest,read_json,require
from p1a_evidence import archive


def micro_reference(fixture):
    """Check the reference-only native SWAP definition without importing any SDK."""
    operations=[]
    for op in fixture['native_input_operations']:
        if op['name']=='swap':
            a,b=op['qubits']
            operations.extend({'name':'cx','qubits':list(pair)} for pair in ((a,b),(b,a),(a,b)))
        else:operations.append(op)
    require(operations==fixture['operations'],'Native microprobe and reference input differ')


def verify(root,bundle):
    root=Path(root).resolve();manifest=read_json(root/'MANIFEST.json')
    files={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file() and p.name!='MANIFEST.json'}
    require(files==set(manifest['files']),'Missing or extra evidence files')
    for name,sha in manifest['files'].items():
        path=(root/name).resolve();require(path.is_relative_to(root),'Evidence path escapes root')
        require(hashlib.sha256(path.read_bytes()).hexdigest()==sha,'File hash mismatch: '+name)
    profile=read_json(root/'profile.json');context=read_json(root/'context.json');report=read_json(root/'report.json')
    registrations={k:Registration(**v) for k,v in read_json(root/'registrations.json').items()}
    admission=read_json(root/'admission.json');configs={v['id']:v for v in profile['variants']}
    require(set(registrations)==set(configs),'Incomplete registrations')
    require(profile['bundle_sha256']==bundle.sha256,'Frozen bundle mismatch')
    require(report['profile_sha256']==digest(profile) and report['implementation']==context['implementation'],'Report provenance mismatch')
    expected={(v['id'],i,s) for v in profile['variants'] for i in profile['frozen_instances'] for s in range(10 if v['seeded'] else 1)}
    expected|={(v,i,0) for v in profile['micro_variants'] for i in profile['micro_ids']}
    seen=set();outcomes=[];swaps=[]
    for path in sorted(root.glob('runs/*/*/*/evidence.json')):
        evidence=read_json(path);folder=path.parent;request=read_json(folder/'request.json')
        key=(evidence['variant'],evidence['input_id'],evidence['seed_index'])
        require(key in expected and key not in seen,'Unexpected/duplicate diagnostic outcome');seen.add(key)
        config=configs[key[0]];micro=key[1] in profile['micro_ids'];instance='ROUTE-LINE-06' if micro else key[1]
        case=bundle.cases[instance];fixture=request['fixture'];registration=registrations[key[0]]
        require(request['config']==config and request['input_id']==key[1] and request['block']==key[2] and request['micro']==micro,'Request scope mismatch')
        require(request['profile_sha256']==digest(profile) and request['fixture_sha256']==digest(fixture),'Request digest mismatch')
        require(request['seed']==bundle.plan['execution_profile']['compiler_seeds'][key[2]],'Compiler seed mismatch')
        options=registration.configuration['options']
        require(options['variant']==config and options['diagnostic_profile_sha256']==digest(profile) and options['implementation']==context['implementation'],'Registration configuration mismatch')
        if micro:
            micro_reference(fixture)
            require({k:v for k,v in fixture.items() if k not in ('operations','native_input_operations')}==
                    {k:v for k,v in bundle.fixtures[instance].items() if k!='operations'},'Microprobe changes non-operation constraints')
            require(request['identity'] is None,'Microprobe misrepresented as a frozen instance')
        else:
            require(fixture==bundle.fixtures[instance],'Frozen input modified')
            require(request['identity']==asdict(registration.identity(bundle,instance)),'Frozen identity binding mismatch')
        execution=evidence['execution'];response=evidence['response'];status=None;metrics={}
        if admission[key[0]]:status='install-failed'
        elif execution is None:status=evidence['verdict']['status'];require(status in ('timeout','access-blocked','error'),'Unexecuted success')
        else:
            limits=execution['limits']
            require(limits['memory_bytes']==16*1024**3 and 0<limits['wall_seconds']<=case['case_wall_limit_seconds'],'Resource cap differs from protocol')
            require(limits['cpu']==context['cpu'] and execution['enforced_cpu_set']==str(context['cpu']),'CPU assignment mismatch')
            require(execution['network_policy']=='seccomp-deny-sockets-and-io-uring','Missing network isolation')
            if execution['execution_status']!='completed':
                status='timeout' if execution.get('returncode')==-signal.SIGALRM else execution['execution_status']
                if status not in ('timeout','out-of-memory'):status='error'
            else:
                require(response and response==read_json(folder/'response.json'),'Missing response evidence')
                require((folder/'response.json').read_text()==execution['stdout'],'Response differs from raw stdout')
                require(response['request_sha256']==digest(request) and response['worker_pid']==execution['pid'],'Worker binding mismatch')
                status=response['status']
                if status=='completed':
                    if micro:
                        try:metrics=routing(response['payload'],fixture,None,case,0);status='accepted'
                        except (ValueError,TypeError,KeyError):status='incorrect'
                    else:
                        verdict=evaluate(bundle,ResultRecord(registration.identity(bundle,instance),0,0,'completed',response['payload']))
                        status=verdict.status;metrics=verdict.metrics
        if evidence['case_budget_remaining_seconds']<=0 and status=='accepted':status='timeout'
        require(status==evidence['verdict']['status'],'Independent verdict disagrees: '+str(path))
        if status=='accepted':
            for field in ('full_cz_count','two_body_dependency_depth','verification'):
                require(metrics[field]==evidence['verdict']['metrics'][field],'Metric replay disagrees')
        outcomes.append({'variant':key[0],'input_id':key[1],'micro':micro,'seed_index':key[2],
                         'verdict':evidence['verdict']})
        if response and response['status']=='completed' and config['sdk']=='flagquantum':
            stages=response['trace']['stages'];source=next(s for s in stages if s.get('stage')=='layout_policy')
            native=next(s for s in stages if s.get('stage')=='first_native_basis')
            counts=source['opcodes']
            if source['two_qubit_instructions']==sum(counts.get(k,0) for k in ('cx','cz','swap')):
                predicted=counts.get('cx',0)+counts.get('cz',0)+3*counts.get('swap',0)
                require(predicted==native['opcodes'].get('cz',0),'Native lowering arithmetic does not match trace')
                swaps.append({'variant':key[0],'input_id':key[1],'cx':counts.get('cx',0),'swap':counts.get('swap',0),
                              'source_cz':counts.get('cz',0),'first_basis_cz':predicted})
    require(seen==expected,'Missing requested diagnostic outcomes')
    report_rows={(r['variant'],r['input_id'],r['seed_index']):r for r in report['outcomes']}
    require(len(report_rows)==len(report['outcomes']) and set(report_rows)==expected,'Report scope incomplete')
    for row in outcomes:
        key=(row['variant'],row['input_id'],row['seed_index'])
        require(row==report_rows[key],'Report disagrees with block evidence')
    return {'schema_version':1,'context':context,'files_verified':len(files),'outcomes_verified':len(outcomes),
            'status_counts':dict(Counter(r['verdict']['status'] for r in outcomes)),'outcomes':outcomes,
            'flagquantum_lowering_arithmetic':swaps,'publication_eligible':False}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--directory',type=Path,required=True)
    p.add_argument('--bundle',type=Path,default=Path('docs/implementation'));p.add_argument('--archive',type=Path);p.add_argument('--summary',type=Path)
    args=p.parse_args();summary=verify(args.directory,Bundle(args.bundle))
    if args.archive:summary['archive_sha256']=archive(args.directory,args.archive)
    if args.summary:
        require(not args.summary.exists(),'Never overwrite replay evidence');args.summary.write_bytes(canonical_bytes(summary))
    print(json.dumps({k:summary[k] for k in ('files_verified','outcomes_verified','status_counts')},indent=2));return 0


if __name__=='__main__':raise SystemExit(main())
