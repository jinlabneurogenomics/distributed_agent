# Hoxc13 n_degs forecast

Target: `Hoxc13`  
Cell context: `151 TH Prkcd Grin2c Glut`  
Predicted `n_degs`: `0`

## Evidence used

- The declared biology bundle for `Hoxc13` reported exact in-assay focal reach of only 2 expressing nuclei among 23,679 non-target nuclei in `151 TH Prkcd Grin2c Glut`:
  - `pct_cells_expressing = 0.00844630263102327`
  - `total_target_umi = 2`
  - `mean_raw_umi = 8.44630263102327e-05`
  - `mean_cp10k = 6.197890549882673e-05`

- The same bundle characterized Hoxc13 as a free nuclear DNA-binding transcription factor whose stock should substantially decline across the P16 to P37-P44 edit window if the target is expressed, but the external loss and expression evidence was hair/nail/tongue-centered rather than thalamic or postnatal neuronal.

- The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` count table contained 1,674 training perturbations. Its focal-class distribution was already sparse:
  - median `n_degs = 0`
  - 1,205 / 1,674 had `n_degs = 0`
  - 1,481 / 1,674 had `n_degs <= 1`

- I used the Hox/TALE developmental program as the most relevant training boundary because Hoxc13 is a posterior HOX transcription factor, but the available measured members were flat in the focal thalamic class. The `n_degs` values in `151 TH Prkcd Grin2c Glut` were:

| perturbation | focal `n_degs` |
|---|---:|
| Hoxa1 | 0 |
| Hoxa3 | 0 |
| Hoxa13 | 0 |
| Hoxb8 | 0 |
| Hoxd10 | 0 |
| Hoxd13 | 0 |
| Meis1 | 0 |
| Meis2 | 0 |
| Pbx1 | 0 |
| Pbx3 | 0 |
| Pknox2 | 0 |

- Direct Parquet checks in the focal class confirmed that each of those 11 Hox/TALE rows had zero genes with `pvals_adj < 0.05`; the nearest group-13 paralogs, `Hoxa13` and `Hoxd13`, each had zero.

- The same-experiment corpus interpreted the Hox-family training signatures consistently with that table:
  - `Hoxa13:F004`: `Hoxa13` was transcriptionally buffered across 22 of 23 measured neuronal groups, with only one weak non-thalamic group.
  - `Hoxd13:F001`: `Hoxd13` produced zero downstream FDR genes in every measured neuronal group.
  - `Hoxd13:F004` and the higher-order HOX/TALE claim: represented HOX paralogs and PBX/MEIS cofactors did not form a shared postnatal neuronal response module.

## Forecast

The decisive feature was target reach: `Hoxc13` was essentially absent from the aggregated thalamic non-target population, with only two UMIs in two nuclei. A P16 edit can plausibly clear Hoxc13 protein in a truly expressing cell by harvest, but the measured population provides almost no expressing substrate on which to generate a reproducible class-level Wilcoxon signature.

The training distribution makes zero the modal focal-class result even before using gene identity, and the biologically closest visible developmental-HOX/TALE perturbations were all zero in this exact cell class. Their packaged findings further argue that postnatal recovered neurons in this assay do not expose a hidden Hox13 or Hox/TALE transcriptional program. I therefore expect no measured gene to pass the BH-adjusted Wilcoxon `p < 0.05` threshold for held-out `Hoxc13` in `151 TH Prkcd Grin2c Glut`.
