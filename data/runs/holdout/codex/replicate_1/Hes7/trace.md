# Hes7 direct n_degs forecast

Target: `Hes7` in `151 TH Prkcd Grin2c Glut`

Endpoint: number of measured genes with Wilcoxon BH-adjusted `pvals_adj < 0.05`.

## Inputs used

- Declared holdout manifest: one target, `Hes7`.
- Declared biology bundle for `Hes7`.
- `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- `training_de_all_cell_groups.parquet`, filtered to `group_name == "151 TH Prkcd Grin2c Glut"` for hand-selected observed training perturbations.
- Same-experiment corpus Findings for selected training perturbations, used only as semantic summaries of the training measurements, not as independent replication.

## Target biology

The exact focal-population expression measurement in the `Hes7` bundle is extremely weak:

- `n_non_target_cells = 23679`
- `n_cells_expressing = 102`
- `pct_cells_expressing = 0.43076143418218676`
- `mean_raw_umi = 0.004476540394442333`
- `pseudobulk_cpm = 0.28056066088466963`

The curated biology supports effective depletion of HES7 protein only in cells that actually make HES7: wild-type mouse HES7 is a short-lived nuclear transcriptional repressor with a measured half-life of about 22 minutes in the embryonic segmentation-clock system, so an edit that blocks new HES7 synthesis should clear pre-edit protein long before the P37-P44 harvest. That realization prior does not establish a thalamic response, because the same bundle places the established operation and loss phenotype in embryonic presomitic mesoderm and marks postnatal neural relevance, phenotype latency, same-context redundancy, and best context match as unresolved.

## Training measurements

The declared focal count table contains 1,674 observed training perturbations. It is sparse overall:

- 1,205 / 1,674 have `n_degs = 0`
- median `n_degs = 0`
- 75th percentile `n_degs = 1`
- mean `n_degs = 14.0538`, inflated by broad machinery perturbations in the far tail

I used the biology bundle to choose the closest training perturbations along HES/Notch/segmentation and developmental bHLH axes. Exact `pvals_adj < 0.05` counts from the Parquet focal slice were:

| training perturbation | focal n_degs | interpretation |
| --- | ---: | --- |
| `Hesx1` | 0 | closest available HES-family developmental transcriptional repressor; corpus summary reports pan-neuronal FDR silence at P16 |
| `Dll1` | 0 | Notch ligand; corpus summary reports silence across all recovered juvenile-to-young-adult neuronal groups and no Notch-effector program |
| `Notch1` | 0 | core receptor |
| `Notch2` | 0 | core receptor |
| `Notch4` | 0 | core receptor |
| `Tbx6` | 0 | segmentation-associated developmental regulator |
| `Neurod1` | 0 | developmental bHLH comparator |
| `Neurod2` | 0 | developmental bHLH comparator |
| `Neurog3` | 0 | developmental bHLH comparator |
| `Mesp2` | 1 | segmentation-associated developmental regulator; only `Arih2` reached FDR in the focal slice |
| `Fbxw7` | 1 | Notch-pathway/substrate regulator; only `Trp53inp2` reached FDR in the focal slice, and the corpus records available Notch perturbations as nearly silent |
| `Clock` | 3 | bHLH-PAS circadian regulator with three focal circadian-output genes, `Tef`, `Nr1d2`, and `Dbp` |

The profile comparison over these 12 observed nodes found 9 with zero significant focal features and the remaining 3 with only 1-3 significant features. The cohort diagnostic showed little recurrent positive program among them: for `Hesx1`, all leading positive log-fold-change rows had `pvals_adj = 1.0`, and the apparent pairwise profile similarity among quiet nodes was dominated by shared weak negative tails rather than by repeated significant genes.

## Synthesis

`Hes7` has a realizable lesion in an actively expressing cell, but only about 0.43% of focal non-target nuclei had any detected `Hes7` RNA and the established biology is embryonic presomitic mesoderm rather than postnatal thalamic glutamatergic neurons. The training perturbations closest to that biology were overwhelmingly null in the same focal analysis, and the few nonzero comparators were isolated one-gene events or a circadian program without support from the `Hes7` bundle.

Given that combination of exact near-absence in the assayed population, unresolved postnatal thalamic coupling, and null/near-null focal behavior of the HES/Notch/segmentation training analogs, my point forecast is:

`predicted_n_degs = 0`
