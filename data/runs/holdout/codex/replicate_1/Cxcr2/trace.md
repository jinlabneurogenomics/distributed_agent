# Direct `n_degs` forecast for `Cxcr2`

## Target and endpoint

- Target from the declared one-row holdout manifest: `Cxcr2`.
- Endpoint: number of measured genes in `151 TH Prkcd Grin2c Glut` with BH-adjusted Wilcoxon `p < 0.05`.
- Prediction: `0`.

## Evidence used

### Biology-only Cxcr2 bundle

The declared Cxcr2 bundle contained no target endpoint. Its exact focal-population reach measured Cxcr2 in non-targeting `151 TH Prkcd Grin2c Glut` nuclei and found:

- `n_non_target_cells = 23679`
- `n_cells_expressing = 0`
- `pct_cells_expressing = 0.0`
- `mean_raw_umi = 0.0`
- `pseudobulk_cpm = 0.0`
- `total_target_umi = 0.0`

The card-level prior says a disruptive edit should eventually deplete functional CXCR2 protein if the receptor is being made, because CXCR2 is a seven-transmembrane chemokine GPCR that cycles through membrane, recycling, and lysosomal compartments. The same bundle also makes the main context mismatch explicit: established mouse expression and phenotypes are in granulocytes and oligodendrocyte-lineage / white-matter settings, not healthy postnatal thalamic NeuN-positive neurons. I treated the exact in-assay zero expression as the dominant source-context evidence for this scalar endpoint.

### Declared training count table

The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` table has 1,674 visible training perturbations:

- 1,205 / 1,674 have `n_degs = 0`.
- Median `n_degs = 0`.
- 75th percentile `n_degs = 1`.
- 90th percentile `n_degs = 2`.

Thus the local base rate strongly favors zero or near-zero responses for perturbations without an essential, broadly expressed neuronal role in this aggregate thalamic class.

Immune/chemokine/inflammatory receptor and signaling perturbations in the same count table were also nearly all silent. The biologically closest measured receptor comparators I used were:

| training perturbation | `n_degs` |
| --- | ---: |
| `Ccr2` | 0 |
| `Cx3cr1` | 0 |
| `Cxcr4` | 0 |
| `Ifnar1` | 0 |
| `Ifnar2` | 0 |
| `Ifngr1` | 0 |
| `Ifngr2` | 0 |
| `Il1r1` | 0 |
| `Il1rap` | 0 |
| `Il6ra` | 0 |
| `Il6st` | 0 |
| `Nfkb1` | 0 |
| `Tlr2` | 0 |
| `Tlr3` | 0 |
| `Tlr4` | 0 |
| `Tlr5` | 0 |
| `Tlr7` | 0 |
| `Tlr8` | 0 |

`Stat1` was the main checked exception in this immune-signaling panel and had only one significant gene.

### Direct rows from the expression parquet

I queried `training_de_all_cell_groups.parquet` directly for those same training perturbations in `151 TH Prkcd Grin2c Glut` rather than using only the pre-aggregated counts. Each comparator had 17,259 measured genes in this focal population. Their adjusted-p minima were consistent with the count table:

| perturbation | parquet `n_degs`, `pvals_adj < 0.05` | smallest `pvals_adj` |
| --- | ---: | ---: |
| `Ccr2` | 0 | 1.000000 |
| `Cx3cr1` | 0 | 1.000000 |
| `Cxcr4` | 0 | 0.067229 |
| `Ifnar1` | 0 | 1.000000 |
| `Ifnar2` | 0 | 1.000000 |
| `Ifngr1` | 0 | 1.000000 |
| `Ifngr2` | 0 | 1.000000 |
| `Il1r1` | 0 | 0.081453 |
| `Il1rap` | 0 | 1.000000 |
| `Il6ra` | 0 | 1.000000 |
| `Il6st` | 0 | 1.000000 |
| `Nfkb1` | 0 | 1.000000 |
| `Stat1` | 1 | 0.027029 |
| `Tlr2` | 0 | 1.000000 |
| `Tlr3` | 0 | 1.000000 |
| `Tlr4` | 0 | 1.000000 |
| `Tlr5` | 0 | 1.000000 |
| `Tlr7` | 0 | 1.000000 |
| `Tlr8` | 0 | 1.000000 |

These matched perturbations had recovered edited-cell counts from 89 to 258 against the same 23,679 matched controls, so the zero outcomes were not explained by missing contrasts in this cell class.

## Synthesis

The functional-stock prior is positive only for Cxcr2-positive cells; it does not supply a reason for a large transcriptional response when the focal thalamic NeuN-positive population has zero detected Cxcr2 molecules across 23,679 control nuclei. The training data show that most assayed targets have no significant downstream genes in this population, and that several immune or chemokine receptor perturbations, including the related GPCRs `Ccr2`, `Cx3cr1`, and `Cxcr4`, also land at zero. I therefore forecast that Cxcr2 loss will be transcriptionally silent in recovered `151 TH Prkcd Grin2c Glut` nuclei and set the integer point estimate to `0`.
