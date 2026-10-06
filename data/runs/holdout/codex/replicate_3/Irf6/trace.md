# Direct n_degs forecast for Irf6

## Target and endpoint

- Target: `Irf6`
- Cell class: `151 TH Prkcd Grin2c Glut`
- Endpoint: number of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`
- Point prediction: `0`

## Evidence used

### Declared target biology

The held-out biology bundle identifies IRF6 as an intracellular IRF-family DNA-binding transcription factor whose operative pool is renewable rather than a durable installed structure. The functional-stock card therefore expects a disruptive edit at P16 to substantially deplete functional IRF6 by the P37-P44 harvest, because the known IRF6 stability scale is hours rather than 21-28 days. This supports the loss as biologically realizable in any cell that both expressed and edited `Irf6`.

The same bundle strongly limits expected focal reach. In non-target cells from `151 TH Prkcd Grin2c Glut`, `Irf6` had only 13 UMIs across 23,679 nuclei, a mean raw UMI of 0.000549, mean CP10K of 0.000414, pseudobulk CPM of 0.0344, and only 0.0549% of nuclei with any detected `Irf6`. The bundle also does not provide a matched acute postnatal thalamic loss phenotype; the strongest mouse phenotypes are developmental and mostly epithelial, with only weak cross-context neural evidence.

### Training counts in the requested class

The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` table contains 1,674 training perturbations and is zero-heavy:

- 1,205 / 1,674 have `n_degs = 0`
- median `n_degs = 0`
- third quartile `n_degs = 1`
- 90th percentile `n_degs = 2`
- 95th percentile `n_degs = 18`
- 99th percentile `n_degs = 430`

All represented IRF-family training perturbations in this class were null at FDR 0.05:

| training target | n_degs |
|---|---:|
| Irf1 | 0 |
| Irf2 | 0 |
| Irf2bpl | 0 |
| Irf3 | 0 |
| Irf5 | 0 |
| Irf8 | 0 |
| Irf9 | 0 |

Nearby basal innate-immune and cytokine-response perturbations were also essentially silent in this class: `Ifnar1`, `Ifnar2`, `Ifngr1`, `Ifngr2`, `Nfkb1`, `Stat2`, `Stat3`, `Stat4`, `Stat5b`, and `Tlr2/3/4/5/7/8` all had 0 FDR 0.05 genes; `Stat1` had 1.

### Training Parquet check

I queried the declared `training_de_all_cell_groups.parquet` rather than the held-out target signature. Across all measured neuronal classes for the same IRF/IFN/TLR/STAT axis:

- `Irf1`, `Irf2`, `Irf2bpl`, `Irf3`, `Irf5`, `Irf8`, and `Irf9` each had 0 FDR 0.05 hits in every measured group.
- `Ifnar1`, `Ifnar2`, `Ifngr1`, `Ifngr2`, `Nfkb1`, `Stat2`, `Stat3`, `Stat4`, `Stat5b`, `Tlr2`, `Tlr4`, `Tlr5`, and `Tlr7` likewise had 0 FDR 0.05 hits across their measured groups.
- The few nonzero axis perturbations were isolated off-class events: `Stat1` had 2 all-group FDR 0.05 hits, `Tlr3` had 1, and `Tlr8` had 1.

The packaged same-experiment corpus agreed with this as interpretation rather than independent replication: `Irf5` was reported as having no robust downstream response in any recovered NeuN-positive class, and the `Irf1`, `Irf2`, `Irf3`, `Irf9`, `Stat1`, `Stat2`, and `Stat3` reports all describe a flat basal neuronal IRF/IFN/STAT neighborhood rather than a constitutive interferon module.

## Synthesis

I treated the functional-stock prior and expression reach separately. The stock prior says an edit could remove IRF6 protein within the assay window, but the exact focal expression says there is almost no aggregate thalamic substrate to remove: only 13 of 23,679 matched non-target nuclei had any `Irf6` molecule detected. Against that, the training base rate is already dominated by zeros, and every direct IRF-family comparator measured in this focal class had `n_degs = 0`.

The main uncertainty is unobserved protein in a very rare `Irf6`-positive subpopulation or a low-RNA/high-protein state. I did not upshift for that because a response in fewer than one tenth of one percent of assayed nuclei would need an unusually large and coherent survivor-state program to create BH-significant aggregate DE, and the training IRF/IFN axis gives no empirical evidence for such basal neuronal amplification.

Therefore the most likely integer endpoint is:

```tsv
target_name	predicted_n_degs
Irf6	0
```
