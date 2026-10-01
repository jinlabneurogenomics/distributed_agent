# Supplementary Figure 10E source

- Original plotter: `manuscript/_archive_260924/fig4/c/build_gt_panels.py`
- Shared archived loader and palette: `manuscript/_archive_260924/fig4/c/_common.py`
- Archived export: `manuscript/_archive_260924/fig4/c/panels/gt_recovery_vs_aav.{png,svg,pdf}`
- Full Fisher source: `debug/depletion/ground_truth/fisher/fisher_results_per_gene_predicted_group.csv`
- Top-rank source: `debug/depletion/ground_truth/fisher/top150_depletion_151_TH_Prkcd_Grin2c_Glut_predicted_group.csv`

`fisher_results_151_TH_Prkcd_Grin2c_Glut.csv` is a lossless row filter of the
full Fisher source to the focal cell type (1,948 unique targets). The notebook
recomputes `log2(odds_ratio)`, identifies ranks 1–100 from the copied ranking,
and reproduces the archived log-log recovery scatter.
