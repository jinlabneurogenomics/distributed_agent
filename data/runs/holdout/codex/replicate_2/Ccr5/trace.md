# Ccr5 n_degs forecast

Endpoint: number of measured genes in `151 TH Prkcd Grin2c Glut` with Wilcoxon
BH-adjusted `p < 0.05`.

Point prediction: `0`.

## Evidence used

- The one-row declared holdout manifest names `Ccr5`.
- The exact Ccr5 focal-population reach in the declared biology bundle is very
  low: 76 of 23,679 matched non-target `151 TH Prkcd Grin2c Glut` nuclei
  expressed Ccr5, with `pct_cells_expressing = 0.3209595`,
  `mean_raw_umi = 0.00363191`, `mean_log1p_cp10k = 0.00162893`, and
  `pseudobulk_cpm = 0.227625`.
- The same bundle adjudicates functional stock as
  `likely_substantially_depleted`: CCR5 is a renewable cell-surface GPCR, and
  the best turnover/timing evidence says loss of new receptor supply should be
  realized by the 21-28 day harvest window in cells that normally use CCR5.
- The same biology bundle leaves thalamic-neuron demand uncertain. Its strongest
  postnatal neural evidence comes from adult hippocampus/cortex or injury
  contexts, not from healthy juvenile thalamic glutamatergic neurons; it also
  notes unresolved buffering by the paralog Ccr2.
- The declared focal count table contains 1,674 visible training perturbations.
  Its response distribution is zero-heavy in this cell class: 1,205 of 1,674
  training targets have `n_degs = 0`, the median is 0, and only 193 targets have
  at least two DE genes.
- Training perturbations in the closest visible receptor neighborhood were also
  quiet in the declared focal count table:
  - `Ccr2`, the curated Ccr5 paralog, had `n_degs = 0`.
  - Other visible chemokine-receptor perturbations, `Cx3cr1` and `Cxcr4`, also
    had `n_degs = 0`.
  - A broader manual GPCR/receptor sweep of the same table gave 63 zeros among
    74 visible receptor-like targets; the remaining 11 each had exactly one DEG.
- Direct inspection of the declared expression Parquet for the focal cell class
  confirmed that the selected visible chemokine-family rows were zero because no
  measured gene passed the same BH threshold:
  - `Ccr2`: 17,259 measured genes, `n_pert_matched = 170`,
    `n_ctrl_matched = 23679`, 0 genes with `pvals_adj < 0.05`, minimum adjusted
    p-value 1.0.
  - `Cx3cr1`: 17,259 measured genes, `n_pert_matched = 258`,
    `n_ctrl_matched = 23679`, 0 genes with `pvals_adj < 0.05`, minimum adjusted
    p-value 1.0.
  - `Cxcr4`: 17,259 measured genes, `n_pert_matched = 191`,
    `n_ctrl_matched = 23679`, 0 genes with `pvals_adj < 0.05`, minimum adjusted
    p-value 0.067228836.

## Reasoning

The functional-stock card argues against a long-lived pre-edit CCR5 pool: if a
thalamic neuron depends on CCR5, the P16 edit should plausibly deplete receptor
activity before P37-P44. That keeps the perturbation biologically real rather
than an automatic stock-retention null.

The stronger quantitative bearing is reach. The exact in-assay Ccr5 expression
measurement shows only a minute detected receptor pool in the aggregated
thalamic glutamatergic population. Because the endpoint is a recovered-nucleus
transcriptional signature averaged over this population, a dynamic GPCR present
in roughly 0.3% of matched controls has little opportunity to drive a broader
class-wide FDR-significant program unless it gates a separate nonautonomous
state.

The visible training data support the low end of the count scale for this kind
of perturbation. The focal count table is already zero-inflated, and every
available chemokine-family receptor comparator, including the curated paralog
`Ccr2`, has zero significant genes in the same cell class. The Parquet rows
show that these were not threshold-masked large responses: each selected
comparator had no adjusted p-value below 0.05 across the 17,259 focal measured
genes.

Therefore, Ccr5 loss in `151 TH Prkcd Grin2c Glut` is expected to be
transcriptionally silent at the requested threshold. The exact integer forecast
is `0`.
