"""Versioned, SDK-neutral evidence records. Semantic and execution outcomes stay separate."""
from dataclasses import asdict, dataclass, field
import hashlib
import json
import math
import re
from typing import Any, Protocol

SCHEMA_VERSION = 1
PARTICIPANT_STATUSES = frozenset({
    'completed', 'not-implemented', 'unsupported', 'install-failed', 'access-blocked',
    'not-measured', 'timeout', 'out-of-memory', 'error',
})


class ContractError(ValueError):
    """Malformed, incomplete or incorrect task evidence."""


def require(condition, message):
    if not condition:
        raise ContractError(message)


def keys(value, required, optional=()):
    require(isinstance(value, dict), 'Expected an object')
    require(set(required) <= value.keys() <= set(required) | set(optional),
            'Missing or unknown fields: ' + ', '.join(sorted(set(required) ^ set(value))))


def integer(value, lower=0):
    require(type(value) is int and value >= lower, 'Expected an integer >= ' + str(lower))
    return value


def finite(value):
    require(type(value) in (int, float) and math.isfinite(value), 'Expected a finite real number')
    return value


def canonical_bytes(value):
    return (json.dumps(value, sort_keys=True, indent=2, allow_nan=False) + '\n').encode('utf-8')


def digest(value):
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def read_json(path, max_bytes=32 * 1024 * 1024):
    """Bounded JSON, rejecting duplicate keys and nonstandard nonfinite constants."""
    def pairs(items):
        result = {}
        for k, v in items:
            require(k not in result, 'Duplicate JSON key: ' + k)
            result[k] = v
        return result
    with open(path, 'rb') as stream:
        data = stream.read(max_bytes + 1)
    require(len(data) <= max_bytes, 'JSON artifact exceeds byte limit')
    try:
        return json.loads(data, object_pairs_hook=pairs,
                          parse_constant=lambda v: (_ for _ in ()).throw(ContractError('Nonfinite JSON: ' + v)))
    except (UnicodeError, json.JSONDecodeError, RecursionError) as exc:
        raise ContractError('Invalid JSON artifact') from exc


@dataclass(frozen=True)
class Identity:
    protocol_revision: str
    instance_id: str
    fixture_sha256: str
    reference_sha256: str
    bundle_sha256: str
    stack_id: str
    configuration_sha256: str
    environment_sha256: str

    def __post_init__(self):
        for name in ('protocol_revision', 'instance_id', 'stack_id'):
            require(isinstance(getattr(self, name), str) and bool(getattr(self, name)), 'Empty identity: ' + name)
        for name in ('fixture_sha256', 'reference_sha256', 'bundle_sha256', 'configuration_sha256', 'environment_sha256'):
            require(isinstance(getattr(self, name), str) and re.fullmatch('[0-9a-f]{64}', getattr(self, name)),
                    'Invalid SHA256: ' + name)


@dataclass(frozen=True)
class ResultRecord:
    identity: Identity
    block: int
    repetition: int
    status: str
    payload: dict | None = None
    reason: str | None = None
    measurements: dict = field(default_factory=dict)
    schema_version: int = SCHEMA_VERSION

    def __post_init__(self):
        require(type(self.schema_version) is int and self.schema_version == SCHEMA_VERSION, 'Unsupported result schema')
        require(isinstance(self.identity, Identity), 'Expected a typed identity')
        integer(self.block); integer(self.repetition)
        require(self.block < 10, 'Block must be in 0..9')
        require(self.status in PARTICIPANT_STATUSES, 'Unknown participant status')
        if self.status == 'completed':
            require(isinstance(self.payload, dict) and self.reason is None, 'Completed results require a payload and no failure reason')
        else:
            require(self.payload is None and isinstance(self.reason, str) and bool(self.reason.strip()),
                    'Noncompleted results require a reason and no success payload')
        require(isinstance(self.measurements, dict), 'Measurements must be an object')
        for key, value in self.measurements.items():
            require(isinstance(key, str), 'Invalid measurement name')
            require(finite(value) >= 0, 'Negative measurement')
        try:
            canonical_bytes(self.to_dict())
        except (ValueError, TypeError, RecursionError) as exc:
            raise ContractError('Result must contain finite JSON data') from exc

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, value):
        keys(value, ('identity', 'block', 'repetition', 'status', 'schema_version'),
             ('payload', 'reason', 'measurements'))
        keys(value['identity'], Identity.__dataclass_fields__)
        return cls(**{**value, 'identity': Identity(**value['identity'])})


def implementation_fingerprint():
    """Identify the actual evaluator/supervisor source, including unreleased edits."""
    from pathlib import Path
    from .. import __version__
    hasher = hashlib.sha256()
    for path in sorted(Path(__file__).parent.glob('*.py')):
        hasher.update(path.name.encode()); hasher.update(b'\0'); hasher.update(path.read_bytes())
    return {'sdkbench_version': __version__, 'p0_source_sha256': hasher.hexdigest()}


@dataclass(frozen=True)
class Verdict:
    status: str
    reasons: tuple[str, ...] = ()
    metrics: dict[str, Any] = field(default_factory=dict)
    scope: str = 'semantic-evidence-only; not a qualified performance publication'

    def to_dict(self):
        return {**asdict(self), 'implementation': implementation_fingerprint()}


class Adapter(Protocol):
    """A future adapter receives fixture inputs, never a numerical gold payload.

    Adapter configuration and environment are registered outside the worker.
    Construction, JIT, synchronization and materialization belong to execute().
    Unavailable capabilities must return an explicit noncompleted result.
    """
    def execute(self, request: dict) -> ResultRecord: ...
