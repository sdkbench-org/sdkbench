# Supervised external-program input preparation

Status: synthetic preparation conformance. The seven frozen external program
bodies have not been read. This command prepares a common bundle; it does not
run participants, admit a measurement host, complete a novelty audit or authorize
an execution study. Freeze the final preparation/harness revision and complete
execution/replay budgets publicly before inspecting that population.

## Existing boundaries and bounded workflow

`candidates.external_bundle` combines the admitted
[converter](COMPILER_EXTERNAL_QASM_PREPARATION.md), existing P0 `run_command`
Linux cgroup/seccomp supervisor and existing `Bundle`. It introduces no parser,
evaluator, reference engine, participant adapter, execution profile, threshold
or resource-control implementation. Maintained parsers remain optional source
preparation dependencies; all four participants receive identical converted
operation lists. A source refusal never manufactures a participant result.

The population manifest supplies the complete original path/size/Git-blob census,
topologies, intended participant workflows and original LICENSE/NOTICE hashes.
Verify and retain those notices verbatim before preparing inputs. Check source
paths remain under the supplied root, enforce the 1 MiB source bound, and verify
exact Git-blob identity before conversion. Every attempted original source is
retained. Modified source, missing files, parsing/conformance refusal, dependency
failure, process crash, timeout, OOM and unavailable isolation remain distinct
raw diagnostics. No replacement input or retry occurs.

Each source gets a separate fresh worker under the existing supervisor: 300
seconds, one selected CPU/thread, 16 GiB aggregate cgroup memory, no swap or
network, default bounded stdout/files/tasks and descendant cleanup. Seven source
attempts therefore have a 2100-second conversion ceiling, excluding operator
setup and bundle assembly. The final execution declaration must additionally
bound all outer preparation, novelty audit, host qualification and replay work;
this limit is not permission to start without sufficient reserved time.

The worker calls only source conversion/conformance. Retain each request, exact
original, conversion response and raw supervisor observation, including stderr
and failed status. Preparation environment dependencies must actually be
installed in the selected interpreter; the worker inherits only the source path
and the supervisor's controlled environment. Record the interpreter, dependency
lock and import origins separately in the final freeze.

For every admitted source, make both deterministic line and two-row grid tasks,
including all idle wires and ordered operands. Copy the width-specific W03 case,
acceptance, complete execution profile, memory/wall limits and three probe
preparations unchanged. Only task identity, input operations and explicit target
edges differ. The existing W03 evaluator recomputes operators/output states from
this common input; preparation observations never substitute for its verdict.
No optimal routing reference or algorithmic/scientific validity claim is added.

`preparation.json` accounts for every intended source/target/workflow row,
including refused sources. Each row says participant execution has not started.
The runnable bundle contains only admitted inputs; its case count must never be
used as the complete intended denominator. With zero admitted inputs, retain the
empty bundle and all refusal records, and do not run a campaign or report a
passing qualification. An interrupted parent leaves partial source/request files
and, after each completed decision, an explicitly incomplete preparation record.
It is not a complete attempt. Existing output directories are never reused.

## Operator command

In a Linux preparation environment with the declared native parsers and their
optional dependencies, a verified external source checkout and delegated cgroup:

```sh
PYTHONPATH=src python -m sdkbench.candidates.external_bundle \
  --base docs/implementation \
  --population docs/analysis/COMPILER_EXTERNAL_PROGRAM_POPULATION_20261123.json \
  --sources /data/verified-qasmbench-source \
  --output /data/new-external-preparation \
  --cpu 96 --cgroup-parent /sys/fs/cgroup/DELEGATED_SUBTREE
```

Expected: all seven input decisions and 56 intended workflow rows are retained;
both targets for each admitted input load through the existing verified Bundle.
There is no guarantee that any particular source is supported or admitted.
Keep the entire preparation root, including verbatim LICENSE/NOTICE, with every
redistributed original or derived fixture archive. Do not distribute the nested
bundle alone without those required materials. Preserve custom external license
terms; the preparation command does not relicense sources under SDKBench's license.

After novelty auditing and a separate public execution freeze, the existing
candidate CLI can consume the explicit `--bundle` path. No campaign command is
invoked automatically. Publication eligibility remains false.

## Synthetic conformance

```sh
PYTHONPATH=src python -m pytest tests/test_external_bundle_preparation.py \
  tests/test_external_qasm_preparation.py -q
```

The first focused preparation/converter/resource-replay/P0 run passed 167 tests
in 46.00 seconds. Tests use freshly written synthetic source text and synthetic license notices,
never selected external programs. They check Bell-program full-operator semantics
through the unchanged W03 evaluator, line/grid construction, exact acceptance and
probe preservation, all intended denominator rows, dynamic refusal, source/notice
identity failures, missing cgroup controls, timeout/OOM/process/output/isolation
failures and refusal to reuse an output directory. The worker CLI also runs in a real subprocess for both conversion and refusal.
The outer supervisor is a test double here; real Linux control behavior remains the existing resource
positive/negative suite, and a real supervised native-preparation smoke check is
still required before external input admission. Native parser tests skip when
optional dependencies are absent; skips do not establish native conformance.

The final preparation-only run passed thirteen tests in 2.61 seconds, including
the direct worker subprocess, path-escape and malformed-response controls added
after the combined run. No external source bodies or participant outcomes were
used. Full exact-head CI and real Linux supervised preparation remain pending.

Final combined verification after the incomplete-payload control: 172 tests
passed in 47.88 seconds (preparation, converter, existing resource replay and P0
evaluators). No full repository-suite pass is claimed.
