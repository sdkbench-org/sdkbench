# Ordinary compiler application results (2026-11-20)

90/90 complete case/participant pairs passed this engineering campaign. All 30 cases and all three participant pairings are retained. This is a bounded restored-layout study, not a global SDK ranking or a publication-qualified performance claim.

The study follows the [prospective declaration](COMPILER_QUALIFICATION_DECLARATION_20261119.md) and [unchanged matched-layout protocol](COMPILER_APPLICATION_CAMPAIGN.md). The two declared profiles draw independent cohorts; do not combine their results, choose the better FlagQuantum profile per case, divide their metrics, or attribute between-profile differences to one compiler pass.

## Immutable execution and evidence

- [Original workflow run](https://github.com/sdkbench-org/sdkbench/actions/runs/44587635615), attempt 1; no campaign rerun or redraw.
- FlagQuantum source: `858df9dbd5ba964e8e59b3383304547710a1dee5`; SDKBench harness: `9e3992d14342601662443b6720dd6757905c3f3b`.
- Qiskit 2.6.2 and Cirq 1.7.0; actual wheels, build files and registrations were frozen before drawing.
- Freeze timestamp: `2026-11-19T18:28:11.527854+00:00`; draw timestamp: `2026-11-19T18:28:11.530969+00:00`. These are local event records, not independent timestamp attestations.
- [Evidence index](evidence/compiler-ordinary-44587635615-index.json), [complete raw campaign archive](evidence/compiler-ordinary-44587635615.tar.xz), [local verification](evidence/compiler-ordinary-44587635615-verification.json), [layout/resource audit](evidence/compiler-ordinary-44587635615-layout-resources.json), [machine-readable summary](evidence/compiler-ordinary-44587635615-summary.json.gz) and [all 90 paired comparisons](evidence/compiler-ordinary-44587635615-comparisons.json).

The retained archive contains 2,907 original files, including every one of the 2,705 campaign manifest entries; every retained member was hash-verified. It preserves requests, responses, warmups, measurements, supervisor evidence and failures unchanged. The index pins the original ZIP, source archive and wheel hashes. Build binaries and extracted compiler sources remain in the original artifact, expiring `2027-02-17T18:25:28Z`; they are not duplicated in Git. This retention limit must not be hidden.

Independent local replay denied imports of FlagQuantum, Qiskit and Cirq. It verified 900 blocks and 2,700 measured records, reproduced the hosted case decisions, and matched every hosted pair metric and coverage entry. Preparation was regenerated using the retained nonce without drawing again. No acceptance, resource ceiling or adapter was changed.

An initial local audit completed record replay, then failed when calling a comparison helper that had been shadowed by an older scratch copy. The audit entry was corrected to load and verify the frozen repository's helper paths, then local auditing was repeated. This was an analysis-tool failure; neither the campaign nor its measurements were rerun.

The local and hosted summary digests differ only in independently recomputed maximum semantic-error values. Substituting the retained hosted error values, while leaving every other local summary field unchanged, reconstructs the exact hosted digest; see the [reconciliation proof](evidence/compiler-ordinary-44587635615-summary-reconciliation.json). Both error sets remain retained under the unchanged acceptance threshold. All case decisions, gate/depth metrics and timing/memory comparisons match. The original local digest is not rewritten.

## Applicability and measurement boundary

Five application families (QAOA, Ising evolution, hopping, QFT and repetition), widths 6/8/12, and line/grid targets produce 30 cases. Ring/sparse targets and the broader SDK task catalog remain outside this campaign. No GPU, QPU, distributed execution, hardware-fidelity or global SDK capability claim follows from these CPU compiler results.

Measurement host: `Intel(R) Xeon(R) 6975P-C`; `Linux-7.0.0-1014-aws-x86_64-with-glibc2.39`; Python `3.12.14`. Each supervised process was pinned to one CPU with one numerical thread, 16 GiB memory, socket/io-uring denial, two warmups and three measured compilations. Ten blocks are required per case. A 120-second per-compilation ceiling, the frozen width-specific cumulative case ceilings, the 270-minute measurement step and the 360-minute job ceiling remain unchanged.

All three registrations start with identity placement and use the same timed spanning-tree token-restoration policy. The final identity placement was separately checked in all retained warmups and measurements. Quality metrics therefore include the cost of that common delivered-layout obligation; they do not isolate routing, layout search or synthesis individually.

The target family is full CZ plus arbitrary one-qubit unitaries on the declared undirected edges, without ancillas. Independent semantic acceptance uses absolute error at most 1e-8, zero relative tolerance, normalization error at most 1e-10 and zero target violations. Six-qubit cases validate the complete operator up to one global phase. Widths 8/12 validate three complete probe-output states up to a phase per probe; they are not universal equivalence proofs.

FlagQuantum runs its public compiler's default routing followed by ordinary native-gate legalization. This path does not invoke target-aware CZ block resynthesis. Qiskit uses optimization level 2, exact approximation degree 1.0, identity initial placement and one process. Cirq uses identity-mapped RouteCQC followed by full-CZ target optimization at 1e-12 synthesis tolerance. Exact options and package identities are retained per registration. Different native search implementations are part of the compared workflows, not an equal-algorithm control.

## Observed trade-offs and remaining work

These examples were inspected after execution and illustrate individual cases.
The complete tables below retain every participant and case.

- On `APP-QAOA-GRID-06`, FlagQuantum delivers 42 CZ gates and dependency depth
  18; Qiskit and Cirq each deliver 52 and 30. The median block times are
  10.567 ms, 5.5411 ms and 42.023 ms respectively. The corresponding process
  peaks are 152.29, 64.855 and 142.98 MiB. The lower interaction count does not
  remove FlagQuantum's time and process-memory gap to Qiskit on this case.
  This six-qubit case has full-operator acceptance.
- On `APP-QFT-LINE-12`, FlagQuantum delivers 534 CZ gates and depth 206,
  compared with Qiskit's 426/146 and Cirq's 410/144. Median block times are
  86.812 ms, 18.479 ms and 399.28 ms respectively. FlagQuantum uses more
  interactions and dependency depth than both comparators here; its workflow
  is slower than Qiskit's and faster than Cirq's on this case.
- On `APP-HOPPING-GRID-12`, FlagQuantum delivers 346 CZ gates and depth 279,
  Qiskit 428/347 and Cirq 454/361. Median block times are 88.500 ms,
  20.146 ms and 733.27 ms. This is another distinct quality/time trade-off.
  Both twelve-qubit examples retain three-probe acceptance only.

The measured compiler is not uniformly best. The QFT line case provides a
concrete quality gap to investigate, while the QAOA and hopping examples show
why compiler quality and compilation latency must stay separate. Common target,
identity input/output placement and resource controls make these registered
workflow comparisons interpretable; they do not make the internal algorithms
or search effort identical.

Follow-up engineering should profile the public default workflow's routing,
layout restoration and target lowering separately on new development inputs,
then use a separately declared qualification for a changed candidate. The
current data does not isolate which pass causes a gap. Process-memory peaks
include imports and export, so an additional attribution experiment is needed
before assigning that gap to compiler workspace. The ordinary path's omission
of target-aware CZ resynthesis remains explicit; the separately drawn
target-artifact profile must supply its own evidence.

This campaign compares one integrated FlagQuantum revision with two published
comparators. It contains no old-FlagQuantum control and cannot establish a
prospective causal improvement for any individual upstream-derived pass.
Development ablations and source-level reuse evidence remain separate from
these application results. Improvements must be implemented in the SDK product;
participant-specific benchmark helpers or post-outcome option selection are
not admitted.

## Complete coverage

| Workflow | Accepted complete cases | Other complete-case outcomes | Accepted measured records / expected |
| --- | ---: | --- | ---: |
| `flagquantum-ordinary-restored` | 30/30 | none | 900/900 |
| `qiskit-transpile-restored` | 30/30 | none | 900/900 |
| `cirq-route-cz-restored` | 30/30 | none | 900/900 |

Retained warmup records: 1800/1,800. Failed warmups, unsupported, timeout, isolation, memory and semantic failures remain in the case denominator. A failed case receives no paired performance ratios, even if some records passed. Conditional diagnostics, if present, remain in the machine-readable summary.

## Every case and participant

CZ count and dependency depth show the median [minimum, maximum] across 30 accepted measured records. Time is milliseconds: the median [Q1, Q3] of ten block medians, each formed from three accepted measurements. Memory is MiB: the median [minimum, maximum] of ten kernel process peaks, including imports, warmups, computation and export. It is not compiler-only workspace. Maximum semantic error below is for measured records. Quartiles describe observed variation, not confidence intervals or statistical significance.

| Case | SDK | Status | Full CZ | Two-body dependency depth | Workflow time, ms | Process peak, MiB | Maximum semantic error |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| `APP-HOPPING-GRID-06` | FlagQuantum | accepted | 90 [90, 90] | 86 [86, 86] | 31.604 [31.534, 31.89] | 153.18 [153.17, 153.22] | 1.5099e-14 |
| `APP-HOPPING-GRID-06` | Qiskit | accepted | 86 [84, 86] | 78 [76, 78] | 8.0604 [7.932, 8.1632] | 66.375 [66.371, 66.379] | 1.1488e-13 |
| `APP-HOPPING-GRID-06` | Cirq | accepted | 96 [96, 96] | 89 [89, 89] | 140.24 [139.65, 140.99] | 145.98 [145.33, 145.99] | 1.6432e-14 |
| `APP-HOPPING-GRID-08` | FlagQuantum | accepted | 148 [148, 148] | 111 [111, 111] | 45.954 [45.796, 46.463] | 154.53 [154.52, 154.58] | 1.0161e-14 |
| `APP-HOPPING-GRID-08` | Qiskit | accepted | 138 [138, 138] | 106 [106, 106] | 9.9736 [9.8633, 10.058] | 70.117 [70.117, 70.125] | 4.1993e-15 |
| `APP-HOPPING-GRID-08` | Cirq | accepted | 166 [166, 166] | 129 [129, 129] | 259.22 [257.78, 260.77] | 149.58 [149.57, 149.87] | 3.3571e-15 |
| `APP-HOPPING-GRID-12` | FlagQuantum | accepted | 346 [346, 346] | 279 [279, 279] | 88.5 [88.142, 89.234] | 157.75 [157.73, 157.89] | 1.5044e-14 |
| `APP-HOPPING-GRID-12` | Qiskit | accepted | 428 [422, 456] | 347 [345, 356] | 20.146 [19.818, 20.57] | 81.389 [80.375, 82.352] | 6.0991e-15 |
| `APP-HOPPING-GRID-12` | Cirq | accepted | 454 [454, 454] | 361 [361, 361] | 733.27 [731.17, 738.45] | 163.81 [163.8, 163.82] | 5.5936e-15 |
| `APP-HOPPING-LINE-06` | FlagQuantum | accepted | 72 [72, 72] | 70 [70, 70] | 28.578 [28.382, 28.712] | 153.04 [153.03, 153.22] | 1.1993e-14 |
| `APP-HOPPING-LINE-06` | Qiskit | accepted | 66 [66, 66] | 64 [64, 64] | 7.1233 [7.0743, 7.1711] | 66.266 [66.266, 66.27] | 2.0545e-13 |
| `APP-HOPPING-LINE-06` | Cirq | accepted | 66 [66, 66] | 64 [64, 64] | 129.03 [128.27, 130.42] | 144.83 [144.82, 144.85] | 1.386e-14 |
| `APP-HOPPING-LINE-08` | FlagQuantum | accepted | 112 [112, 112] | 96 [96, 96] | 40.475 [40.253, 40.708] | 154.27 [154.03, 154.36] | 7.5512e-15 |
| `APP-HOPPING-LINE-08` | Qiskit | accepted | 104 [104, 104] | 89 [89, 89] | 8.7409 [8.6751, 8.8261] | 69.844 [69.812, 69.852] | 2.0932e-15 |
| `APP-HOPPING-LINE-08` | Cirq | accepted | 104 [104, 104] | 89 [89, 89] | 202.27 [201.2, 203.21] | 146.66 [145.82, 146.81] | 3.6142e-15 |
| `APP-HOPPING-LINE-12` | FlagQuantum | accepted | 256 [256, 256] | 236 [236, 236] | 71.851 [71.337, 72.413] | 156.51 [156.24, 156.64] | 1.1658e-14 |
| `APP-HOPPING-LINE-12` | Qiskit | accepted | 244 [244, 244] | 224 [224, 224] | 14.404 [13.814, 14.465] | 75.848 [75.844, 75.855] | 4.8193e-15 |
| `APP-HOPPING-LINE-12` | Cirq | accepted | 244 [244, 244] | 224 [224, 224] | 473.87 [472.25, 475.3] | 153.06 [153.04, 153.28] | 2.5203e-15 |
| `APP-ISING-GRID-06` | FlagQuantum | accepted | 48 [48, 48] | 28 [28, 28] | 14.475 [14.398, 14.583] | 152.58 [152.54, 152.64] | 5.431e-15 |
| `APP-ISING-GRID-06` | Qiskit | accepted | 52 [52, 52] | 33 [33, 33] | 5.931 [5.9062, 5.9529] | 65.215 [65.207, 65.324] | 3.3422e-15 |
| `APP-ISING-GRID-06` | Cirq | accepted | 52 [52, 52] | 33 [33, 33] | 53.036 [52.118, 53.376] | 143.29 [143.28, 143.34] | 2.9166e-14 |
| `APP-ISING-GRID-08` | FlagQuantum | accepted | 60 [60, 60] | 31 [31, 31] | 18.565 [18.52, 18.665] | 152.9 [152.89, 152.98] | 4.5594e-15 |
| `APP-ISING-GRID-08` | Qiskit | accepted | 70 [70, 70] | 39 [39, 39] | 6.6089 [6.5721, 6.688] | 65.906 [65.902, 65.91] | 1.9642e-15 |
| `APP-ISING-GRID-08` | Cirq | accepted | 70 [70, 70] | 39 [39, 39] | 70.636 [70.167, 71.094] | 144.11 [144.08, 144.12] | 2.8646e-15 |
| `APP-ISING-GRID-12` | FlagQuantum | accepted | 174 [174, 174] | 77 [77, 77] | 35.367 [35.188, 35.5] | 155.05 [154.91, 155.09] | 7.6214e-15 |
| `APP-ISING-GRID-12` | Qiskit | accepted | 210 [184, 216] | 123 [98, 128] | 10.328 [10.183, 10.512] | 70.104 [69.688, 70.363] | 3.7397e-15 |
| `APP-ISING-GRID-12` | Cirq | accepted | 210 [210, 210] | 102 [102, 102] | 180.65 [179.55, 180.96] | 148.83 [148.82, 149.11] | 4.0433e-15 |
| `APP-ISING-LINE-06` | FlagQuantum | accepted | 78 [78, 78] | 58 [58, 58] | 17.341 [17.231, 17.446] | 153.15 [153.04, 153.17] | 7.9505e-15 |
| `APP-ISING-LINE-06` | Qiskit | accepted | 74 [74, 74] | 51 [51, 51] | 6.4387 [6.3665, 6.4875] | 64.02 [64.016, 64.023] | 4.3088e-15 |
| `APP-ISING-LINE-06` | Cirq | accepted | 74 [74, 74] | 47 [47, 47] | 69.267 [68.839, 69.795] | 144.37 [143.84, 144.38] | 6.9909e-15 |
| `APP-ISING-LINE-08` | FlagQuantum | accepted | 102 [102, 102] | 67 [67, 67] | 21.896 [21.832, 22.034] | 153.65 [153.64, 153.74] | 8.0997e-15 |
| `APP-ISING-LINE-08` | Qiskit | accepted | 96 [96, 96] | 53 [53, 53] | 7.3943 [7.2992, 7.5315] | 66.373 [66.371, 66.375] | 2.3876e-15 |
| `APP-ISING-LINE-08` | Cirq | accepted | 106 [106, 106] | 65 [65, 65] | 108 [107.54, 108.9] | 145.34 [145.33, 146.12] | 2.5019e-15 |
| `APP-ISING-LINE-12` | FlagQuantum | accepted | 234 [234, 234] | 105 [105, 105] | 40.178 [39.895, 40.358] | 156.08 [156.05, 156.1] | 9.7509e-15 |
| `APP-ISING-LINE-12` | Qiskit | accepted | 240 [234, 240] | 106 [100, 112] | 11.417 [10.839, 11.642] | 71.371 [71.117, 71.863] | 3.4598e-15 |
| `APP-ISING-LINE-12` | Cirq | accepted | 222 [222, 222] | 94 [94, 94] | 189.93 [188.45, 190.97] | 149.83 [149.82, 149.84] | 2.8149e-14 |
| `APP-QAOA-GRID-06` | FlagQuantum | accepted | 42 [42, 42] | 18 [18, 18] | 10.567 [10.495, 10.608] | 152.29 [152.18, 152.37] | 2.5637e-15 |
| `APP-QAOA-GRID-06` | Qiskit | accepted | 52 [52, 52] | 30 [30, 30] | 5.5411 [5.5319, 5.5861] | 64.855 [64.828, 64.887] | 1.7783e-15 |
| `APP-QAOA-GRID-06` | Cirq | accepted | 52 [52, 52] | 30 [30, 30] | 42.023 [41.838, 42.361] | 142.98 [142.98, 142.99] | 3.3422e-15 |
| `APP-QAOA-GRID-08` | FlagQuantum | accepted | 74 [74, 74] | 46 [46, 46] | 15.099 [15.003, 15.144] | 153.14 [153.1, 153.16] | 3.159e-15 |
| `APP-QAOA-GRID-08` | Qiskit | accepted | 90 [88, 90] | 60 [57, 60] | 7.0618 [6.8776, 7.2184] | 64.623 [64.133, 64.773] | 1.9224e-15 |
| `APP-QAOA-GRID-08` | Cirq | accepted | 84 [84, 84] | 53 [53, 53] | 74.221 [73.811, 75.076] | 144.81 [144.78, 144.83] | 1.5516e-15 |
| `APP-QAOA-GRID-12` | FlagQuantum | accepted | 180 [180, 180] | 93 [93, 93] | 29.424 [29.313, 29.584] | 154.83 [154.8, 154.86] | 1.0091e-14 |
| `APP-QAOA-GRID-12` | Qiskit | accepted | 168 [168, 168] | 84 [84, 84] | 8.8051 [8.6513, 8.8925] | 68.379 [68.363, 68.383] | 3.6312e-15 |
| `APP-QAOA-GRID-12` | Cirq | accepted | 184 [184, 184] | 83 [83, 83] | 143.48 [141.26, 143.97] | 148.09 [148.06, 148.11] | 3.44e-15 |
| `APP-QAOA-LINE-06` | FlagQuantum | accepted | 72 [72, 72] | 40 [40, 40] | 12.941 [12.915, 13.018] | 152.8 [152.79, 152.92] | 4.4392e-15 |
| `APP-QAOA-LINE-06` | Qiskit | accepted | 72 [72, 72] | 40 [40, 40] | 6.3235 [6.2661, 6.476] | 65.973 [65.965, 66.023] | 1.8453e-15 |
| `APP-QAOA-LINE-06` | Cirq | accepted | 70 [70, 70] | 41 [41, 41] | 69.811 [69.525, 70.178] | 144.37 [144.36, 144.38] | 2.513e-15 |
| `APP-QAOA-LINE-08` | FlagQuantum | accepted | 116 [116, 116] | 51 [51, 51] | 18.325 [18.213, 18.36] | 153.4 [153.39, 153.53] | 4.8286e-15 |
| `APP-QAOA-LINE-08` | Qiskit | accepted | 118 [110, 118] | 60 [54, 61] | 7.7139 [7.604, 7.8011] | 68.021 [67.91, 68.027] | 1.6447e-15 |
| `APP-QAOA-LINE-08` | Cirq | accepted | 128 [128, 128] | 70 [70, 70] | 120.54 [119.69, 121.47] | 146.59 [146.58, 146.84] | 2.423e-15 |
| `APP-QAOA-LINE-12` | FlagQuantum | accepted | 252 [252, 252] | 100 [100, 100] | 35.388 [35.226, 35.56] | 156.11 [155.79, 156.14] | 1.3646e-14 |
| `APP-QAOA-LINE-12` | Qiskit | accepted | 256 [252, 296] | 102 [100, 142] | 12.331 [12.257, 12.453] | 72.627 [72.379, 73.629] | 4.8739e-15 |
| `APP-QAOA-LINE-12` | Cirq | accepted | 334 [334, 334] | 122 [122, 122] | 289.35 [286.08, 290.36] | 155.34 [155.33, 155.35] | 6.5402e-15 |
| `APP-QFT-GRID-06` | FlagQuantum | accepted | 75 [75, 75] | 52 [52, 52] | 21.425 [21.355, 21.554] | 153.09 [153.04, 153.11] | 1.8958e-15 |
| `APP-QFT-GRID-06` | Qiskit | accepted | 81 [81, 83] | 56 [56, 58] | 6.8679 [6.7878, 6.8833] | 66.498 [66.465, 66.578] | 3.4294e-15 |
| `APP-QFT-GRID-06` | Cirq | accepted | 81 [81, 81] | 56 [56, 56] | 75.035 [74.932, 75.318] | 144.98 [144.98, 145.02] | 1.6475e-15 |
| `APP-QFT-GRID-08` | FlagQuantum | accepted | 176 [176, 176] | 110 [110, 110] | 35.153 [35.055, 35.306] | 154.73 [154.69, 154.75] | 6.8336e-15 |
| `APP-QFT-GRID-08` | Qiskit | accepted | 152 [138, 152] | 95 [84, 103] | 9.4037 [9.3197, 9.5372] | 68.873 [68.625, 68.879] | 1.2836e-14 |
| `APP-QFT-GRID-08` | Cirq | accepted | 154 [154, 154] | 87 [87, 87] | 151.59 [151.16, 152.36] | 147.93 [147.83, 147.95] | 2.1417e-15 |
| `APP-QFT-GRID-12` | FlagQuantum | accepted | 408 [408, 408] | 191 [191, 191] | 78.442 [78.321, 78.939] | 158.88 [158.87, 159.01] | 8.8674e-15 |
| `APP-QFT-GRID-12` | Qiskit | accepted | 382 [354, 388] | 193 [171, 206] | 18.594 [18.441, 19.411] | 80.936 [79.855, 81.18] | 5.2045e-14 |
| `APP-QFT-GRID-12` | Cirq | accepted | 388 [388, 388] | 176 [176, 176] | 417.3 [414.61, 421.67] | 159.58 [159.56, 159.59] | 2.6011e-15 |
| `APP-QFT-LINE-06` | FlagQuantum | accepted | 117 [117, 117] | 74 [74, 74] | 22.482 [22.347, 22.61] | 153.79 [153.78, 153.84] | 2.9303e-15 |
| `APP-QFT-LINE-06` | Qiskit | accepted | 99 [93, 99] | 76 [67, 76] | 7.4472 [7.3468, 7.5324] | 66.881 [66.379, 67.551] | 1.8395e-14 |
| `APP-QFT-LINE-06` | Cirq | accepted | 95 [95, 95] | 59 [59, 59] | 90.444 [89.81, 90.96] | 145.09 [145.08, 145.87] | 3.1436e-15 |
| `APP-QFT-LINE-08` | FlagQuantum | accepted | 224 [224, 224] | 120 [120, 120] | 38.727 [38.681, 39.194] | 155.6 [155.57, 155.62] | 8.6765e-15 |
| `APP-QFT-LINE-08` | Qiskit | accepted | 180 [180, 186] | 91 [89, 98] | 10.136 [9.9998, 10.309] | 70.125 [69.875, 70.129] | 1.8223e-14 |
| `APP-QFT-LINE-08` | Cirq | accepted | 176 [176, 176] | 88 [88, 88] | 168.87 [167.58, 169.44] | 148.89 [148.58, 148.93] | 4.1998e-15 |
| `APP-QFT-LINE-12` | FlagQuantum | accepted | 534 [534, 534] | 206 [206, 206] | 86.812 [85.984, 87.249] | 160.63 [160.51, 160.77] | 1.1525e-14 |
| `APP-QFT-LINE-12` | Qiskit | accepted | 426 [420, 430] | 146 [134, 154] | 18.479 [18.002, 18.795] | 81.869 [81.613, 82.121] | 5.3786e-14 |
| `APP-QFT-LINE-12` | Cirq | accepted | 410 [410, 410] | 144 [144, 144] | 399.28 [398.59, 404.43] | 159.83 [159.8, 159.85] | 2.4974e-15 |
| `APP-REPETITION-GRID-06` | FlagQuantum | accepted | 72 [72, 72] | 69 [69, 69] | 17.499 [17.394, 17.581] | 153 [152.92, 153.04] | 1.3195e-14 |
| `APP-REPETITION-GRID-06` | Qiskit | accepted | 54 [46, 62] | 45 [42, 56] | 6.2153 [6.0316, 6.3097] | 65.223 [65.027, 65.383] | 5.6839e-15 |
| `APP-REPETITION-GRID-06` | Cirq | accepted | 72 [72, 72] | 55 [55, 55] | 73.269 [72.943, 73.614] | 144.18 [144.17, 144.24] | 1.0854e-14 |
| `APP-REPETITION-GRID-08` | FlagQuantum | accepted | 72 [72, 72] | 61 [61, 61] | 21.771 [21.582, 21.892] | 153.04 [153.02, 153.12] | 7.2478e-15 |
| `APP-REPETITION-GRID-08` | Qiskit | accepted | 86 [82, 94] | 71 [55, 75] | 6.5661 [6.5415, 6.6159] | 66.189 [66.074, 66.414] | 4.7233e-15 |
| `APP-REPETITION-GRID-08` | Cirq | accepted | 90 [90, 90] | 73 [73, 73] | 81.144 [80.813, 81.6] | 144.83 [144.79, 144.87] | 4.0099e-15 |
| `APP-REPETITION-GRID-12` | FlagQuantum | accepted | 96 [96, 96] | 68 [68, 68] | 24.862 [24.749, 25.062] | 153.53 [153.43, 153.55] | 6.1227e-15 |
| `APP-REPETITION-GRID-12` | Qiskit | accepted | 122 [110, 134] | 91 [70, 96] | 7.7153 [7.5412, 7.7915] | 66.881 [66.625, 67.965] | 3.876e-15 |
| `APP-REPETITION-GRID-12` | Cirq | accepted | 134 [134, 134] | 94 [94, 94] | 112.4 [111.91, 113.19] | 146.09 [146.08, 146.84] | 3.5323e-15 |
| `APP-REPETITION-LINE-06` | FlagQuantum | accepted | 96 [96, 96] | 75 [75, 75] | 19.842 [19.722, 19.972] | 153.43 [153.29, 153.43] | 1.7257e-14 |
| `APP-REPETITION-LINE-06` | Qiskit | accepted | 88 [88, 90] | 69 [69, 69] | 7.1792 [7.1167, 7.2893] | 66.139 [66.133, 66.809] | 8.0793e-15 |
| `APP-REPETITION-LINE-06` | Cirq | accepted | 88 [88, 88] | 69 [69, 69] | 97.848 [97.432, 98.506] | 144.84 [144.82, 145.48] | 9.091e-15 |
| `APP-REPETITION-LINE-08` | FlagQuantum | accepted | 102 [102, 102] | 72 [72, 72] | 20.754 [20.677, 20.839] | 153.54 [153.53, 153.66] | 9.7354e-15 |
| `APP-REPETITION-LINE-08` | Qiskit | accepted | 96 [96, 100] | 68 [68, 74] | 7.3712 [7.3322, 7.4363] | 66.633 [66.625, 66.637] | 3.9798e-15 |
| `APP-REPETITION-LINE-08` | Cirq | accepted | 100 [100, 100] | 74 [74, 74] | 105.34 [104.69, 106.28] | 145.35 [145.33, 146.03] | 3.9765e-15 |
| `APP-REPETITION-LINE-12` | FlagQuantum | accepted | 126 [126, 126] | 83 [83, 83] | 23.826 [23.75, 23.88] | 153.63 [153.62, 153.68] | 7.9724e-15 |
| `APP-REPETITION-LINE-12` | Qiskit | accepted | 114 [110, 114] | 71 [67, 71] | 7.9465 [7.8888, 8.1566] | 67.906 [67.125, 67.969] | 2.4746e-15 |
| `APP-REPETITION-LINE-12` | Cirq | accepted | 114 [114, 114] | 71 [71, 71] | 116.73 [115.53, 117.72] | 145.85 [145.83, 146.73] | 2.196e-15 |

## All paired descriptive comparisons

Each ratio is the named numerator divided by denominator. Values below one indicate less of that metric for the numerator on that case only. CZ/depth divide accepted-record medians. Time and memory pair matching block indices and show median [Q1, Q3] of the ten block ratios. These are separate metrics; no combined score, across-case aggregate or overall winner is calculated.

| Case | Numerator / denominator | Both cases complete | CZ ratio | Dependency-depth ratio | Time ratio [Q1, Q3] | Process-memory ratio [Q1, Q3] |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| `APP-HOPPING-GRID-06` | Cirq / FlagQuantum | true | 1.0667 | 1.0349 | 4.4317 [4.382, 4.436] | 0.95294 [0.94987, 0.95302] |
| `APP-HOPPING-GRID-06` | Cirq / Qiskit | true | 1.1163 | 1.141 | 17.441 [17.221, 17.557] | 2.1993 [2.1922, 2.1993] |
| `APP-HOPPING-GRID-06` | FlagQuantum / Qiskit | true | 1.0465 | 1.1026 | 3.9444 [3.9159, 3.9853] | 2.3079 [2.3077, 2.308] |
| `APP-HOPPING-GRID-08` | Cirq / FlagQuantum | true | 1.1216 | 1.1622 | 5.6335 [5.5858, 5.6695] | 0.96797 [0.96791, 0.96799] |
| `APP-HOPPING-GRID-08` | Cirq / Qiskit | true | 1.2029 | 1.217 | 25.99 [25.795, 26.375] | 2.1333 [2.1332, 2.1333] |
| `APP-HOPPING-GRID-08` | FlagQuantum / Qiskit | true | 1.0725 | 1.0472 | 4.6314 [4.5936, 4.6621] | 2.2038 [2.2038, 2.204] |
| `APP-HOPPING-GRID-12` | Cirq / FlagQuantum | true | 1.3121 | 1.2939 | 8.3008 [8.2268, 8.3579] | 1.0384 [1.0377, 1.0385] |
| `APP-HOPPING-GRID-12` | Cirq / Qiskit | true | 1.0607 | 1.0403 | 36.545 [35.704, 36.874] | 2.0128 [2.012, 2.0317] |
| `APP-HOPPING-GRID-12` | FlagQuantum / Qiskit | true | 0.80841 | 0.80403 | 4.3833 [4.3181, 4.4728] | 1.9399 [1.9376, 1.9576] |
| `APP-HOPPING-LINE-06` | Cirq / FlagQuantum | true | 0.91667 | 0.91429 | 4.5325 [4.5143, 4.5408] | 0.9463 [0.94554, 0.94637] |
| `APP-HOPPING-LINE-06` | Cirq / Qiskit | true | 1 | 1 | 18.099 [17.925, 18.207] | 2.1856 [2.1854, 2.1857] |
| `APP-HOPPING-LINE-06` | FlagQuantum / Qiskit | true | 1.0909 | 1.0938 | 4.0024 [3.9959, 4.0297] | 2.3096 [2.3094, 2.3114] |
| `APP-HOPPING-LINE-08` | Cirq / FlagQuantum | true | 0.92857 | 0.92708 | 5.0046 [4.9721, 5.0342] | 0.95054 [0.94624, 0.95097] |
| `APP-HOPPING-LINE-08` | Cirq / Qiskit | true | 1 | 1 | 23.247 [22.998, 23.302] | 2.0998 [2.0882, 2.1011] |
| `APP-HOPPING-LINE-08` | FlagQuantum / Qiskit | true | 1.0769 | 1.0787 | 4.6246 [4.6051, 4.6634] | 2.2087 [2.2067, 2.209] |
| `APP-HOPPING-LINE-12` | Cirq / FlagQuantum | true | 0.95312 | 0.94915 | 6.6038 [6.5446, 6.6369] | 0.97795 [0.97775, 0.97948] |
| `APP-HOPPING-LINE-12` | Cirq / Qiskit | true | 1 | 1 | 33.342 [32.742, 34.095] | 2.0179 [2.0178, 2.018] |
| `APP-HOPPING-LINE-12` | FlagQuantum / Qiskit | true | 1.0492 | 1.0536 | 5.0276 [4.9938, 5.154] | 2.0634 [2.0609, 2.0637] |
| `APP-ISING-GRID-06` | Cirq / FlagQuantum | true | 1.0833 | 1.1786 | 3.6355 [3.6231, 3.6661] | 0.9392 [0.93904, 0.93935] |
| `APP-ISING-GRID-06` | Cirq / Qiskit | true | 1 | 1 | 8.9144 [8.8019, 9.0443] | 2.1974 [2.1971, 2.1979] |
| `APP-ISING-GRID-06` | FlagQuantum / Qiskit | true | 0.92308 | 0.84848 | 2.4495 [2.435, 2.4635] | 2.3398 [2.3393, 2.34] |
| `APP-ISING-GRID-08` | Cirq / FlagQuantum | true | 1.1667 | 1.2581 | 3.8087 [3.7724, 3.8382] | 0.94246 [0.9424, 0.94251] |
| `APP-ISING-GRID-08` | Cirq / Qiskit | true | 1 | 1 | 10.673 [10.567, 10.796] | 2.1865 [2.1864, 2.1867] |
| `APP-ISING-GRID-08` | FlagQuantum / Qiskit | true | 0.85714 | 0.79487 | 2.8135 [2.7674, 2.8295] | 2.3199 [2.3199, 2.3201] |
| `APP-ISING-GRID-12` | Cirq / FlagQuantum | true | 1.2069 | 1.3247 | 5.0849 [5.0628, 5.1339] | 0.95993 [0.95983, 0.96] |
| `APP-ISING-GRID-12` | Cirq / Qiskit | true | 1 | 0.82927 | 17.412 [17.126, 17.704] | 2.1234 [2.1226, 2.1269] |
| `APP-ISING-GRID-12` | FlagQuantum / Qiskit | true | 0.82857 | 0.62602 | 3.4141 [3.3808, 3.4678] | 2.212 [2.2104, 2.212] |
| `APP-ISING-LINE-06` | Cirq / FlagQuantum | true | 0.94872 | 0.81034 | 3.9979 [3.982, 4.0475] | 0.94264 [0.94252, 0.94291] |
| `APP-ISING-LINE-06` | Cirq / Qiskit | true | 1 | 0.92157 | 10.813 [10.696, 10.864] | 2.255 [2.2547, 2.2551] |
| `APP-ISING-LINE-06` | FlagQuantum / Qiskit | true | 1.0541 | 1.1373 | 2.6987 [2.6768, 2.7088] | 2.3921 [2.3916, 2.3923] |
| `APP-ISING-LINE-08` | Cirq / FlagQuantum | true | 1.0392 | 0.97015 | 4.9276 [4.895, 4.9642] | 0.94596 [0.94588, 0.94932] |
| `APP-ISING-LINE-08` | Cirq / Qiskit | true | 1.1042 | 1.2264 | 14.664 [14.362, 14.812] | 2.1897 [2.1896, 2.1983] |
| `APP-ISING-LINE-08` | FlagQuantum / Qiskit | true | 1.0625 | 1.2642 | 2.9467 [2.9051, 3.0324] | 2.315 [2.3149, 2.3159] |
| `APP-ISING-LINE-12` | Cirq / FlagQuantum | true | 0.94872 | 0.89524 | 4.7274 [4.7017, 4.7741] | 0.95994 [0.95989, 0.96001] |
| `APP-ISING-LINE-12` | Cirq / Qiskit | true | 0.925 | 0.88679 | 16.774 [16.337, 17.571] | 2.0994 [2.092, 2.0996] |
| `APP-ISING-LINE-12` | FlagQuantum / Qiskit | true | 0.975 | 0.99057 | 3.5277 [3.4675, 3.6892] | 2.1869 [2.179, 2.1874] |
| `APP-QAOA-GRID-06` | Cirq / FlagQuantum | true | 1.2381 | 1.6667 | 3.9822 [3.9693, 3.9998] | 0.93893 [0.93882, 0.93899] |
| `APP-QAOA-GRID-06` | Cirq / Qiskit | true | 1 | 1 | 7.5522 [7.5391, 7.5702] | 2.2046 [2.2039, 2.2054] |
| `APP-QAOA-GRID-06` | FlagQuantum / Qiskit | true | 0.80769 | 0.6 | 1.8943 [1.891, 1.9152] | 2.3474 [2.3471, 2.3491] |
| `APP-QAOA-GRID-08` | Cirq / FlagQuantum | true | 1.1351 | 1.1522 | 4.9327 [4.9119, 4.9521] | 0.94559 [0.94548, 0.94566] |
| `APP-QAOA-GRID-08` | Cirq / Qiskit | true | 0.93333 | 0.88333 | 10.52 [10.418, 10.858] | 2.241 [2.2401, 2.2575] |
| `APP-QAOA-GRID-08` | FlagQuantum / Qiskit | true | 0.82222 | 0.76667 | 2.1333 [2.0833, 2.2086] | 2.3697 [2.369, 2.3878] |
| `APP-QAOA-GRID-12` | Cirq / FlagQuantum | true | 1.0222 | 0.89247 | 4.8553 [4.8146, 4.8863] | 0.95647 [0.95637, 0.9566] |
| `APP-QAOA-GRID-12` | Cirq / Qiskit | true | 1.0952 | 0.9881 | 16.242 [16.052, 16.413] | 2.1658 [2.1656, 2.1659] |
| `APP-QAOA-GRID-12` | FlagQuantum / Qiskit | true | 1.0714 | 1.1071 | 3.3675 [3.3151, 3.3968] | 2.2644 [2.2641, 2.2645] |
| `APP-QAOA-LINE-06` | Cirq / FlagQuantum | true | 0.97222 | 1.025 | 5.3818 [5.3178, 5.4256] | 0.94481 [0.9443, 0.94487] |
| `APP-QAOA-LINE-06` | Cirq / Qiskit | true | 0.97222 | 1.025 | 10.929 [10.763, 11.143] | 2.1884 [2.1883, 2.1885] |
| `APP-QAOA-LINE-06` | FlagQuantum / Qiskit | true | 1 | 1 | 2.0453 [2.0136, 2.0605] | 2.3162 [2.3161, 2.3175] |
| `APP-QAOA-LINE-08` | Cirq / FlagQuantum | true | 1.1034 | 1.3725 | 6.5696 [6.554, 6.6148] | 0.95559 [0.95525, 0.95563] |
| `APP-QAOA-LINE-08` | Cirq / Qiskit | true | 1.0847 | 1.1667 | 15.64 [15.42, 15.755] | 2.1559 [2.155, 2.158] |
| `APP-QAOA-LINE-08` | FlagQuantum / Qiskit | true | 0.98305 | 0.85 | 2.3723 [2.3486, 2.3953] | 2.2563 [2.2551, 2.2582] |
| `APP-QAOA-LINE-12` | Cirq / FlagQuantum | true | 1.3254 | 1.22 | 8.1677 [8.0658, 8.2085] | 0.99507 [0.99492, 0.99527] |
| `APP-QAOA-LINE-12` | Cirq / Qiskit | true | 1.3047 | 1.1961 | 23.454 [23.075, 23.612] | 2.1388 [2.1169, 2.1392] |
| `APP-QAOA-LINE-12` | FlagQuantum / Qiskit | true | 0.98438 | 0.98039 | 2.8538 [2.8433, 2.8904] | 2.1492 [2.1275, 2.1502] |
| `APP-QFT-GRID-06` | Cirq / FlagQuantum | true | 1.08 | 1.0769 | 3.5043 [3.4793, 3.5113] | 0.94713 [0.94704, 0.94725] |
| `APP-QFT-GRID-06` | Cirq / Qiskit | true | 1 | 1 | 10.932 [10.9, 11.052] | 2.1803 [2.1784, 2.1812] |
| `APP-QFT-GRID-06` | FlagQuantum / Qiskit | true | 0.92593 | 0.92857 | 3.1394 [3.1209, 3.1924] | 2.302 [2.2999, 2.3032] |
| `APP-QFT-GRID-08` | Cirq / FlagQuantum | true | 0.875 | 0.79091 | 4.3086 [4.2896, 4.3279] | 0.95605 [0.95592, 0.95612] |
| `APP-QFT-GRID-08` | Cirq / Qiskit | true | 1.0132 | 0.91579 | 16.02 [15.911, 16.327] | 2.1481 [2.1477, 2.1521] |
| `APP-QFT-GRID-08` | FlagQuantum / Qiskit | true | 1.1579 | 1.1579 | 3.732 [3.6858, 3.7617] | 2.2467 [2.2465, 2.2516] |
| `APP-QFT-GRID-12` | Cirq / FlagQuantum | true | 0.95098 | 0.92147 | 5.3079 [5.2994, 5.3255] | 1.0044 [1.0038, 1.0044] |
| `APP-QFT-GRID-12` | Cirq / Qiskit | true | 1.0157 | 0.91192 | 22.35 [21.783, 22.554] | 1.9716 [1.9659, 1.9857] |
| `APP-QFT-GRID-12` | FlagQuantum / Qiskit | true | 1.0681 | 0.98964 | 4.2171 [4.0776, 4.2522] | 1.963 [1.9588, 1.9768] |
| `APP-QFT-LINE-06` | Cirq / FlagQuantum | true | 0.81197 | 0.7973 | 4.013 [3.9973, 4.062] | 0.94346 [0.94337, 0.9435] |
| `APP-QFT-LINE-06` | Cirq / Qiskit | true | 0.9596 | 0.77632 | 12.122 [12.016, 12.216] | 2.1694 [2.1619, 2.1856] |
| `APP-QFT-LINE-06` | FlagQuantum / Qiskit | true | 1.1818 | 0.97368 | 3.0292 [3.0077, 3.0517] | 2.2998 [2.2832, 2.3167] |
| `APP-QFT-LINE-08` | Cirq / FlagQuantum | true | 0.78571 | 0.73333 | 4.3209 [4.303, 4.3661] | 0.9569 [0.95505, 0.95697] |
| `APP-QFT-LINE-08` | Cirq / Qiskit | true | 0.97778 | 0.96703 | 16.671 [16.221, 16.799] | 2.1233 [2.1201, 2.1247] |
| `APP-QFT-LINE-08` | FlagQuantum / Qiskit | true | 1.2444 | 1.3187 | 3.8029 [3.7449, 3.8849] | 2.2191 [2.2189, 2.2202] |
| `APP-QFT-LINE-12` | Cirq / FlagQuantum | true | 0.76779 | 0.69903 | 4.6214 [4.5847, 4.6405] | 0.99497 [0.99488, 0.99557] |
| `APP-QFT-LINE-12` | Cirq / Qiskit | true | 0.96244 | 0.9863 | 21.693 [21.392, 22.074] | 1.9521 [1.948, 1.9527] |
| `APP-QFT-LINE-12` | FlagQuantum / Qiskit | true | 1.2535 | 1.411 | 4.6779 [4.6205, 4.7878] | 1.9614 [1.9585, 1.9623] |
| `APP-REPETITION-GRID-06` | Cirq / FlagQuantum | true | 1 | 0.7971 | 4.1921 [4.1665, 4.233] | 0.94233 [0.94221, 0.94279] |
| `APP-REPETITION-GRID-06` | Cirq / Qiskit | true | 1.3333 | 1.2222 | 11.819 [11.625, 12.191] | 2.2108 [2.2069, 2.2135] |
| `APP-REPETITION-GRID-06` | FlagQuantum / Qiskit | true | 1.3333 | 1.5333 | 2.7957 [2.7848, 2.8749] | 2.3464 [2.3422, 2.3491] |
| `APP-REPETITION-GRID-08` | Cirq / FlagQuantum | true | 1.25 | 1.1967 | 3.7226 [3.7176, 3.7457] | 0.94635 [0.94628, 0.94646] |
| `APP-REPETITION-GRID-08` | Cirq / Qiskit | true | 1.0465 | 1.0282 | 12.381 [12.339, 12.415] | 2.1884 [2.1867, 2.1918] |
| `APP-REPETITION-GRID-08` | FlagQuantum / Qiskit | true | 0.83721 | 0.85915 | 3.3276 [3.289, 3.3345] | 2.3122 [2.3109, 2.316] |
| `APP-REPETITION-GRID-12` | Cirq / FlagQuantum | true | 1.3958 | 1.3824 | 4.5221 [4.4932, 4.535] | 0.95154 [0.9515, 0.952] |
| `APP-REPETITION-GRID-12` | Cirq / Qiskit | true | 1.0984 | 1.033 | 14.571 [14.417, 14.907] | 2.1844 [2.162, 2.1926] |
| `APP-REPETITION-GRID-12` | FlagQuantum / Qiskit | true | 0.78689 | 0.74725 | 3.2335 [3.1765, 3.2988] | 2.2957 [2.2714, 2.304] |
| `APP-REPETITION-LINE-06` | Cirq / FlagQuantum | true | 0.91667 | 0.92 | 4.9371 [4.8877, 4.9636] | 0.94419 [0.94402, 0.94485] |
| `APP-REPETITION-LINE-06` | Cirq / Qiskit | true | 1 | 1 | 13.596 [13.519, 13.675] | 2.1899 [2.1711, 2.1901] |
| `APP-REPETITION-LINE-06` | FlagQuantum / Qiskit | true | 1.0909 | 1.087 | 2.7651 [2.7211, 2.8023] | 2.3185 [2.297, 2.3198] |
| `APP-REPETITION-LINE-08` | Cirq / FlagQuantum | true | 0.98039 | 1.0278 | 5.0803 [5.0297, 5.1262] | 0.94668 [0.94659, 0.95092] |
| `APP-REPETITION-LINE-08` | Cirq / Qiskit | true | 1.0417 | 1.0882 | 14.301 [14.198, 14.408] | 2.1814 [2.1812, 2.1913] |
| `APP-REPETITION-LINE-08` | FlagQuantum / Qiskit | true | 1.0625 | 1.0588 | 2.809 [2.787, 2.8525] | 2.3042 [2.3041, 2.3052] |
| `APP-REPETITION-LINE-12` | Cirq / FlagQuantum | true | 0.90476 | 0.85542 | 4.8918 [4.8457, 4.9519] | 0.94935 [0.94924, 0.95471] |
| `APP-REPETITION-LINE-12` | Cirq / Qiskit | true | 1 | 1 | 14.542 [14.399, 14.789] | 2.1601 [2.1464, 2.1697] |
| `APP-REPETITION-LINE-12` | FlagQuantum / Qiskit | true | 1.1053 | 1.169 | 2.9894 [2.9341, 3.0045] | 2.2626 [2.261, 2.2823] |

## Reproduce acceptance and comparisons

Use a clean checkout of the pinned SDKBench harness, install its independent evaluator requirements, and extract the retained archive into a fresh directory. Participant SDKs are unnecessary for replay. Binary/source build admission needs the original full GitHub artifact described in the index; semantic replay uses the durable raw archive.

```bash
tar -xJf docs/analysis/evidence/compiler-ordinary-44587635615.tar.xz -C /path/to/fresh-evidence
PYTHONPATH=src python -m sdkbench.candidates.cli replay \
  --directory /path/to/fresh-evidence/campaign \
  --bundle /path/to/fresh-evidence/preparation/cohort
PYTHONPATH=src python tools/compare_compiler_applications.py \
  --profile ordinary \
  --directory /path/to/fresh-evidence/campaign \
  --bundle /path/to/fresh-evidence/preparation/cohort \
  --output /path/to/new-comparisons.json
```

Expected: 900 blocks replayed, 90 case/participant outcomes, and 90 case/pair comparisons. Output paths must be new. Complete raw evidence, not rounded Markdown values, is authoritative. Build observation, kernel-policy consistency and local freeze/draw ordering do not establish independent build attestation or host qualification. Publication eligibility remains false pending the protocol's separate review and attestation requirements.
