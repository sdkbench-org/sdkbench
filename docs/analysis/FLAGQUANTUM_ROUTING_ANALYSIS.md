# FlagQuantum routing cost attribution

The large P1b CZ counts are reproducible for the registered FlagQuantum 0.3.1 pipeline. Most of the observed excess is explained by routing and layout policy, with a smaller demonstrated gap in native local optimization. This does not establish poor performance across FlagQuantum, a simulator defect, or a global SDK ranking. Existing native FlagQuantum APIs substantially reduce these counts without changing input circuits or acceptance rules.

The original comparison is valid as a comparison of declared pipelines. It is insufficient as a comparison of best available SDK capability, and describing all three pipelines as comparable out-of-the-box defaults is too strong. Qiskit explicitly uses level 2, and Cirq explicitly combines routing and target synthesis. FlagQuantum's expert compiler default performs layout restoration that this task does not require.

## Scope and reproducibility

The [protocol](ROUTING_PROTOCOL.md) and [profile](routing-profile.json) were committed before controlled execution at `6d3462cf99398f52a653f94a747e3dba05fc478c`. The [Linux run](https://github.com/sdkbench-org/sdkbench/actions/runs/44273899460) produced 210 frozen-instance outcomes and 54 microprobe outcomes. All 264 passed independent semantic acceptance. The lossless [archive](evidence/routing-6d3462c.json.gz), [index](evidence/index.json), [machine-readable summary](routing-summary.json), and [all configuration tables](ROUTING_TABLES.md) retain every arm, including configurations with worse counts.

The archive SHA-256 is `1c388fc12fd9b9ffc4230c356fd691edd98af72ad55672a11906334365528d67`. Independent replay verified 798 files and all 264 outcomes. Thirty Qiskit seed/case pairs and three cases each for FlagQuantum and Cirq reproduce the original P1b baseline gate counts and common dependency depths: 36 of 36 comparisons match.

The measured cohort is FlagQuantum 0.3.1, Qiskit 2.6.2 and cirq-core 1.7.0. Every outcome uses one CPU, one numerical thread, 16 GiB, the P0 Linux isolation controls, a 120-second compilation alarm and the frozen cumulative case wall limit. Profiling and callbacks perturb timing. There are zero warmups and one compilation per diagnostic outcome; these are gate-count mechanism diagnostics, not complete-case timing scores. `publication_eligible` remains false.

All configurations preserve identity initial placement, no ancillas, original topology, arbitrary one-qubit gates plus full CZ, and an allowed final permutation. Six-qubit checks reconstruct the complete operator. Eight- and twelve-qubit checks retain the original three probes; passing them is not a complete operator proof. No evaluator, original adapter, fixture or historical archive is changed.

## What the default router does

The observed default restores the layout after each remote gate. Let `d` be the original graph distance between a CX's operands. Moving together and restoring costs `2 * (d - 1)` SWAPs. The traces retain every resulting SWAP, and native per-instruction lowering costs one CZ per CX and three CZs per SWAP:

| Input | Original CX | Sum of `d - 1` | Forward / restoring SWAPs | Predicted and observed CZ |
| --- | ---: | ---: | ---: | ---: |
| ROUTE-LINE-06 | 24 | 34 | 34 / 34 | `24 + 3 * 68 = 228` |
| ROUTE-GRID-08 | 32 | 31 | 31 / 31 | `32 + 3 * 62 = 218` |
| ROUTE-LINE-12 | 48 | 174 | 174 / 174 | `48 + 3 * 348 = 1092` |

Pre-routing and post-routing level-2 optimization leave these input CX and routed SWAP counts unchanged. Levels 0 and 1 give the same CZ counts on these inputs. Restricting the one-qubit basis to RX/RZ also leaves these counts unchanged. The adapter is not inventing or double-counting entangling gates: the common evaluator counts native output CZs, and the intermediate arithmetic explains the totals exactly.

## Existing native controls close much of the gap

The following is one specified path through the factorial, not a unique additive causal decomposition. Routing, layout and optimization interact.

| Pipeline | LINE-06 CZ | GRID-08 CZ | LINE-12 CZ |
| --- | ---: | ---: | ---: |
| Registered FlagQuantum default | 228 | 218 | 1092 |
| Native SABRE, restore final layout | 138 | 146 | 438 |
| Native SABRE, remove final restoration | 108 | 98 | 381 |
| Above plus native post-basis optimization/legalization | 108 | 96 | 375 |
| Qiskit registered baseline, ten fixed seeds | 68 | 85 | 339–348 |
| Cirq registered baseline | 68 | 84 | 360 |

The final FlagQuantum configuration reduces CZ counts by 52.63%, 55.96% and 65.66%. Its common two-body dependency depths are 94, 55 and 173. On LINE-12, Qiskit has fewer CZs but depth 192–219; Cirq has fewer CZs but depth 198. Thus even this small cohort contains a count/depth tradeoff. These diagnostics do not justify saying that every aspect of FlagQuantum's compiled circuit is worse.

For SABRE, final restoration accounts for 10, 16 and 19 SWAPs, or 30, 48 and 57 CZs. Removing it respects this task's output-layout contract through the native public `remove_layout_restore` API. Removing a final restoration from the default per-gate restore strategy is a no-op. Merely selecting persistent layout is insufficient: restoring configurations give 294, 212 and 1194 CZs; free-layout configurations give 165, 125 and 621. The released `auto` chooses the original restoring result in these cases.

## A distinct implementation opportunity

The [microprobes](ROUTING_TABLES.md) separate native synthesis from global routing. On the reversed local pair `SWAP(0,1); CX(1,0)`, FlagQuantum emits four CZs even after another native optimization/legalization cycle. The independently equivalent input `CX(1,0); CX(0,1)` emits two, with identity final layout in both cases. Saved [released](source-probes/local-pair-release.json) and [upstream](source-probes/local-pair-upstream.json) artifacts independently reconstruct both complete 4-by-4 operators. This is an optimization opportunity, not a correctness failure.

The [minimal reproducer](../../examples/flagquantum_routing_pair.py) and [issue #1215](https://github.com/flagos-ai/FlagQuantum/issues/1215) document it. Source inspection indicates that target-independent ordered-pair folding does not perform general target-aware two-qubit resynthesis; operand-order changes also split its block collection. This mechanism is consistent with the reproducer but does not quantify every residual CZ difference on large inputs. Changing wire order without transforming the local basis would be incorrect.

Cirq gives two CZs on this probe. Qiskit gives one while using final permutation `[1, 0, 2, 3, 4, 5]`, absorbing the logical SWAP. Comparing one versus four as a pure local synthesis difference would therefore be misleading. The full artifact and layout must accompany the count.

## Release and upstream scope

[Inspection records](source-probes/inspection.json) pin release file hashes and upstream commit `305b58f5f1d862cdad0770ffdd35dfaf1713ee67`, whose source version is 0.4.0. The live PyPI observation on November 18, 2026 reported release 0.3.1 and no 0.4.0 release. The inspected upstream `auto` already considers SABRE; the released selector does not. Do not report the released selector limitation as absent upstream work.

The local upstream pair and six-qubit operator probes are separate source checks, with explicit module-path adaptation and no source patch. They are not resource-qualified outcomes from the installed-wheel cohort and supply no timing comparison. The local four-versus-two opportunity remains in both inspected versions.

## Fairness assessment and action

The original registered experiment matched task semantics and enforced resources. Its adapter chose the public expert compiler, then native basis legalization. That choice exposes the SDK's default routing policy and omits available free-final-layout and extra post-basis optimization controls. Consequently the default penalty is partly a product/API orchestration issue and partly a configuration choice in the benchmark; it cannot be assigned entirely to a missing algorithm. The remaining local opportunity belongs to SDK implementation and pipeline composition.

Numeric optimization levels do not equate effort across SDKs. Nineteen FlagQuantum configurations, five seeded Qiskit configurations and one Cirq configuration are intentionally asymmetric diagnostic searches, not a fair tournament of best-tuned compilers. There is no speed or global capability ranking here. A future study should separately register ordinary documented workflows and explicitly tuned workflows, declare equal total search budgets, record layout obligations and optimization objectives, and retain failures and seed distributions. The old evidence must remain immutable.

The recommended product work is [native integration into FlagQuantum's own IR and compilation pipeline](COMPILER_INTEGRATION_PLAN.md): compose existing routing/layout capabilities first, then improve target-aware local synthesis, and test all changes independently. SDKBench must continue to evaluate every participant under common contracts and must not implement a hidden FlagQuantum optimizer in its adapter.

## Independent replay

The archive is gzip-compressed JSON mapping relative file paths to UTF-8 content and hashes, using the same lossless format as earlier P1b archives. Extract only paths contained within a new directory and verify each content hash before writing. Then run without importing any participant SDK:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python tools/routing_evidence.py \
  --directory /path/to/extracted-evidence --bundle docs/implementation \
  --summary /path/to/new-replay-summary.json
python -m pytest -q tests/test_routing_evidence.py tests/test_routing_source_probes.py
```

The tests perform safe extraction and full independent replay, and reject changed hashes, modified registration bindings and a changed frozen initial-layout contract even after resealing file hashes.
