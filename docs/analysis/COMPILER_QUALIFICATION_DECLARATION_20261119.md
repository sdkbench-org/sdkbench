# Native compiler qualification declaration

Declared on 2026-11-19 before either prospective application campaign has been
dispatched. This document records intended execution of the existing
[matched-layout application protocol](COMPILER_APPLICATION_CAMPAIGN.md); it
changes no task, reference, adapter, tolerance, resource limit or analysis rule.
It is an auditable repository declaration, not independent timestamp attestation.

## Question and intended executions

Assess the integrated FlagQuantum native compiler alongside Qiskit 2.6.2 and
Cirq 1.7.0 on the preregistered quantum application cohort. No participant is
presumed to be superior. Gate count, dependency depth, whole-workflow time,
process memory and failures answer different questions and remain separate.

Run both existing profiles, retaining both outcomes:

| Profile | FlagQuantum workflow | Comparison scope |
| --- | --- | --- |
| `ordinary` | `flagquantum-ordinary-restored` | Ordinary compiler workflow with identity output placement restored |
| `target-artifact` | `flagquantum-target-artifact` | Target-aware workflow including target validation, artifact construction and serialization |

Both profiles retain `qiskit-transpile-restored` and
`cirq-route-cz-restored`. Each uses all 30 selected cases: five application
families, widths 6/8/12, and line/grid targets. All 90 case/participant pairs,
900 process blocks, 2,700 measurements and 1,800 warmups belong in each complete
campaign. Unsupported, timeout, memory, isolation and semantic failures remain
in its coverage denominator. These counts are expected scope, not results.

## Source selection before the draw

Select one immutable FlagQuantum commit reachable from main containing the
integrated routing recovery, relative scorer, bounded routing trials, bounded
layer lookahead and native CZ local cleanup. The corresponding changes are
FlagQuantum PRs #1227, #1232, #1233, #1234 and #1229. Required CI must pass before
the final candidate is admitted. A passing older candidate or local rehearsal
does not substitute for those integration requirements.

Record that full commit and the integrated SDKBench workflow commit before
dispatch. Both profiles must use the same compiler and harness revisions.
Freeze actual built wheel identities, installed dependencies, registrations and
environment through the existing preparation workflow before requesting entropy.
The current harness implementation baseline is
`9c4edb83248c970de339418ab1f70d28791aaf7b`; this declaration adds no execution code.

Do not choose the source revision, compiler options or profile using campaign
outcomes. A necessary harness or compiler repair must be recorded explicitly.
If a campaign has already drawn cases, retain that campaign and its failures;
any later study requires a separate declaration and must not replace its result.

## Execution and failure handling

Dispatch `compiler-applications.yml` once with `workflow_profile=ordinary` and
once with `workflow_profile=target-artifact`, using the selected full compiler
commit. The existing immutable-commit and main-reachability checks apply.
Do not rerun a campaign's GitHub job attempt: the workflow refuses repeated
attempts before drawing. Do not delete a preparation directory or search for a
different nonce.

Each profile independently freezes and draws its cohort once. Its cases are
therefore not matched to the other profile's cases. Do not divide results across
these campaigns, choose the better FlagQuantum profile per case, or attribute
between-campaign differences to one compiler pass. The existing inspected
development probes remain separate from prospective evidence.

Retain the existing one-CPU/one-thread, 16 GiB process limit, ten blocks, two
warmups, three measurements, case budgets and 120-second per-compilation limit.
The 270-minute measurement step and 360-minute job limit also remain unchanged.
If interrupted, retain all partial artifacts and report the campaign as
incomplete. Unavailable kernel isolation must fail closed.

## Acceptance and reporting

Independent replay must verify the complete campaign and its retained execution
policy before descriptive comparisons are admitted. A successful build,
uploaded artifact, process exit or semantic-only test is insufficient. Keep
source archives, wheel/build evidence, requirements, registrations,
freeze/draw/selection records, references, raw warmups and measurements,
supervisor evidence, failures, replay and comparisons.

Publish separate reports for the two declared profiles. Report all cases and
all three unordered participant pairs. Accepted-pair ratios require both full
cases to pass; partial passing blocks do not rescue a failed case. Keep the
existing ten-block descriptive variation, not a confidence interval or
significance claim. No across-case winner or global SDK ranking is calculated.
Target-artifact timing includes the extra end-to-end artifact work and must not
be described as pure compiler timing.

Six-qubit cases use complete-operator validation. Widths 8/12 retain their
three-probe semantic scope. Neither a prospective draw nor a passing campaign
upgrades that scope or establishes hardware fidelity. Publication eligibility
remains false pending the protocol's separate host qualification, independent
attestation and review requirements.

Report unresolved product gaps, regressions, unsupported cases, incomplete
campaigns and negative results alongside improvements. There is no requirement
that FlagQuantum win for this study to produce a useful result.
