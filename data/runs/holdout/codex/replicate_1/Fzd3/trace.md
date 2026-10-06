# Fzd3 n_degs forecast

## Target and endpoint

- Target: `Fzd3`
- Cell class: `151 TH Prkcd Grin2c Glut`
- Endpoint: measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05` in the held-out `Fzd3` perturbation profile.
- The one-row manifest names only `Fzd3`. The training count table has 1,674 other targets and does not contain `Fzd3`.

## Evidence used

The declared `Fzd3` biology bundle shows that the target is present in the exact focal population but at modest single-cell depth:

- 15,381 of 23,679 non-target nuclei expressed `Fzd3`;
- `pct_cells_expressing = 64.9563`;
- `mean_cp10k = 0.7779`;
- `mean_log1p_cp10k = 0.4824`;
- `mean_raw_umi = 1.2389`.

The functional-stock card judged the FZD3 membrane-receptor pool likely to be substantially depleted by P37-P44, because a disruptive edit should stop new receptor production and ordinary membrane-receptor turnover is compatible with depletion over 21-28 days. The same card left the postnatal transcriptional consequence unresolved: the direct mouse loss phenotype is embryonic forebrain axon-tract construction, no matched P16 thalamic-neuron deletion clock was found, and engineered Fzd6 rescue is context-limited rather than evidence for endogenous postnatal compensation.

The 151-class training count distribution is zero-inflated and strongly skewed:

- 1,205 / 1,674 training targets have `n_degs = 0`;
- median = 0, 75th percentile = 1, 90th percentile = 2;
- mean = 14.05 because a small tail of RNA-processing, proteasome, and general transcriptional regulators has hundreds to thousands of DEGs.

The closest measured Fzd3 analogs in the same class were nearly all silent:

| training set | same-class counts |
| --- | --- |
| Frizzled paralogs | `Fzd2 = 0`, `Fzd4 = 0`, `Fzd6 = 0`, `Fzd9 = 0` |
| Wnt/PCP receptors and proximal receptors | `Celsr2 = 1`, `Prickle1 = 0`, `Ryk = 0`, `Ror1 = 0`, `Ror2 = 0`, `Lrp5 = 0`, `Lrp6 = 4` |
| Wnt intracellular/canonical effectors | `Gsk3b = 6`, `Tcf7l2 = 106`, `Ctnnb1 = 383` |

A direct scan of `training_de_all_cell_groups.parquet` in `151 TH Prkcd Grin2c Glut` confirmed these counts over 17,259 measured features for the Wnt/Frizzled comparator set. Profile comparison of the 14 Wnt/Frizzled training nodes likewise found no significant genes for 9/14 nodes, 1-9 significant genes for 3/14, and at least 50 significant genes only for the broader downstream effectors `Ctnnb1` and `Tcf7l2`.

Axon-guidance receptor perturbations in the same count table gave the same boundary: among 25 available receptors and guidance cues that overlapped the table, the median was 0, the mean was 0.4, and the maximum was `Ntrk2` at 3.

## Synthesis

I did not pool the high `Ctnnb1` or `Tcf7l2` counts into the point estimate. They are broad nuclear or pathway-level effectors and much less target-adjacent than the Frizzled-family and PCP/guidance receptor perturbations, all of which were null or single-digit in the same class.

`Fzd3` itself is expressed in many focal nuclei and should be an editable functional substrate by harvest, so a tiny response would not be surprising. However, the held-out perturbation is postmitotic and acute, while the strongest direct Fzd3 phenotypes are developmental wiring phenotypes likely installed before P16. Given four assayed Frizzled paralogs at zero DEGs, the broader proximal Wnt/PCP receptor set centered at zero, and the same behavior across guidance receptors, the most likely exact count is the modal count rather than a small positive tail value.

Predicted `n_degs`: 0
