# Target-artifact application results (2026-11-20)

90/90 complete case/participant pairs passed this engineering campaign. All 30 cases and all three participant pairings are retained. This is a bounded restored-layout study, not a global SDK ranking or a publication-qualified performance claim.

The study follows the [prospective declaration](COMPILER_QUALIFICATION_DECLARATION_20261119.md) and [unchanged matched-layout protocol](COMPILER_APPLICATION_CAMPAIGN.md). The two declared profiles draw independent cohorts; do not combine their results, choose the better FlagQuantum profile per case, divide their metrics, or attribute between-profile differences to one compiler pass.

## Immutable execution and evidence

- [Original workflow run](https://github.com/sdkbench-org/sdkbench/actions/runs/44587642527), attempt 1; no campaign rerun or redraw.
- FlagQuantum source: `858df9dbd5ba964e8e59b3383304547710a1dee5`; SDKBench harness: `9e3992d14342601662443b6720dd6757905c3f3b`.
- Qiskit 2.6.2 and Cirq 1.7.0; actual wheels, build files and registrations were frozen before drawing.
- Freeze timestamp: `2026-11-19T18:28:31.076689+00:00`; draw timestamp: `2026-11-19T18:28:31.080757+00:00`. These are local event records, not independent timestamp attestations.
- [Evidence index](evidence/compiler-target-artifact-44587642527-index.json), [complete raw campaign archive](evidence/compiler-target-artifact-44587642527.tar.xz), [local verification](evidence/compiler-target-artifact-44587642527-verification.json), [layout/resource audit](evidence/compiler-target-artifact-44587642527-layout-resources.json), [machine-readable summary](evidence/compiler-target-artifact-44587642527-summary.json.gz) and [all 90 paired comparisons](evidence/compiler-target-artifact-44587642527-comparisons.json).

The retained archive contains 4,407 original files, including every one of the 4,205 campaign manifest entries; every retained member was hash-verified. It preserves requests, responses, warmups, measurements, supervisor evidence and failures unchanged. The index pins the original ZIP, source archive and wheel hashes. Build binaries and extracted compiler sources remain in the original artifact, expiring `2027-02-17T18:25:30Z`; they are not duplicated in Git. This retention limit must not be hidden.

Independent local replay denied imports of FlagQuantum, Qiskit and Cirq. It verified 900 blocks and 2,700 measured records, reproduced the hosted case decisions, and matched every hosted pair metric and coverage entry. Preparation was regenerated using the retained nonce without drawing again. No acceptance, resource ceiling or adapter was changed.

The local and hosted summary digests differ only in independently recomputed maximum semantic-error values. Substituting the retained hosted error values, while leaving every other local summary field unchanged, reconstructs the exact hosted digest; see the [reconciliation proof](evidence/compiler-target-artifact-44587642527-summary-reconciliation.json). Both error sets remain retained under the unchanged acceptance threshold. All case decisions, gate/depth metrics and timing/memory comparisons match. The original local digest is not rewritten.

There are 72 differing maximum-error fields. All remaining local summary fields reconstruct the hosted digest unchanged. The successful [local audit log](evidence/compiler-target-artifact-44587642527-local-audit.log) and [audit entry](source-probes/compiler-qualification-audit-20261120.py.txt) are retained. The original ZIP transfer reached its 600-second download limit; a verified HTTP 206 byte-range continuation completed the same file. An alternate transport failed TLS before receiving data. Initial extraction exhausted local disk space; only the completed ordinary campaign's reproducible temporary extraction was removed, after verifying its retained full ZIP and raw archive. Final target extraction and all checks succeeded. No measured compilation or campaign draw was repeated.

The preregistered evaluator checks the hash and presence of serialized artifact sidecars; its numerical acceptance applies to the normalized operation payload. A separate [post-campaign QASM consistency audit](evidence/compiler-target-artifact-44587642527-serialized-qasm.json) additionally checks all 1,500 FlagQuantum artifacts: payload hashes, literal RX/RZ/CZ instructions in exact order, numeric angles, register widths and identity terminal measurement mapping match the independently accepted payloads. Five malformed negative controls are rejected and a changed angle is detected. The [retained audit entry](source-probes/compiler-serialized-qasm-audit-20261120.py.txt) imports no participant SDK. This supplemental check does not change campaign admission, implement general QASM conformance, reimplement artifact identity/provenance contracts, or upgrade three-probe numerical assurance.

## Applicability and measurement boundary

Five application families (QAOA, Ising evolution, hopping, QFT and repetition), widths 6/8/12, and line/grid targets produce 30 cases. Ring/sparse targets and the broader SDK task catalog remain outside this campaign. No GPU, QPU, distributed execution, hardware-fidelity or global SDK capability claim follows from these CPU compiler results.

Measurement host: `AMD EPYC 9V74 80-Core Processor`; `Linux-7.0.0-1017-azure-x86_64-with-glibc2.39`; Python `3.12.14`. Each supervised process was pinned to one CPU with one numerical thread, 16 GiB memory, socket/io-uring denial, two warmups and three measured compilations. Ten blocks are required per case. A 120-second per-compilation ceiling, the frozen width-specific cumulative case ceilings, the 270-minute measurement step and the 360-minute job ceiling remain unchanged.

All three registrations require identity initial and final placement, verified in every retained warmup and measurement. FlagQuantum restores layout inside its native target-artifact compiler. Qiskit and Cirq use the same timed external spanning-tree token-restoration policy. The delivered layout is matched; restoration algorithms and integration points are not identical. Quality and time include these respective obligations and cannot isolate routing, layout search or synthesis individually.

The target family is full CZ plus arbitrary one-qubit unitaries on the declared undirected edges, without ancillas. Independent semantic acceptance uses absolute error at most 1e-8, zero relative tolerance, normalization error at most 1e-10 and zero target violations. Six-qubit cases validate the complete operator up to one global phase. Widths 8/12 validate three complete probe-output states up to a phase per probe; they are not universal equivalence proofs.

FlagQuantum's target-aware workflow includes target validation, automatic eligible CZ block resynthesis, provenance, artifact construction and serialization in timed work. Qiskit and Cirq retain their registered restored compiler workflows. This is an end-to-end target-artifact versus compiler-workflow comparison, not pure compiler or isolated synthesis timing. Exact options and package identities remain in the registrations.

The ordinary campaign ran on a different host and drew a separate cohort. Its numbers are not a controlled baseline for this report. Neither differences between profiles nor SDK-reported native baseline/rewrite counters establish the causal contribution of an individual compiler pass.

## Findings and product gaps

The following examples illustrate distinct trade-offs; the complete tables below retain every case. They are not an across-case score or a selection of a winning SDK. Counts and dependency depths are medians of accepted records; the paired time ratios use the ten matching block indices.

On QFT line-12, FlagQuantum emits 396 CZ operations with two-body dependency depth 137, compared with Qiskit's 426/146 and Cirq's 410/144. The whole-workflow block-median time is 2,838.3 ms for FlagQuantum, 21.984 ms for Qiskit and 476.01 ms for Cirq. The paired FlagQuantum/Qiskit time ratio is 128.36 [126.28, 130.60]. Lower output cost here accompanies a substantial latency cost; the extra artifact work is included, and this measurement does not isolate which stage causes the gap.

On hopping grid-12, FlagQuantum emits 298 CZ operations at depth 202; Qiskit emits median 392 at depth 290, and Cirq emits 438 at depth 331. The observed Qiskit CZ range is 370 to 418, so medians must not be described as one invariant circuit. Whole-workflow block-median times are 1,779.1, 22.355 and 743.69 ms respectively. This is another quality/time trade-off, not evidence that lower CZ count implies faster compilation or better hardware fidelity.

FlagQuantum does not uniformly reduce output cost. On Ising line-8 it emits 128 CZ operations at depth 77, compared with Qiskit's 112/66 and Cirq's 116/63. On QAOA grid-8 all three emit 60 CZ operations, while FlagQuantum's depth is 38 versus 32 for both comparators. These are remaining routing/synthesis-quality gaps on accepted cases; successful semantics do not erase them.

Memory also needs a separate boundary. On QFT line-12 the process-peak medians are 173.45 MiB for FlagQuantum, 81.865 MiB for Qiskit and 159.83 MiB for Cirq. These peaks include imports, warmups and export as well as computation. They cannot establish compiler workspace consumption or attribute the difference to a particular dependency without a separate experiment.

The next product questions are to profile FlagQuantum's existing target-artifact stages, reduce duplicated work behind their current contracts where evidence supports it, and investigate the accepted Ising/QAOA quality gaps on independent development cases. The ordinary workflow's lack of target-aware CZ block optimization remains an explicitly separate product boundary. This campaign provides no old-FlagQuantum control, no isolated pass ablation and no evidence for a global SDK winner. Follow-up changes need their own frozen source and prospective evaluation rather than replacing these results.

## Complete coverage

| Workflow | Accepted complete cases | Other complete-case outcomes | Accepted measured records / expected |
| --- | ---: | --- | ---: |
| `flagquantum-target-artifact` | 30/30 | none | 900/900 |
| `qiskit-transpile-restored` | 30/30 | none | 900/900 |
| `cirq-route-cz-restored` | 30/30 | none | 900/900 |

Retained warmup records: 1800/1,800. Failed warmups, unsupported, timeout, isolation, memory and semantic failures remain in the case denominator. A failed case receives no paired performance ratios, even if some records passed. Conditional diagnostics, if present, remain in the machine-readable summary.

## Every case and participant

CZ count and dependency depth show the median [minimum, maximum] across 30 accepted measured records. Time is milliseconds: the median [Q1, Q3] of ten block medians, each formed from three accepted measurements. Memory is MiB: the median [minimum, maximum] of ten kernel process peaks, including imports, warmups, computation and export. It is not compiler-only workspace. Maximum semantic error below is for measured records. Quartiles describe observed variation, not confidence intervals or statistical significance.

| Case | SDK | Status | Full CZ | Two-body dependency depth | Workflow time, ms | Process peak, MiB | Maximum semantic error |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| `APP-HOPPING-GRID-06` | FlagQuantum | accepted | 82 [82, 82] | 79 [79, 79] | 507.27 [499.71, 517.41] | 156.43 [156.39, 156.44] | 8.6281e-15 |
| `APP-HOPPING-GRID-06` | Qiskit | accepted | 102 [102, 102] | 87 [87, 87] | 9.4204 [9.1053, 9.5171] | 66.625 [66.621, 66.629] | 3.4477e-15 |
| `APP-HOPPING-GRID-06` | Cirq | accepted | 84 [84, 84] | 80 [80, 80] | 169.13 [168.17, 169.88] | 145.73 [145.08, 145.78] | 1.3255e-14 |
| `APP-HOPPING-GRID-08` | FlagQuantum | accepted | 120 [120, 120] | 103 [103, 103] | 765.58 [745.15, 777.45] | 158.83 [158.78, 158.84] | 2.3833e-15 |
| `APP-HOPPING-GRID-08` | Qiskit | accepted | 156 [152, 156] | 128 [119, 128] | 11.824 [11.428, 12.416] | 70.621 [70.617, 70.641] | 3.6408e-15 |
| `APP-HOPPING-GRID-08` | Cirq | accepted | 120 [120, 120] | 103 [103, 103] | 225.25 [223.21, 226.6] | 146.58 [146.57, 146.59] | 2.3995e-14 |
| `APP-HOPPING-GRID-12` | FlagQuantum | accepted | 298 [298, 298] | 202 [202, 202] | 1779.1 [1713.2, 1832] | 167.6 [167.48, 167.65] | 3.4384e-15 |
| `APP-HOPPING-GRID-12` | Qiskit | accepted | 392 [370, 418] | 290 [268, 301] | 22.355 [21.952, 22.58] | 79.73 [78.859, 82.355] | 3.9995e-15 |
| `APP-HOPPING-GRID-12` | Cirq | accepted | 438 [438, 438] | 331 [331, 331] | 743.69 [740.9, 750.54] | 163.06 [163.05, 163.29] | 4.4135e-15 |
| `APP-HOPPING-LINE-06` | FlagQuantum | accepted | 66 [66, 66] | 64 [64, 64] | 429.1 [414.74, 436.99] | 155.62 [155.57, 155.67] | 6.3211e-15 |
| `APP-HOPPING-LINE-06` | Qiskit | accepted | 66 [66, 66] | 64 [64, 64] | 8.3566 [8.2995, 8.6661] | 66.211 [66.207, 66.266] | 3.2414e-15 |
| `APP-HOPPING-LINE-06` | Cirq | accepted | 66 [66, 66] | 64 [64, 64] | 151.85 [151.22, 153.66] | 144.88 [144.87, 144.92] | 6.0556e-15 |
| `APP-HOPPING-LINE-08` | FlagQuantum | accepted | 86 [86, 86] | 80 [80, 80] | 544.96 [529.11, 557.16] | 156.71 [156.68, 156.76] | 1.7626e-15 |
| `APP-HOPPING-LINE-08` | Qiskit | accepted | 86 [86, 86] | 80 [80, 80] | 9.4371 [9.2922, 10.41] | 68.371 [68.367, 68.375] | 3.8767e-15 |
| `APP-HOPPING-LINE-08` | Cirq | accepted | 86 [86, 86] | 80 [80, 80] | 197.47 [196.31, 198.69] | 146.25 [146.23, 146.26] | 2.4711e-14 |
| `APP-HOPPING-LINE-12` | FlagQuantum | accepted | 212 [212, 212] | 168 [168, 168] | 1357.5 [1265.9, 1384.5] | 163.32 [163.23, 163.34] | 2.0596e-15 |
| `APP-HOPPING-LINE-12` | Qiskit | accepted | 212 [212, 212] | 168 [168, 168] | 15.657 [15.081, 16.218] | 72.844 [72.836, 72.848] | 2.0566e-15 |
| `APP-HOPPING-LINE-12` | Cirq | accepted | 212 [212, 212] | 168 [168, 168] | 482.73 [481.84, 492.58] | 151.56 [151.54, 151.57] | 1.8619e-15 |
| `APP-ISING-GRID-06` | FlagQuantum | accepted | 42 [42, 42] | 26 [26, 26] | 198.46 [197.71, 200.81] | 154.03 [154, 154.11] | 7.0758e-15 |
| `APP-ISING-GRID-06` | Qiskit | accepted | 48 [48, 48] | 32 [32, 32] | 6.7329 [6.6747, 6.8685] | 65.133 [65.121, 65.137] | 2.4526e-15 |
| `APP-ISING-GRID-06` | Cirq | accepted | 52 [52, 52] | 42 [42, 42] | 71.082 [70.579, 72.004] | 143.53 [143.49, 143.58] | 9.3602e-15 |
| `APP-ISING-GRID-08` | FlagQuantum | accepted | 52 [52, 52] | 26 [26, 26] | 285.83 [284.31, 289.11] | 154.92 [154.88, 154.96] | 1.2702e-15 |
| `APP-ISING-GRID-08` | Qiskit | accepted | 60 [60, 60] | 29 [29, 29] | 8.0273 [7.6393, 8.3027] | 65.715 [65.664, 65.719] | 1.8488e-15 |
| `APP-ISING-GRID-08` | Cirq | accepted | 60 [60, 60] | 29 [29, 29] | 80.815 [80.491, 82.009] | 143.91 [143.87, 143.93] | 2.6452e-15 |
| `APP-ISING-GRID-12` | FlagQuantum | accepted | 194 [194, 194] | 97 [97, 97] | 1142.1 [1105.3, 1158.7] | 161.06 [161.02, 161.23] | 2.4856e-15 |
| `APP-ISING-GRID-12` | Qiskit | accepted | 178 [178, 186] | 88 [88, 95] | 12.35 [12.028, 12.948] | 69.76 [69.629, 69.859] | 2.247e-15 |
| `APP-ISING-GRID-12` | Cirq | accepted | 196 [196, 196] | 103 [103, 103] | 226.26 [224.01, 228.73] | 149.33 [149.32, 149.34] | 8.3272e-14 |
| `APP-ISING-LINE-06` | FlagQuantum | accepted | 46 [46, 46] | 26 [26, 26] | 246.38 [244.92, 248.61] | 154.32 [154.31, 154.38] | 7.3277e-15 |
| `APP-ISING-LINE-06` | Qiskit | accepted | 50 [50, 50] | 35 [35, 35] | 6.84 [6.7255, 7.087] | 65.27 [65.215, 65.273] | 3.6002e-15 |
| `APP-ISING-LINE-06` | Cirq | accepted | 64 [64, 64] | 47 [47, 47] | 86.677 [86.313, 87.886] | 144.31 [144.29, 144.37] | 5.9664e-15 |
| `APP-ISING-LINE-08` | FlagQuantum | accepted | 128 [128, 128] | 77 [77, 77] | 684.28 [680.84, 703.45] | 157.99 [157.91, 158.04] | 4.2325e-15 |
| `APP-ISING-LINE-08` | Qiskit | accepted | 112 [112, 126] | 66 [56, 66] | 9.9665 [9.7572, 10.553] | 67.631 [67.621, 67.879] | 2.2848e-15 |
| `APP-ISING-LINE-08` | Cirq | accepted | 116 [116, 116] | 63 [63, 63] | 127.66 [126.6, 128.58] | 146.45 [145.58, 146.48] | 3.1468e-15 |
| `APP-ISING-LINE-12` | FlagQuantum | accepted | 250 [250, 250] | 106 [106, 106] | 1391.7 [1350, 1429.5] | 163.57 [163.45, 163.61] | 2.4403e-15 |
| `APP-ISING-LINE-12` | Qiskit | accepted | 286 [286, 286] | 166 [165, 166] | 15.552 [14.919, 15.832] | 73.373 [73.359, 73.379] | 4.0254e-15 |
| `APP-ISING-LINE-12` | Cirq | accepted | 250 [250, 250] | 114 [114, 114] | 253.99 [251.14, 257.63] | 151.08 [150.84, 151.09] | 3.7951e-15 |
| `APP-QAOA-GRID-06` | FlagQuantum | accepted | 42 [42, 42] | 31 [31, 31] | 188.28 [187.3, 191.82] | 154.42 [154.36, 154.43] | 1.214e-15 |
| `APP-QAOA-GRID-06` | Qiskit | accepted | 42 [42, 42] | 31 [31, 31] | 6.4874 [6.3787, 6.5519] | 64.885 [64.871, 64.887] | 9.2649e-16 |
| `APP-QAOA-GRID-06` | Cirq | accepted | 54 [54, 54] | 31 [31, 31] | 62.75 [61.804, 63.371] | 143.5 [143.47, 143.55] | 1.8094e-15 |
| `APP-QAOA-GRID-08` | FlagQuantum | accepted | 60 [60, 60] | 38 [38, 38] | 356.5 [352.38, 368.85] | 155.14 [155.13, 155.17] | 1.0179e-15 |
| `APP-QAOA-GRID-08` | Qiskit | accepted | 60 [60, 60] | 32 [32, 32] | 7.2685 [7.1528, 7.32] | 65.521 [65.473, 65.527] | 9.9952e-16 |
| `APP-QAOA-GRID-08` | Cirq | accepted | 60 [60, 60] | 32 [32, 32] | 72.196 [71.81, 73.23] | 143.87 [143.86, 143.93] | 1.0855e-15 |
| `APP-QAOA-GRID-12` | FlagQuantum | accepted | 114 [114, 114] | 46 [46, 46] | 648.17 [626.68, 658.96] | 158.22 [158.18, 158.43] | 1.2917e-15 |
| `APP-QAOA-GRID-12` | Qiskit | accepted | 132 [132, 142] | 57 [57, 58] | 9.8169 [9.3727, 10.27] | 68.021 [67.625, 68.055] | 2.3414e-15 |
| `APP-QAOA-GRID-12` | Cirq | accepted | 140 [140, 140] | 63 [63, 63] | 135.86 [135.02, 136.47] | 146.59 [146.58, 146.6] | 2.5569e-15 |
| `APP-QAOA-LINE-06` | FlagQuantum | accepted | 78 [78, 78] | 44 [44, 44] | 366.3 [363.48, 371.65] | 155.67 [155.61, 155.7] | 1.9876e-15 |
| `APP-QAOA-LINE-06` | Qiskit | accepted | 80 [80, 88] | 53 [53, 53] | 7.7098 [7.5659, 8.3083] | 66.539 [66.137, 66.723] | 1.8515e-15 |
| `APP-QAOA-LINE-06` | Cirq | accepted | 82 [82, 82] | 47 [47, 47] | 91.411 [91.025, 91.543] | 145.07 [144.34, 145.09] | 2.9275e-15 |
| `APP-QAOA-LINE-08` | FlagQuantum | accepted | 142 [142, 142] | 83 [83, 83] | 779.96 [759.86, 803.89] | 158.53 [158.42, 158.58] | 2.0839e-15 |
| `APP-QAOA-LINE-08` | Qiskit | accepted | 154 [146, 156] | 77 [69, 84] | 10.444 [10.153, 11.376] | 68.65 [68.625, 68.887] | 3.4986e-15 |
| `APP-QAOA-LINE-08` | Cirq | accepted | 152 [152, 152] | 73 [73, 73] | 160.38 [159.72, 161.38] | 147.59 [147.57, 147.62] | 2.607e-15 |
| `APP-QAOA-LINE-12` | FlagQuantum | accepted | 180 [180, 180] | 65 [65, 65] | 1068.6 [1000.2, 1074.9] | 160.32 [160.19, 160.42] | 1.8077e-15 |
| `APP-QAOA-LINE-12` | Qiskit | accepted | 176 [170, 176] | 65 [65, 68] | 11.725 [11.217, 12.753] | 69.629 [69.375, 69.68] | 2.2022e-15 |
| `APP-QAOA-LINE-12` | Cirq | accepted | 170 [170, 170] | 68 [68, 68] | 188.22 [186.35, 189.79] | 148.59 [148.58, 148.82] | 2.4531e-15 |
| `APP-QFT-GRID-06` | FlagQuantum | accepted | 65 [65, 65] | 48 [48, 48] | 446.94 [435.12, 454.62] | 155.36 [155.29, 155.36] | 1.7745e-15 |
| `APP-QFT-GRID-06` | Qiskit | accepted | 81 [81, 83] | 56 [56, 58] | 8.0312 [7.7088, 8.2072] | 66.494 [66.465, 66.578] | 3.4294e-15 |
| `APP-QFT-GRID-06` | Cirq | accepted | 81 [81, 81] | 56 [56, 56] | 88.933 [87.908, 89.072] | 145.01 [144.98, 145.03] | 1.6475e-15 |
| `APP-QFT-GRID-08` | FlagQuantum | accepted | 162 [162, 162] | 97 [97, 97] | 939.44 [912.07, 954.86] | 159.63 [159.62, 159.66] | 3.663e-15 |
| `APP-QFT-GRID-08` | Qiskit | accepted | 152 [138, 152] | 95 [84, 103] | 11.495 [10.841, 11.988] | 68.877 [68.617, 68.879] | 1.5849e-14 |
| `APP-QFT-GRID-08` | Cirq | accepted | 154 [154, 154] | 87 [87, 87] | 180.57 [179.61, 184.08] | 147.93 [147.82, 148.07] | 3.8198e-15 |
| `APP-QFT-GRID-12` | FlagQuantum | accepted | 352 [352, 352] | 150 [150, 150] | 2462.4 [2388.1, 2537.4] | 170.48 [170.15, 170.84] | 9.1721e-15 |
| `APP-QFT-GRID-12` | Qiskit | accepted | 382 [354, 388] | 193 [171, 206] | 22.151 [21.718, 22.536] | 80.643 [79.855, 81.172] | 4.3548e-14 |
| `APP-QFT-GRID-12` | Cirq | accepted | 388 [388, 388] | 176 [176, 176] | 496.6 [489.25, 501.01] | 159.58 [159.56, 159.59] | 2.3828e-15 |
| `APP-QFT-LINE-06` | FlagQuantum | accepted | 75 [75, 75] | 52 [52, 52] | 517.8 [506.19, 525.94] | 155.85 [155.8, 155.91] | 3.5043e-15 |
| `APP-QFT-LINE-06` | Qiskit | accepted | 99 [93, 99] | 76 [67, 76] | 8.8041 [8.4527, 9.1221] | 66.881 [66.379, 67.555] | 1.8395e-14 |
| `APP-QFT-LINE-06` | Cirq | accepted | 95 [95, 95] | 59 [59, 59] | 106.58 [105.94, 107.29] | 145.09 [145.08, 145.87] | 3.1436e-15 |
| `APP-QFT-LINE-08` | FlagQuantum | accepted | 156 [156, 156] | 77 [77, 77] | 1065.8 [1022.3, 1095.3] | 159.73 [159.71, 159.85] | 4.3433e-15 |
| `APP-QFT-LINE-08` | Qiskit | accepted | 180 [180, 186] | 91 [89, 98] | 12.488 [11.752, 12.747] | 70.123 [70.086, 70.129] | 2.222e-14 |
| `APP-QFT-LINE-08` | Cirq | accepted | 176 [176, 176] | 88 [88, 88] | 201.16 [199.22, 202.31] | 148.89 [148.58, 148.93] | 3.6159e-15 |
| `APP-QFT-LINE-12` | FlagQuantum | accepted | 396 [396, 396] | 137 [137, 137] | 2838.3 [2736, 2938.7] | 173.45 [171.46, 173.94] | 2.9042e-14 |
| `APP-QFT-LINE-12` | Qiskit | accepted | 426 [420, 430] | 146 [134, 154] | 21.984 [21.881, 22.321] | 81.865 [81.668, 82.109] | 4.5179e-14 |
| `APP-QFT-LINE-12` | Cirq | accepted | 410 [410, 410] | 144 [144, 144] | 476.01 [465.45, 481.07] | 159.83 [159.82, 159.84] | 3.649e-15 |
| `APP-REPETITION-GRID-06` | FlagQuantum | accepted | 52 [52, 52] | 50 [50, 50] | 294.71 [293.88, 298.81] | 155.12 [155.11, 155.2] | 6.371e-15 |
| `APP-REPETITION-GRID-06` | Qiskit | accepted | 60 [48, 68] | 52 [43, 60] | 7.1946 [7.0963, 7.33] | 65.416 [65.137, 65.668] | 5.4675e-15 |
| `APP-REPETITION-GRID-06` | Cirq | accepted | 52 [52, 52] | 50 [50, 50] | 84.175 [83.757, 85.325] | 143.68 [143.66, 143.69] | 8.0173e-15 |
| `APP-REPETITION-GRID-08` | FlagQuantum | accepted | 66 [66, 66] | 54 [54, 54] | 419.54 [414.37, 434.49] | 155.46 [155.39, 155.52] | 1.7721e-15 |
| `APP-REPETITION-GRID-08` | Qiskit | accepted | 84 [70, 86] | 68 [57, 73] | 7.7268 [7.4077, 8.1868] | 66.045 [65.719, 66.137] | 2.7845e-15 |
| `APP-REPETITION-GRID-08` | Cirq | accepted | 82 [82, 82] | 67 [67, 67] | 89.286 [88.288, 90.394] | 144.43 [144.42, 144.49] | 5.1701e-15 |
| `APP-REPETITION-GRID-12` | FlagQuantum | accepted | 82 [82, 82] | 60 [60, 60] | 481.63 [473.54, 492.36] | 156.14 [156.09, 156.22] | 1.3911e-15 |
| `APP-REPETITION-GRID-12` | Qiskit | accepted | 92 [92, 98] | 65 [60, 69] | 8.6665 [8.5216, 8.8969] | 66.424 [66.125, 66.828] | 2.1985e-15 |
| `APP-REPETITION-GRID-12` | Cirq | accepted | 82 [82, 82] | 60 [60, 60] | 109.79 [108, 111.05] | 144.6 [144.58, 145.32] | 1.3606e-15 |
| `APP-REPETITION-LINE-06` | FlagQuantum | accepted | 72 [72, 72] | 62 [62, 62] | 379.02 [371.05, 386.2] | 155.64 [155.56, 155.68] | 9.4155e-15 |
| `APP-REPETITION-LINE-06` | Qiskit | accepted | 72 [72, 80] | 62 [62, 67] | 8.0443 [7.9432, 8.5237] | 66.422 [66.41, 66.586] | 5.6297e-15 |
| `APP-REPETITION-LINE-06` | Cirq | accepted | 72 [72, 72] | 62 [62, 62] | 110.27 [109.51, 111.52] | 145.12 [144.35, 145.17] | 1.5713e-14 |
| `APP-REPETITION-LINE-08` | FlagQuantum | accepted | 90 [90, 90] | 65 [65, 65] | 509.21 [501.55, 520.42] | 156.64 [156.58, 156.67] | 3.4507e-15 |
| `APP-REPETITION-LINE-08` | Qiskit | accepted | 98 [90, 98] | 70 [65, 70] | 8.746 [8.5729, 9.4585] | 66.625 [66.375, 66.637] | 1.9555e-15 |
| `APP-REPETITION-LINE-08` | Cirq | accepted | 90 [90, 90] | 65 [65, 65] | 129.05 [128.27, 129.76] | 145.87 [145.09, 145.88] | 2.9315e-15 |
| `APP-REPETITION-LINE-12` | FlagQuantum | accepted | 148 [148, 148] | 90 [90, 90] | 815.61 [805.75, 836.33] | 159.63 [159.57, 159.66] | 2.8087e-15 |
| `APP-REPETITION-LINE-12` | Qiskit | accepted | 148 [144, 148] | 90 [81, 90] | 9.8 [9.6983, 10.307] | 67.881 [67.875, 67.898] | 2.8851e-15 |
| `APP-REPETITION-LINE-12` | Cirq | accepted | 148 [148, 148] | 90 [90, 90] | 154.86 [153.19, 156.34] | 146.84 [146.83, 146.85] | 2.8262e-15 |

## All paired descriptive comparisons

Each ratio is the named numerator divided by denominator. Values below one indicate less of that metric for the numerator on that case only. CZ/depth divide accepted-record medians. Time and memory pair matching block indices and show median [Q1, Q3] of the ten block ratios. These are separate metrics; no combined score, across-case aggregate or overall winner is calculated.

| Case | Numerator / denominator | Both cases complete | CZ ratio | Dependency-depth ratio | Time ratio [Q1, Q3] | Process-memory ratio [Q1, Q3] |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| `APP-HOPPING-GRID-06` | Cirq / FlagQuantum | true | 1.0244 | 1.0127 | 0.33185 [0.32682, 0.33915] | 0.93163 [0.92864, 0.93165] |
| `APP-HOPPING-GRID-06` | Cirq / Qiskit | true | 0.82353 | 0.91954 | 18.126 [17.733, 18.524] | 2.1873 [2.1801, 2.1875] |
| `APP-HOPPING-GRID-06` | FlagQuantum / Qiskit | true | 0.80392 | 0.90805 | 54.022 [53.424, 54.76] | 2.3479 [2.3478, 2.348] |
| `APP-HOPPING-GRID-08` | Cirq / FlagQuantum | true | 1 | 1 | 0.29572 [0.29135, 0.29849] | 0.92291 [0.92284, 0.92298] |
| `APP-HOPPING-GRID-08` | Cirq / Qiskit | true | 0.76923 | 0.80469 | 19.174 [18.177, 19.469] | 2.0756 [2.0756, 2.0757] |
| `APP-HOPPING-GRID-08` | FlagQuantum / Qiskit | true | 0.76923 | 0.80469 | 64.243 [62.746, 65.041] | 2.249 [2.2486, 2.2491] |
| `APP-HOPPING-GRID-12` | Cirq / FlagQuantum | true | 1.4698 | 1.6386 | 0.42184 [0.41003, 0.42988] | 0.97299 [0.97285, 0.97314] |
| `APP-HOPPING-GRID-12` | Cirq / Qiskit | true | 1.1173 | 1.1414 | 33.476 [33.097, 33.651] | 2.0451 [1.9984, 2.0488] |
| `APP-HOPPING-GRID-12` | FlagQuantum / Qiskit | true | 0.7602 | 0.69655 | 79.518 [78.166, 82.747] | 2.1019 [2.0543, 2.1058] |
| `APP-HOPPING-LINE-06` | Cirq / FlagQuantum | true | 1 | 1 | 0.35612 [0.34887, 0.36188] | 0.93094 [0.93081, 0.9312] |
| `APP-HOPPING-LINE-06` | Cirq / Qiskit | true | 1 | 1 | 18.183 [17.688, 18.266] | 2.1881 [2.188, 2.1881] |
| `APP-HOPPING-LINE-06` | FlagQuantum / Qiskit | true | 1 | 1 | 50.321 [49.608, 51.101] | 2.3501 [2.3496, 2.3507] |
| `APP-HOPPING-LINE-08` | Cirq / FlagQuantum | true | 1 | 1 | 0.36505 [0.35568, 0.37138] | 0.9333 [0.93322, 0.93336] |
| `APP-HOPPING-LINE-08` | Cirq / Qiskit | true | 1 | 1 | 21.045 [19.119, 21.243] | 2.139 [2.139, 2.1392] |
| `APP-HOPPING-LINE-08` | FlagQuantum / Qiskit | true | 1 | 1 | 56.286 [53.458, 57.297] | 2.292 [2.2917, 2.2921] |
| `APP-HOPPING-LINE-12` | Cirq / FlagQuantum | true | 1 | 1 | 0.36416 [0.34951, 0.38149] | 0.92794 [0.92788, 0.92809] |
| `APP-HOPPING-LINE-12` | Cirq / Qiskit | true | 1 | 1 | 31.009 [30.162, 31.962] | 2.0806 [2.0805, 2.0806] |
| `APP-HOPPING-LINE-12` | FlagQuantum / Qiskit | true | 1 | 1 | 84.368 [83.466, 85.275] | 2.2421 [2.2416, 2.2422] |
| `APP-ISING-GRID-06` | Cirq / FlagQuantum | true | 1.2381 | 1.6154 | 0.36003 [0.35306, 0.3632] | 0.93197 [0.93173, 0.932] |
| `APP-ISING-GRID-06` | Cirq / Qiskit | true | 1.0833 | 1.3125 | 10.559 [10.31, 10.694] | 2.2038 [2.2037, 2.2041] |
| `APP-ISING-GRID-06` | FlagQuantum / Qiskit | true | 0.875 | 0.8125 | 29.371 [29.179, 29.514] | 2.3649 [2.3647, 2.3653] |
| `APP-ISING-GRID-08` | Cirq / FlagQuantum | true | 1.1538 | 1.1154 | 0.28297 [0.28069, 0.28487] | 0.92891 [0.92875, 0.92896] |
| `APP-ISING-GRID-08` | Cirq / Qiskit | true | 1 | 1 | 10.207 [9.73, 10.721] | 2.19 [2.1895, 2.1901] |
| `APP-ISING-GRID-08` | FlagQuantum / Qiskit | true | 0.86667 | 0.89655 | 36.822 [34.819, 37.629] | 2.3575 [2.3575, 2.3577] |
| `APP-ISING-GRID-12` | Cirq / FlagQuantum | true | 1.0103 | 1.0619 | 0.19947 [0.19423, 0.20478] | 0.92716 [0.92645, 0.92732] |
| `APP-ISING-GRID-12` | Cirq / Qiskit | true | 1.1011 | 1.1705 | 18.358 [17.511, 18.585] | 2.1407 [2.1402, 2.1408] |
| `APP-ISING-GRID-12` | FlagQuantum / Qiskit | true | 1.0899 | 1.1023 | 90.258 [89.788, 91.841] | 2.3099 [2.3085, 2.3106] |
| `APP-ISING-LINE-06` | Cirq / FlagQuantum | true | 1.3913 | 1.8077 | 0.35288 [0.35034, 0.35553] | 0.93504 [0.935, 0.9351] |
| `APP-ISING-LINE-06` | Cirq / Qiskit | true | 1.28 | 1.3429 | 12.712 [12.243, 12.909] | 2.211 [2.2108, 2.2121] |
| `APP-ISING-LINE-06` | FlagQuantum / Qiskit | true | 0.92 | 0.74286 | 36.086 [35.652, 36.517] | 2.3649 [2.3645, 2.3658] |
| `APP-ISING-LINE-08` | Cirq / FlagQuantum | true | 0.90625 | 0.81818 | 0.18635 [0.18432, 0.18838] | 0.92695 [0.923, 0.92708] |
| `APP-ISING-LINE-08` | Cirq / Qiskit | true | 1.0357 | 0.95455 | 12.61 [12.039, 13.063] | 2.1614 [2.154, 2.1658] |
| `APP-ISING-LINE-08` | FlagQuantum / Qiskit | true | 1.1429 | 1.1667 | 68.785 [67.381, 70.311] | 2.3357 [2.3295, 2.3362] |
| `APP-ISING-LINE-12` | Cirq / FlagQuantum | true | 1 | 1.0755 | 0.18431 [0.17747, 0.18709] | 0.92363 [0.92352, 0.92415] |
| `APP-ISING-LINE-12` | Cirq / Qiskit | true | 0.87413 | 0.68675 | 16.639 [16.283, 16.806] | 2.0591 [2.0589, 2.0591] |
| `APP-ISING-LINE-12` | FlagQuantum / Qiskit | true | 0.87413 | 0.63855 | 90.377 [89.301, 91.874] | 2.2291 [2.2282, 2.2296] |
| `APP-QAOA-GRID-06` | Cirq / FlagQuantum | true | 1.2857 | 1 | 0.32715 [0.32513, 0.33581] | 0.9294 [0.92915, 0.92951] |
| `APP-QAOA-GRID-06` | Cirq / Qiskit | true | 1.2857 | 1 | 9.6262 [9.4993, 9.691] | 2.2118 [2.2113, 2.2122] |
| `APP-QAOA-GRID-06` | FlagQuantum / Qiskit | true | 1 | 1 | 29.083 [28.653, 29.71] | 2.3799 [2.3794, 2.38] |
| `APP-QAOA-GRID-08` | Cirq / FlagQuantum | true | 1 | 0.84211 | 0.20184 [0.19533, 0.20681] | 0.92738 [0.92731, 0.9275] |
| `APP-QAOA-GRID-08` | Cirq / Qiskit | true | 1 | 1 | 10.013 [10.003, 10.073] | 2.196 [2.1957, 2.1966] |
| `APP-QAOA-GRID-08` | FlagQuantum / Qiskit | true | 1 | 1.1875 | 50.025 [48.438, 50.718] | 2.3679 [2.3677, 2.3681] |
| `APP-QAOA-GRID-12` | Cirq / FlagQuantum | true | 1.2281 | 1.3696 | 0.20999 [0.20657, 0.21355] | 0.9265 [0.92646, 0.92656] |
| `APP-QAOA-GRID-12` | Cirq / Qiskit | true | 1.0606 | 1.1053 | 13.835 [13.318, 14.311] | 2.1551 [2.1542, 2.1676] |
| `APP-QAOA-GRID-12` | FlagQuantum / Qiskit | true | 0.86364 | 0.80702 | 65.328 [63.704, 67.566] | 2.3279 [2.3256, 2.3394] |
| `APP-QAOA-LINE-06` | Cirq / FlagQuantum | true | 1.0513 | 1.0682 | 0.24801 [0.24489, 0.25051] | 0.93197 [0.93181, 0.93204] |
| `APP-QAOA-LINE-06` | Cirq / Qiskit | true | 1.025 | 0.88679 | 11.726 [10.999, 11.987] | 2.18 [2.1766, 2.1809] |
| `APP-QAOA-LINE-06` | FlagQuantum / Qiskit | true | 0.975 | 0.83019 | 47.311 [45.629, 48.303] | 2.3393 [2.3388, 2.3401] |
| `APP-QAOA-LINE-08` | Cirq / FlagQuantum | true | 1.0704 | 0.87952 | 0.2063 [0.20324, 0.21024] | 0.93104 [0.93081, 0.93124] |
| `APP-QAOA-LINE-08` | Cirq / Qiskit | true | 0.98701 | 0.94805 | 15.357 [14.381, 15.667] | 2.1498 [2.143, 2.1503] |
| `APP-QAOA-LINE-08` | FlagQuantum / Qiskit | true | 0.92208 | 1.0779 | 73.797 [70.213, 74.358] | 2.3088 [2.3019, 2.3097] |
| `APP-QAOA-LINE-12` | Cirq / FlagQuantum | true | 0.94444 | 1.0462 | 0.17725 [0.17496, 0.18587] | 0.92727 [0.92678, 0.92785] |
| `APP-QAOA-LINE-12` | Cirq / Qiskit | true | 0.96591 | 1.0462 | 15.994 [14.811, 16.577] | 2.1363 [2.1345, 2.1369] |
| `APP-QAOA-LINE-12` | FlagQuantum / Qiskit | true | 1.0227 | 1 | 88.451 [84.304, 89.668] | 2.3021 [2.3019, 2.3048] |
| `APP-QFT-GRID-06` | Cirq / FlagQuantum | true | 1.2462 | 1.1667 | 0.20021 [0.19592, 0.20201] | 0.9335 [0.93335, 0.93363] |
| `APP-QFT-GRID-06` | Cirq / Qiskit | true | 1 | 1 | 11.109 [10.756, 11.462] | 2.1808 [2.1784, 2.1817] |
| `APP-QFT-GRID-06` | FlagQuantum / Qiskit | true | 0.80247 | 0.85714 | 55.872 [54.984, 56.485] | 2.3361 [2.334, 2.3373] |
| `APP-QFT-GRID-08` | Cirq / FlagQuantum | true | 0.95062 | 0.89691 | 0.1943 [0.1902, 0.19675] | 0.92666 [0.92665, 0.92676] |
| `APP-QFT-GRID-08` | Cirq / Qiskit | true | 1.0132 | 0.91579 | 16.011 [15.301, 16.538] | 2.1481 [2.1476, 2.1542] |
| `APP-QFT-GRID-08` | FlagQuantum / Qiskit | true | 1.0658 | 1.0211 | 83.062 [80.089, 84.91] | 2.3177 [2.3176, 2.3262] |
| `APP-QFT-GRID-12` | Cirq / FlagQuantum | true | 1.1023 | 1.1733 | 0.20503 [0.19439, 0.20755] | 0.93607 [0.93457, 0.93748] |
| `APP-QFT-GRID-12` | Cirq / Qiskit | true | 1.0157 | 0.91192 | 22.488 [22.214, 22.839] | 1.9788 [1.968, 1.9856] |
| `APP-QFT-GRID-12` | FlagQuantum / Qiskit | true | 0.92147 | 0.7772 | 111.63 [110.46, 112.59] | 2.1137 [2.1058, 2.1204] |
| `APP-QFT-LINE-06` | Cirq / FlagQuantum | true | 1.2667 | 1.1346 | 0.20691 [0.20265, 0.20939] | 0.93113 [0.93082, 0.93458] |
| `APP-QFT-LINE-06` | Cirq / Qiskit | true | 0.9596 | 0.77632 | 12.132 [11.765, 12.6] | 2.1809 [2.1692, 2.1856] |
| `APP-QFT-LINE-06` | FlagQuantum / Qiskit | true | 0.75758 | 0.68421 | 58.695 [57.66, 60.442] | 2.3306 [2.3303, 2.3473] |
| `APP-QFT-LINE-08` | Cirq / FlagQuantum | true | 1.1282 | 1.1429 | 0.18729 [0.18449, 0.19592] | 0.93182 [0.93028, 0.93212] |
| `APP-QFT-LINE-08` | Cirq / Qiskit | true | 0.97778 | 0.96703 | 16.149 [15.797, 16.998] | 2.1235 [2.1192, 2.124] |
| `APP-QFT-LINE-08` | FlagQuantum / Qiskit | true | 0.86667 | 0.84615 | 86.56 [85.423, 87.199] | 2.2783 [2.2776, 2.2791] |
| `APP-QFT-LINE-12` | Cirq / FlagQuantum | true | 1.0354 | 1.0511 | 0.16955 [0.16454, 0.17051] | 0.92145 [0.92017, 0.93139] |
| `APP-QFT-LINE-12` | Cirq / Qiskit | true | 0.96244 | 0.9863 | 21.492 [21.383, 21.645] | 1.9522 [1.9517, 1.9526] |
| `APP-QFT-LINE-12` | FlagQuantum / Qiskit | true | 0.92958 | 0.93836 | 128.36 [126.28, 130.6] | 2.1177 [2.0962, 2.1213] |
| `APP-REPETITION-GRID-06` | Cirq / FlagQuantum | true | 1 | 1 | 0.28438 [0.28204, 0.28737] | 0.92619 [0.92599, 0.92629] |
| `APP-REPETITION-GRID-06` | Cirq / Qiskit | true | 0.86667 | 0.96154 | 11.756 [11.55, 11.798] | 2.1965 [2.1925, 2.2015] |
| `APP-REPETITION-GRID-06` | FlagQuantum / Qiskit | true | 0.86667 | 0.96154 | 41.431 [40.763, 41.801] | 2.3716 [2.3672, 2.377] |
| `APP-REPETITION-GRID-08` | Cirq / FlagQuantum | true | 1.2424 | 1.2407 | 0.21414 [0.2079, 0.21497] | 0.9291 [0.9289, 0.92915] |
| `APP-REPETITION-GRID-08` | Cirq / Qiskit | true | 0.97619 | 0.98529 | 11.486 [10.909, 11.959] | 2.1869 [2.1852, 2.1961] |
| `APP-REPETITION-GRID-08` | FlagQuantum / Qiskit | true | 0.78571 | 0.79412 | 55.309 [52.304, 55.793] | 2.3539 [2.3527, 2.3641] |
| `APP-REPETITION-GRID-12` | Cirq / FlagQuantum | true | 1 | 1 | 0.22717 [0.22565, 0.22985] | 0.92614 [0.92569, 0.93046] |
| `APP-REPETITION-GRID-12` | Cirq / Qiskit | true | 0.8913 | 0.92308 | 12.521 [12.392, 12.61] | 2.1804 [2.1691, 2.1866] |
| `APP-REPETITION-GRID-12` | FlagQuantum / Qiskit | true | 0.8913 | 0.92308 | 55.576 [54.918, 56.085] | 2.3506 [2.3385, 2.3616] |
| `APP-REPETITION-LINE-06` | Cirq / FlagQuantum | true | 1 | 1 | 0.29163 [0.28624, 0.29758] | 0.93244 [0.93223, 0.93269] |
| `APP-REPETITION-LINE-06` | Cirq / Qiskit | true | 1 | 1 | 13.856 [12.96, 13.926] | 2.1798 [2.1794, 2.1849] |
| `APP-REPETITION-LINE-06` | FlagQuantum / Qiskit | true | 1 | 1 | 47.056 [44.89, 48.003] | 2.3424 [2.3377, 2.3433] |
| `APP-REPETITION-LINE-08` | Cirq / FlagQuantum | true | 1 | 1 | 0.25229 [0.25027, 0.25628] | 0.93119 [0.92773, 0.9314] |
| `APP-REPETITION-LINE-08` | Cirq / Qiskit | true | 0.91837 | 0.92857 | 14.65 [13.704, 15.119] | 2.1891 [2.1865, 2.1955] |
| `APP-REPETITION-LINE-08` | FlagQuantum / Qiskit | true | 0.91837 | 0.92857 | 57.779 [56.07, 58.617] | 2.3512 [2.3509, 2.3595] |
| `APP-REPETITION-LINE-12` | Cirq / FlagQuantum | true | 1 | 1 | 0.18825 [0.18536, 0.19021] | 0.91984 [0.91979, 0.91989] |
| `APP-REPETITION-LINE-12` | Cirq / Qiskit | true | 1 | 1 | 15.609 [14.868, 15.939] | 2.1632 [2.1629, 2.1632] |
| `APP-REPETITION-LINE-12` | FlagQuantum / Qiskit | true | 1 | 1 | 83.146 [80.12, 83.823] | 2.3516 [2.3513, 2.3519] |

## Reproduce acceptance and comparisons

Use a clean checkout of the pinned SDKBench harness, install its independent evaluator requirements, and extract the retained archive into a fresh directory. Participant SDKs are unnecessary for replay. Binary/source build admission needs the original full GitHub artifact described in the index; semantic replay uses the durable raw archive.

```bash
tar -xJf docs/analysis/evidence/compiler-target-artifact-44587642527.tar.xz -C /path/to/fresh-evidence
PYTHONPATH=src python -m sdkbench.candidates.cli replay \
  --directory /path/to/fresh-evidence/campaign \
  --bundle /path/to/fresh-evidence/preparation/cohort
PYTHONPATH=src python tools/compare_compiler_applications.py \
  --profile target-artifact \
  --directory /path/to/fresh-evidence/campaign \
  --bundle /path/to/fresh-evidence/preparation/cohort \
  --output /path/to/new-comparisons.json
```

Expected: 900 blocks replayed, 90 case/participant outcomes, and 90 case/pair comparisons. Output paths must be new. Complete raw evidence, not rounded Markdown values, is authoritative. Build observation, kernel-policy consistency and local freeze/draw ordering do not establish independent build attestation or host qualification. Publication eligibility remains false pending the protocol's separate review and attestation requirements.
