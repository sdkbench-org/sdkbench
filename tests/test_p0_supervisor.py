"""Real Linux resource fault tests; strict CI opts in and may not silently skip."""
import json
import os
from pathlib import Path
import sys
import time
import pytest
from sdkbench.p0.execution import CaseBudget, execute_once
from sdkbench.p0 import Bundle
from sdkbench.p0.models import ContractError
from sdkbench.p0.supervisor import IsolationUnavailable, Limits, THREAD_ENV, run_command

ROOT = Path(__file__).resolve().parents[1]
PARENT = os.environ.get('SDKBENCH_TEST_CGROUP')
RUNTIME_ENV = {'LD_LIBRARY_PATH': os.environ['LD_LIBRARY_PATH']} if 'LD_LIBRARY_PATH' in os.environ else {}
linux = pytest.mark.skipif(not PARENT, reason='Strict cgroup integration runs in the dedicated Linux CI job')


def test_limits_and_case_budget():
    clock = [100.]; budget = CaseBudget(5, clock=lambda: clock[0]); assert budget.remaining == 5
    clock[0] += 4; assert budget.remaining == 1
    clock[0] += 4; assert budget.remaining == 0
    with pytest.raises(ContractError):Limits(-1, 1024, 0)
    with pytest.raises(ContractError):Limits(1, True, 0)
    assert Limits.for_case({'kind': 'route', 'case_wall_limit_seconds': 600, 'process_memory_limit_gib': 16, 'acceptance': {'per_compile_wall_limit_seconds': 120}}, 0, 'compile').wall_seconds == 120


def test_no_fallback_when_controls_unavailable(tmp_path):
    marker = tmp_path / 'must-not-exist'
    with pytest.raises(IsolationUnavailable):
        run_command([sys.executable, '-c', f'open({str(marker)!r},"w").write("ran")'], cwd=tmp_path,
                    cgroup_parent=tmp_path, limits=Limits(2, 128 * 1024**2, 0))
    assert not marker.exists()


@linux
def test_candidate_environment_selection_under_real_kernel_controls(tmp_path):
    from sdkbench.candidates.environment import interpreter_identity
    from sdkbench.p1a.campaign import ActiveCaseBudget, run_block
    from test_candidate_environments import synthetic_environments
    from test_candidate_runner import admission

    bundle = Bundle(ROOT / 'docs/implementation')
    environments = synthetic_environments(tmp_path)
    for python, registration in environments:
        selection = interpreter_identity(python)
        identity = registration.identity(bundle, 'ROUTE-LINE-06')
        directory = tmp_path / registration.stack_id
        result = run_block(
            bundle, identity, registration.stack_id, 0, mode='protocol',
            directory=directory, cgroup_parent=PARENT,
            cpu=min(os.sched_getaffinity(0)), budget=ActiveCaseBudget(600),
            runtime_environment={**RUNTIME_ENV, 'PYTHONPATH': str(ROOT / 'src')},
            suite='compiler-candidate', candidate=registration, interpreter=selection,
        )
        execution, response = result['execution'], result['response']
        assert execution['execution_status'] == 'completed'
        assert execution['argv'][0] == python
        assert execution['limits']['memory_bytes'] == 16 * 1024**3
        assert execution['network_policy'] == 'seccomp-deny-sockets-and-io-uring'
        assert response['candidate_interpreter'] == selection
        assert response['candidate_admission'] == admission(registration)
        assert len(response['warmups']) == 2 and len(response['records']) == 3
        version = response['sdk_version']
        assert all(r['status'] == 'error' and f'synthetic-sdk-{version}-imported' in r['reason']
                   for r in response['warmups'] + response['records'])
        assert result['block_verdict']['status'] != 'accepted'
    assert not list(Path(PARENT).glob('sdkbench-*'))


def invoke(code, tmp_path, *, wall=3, memory=128 * 1024**2, output=100000):
    return run_command([sys.executable, '-c', code], cwd=tmp_path, cgroup_parent=PARENT,
                       limits=Limits(wall, memory, min(os.sched_getaffinity(0)), output_bytes=output),
                       environment={**RUNTIME_ENV, 'OMP_NUM_THREADS': '32'})


@linux
def test_real_limits_affinity_threads_and_clock(tmp_path, monkeypatch):
    monkeypatch.setenv('SDKBENCH_FAKE_SECRET', 'not-in-worker')
    start = time.perf_counter()
    r = invoke('import os,time,json; time.sleep(.1); print(json.dumps({"cpus":list(os.sched_getaffinity(0)),"threads":os.environ["OMP_NUM_THREADS"],"home":os.environ["HOME"],"secret":os.environ.get("SDKBENCH_FAKE_SECRET")}))', tmp_path)
    assert r['execution_status'] == 'completed', r['stderr'] or r
    data = json.loads(r['stdout']); assert len(data['cpus']) == 1 and data['threads'] == '1' and data['secret'] is None
    assert r['wall_seconds'] >= .1 and r['wall_seconds'] <= time.perf_counter() - start
    assert r['kernel_memory_peak_bytes'] > 0 and r['peak_sampled_rss_bytes'] > 0
    assert r['cpu_stat']['usage_usec'] > 0
    assert not list(Path(PARENT).glob('sdkbench-*'))


@linux
def test_actual_timeout_and_child_group_cleanup(tmp_path):
    r = invoke('import subprocess,sys,time; subprocess.Popen([sys.executable,"-c","import os,time;os.setsid();time.sleep(20)"]);time.sleep(20)', tmp_path, wall=.4)
    assert r['execution_status'] == 'timeout', r
    assert r['wall_seconds'] < 2
    assert not list(Path(PARENT).glob('sdkbench-*'))


@linux
def test_actual_kernel_oom_in_child(tmp_path):
    r = invoke('import subprocess,sys; subprocess.run([sys.executable,"-c","x=bytearray(400*1024*1024)"]);print("parent survived")', tmp_path, memory=64 * 1024**2)
    assert r['execution_status'] == 'out-of-memory', r
    assert r['memory_events']['oom_kill'] > 0
    assert not list(Path(PARENT).glob('sdkbench-*'))


@linux
def test_detached_child_cannot_leak_after_parent_exit(tmp_path):
    r = invoke('import subprocess,sys; subprocess.Popen([sys.executable,"-c","import os,time;os.setsid();time.sleep(20)"],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)', tmp_path)
    assert r['execution_status'] == 'child-leak', r
    assert not list(Path(PARENT).glob('sdkbench-*'))


@linux
@pytest.mark.parametrize('family', ['AF_INET', 'AF_INET6', 'AF_UNIX'])
def test_network_syscalls_denied_in_process_and_descendant(tmp_path, family):
    code = f'import socket,errno;\ntry: socket.socket(socket.{family},socket.SOCK_STREAM)\nexcept OSError as e: assert e.errno == errno.EPERM;print("denied")\nelse: raise RuntimeError("network escaped")'
    r = invoke(code, tmp_path); assert r['execution_status'] == 'completed' and r['stdout'].strip() == 'denied', r
    child = invoke('import subprocess,sys;subprocess.run([sys.executable,"-c",' + repr(code) + '],check=True)', tmp_path)
    assert child['execution_status'] == 'completed' and child['stdout'].strip() == 'denied', child


@linux
def test_bounded_output_and_crash(tmp_path):
    r = invoke('import os;os.write(1,b"x"*1000000)', tmp_path, output=1000)
    assert r['execution_status'] == 'output-limit' and len(r['stdout']) <= 1000
    assert r['output_truncated']
    r = invoke('raise RuntimeError("fault")', tmp_path)
    assert r['execution_status'] == 'error' and 'RuntimeError: fault' in r['stderr']


@linux
def test_worker_integration_rejects_false_success_and_invalid_output(tmp_path):
    bundle = Bundle(ROOT / 'docs/implementation'); identity = bundle.identity('PARAM-04', 'synthetic-only', '1' * 64, '2' * 64)
    for index, code in enumerate(['print("not JSON")', 'import time;time.sleep(20)', 'import json;print(json.dumps({"status":"accepted"}))']):
        worker = tmp_path / f'worker-{index}.py'; worker.write_text(code)
        budget = CaseBudget(.5)
        evidence = execute_once(bundle, identity, [sys.executable, str(worker)], cgroup_parent=PARENT,
                                cpu=min(os.sched_getaffinity(0)), directory=tmp_path / f'run-{index}', budget=budget, environment=RUNTIME_ENV)
        assert evidence['verdict']['status'] in ('incorrect', 'timeout'), evidence
        assert (tmp_path / f'run-{index}/evidence.json').is_file()


def test_shared_budget_exhaustion_does_not_launch(tmp_path):
    bundle = Bundle(ROOT / 'docs/implementation'); identity = bundle.identity('PARAM-04', 'synthetic-only', '1' * 64, '2' * 64)
    clock = [0.]; budget = CaseBudget(1, clock=lambda: clock[0]); clock[0] = 2.
    marker = tmp_path / 'not-launched'
    evidence = execute_once(bundle, identity, [sys.executable, '-c', f'open({str(marker)!r},"w").write("bad")'],
                            cgroup_parent=tmp_path, cpu=0, directory=tmp_path / 'run', budget=budget)
    assert evidence['verdict']['status'] == 'timeout' and evidence['execution'] is None
    assert not marker.exists()
    with pytest.raises(ContractError):
        execute_once(bundle, identity, ['irrelevant'], cgroup_parent=tmp_path, cpu=0, directory=tmp_path / 'run')


@linux
def test_worker_positive_and_kernel_failure_cannot_claim_success(tmp_path):
    from p0_cases import record
    bundle = Bundle(ROOT / 'docs/implementation'); result = record(bundle, 'PARAM-04')
    worker = tmp_path / 'positive.py'; serialized = json.dumps(result.to_dict(), allow_nan=False)
    worker.write_text('import sys,json\nrequest=json.load(open(sys.argv[1]))\nassert "reference" not in request\nprint(' + repr(serialized) + ')\n')
    evidence = execute_once(bundle, result.identity, [sys.executable, str(worker)], cgroup_parent=PARENT,
                            cpu=min(os.sched_getaffinity(0)), directory=tmp_path / 'positive', environment=RUNTIME_ENV)
    assert evidence['verdict']['status'] == 'accepted', evidence['execution']['stderr'] or evidence
    assert evidence['execution']['execution_status'] == 'completed'
    worker.write_text('import time\nprint(' + repr(serialized) + ',flush=True)\ntime.sleep(20)\n')
    evidence = execute_once(bundle, result.identity, [sys.executable, str(worker)], cgroup_parent=PARENT,
                            cpu=min(os.sched_getaffinity(0)), directory=tmp_path / 'false-success', budget=CaseBudget(.4), environment=RUNTIME_ENV)
    assert evidence['verdict']['status'] == 'timeout' and evidence['record'] is None


def test_materialization_cannot_overrun_shared_case_budget(tmp_path, monkeypatch):
    from p0_cases import record
    import sdkbench.p0.execution as execution
    bundle = Bundle(ROOT / 'docs/implementation'); result = record(bundle, 'PARAM-04')
    clock = [0.]; budget = CaseBudget(1, clock=lambda: clock[0])
    def fake_run(*args, **kwargs):
        clock[0] = 2.
        return {'execution_status': 'completed', 'stdout': json.dumps(result.to_dict())}
    monkeypatch.setattr(execution, 'run_command', fake_run)
    evidence = execute_once(bundle, result.identity, ['reviewed-worker'], cgroup_parent=tmp_path, cpu=0,
                            directory=tmp_path / 'run', budget=budget)
    assert evidence['verdict']['status'] == 'timeout'
    assert evidence['record'] is not None
