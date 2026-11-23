# Results storage

The private `sdkbench-org/sdkbench-results` repository is the storage destination
for new experiment data. This engine remains responsible for task definitions,
protocols, adapters, resource supervision and semantic evaluation. The private
`sdkbench-org/sdkbench-web` repository maintains presentation code and pinned
offline snapshots; its website remains locally deployed.

The initial storage import covers only the existing ordinary compiler cohort
`compiler-ordinary-44587635615`: 30 instances, three participant workflows, 900
blocks, 2,700 measured records and 1,800 warmup records. It is a historical import,
not a new experiment or semantic replay. Publication eligibility remains false.
Other historical datasets have not been migrated, and no historical evidence is
removed or rewritten here. The current website importer still pins this engine's
evidence rather than reading the results repository.

## Storage contract

Each sealed run has a unique ID and preserves engine source/execution revisions,
protocol revision, bundle/input/reference/configuration/environment identities,
participant registrations and versions, execution and semantic statuses, host
limitations and publication eligibility. Its storage schema is separately
versioned and does not replace the engine's result contract.

Small reviewable files are committed to Git: manifest, observed environments,
per-repetition measurement projections, unchanged source summary, analysis,
provenance and archive indices. The initial records projection preserves all
upstream record fields except payload, plus compile_wall_seconds if present.
Full payloads, original requests/responses and supervision evidence remain in the
original content-addressed archive outside Git. Every projection identifies its
archive member/JSON Pointer and canonical record/payload hashes. Warmups and
measured records are distinct. Missing and failed results are retained, not zeroed.

Complete large archives, binaries and performance traces are stored outside Git,
with exact sizes, SHA-256 digests, source locations and retention/backup facts in
the run's artifact index. The initial local archive has no verified independent
backup. The original build binaries and source packages have not been copied;
the upstream artifact's recorded expiry is 2027-02-17T18:25:28Z. Do not equate this
storage setup with full long-term preservation of all build artifacts.

Sealed runs are append-only by policy. Corrections receive a new ID, reference the
superseded run and explain the reason; original measurements remain available.
Storage checksum/projection validation does not replay semantic evaluation,
qualify a host or establish independent scientific review. It is not a signature.

Future website imports must pin the results-repository commit, run ID, manifest
and data hashes, preserve original engine provenance and retain all eligibility
limits. No cross-cohort pooling, favorable per-case workflow selection or implied
global SDK ranking follows from this separation. Private storage does not make
evidence externally reviewable; conclusions shared outside the project need an
explicitly selected accompanying evidence package.
