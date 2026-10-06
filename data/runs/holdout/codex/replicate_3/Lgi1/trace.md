# Lgi1 DEG-count forecast

Target: `Lgi1` in `151 TH Prkcd Grin2c Glut`

Predicted `n_degs`: **1**

## Evidence

- The declared holdout manifest contains the single target `Lgi1`; the 151-class training count table contains 1,674 other targets and excludes `Lgi1`.
- The endpoint is the count of measured genes with Wilcoxon BH-adjusted `p < 0.05` in the 151 thalamic glutamatergic population.
- The canonical `Lgi1` biology bundle reports exact focal-population expression in the matched non-target 151 cells: `Lgi1` is measured, with `10872 / 23679` cells expressing it, `pct_cells_expressing = 45.914`, `mean_raw_umi = 0.802`, and `mean_log1p_cp10k = 0.322`.
- The same bundle supports target realization by harvest but with important dilution: LGI1 is a secreted ADAM22/ADAM23 synaptic ligand, existing extracellular/receptor-bound ligand is not edited directly, synaptic-protein turnover favors depletion over the 21-28 day window, and unedited neighbors could still supply ligand.
- The 151 training table is very sparse: median `n_degs = 0`; 1,205/1,674 targets are zero; 1,481/1,674 are `0` or `1`; only the upper tail of broad RNA, proteostasis, chromatin, or transcriptional regulators reaches hundreds of DEGs.
- Typed analog nomination against the actual training universe placed only `Adam22` in the exact-complex tier for `Lgi1`; the next LGI-ADAM narrow-module genes present in training were `Dlg4`, `Cacng3`, `Cacng2`, and `Stx1b`.
- Those exact/narrow analog counts in the requested 151 count table were low: `Adam22 = 1`, `Dlg4 = 1`, `Cacng3 = 0`, `Cacng2 = 0`, `Stx1b = 0`.
- Direct inspection of the 151 rows in the expression Parquet showed that the `Adam22` and `Dlg4` counts were self-transcript calls only; the `Cacng2`, `Cacng3`, and `Stx1b` 151 signatures had no BH-significant row at `p_adj < 0.05`.
- Broader nominated synaptic comparators had the same behavior. Among the first 40 typed nominees, 28 had zero 151 DEGs; after excluding the broad `Grin1` NMDAR outlier, the mean count was only `0.385`.
- Same-experiment packaged Findings for the training comparators matched this quantitative picture at the broader report level: `Adam22`, `Dlg4`, `Cacng2`, `Cacng3`, and `Stx1b` were interpreted as buffered or transcriptionally flat downstream perturbations, while `Grin1` was a mechanistically broader thalamic NMDAR exception and `Grin2b` was mainly cortical.

## Synthesis

I treated `Adam22` as the strongest scale-bearing comparator because it is the only training-available ADAM22-LGI1 complex member and its 151 response is exactly one significant gene, the target transcript itself. The broader LGI-ADAM/TARP/PSD-95 module adds four more relevant near-null observations and argues against a durable 3-4 week nuclear activity, stress, or synaptic-remodeling program from a sparse perturbation of this postsynaptic organizer axis.

The exact `Lgi1` expression reach keeps the target from being a pure context-null: roughly 46% of 151 non-target cells express detectable `Lgi1`, so a self-feature call is plausible. But the secreted ligand biology makes a large cell-autonomous downstream program less likely than for a receptor-channel core such as `Grin1`: edited cells can retain pre-existing extracellular/receptor-bound LGI1 initially, the experiment is mosaic, and unedited neighboring neurons may replenish secreted ligand.

Balancing those bearings, I forecast a near-null 151 signature and round the point to the single self-transcript-scale call:

`predicted_n_degs = 1`
