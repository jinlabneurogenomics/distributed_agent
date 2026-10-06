# Slc24a5 n_degs forecast

Target: `Slc24a5`

Population: `151 TH Prkcd Grin2c Glut`

Predicted `n_degs`: `0`

## Evidence used

- The declared one-row holdout manifest names only `Slc24a5`.
- The requested endpoint is the number of measured genes in `151 TH Prkcd Grin2c Glut` with BH-adjusted Wilcoxon `p < 0.05`.
- The declared biology bundle says NCKX5 is an intracellular potassium-dependent sodium-calcium exchanger best established in melanocytes and pigment-organelle/trans-Golgi biology. Slc24a5-null mice have ocular and pigment phenotypes, but the bundle identified no matched thalamic-neuron loss phenotype.
- The same biology bundle adjudicates existing NCKX5 stock as likely substantially depleted by a disruptive P16 edit by the P37-P44 harvest if the target is present, but this only establishes that the perturbation can be functionally realized; it does not establish thalamic neuronal demand.
- Exact focal-population expression in matched non-target `151 TH Prkcd Grin2c Glut` nuclei is nearly absent: 73 total Slc24a5 UMIs across 23,679 nuclei, 64 expressing nuclei, `pct_cells_expressing = 0.2702816841927446`, `mean_raw_umi = 0.0030829004603234933`, and `mean_cp10k = 0.0016082558476091483`.
- The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` contains 1,674 training perturbations. Its median DEG count is 0; 1,205/1,674 targets have 0 DEGs, 1,481/1,674 have at most 1 DEG, the 90th percentile is 2 DEGs, and the 95th percentile is 18 DEGs.
- No close Slc24 paralog, Slc8b1 paralog, or canonical pigment genes were present as training perturbations in that count table. The looser set of `Slc*` transporter targets in the table was mostly silent in this cell class: 14/23 had 0 DEGs and 21/23 had at most 1 DEG. A direct Parquet query over the `151 TH Prkcd Grin2c Glut` rows confirmed those `Slc*` counts against 17,259 measured genes per queried target.

## Reasoning

The Slc24a5 edit should stop production of any renewed NCKX5 protein, so I did not treat the perturbation as impossible. The limiting evidence is instead context reach. The assayed thalamic glutamatergic population contains essentially no Slc24a5 RNA in the matched non-target cells, and the curated mammalian loss biology points to pigment cells and ocular pigment epithelium rather than a postnatal thalamic-neuron requirement.

Because no matched Slc24/pigment comparator exists in the training count table, the useful quantitative anchors are the focal class base rate and the loose transporter perturbations. Both favor the point mass at zero: the overall training median is 0 and nearly three quarters of training targets are zero; transporter perturbations with far clearer neuronal solute-carrier annotations were also usually zero or self-only in this cell class. Given a 0.27% expressing-cell reach for Slc24a5, even a real cell-autonomous effect would be averaged across an almost entirely non-expressing recovered population and is unlikely to produce any BH-significant aggregate gene in this endpoint.

I therefore forecast `0` DEGs.
