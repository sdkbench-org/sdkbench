# Exact external-program exposure audit

This is preparation evidence, not a compiler benchmark or novelty certificate.
The population and converter remain frozen separately. Do not tune a compiler
against this audit's selected programs and later call them unseen inputs.

`candidates.exposure` compares every retained original source byte hash and each
admitted converted operation fingerprint with explicit historical directories.
It uses the existing canonical JSON hashing and bounded JSON reader. It imports
no participant SDK, numerical reference, or compiler. Extract historical evidence
archives safely before this command, retaining their archive identities and
extraction manifests separately. Supply both repositories' checked-in evidence,
available historical campaign directories, and extracted retained archives;
record unavailable sources. Do not silently limit the search to convenient roots.

```sh
PYTHONPATH=src python -m sdkbench.candidates.exposure \
  --preparation /data/external-preparation \
  --history /data/frozen-sdkbench-history \
  --history /data/frozen-flagquantum-history \
  --history /data/extracted-historical-evidence \
  --output /data/exposure-audit.json
```

Run under the separately declared outer audit timeout. Each input file is
bounded at 32 MiB. Output creation is exclusive, so an existing result is never
replaced. The command verifies the preparation's source Git blobs and admitted
conversion hashes before comparing them. Its inventory records every readable
historical file's path, byte count and SHA-256. Git object databases are excluded;
commits and historical archives must be materialized explicitly. Symlinks are
not followed. Missing roots, malformed/oversized JSON, unrecognized operation
representations and raw-only archive/QASM inputs are retained as coverage gaps.

For JSON objects, the recognized representations are the existing fixture's
`n_qubits`/`operations` and FlagQuantum IR's `n_wires`/`instructions`. Recursive
object traversal finds nested records. Ordered scalar numeric gates normalize
to the fixture spelling; integer/float spellings of the same angle compare
identically. Width, idle wires, opcode, operation order, angle and operand order
are retained. Symbolic, annotated, matrix-valued or unknown operations are gaps.
The algorithm does not rewrite gates, wrap angles, cancel identities, remap
wires, synthesize circuits, or test semantic equivalence. JSON-encoded strings,
logs, source code, notebooks, JSONL and other non-JSON material receive only raw
file-byte comparison; the report's coverage statement records this limitation.
A raw source embedded within another file will not be detected by file hashing.

Every exact raw or ordered-operation match is a known-exposure control, with all
matching paths retained. A source without a match is labeled only
`no-exact-match-in-audited-material`, including when roots are unavailable.
`novelty_certified` is always false. No match establishes neither algorithmic
novelty nor the absence of prior developer knowledge. Review recorded gaps and
other exposure evidence before any stronger prospective holdout description.
No source is removed, replaced or assigned a participant failure by this tool.

Synthetic tests cover raw/nested/IR matches, reversed control and target, operation
order, idle width, malformed/annotated/symbolic operations, missing roots,
compressed evidence, symlinks, inaccessible subtrees, absent refused-source bytes,
tampered preparation and exclusive CLI output.
No selected external program body is used in development or test fixtures.

```sh
PYTHONPATH=src python -m pytest tests/test_external_exposure.py -q
```

The final focused run passed 58 tests in 13.32 seconds across the converter,
supervised preparation and exposure audit, using the optional native parsers.
The exposure-only suite contains 23 synthetic cases. This does not establish
full repository CI, actual-population admission or compiler performance.
