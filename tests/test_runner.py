import csv
import json
import copy
import pytest
from sdkbench import run_benchmarks,compare_reports,write_csv,write_json
from sdkbench.backends import BackendUnavailable,ReferenceBackend,get_backend
from sdkbench.cli import main
from sdkbench.runner import measure,summarize


def small_report():
    return run_benchmarks(workloads=['ghz'],n_qubits=3,repeats=2,warmups=0)


def test_reference_end_to_end():
    report=small_report()
    assert report['summary']=={'passed':4,'failed':0,'skipped':1,'error':0}
    for row in report['results']:
        if row['status']=='passed':
            assert len(row['samples_ns'])==2
            assert row['validation']['probe_count']==3
            assert len(row['circuit_sha256'])==64
    assert report['sdks']['reference']['role']=='oracle'
    assert 'python' in report['environment']


def test_timer_counts_and_statistics():
    calls=[]
    result,samples=measure(lambda:calls.append(1) or len(calls),3,2)
    assert result==5 and len(calls)==5 and len(samples)==3
    summary=summarize([10,20,30])
    assert summary['median_ns']==20 and summary['p95_ns']==29 and summary['stdev_ns']==10
    assert summarize([1])['stdev_ns']==0
    with pytest.raises(ValueError): summarize([])


def test_report_exports_and_comparison(tmp_path):
    report=small_report(); path=tmp_path/'r.json'; csv_path=tmp_path/'r.csv'
    write_json(report,path); write_csv(report,csv_path)
    assert json.loads(path.read_text())==report
    with csv_path.open() as f: rows=list(csv.DictReader(f))
    assert len(rows)==5 and rows[0]['status']=='passed'
    candidate=copy.deepcopy(report)
    for row in candidate['results']:
        if row['status']=='passed': row['timing']['median_ns']/=2
    compared=compare_reports(report,candidate)
    assert compared['environment_matches']
    assert all(row['speedup']==2 for row in compared['comparisons'] if 'speedup' in row)
    candidate['config']['seed']=9
    with pytest.raises(ValueError,match='configurations'): compare_reports(report,candidate)


@pytest.mark.parametrize('change',['schema','keys','duplicate','fingerprint','median'])
def test_comparison_rejects_invalid_reports(change):
    report=small_report(); other=copy.deepcopy(report)
    if change=='schema': other['schema_version']=2
    if change=='keys': other['results'].pop()
    if change=='duplicate': other['results'].append(other['results'][0])
    if change=='fingerprint': other['results'][0]['circuit_sha256']='wrong'
    if change=='median': other['results'][0]['timing']['median_ns']=float('nan')
    with pytest.raises(ValueError): compare_reports(report,other)


@pytest.mark.parametrize('kwargs',[
    {'repeats':0},{'warmups':-1},{'seed':-1},{'seed':2**32},{'n_qubits':1},{'depth':0},
    {'sdks':[]},{'sdks':['bad']},{'sdks':['reference','reference']},
    {'workloads':[]},{'operations':['bad']},{'repeats':True},
])
def test_invalid_parameters(kwargs):
    with pytest.raises(ValueError): run_benchmarks(**kwargs)


def test_missing_sdk_is_reported(monkeypatch):
    def unavailable(name): raise BackendUnavailable('not installed')
    monkeypatch.setattr('sdkbench.runner.get_backend',unavailable)
    report=run_benchmarks(sdks=['qiskit'],workloads=['ghz'],operations=['build'],n_qubits=2)
    assert report['summary']['skipped']==1
    assert report['results'][0]['reason']=='not installed'


def test_wrong_backend_fails_correctness(monkeypatch):
    class Wrong(ReferenceBackend):
        def inverse(self,circuit): return circuit
    monkeypatch.setattr('sdkbench.runner.get_backend',lambda name:Wrong())
    report=run_benchmarks(workloads=['brickwork'],operations=['inverse'],n_qubits=2,repeats=1)
    assert report['summary']['failed']==1


def test_backend_exception_is_visible(monkeypatch):
    class Broken(ReferenceBackend):
        def compose(self,circuit): raise RuntimeError('deliberate')
    monkeypatch.setattr('sdkbench.runner.get_backend',lambda name:Broken())
    report=run_benchmarks(workloads=['ghz'],operations=['compose'],n_qubits=2,repeats=1)
    assert report['summary']['error']==1
    assert 'deliberate' in report['results'][0]['reason']


def test_cli(tmp_path,capsys):
    assert main(['list'])==0
    assert 'ghz' in capsys.readouterr().out
    path=tmp_path/'r.json'
    assert main(['run','--qubits','2','--workload','ghz','--repeats','1','--output',str(path)])==0
    assert json.loads(path.read_text())['summary']['passed']==4
    capsys.readouterr()
    assert main(['compare',str(path),str(path)])==0
    assert 'speedup' in capsys.readouterr().out
    assert main(['run','--qubits','0'])==2
    assert 'n_qubits' in capsys.readouterr().err
    assert main(['compare',str(tmp_path/'missing.json'),str(path)])==2
