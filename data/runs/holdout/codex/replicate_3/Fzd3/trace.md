# Direct Fzd3 DEG-count forecast

Target and endpoint:

- `gene_target`: `Fzd3`
- `group_name`: `151 TH Prkcd Grin2c Glut`
- Predicted endpoint: number of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`

## Evidence used

### Declared target and biology bundle

- `task_bindings_receipt.json` resolves the one-row holdout manifest and the biology bundle to the same target, `Fzd3`.
- The held-out target is absent from the declared held-in measurements: the training Parquet contains 0 `Fzd3` rows overall and 0 `Fzd3` rows in `151 TH Prkcd Grin2c Glut`.
- The Fzd3 biology bundle reports exact non-target expression in the focal class:
  - 15,381 of 23,679 non-target nuclei express `Fzd3` in `151 TH Prkcd Grin2c Glut`.
  - `pct_cells_expressing = 64.956%`
  - `mean_raw_umi = 1.239`
  - `mean_cp10k = 0.778`
- The same bundle adjudicates the edited product as a renewable membrane Wnt/planar-polarity receptor whose functional stock is likely substantially depleted by P37-P44 after the P16 edit.
- The bundle also makes the main biological caveat explicit: direct Fzd3 loss evidence is embryonic tract-construction evidence, including thalamocortical/corticothalamic development, not a matched postnatal thalamic-neuron maintenance experiment.

### Same-experiment corpus

- `target_context(Fzd3)` in the selected same-experiment corpus release returned no Fzd3 Findings, no Fzd3 Claims, and no explicit Fzd3 references, so it did not expose the held-out target response.
- The held-in Frizzled/Wnt receptor layer is repeatedly annotated as weak in this snRNA-seq experiment:
  - `Fzd6:F001`: acute Fzd6 loss was transcriptomically silent in every recovered neuronal group.
  - `Fzd6:F002`: the Fzd6 null is not explained by a complete inability to detect Wnt output, because Ctnnb1, Tcf7l2, and Lrp6 produced detectable thalamic Wnt/beta-catenin/TCF responses.
  - `Fzd6:F003`: represented Frizzled and PCP receptors did not form a hidden single-gene receptor-level module.
  - Inventory records for `Fzd2`, `Fzd4`, and `Fzd9` likewise summarize every represented single-Frizzled perturbation as flat or buffered.

The corpus summaries and the Parquet are different representations of the same experiment, not independent replication.

### Held-in count table and Parquet checks

From `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`:

- Held-in targets: 1,674
- Targets with `n_degs = 0`: 1,205
- Median `n_degs`: 0
- 75th percentile: 1
- 90th percentile: 2
- 95th percentile: 18
- Mean: 14.05, dominated by the long upper tail

Exact held-in Wnt/PCP and receptor-adjacent counts in `151 TH Prkcd Grin2c Glut` at the requested FDR < 0.05 endpoint:

| target | n_degs |
| --- | ---: |
| Fzd2 | 0 |
| Fzd4 | 0 |
| Fzd6 | 0 |
| Fzd9 | 0 |
| Celsr2 | 1 |
| Prickle1 | 0 |
| Ror1 | 0 |
| Ror2 | 0 |
| Ryk | 0 |
| Lrp5 | 0 |
| Lrp6 | 4 |
| Gsk3b | 6 |
| Tcf7l2 | 106 |
| Ctnnb1 | 383 |

Parquet aggregation over the same group reproduced these counts for the queried targets and showed the same separation between receptor-layer perturbations and intracellular Wnt/core transcriptional nodes. For example, the queried single-Frizzled targets all had 0 genes with `pvals_adj < 0.05`; by contrast `Ctnnb1` had 383 and `Tcf7l2` had 106.

## Forecast rationale

Fzd3 is genuinely present in the focal thalamic population, and the P16-to-P37/P44 window should be long enough to deplete much of a renewable FZD3 receptor pool. I therefore did not treat the target as biologically unreachable.

The decisive quantitative evidence was instead the receptor-layer precedent in the exact endpoint table. Four held-in Frizzled perturbations, plus Ror/Ryk and Prickle1, were silent at FDR < 0.05 in the same thalamic class; `Celsr2` was only a singleton. The same Parquet slice clearly recovers downstream/core Wnt biology through `Ctnnb1`, `Tcf7l2`, and weakly `Lrp6`, so the flat Frizzled results are more consistent with single-receptor buffering or postnatal PCP transcriptional silence than with a powerless thalamic assay.

Fzd3 is not an identical replicate of Fzd6: its best mouse phenotype is forebrain axon guidance and it is focally expressed, so a very small count is possible. But that phenotype is embryonic, installed-tract biology rather than a known ongoing P16 thalamic RNA-maintenance program, and the nearest observed receptor/PCP perturbations point to zero-to-singleton burdens.

Point prediction: `0`.
