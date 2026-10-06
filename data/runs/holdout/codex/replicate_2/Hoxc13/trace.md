# Hoxc13 direct DEG-count forecast

Target endpoint: `Hoxc13` in `151 TH Prkcd Grin2c Glut`; predict the number of measured genes with BH-adjusted Wilcoxon `p < 0.05`.

## Evidence used

### Exact focal-population reach from the declared Hoxc13 bundle

The target bundle reports exact non-target expression for `Hoxc13` in the focal population:

- `2 / 23679` non-target nuclei expressed the gene.
- `pct_cells_expressing = 0.00844630263102327`.
- `total_target_umi = 2`.
- `pseudobulk_cpm = 0.0052935973751824465`.
- `mean_log1p_cp10k = 4.644409072844238e-05`.

This expression reach supersedes the qualitative tissue priors. It makes Hoxc13 a nearly absent transcript in the assayed thalamic neuronal class; even if Cas9 disrupts edited alleles efficiently, the perturbation has almost no target-expressing focal nuclei in which to remove an active Hoxc13 program.

The same bundle characterizes Hoxc13 as a nuclear DNA-binding transcription factor whose established mouse loss phenotypes and expression are hair/nail/tongue/caudal-structure phenotypes rather than a postnatal thalamic-neuron program. The functional stock card says existing Hoxc13 protein would likely decline over the 21-28 day P16-to-P37/P44 experimental window if present, so persistent protein is not the main reason to expect a null; lack of a focal Hoxc13-expressing program is.

### Training measurements in the exact endpoint

The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` table has 1,674 training perturbations. Its zero-count mass is large:

- `1205 / 1674` training targets have `n_degs = 0`.
- `276 / 1674` have `n_degs = 1`.
- The mean count is `14.05`, but the distribution is very skewed: only 106 targets have at least 10 DEGs and only 43 have at least 100.

All training-available Hox perturbations in this focal class are zero in the declared count table:

| target | n_degs |
|---|---:|
| Hoxa1 | 0 |
| Hoxa13 | 0 |
| Hoxa3 | 0 |
| Hoxb8 | 0 |
| Hoxd10 | 0 |
| Hoxd13 | 0 |

`Hoxa13` and `Hoxd13` are the closest group-13 Hox comparators available in training; `Hoxb13` is not in the table, and `Hoxc13` is correctly absent from the training count table.

I also checked those six Hox perturbations directly in the declared expression Parquet, filtered to `group_name = "151 TH Prkcd Grin2c Glut"`. The symmetric profile comparison reported all six as `no_significant_features`, confirming that the zero counts are backed by exact FDR rows in the same endpoint rather than a parsing artifact of the count table.

## Synthesis

The forecast is dominated by exact focal expression: a Hoxc13 knockout in postmitotic thalamic neurons should not create a broad recovered-nucleus transcriptional state when Hoxc13 is detected in only two matched control nuclei. The direct quantitative analogs point the same way: every observed Hox perturbation available for this class, including both available group-13 relatives, has zero significant measured genes.

Residual uncertainty is one-sided but small. Sparse nuclear RNA can miss rare expression, and the bundle lacks a target-specific Hoxc13 protein half-life, but the bundle's own protein-stock adjudication would make a functional lesion plausible only conditional on expression. With near-zero exact focal reach and zero-count Hox family measurements, the integer point forecast is:

`predicted_n_degs = 0`

The Hoxc13 held-out differential-expression signature and held-out DEG count were not used.
