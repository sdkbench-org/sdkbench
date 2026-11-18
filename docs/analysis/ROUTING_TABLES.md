# Routing configuration data tables

These are gate-count diagnostics under the declared [protocol](ROUTING_PROTOCOL.md), not speed scores or best-SDK rankings. Each Qiskit frozen-instance cell is the range across the ten fixed compiler seeds; deterministic configurations have one outcome. Every cell passed the same semantic rules. See [the analysis](FLAGQUANTUM_ROUTING_ANALYSIS.md) for interpretation, final-layout differences and source scope.

## All configuration arms: full-CZ counts

| Configuration ID | LINE-06 | GRID-08 | LINE-12 |
| --- | ---: | ---: | ---: |
| fq-default | 228 | 218 | 1092 |
| fq-restore_after_each_gate-restored-post | 228 | 218 | 1092 |
| fq-restore_after_each_gate-free-plain | 228 | 218 | 1092 |
| fq-restore_after_each_gate-free-post | 228 | 218 | 1092 |
| fq-persistent_layout-restored-plain | 294 | 212 | 1194 |
| fq-persistent_layout-restored-post | 294 | 212 | 1194 |
| fq-persistent_layout-free-plain | 165 | 125 | 621 |
| fq-persistent_layout-free-post | 165 | 125 | 621 |
| fq-auto-restored-plain | 228 | 218 | 1092 |
| fq-auto-restored-post | 228 | 218 | 1092 |
| fq-auto-free-plain | 228 | 218 | 1092 |
| fq-auto-free-post | 228 | 218 | 1092 |
| fq-sabre-restored-plain | 138 | 146 | 438 |
| fq-sabre-restored-post | 138 | 144 | 432 |
| fq-sabre-free-plain | 108 | 98 | 381 |
| fq-sabre-free-post | 108 | 96 | 375 |
| fq-default-level0 | 228 | 218 | 1092 |
| fq-default-level1 | 228 | 218 | 1092 |
| fq-default-rotation-basis | 228 | 218 | 1092 |
| qiskit-default | 68 | 85 | 339–348 |
| qiskit-sabre | 68 | 85 | 339–348 |
| qiskit-basic | 165 | 159 | 587 |
| qiskit-lookahead | 79 | 85 | 418 |
| qiskit-default-level0 | 87–102 | 92–101 | 426–441 |
| cirq-default | 68 | 84 | 360 |

## Microprobe full-CZ counts

| Input | FQ default | FQ default + post-basis | FQ SABRE/free | Qiskit default | Cirq default |
| --- | ---: | ---: | ---: | ---: | ---: |
| MICRO-LOCAL-CX | 1 | 1 | 1 | 1 | 1 |
| MICRO-LOCAL-CANCEL | 0 | 0 | 0 | 0 | 0 |
| MICRO-LOCAL-SWAP | 3 | 3 | 3 | 3 | 3 |
| MICRO-REMOTE-REUSE | 50 | 50 | 14 | 14 | 14 |
| MICRO-SWAP-CX-SAME | 4 | 2 | 4 | 1 | 2 |
| MICRO-SWAP-CX-REVERSED | 4 | 4 | 4 | 1 | 2 |
