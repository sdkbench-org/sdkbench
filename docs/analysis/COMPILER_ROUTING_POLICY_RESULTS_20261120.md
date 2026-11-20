# Native routing-policy results (2026-11-20)

120/120 complete case/policy pairs passed this engineering campaign. All 30 cases, four policies and six unordered pairs per case remain reported. This is a same-revision policy control, not a cross-SDK ranking or a publication-qualified performance claim.

The [prospective declaration](COMPILER_ROUTING_POLICY_DECLARATION_20261120.md) specifies the question and unchanged acceptance. This supplies later held-out evidence for acceptance item 4 of the approved automatic-routing proposal. Its original before-merge timing requirement was unmet; this study cannot retroactively establish it.

## Immutable execution and evidence

- [Workflow run](https://github.com/sdkbench-org/sdkbench/actions/runs/44623673659), attempt 1. One hosted execution, no campaign rerun or redraw.
- Compiler `858df9dbd5ba964e8e59b3383304547710a1dee5`; harness `9ce37f85bef327603bc64f63eec7e0fddc9436ef`. The harness passed 14 exact-head CI checks and was merged in `9aa9260920984e2ca05bcb293abb885fccd9c144` before dispatch on its retained feature ref.
- Freeze `2026-11-19T22:00:18.318533+00:00`; draw `2026-11-19T22:00:18.325170+00:00`. These are recorded events, not independently attested timestamps.
- [Pre-dispatch receipt](evidence/compiler-routing-policies-44623673659-pre-dispatch.json), [evidence index](evidence/compiler-routing-policies-44623673659-index.json), [complete raw archive](evidence/compiler-routing-policies-44623673659.tar.xz), [verification](evidence/compiler-routing-policies-44623673659-verification.json), [resource/layout audit](evidence/compiler-routing-policies-44623673659-layout-resources.json), [120-outcome summary](evidence/compiler-routing-policies-44623673659-summary.json.gz) and [180 pair rows](evidence/compiler-routing-policies-44623673659-comparisons.json).

- Original workflow conclusion: `success`; [complete terminal job steps](evidence/compiler-routing-policies-44623673659-github-jobs.json) retain any orchestration, replay, upload or cleanup failure separately from case acceptance.

The initial sandbox transport could not connect to the GitHub API. A run-history query verified that no new run existed before one network-enabled dispatch succeeded. Both transport attempts and the query are retained in the receipt. No study draw or worker was rerun.

The archive contains 3,808 original files, including every one of 3,605 campaign manifest entries; every retained member was hash-verified. All requests, responses, warmups, measurements, supervisor controls and failures remain unchanged. Build binaries and extracted source remain in the original hash-pinned GitHub artifact until `2027-02-17T21:56:01Z`; the durable Git archive omits them and explicitly records this retention limit.

Local replay denied participant SDK imports, regenerated preparation using the retained nonce, verified 1,200 blocks and 3,600 expected measured records, and matched every hosted pair metric and coverage entry. The local and hosted maximum semantic-error values are both retained. Substituting only the retained hosted error maxima reconstructs the exact hosted summary digest; the local summary is never rewritten. See the [reconciliation proof](evidence/compiler-routing-policies-44623673659-summary-reconciliation.json).

## Controlled workflow and acceptance

The omitted default and explicit `restore_after_each_gate`, `persistent_layout` and `sabre` use one source build and installed wheel, one host and one newly drawn cohort. Only the native routing keyword changes. Both admission and reporting verify identical source/build/dependency/configuration/environment evidence after normalizing that keyword and workflow identity. Raw `/proc/cpuinfo` hashes remain retained but are excluded from host equality because observed CPU frequencies vary.

Every workflow builds the same native circuit, calls ordinary `compiler.compile`, legalizes native gates and applies the same timed spanning-tree identity restoration. Identity input and delivered output layouts are required. `sabre_layout` is excluded because it changes the initial-layout contract. This path does not invoke target-artifact construction or CZ block resynthesis. Qiskit and Cirq are installed in the shared environment but are not study participants.

Host: `AMD EPYC 7763 64-Core Processor`; `Linux-7.0.0-1017-azure-x86_64-with-glibc2.39`; Python `3.12.14`. One pinned CPU, one numerical thread, 16 GiB, socket/io-uring denial, two warmups and three measurements in each of ten blocks. The per-compilation ceiling remains 120 seconds; width-specific cumulative case limits, the 270-minute measurement step and 360-minute job ceiling are unchanged.

The [cross-campaign host review](evidence/compiler-routing-policies-44623673659-host-qualification.json) retains the recorded host facts and unchanged minima for all three studies.

Recorded logical CPU count: `4`; allowed CPU indices: `[0, 1, 2, 3]`. The protocol requires at least eight physical cores and 64 GiB host memory. A logical CPU count below eight cannot meet that physical-core minimum. The registration does not establish host RAM, inactive SMT siblings, exclusive physical-host load or independent attestation. These host-qualification gaps are not waived; process affinity and resource limits are separate recorded controls. This is an engineering study with `publication_eligible=false`.

QAOA, Ising evolution, hopping, QFT and repetition at widths 6/8/12 on line/grid targets produce 30 cases. The same ten-block order rotation is retained: four policies occupy each position two or three times, not exactly balanced. No simultaneous participant workers are permitted. Timing includes native construction, compilation, legalization, export and restoration; process memory includes imports, warmups and all measured work. It is not isolated router latency or compiler workspace.

The target is full CZ plus arbitrary one-qubit unitaries on declared undirected edges without ancillas. Unchanged independent checks require semantic absolute error at most `1e-8`, zero relative tolerance, normalization error at most `1e-10`, zero target violations and identity final placement. Six-qubit cases use complete operators up to one global phase; widths 8/12 use three complete probe outputs up to a phase per probe, not universal equivalence proofs.

The native automatic selector preserves its established route objective; it does not promise minimum emitted CZ count, dependency depth, compilation time or process memory. The adapter retains emitted operations and placement, but not the selected internal candidate metadata. Equal delivered metrics do not independently establish which internal strategy was selected. A causal stage attribution requires separate profiling or an explicitly declared ablation.

The other SDKBench application campaigns use different cohorts and hosts. No cross-campaign improvement ratio, favorable policy selection or per-pass causal claim is made. No global SDK ranking, GPU/QPU/distributed claim or universal superiority follows from this study.

## Observed tradeoffs

All 120 complete outcomes passed, including 3,600 measured records and 2,400 warmups. The following examples explain distinct tradeoffs; the complete tables remain authoritative, and these examples are not a ranking or a new selection rule.

- In `APP-QFT-LINE-12`, default auto emits 534 CZ gates with dependency depth 206, compared with 2,010 / 1,760 for explicit restore-after-each-gate and 1,560 / 473 for persistent layout. Explicit SABRE also emits 534 / 206. Default versus restore-after-each-gate has paired workflow-time ratio 0.52625 and process-memory ratio 0.86188. These are same-revision delivered-workflow observations; they do not isolate an implementation change or prove which candidate auto chose.
- In `APP-HOPPING-GRID-06`, default emits 74 CZ gates with depth 55; explicit SABRE emits 80 with depth 52. Auto reduces CZ count by 7.5% while increasing dependency depth by 5.77%. The selector's route objective does not guarantee minimum delivered dependency depth.
- In `APP-HOPPING-GRID-12`, default and persistent layout have equal CZ counts and dependency depths, but the default workflow-time ratio is 1.1019 [1.0852, 1.1079]. The measured 10.2% median latency cost remains reported. This does not attribute the difference to an internal phase without profiling.

Policy choice is therefore a quality/time tradeoff on the declared task and delivered-layout contract. Equal process-memory values include SDK imports and must not be read as equal compiler workspace. No new tuning, favorable per-case policy selection, threshold change or rerun follows from inspecting these outcomes.

## Complete coverage

| Workflow | Accepted complete cases | Other complete outcomes | Accepted measured records / expected |
| --- | ---: | --- | ---: |
| `flagquantum-ordinary-restored` | 30/30 | none | 900/900 |
| `flagquantum-restore-after-each-gate-restored` | 30/30 | none | 900/900 |
| `flagquantum-persistent-layout-restored` | 30/30 | none | 900/900 |
| `flagquantum-sabre-restored` | 30/30 | none | 900/900 |

Retained warmups: 2400/2,400. Failed warmups, timeout, memory, isolation, unsupported and semantic failures remain in coverage. No paired ratio is admitted when either complete case fails. Conditional diagnostics do not erase failure.

Retained measured-phase result records: 3600/3,600 expected; independently accepted records: 3600. Error and supervisor-produced failure records remain results, not successful measured compilations.

## Every case and policy

CZ and dependency depth show median [minimum, maximum] across accepted records. Time is milliseconds: median [Q1, Q3] of the ten three-measurement block medians. Memory is MiB: median [minimum, maximum] of ten supervised process peaks. Maximum semantic error covers measured records. Quartiles describe variation, not confidence intervals or significance.

| Case | Policy | Status | Full CZ | Two-body dependency depth | Workflow time, ms | Process peak, MiB | Maximum semantic error |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| `APP-HOPPING-GRID-06` | Default (auto) | accepted | 74 [74, 74] | 55 [55, 55] | 52.806 [52.766, 53.194] | 153.29 [153.16, 153.3] | 1.3118e-14 |
| `APP-HOPPING-GRID-06` | Restore after each gate | accepted | 104 [104, 104] | 88 [88, 88] | 62.075 [61.714, 62.976] | 153.41 [153.39, 153.48] | 1.7991e-14 |
| `APP-HOPPING-GRID-06` | Persistent layout | accepted | 74 [74, 74] | 55 [55, 55] | 48.209 [47.981, 48.476] | 153.24 [153.18, 153.29] | 1.3118e-14 |
| `APP-HOPPING-GRID-06` | SABRE | accepted | 80 [80, 80] | 52 [52, 52] | 52.296 [51.919, 52.549] | 153.36 [153.29, 153.4] | 1.3889e-14 |
| `APP-HOPPING-GRID-08` | Default (auto) | accepted | 132 [132, 132] | 93 [93, 93] | 73.922 [73.253, 75.5] | 154.33 [154.27, 154.39] | 7.7829e-15 |
| `APP-HOPPING-GRID-08` | Restore after each gate | accepted | 240 [240, 240] | 222 [222, 222] | 93.779 [91.805, 96.035] | 156.02 [155.79, 156.03] | 1.4387e-14 |
| `APP-HOPPING-GRID-08` | Persistent layout | accepted | 132 [132, 132] | 93 [93, 93] | 67.795 [67.296, 69.652] | 154.27 [154.26, 154.28] | 7.7829e-15 |
| `APP-HOPPING-GRID-08` | SABRE | accepted | 138 [138, 138] | 99 [99, 99] | 75.975 [74.114, 78.319] | 154.53 [154.48, 154.54] | 8.4035e-15 |
| `APP-HOPPING-GRID-12` | Default (auto) | accepted | 346 [346, 346] | 269 [269, 269] | 149.07 [148.12, 149.23] | 157.89 [157.75, 158.1] | 2.7091e-14 |
| `APP-HOPPING-GRID-12` | Restore after each gate | accepted | 736 [736, 736] | 700 [700, 700] | 209.86 [200.48, 211.56] | 164.1 [163.87, 164.14] | 5.7019e-14 |
| `APP-HOPPING-GRID-12` | Persistent layout | accepted | 346 [346, 346] | 269 [269, 269] | 134.98 [134.6, 135.57] | 157.84 [157.75, 158.04] | 2.7091e-14 |
| `APP-HOPPING-GRID-12` | SABRE | accepted | 346 [346, 346] | 269 [269, 269] | 145.23 [141.59, 146.53] | 157.99 [157.75, 158.08] | 2.7369e-14 |
| `APP-HOPPING-LINE-06` | Default (auto) | accepted | 56 [56, 56] | 40 [40, 40] | 47.06 [46.688, 47.287] | 152.91 [152.79, 153.03] | 9.447e-15 |
| `APP-HOPPING-LINE-06` | Restore after each gate | accepted | 56 [56, 56] | 40 [40, 40] | 45.841 [45.435, 46.459] | 152.91 [152.8, 152.93] | 9.447e-15 |
| `APP-HOPPING-LINE-06` | Persistent layout | accepted | 56 [56, 56] | 40 [40, 40] | 46.289 [45.648, 46.741] | 152.98 [152.79, 152.98] | 9.447e-15 |
| `APP-HOPPING-LINE-06` | SABRE | accepted | 56 [56, 56] | 40 [40, 40] | 46.373 [46.059, 47.113] | 152.95 [152.9, 153.05] | 1.0009e-14 |
| `APP-HOPPING-LINE-08` | Default (auto) | accepted | 96 [96, 96] | 76 [76, 76] | 66.817 [66.442, 67.358] | 153.64 [153.54, 153.64] | 6.1072e-15 |
| `APP-HOPPING-LINE-08` | Restore after each gate | accepted | 96 [96, 96] | 76 [76, 76] | 65.434 [64.902, 65.839] | 153.58 [153.53, 153.59] | 6.1072e-15 |
| `APP-HOPPING-LINE-08` | Persistent layout | accepted | 96 [96, 96] | 76 [76, 76] | 65.148 [65.009, 66.661] | 153.53 [153.52, 153.61] | 6.1072e-15 |
| `APP-HOPPING-LINE-08` | SABRE | accepted | 96 [96, 96] | 76 [76, 76] | 66.229 [65.559, 66.93] | 153.61 [153.54, 153.64] | 6.0326e-15 |
| `APP-HOPPING-LINE-12` | Default (auto) | accepted | 256 [256, 256] | 237 [237, 237] | 127.45 [124.46, 128.84] | 156.44 [156.24, 156.56] | 2.0471e-14 |
| `APP-HOPPING-LINE-12` | Restore after each gate | accepted | 256 [256, 256] | 237 [237, 237] | 119.45 [117.47, 123.6] | 156.53 [156.36, 156.58] | 2.0471e-14 |
| `APP-HOPPING-LINE-12` | Persistent layout | accepted | 256 [256, 256] | 237 [237, 237] | 119.89 [118.63, 122.6] | 156.53 [156.25, 156.55] | 2.0471e-14 |
| `APP-HOPPING-LINE-12` | SABRE | accepted | 256 [256, 256] | 237 [237, 237] | 123.54 [120.3, 124.86] | 156.52 [156.24, 156.53] | 2.0805e-14 |
| `APP-ISING-GRID-06` | Default (auto) | accepted | 48 [48, 48] | 30 [30, 30] | 26.843 [26.771, 27.074] | 152.6 [152.4, 152.61] | 4.2935e-15 |
| `APP-ISING-GRID-06` | Restore after each gate | accepted | 102 [102, 102] | 96 [96, 96] | 29.921 [29.644, 30.347] | 153.79 [153.65, 153.8] | 9.0347e-15 |
| `APP-ISING-GRID-06` | Persistent layout | accepted | 66 [66, 66] | 60 [60, 60] | 30.011 [29.631, 30.416] | 152.79 [152.78, 152.93] | 5.9993e-15 |
| `APP-ISING-GRID-06` | SABRE | accepted | 48 [48, 48] | 30 [30, 30] | 26.174 [26.009, 26.733] | 152.59 [152.41, 152.6] | 4.2935e-15 |
| `APP-ISING-GRID-08` | Default (auto) | accepted | 72 [72, 72] | 38 [38, 38] | 36.425 [36.134, 36.877] | 153.15 [153.14, 153.29] | 5.474e-15 |
| `APP-ISING-GRID-08` | Restore after each gate | accepted | 150 [150, 150] | 109 [109, 109] | 41.038 [40.161, 41.627] | 154.18 [154.15, 154.23] | 1.0298e-14 |
| `APP-ISING-GRID-08` | Persistent layout | accepted | 120 [120, 120] | 98 [98, 98] | 44.205 [43.345, 44.455] | 153.67 [153.61, 153.68] | 8.2779e-15 |
| `APP-ISING-GRID-08` | SABRE | accepted | 72 [72, 72] | 38 [38, 38] | 35.626 [35.558, 35.834] | 153.23 [153.22, 153.37] | 5.474e-15 |
| `APP-ISING-GRID-12` | Default (auto) | accepted | 174 [174, 174] | 64 [64, 64] | 70.141 [69.635, 72.018] | 155.09 [155.06, 155.15] | 7.7595e-15 |
| `APP-ISING-GRID-12` | Restore after each gate | accepted | 498 [498, 498] | 343 [343, 343] | 89.619 [87.474, 90.867] | 160.14 [159.89, 160.15] | 2.1723e-14 |
| `APP-ISING-GRID-12` | Persistent layout | accepted | 462 [462, 462] | 378 [378, 378] | 98.505 [97.981, 99.011] | 159.52 [159.41, 159.53] | 2.0114e-14 |
| `APP-ISING-GRID-12` | SABRE | accepted | 174 [174, 174] | 64 [64, 64] | 70.299 [68.324, 72.083] | 155.07 [155.03, 155.09] | 7.7595e-15 |
| `APP-ISING-LINE-06` | Default (auto) | accepted | 48 [48, 48] | 32 [32, 32] | 26.686 [26.4, 26.893] | 152.6 [152.54, 152.65] | 4.6818e-15 |
| `APP-ISING-LINE-06` | Restore after each gate | accepted | 138 [138, 138] | 120 [120, 120] | 34.055 [33.34, 34.186] | 153.79 [153.79, 153.86] | 1.2426e-14 |
| `APP-ISING-LINE-06` | Persistent layout | accepted | 126 [126, 126] | 111 [111, 111] | 32.95 [32.857, 33.46] | 153.68 [153.66, 153.79] | 1.1458e-14 |
| `APP-ISING-LINE-06` | SABRE | accepted | 48 [48, 48] | 32 [32, 32] | 25.947 [25.692, 26.167] | 152.6 [152.41, 152.61] | 4.6818e-15 |
| `APP-ISING-LINE-08` | Default (auto) | accepted | 90 [90, 90] | 49 [49, 49] | 39.021 [38.815, 39.249] | 153.54 [153.53, 153.54] | 6.0201e-15 |
| `APP-ISING-LINE-08` | Restore after each gate | accepted | 258 [258, 258] | 177 [177, 177] | 53.493 [51.68, 54.26] | 156.12 [155.9, 156.13] | 1.6978e-14 |
| `APP-ISING-LINE-08` | Persistent layout | accepted | 228 [228, 228] | 184 [184, 184] | 50.454 [48.945, 51.223] | 155.59 [155.56, 155.62] | 1.5185e-14 |
| `APP-ISING-LINE-08` | SABRE | accepted | 90 [90, 90] | 49 [49, 49] | 38.225 [37.985, 38.494] | 153.53 [153.43, 153.57] | 6.0201e-15 |
| `APP-ISING-LINE-12` | Default (auto) | accepted | 222 [222, 222] | 105 [105, 105] | 67.962 [67.094, 69.013] | 155.89 [155.87, 155.91] | 1.0227e-14 |
| `APP-ISING-LINE-12` | Restore after each gate | accepted | 948 [948, 948] | 571 [571, 571] | 192.44 [191.39, 195.42] | 166.98 [166.87, 168.14] | 4.1722e-14 |
| `APP-ISING-LINE-12` | Persistent layout | accepted | 1050 [1050, 1050] | 1003 [1003, 1003] | 153.15 [149.39, 154.77] | 170 [169.42, 170.09] | 4.4883e-14 |
| `APP-ISING-LINE-12` | SABRE | accepted | 222 [222, 222] | 105 [105, 105] | 65.482 [64.977, 68.275] | 155.87 [155.84, 155.9] | 1.0227e-14 |
| `APP-QAOA-GRID-06` | Default (auto) | accepted | 42 [42, 42] | 28 [28, 28] | 18.279 [18.2, 18.483] | 152.34 [152.15, 152.42] | 1.8809e-15 |
| `APP-QAOA-GRID-06` | Restore after each gate | accepted | 48 [48, 48] | 36 [36, 36] | 16.346 [16.085, 16.421] | 152.29 [152.28, 152.42] | 2.1557e-15 |
| `APP-QAOA-GRID-06` | Persistent layout | accepted | 72 [72, 72] | 56 [56, 56] | 19.337 [19.09, 19.464] | 152.79 [152.78, 152.86] | 3.0353e-15 |
| `APP-QAOA-GRID-06` | SABRE | accepted | 42 [42, 42] | 28 [28, 28] | 17.686 [17.513, 18.19] | 152.29 [152.18, 152.37] | 1.8809e-15 |
| `APP-QAOA-GRID-08` | Default (auto) | accepted | 62 [62, 62] | 34 [34, 34] | 29.538 [28.806, 29.724] | 152.9 [152.8, 152.91] | 2.2593e-15 |
| `APP-QAOA-GRID-08` | Restore after each gate | accepted | 104 [104, 104] | 80 [80, 80] | 25.883 [25.38, 26.11] | 153.41 [153.4, 153.54] | 3.9111e-15 |
| `APP-QAOA-GRID-08` | Persistent layout | accepted | 110 [110, 110] | 71 [71, 71] | 31.071 [30.987, 31.699] | 153.68 [153.61, 153.77] | 4.3885e-15 |
| `APP-QAOA-GRID-08` | SABRE | accepted | 62 [62, 62] | 34 [34, 34] | 28.794 [28.407, 29.156] | 152.9 [152.8, 152.91] | 2.2593e-15 |
| `APP-QAOA-GRID-12` | Default (auto) | accepted | 132 [132, 132] | 66 [66, 66] | 51.972 [51.126, 53.045] | 153.98 [153.98, 154] | 3.2486e-15 |
| `APP-QAOA-GRID-12` | Restore after each gate | accepted | 300 [300, 300] | 256 [256, 256] | 60.517 [58.358, 61.217] | 156.9 [156.64, 156.91] | 7.055e-15 |
| `APP-QAOA-GRID-12` | Persistent layout | accepted | 312 [312, 312] | 211 [211, 211] | 62.634 [60.973, 63.868] | 157.03 [156.77, 157.11] | 7.529e-15 |
| `APP-QAOA-GRID-12` | SABRE | accepted | 132 [132, 132] | 66 [66, 66] | 50.195 [49.813, 51.19] | 153.96 [153.89, 153.98] | 3.2486e-15 |
| `APP-QAOA-LINE-06` | Default (auto) | accepted | 66 [66, 66] | 33 [33, 33] | 22.211 [21.826, 22.327] | 152.8 [152.66, 152.9] | 2.6946e-15 |
| `APP-QAOA-LINE-06` | Restore after each gate | accepted | 108 [108, 108] | 100 [100, 100] | 26.214 [26.031, 26.448] | 153.55 [153.52, 153.66] | 4.6501e-15 |
| `APP-QAOA-LINE-06` | Persistent layout | accepted | 120 [120, 120] | 82 [82, 82] | 28.646 [28.497, 29.023] | 153.43 [153.37, 153.54] | 5.189e-15 |
| `APP-QAOA-LINE-06` | SABRE | accepted | 66 [66, 66] | 33 [33, 33] | 21.049 [20.88, 21.153] | 152.79 [152.66, 152.91] | 2.6946e-15 |
| `APP-QAOA-LINE-08` | Default (auto) | accepted | 110 [110, 110] | 59 [59, 59] | 32.415 [32.132, 32.747] | 153.66 [153.65, 153.74] | 4.127e-15 |
| `APP-QAOA-LINE-08` | Restore after each gate | accepted | 188 [188, 188] | 174 [174, 174] | 40.836 [40.384, 41.164] | 154.74 [154.73, 154.75] | 6.8751e-15 |
| `APP-QAOA-LINE-08` | Persistent layout | accepted | 200 [200, 200] | 114 [114, 114] | 42.859 [42.281, 43.016] | 154.93 [154.87, 154.93] | 7.3775e-15 |
| `APP-QAOA-LINE-08` | SABRE | accepted | 110 [110, 110] | 59 [59, 59] | 31.587 [31.094, 32.423] | 153.66 [153.64, 153.69] | 4.127e-15 |
| `APP-QAOA-LINE-12` | Default (auto) | accepted | 294 [294, 294] | 118 [118, 118] | 68.181 [65.558, 68.511] | 156.84 [156.65, 156.85] | 7.0654e-15 |
| `APP-QAOA-LINE-12` | Restore after each gate | accepted | 516 [516, 516] | 496 [496, 496] | 85.262 [84.261, 88.178] | 160.15 [160.04, 160.16] | 1.227e-14 |
| `APP-QAOA-LINE-12` | Persistent layout | accepted | 636 [636, 636] | 308 [308, 308] | 99.963 [97.622, 103.59] | 161.78 [161.77, 161.92] | 1.5332e-14 |
| `APP-QAOA-LINE-12` | SABRE | accepted | 294 [294, 294] | 118 [118, 118] | 66.275 [64.474, 67.105] | 156.82 [156.64, 156.92] | 7.0654e-15 |
| `APP-QFT-GRID-06` | Default (auto) | accepted | 75 [75, 75] | 52 [52, 52] | 39.064 [38.39, 39.318] | 153.1 [153.04, 153.16] | 1.8958e-15 |
| `APP-QFT-GRID-06` | Restore after each gate | accepted | 171 [171, 171] | 152 [152, 152] | 43.079 [42.627, 44.187] | 154.43 [154.43, 154.49] | 4.1442e-15 |
| `APP-QFT-GRID-06` | Persistent layout | accepted | 105 [105, 105] | 84 [84, 84] | 39.276 [39.135, 39.675] | 153.54 [153.53, 153.59] | 2.5087e-15 |
| `APP-QFT-GRID-06` | SABRE | accepted | 75 [75, 75] | 52 [52, 52] | 38.26 [38.091, 38.9] | 153.09 [153.04, 153.15] | 1.8958e-15 |
| `APP-QFT-GRID-08` | Default (auto) | accepted | 176 [176, 176] | 110 [110, 110] | 64.075 [63.369, 64.837] | 154.74 [154.73, 154.88] | 1.0542e-14 |
| `APP-QFT-GRID-08` | Restore after each gate | accepted | 380 [380, 380] | 325 [325, 325] | 79.131 [76.612, 79.302] | 157.98 [157.89, 158.15] | 2.1996e-14 |
| `APP-QFT-GRID-08` | Persistent layout | accepted | 278 [278, 278] | 193 [193, 193] | 76.074 [73.175, 76.402] | 156.49 [156.29, 156.53] | 1.6156e-14 |
| `APP-QFT-GRID-08` | SABRE | accepted | 176 [176, 176] | 110 [110, 110] | 62.635 [62.001, 63.107] | 154.74 [154.74, 154.86] | 1.0542e-14 |
| `APP-QFT-GRID-12` | Default (auto) | accepted | 408 [408, 408] | 191 [191, 191] | 138.86 [135.12, 139.44] | 158.88 [158.88, 159.02] | 8.1038e-15 |
| `APP-QFT-GRID-12` | Restore after each gate | accepted | 1134 [1134, 1134] | 898 [898, 898] | 200.79 [192.57, 204.68] | 171.12 [171.04, 171.25] | 2.214e-14 |
| `APP-QFT-GRID-12` | Persistent layout | accepted | 990 [990, 990] | 525 [525, 525] | 201.38 [198.97, 206.8] | 167.93 [167.88, 168.04] | 1.9551e-14 |
| `APP-QFT-GRID-12` | SABRE | accepted | 408 [408, 408] | 191 [191, 191] | 137.81 [136.72, 138.5] | 159.02 [158.9, 159.03] | 8.1038e-15 |
| `APP-QFT-LINE-06` | Default (auto) | accepted | 117 [117, 117] | 74 [74, 74] | 40.217 [39.792, 40.685] | 153.8 [153.79, 153.8] | 2.9303e-15 |
| `APP-QFT-LINE-06` | Restore after each gate | accepted | 267 [267, 267] | 236 [236, 236] | 53.659 [53.549, 54.661] | 156.1 [155.9, 156.13] | 6.1521e-15 |
| `APP-QFT-LINE-06` | Persistent layout | accepted | 177 [177, 177] | 113 [113, 113] | 43.817 [43.775, 44.426] | 154.51 [154.48, 154.54] | 4.2221e-15 |
| `APP-QFT-LINE-06` | SABRE | accepted | 117 [117, 117] | 74 [74, 74] | 39.124 [37.932, 39.34] | 153.79 [153.79, 153.85] | 2.9303e-15 |
| `APP-QFT-LINE-08` | Default (auto) | accepted | 224 [224, 224] | 120 [120, 120] | 67.37 [66.651, 68.445] | 155.6 [155.59, 155.73] | 1.2716e-14 |
| `APP-QFT-LINE-08` | Restore after each gate | accepted | 620 [620, 620] | 540 [540, 540] | 104.22 [103.21, 107.74] | 161.87 [161.63, 161.92] | 3.4083e-14 |
| `APP-QFT-LINE-08` | Persistent layout | accepted | 440 [440, 440] | 209 [209, 209] | 85.79 [82.821, 86.524] | 158.9 [158.8, 159.04] | 2.4285e-14 |
| `APP-QFT-LINE-08` | SABRE | accepted | 224 [224, 224] | 120 [120, 120] | 67.182 [65.529, 68.694] | 155.63 [155.61, 155.64] | 1.2716e-14 |
| `APP-QFT-LINE-12` | Default (auto) | accepted | 534 [534, 534] | 206 [206, 206] | 154.26 [152.21, 154.93] | 160.63 [160.52, 160.77] | 1.0433e-14 |
| `APP-QFT-LINE-12` | Restore after each gate | accepted | 2010 [2010, 2010] | 1760 [1760, 1760] | 291.2 [288.92, 296.95] | 186.38 [186.32, 186.41] | 4.0043e-14 |
| `APP-QFT-LINE-12` | Persistent layout | accepted | 1560 [1560, 1560] | 473 [473, 473] | 306.89 [305.23, 310.2] | 178.34 [178.21, 178.46] | 3.0707e-14 |
| `APP-QFT-LINE-12` | SABRE | accepted | 534 [534, 534] | 206 [206, 206] | 152.63 [148.81, 153.31] | 160.58 [160.51, 160.77] | 1.0433e-14 |
| `APP-REPETITION-GRID-06` | Default (auto) | accepted | 54 [54, 54] | 47 [47, 47] | 35.154 [35.023, 35.418] | 152.65 [152.64, 152.79] | 1.0199e-14 |
| `APP-REPETITION-GRID-06` | Restore after each gate | accepted | 102 [102, 102] | 89 [89, 89] | 34.552 [34.273, 34.977] | 153.48 [153.42, 153.49] | 1.7449e-14 |
| `APP-REPETITION-GRID-06` | Persistent layout | accepted | 108 [108, 108] | 90 [90, 90] | 30.965 [30.637, 31.132] | 153.6 [153.54, 153.61] | 1.8619e-14 |
| `APP-REPETITION-GRID-06` | SABRE | accepted | 54 [54, 54] | 47 [47, 47] | 34.614 [34.301, 34.863] | 152.66 [152.55, 152.73] | 1.0199e-14 |
| `APP-REPETITION-GRID-08` | Default (auto) | accepted | 78 [78, 78] | 74 [74, 74] | 32.938 [32.632, 33.22] | 153.14 [153.04, 153.15] | 8.3359e-15 |
| `APP-REPETITION-GRID-08` | Restore after each gate | accepted | 138 [138, 138] | 117 [117, 117] | 40.102 [38.96, 40.509] | 153.79 [153.78, 153.82] | 1.3782e-14 |
| `APP-REPETITION-GRID-08` | Persistent layout | accepted | 126 [126, 126] | 114 [114, 114] | 40.812 [40.49, 41.503] | 153.64 [153.6, 153.65] | 1.2427e-14 |
| `APP-REPETITION-GRID-08` | SABRE | accepted | 78 [78, 78] | 74 [74, 74] | 32.121 [31.287, 32.798] | 153.15 [153.04, 153.15] | 8.3359e-15 |
| `APP-REPETITION-GRID-12` | Default (auto) | accepted | 78 [78, 78] | 64 [64, 64] | 41.232 [40.766, 41.877] | 153.14 [153.14, 153.23] | 5.2564e-15 |
| `APP-REPETITION-GRID-12` | Restore after each gate | accepted | 222 [222, 222] | 191 [191, 191] | 48.909 [48.232, 49.81] | 155.42 [155.37, 155.51] | 1.4643e-14 |
| `APP-REPETITION-GRID-12` | Persistent layout | accepted | 180 [180, 180] | 153 [153, 153] | 47.996 [47.679, 48.641] | 154.59 [154.57, 154.61] | 1.1356e-14 |
| `APP-REPETITION-GRID-12` | SABRE | accepted | 78 [78, 78] | 64 [64, 64] | 40.211 [39.799, 40.524] | 153.29 [153.14, 153.41] | 5.2564e-15 |
| `APP-REPETITION-LINE-06` | Default (auto) | accepted | 72 [72, 72] | 63 [63, 63] | 31.695 [31.516, 31.957] | 153.09 [153.04, 153.1] | 1.2888e-14 |
| `APP-REPETITION-LINE-06` | Restore after each gate | accepted | 150 [150, 150] | 143 [143, 143] | 39.957 [39.532, 41.132] | 154.04 [154.02, 154.04] | 2.5148e-14 |
| `APP-REPETITION-LINE-06` | Persistent layout | accepted | 126 [126, 126] | 118 [118, 118] | 40.471 [40.162, 40.938] | 153.6 [153.55, 153.66] | 2.1748e-14 |
| `APP-REPETITION-LINE-06` | SABRE | accepted | 72 [72, 72] | 63 [63, 63] | 30.795 [29.711, 31.232] | 152.91 [152.9, 153.05] | 1.2888e-14 |
| `APP-REPETITION-LINE-08` | Default (auto) | accepted | 114 [114, 114] | 79 [79, 79] | 38.576 [38.322, 38.901] | 153.79 [153.78, 153.84] | 1.1559e-14 |
| `APP-REPETITION-LINE-08` | Restore after each gate | accepted | 306 [306, 306] | 255 [255, 255] | 59.907 [58.062, 60.807] | 156.73 [156.7, 156.87] | 3.0009e-14 |
| `APP-REPETITION-LINE-08` | Persistent layout | accepted | 312 [312, 312] | 225 [225, 225] | 63.451 [61.394, 63.764] | 156.88 [156.54, 156.9] | 3.0898e-14 |
| `APP-REPETITION-LINE-08` | SABRE | accepted | 114 [114, 114] | 79 [79, 79] | 37.701 [37.512, 38.254] | 153.79 [153.74, 153.8] | 1.1559e-14 |
| `APP-REPETITION-LINE-12` | Default (auto) | accepted | 144 [144, 144] | 89 [89, 89] | 43.114 [41.914, 43.379] | 154.03 [154.03, 154.04] | 9.9588e-15 |
| `APP-REPETITION-LINE-12` | Restore after each gate | accepted | 522 [522, 522] | 492 [492, 492] | 84.026 [82.92, 84.671] | 160.03 [160.02, 160.17] | 3.3044e-14 |
| `APP-REPETITION-LINE-12` | Persistent layout | accepted | 258 [258, 258] | 180 [180, 180] | 58.161 [56.36, 59.01] | 155.98 [155.79, 156.04] | 1.663e-14 |
| `APP-REPETITION-LINE-12` | SABRE | accepted | 144 [144, 144] | 89 [89, 89] | 42.449 [42.02, 43.319] | 153.98 [153.98, 153.99] | 9.9588e-15 |

## All paired descriptive comparisons

Ratios divide the named numerator by denominator. Below one means less of that metric on that case. Count/depth ratios divide accepted medians; time/memory pair matching block indices and report median [Q1, Q3]. No combined score or across-case winner is calculated. Zero or missing values remain undefined.

| Case | Numerator / denominator | Both cases complete | CZ ratio | Dependency-depth ratio | Time ratio [Q1, Q3] | Process-memory ratio [Q1, Q3] |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| `APP-HOPPING-GRID-06` | Default (auto) / Persistent layout | true | 1 | 1 | 1.0948 [1.0889, 1.1035] | 1.0001 [0.99954, 1.0003] |
| `APP-HOPPING-GRID-06` | Default (auto) / Restore after each gate | true | 0.71154 | 0.625 | 0.8506 [0.83604, 0.85636] | 0.99908 [0.99859, 0.99929] |
| `APP-HOPPING-GRID-06` | Default (auto) / SABRE | true | 0.925 | 1.0577 | 1.0086 [1.0017, 1.0256] | 0.99933 [0.99882, 0.99969] |
| `APP-HOPPING-GRID-06` | Persistent layout / Restore after each gate | true | 0.71154 | 0.625 | 0.77673 [0.76712, 0.77827] | 0.99894 [0.99877, 0.99913] |
| `APP-HOPPING-GRID-06` | Persistent layout / SABRE | true | 0.925 | 1.0577 | 0.92301 [0.91708, 0.9414] | 0.99927 [0.99917, 0.99954] |
| `APP-HOPPING-GRID-06` | Restore after each gate / SABRE | true | 1.3 | 1.6923 | 1.1941 [1.1794, 1.2141] | 1.0004 [1.0002, 1.0006] |
| `APP-HOPPING-GRID-08` | Default (auto) / Persistent layout | true | 1 | 1 | 1.0839 [1.0695, 1.103] | 1.0004 [1.0001, 1.0004] |
| `APP-HOPPING-GRID-08` | Default (auto) / Restore after each gate | true | 0.55 | 0.41892 | 0.79605 [0.77241, 0.79917] | 0.98937 [0.98917, 0.98973] |
| `APP-HOPPING-GRID-08` | Default (auto) / SABRE | true | 0.95652 | 0.93939 | 0.97401 [0.94085, 1.0082] | 0.99874 [0.99869, 0.99876] |
| `APP-HOPPING-GRID-08` | Persistent layout / Restore after each gate | true | 0.55 | 0.41892 | 0.72827 [0.70401, 0.75442] | 0.98881 [0.98875, 0.98964] |
| `APP-HOPPING-GRID-08` | Persistent layout / SABRE | true | 0.95652 | 0.93939 | 0.89123 [0.85465, 0.93129] | 0.99833 [0.99833, 0.99863] |
| `APP-HOPPING-GRID-08` | Restore after each gate / SABRE | true | 1.7391 | 2.2424 | 1.2226 [1.2099, 1.2695] | 1.0096 [1.0088, 1.0099] |
| `APP-HOPPING-GRID-12` | Default (auto) / Persistent layout | true | 1 | 1 | 1.1019 [1.0852, 1.1079] | 1.0005 [0.99998, 1.0017] |
| `APP-HOPPING-GRID-12` | Default (auto) / Restore after each gate | true | 0.47011 | 0.38429 | 0.71015 [0.69926, 0.7345] | 0.96244 [0.96188, 0.96356] |
| `APP-HOPPING-GRID-12` | Default (auto) / SABRE | true | 1 | 1 | 1.0205 [1.0135, 1.0577] | 0.99947 [0.99908, 1.0004] |
| `APP-HOPPING-GRID-12` | Persistent layout / Restore after each gate | true | 0.47011 | 0.38429 | 0.64592 [0.64324, 0.67463] | 0.96196 [0.96192, 0.96201] |
| `APP-HOPPING-GRID-12` | Persistent layout / SABRE | true | 1 | 1 | 0.936 [0.92585, 0.95598] | 0.99889 [0.9985, 0.99979] |
| `APP-HOPPING-GRID-12` | Restore after each gate / SABRE | true | 2.1272 | 2.6022 | 1.452 [1.3882, 1.4607] | 1.0385 [1.0378, 1.039] |
| `APP-HOPPING-LINE-06` | Default (auto) / Persistent layout | true | 1 | 1 | 1.0194 [1.0034, 1.0375] | 0.99962 [0.99955, 1.0001] |
| `APP-HOPPING-LINE-06` | Default (auto) / Restore after each gate | true | 1 | 1 | 1.0266 [1.0152, 1.0316] | 1.0001 [0.99996, 1.0004] |
| `APP-HOPPING-LINE-06` | Default (auto) / SABRE | true | 1 | 1 | 1.0159 [0.9996, 1.0288] | 0.99997 [0.99922, 1.0001] |
| `APP-HOPPING-LINE-06` | Persistent layout / Restore after each gate | true | 1 | 1 | 1.0101 [0.99189, 1.0176] | 1.0004 [1.0001, 1.0005] |
| `APP-HOPPING-LINE-06` | Persistent layout / SABRE | true | 1 | 1 | 0.99611 [0.96899, 0.99883] | 0.99963 [0.99955, 1.0002] |
| `APP-HOPPING-LINE-06` | Restore after each gate / SABRE | true | 1 | 1 | 0.98163 [0.97308, 1.0029] | 0.9994 [0.99915, 0.99995] |
| `APP-HOPPING-LINE-08` | Default (auto) / Persistent layout | true | 1 | 1 | 1.0228 [1.0098, 1.0278] | 1.0004 [1.0002, 1.0007] |
| `APP-HOPPING-LINE-08` | Default (auto) / Restore after each gate | true | 1 | 1 | 1.0206 [1.0108, 1.0323] | 1.0004 [1.0003, 1.0004] |
| `APP-HOPPING-LINE-08` | Default (auto) / SABRE | true | 1 | 1 | 1.0076 [0.99638, 1.0225] | 1 [0.99996, 1.0003] |
| `APP-HOPPING-LINE-08` | Persistent layout / Restore after each gate | true | 1 | 1 | 1.0041 [0.99315, 1.0334] | 0.99964 [0.9996, 1.0002] |
| `APP-HOPPING-LINE-08` | Persistent layout / SABRE | true | 1 | 1 | 0.99074 [0.9765, 1.0152] | 0.99978 [0.99942, 0.99985] |
| `APP-HOPPING-LINE-08` | Restore after each gate / SABRE | true | 1 | 1 | 0.98382 [0.97687, 0.99335] | 0.99972 [0.99959, 1] |
| `APP-HOPPING-LINE-12` | Default (auto) / Persistent layout | true | 1 | 1 | 1.0484 [1.0263, 1.083] | 0.99999 [0.99883, 1] |
| `APP-HOPPING-LINE-12` | Default (auto) / Restore after each gate | true | 1 | 1 | 1.0505 [1.0118, 1.1004] | 0.99935 [0.99833, 1] |
| `APP-HOPPING-LINE-12` | Default (auto) / SABRE | true | 1 | 1 | 1.0502 [0.99182, 1.0621] | 1 [0.99893, 1.0009] |
| `APP-HOPPING-LINE-12` | Persistent layout / Restore after each gate | true | 1 | 1 | 1.0058 [0.97935, 1.021] | 0.99996 [0.99991, 1] |
| `APP-HOPPING-LINE-12` | Persistent layout / SABRE | true | 1 | 1 | 0.97379 [0.95209, 0.99098] | 1.0001 [1.0001, 1.001] |
| `APP-HOPPING-LINE-12` | Restore after each gate / SABRE | true | 1 | 1 | 0.96995 [0.95308, 1.0267] | 1.0001 [1.0001, 1.0012] |
| `APP-ISING-GRID-06` | Default (auto) / Persistent layout | true | 0.72727 | 0.5 | 0.89732 [0.88731, 0.91574] | 0.99816 [0.99759, 0.9988] |
| `APP-ISING-GRID-06` | Default (auto) / Restore after each gate | true | 0.47059 | 0.3125 | 0.89779 [0.88504, 0.91218] | 0.99219 [0.99189, 0.99225] |
| `APP-ISING-GRID-06` | Default (auto) / SABRE | true | 1 | 1 | 1.0254 [1.0151, 1.0317] | 1 [0.99972, 1.0002] |
| `APP-ISING-GRID-06` | Persistent layout / Restore after each gate | true | 0.64706 | 0.625 | 0.99987 [0.97954, 1.0201] | 0.99388 [0.99342, 0.99435] |
| `APP-ISING-GRID-06` | Persistent layout / SABRE | true | 1.375 | 2 | 1.1358 [1.1195, 1.175] | 1.0014 [1.0012, 1.0023] |
| `APP-ISING-GRID-06` | Restore after each gate / SABRE | true | 2.125 | 3.2 | 1.1359 [1.1116, 1.152] | 1.0079 [1.007, 1.0081] |
| `APP-ISING-GRID-08` | Default (auto) / Persistent layout | true | 0.6 | 0.38776 | 0.83518 [0.82367, 0.84432] | 0.99657 [0.99657, 0.99711] |
| `APP-ISING-GRID-08` | Default (auto) / Restore after each gate | true | 0.48 | 0.34862 | 0.88755 [0.87686, 0.91972] | 0.9933 [0.99327, 0.99377] |
| `APP-ISING-GRID-08` | Default (auto) / SABRE | true | 1 | 1 | 1.0202 [1.0097, 1.0458] | 0.99948 [0.99945, 0.99949] |
| `APP-ISING-GRID-08` | Persistent layout / Restore after each gate | true | 0.8 | 0.89908 | 1.0841 [1.0436, 1.1151] | 0.99668 [0.99644, 0.9967] |
| `APP-ISING-GRID-08` | Persistent layout / SABRE | true | 1.6667 | 2.5789 | 1.2402 [1.2291, 1.245] | 1.0026 [1.0023, 1.0029] |
| `APP-ISING-GRID-08` | Restore after each gate / SABRE | true | 2.0833 | 2.8684 | 1.1451 [1.1048, 1.1757] | 1.0062 [1.0056, 1.0063] |
| `APP-ISING-GRID-12` | Default (auto) / Persistent layout | true | 0.37662 | 0.16931 | 0.71511 [0.69502, 0.73575] | 0.97237 [0.97221, 0.9728] |
| `APP-ISING-GRID-12` | Default (auto) / Restore after each gate | true | 0.3494 | 0.18659 | 0.77918 [0.77275, 0.7986] | 0.96861 [0.96845, 0.96908] |
| `APP-ISING-GRID-12` | Default (auto) / SABRE | true | 1 | 1 | 0.99611 [0.9585, 1.048] | 1.0002 [1.0001, 1.0004] |
| `APP-ISING-GRID-12` | Persistent layout / Restore after each gate | true | 0.92771 | 1.102 | 1.1065 [1.0637, 1.1297] | 0.99618 [0.99562, 0.99669] |
| `APP-ISING-GRID-12` | Persistent layout / SABRE | true | 2.6552 | 5.9062 | 1.4109 [1.373, 1.4394] | 1.0287 [1.0281, 1.0287] |
| `APP-ISING-GRID-12` | Restore after each gate / SABRE | true | 2.8621 | 5.3594 | 1.2495 [1.2245, 1.3234] | 1.0326 [1.0319, 1.0329] |
| `APP-ISING-LINE-06` | Default (auto) / Persistent layout | true | 0.38095 | 0.28829 | 0.80528 [0.79903, 0.82144] | 0.99297 [0.99264, 0.99301] |
| `APP-ISING-LINE-06` | Default (auto) / Restore after each gate | true | 0.34783 | 0.26667 | 0.78966 [0.77513, 0.80026] | 0.99223 [0.99192, 0.99225] |
| `APP-ISING-LINE-06` | Default (auto) / SABRE | true | 1 | 1 | 1.0327 [1.0255, 1.0373] | 1 [1, 1.0004] |
| `APP-ISING-LINE-06` | Persistent layout / Restore after each gate | true | 0.91304 | 0.925 | 0.97202 [0.95982, 0.98829] | 0.99928 [0.99921, 0.99954] |
| `APP-ISING-LINE-06` | Persistent layout / SABRE | true | 2.625 | 3.4688 | 1.2792 [1.2574, 1.294] | 1.0073 [1.0071, 1.0074] |
| `APP-ISING-LINE-06` | Restore after each gate / SABRE | true | 2.875 | 3.75 | 1.2937 [1.2912, 1.3181] | 1.0078 [1.0078, 1.0082] |
| `APP-ISING-LINE-08` | Default (auto) / Persistent layout | true | 0.39474 | 0.2663 | 0.7784 [0.76601, 0.7973] | 0.98679 [0.98663, 0.98697] |
| `APP-ISING-LINE-08` | Default (auto) / Restore after each gate | true | 0.34884 | 0.27684 | 0.73305 [0.72336, 0.74517] | 0.98344 [0.9834, 0.98368] |
| `APP-ISING-LINE-08` | Default (auto) / SABRE | true | 1 | 1 | 1.0169 [1.0092, 1.0318] | 1.0001 [1, 1.0001] |
| `APP-ISING-LINE-08` | Persistent layout / Restore after each gate | true | 0.88372 | 1.0395 | 0.94442 [0.9285, 0.97136] | 0.99657 [0.9964, 0.99702] |
| `APP-ISING-LINE-08` | Persistent layout / SABRE | true | 2.5333 | 3.7551 | 1.3184 [1.2807, 1.3371] | 1.0135 [1.0132, 1.0136] |
| `APP-ISING-LINE-08` | Restore after each gate / SABRE | true | 2.8667 | 3.6122 | 1.4046 [1.352, 1.4203] | 1.0169 [1.0165, 1.0169] |
| `APP-ISING-LINE-12` | Default (auto) / Persistent layout | true | 0.21143 | 0.10469 | 0.44497 [0.4406, 0.45022] | 0.91702 [0.91667, 0.92013] |
| `APP-ISING-LINE-12` | Default (auto) / Restore after each gate | true | 0.23418 | 0.18389 | 0.35205 [0.34022, 0.35591] | 0.93358 [0.93313, 0.93384] |
| `APP-ISING-LINE-12` | Default (auto) / SABRE | true | 1 | 1 | 1.0149 [0.98333, 1.0633] | 1.0001 [1, 1.0002] |
| `APP-ISING-LINE-12` | Persistent layout / Restore after each gate | true | 1.1076 | 1.7566 | 0.78023 [0.76507, 0.79553] | 1.0164 [1.0142, 1.0185] |
| `APP-ISING-LINE-12` | Persistent layout / SABRE | true | 4.7297 | 9.5524 | 2.2918 [2.2285, 2.3921] | 1.0907 [1.087, 1.0909] |
| `APP-ISING-LINE-12` | Restore after each gate / SABRE | true | 4.2703 | 5.4381 | 2.9392 [2.8144, 3.005] | 1.0714 [1.0709, 1.0717] |
| `APP-QAOA-GRID-06` | Default (auto) / Persistent layout | true | 0.58333 | 0.5 | 0.94428 [0.934, 0.96576] | 0.99664 [0.99609, 0.99702] |
| `APP-QAOA-GRID-06` | Default (auto) / Restore after each gate | true | 0.875 | 0.77778 | 1.123 [1.0776, 1.1375] | 1.0002 [0.99923, 1.0004] |
| `APP-QAOA-GRID-06` | Default (auto) / SABRE | true | 1 | 1 | 1.036 [0.99606, 1.0419] | 1.0002 [0.9998, 1.0004] |
| `APP-QAOA-GRID-06` | Persistent layout / Restore after each gate | true | 1.5 | 1.5556 | 1.1683 [1.154, 1.2] | 1.0033 [1.0032, 1.0036] |
| `APP-QAOA-GRID-06` | Persistent layout / SABRE | true | 1.7143 | 2 | 1.0878 [1.0439, 1.108] | 1.0033 [1.0032, 1.0038] |
| `APP-QAOA-GRID-06` | Restore after each gate / SABRE | true | 1.1429 | 1.2857 | 0.90445 [0.86042, 0.94792] | 1.0001 [0.99994, 1.0006] |
| `APP-QAOA-GRID-08` | Default (auto) / Persistent layout | true | 0.56364 | 0.47887 | 0.93909 [0.91556, 0.95952] | 0.99499 [0.99497, 0.99503] |
| `APP-QAOA-GRID-08` | Default (auto) / Restore after each gate | true | 0.59615 | 0.425 | 1.1386 [1.1104, 1.1695] | 0.99644 [0.9962, 0.99676] |
| `APP-QAOA-GRID-08` | Default (auto) / SABRE | true | 1 | 1 | 1.0118 [0.9915, 1.0446] | 1 [1, 1] |
| `APP-QAOA-GRID-08` | Persistent layout / Restore after each gate | true | 1.0577 | 0.8875 | 1.2196 [1.1991, 1.2298] | 1.0018 [1.0012, 1.0018] |
| `APP-QAOA-GRID-08` | Persistent layout / SABRE | true | 1.7742 | 2.0882 | 1.0936 [1.0836, 1.0988] | 1.005 [1.005, 1.0051] |
| `APP-QAOA-GRID-08` | Restore after each gate / SABRE | true | 1.6774 | 2.3529 | 0.89769 [0.88424, 0.90381] | 1.0035 [1.0033, 1.0039] |
| `APP-QAOA-GRID-12` | Default (auto) / Persistent layout | true | 0.42308 | 0.3128 | 0.84281 [0.80204, 0.86547] | 0.98065 [0.98058, 0.98181] |
| `APP-QAOA-GRID-12` | Default (auto) / Restore after each gate | true | 0.44 | 0.25781 | 0.8609 [0.83936, 0.92058] | 0.98143 [0.9814, 0.98145] |
| `APP-QAOA-GRID-12` | Default (auto) / SABRE | true | 1 | 1 | 1.0254 [1.0236, 1.0513] | 1.0002 [1, 1.0005] |
| `APP-QAOA-GRID-12` | Persistent layout / Restore after each gate | true | 1.04 | 0.82422 | 1.0437 [1.0079, 1.0792] | 1.0008 [0.99963, 1.001] |
| `APP-QAOA-GRID-12` | Persistent layout / SABRE | true | 2.3636 | 3.197 | 1.2465 [1.2149, 1.2766] | 1.0199 [1.0188, 1.0203] |
| `APP-QAOA-GRID-12` | Restore after each gate / SABRE | true | 2.2727 | 3.8788 | 1.1976 [1.1557, 1.2121] | 1.019 [1.0189, 1.0194] |
| `APP-QAOA-LINE-06` | Default (auto) / Persistent layout | true | 0.55 | 0.40244 | 0.76864 [0.7536, 0.78293] | 0.99593 [0.99584, 0.99619] |
| `APP-QAOA-LINE-06` | Default (auto) / Restore after each gate | true | 0.61111 | 0.33 | 0.83834 [0.83522, 0.85282] | 0.99514 [0.99473, 0.99538] |
| `APP-QAOA-LINE-06` | Default (auto) / SABRE | true | 1 | 1 | 1.0531 [1.0412, 1.0681] | 1.0002 [1, 1.0007] |
| `APP-QAOA-LINE-06` | Persistent layout / Restore after each gate | true | 1.1111 | 0.82 | 1.0848 [1.082, 1.1137] | 0.99916 [0.99907, 0.99931] |
| `APP-QAOA-LINE-06` | Persistent layout / SABRE | true | 1.8182 | 2.4848 | 1.3683 [1.3602, 1.3848] | 1.0043 [1.0041, 1.0048] |
| `APP-QAOA-LINE-06` | Restore after each gate / SABRE | true | 1.6364 | 3.0303 | 1.2533 [1.2327, 1.2613] | 1.0052 [1.0049, 1.0057] |
| `APP-QAOA-LINE-08` | Default (auto) / Persistent layout | true | 0.55 | 0.51754 | 0.75867 [0.75315, 0.7749] | 0.99182 [0.99179, 0.99197] |
| `APP-QAOA-LINE-08` | Default (auto) / Restore after each gate | true | 0.58511 | 0.33908 | 0.79852 [0.78472, 0.80765] | 0.99303 [0.99298, 0.99322] |
| `APP-QAOA-LINE-08` | Default (auto) / SABRE | true | 1 | 1 | 1.0243 [1.0174, 1.0358] | 1 [0.99997, 1.0002] |
| `APP-QAOA-LINE-08` | Persistent layout / Restore after each gate | true | 1.0638 | 0.65517 | 1.0458 [1.0348, 1.0774] | 1.0012 [1.0012, 1.0012] |
| `APP-QAOA-LINE-08` | Persistent layout / SABRE | true | 1.8182 | 1.9322 | 1.3413 [1.3192, 1.3559] | 1.0082 [1.0081, 1.0083] |
| `APP-QAOA-LINE-08` | Restore after each gate / SABRE | true | 1.7091 | 2.9492 | 1.2786 [1.2609, 1.3126] | 1.007 [1.007, 1.0071] |
| `APP-QAOA-LINE-12` | Default (auto) / Persistent layout | true | 0.46226 | 0.38312 | 0.66432 [0.65407, 0.68952] | 0.96947 [0.96939, 0.9695] |
| `APP-QAOA-LINE-12` | Default (auto) / Restore after each gate | true | 0.56977 | 0.2379 | 0.77456 [0.76638, 0.81959] | 0.97936 [0.97927, 0.97942] |
| `APP-QAOA-LINE-12` | Default (auto) / SABRE | true | 1 | 1 | 1.0268 [1.0033, 1.0361] | 1.0001 [0.99984, 1.0009] |
| `APP-QAOA-LINE-12` | Persistent layout / Restore after each gate | true | 1.2326 | 0.62097 | 1.1677 [1.1542, 1.1746] | 1.0102 [1.0101, 1.0102] |
| `APP-QAOA-LINE-12` | Persistent layout / SABRE | true | 2.1633 | 2.6102 | 1.5314 [1.5026, 1.5557] | 1.0316 [1.0315, 1.0324] |
| `APP-QAOA-LINE-12` | Restore after each gate / SABRE | true | 1.7551 | 4.2034 | 1.3059 [1.27, 1.3327] | 1.0212 [1.0211, 1.0215] |
| `APP-QFT-GRID-06` | Default (auto) / Persistent layout | true | 0.71429 | 0.61905 | 0.98929 [0.98096, 0.9991] | 0.99696 [0.99678, 0.99712] |
| `APP-QFT-GRID-06` | Default (auto) / Restore after each gate | true | 0.4386 | 0.34211 | 0.89711 [0.88322, 0.92226] | 0.99102 [0.991, 0.99137] |
| `APP-QFT-GRID-06` | Default (auto) / SABRE | true | 1 | 1 | 1.0237 [1.0004, 1.03] | 1 [0.9997, 1.0003] |
| `APP-QFT-GRID-06` | Persistent layout / Restore after each gate | true | 0.61404 | 0.55263 | 0.90822 [0.89965, 0.91872] | 0.99423 [0.99417, 0.99449] |
| `APP-QFT-GRID-06` | Persistent layout / SABRE | true | 1.4 | 1.6154 | 1.0179 [1.008, 1.0407] | 1.0032 [1.003, 1.0033] |
| `APP-QFT-GRID-06` | Restore after each gate / SABRE | true | 2.28 | 2.9231 | 1.1148 [1.1034, 1.149] | 1.0089 [1.0088, 1.0091] |
| `APP-QFT-GRID-08` | Default (auto) / Persistent layout | true | 0.63309 | 0.56995 | 0.84258 [0.82902, 0.88127] | 0.98921 [0.98871, 0.98941] |
| `APP-QFT-GRID-08` | Default (auto) / Restore after each gate | true | 0.46316 | 0.33846 | 0.8213 [0.8025, 0.84249] | 0.97978 [0.97911, 0.97995] |
| `APP-QFT-GRID-08` | Default (auto) / SABRE | true | 1 | 1 | 1.024 [0.98583, 1.0364] | 0.99994 [0.99965, 1] |
| `APP-QFT-GRID-08` | Persistent layout / Restore after each gate | true | 0.73158 | 0.59385 | 0.95793 [0.93288, 1.0029] | 0.99031 [0.98998, 0.99092] |
| `APP-QFT-GRID-08` | Persistent layout / SABRE | true | 1.5795 | 1.7545 | 1.2065 [1.1606, 1.2345] | 1.0113 [1.0104, 1.0115] |
| `APP-QFT-GRID-08` | Restore after each gate / SABRE | true | 2.1591 | 2.9545 | 1.2654 [1.209, 1.2787] | 1.0208 [1.0204, 1.0216] |
| `APP-QFT-GRID-12` | Default (auto) / Persistent layout | true | 0.41212 | 0.36381 | 0.67362 [0.66199, 0.69544] | 0.94608 [0.94567, 0.94642] |
| `APP-QFT-GRID-12` | Default (auto) / Restore after each gate | true | 0.35979 | 0.21269 | 0.70011 [0.65736, 0.72221] | 0.92856 [0.92845, 0.92871] |
| `APP-QFT-GRID-12` | Default (auto) / SABRE | true | 1 | 1 | 1.0027 [0.98671, 1.0114] | 0.99915 [0.99907, 0.99988] |
| `APP-QFT-GRID-12` | Persistent layout / Restore after each gate | true | 0.87302 | 0.58463 | 1.0095 [0.97871, 1.0519] | 0.98154 [0.98122, 0.98182] |
| `APP-QFT-GRID-12` | Persistent layout / SABRE | true | 2.4265 | 2.7487 | 1.4773 [1.4431, 1.5073] | 1.0565 [1.0563, 1.0565] |
| `APP-QFT-GRID-12` | Restore after each gate / SABRE | true | 2.7794 | 4.7016 | 1.4634 [1.4132, 1.495] | 1.0763 [1.0761, 1.0767] |
| `APP-QFT-LINE-06` | Default (auto) / Persistent layout | true | 0.66102 | 0.65487 | 0.9113 [0.90067, 0.9287] | 0.99536 [0.99518, 0.99552] |
| `APP-QFT-LINE-06` | Default (auto) / Restore after each gate | true | 0.4382 | 0.31356 | 0.74509 [0.73868, 0.76175] | 0.98524 [0.98509, 0.98553] |
| `APP-QFT-LINE-06` | Default (auto) / SABRE | true | 1 | 1 | 1.0311 [1.0223, 1.0576] | 1 [0.99968, 1] |
| `APP-QFT-LINE-06` | Persistent layout / Restore after each gate | true | 0.66292 | 0.47881 | 0.81863 [0.78893, 0.82525] | 0.98993 [0.98958, 0.99003] |
| `APP-QFT-LINE-06` | Persistent layout / SABRE | true | 1.5128 | 1.527 | 1.1213 [1.1066, 1.1627] | 1.0045 [1.0045, 1.0048] |
| `APP-QFT-LINE-06` | Restore after each gate / SABRE | true | 2.2821 | 3.1892 | 1.3771 [1.366, 1.4308] | 1.0148 [1.0144, 1.0151] |
| `APP-QFT-LINE-08` | Default (auto) / Persistent layout | true | 0.50909 | 0.57416 | 0.79443 [0.7844, 0.81031] | 0.9796 [0.97925, 0.97983] |
| `APP-QFT-LINE-08` | Default (auto) / Restore after each gate | true | 0.36129 | 0.22222 | 0.64957 [0.63529, 0.65846] | 0.96148 [0.96113, 0.96221] |
| `APP-QFT-LINE-08` | Default (auto) / SABRE | true | 1 | 1 | 1.0048 [0.97849, 1.0294] | 0.99985 [0.99972, 0.9999] |
| `APP-QFT-LINE-08` | Persistent layout / Restore after each gate | true | 0.70968 | 0.38704 | 0.80627 [0.79449, 0.83382] | 0.98164 [0.98146, 0.9824] |
| `APP-QFT-LINE-08` | Persistent layout / SABRE | true | 1.9643 | 1.7417 | 1.2578 [1.2425, 1.2971] | 1.0209 [1.0203, 1.0211] |
| `APP-QFT-LINE-08` | Restore after each gate / SABRE | true | 2.7679 | 4.5 | 1.5385 [1.5052, 1.6501] | 1.0401 [1.0393, 1.0403] |
| `APP-QFT-LINE-12` | Default (auto) / Persistent layout | true | 0.34231 | 0.43552 | 0.49745 [0.48674, 0.50425] | 0.90079 [0.90056, 0.90089] |
| `APP-QFT-LINE-12` | Default (auto) / Restore after each gate | true | 0.26567 | 0.11705 | 0.52625 [0.50399, 0.53222] | 0.86188 [0.86177, 0.86208] |
| `APP-QFT-LINE-12` | Default (auto) / SABRE | true | 1 | 1 | 1.0146 [0.98093, 1.0216] | 1.0004 [0.99944, 1.0007] |
| `APP-QFT-LINE-12` | Persistent layout / Restore after each gate | true | 0.77612 | 0.26875 | 1.0536 [1.0258, 1.0701] | 0.95689 [0.95674, 0.95705] |
| `APP-QFT-LINE-12` | Persistent layout / SABRE | true | 2.9213 | 2.2961 | 2.0097 [1.9994, 2.1248] | 1.1104 [1.1099, 1.1109] |
| `APP-QFT-LINE-12` | Restore after each gate / SABRE | true | 3.764 | 8.5437 | 1.9316 [1.908, 1.9792] | 1.1605 [1.1596, 1.1611] |
| `APP-REPETITION-GRID-06` | Default (auto) / Persistent layout | true | 0.5 | 0.52222 | 1.1435 [1.1213, 1.153] | 0.994 [0.99382, 0.9944] |
| `APP-REPETITION-GRID-06` | Default (auto) / Restore after each gate | true | 0.52941 | 0.52809 | 1.0181 [1.0134, 1.0297] | 0.99474 [0.99455, 0.99537] |
| `APP-REPETITION-GRID-06` | Default (auto) / SABRE | true | 1 | 1 | 1.0183 [1.0069, 1.0271] | 1.0003 [0.99997, 1.0006] |
| `APP-REPETITION-GRID-06` | Persistent layout / Restore after each gate | true | 1.0588 | 1.0112 | 0.89643 [0.8873, 0.90569] | 1.0008 [1.0007, 1.0008] |
| `APP-REPETITION-GRID-06` | Persistent layout / SABRE | true | 2 | 1.9149 | 0.89167 [0.87669, 0.90156] | 1.0062 [1.0062, 1.0062] |
| `APP-REPETITION-GRID-06` | Restore after each gate / SABRE | true | 1.8889 | 1.8936 | 0.99583 [0.98638, 1.0073] | 1.0054 [1.0054, 1.0055] |
| `APP-REPETITION-GRID-08` | Default (auto) / Persistent layout | true | 0.61905 | 0.64912 | 0.80057 [0.78759, 0.82045] | 0.99672 [0.9967, 0.99682] |
| `APP-REPETITION-GRID-08` | Default (auto) / Restore after each gate | true | 0.56522 | 0.63248 | 0.82765 [0.8119, 0.84496] | 0.99581 [0.99564, 0.99583] |
| `APP-REPETITION-GRID-08` | Default (auto) / SABRE | true | 1 | 1 | 1.0277 [1.0013, 1.0398] | 0.99997 [0.99996, 1.0005] |
| `APP-REPETITION-GRID-08` | Persistent layout / Restore after each gate | true | 0.91304 | 0.97436 | 1.0185 [1.0002, 1.0682] | 0.99897 [0.99891, 0.99909] |
| `APP-REPETITION-GRID-08` | Persistent layout / SABRE | true | 1.6154 | 1.5405 | 1.2992 [1.2308, 1.3159] | 1.0033 [1.0032, 1.0038] |
| `APP-REPETITION-GRID-08` | Restore after each gate / SABRE | true | 1.7692 | 1.5811 | 1.2306 [1.2189, 1.2627] | 1.0043 [1.0042, 1.0048] |
| `APP-REPETITION-GRID-12` | Default (auto) / Persistent layout | true | 0.43333 | 0.4183 | 0.86439 [0.83607, 0.88029] | 0.99069 [0.99065, 0.99076] |
| `APP-REPETITION-GRID-12` | Default (auto) / Restore after each gate | true | 0.35135 | 0.33508 | 0.83916 [0.82067, 0.86046] | 0.98537 [0.98535, 0.98567] |
| `APP-REPETITION-GRID-12` | Default (auto) / SABRE | true | 1 | 1 | 1.0262 [1.0009, 1.0579] | 0.99915 [0.99837, 0.99988] |
| `APP-REPETITION-GRID-12` | Persistent layout / Restore after each gate | true | 0.81081 | 0.80105 | 0.98234 [0.9581, 1.0075] | 0.9947 [0.99459, 0.99474] |
| `APP-REPETITION-GRID-12` | Persistent layout / SABRE | true | 2.3077 | 2.3906 | 1.1975 [1.1835, 1.2082] | 1.0085 [1.0078, 1.0091] |
| `APP-REPETITION-GRID-12` | Restore after each gate / SABRE | true | 2.8462 | 2.9844 | 1.2067 [1.1925, 1.2504] | 1.0137 [1.0135, 1.0146] |
| `APP-REPETITION-LINE-06` | Default (auto) / Persistent layout | true | 0.57143 | 0.5339 | 0.78008 [0.77588, 0.79381] | 0.99668 [0.99634, 0.99671] |
| `APP-REPETITION-LINE-06` | Default (auto) / Restore after each gate | true | 0.48 | 0.44056 | 0.79427 [0.77251, 0.79972] | 0.99388 [0.99361, 0.99389] |
| `APP-REPETITION-LINE-06` | Default (auto) / SABRE | true | 1 | 1 | 1.0311 [1.0088, 1.0694] | 1.0009 [1.0005, 1.0012] |
| `APP-REPETITION-LINE-06` | Persistent layout / Restore after each gate | true | 0.84 | 0.82517 | 1.0163 [0.98414, 1.0293] | 0.99716 [0.99716, 0.99718] |
| `APP-REPETITION-LINE-06` | Persistent layout / SABRE | true | 1.75 | 1.873 | 1.311 [1.2976, 1.3516] | 1.0045 [1.0039, 1.0045] |
| `APP-REPETITION-LINE-06` | Restore after each gate / SABRE | true | 2.0833 | 2.2698 | 1.3199 [1.2684, 1.3586] | 1.0074 [1.0067, 1.0074] |
| `APP-REPETITION-LINE-08` | Default (auto) / Persistent layout | true | 0.36538 | 0.35111 | 0.61649 [0.61118, 0.62761] | 0.98036 [0.98028, 0.98064] |
| `APP-REPETITION-LINE-08` | Default (auto) / Restore after each gate | true | 0.37255 | 0.3098 | 0.64808 [0.63282, 0.66523] | 0.98122 [0.98119, 0.98151] |
| `APP-REPETITION-LINE-08` | Default (auto) / SABRE | true | 1 | 1 | 1.0206 [1.002, 1.0242] | 0.99999 [0.99996, 1.0003] |
| `APP-REPETITION-LINE-08` | Persistent layout / Restore after each gate | true | 1.0196 | 0.88235 | 1.0533 [1.0119, 1.0908] | 1.001 [1.0003, 1.0011] |
| `APP-REPETITION-LINE-08` | Persistent layout / SABRE | true | 2.7368 | 2.8481 | 1.6562 [1.5977, 1.6889] | 1.0201 [1.0201, 1.0202] |
| `APP-REPETITION-LINE-08` | Restore after each gate / SABRE | true | 2.6842 | 3.2278 | 1.5435 [1.5339, 1.6056] | 1.0191 [1.0191, 1.0193] |
| `APP-REPETITION-LINE-12` | Default (auto) / Persistent layout | true | 0.55814 | 0.49444 | 0.741 [0.72515, 0.7445] | 0.9875 [0.98726, 0.98839] |
| `APP-REPETITION-LINE-12` | Default (auto) / Restore after each gate | true | 0.27586 | 0.18089 | 0.51388 [0.50077, 0.52013] | 0.96253 [0.96251, 0.96255] |
| `APP-REPETITION-LINE-12` | Default (auto) / SABRE | true | 1 | 1 | 1.0162 [0.9841, 1.0313] | 1.0003 [1.0003, 1.0003] |
| `APP-REPETITION-LINE-12` | Persistent layout / Restore after each gate | true | 0.49425 | 0.36585 | 0.70063 [0.68977, 0.70591] | 0.9747 [0.97366, 0.97496] |
| `APP-REPETITION-LINE-12` | Persistent layout / SABRE | true | 1.7917 | 2.0225 | 1.3697 [1.3317, 1.3796] | 1.013 [1.0121, 1.0132] |
| `APP-REPETITION-LINE-12` | Restore after each gate / SABRE | true | 3.625 | 5.5281 | 1.9614 [1.9383, 2.0027] | 1.0392 [1.0392, 1.0393] |

## Reproduce acceptance and comparisons

Use the pinned harness and independent evaluator dependencies. Extract the retained archive into a fresh directory; participant SDKs are unnecessary for semantic replay. Source/build admission additionally needs the original full artifact described in the index.

```bash
tar -xJf docs/analysis/evidence/compiler-routing-policies-44623673659.tar.xz -C /path/to/fresh-evidence
PYTHONPATH=src python -m sdkbench.candidates.cli replay \
  --directory /path/to/fresh-evidence/campaign \
  --bundle /path/to/fresh-evidence/preparation/cohort
PYTHONPATH=src python tools/compare_compiler_applications.py \
  --profile routing-policies \
  --directory /path/to/fresh-evidence/campaign \
  --bundle /path/to/fresh-evidence/preparation/cohort \
  --output /path/to/new-comparisons.json
```

Expected: 1,200 replayed blocks, 120 case/policy outcomes and 180 pair rows. Output paths must be new. Complete raw evidence is authoritative over rounded Markdown. Resource-policy consistency and local build/freeze records do not independently attest the host or build. Publication eligibility remains false.
