# Prdm12 direct n_degs forecast

## Target and endpoint

- Manifest target: `Prdm12`.
- Cell group: `151 TH Prkcd Grin2c Glut`.
- Endpoint: the integer count of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05` in that cell group.
- Declared training count table: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Declared profile table: `[local file: training_de_all_cell_groups.parquet]`.
- Target biology bundle: `[local file: Prdm12.json]`.

## Evidence used

The target bundle gives the decisive context for the target itself. PRDM12 is a nuclear transcriptional regulator, and the functional-stock card judges active PRDM12 as likely substantially depleted by the P37-P44 harvest after a P16 edit. Thus the perturbation could be realized if assayed cells require PRDM12. The exact same-assay reach, however, is extremely restricted in the focal population: only 30 of 23,679 non-target `151 TH Prkcd Grin2c Glut` nuclei express `Prdm12`, with `pct_cells_expressing = 0.12669453946534903`, `mean_raw_umi = 0.0014358714472739557`, `mean_cp10k = 0.0008068331897905696`, and 34 total target UMIs. The card also records only restricted postnatal thalamic-area expression and no directly matched P16 thalamic loss study.

The focal training count table is dominated by null and near-null outcomes:

| subset | count |
|---|---:|
| training perturbations | 1674 |
| `n_degs = 0` | 1205 |
| `n_degs <= 1` | 1481 |
| `n_degs <= 5` | 1546 |
| median `n_degs` | 0 |
| 90th percentile | 2 |
| mean `n_degs` | 14.0538 |
| max `n_degs` | 2677 |

This background matters because a target whose relevant expression is present in roughly one-tenth of one percent of the aggregate thalamic class needs a very large and coherent effect in those rare cells to produce a BH-supported whole-class Wilcoxon count.

I used the PRDM-family training perturbations as the closest measured operation class:

| perturbation | 151 `n_degs` |
|---|---:|
| `Prdm10` | 52 |
| `Prdm16` | 0 |
| `Prdm2` | 0 |
| `Prdm5` | 0 |

The July same-experiment corpus reports that `Prdm10`, but not `Prdm5` or `Prdm16`, produced a multi-cell-type neuronal PRDM-family signature, and that represented PRDM-family perturbations did not phenocopy `Prdm10`: `Prdm16` and `Prdm5` were flat, while `Prdm2` had only one non-overlapping Pvalb gene at FDR < 0.10 across the full screen.

I compared the four observed PRDM profiles in the 151-only Parquet context. At FDR < 0.05 in `151 TH Prkcd Grin2c Glut`, the profile artifact reported:

| perturbation | significant features |
|---|---:|
| `Prdm10` | 52 |
| `Prdm16` | 0 |
| `Prdm2` | 0 |
| `Prdm5` | 0 |

The `Prdm10` program had weak whole-profile similarity to the quiet PRDM perturbations rather than a coherent family module: Pearson correlations were -0.0135 to `Prdm16`, 0.0338 to `Prdm2`, and 0.0528 to `Prdm5`, with no positive or negative significant-gene overlap in any of those pairs. In its eligible-neighbor scan, `Prdm10`'s nearest whole-profile neighbors were not PRDM genes but broader high-response perturbations such as `Cic`, `Rab7`, and `Uba5`. I therefore treated `Prdm10 = 52` as a high-side boundary showing that the assay can see one PRDM loss when it engages a 151 program, not as the quantitative center for `Prdm12`.

## Synthesis

`Prdm12` has some upward biology: it is a dynamic transcriptional regulator, adult postmitotic loss has transcriptional consequences in other neural contexts, and no close mouse paralog is known. Those factors argue against forcing a universal assay-failure null.

The downward evidence is stronger for this exact endpoint. The outcome is a whole-aggregate 151-class DEG count, and `Prdm12` is essentially absent from that focal population by exact non-target RNA reach. The same-family training data are 3/4 zero in this cell class and show that the one responsive PRDM member is a distinct program rather than a shared family state. Most developmental or transcription-factor-like entries in the 151 training count table were also null, consistent with a P16 postmitotic assay often missing genes whose main roles are developmental or active in a smaller context.

I therefore forecast a null aggregate signature at the requested BH threshold:

```text
predicted_n_degs = 0
```

I used only the declared biology bundle, the declared training count table, the declared training Parquet through profile tools, and corpus records for training perturbations. I did not inspect or reconstruct a `Prdm12` endpoint profile or count.
