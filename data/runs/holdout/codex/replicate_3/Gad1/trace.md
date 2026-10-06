# Gad1 DEG-count forecast

Target and endpoint:

- Held-out target: `Gad1`, from the declared one-row manifest.
- Focal population: `151 TH Prkcd Grin2c Glut`.
- Endpoint: number of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`.
- Point prediction: `0`.

Evidence used:

- The biology-only `Gad1` characterization says a disruptive P16 edit should stop new GAD67 supply and should substantially deplete the Gad1-encoded enzymatic stock by the P37-P44 harvest. Existing GAD67/GABA are not instantaneously removed, and Gad2 can partially buffer GABA synthesis, but the bundle judges the Gad1 stock as likely substantially depleted over the 21-28 day window.
- The same bundle reports exact in-assay reach for `Gad1` in `151 TH Prkcd Grin2c Glut`: 2,900 of 23,679 non-target nuclei expressed the feature, `pct_cells_expressing = 12.247%`, mean raw UMI was `0.184`, and pseudobulk CPM was `11.52`. The perturbation is therefore well aligned with a GABA-synthesis enzyme but poorly aligned with most cells in this broad thalamic glutamatergic population.
- The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` table is heavily zero-inflated: 1,205 of 1,674 measured training targets had `n_degs = 0`; the median was 0 and the 75th percentile was 1.
- Direct presynaptic or metabolic GABA-axis comparators in the declared count table were all null in the requested focal population at the exact BH 0.05 endpoint: `Gad2 = 0`, `Abat = 0`, `Slc32a1 = 0`, and `Slc6a1 = 0`.
- A DuckDB scan of the declared expression Parquet for `151 TH Prkcd Grin2c Glut` reproduced those zeros over 17,259 measured rows per comparator. The smallest adjusted p-values were `1.0` for `Gad2`, `1.0` for `Slc32a1`, `1.0` for `Slc6a1`, and `0.831` for `Abat`; this was not a threshold rounding artifact.
- Represented GABA-receptor perturbations were also tiny in the focal count table: the 13 alpha/beta/gamma/delta/rho/GABA_B targets present summed to 10 DE genes, with a maximum of 4 for `Gabrb2`. The one receptor subunit with a visible 151-TH response was a postsynaptic activity-threshold case rather than a close presynaptic GABA-supply analogue for `Gad1`.
- Same-experiment packaged Findings for the measured paralog `Gad2` reported no meaningful whole-universe signature neighbor and placed `Gad2`, `Slc32a1`, `Slc6a1`, and `Abat` in an effectively self-only/sparse presynaptic GABA-axis group. Those reports are a semantic layer over the same experiment, so I used them to interpret the training perturbations rather than as independent replication.

Reasoning:

`Gad1` has stronger basal-GABA biology than `Gad2`, so I did not copy the `Gad2` null blindly. However, the focal class is glutamatergic and only a small minority of recovered non-target nuclei showed any `Gad1` RNA. In this sparse mosaic, survivor-conditioned nuclear assay, the most endpoint-matched training perturbations that change GABA production, loading, catabolism, or uptake were exactly or nearly flat, even when related GABA receptor genes could occasionally make one to four detectable downstream hits. The low focal reach and the presynaptic GABA-axis nulls outweighed the fact that functional GAD67 stock should turn over after editing, so the most likely BH 0.05 DEG count is at the point mass of the local training distribution.
