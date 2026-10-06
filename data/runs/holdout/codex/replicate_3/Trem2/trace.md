# Trem2 n_degs forecast

## Target and endpoint

- Target: `Trem2`, from the declared one-row holdout manifest.
- Endpoint: `n_degs`, the number of measured genes with BH-adjusted Wilcoxon `p < 0.05` in `151 TH Prkcd Grin2c Glut`.
- Point prediction: `0`.

## Evidence used

1. **Exact focal-population target reach from the declared `Trem2` biology bundle**

   The requested assay population is postmitotic mouse thalamic NeuN-positive neuronal nuclei harvested 21-28 days after a P16 edit. In matched non-target nuclei from the exact focal class, `Trem2` was essentially absent:

   - `n_non_target_cells = 23679`
   - `total_target_umi = 112`
   - `n_cells_expressing = 110`
   - `pct_cells_expressing = 0.4645466447062798`
   - `mean_raw_umi = 0.004729929473373031`
   - `pseudobulk_cpm = 0.29644145301021696`

   The same biology card places the principal TREM2 function in microglia/myeloid cells as a TREM2-TYROBP surface receptor complex rather than as a neuronal-autonomous pathway. Its stock conclusion says a productive edit in a Trem2-expressing microglial cell should deplete full-length surface TREM2 well within this experimental window, so slow stock turnover is not the limiting factor. The limiting factor is reach: the readout is a NeuN-positive thalamic neuronal population in which the target transcript is nearly undetectable.

2. **Training endpoint distribution**

   The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` table contains 1,674 training perturbations for this same endpoint. It is highly zero-inflated:

   - 1,205 / 1,674 targets have `n_degs = 0`.
   - Median `n_degs = 0`.
   - 75th percentile `n_degs = 1`.
   - 1,571 / 1,674 targets have `n_degs <= 10`.
   - Only 43 / 1,674 targets have `n_degs >= 100`.

   Thus a literal zero is the typical outcome for targets that are weakly coupled to this focal thalamic neuronal readout.

3. **Biologically chosen training comparators**

   I used the training count table, not any Trem2 target outcome, to inspect perturbations of microglial/innate-immune receptors or regulators available in the same table. Every close context comparator I selected was null in the requested cell class:

   | training target | `n_degs` in `151 TH Prkcd Grin2c Glut` |
   | --- | ---: |
   | `Axl` | 0 |
   | `Csf1r` | 0 |
   | `Cx3cr1` | 0 |
   | `Irf8` | 0 |
   | `Lgals3` | 0 |
   | `Mertk` | 0 |
   | `P2ry12` | 0 |
   | `Sall1` | 0 |
   | `Spi1` | 0 |
   | `Tgfbr1` | 0 |
   | `Tlr2` | 0 |
   | `Tlr4` | 0 |

   A direct Parquet filter on `training_de_all_cell_groups.parquet` for the same `group_name` confirmed that these comparators had no gene with `pvals_adj < 0.05`; their best adjusted p-values were all non-significant, ranging from 0.121 for `Irf8` and 0.363 for `Axl` to 1.0 for several receptors.

## Synthesis

The dominant bearing is downward. `Trem2` is a microglial receptor with a plausible acute loss state in Trem2-positive cells, but the perturbation endpoint is recovered thalamic NeuN-positive nuclei where the exact baseline reach is only 112 UMIs across 23,679 non-target nuclei. Published microglial Trem2-loss phenotypes and TREM2-TYROBP receptor biology show that Trem2 loss can matter in neural tissue, yet they require a microglial compartment and do not establish a P16 sparse neuronal edit effect in thalamic neurons.

The matched training data reinforce that interpretation: the endpoint background is mostly zero, and perturbing other microglial/innate-immune targets in the same focal cell class produced zero BH-significant measured genes, with no borderline raw Parquet signal. I therefore put the integer point forecast at the floor rather than assigning a small positive DEG count.

The Trem2 held-out target expression signature and held-out Trem2 DEG count were not used.
