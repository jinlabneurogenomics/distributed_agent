# Il10rb n_degs forecast

## Declared target and endpoint

- Target: `Il10rb`
- Cell population: `151 TH Prkcd Grin2c Glut`
- Endpoint: `n_degs`, the number of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`
- The declared training count table contains 1,674 non-held-out targets for this exact population; `Il10rb` is not present in that table.

## Evidence used

### Training-count scale

The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` table is sparse and heavy-tailed:

- 1,205 / 1,674 training targets have `n_degs = 0`.
- The median is 0.
- The 75th percentile is 1.
- The 90th percentile is 2.
- Only 106 / 1,674 have at least 10 DEGs and 43 / 1,674 have at least 100.

This makes a zero or singleton count the default regime unless the biology points to one of the rare broad survivor-state programs.

### Target biology and reach

The canonical `Il10rb` biology bundle says IL10RB is a shared class-II cytokine-receptor accessory chain. A disruptive edit should stop new IL10RB production, but it does not directly inactivate already assembled surface receptor chains; ligand-triggered endocytosis supports some turnover, while recycling versus irreversible stock loss over the 21-28 day assay interval remains unresolved. The card therefore calls the expected harvest state `partially_depleted_or_leading_edge`, with sparse stock evidence.

Exact focal-population expression also argues against a broad cell-autonomous response in this thalamic class:

- `Il10rb` was detected in 818 / 23,679 non-target nuclei in `151 TH Prkcd Grin2c Glut`.
- `pct_cells_expressing = 3.4545`.
- `mean_raw_umi = 0.0395`, `mean_cp10k = 0.0258`, and pseudobulk expression was 2.477 CPM.

The bundle contains postnatal neural and systemic evidence that IL10RB can matter biologically, but the closest neural phenotype was mediated by transferred CD4 T cells in an adult facial-axotomy model, not by healthy thalamic neurons. That supports possible observability in some neural setting, but it is not a reason to expect a large neuron-autonomous transcriptional footprint here.

### Measured same-pathway training perturbations

The closest represented direct partner, `Il10ra`, had `n_degs = 0` in the focal count table. Same-experiment Findings summarized `Il10ra` as transcriptionally silent at FDR < 0.10 in every recovered neuronal class and specifically reported absence of the expected IL-10/STAT3 inflammatory and neuronal-survival programs after `Il10ra` perturbation.

Other measured receptor and JAK/STAT-family comparators in this same population were also flat:

- `Il6st = 0`
- `Osmr = 0`
- `Ifnar1 = 0`
- `Ifnar2 = 0`
- `Ifngr1 = 0`
- `Ifngr2 = 0`
- `Stat2 = 0`
- `Stat3 = 0`
- `Stat1 = 1`

The corpus records for `Ifnar1`, `Ifnar2`, `Ifngr1`, `Ifngr2`, `Il6st`, `Osmr`, `Stat1`, `Stat2`, and `Stat3` all support the same interpretation: basal postmitotic neuronal loss of these cytokine/JAK-STAT receptor axes either produced no corrected downstream response or at most isolated singleton hits, without a coherent interferon, STAT, or inflammatory module in recovered neurons.

I also compared the declared Parquet score profiles for `Il10ra`, `Il6st`, `Ifnar1`, `Ifnar2`, `Ifngr1`, `Ifngr2`, `Osmr`, `Stat1`, `Stat2`, `Stat3`, and `Atg16l1` within `151 TH Prkcd Grin2c Glut`. The FDR activity counts in that exact Parquet slice were zero for 10 / 11 of those targets and one for `Stat1`. Pairwise whole-profile correlations among focal receptor/STAT nodes were near background, for example:

- `Il10ra` versus `Stat1`: Pearson -0.0066, cosine -0.0065
- `Il10ra` versus `Stat2`: Pearson -0.0176, cosine -0.0175
- `Stat3` versus `Stat1`: Pearson 0.0292, cosine 0.0302
- `Ifnar1` versus `Stat2`: Pearson 0.0151, cosine 0.0148

Thus the expression parquet did not reveal a recurrent cytokine-receptor module hidden below the DEG-count table; these were weak, mostly null basal signatures.

## Forecast

Two considerations push down from the already-zero-centered training distribution: exact `Il10rb` expression reaches only a small minority of this recovered thalamic population, and measured IL-10/JAK-STAT/inflammatory receptor comparators are quiet in the same basal postnatal neuronal assay. Two considerations keep the estimate from being a structural zero: IL10RB is a nonredundant shared receptor chain, and the biology bundle favors at least partial depletion of dynamic receptor pools by harvest.

Balancing those, the most likely integer count is the same as the closest measured partner and the wider cytokine-receptor neighborhood in this population:

`predicted_n_degs = 0`
