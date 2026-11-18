# P1a engineering qualification results

Date: 2026-11-18. Protocol: `sdkbench-first-wave / 0.1-candidate-1`. This records real native SDK execution, not a universal SDK ranking or an independently approved performance study.

## Outcomes

All three published stacks passed every attempted frozen instance in the extended one-outcome qualification. No native unsupported outcome, incorrect result, timeout, OOM or execution failure was observed in these completed runs. This statement is limited to the specified tasks and package versions; it does not certify every variant in their parent requirement families.

| Frozen instance | FlagQuantum 0.3.1 | Qiskit 2.6.2 | Cirq 1.7.0 |
| --- | --- | --- | --- |
| PARAM-04 | Accepted qualification | Accepted qualification | Accepted qualification |
| PARAM-12 | Accepted qualification | Accepted qualification | Accepted qualification |
| PARAM-24 | Accepted qualification | Accepted qualification | Accepted qualification |
| OBS-04 | Accepted qualification | Accepted qualification | Accepted qualification |
| OBS-12 | Accepted qualification | Accepted qualification | Accepted qualification |
| OBS-20 | Accepted qualification | Accepted qualification | Accepted qualification |
| SAMPLE-03 | Accepted qualification | Accepted qualification | Accepted qualification |
| SAMPLE-05 | Accepted qualification | Accepted qualification | Accepted qualification |

Each cell above is one complete measured outcome in one fresh process, using the original inputs, thresholds and caps. These 24 successful qualifications remain `not-measured` at complete-case level because ten blocks are absent. They must not be presented as 24 completed full protocol cases.

The final small-case run additionally completed the prescribed ten fresh process blocks, including two warmups and three measured repetitions for each numeric block, and zero warmups/one measured acquisition for each sampling block:

| Complete case | Per SDK measured records | Per SDK warmups | Complete-case acceptance across three SDKs |
| --- | --- | --- | --- |
| PARAM-04 | 30 | 20 | 3 / 3 accepted |
| OBS-04 | 30 | 20 | 3 / 3 accepted |
| SAMPLE-03 | 10 | 0 | 3 / 3 accepted |
| SAMPLE-05 | 10 | 0 | 3 / 3 accepted |

The final run therefore contains **120 fresh worker blocks, 240 measured records and 120 independently checked warmups**. All pass the same P0 evaluators. The complete W08 sampling family passes for each SDK. W01 and W04 retain incomplete workflow coverage: their larger sizes have one-outcome qualification, not ten-block execution.

## Reproducible evidence

| Dataset | Executed source | CI run | Retained scope |
| --- | --- | --- | --- |
| [Extended archive](evidence/p1a-extended-7797c24.json.gz) | `7797c246e2f7e504afe8fd0156ab6284a451b6b4` | [Completed extended run](https://github.com/sdkbench-org/sdkbench/actions/runs/44260127517) | All eight sizes plus original small protocol; 144 blocks, 264 measured records, 120 warmups; 444 verified evidence files |
| [Final small archive](evidence/p1a-small-51ce241.json.gz) | `51ce241287e8c7fc752889290074586baebf0de3` | [Completed final small run](https://github.com/sdkbench-org/sdkbench/actions/runs/44262299896) | Final implementation's complete small protocol; 120 blocks, 240 measured records, 120 warmups; 367 verified evidence files |

[Evidence index](evidence/index.json) records archive hashes, source commits, versions and limitations. Every original UTF-8 file is preserved losslessly inside the compressed JSON containers with its original path and SHA256. The archives include requests, native outputs, raw bounded process streams, registrations, package-content hashes, environment/dependency facts, resource telemetry, warnings, warmups, measured records, admission decisions and P0 verdicts. The original artifact manifests and all retained file hashes were checked; every measured/warmup decision was independently replayed without rerunning or importing a participant SDK.

The extended run uses the earlier Qiskit bitstring normalization. The final small run verifies the native `BitArray.to_bool_array(order='little')` path. Sampling generation, numeric adapters, frozen references and thresholds were unchanged; the implementation provenance is recorded separately. No timing data from those revisions or different hosts is pooled into a performance claim.

To inspect an archive:

```python
import gzip
import hashlib
import json
from pathlib import Path

archive = Path("docs/implementation/evidence/p1a-small-51ce241.json.gz")
container = json.loads(gzip.decompress(archive.read_bytes()))
for relative, entry in container["files"].items():
    original = entry["utf8"].encode("utf-8")
    assert hashlib.sha256(original).hexdigest() == entry["sha256"]
    # Inspect original JSON/text bytes; preserve their relative paths when extracting.
```

After extracting to an empty directory, `python tools/p1a_evidence.py --directory PATH --bundle docs/implementation` verifies the original manifest and replays the P0 decisions.

## Failure-accounting qualification

Synthetic adverse tests separately exercise missing installations, absent native capabilities, native exceptions, timeouts, malformed JSON/records, wrong identities/PIDs, missing repetitions, bad warmups, accumulated resource budgets and tampered archives. These deliberately injected failures are labeled synthetic tests and are not presented as failures of any real SDK. Real-adapter tests also reject the same corrupted values/counts for every SDK.

Shared invalid-request checks validate the benchmark request contract. They do not establish that every native SDK binder independently diagnoses the same bad input; no native error-handling capability is credited from those precondition checks.

## Limits and next gates

All evidence remains `publication_eligible: false`. These are observed engineering CI environments, not sealed dedicated study hosts. No global SDK position, speed winner, chemistry/ML utility or general simulation capacity follows from these passes. Independent review, sealed environments and complete large-instance ten-block campaigns remain necessary before a qualified P1a performance study. Missing/failed results in future runs must be retained under the same rules, without SDK-specific thresholds or retries.
