# Avpr2 direct `n_degs` forecast

Endpoint: number of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`
for perturbation `Avpr2` in `151 TH Prkcd Grin2c Glut`.

## Declared target

- Holdout manifest: `[local file: Avpr2.csv]`
- Target: `Avpr2`
- Cell class: `151 TH Prkcd Grin2c Glut`

The declared biology bundle for `Avpr2` reports that the exact in-assay focal
expression feature is present but nearly absent:

| field | value |
|---|---:|
| non-target nuclei in `151 TH Prkcd Grin2c Glut` | 23,679 |
| nuclei with any Avpr2 UMI | 1 |
| percent expressing | 0.004223% |
| total Avpr2 UMI | 1 |
| pseudobulk CPM | 0.0026468 |
| mean raw UMI | 0.00004223 |

The same bundle makes Avpr2 a plausible short-lived functional target only in a
cell that expresses it: Avpr2 is a Gs-coupled vasopressin membrane GPCR, and
heterologous pulse-chase measurements put total V2 receptor turnover on an
hours scale, so a P16 disruptive edit should clear receptor stock by P37-P44 if
new Avpr2 production had been required. The dominant uncertainty is therefore
not protein persistence, but context reach: mouse loss evidence is renal/systemic
and regional mouse thalamus assays did not detect Avpr2.

## Endpoint-matched training table

From the declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` count table:

| statistic | value |
|---|---:|
| training perturbations | 1,674 |
| zero-DEG rows | 1,205 |
| median `n_degs` | 0 |
| 75th percentile `n_degs` | 1 |
| 90th percentile `n_degs` | 2 |

The training Parquet contains no `Avpr2` rows (`Avpr2` is absent as a training
`gene_target`), so these are endpoint-matched observations from other training
perturbations only.

Closest available vasopressin/oxytocin receptor and immediate cAMP-generation
perturbations in the declared count table were all silent in this population:

| target | `n_degs` |
|---|---:|
| Avpr1a | 0 |
| Avpr1b | 0 |
| Oxtr | 0 |
| Adcy1 | 0 |
| Adcy3 | 0 |
| Adcy5 | 0 |

Avpr1a and Avpr1b are the closest paralogous vasopressin receptors present in
the training table. Their zero counts are not independent validation of Avpr2,
but they are compatible with the quantitative prior that sparse neuropeptide
GPCR perturbations often produce no FDR-detectable downstream program in this
thalamic class.

## Synthesis

I assign the point estimate to `0`. The exact target reach is the decisive
evidence: Avpr2 is represented by one molecule in one of 23,679 focal
non-target nuclei, which makes a cell-autonomous loss response in recovered
`151 TH Prkcd Grin2c Glut` neurons unlikely even though a successfully edited
Avpr2-expressing cell should lose functional receptor during the 21-28 day
window. The declared training distribution is strongly zero-inflated in this
cell class, and the closest measured receptor comparators do not provide a
reason to lift the prediction above that zero mode.
