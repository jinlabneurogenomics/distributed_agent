# Foxp1 DEG-count forecast

## Target-side evidence

- Declared target: `Foxp1` from the one-row holdout manifest.
- Focal population: `151 TH Prkcd Grin2c Glut`, the exact thalamic glutamatergic class requested by the task.
- Biology-only bundle used: `biology_bundles/Foxp1.json`.

The target card supports perturbation realization but only a moderate
population-level reach. `Foxp1` is a soluble nuclear FOXP DNA-binding
transcription factor, so new intact FOXP1 supply should stop in edited cells
and the pre-edit functional stock is likely substantially depleted by the
P37-P44 harvest. The bundle also notes that this inference is partial: no
FOXP1 neuronal half-life was available, the strongest postnatal neural evidence
is striatal rather than thalamic, and thalamic compensation by `Foxp2` or
`Foxp4` is untested.

The exact in-assay non-target expression measurement in the requested class was:

| measurement | value |
|---|---:|
| `pct_cells_expressing` | 50.1204 |
| `n_cells_expressing` / `n_non_target_cells` | 11868 / 23679 |
| `mean_raw_umi` | 1.1523 |
| `mean_log1p_cp10k` | 0.4094 |
| `pseudobulk_cpm` | 72.2205 |

I therefore treated `Foxp1` as a real, likely engaged transcription-factor
loss in only a subset of the aggregated thalamic population, not as a pan-class
driver expected to create a large DEG burden.

## Training measurements

The endpoint is the declared training count table
`151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`, checked against
`training_de_all_cell_groups.parquet` by recounting rows with
`pvals_adj < 0.05` in the focal class.

Screen-wide within the training count table:

| statistic | `n_degs` |
|---|---:|
| targets | 1674 |
| zeros | 1205 |
| median | 0 |
| 75th percentile | 1 |
| 95th percentile | 18 |
| max | 2677 |

Because the `Foxp1` card pointed to a postmitotic neuronal transcription
factor rather than to RNA processing, proteasome, or broad chromatin toxicity,
I weighted the low-burden fate-regulator measurements most heavily:

| training perturbation | `n_degs` |
|---|---:|
| `Foxp2` | 0 |
| `Sox5` | 2 |
| `Satb2` | 0 |
| `Bcl11a` | 0 |
| `Bcl11b` | 0 |
| `Tbr1` | 0 |
| `Zbtb20` | 0 |
| `Zbtb18` | 5 |
| `Mef2c` | 1 |
| `Pax6` | 0 |

These ten direct fate/transcriptional comparators have 7 zeros, a median of 0,
a mean of 0.8, and a maximum of 5 DEGs in `151 TH Prkcd Grin2c Glut`. The
Parquet slice had 17,259 measured rows for every listed target and matched
perturbed-nucleus counts from 138 to 288, so their near-zero counts are observed
quiet signatures rather than missing focal measurements. A profile comparison
over these ten perturbations gave 45/45 available pairwise comparisons but no
shared significant program; seven nodes had no significant genes and three had
only 1-9 significant genes.

I used a broader NDD/chromatin group only as an upper-context check:
`Adnp = 25`, `Chd8 = 61`, `Setd5 = 9`, `Kmt2a = 24`, `Kdm5c = 18`,
and `Mecp2 = 16`. Those genes are broader chromatin or methyl-CpG regulators
with higher focal DEG burdens than the direct fate-factor cohort, so they
argued against forcing the `Foxp1` forecast exactly to zero but were too
pleiotropic to set the point estimate.

## Synthesis

The direct thalamic fate-factor cohort centers below one DEG, and the closest
training FOXP-family member, `Foxp2`, has zero. `Foxp1` itself is nevertheless
measurably present in about half of the focal nuclei and its soluble nuclear
stock is expected to turn over within the experimental window. I therefore
placed the forecast just above the direct-cohort median but still within its
quiet range, rounding the direct-cohort mean of 0.8 to a point prediction of:

`predicted_n_degs = 1`
