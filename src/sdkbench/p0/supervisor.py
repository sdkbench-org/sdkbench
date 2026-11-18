"""Fail-closed Linux resource execution for reviewed adapters, not hostile-code isolation."""
from dataclasses import asdict, dataclass
import hashlib
import os
from pathlib import Path
import platform
import selectors
import subprocess
import sys
import tempfile
import time
import uuid
from .models import canonical_bytes, finite, integer, require

THREAD_ENV = ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS',
              'VECLIB_MAXIMUM_THREADS', 'BLIS_NUM_THREADS', 'NUMBA_NUM_THREADS', 'TF_NUM_INTRAOP_THREADS',
              'TF_NUM_INTEROP_THREADS')


class IsolationUnavailable(RuntimeError):
    """A required kernel control is unavailable; no participant command was started."""


@dataclass(frozen=True)
class Limits:
    wall_seconds: float
    memory_bytes: int
    cpu: int
    output_bytes: int = 8 * 1024 * 1024
    file_bytes: int = 32 * 1024 * 1024
    tasks: int = 128

    def __post_init__(self):
        require(0 < finite(self.wall_seconds) <= 86400, 'Invalid wall limit')
        for name in ('memory_bytes', 'output_bytes', 'file_bytes', 'tasks'):integer(getattr(self, name), 1)
        integer(self.cpu)

    @classmethod
    def for_case(cls, case, cpu, stage='case'):
        require(stage in ('case', 'compile'), 'Unknown execution stage')
        wall = case['case_wall_limit_seconds']
        if stage == 'compile':
            require(case['kind'] == 'route', 'Compilation stage is only defined for routing')
            wall = min(wall, case['acceptance']['per_compile_wall_limit_seconds'])
        return cls(wall, case['process_memory_limit_gib'] * 1024**3, cpu)


def _read_counters(path):
    return {line.split()[0]: int(line.split()[1]) for line in path.read_text().splitlines()}


def _rss_and_threads(group):
    rss = threads = 0
    for pid in (group / 'cgroup.procs').read_text().split():
        try:
            lines = Path('/proc', pid, 'status').read_text().splitlines()
            for line in lines:
                if line.startswith('VmRSS:'):rss += int(line.split()[1]) * 1024
                if line.startswith('Threads:'):threads += int(line.split()[1])
        except (FileNotFoundError, ProcessLookupError):pass
    return rss, threads


def host_snapshot():
    """Observed host facts, not a sealed or independently reviewed study manifest."""
    result = {'platform': platform.platform(), 'python': platform.python_version(), 'machine': platform.machine(),
              'clock': vars(time.get_clock_info('perf_counter')), 'cpu_count': os.cpu_count()}
    if hasattr(os, 'sched_getaffinity'):result['allowed_cpus'] = sorted(os.sched_getaffinity(0))
    if Path('/proc/cpuinfo').is_file():
        result['cpuinfo_sha256'] = hashlib.sha256(Path('/proc/cpuinfo').read_bytes()).hexdigest()
        result['cpu_models'] = sorted({line.partition(':')[2].strip() for line in Path('/proc/cpuinfo').read_text().splitlines() if line.startswith('model name')})
    return result


def _create_group(parent, limits):
    if sys.platform != 'linux':raise IsolationUnavailable('Strict execution requires Linux cgroup v2 and libseccomp; no fallback')
    parent = Path(parent).resolve()
    if not parent.is_relative_to('/sys/fs/cgroup') or parent == Path('/sys/fs/cgroup'):
        raise IsolationUnavailable('Provide an explicitly delegated non-root cgroup-v2 subtree')
    group = parent / ('sdkbench-' + uuid.uuid4().hex)
    try:
        group.mkdir()
        required = ('memory.max', 'memory.swap.max', 'memory.oom.group', 'memory.peak', 'memory.events',
                    'cpu.max', 'cpu.stat', 'cpuset.cpus', 'cpuset.mems', 'pids.max', 'cgroup.kill')
        if not all((group / name).exists() for name in required):
            raise OSError('Delegate memory, cpu, cpuset and pids controllers on cgroup v2 with memory.peak/cgroup.kill')
        if limits.cpu not in os.sched_getaffinity(0):raise OSError('Requested CPU is outside supervisor affinity')
        values = {'memory.max': limits.memory_bytes, 'memory.swap.max': 0, 'memory.oom.group': 1,
                  'cpu.max': '100000 100000', 'cpuset.cpus': limits.cpu,
                  'cpuset.mems': (parent / 'cpuset.mems.effective').read_text().strip(), 'pids.max': limits.tasks}
        for name, value in values.items():(group / name).write_text(str(value))
        return group
    except OSError as exc:
        if group.exists():group.rmdir()
        raise IsolationUnavailable(str(exc)) from exc


def run_command(argv, *, cwd, cgroup_parent, limits, environment=None):
    """Execute one bounded stage. Returns raw evidence; never implies task acceptance.

    The trusted operator delegates a cgroup subtree. There is no privileged host
    configuration, shell, SDK allowlist or quiet resource-control fallback here.
    Kernel memory.max is stricter than an RSS-only limit (it includes charged cache).
    """
    require(isinstance(argv, list) and argv and all(isinstance(x, str) and x for x in argv), 'Command must be an argv list')
    cwd = Path(cwd).resolve(); require(cwd.is_dir(), 'Missing working directory')
    require(isinstance(limits, Limits), 'Missing explicit limits')
    custom = environment or {}
    require(isinstance(custom, dict) and all(isinstance(k, str) and isinstance(v, str) for k, v in custom.items()), 'Invalid environment')
    # Explicit environment only: do not inherit credentials from the operator shell.
    env = {'PATH': '/usr/local/bin:/usr/bin:/bin', 'LANG': 'C.UTF-8', 'PYTHONHASHSEED': '0', **custom}
    env.update({k: '1' for k in THREAD_ENV}); env['OMP_DYNAMIC'] = 'FALSE'; env['MKL_DYNAMIC'] = 'FALSE'
    group = _create_group(cgroup_parent, limits)
    started = time.perf_counter(); clock_start_ns = time.time_ns()
    output = {'stdout': bytearray(), 'stderr': bytearray()}; ready_data = bytearray()
    truncated = False
    status = None; peak_rss = peak_threads = 0; process = None; selector = selectors.DefaultSelector()
    read_ready, write_ready = os.pipe()
    try:
        with tempfile.TemporaryDirectory(prefix='sdkbench-launch-') as temporary:
            env['HOME'] = temporary; env['TMPDIR'] = temporary
            config = {'cgroup': str(group), 'cpu': limits.cpu, 'file_bytes': limits.file_bytes,
                      'cwd': str(cwd), 'argv': argv, 'environment': env}
            config_path = Path(temporary) / 'launch.json'; config_path.write_bytes(canonical_bytes(config))
            launcher = Path(__file__).with_name('_isolate.py')
            process = subprocess.Popen([sys.executable, '-I', str(launcher), str(config_path), str(write_ready)],
                                       stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                       pass_fds=(write_ready,), start_new_session=True)
            os.close(write_ready); write_ready = None
            for stream, name in ((process.stdout, 'stdout'), (process.stderr, 'stderr'), (read_ready, 'ready')):
                fd = stream if isinstance(stream, int) else stream.fileno()
                os.set_blocking(fd, False); selector.register(fd, selectors.EVENT_READ, name)
            while True:
                elapsed = time.perf_counter() - started
                if elapsed >= limits.wall_seconds and status is None:status = 'timeout'
                rss, threads = _rss_and_threads(group); peak_rss = max(peak_rss, rss); peak_threads = max(peak_threads, threads)
                if _read_counters(group / 'memory.events').get('oom_kill', 0):status = 'out-of-memory'
                if status is not None:(group / 'cgroup.kill').write_text('1')
                for key, _ in selector.select(.01):
                    try:data = os.read(key.fd, 65536)
                    except BlockingIOError:continue
                    if not data:selector.unregister(key.fd); continue
                    if key.data == 'ready':ready_data.extend(data)
                    else:
                        remaining = limits.output_bytes - sum(len(b) for b in output.values())
                        output[key.data].extend(data[:max(0, remaining)])
                        if len(data) > remaining:
                            truncated = True
                            if status is None:status = 'output-limit'
                if process.poll() is not None:
                    if (group / 'cgroup.events').read_text().find('populated 1') >= 0:
                        if status is None:status = 'child-leak'
                        (group / 'cgroup.kill').write_text('1')
                    if not selector.get_map():break
                if elapsed > limits.wall_seconds + 5:
                    raise IsolationUnavailable('Process group did not terminate after enforced kill')
            process.wait()
            elapsed = time.perf_counter() - started
            if ready_data != b'ready\n':status = 'isolation-failed'
            elif status is None:status = 'completed' if process.returncode == 0 else 'error'
            events = _read_counters(group / 'memory.events')
            if events.get('oom_kill', 0):status = 'out-of-memory'
            return {'schema_version': 1, 'execution_status': status, 'returncode': process.returncode,
                    'wall_seconds': elapsed, 'started_unix_ns': clock_start_ns,
                    'peak_sampled_rss_bytes': peak_rss, 'peak_sampled_threads': peak_threads,
                    'kernel_memory_peak_bytes': int((group / 'memory.peak').read_text()),
                    'memory_events': events, 'cpu_stat': _read_counters(group / 'cpu.stat'),
                    'pids_events': _read_counters(group / 'pids.events'),
                    'enforced_cpu_set': (group / 'cpuset.cpus.effective').read_text().strip(),
                    'limits': asdict(limits), 'network_policy': 'seccomp-deny-sockets-and-io-uring',
                    'host': host_snapshot(), 'argv': argv,
                    'environment_sha256': hashlib.sha256(canonical_bytes(env)).hexdigest(),
                    'stdout': output['stdout'].decode('utf-8', errors='replace'),
                    'stderr': output['stderr'].decode('utf-8', errors='replace'),
                    'stdout_sha256': hashlib.sha256(output['stdout']).hexdigest(),
                    'stderr_sha256': hashlib.sha256(output['stderr']).hexdigest(),
                    'output_truncated': truncated}
    finally:
        try:
            (group / 'cgroup.kill').write_text('1')
            if process is not None:process.wait(timeout=5)
            deadline = time.monotonic() + 3
            while 'populated 1' in (group / 'cgroup.events').read_text() and time.monotonic() < deadline:time.sleep(.01)
            group.rmdir()
        finally:
            selector.close(); os.close(read_ready)
            if write_ready is not None:os.close(write_ready)
            if process is not None:
                if process.stdout:process.stdout.close()
                if process.stderr:process.stderr.close()
