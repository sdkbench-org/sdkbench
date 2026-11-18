#!/usr/bin/env python3
"""Render/check the candidate roadmap; freeze reference artifacts only on explicit request."""
import argparse
import csv
import hashlib
import io
import json
from pathlib import Path
import platform
import re
import sys
import requirements_docs as requirements

ROOT=Path(__file__).resolve().parents[1]
DOCS=ROOT/'docs/implementation'

def require(value,message):
    if not value:raise ValueError(message)

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def load():return json.loads((DOCS/'roadmap.json').read_text())

def validate(d):
    catalog=json.loads((ROOT/'docs/requirements/catalog.json').read_text())
    require(d['requirements_catalog_sha256']==sha(ROOT/'docs/requirements/catalog.json'),'Requirements baseline changed: review phase assignments')
    tasks={t['id']:t for t in catalog['tasks']}
    assigned=[t['task_id'] for t in d['task_assignments']]
    require(len(assigned)==len(set(assigned)) and set(assigned)==set(tasks),'Missing/duplicate/unknown task assignment')
    phases={p['id'] for p in d['phases']}
    for t in d['task_assignments']:
        require(t['phase'] in phases,'Unknown phase')
        require(all(t[k] in (1,2,3) for k in ['outcome_impact','wrong_answer_consequence','cross_journey_reuse']),'Invalid ordinal')
        require(t['need_score']==4*t['outcome_impact']+3*t['wrong_answer_consequence']+2*t['cross_journey_reuse'],'Stale priority score')
    cases={c['id']:c for c in d['instances']};workflows={w['id']:w for w in d['workflows']}
    require(len(cases)==24==len(d['instances']) and len(workflows)==10,'Unexpected first-wave inventory')
    refs=[];cohorts={c['id'] for c in d['cohorts']}
    for w in workflows.values():
        require(w['primary_task'] in tasks and all(t in tasks for t in w['supporting_tasks']),'Unknown workflow task')
        require(w['cohort'] in cohorts,'Unknown cohort')
        for c in w['instances']:
            require(c in cases and cases[c]['workflow']==w['id'],'Broken workflow/case edge');refs.append(c)
    require(len(refs)==len(set(refs)) and set(refs)==set(cases),'Unassigned/duplicate instance')
    for c in cases.values():
        require(c['case_wall_limit_seconds']>0 and 0<c['process_memory_limit_gib']<=16,'Invalid resource budget')
        require(c['acceptance'] and c['required_negative'] and c['reference'],'Incomplete acceptance contract')
        for field,prefix in [('fixture','fixtures/'),('reference_artifact','references/')]:
            require(c[field]==prefix+c['id']+'.json','Unsafe/mismatched artifact path')
    packages={p['package'] for p in json.loads((DOCS/'candidate-packages.json').read_text())}
    require(all(set(c['packages'])<=packages for c in d['cohorts']),'Unpinned candidate package')
    return catalog,tasks

def render(d,catalog,tasks):
    out={};journeys={j['id']:j for j in catalog['journeys']}
    def tasklink(t):return '../requirements/'+requirements.task_path(tasks[t],journeys)+'#'+t.lower()
    lines=['# First-wave instance contracts\n\n','Generated from [roadmap.json](roadmap.json). Candidate specification only: no participant adapter, result or support claim is implied. All thresholds must pass before reporting accepted timing. These bounded instances do not certify the entire parent task family.\n\n','See [measurement rules](MEASUREMENT_PROTOCOL.md), [references](REFERENCES.md) and [comparison scope](COHORTS.md). Each fixture contains explicit input values, operations, datasets or events; each reference artifact contains the independent expected outputs.\n\n']
    for w in d['workflows']:
        lines += [f"## {w['id']} - {w['title']}\n\n",w['user_outcome']+'\n\n',f"Primary requirement: [{w['primary_task']}]({tasklink(w['primary_task'])}); cohort: `{w['cohort']}`. "]
        if w['supporting_tasks']:lines += ['Supporting requirements: '+', '.join(w['supporting_tasks'])+'. ']
        lines += ['All parent personas, capability/function edges and acceptance profiles remain in the linked requirements baseline.\n\n']
        for c in [c for c in d['instances'] if c['workflow']==w['id']]:
            lines += [f"### {c['id']}\n\n",f"Inputs: [fixture]({c['fixture']}); expected outputs: [reference]({c['reference_artifact']}). Construction arguments: `{json.dumps(c['arguments'],sort_keys=True)}`.\n\n",f"Budget: {c['case_wall_limit_seconds']} seconds for the complete case, {c['process_memory_limit_gib']} GiB aggregate participant memory.\n\n",'Independent reference: '+c['reference']+'\n\n','| Acceptance field | Required value |\n| --- | --- |\n']
            for key,value in c['acceptance'].items():lines += [f"| {key} | {str(value).replace('|',' / ')} |\n"]
            lines += ['\nRequired negative control: '+c['required_negative']+'\n\n','Record: '+c['measurements'].replace(';',', ')+'.\n\n']
    out['FIRST_WAVE.md']=''.join(lines)
    lines=['# Phase assignment and priority register\n\n','Generated from [roadmap.json](roadmap.json). Scores are ordinal maintainer judgments, not validated demand measurements or SDK scores. See [priority policy](PRIORITIES.md). Phase assignment is a delivery plan, not a ranking of user importance; P0 means foundational work on that family, not complete coverage.\n\n','| Task | User outcome | Need score | Phase |\n| --- | --- | --- | --- |\n']
    stream=io.StringIO(newline='');fields=['task_id','title','journey','personas','functions','phase','outcome_impact','wrong_answer_consequence','cross_journey_reuse','need_score','score_evidence','rationale']
    writer=csv.DictWriter(stream,fieldnames=fields,lineterminator='\n');writer.writeheader()
    for a in d['task_assignments']:
        t=tasks[a['task_id']];lines += [f"| [{t['id']}]({tasklink(t['id'])}) | {t['title']} | {a['need_score']} | {a['phase']} |\n"]
        row=dict(a,title=t['title'],journey=t['journey'],personas=';'.join(t['personas']),functions=';'.join(t['functions']));writer.writerow(row)
    out['PHASE_ASSIGNMENTS.md']=''.join(lines);out['priorities.csv']=stream.getvalue()
    lines=['# Candidate package snapshot\n\n','Observed from PyPI metadata on 2026-11-18. These are candidate versions, not resolved environments, verified installs, compatible component stacks or evidence of task support. Freeze full dependency locks and wheel/source hashes after eligibility review; a changed version requires an explicit protocol/environment amendment.\n\n','| Package | Observed version | Declared Python requirement | Metadata source |\n| --- | --- | --- | --- |\n']
    for p in json.loads((DOCS/'candidate-packages.json').read_text()):lines += [f"| {p['package']} | {p['version']} | {p['requires_python'] or 'not declared'} | [PyPI]({p['source']}) |\n"]
    lines += ['\n## Proposed eligibility review by role\n\n','Package names identify components for investigation, not independent leaderboard entries. The actual registered unit is one declared SDK/component/backend stack.\n\n']
    for c in d['cohorts']:lines += [f"### {c['id']}\n\n",c['purpose']+'\n\n',', '.join('`'+p+'`' for p in c['packages'])+'.\n\n']
    out['CANDIDATES.md']=''.join(lines)
    return {p:t.rstrip()+'\n' for p,t in out.items()}

def freeze(d):
    import numpy as np
    import roadmap_reference as oracle
    oracle.verify_anchors()
    artifacts={}
    for c in d['instances']:
        fixture,reference=getattr(oracle,c['kind']+'_fixture')(**c['arguments'])
        for field,value in [('fixture',fixture),('reference_artifact',reference)]:
            path=DOCS/c[field];path.parent.mkdir(parents=True,exist_ok=True)
            path.write_bytes(oracle.json_bytes(value));artifacts[c[field]]=sha(path)
        print('Constructed '+c['id'],flush=True)
    for p in ['roadmap.json','candidate-packages.json']:artifacts[p]=sha(DOCS/p)
    manifest={'protocol_revision':d['protocol_revision'],'role':'Candidate fixture/reference integrity, not participant results or a validated run environment','generator_sha256':sha(ROOT/'tools/roadmap_reference.py'),'python':platform.python_version(),'numpy':np.__version__,'files':artifacts}
    (DOCS/'artifacts.json').write_bytes(oracle.json_bytes(manifest))

def check_artifacts(d):
    manifest=json.loads((DOCS/'artifacts.json').read_text())
    expected={c[f] for c in d['instances'] for f in ['fixture','reference_artifact']}|{'roadmap.json','candidate-packages.json'}
    require(set(manifest['files'])==expected,'Incomplete artifact manifest')
    require(manifest['generator_sha256']==sha(ROOT/'tools/roadmap_reference.py'),'Reference generator changed; reviewed refreeze required')
    for path,digest in manifest['files'].items():require(sha(DOCS/path)==digest,'Artifact hash mismatch: '+path)
    for path in DOCS.rglob('*'):
        if path.is_file() and path.suffix in {'.md','.json','.csv'}:
            content=path.read_text();require(not re.search(r'[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]',content),'CJK text: '+str(path))
            if path.suffix=='.json':require(not re.search(r'[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]',json.dumps(json.loads(content),ensure_ascii=False)),'Decoded CJK')
    old=requirements.DOCS
    try:requirements.DOCS=DOCS;requirements.check_documents()
    finally:requirements.DOCS=old

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--check',action='store_true');parser.add_argument('--freeze',action='store_true');parser.add_argument('--verify-small',action='store_true');args=parser.parse_args()
    d=load();catalog,tasks=validate(d)
    if args.freeze:freeze(d)
    for path,content in render(d,catalog,tasks).items():
        if args.check:require((DOCS/path).read_text()==content,'Stale generated document: '+path)
        else:(DOCS/path).write_text(content)
    check_artifacts(d)
    if args.verify_small:
        import roadmap_reference as oracle
        oracle.verify_anchors()
        import numpy as np
        def compare(a,b):
            if isinstance(a,dict):
                require(a.keys()==b.keys(),'Reference keys differ')
                for k in a:compare(a[k],b[k])
            elif isinstance(a,list):
                require(len(a)==len(b),'Reference shape differs')
                for x,y in zip(a,b):compare(x,y)
            elif isinstance(a,(int,float)):np.testing.assert_allclose(a,b,atol=2e-11,rtol=2e-10)
            else:require(a==b,'Reference value differs')
        for c in d['instances']:
            if c['id'] in {'PARAM-04','OBS-04','GRAD-04','TRAIN-04-B16','DYN-04-S32','SAMPLE-03','ADAPT-TELEPORT','ADAPT-RESET-LOOP','JOB-LOST-ACK','JOB-PARTIAL-CANCEL','ROUND-QASM2','ROUND-QASM3'}:
                _,r=getattr(oracle,c['kind']+'_fixture')(**c['arguments']);compare(r,json.loads((DOCS/c['reference_artifact']).read_text()))
        print('Analytic/dense/derivative/branch anchors and 12 small stored references agree.')
    print('Validated 92 phase assignments, 10 workflows, 24 instances, artifact hashes, English text and local links.')

if __name__=='__main__':main()
