"""Connect the bounded worker protocol to independent evaluation, without SDK logic."""
from dataclasses import replace
from pathlib import Path
import time
from .evaluators import evaluate
from .models import ContractError, ResultRecord, Verdict, canonical_bytes, finite, read_json, require
from .supervisor import IsolationUnavailable, Limits, run_command


class CaseBudget:
    """One shared elapsed-time budget for an entire case, including setup and cleanup.

    Create before case setup and retain it across warmups, stages and blocks.
    A future campaign scheduler must use this object rather than resetting it per call.
    """
    def __init__(self, wall_seconds, clock=time.perf_counter):
        require(finite(wall_seconds) > 0, 'Invalid case wall budget')
        self.wall_seconds = wall_seconds; self._clock = clock; self._started = clock()

    @property
    def remaining(self):return max(0., self.wall_seconds - (self._clock() - self._started))


def execute_once(bundle, identity, argv, *, cgroup_parent, cpu, directory, block=0, repetition=0,
                 budget=None, stage='case'):
    """Run one adapter invocation; not a complete ten-block performance study.

    The adapter command receives one final argument, the absolute request JSON path.
    It returns one ResultRecord on stdout and writes diagnostics to stderr.
    The caller must register argv/configuration and inspect all returned evidence.
    """
    bundle.verify_identity(identity)
    directory = Path(directory).resolve(); directory.mkdir(parents=True, exist_ok=True)
    require(not any(directory.iterdir()), 'Never overwrite a nonempty evidence directory')
    require(isinstance(argv, list) and argv and all(isinstance(x, str) and x for x in argv), 'Missing adapter command')
    request = bundle.request(identity, block, repetition)
    request_path = directory / 'request.json'; request_path.write_bytes(canonical_bytes(request))
    case = bundle.cases[identity.instance_id]; budget = budget or CaseBudget(case['case_wall_limit_seconds'])
    limits = Limits.for_case(case, cpu, stage)
    record = None; execution = None
    if budget.remaining <= 0:
        verdict = Verdict('timeout', ('Shared case budget exhausted before launch',))
    else:
        limits = replace(limits, wall_seconds=min(limits.wall_seconds, budget.remaining))
        try:
            execution = run_command(argv + [str(request_path)], cwd=directory, cgroup_parent=cgroup_parent, limits=limits)
            outcome = execution['execution_status']
            if outcome != 'completed':
                status = outcome if outcome in ('timeout', 'out-of-memory') else 'access-blocked' if outcome == 'isolation-failed' else 'error'
                verdict = Verdict(status, ('Supervisor outcome: ' + outcome,))
            else:
                stdout = directory / 'result.stdout.json'; stdout.write_text(execution['stdout'], encoding='utf-8')
                try:
                    record = ResultRecord.from_dict(read_json(stdout))
                    require(record.block == block and record.repetition == repetition, 'Invocation/block/repetition mismatch')
                    verdict = evaluate(bundle, record, identity)
                except (ContractError, ValueError, TypeError, KeyError) as exc:
                    verdict = Verdict('incorrect', ('Invalid worker result: ' + str(exc),))
        except IsolationUnavailable as exc:
            verdict = Verdict('access-blocked', ('Isolation unavailable: ' + str(exc),))
    evidence = {'schema_version': 1, 'request': request, 'execution': execution,
                'record': record.to_dict() if record is not None else None, 'verdict': verdict.to_dict(),
                'case_budget_remaining_seconds': budget.remaining,
                'scope': 'one adapter invocation; not P0 review certification or a performance study'}
    (directory / 'evidence.json').write_bytes(canonical_bytes(evidence))
    return evidence
