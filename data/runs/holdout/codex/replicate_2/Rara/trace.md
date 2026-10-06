# Rara direct n_degs forecast

## Declared target

- Target: `Rara`
- Cell context: `151 TH Prkcd Grin2c Glut`
- Endpoint: count of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`
- Prediction: `0`

## Evidence used

I used the declared `Rara` biology bundle, the declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` count table, the declared `training_de_all_cell_groups.parquet` in the exact `151 TH Prkcd Grin2c Glut` context, and same-experiment July-corpus Findings for measured training analogs. The Parquet, count table, and Findings were treated as different representations of this experiment rather than independent replication.

The `Rara` card supports within-window functional loss but not broad focal-population reach:

- RARalpha is a retinoic-acid receptor that heterodimerizes with RXR and regulates RARE-linked transcription.
- Neuronal RARalpha also binds dendritic mRNAs and suppresses local translation in hippocampal/rodent neuronal systems.
- Acute Rara deletion blocks a RARalpha-dependent homeostatic-plasticity response in cultured mouse hippocampal neurons, and postnatal cortical RARalpha loss disrupts juvenile circuit remodeling.
- Endogenous RARalpha protein turned over on an approximately 23-hour scale in mouse P19 cells and is subject to proteasomal removal, so the P16-to-P37/P44 interval should be long enough to substantially deplete newly edited cells.
- Exact in-assay reach is low: in `151 TH Prkcd Grin2c Glut`, `Rara` was detected in 2,949 / 23,679 non-target nuclei, `12.454%`, with mean `log1p(CP10K) = 0.06467`.

The focal training count table is highly zero-inflated: among 1,674 training targets, 1,205 have `n_degs = 0`, the median is `0`, the 75th percentile is `1`, the 90th percentile is `2`, and the 95th percentile is `18`.

I used the retinoic-acid receptor family and RXR heterodimer partners as the closest measured analogs. All were flat in the exact focal-class training table:

| target | focal `n_degs` |
|---|---:|
| `Rarb` | 0 |
| `Rarg` | 0 |
| `Rxra` | 0 |
| `Rxrb` | 0 |
| `Rxrg` | 0 |

The matched profile comparison over the declared Parquet reproduced the same result: each of `Rarb`, `Rarg`, `Rxra`, `Rxrb`, and `Rxrg` had `0` positive and `0` negative significant features at FDR 0.05 in `151 TH Prkcd Grin2c Glut`. Same-experiment Findings for these measured relatives also describe no broad acute postnatal RAR/RXR transcriptomic module: `Rarg`, `Rxra`, and `Rxrg` were globally buffered or null across measured neuronal groups; `Rarb` and `Rxrb` produced only isolated one-gene responses outside the focal thalamic group; and RXR/RAR relatives did not phenocopy one another.

I kept four broader nuclear receptors as scale checks rather than direct donors:

| target | relation to forecast | focal `n_degs` |
|---|---|---:|
| `Rorb` | ROR-family boundary; focal class flat | 0 |
| `Thra` | RXR heterodimer partner from a thyroid-receptor axis | 3 |
| `Nr1d1` | distant clock-loop receptor with a strong, distinct thalamic program | 116 |
| `Rora` | distant ROR receptor with a strong, distinct thalamic program | 278 |

These show that a nuclear receptor can be detected in this high-yield cell class, but the large `Rora` and `Nr1d1` programs are circadian/RORE biology rather than retinoic-acid/RXR biology. They therefore raise the upper uncertainty for ligandable nuclear receptors in general but do not outweigh the direct RAR/RXR-family nulls.

## Synthesis

The upward case is real: a successful `Rara` edit should deplete a dynamic receptor protein over 21-28 days, and RARalpha loss has postnatal neuronal phenotypes outside thalamus. The downward case is more task-matched: the focal expression reach is only about one eighth of the assayed aggregate, related RAR/RXR single-gene perturbations are silent in the same focal count table and Parquet slice, and the training endpoint’s local prior is already concentrated at zero or one DEG.

I therefore placed `Rara` at the focal null rather than at the `Rora`/`Nr1d1` response scale. Because the closest measured retinoid-family and RXR anchors were all exactly `0` and the low expression fraction makes small target-positive shifts hard to clear BH FDR 0.05 after aggregation, the integer point forecast is:

```tsv
target_name	predicted_n_degs
Rara	0
```
