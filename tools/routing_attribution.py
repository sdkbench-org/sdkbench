#!/usr/bin/env python3
"""Run declared native routing controls under the unchanged P0 Linux supervisor."""
import argparse
from dataclasses import replace
import hashlib
import json
import os
from pathlib import Path
import signal
import sys
from sdkbench.p0 import Bundle, Registration, ResultRecord, Verdict, evaluate
from sdkbench.p0.evaluators import routing
from sdkbench.p0.models import canonical_bytes,digest,read_json,require
from sdkbench.p0.supervisor import IsolationUnavailable,Limits,run_command
from sdkbench.p1a.campaign import ActiveCaseBudget
from sdkbench.p1a.common import DISTRIBUTIONS,VERSIONS
from sdkbench.p1a.provenance import capture_environment,distribution_fingerprint,source_fingerprint
from sdkbench.diagnostics.routing import micro_fixtures,variants


def write(path,value):path.write_bytes(canonical_bytes(value))


def implementation():
    root=Path(__file__).resolve().parents[1]
    paths=sorted((root/'src/sdkbench/diagnostics').glob('*.py'))+[Path(__file__).resolve()]
    return source_fingerprint() | {'diagnostic_source_sha256':digest({p.relative_to(root).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in paths})}


def validate(bundle, fixture, instance, micro, identity, response):
    if response['status']!='completed':return Verdict(response['status'],(response['reason'],))
    if not micro:return evaluate(bundle,ResultRecord(identity,0,0,'completed',response['payload']),identity)
    try:return Verdict('accepted',metrics=routing(response['payload'],fixture,None,bundle.cases[instance],0))
    except (ValueError,TypeError,KeyError) as exc:return Verdict('incorrect',(str(exc),))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--directory',required=True,type=Path)
    parser.add_argument('--cgroup-parent',required=True,type=Path)
    parser.add_argument('--bundle',type=Path,default=Path('docs/implementation'))
    parser.add_argument('--profile',type=Path,default=Path('docs/analysis/routing-profile.json'))
    args=parser.parse_args();root=args.directory.resolve();root.mkdir(parents=True,exist_ok=True)
    require(not any(root.iterdir()),'Never overwrite diagnostic evidence')
    bundle=Bundle(args.bundle);profile=read_json(args.profile)
    require(profile['variants']==variants(),'Declared variants differ from implementation')
    require(profile['bundle_sha256']==bundle.sha256,'Diagnostic profile bundle mismatch')
    cpu=min(os.sched_getaffinity(0));runtime={k:os.environ[k] for k in ('LD_LIBRARY_PATH',) if k in os.environ}
    env=capture_environment();impl=implementation();components={};registrations={};admission={}
    write(root/'profile.json',profile);write(root/'environment.json',env)
    write(root/'context.json',{'source_commit':os.environ.get('GITHUB_SHA'),'github_run_id':os.environ.get('GITHUB_RUN_ID'),
           'implementation':impl,'cpu':cpu,'publication_eligible':False,'runtime_environment':runtime,
           'scope':'configuration attribution; one outcome per fresh process; not full-case timing acceptance'})
    cache={}
    for v in profile['variants']:
        sdk=v['sdk'];entries=[{'name':'sdkbench-routing-diagnostics','role':'harness','version':'1',
                              'artifact_sha256':digest(impl)}];reason=None
        for name in [DISTRIBUTIONS[sdk],'numpy']+(['torch'] if sdk=='flagquantum' else ['sympy','networkx'] if sdk=='cirq' else []):
            try:
                if name not in cache:cache[name]=distribution_fingerprint(name)
                item=cache[name];entries.append({k:item[k] for k in ('name','version','artifact_sha256')} | {'role':'frontend' if name==DISTRIBUTIONS[sdk] else 'dependency'})
                if name==DISTRIBUTIONS[sdk] and item['version']!=VERSIONS[sdk]:reason='Pinned SDK version mismatch'
            except Exception as exc:reason=f'{type(exc).__name__}: {exc}'
        components[v['id']]=entries;admission[v['id']]=reason
        registrations[v['id']]=Registration(v['id'],entries,{'profile':'CPU1-FP64','precision':'float64/complex128','threads':1,
           'options':{'variant':v,'diagnostic_profile_sha256':digest(profile),'implementation':impl}},
           {'python':__import__('platform').python_version(),'os':__import__('platform').platform(),
            'image_sha256':env['image_descriptor_sha256'],'dependency_lock_sha256':env['dependency_lock_sha256'],'host':env['host']})
    write(root/'registrations.json',{k:v.to_dict() for k,v in registrations.items()});write(root/'admission.json',admission)
    micros=micro_fixtures(bundle.fixtures['ROUTE-LINE-06']);require(set(micros)==set(profile['micro_ids']),'Microprobe scope mismatch')
    jobs=[]
    for v in profile['variants']:
        for instance in profile['frozen_instances']:
            for block in range(10 if v['seeded'] else 1):jobs.append((v,instance,instance,False,block,bundle.fixtures[instance]))
        if v['id'] in profile['micro_variants']:
            for name in profile['micro_ids']:jobs.append((v,name,'ROUTE-LINE-06',True,0,micros[name]))
    # Rotate configuration order by seed and case; only one participant executes at once.
    jobs.sort(key=lambda j:(j[4],j[1],(profile['variants'].index(j[0])-j[4])%len(profile['variants'])))
    budgets={};outcomes=[]
    try:
        for v,name,instance,micro,block,fixture in jobs:
            folder=root/'runs'/v['id']/name/f'seed-{block:02}';folder.mkdir(parents=True)
            case=bundle.cases[instance];key=(v['id'],name)
            budget=budgets.setdefault(key,ActiveCaseBudget(case['case_wall_limit_seconds']))
            identity=registrations[v['id']].identity(bundle,instance)
            seed=bundle.plan['execution_profile']['compiler_seeds'][block]
            request={'schema_version':1,'config':v,'fixture':fixture,'seed':seed,'block':block,'input_id':name,
                     'micro':micro,'fixture_sha256':digest(fixture),'identity':identity.__dict__ if not micro else None,
                     'profile_sha256':digest(profile)}
            write(folder/'request.json',request);execution=None;response=None
            with budget.active():
                if admission[v['id']]:verdict=Verdict('install-failed',(admission[v['id']],))
                elif budget.remaining<=0:verdict=Verdict('timeout',('Cumulative diagnostic case budget exhausted',))
                else:
                    try:
                        execution=run_command([sys.executable,'-m','sdkbench.diagnostics.worker',str(folder/'request.json')],cwd=folder,
                          cgroup_parent=args.cgroup_parent,limits=replace(Limits.for_case(case,cpu),wall_seconds=budget.remaining),environment=runtime)
                        if execution['execution_status']!='completed':
                            status='timeout' if execution.get('returncode')==-signal.SIGALRM else execution['execution_status']
                            verdict=Verdict(status if status in ('timeout','out-of-memory') else 'error',('Supervisor outcome: '+status,))
                        else:
                            (folder/'response.json').write_text(execution['stdout'])
                            response=read_json(folder/'response.json')
                            require(response['worker_pid']==execution['pid'] and response['request_sha256']==digest(request),'Worker response binding mismatch')
                            verdict=validate(bundle,fixture,instance,micro,identity,response)
                    except IsolationUnavailable as exc:verdict=Verdict('access-blocked',(str(exc),))
                    except (ValueError,TypeError,KeyError,OSError) as exc:verdict=Verdict('error',(f'{type(exc).__name__}: {exc}',))
                if budget.remaining<=0 and verdict.status=='accepted':verdict=Verdict('timeout',('Budget exhausted during independent validation',))
                evidence={'variant':v['id'],'input_id':name,'frozen_instance':None if micro else instance,'micro':micro,'seed_index':block,
                          'execution':execution,'response':response,'verdict':verdict.to_dict(),'case_budget_remaining_seconds':budget.remaining}
                write(folder/'evidence.json',evidence)
            if budget.remaining<=0 and evidence['verdict']['status']=='accepted':
                evidence['verdict']=Verdict('timeout',('Budget exhausted during evidence export',)).to_dict();write(folder/'evidence.json',evidence)
            outcomes.append({k:evidence[k] for k in ('variant','input_id','micro','seed_index','verdict')})
            print(v['id'],name,block,evidence['verdict']['status'],flush=True)
        report={'schema_version':1,'profile_sha256':digest(profile),'implementation':impl,'outcomes':outcomes,
                'publication_eligible':False,'full_case_acceptance_claimed':False}
        write(root/'report.json',report)
        return int(any(row['verdict']['status']!='accepted' for row in outcomes))
    finally:
        write(root/'MANIFEST.json',{'schema_version':1,'files':{p.relative_to(root).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()
                                  for p in sorted(root.rglob('*')) if p.is_file() and p.name!='MANIFEST.json'}})


if __name__=='__main__':raise SystemExit(main())
