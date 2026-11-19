# Compiler candidate resource replay

Independent replay must reject evidence that contradicts the execution policy,
even when a modified campaign has been resealed with internally consistent
file hashes. A hash manifest detects changes relative to that manifest; it
does not make the manifest an independent attestation.

## Enforced consistency checks

For every retained supervised execution, replay compares all declared limits
with the existing `Limits.for_case` policy: memory, output, file size, process
tasks and CPU, with a positive wall limit no greater than the frozen case cap.
The wall limit may be smaller because earlier blocks consumed part of the
case budget. Limit types, CPU affinity and the existing network-isolation
requirement are checked without importing a participant SDK.

Accepted blocks additionally require an integer zero process return code and
a positive integer kernel memory peak. Missing, boolean or invalid execution
measurements cannot become accepted resource evidence. A recorded execution
elapsed time must be finite and nonnegative. An accepted case cannot have a
sum of supervised block elapsed times larger than its frozen cumulative cap.

The summed execution time is only a lower bound on total case cost. The actual
runner also charges admission, serialization and validation work through its
existing `ActiveCaseBudget`. Replay does not reconstruct unrecorded parent
overhead, infer a wall-time speedup, or independently attest kernel controls.
It checks consistency of retained evidence; host qualification and independent
attestation remain separate. Failed cases stay in the report and denominator.

No resource cap, acceptance tolerance, SDK option, task fixture, reference or
measurement count is changed. All participants use the same checks.

## Reproduce the checks

```bash
PYTHONPATH=src python -m pytest tests/test_candidate_resource_replay.py -q
PYTHONPATH=src python -m sdkbench.candidates.cli replay \
  --directory candidate-evidence/campaign \
  --bundle candidate-evidence/preparation/cohort
```

Valid complete evidence replays normally. Contradictory evidence raises a
contract error rather than being reported as a successful case. The focused
tests retain a complete synthetic campaign, then alter and reseal individual
limits, process results, measurements or cumulative elapsed time. Before the
fix, the altered-output-limit regression was accepted; after the fix it must
be rejected. Synthetic campaigns are protocol tests, not SDK measurements.
