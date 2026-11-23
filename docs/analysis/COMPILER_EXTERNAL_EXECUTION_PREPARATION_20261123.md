# Prospective external execution preparation

The [prepared manifest](COMPILER_EXTERNAL_EXECUTION_PREPARATION_20261123.json)
binds the frozen converter/audit, admitted common bundle, all intended rows,
exact candidate wheels, new registrations, unchanged compiler configurations,
installed dependencies and preliminary host/control observations. It is not the
final execution freeze: `ci_receipt_sha256` is null and participant execution is
prohibited until the exact frozen harness has passed all fourteen required checks.
Publish a final manifest bound to that receipt before the first participant
outcome. Do not treat this pending record as host or benchmark certification.

All four new registrations successfully reverified installed wheel contents,
package/import identities, comparator metadata, dependencies and compiler options
against the retained historical registrations. Only the declared harness identity
changed. The installed dependency inventory hash is
`e67b99c5a9eaebb5da811f3014d515c853305d6bfc5321196c29afdd29ba52b6`.
This hashes canonical installed name/version/RECORD entries; the separately
reported requirements-text hash identifies a different artifact. Neither hash
is a sealed-image or independent build attestation.

A file comparison found all 49 existing SDKBench Python files unchanged from the
historical measured harness. The only additions are `external_qasm.py`,
`external_bundle.py` and `exposure.py`. Participant adapters, P0/P1a/P1b semantics,
acceptance, execution, replay and resource-control implementation are unchanged.

The sixteen study-host CI runner label sets were retained before replacing their
custom scheduling labels with a study reservation label. The one existing active
job finished naturally; no job, process, container, machine or service was stopped.
All original label sets must be restored on completion, timeout or abandonment
of this attempt. This is still the original reservation ending
`2026-11-24T05:36:41Z`, not a new reservation or an extension.

Fresh host-local controls passed: fifteen real Linux supervisor positive/negative
tests in 4.73 seconds and ten frozen native adapter checks in 12.00 seconds,
with fifty other native scenarios explicitly deselected. All control cgroups were
removed. A five-second observation found zero busy ticks on CPU 96 and sibling
288, and no foreign CI workers. The raw host/environment inventories remain
private; the manifest retains their hashes. Repeat baseline/idleness and input
identity checks immediately before participant execution.

The staged execution driver reuses the previously reviewed phase heartbeat,
resource observation and owned-descendant cleanup helper, bound by its SHA-256.
It enforces one fresh campaign directory, exact source/input/registration hashes,
the CI receipt, latest admission time, whole-case ceilings, a 50400-second outer
campaign ceiling and 10800-second producer-free replay ceiling. The existing
numerical reporting tool is separately bound and receives the declared
900-second summary ceiling, including its own independent replay. A summary
timeout remains incomplete reporting; unused phase time never extends it. Failed participant
outcomes are retained and still replayed; an interrupted process is never rerun
as a complete successful study. Its final host comparison preserves OS-package,
clock/topology baseline changes and any remaining worker cgroups. The final
manifest must bind the exact driver before use. Driver syntax was checked; it
has not executed the external participant campaign.

The first test-staging command extracted the verified frozen tests successfully
but its summary then queried a closed `TarFile` and returned an error. The files
were inspected in place and reused; staging was not repeated. No harness runtime
source was modified. This diagnostic did not execute a participant or alter a
measurement outcome.

No external SDK performance, semantic acceptance, ranking or novelty claim is
made by this preparation. Input admission and limited exposure observations
remain those recorded in the preceding documents. Complete exact-head CI and
publish the final outcome-independent manifest before measuring, or retain this
as incomplete preparation and restore the scheduling labels.
