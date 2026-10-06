# Tspan12 direct DEG-count forecast

Target: `Tspan12` in `151 TH Prkcd Grin2c Glut`

Predicted `n_degs`: `0`

## Evidence used

- The declared holdout manifest contains the single target `Tspan12`.
- The requested endpoint is the `151 TH Prkcd Grin2c Glut` count of measured genes with BH-adjusted Wilcoxon `p < 0.05`.
- In the declared 151-class training count table, the response distribution is highly zero-inflated: 1,205 of 1,674 training perturbations have `n_degs = 0`; the median is 0, the 75th percentile is 1, and the 90th percentile is 2.
- The exact target-expression card shows that `Tspan12` is detectable but dilute in the focal non-target nuclei: 6,134 / 23,679 nuclei express it, `pct_cells_expressing = 25.9048`, `mean_raw_umi = 0.3232`, `mean_log1p_cp10k = 0.1396`, and `pseudobulk_cpm = 20.256`.
- The same card assigns the established TSPAN12 operation to a Norrin/FZD4/LRP5/6 plasma-membrane co-receptor in retinal vascular endothelial cells, not to thalamic NeuN-positive neurons. It also adjudicates the P16 to P37-P44 CRISPR window as an early or partially depleted phase because adult endothelial Tspan12 loss produces progressive blood-retina-barrier dysfunction over roughly 2-3 months rather than immediate loss of all installed function.
- Direct Parquet counts in the requested `151 TH Prkcd Grin2c Glut` context show that the represented receptor-layer Wnt relatives closest to a Tspan12/Norrin receptor perturbation were flat at FDR 0.05: `Fzd2 = 0`, `Fzd4 = 0`, `Fzd6 = 0`, `Fzd9 = 0`, `Lrp5 = 0`, `Lgr4 = 0`, `Lrp4 = 0`, `Ror1 = 0`, `Ror2 = 0`, and `Ryk = 0`. These were not all unpowered nulls; for example the matched 151-class perturbed-cell counts were 188 for `Fzd4` and 230 for `Lrp5` versus 171 for the strongly responsive `Ctnnb1`.
- In the same Parquet slice, the canonical downstream Wnt effectors were the responsive exceptions rather than the receptor-layer norm: `Ctnnb1 = 383`, `Tcf7l2 = 106`, `Gsk3b = 6`, and `Lrp6 = 4` at BH `p < 0.05`. The more TSPAN12-proximal `Fzd4` and `Lrp5` counts were both 0.
- Same-experiment corpus Findings agree with that split. `Fzd4:F001` reports that `Fzd4` loss was transcriptionally silent in every recovered NeuN-positive neuronal class, and `Fzd4:F002` reports non-convergence with the Wnt nodes that were detectable in the neuronal data: `Ctnnb1` and weakly `Lrp6` in thalamic glutamatergic cells. `Lrp5:F003` reports that `Lrp6`, not `Lrp5`, converged with `Ctnnb1` on the six-gene 151-class module. `Lrp6:F004` and `Ctnnb1:F007` both frame the observed Wnt state as branch-specific: it links `Lrp6` with `Ctnnb1`/`Tcf7l2` and does not extend to `Lrp5`, single Frizzled receptors, `Lgr4`, `Ror1`, `Ror2`, or `Ryk`.
- The only represented tetraspanin target in the 151 count table, `Tspan7`, had `n_degs = 1`; querying the Parquet showed that its lone 151-class FDR 0.05 hit was its own target transcript. This supports a near-flat expectation for membrane tetraspanins in this nuclear-RNA endpoint rather than a multi-gene response.

## Forecast rationale

`Tspan12` is expressed in a minority of the assayed thalamic nuclei, so a transcript-level self hit or a very small response was possible. The closer biological comparators nevertheless point to a zero count. TSPAN12 is a receptor cofactor most specifically tied to the Norrin/FZD4/LRP5/6 receptor layer; in the actual 151-class training measurements, `Fzd4`, `Lrp5`, the other measured Frizzled receptors, `Lgr4`, and the ROR/RYK receptor comparators were all `0` despite the assay being able to recover a Wnt/catenin state downstream through `Ctnnb1`, `Tcf7l2`, and weakly `Lrp6`. The biology bundle further weakens the case for a 3-4 week cell-autonomous thalamic neuronal response because the best-supported function is retinal endothelial and existing TSPAN12-dependent stock is expected to be only partly depleted by harvest.

I therefore used the receptor-layer nulls, not the downstream `Ctnnb1` footprint, as the quantitative anchor. My point forecast is a flat 151-class signature with no measured genes crossing BH-adjusted Wilcoxon `p < 0.05`.
