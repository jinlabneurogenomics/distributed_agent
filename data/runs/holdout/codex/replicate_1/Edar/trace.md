# Direct n_degs forecast for Edar in 151 TH Prkcd Grin2c Glut

## Target and endpoint

- Target from the one-row holdout manifest: `Edar`.
- Endpoint: count of measured genes in `151 TH Prkcd Grin2c Glut` with Wilcoxon `pvals_adj < 0.05`.
- The requested target profile and its DEG count were withheld; the number below is inferred from the biology-only Edar bundle plus the declared training count table, the declared training Parquet, and same-experiment Findings for visible training perturbations.

## Evidence used

### Edar focal-population reach

The Edar biology bundle reports exact non-target expression in the focal population:

- `n_non_target_cells = 23679`
- `n_cells_expressing = 19`
- `pct_cells_expressing = 0.08023987499472106`
- `total_target_umi = 22`
- `mean_raw_umi = 0.0009290932894125596`
- `pseudobulk_cpm = 0.058229571127006906`

Thus Edar RNA is essentially at the detection floor in these recovered thalamic neurons. The same bundle adjudicates EDAR as a renewable cell-surface TNFR-family receptor whose EDA-A1 engagement can activate NF-kappaB. A P16 disruptive edit should stop new receptor supply and the 21-28 day interval plausibly allows depletion of an existing receptor pool, but the source card found only developmental ectodermal loss phenotypes and no direct postnatal thalamic requirement.

### Training n_degs distribution

The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` has 1,674 visible perturbations. It is strongly zero-inflated:

- 1,205 / 1,674 targets have `n_degs = 0`.
- Median `n_degs = 0`.
- 75th percentile = 1.
- 90th percentile = 2.
- Mean = 14.05 only because of a small heavy tail; the maximum visible value is 2,677.

So the non-specific prior for a held-out target in this cell class is already a null or near-null response, with only 85 / 1,674 visible targets reaching at least 18 DEGs and 59 / 1,674 reaching at least 50.

### Local EDA/NF-kappaB/TNF training controls

Training perturbations closest to an EDAR receptor signal were all null in this same focal class:

| target | `n_degs` at BH < 0.05 |
| --- | ---: |
| `Eda` | 0 |
| `Chuk` | 0 |
| `Nfkb1` | 0 |
| `Rel` | 0 |
| `Traf3` | 0 |
| `Tnfrsf1a` | 0 |
| `Fas` | 0 |
| `Map3k7` | 0 |
| `Mapk1` | 0 |
| `Mapk9` | 0 |
| `Bcl2` | 0 |

Direct Parquet aggregation in `151 TH Prkcd Grin2c Glut` reproduced zero BH<0.05 and zero BH<0.10 genes for each of these controls. They were present with matched perturbed-cell recovery rather than missing: 90-249 matched perturbed nuclei, against 23,679 matched controls in this class.

The same-experiment Finding layer, interpreted as the packaged semantic view of the same measurements rather than an independent replicate, was consistent with those counts:

- `Eda:F001` called Eda a pan-neuronal corrected-DE null with zero downstream genes at FDR<0.10 in all 23 measured neuronal groups.
- `Eda:F003` reported that the embryonic EDA/EDAR/NF-kappaB placode program was not recovered and that visible downstream genes such as `Dkk4`, `Lrp4`, `Shh`, `Ccnd1`, and `Edar` had minimum FDR 1.0 in the Eda perturbation.
- `Chuk:F001` called acute Chuk loss null across the measured neuronal surface.
- `Chuk:F003` noted a shared null among the represented NF-kappaB relatives `Nfkb1`, `Rel`, `Traf3`, and `Tnfrsf1a`, with the caveat that `Ikbkb`, `Ikbkg`, `Map3k14`, `Nfkb2`, `Rela`, and `Relb` were not available as perturbation targets.

As a detectability counterpoint, this focal class does yield substantial responses for some developmental signaling perturbations: `Ctnnb1` has 383 BH<0.05 genes and `Tcf7l2` has 106. The Edar prediction is therefore not based on assuming that 151 TH Prkcd Grin2c Glut cannot respond, but on the combination of near-absent Edar expression and the local EDA/TNF/NF-kappaB nulls.

## Synthesis

Edar is an upstream receptor in a pathway whose visible ligand, kinase, transcription-factor, TRAF, and TNFR/death-receptor perturbations are all transcriptionally silent in this cell class and usually silent pan-neuronally. Loss of a barely expressed receptor should not create a broader cell-autonomous transcriptional response than loss of `Eda`, `Chuk`, `Nfkb1`, `Rel`, `Traf3`, or `Tnfrsf1a`. Functional EDAR stock could decline in the rare edited cells that truly express it, but those cells account for only 19 of 23,679 non-target nuclei in the matched class, which makes a BH-detectable population-level signature unlikely.

The point forecast is therefore the null count:

`predicted_n_degs = 0`
