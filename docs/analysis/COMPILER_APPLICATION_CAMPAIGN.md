# Matched-layout application campaign

Status: execution workflow and preparation checks implemented. No campaign
result or publication qualification is claimed. This is a preregistered reduced
cohort of the [application protocol](COMPILER_APPLICATION_PROTOCOL.md).

## Selection fixed before execution

The cohort contains all five families (QAOA, Ising, hopping, QFT and repetition),
all three widths (6, 8 and 12), and line/grid targets: 30 cases. Ring and sparse
targets are excluded in advance to bound the first campaign. They remain part
of the full 60-case development bundle and future qualification scope.

Three separately registered workflows participate: `flagquantum-ordinary-restored`,
`qiskit-transpile-restored`, and `cirq-route-cz-restored`. All restore identity
output placement. This control does not isolate synthesis from routing and does
not establish a global SDK ranking. Target-artifact and free-layout workflows
remain separate comparisons and are not substituted into this cohort.

Every selected case retains its fixture/reference bytes, width-specific
acceptance and resource limits from the full bundle. The base frozen W03 bundle,
reference evaluator, historical adapters, compiler seeds, ten process blocks,
two warmups and three measurements per block remain unchanged. Each process gets
one CPU, one numerical thread and 16 GiB under Linux cgroup/seccomp isolation.
The 90 case/registration pairs produce 900 blocks and 2,700 measured records
when complete, plus 1,800 retained warmup records.

The cumulative per-case ceilings sum to 99,000 seconds across the three
registrations; they are worst-case ceilings, not a runtime estimate. An outer
270-minute measurement step and 360-minute job limit bound CI use. If either
interrupts execution, retain the partial evidence and call the campaign
incomplete. Do not shorten case limits, discard difficult cases, or infer a
passing result from a partial manifest.

## Freeze, draw and provenance

The workflow requires a full FlagQuantum source commit already reachable from
`flagos-ai/FlagQuantum` main. It builds that archive, retains its build record and
wheel, and verifies installed bytes. Comparator versions remain Qiskit 2.6.2 and
Cirq 1.7.0 with retained wheels and PyPI metadata. The measurement environment,
dependency inventory and each actual registration are recorded before drawing.
Native adapter conformance is checked before registration and before the draw.

`tools/prepare_compiler_applications.py` then:

1. Verifies all three live registrations and their exact matched-layout choices.
2. Exclusively creates the output directory and writes `freeze.json`, containing
   the registrations, harness revision/source identity, base bundle, cohort,
   outer budget, timestamp and workflow identity.
3. Draws exactly 32 bytes from the OS-backed `secrets` API and writes `draw.json`
   bound to the freeze digest. No user-selected or searched nonce is accepted.
4. Retains the full 60-case generated bundle and a separately hashed 30-case
   selection, without changing any selected acceptance/resource object.
5. Writes `selection.json`, binding freeze, draw and both bundle identities.

These are auditable local event records, not an independent timestamp or build
attestation. Generated bundles retain their development label; the draw record
alone cannot establish publication eligibility. The campaign and independent
replay continue to report publication eligibility as false.

Existing preparation directories are refused without requesting more entropy.
Repeated GitHub job attempts are refused before the build/draw. A failed draw
or campaign must remain visible; investigation must not silently retry with a
fresh nonce. Any separately declared later campaign must retain the earlier
failure and cannot replace it in reported results.

## Execute and inspect

Dispatch `.github/workflows/compiler-applications.yml` with the integrated
40-character compiler commit. The workflow itself must be merged before the
production run, so its checkout is an immutable integrated harness revision.
No automatic run is triggered by pushing this workflow.

The `compiler-application-evidence` artifact retains builds, registrations,
requirements, both bundles, freeze/draw/selection records, warmups, individual
results, supervisor limits, failures, campaign output and independent replay.
A missing complete manifest is a failed/incomplete campaign. A completed process
or uploaded artifact is insufficient: replay must verify all 900 blocks, source
identities, semantic decisions and the unchanged resource controls.

Report full-CZ count, common dependency depth, wall time, peak memory, timeout,
OOM, unsupported and correctness failures per case and registration. Preserve
per-block data and uncertainty; never combine failed cases into a winners-only
aggregate. Source widths 8/12 retain three-probe-only semantic scope; they do not
become full-operator proofs because the draw was prospective.

## Local preparation checks

```bash
PYTHONPATH=src python -m pytest tests/test_prepare_compiler_applications.py \
  tests/test_candidate_application_bundle.py tests/test_candidate_runner.py -q
```

The tests cover freeze-before-entropy ordering, registration rejection, refusal
to redraw, complete cohort shape and unchanged selected artifacts. They do not
replace native Linux execution, independent replay or comparative analysis.

Local validation: eight preparation/bundle tests pass; Ruff and YAML/shell
syntax checks pass. The broader local suite exceeded its 300-second budget and
a runner-inclusive subset exceeded 180 seconds; neither is reported as passing.
Full Linux CI and the actual campaign remain required.

## Descriptive paired comparisons

After the campaign completes, run:

```bash
PYTHONPATH=src python tools/compare_compiler_applications.py \
  --directory candidate-evidence/campaign \
  --bundle candidate-evidence/preparation/cohort \
  --output candidate-evidence/comparisons.json
```

The command invokes independent replay through the existing summary tool before
comparison. Every case and every matched-restoration workflow remains in the
coverage denominator. All three unordered participant pairs are emitted for
each case, with explicit numerator/denominator names and original statuses.
Neither participant receives a performance ratio if either complete case failed,
even when some measured records passed. No across-case winner is calculated.

For a fully accepted pair, full-CZ and dependency-depth ratios divide the
independently recomputed record medians. Timing ratios pair identical block
indices and divide each block's three-measurement median. Memory ratios pair
whole-process kernel peaks by block. The report retains count, median, range
and inclusive quartiles of the ten ratios. These are descriptive variation,
not confidence intervals, significance tests or proof of a speedup. Zero,
missing and nonfinite inputs produce an undefined ratio without deleting the
case or selecting only convenient blocks. Memory includes import, warmup and
export costs. A lower ratio favors the named numerator only for that metric
and case; correctness, resource failures and other metrics remain separate.

The output binds the recomputed summary digest and independent replay report.
It remains publication-ineligible and supports no global SDK ranking. The
eight focused report tests cover exact ratios, immutable input, failures,
undefined values, refused incomplete/mixed comparisons and CLI replay of a
sealed synthetic campaign with all three participants denied access. These
synthetic results are not measurements of any SDK.
