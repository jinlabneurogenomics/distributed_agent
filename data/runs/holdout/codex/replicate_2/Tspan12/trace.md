# Tspan12 direct n_degs forecast

## Target and endpoint

- Target manifest: `Tspan12`, from the declared one-row `Tspan12.csv` manifest.
- Endpoint: number of measured genes in `151 TH Prkcd Grin2c Glut` with BH-adjusted Wilcoxon `pvals_adj < 0.05`.
- Numerical inputs used:
  - declared training count table `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`;
  - declared full-count DE Parquet `training_de_all_cell_groups.parquet`;
  - declared biology-only Tspan12 bundle `biology_bundles/Tspan12.json`;
  - same-experiment corpus summaries for visible training genes only.

I treated the count table, Parquet, and corpus as different views of the same
PerturbAI atlas experiment rather than independent replication.  I did not use
the withheld Tspan12 DE rows or an observed Tspan12 count.

## Tspan12 biology

The declared characterization bundle places the established TSPAN12 operation
at the plasma membrane as a Norrin/FZD4/LRP5/6 beta-catenin co-receptor.  The
direct in-vivo phenotypes are retinal vascular and adult retinal-endothelial:
they sit outside the NeuN-positive thalamic neurons assayed here.  The same
bundle gives exact focal-population expression for the target, so Tspan12 RNA is
not absent from `151 TH Prkcd Grin2c Glut`, but the reach is modest:

- `mean_raw_umi = 0.3232`
- `mean_log1p_cp10k = 0.1396`
- `pct_cells_expressing = 25.90%`
- `pseudobulk_cpm = 20.26`

The functional-stock card also calls harvest an early/partial-loss point:
disruptive editing should stop new TSPAN12 supply, but the best timing data
showed a retinal-endothelial barrier program declining over roughly 2-3 months,
not immediate loss within the 21-28 day atlas window.

My interpretation is therefore: there is enough assayed-cell RNA that a
self-target or very small response is plausible, but the best-supported
function is endothelial and persistent enough that a broad thalamic neuronal
signature should not be expected.

## Training measurements

The held-out 151-class count table contains 1,674 visible perturbations.
At the requested FDR < 0.05 threshold:

- 1,205 / 1,674 are zero-count responses, or 71.98%.
- 1,481 / 1,674 have at most 1 DEG, or 88.47%.
- 1,546 / 1,674 have at most 5 DEGs, or 92.35%.
- The median is 0; the mean is 14.05 because a small number of targets have
  hundreds to thousands of DEGs.

The most relevant visible genes were the exact Norrin/FZD4/LRP5/6 pathway
relatives from the Tspan12 card:

| training target | 151-class FDR < 0.05 DEGs |
|---|---:|
| Fzd4 | 0 |
| Lrp5 | 0 |
| Lrp6 | 4 |
| Ctnnb1 | 383 |
| Tcf7l2 | 106 |

I verified those counts directly against the Parquet in `151 TH Prkcd Grin2c
Glut`: `Fzd4` and `Lrp5` had zero FDR < 0.05 genes among 17,259 profiled
features, `Lrp6` had 4, `Ctnnb1` had 383, and `Tcf7l2` had 106.  The broader
responses belong to intracellular beta-catenin/TCF effectors; I considered them
upper biological context rather than magnitude analogs for the extracellular
TSPAN12 co-receptor.

The same-experiment corpus reinforces that separation without adding an
independent measurement: its visible Fzd4/Lrp5/Lrp6 reports state that Fzd4 was
silent in recovered NeuN-positive neuronal classes, Lrp5 lacked canonical
beta-catenin/TCF feedback in the DE surface, and only Lrp6 weakly converged with
Ctnnb1 in the 151 thalamic class.

I also ran a symmetric profile comparison for `Fzd4`, `Lrp5`, `Lrp6`, `Ctnnb1`,
and `Tcf7l2` on the 151 Parquet rows.  The response activity split was exactly
the count-table split:

| node | significant features | profile activity |
|---|---:|---|
| Fzd4 | 0 | no significant features |
| Lrp5 | 0 | no significant features |
| Lrp6 | 4 | 1_to_9_significant_features |
| Ctnnb1 | 383 | at_least_50_significant_features |
| Tcf7l2 | 106 | at_least_50_significant_features |

Fzd4 is the most literal receptor-complex comparator for Tspan12, and both Fzd4
and Lrp5 were flat in the same assayed population.  Lrp6 shows that a proximal
Wnt receptor can be detectable in 151, but even that response was only four
genes at the task threshold.

## Point forecast

The zero-heavy empirical base rate, the flat Fzd4/Lrp5 receptor analogs, and the
retinal-endothelial rather than thalamic-neuronal Tspan12 biology all point to a
near-null endpoint.  Modest Tspan12 RNA reach and the nonredundant co-receptor
role keep the forecast from being a biological impossibility, but they do not
raise it above the no-DEG state for this 3-4 week recovered-neuron assay.

Predicted `n_degs`: **0**.
