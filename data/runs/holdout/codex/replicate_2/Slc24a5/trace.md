# Slc24a5 DEG-count forecast

Target: `Slc24a5`

Cell class: `151 TH Prkcd Grin2c Glut`

Endpoint: number of measured genes with BH-adjusted Wilcoxon `p < 0.05`

Predicted `n_degs`: `0`

## Evidence

- The holdout manifest contains one target, `Slc24a5`.
- The exact focal-population expression card reports very little detectable Slc24a5 RNA in the matched non-target nuclei for this class: 73 total target UMIs across 23,679 nuclei, 64 expressing nuclei, 0.270281684% expressing nuclei, mean raw UMI 0.003082900, mean CP10k 0.001608256, and pseudobulk CPM 0.1932163. This argues that only a tiny fraction of the aggregated thalamic neuronal population has detectable in-assay target expression.
- The biology bundle supports functional realization only weakly for the requested context. NCKX5/Slc24a5 is an intracellular potassium-dependent sodium/calcium exchanger best established at the trans-Golgi/pigment-organelle axis; loss in mouse is ocular/pigment rather than postnatal neuronal; adult mouse brain evidence points to low average abundance and strong choroid-plexus expression. The P16-to-P37/P44 edit interval is long enough that existing exchanger stock would probably decline in edited expressing cells, but no thalamic-neuron requirement or direct neural turnover clock was identified.
- The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` table has 1,674 training targets. It is zero-heavy: 1,205/1,674 targets have 0 DEGs, 1,481/1,674 have 0 or 1 DEG, the median is 0, the 75th percentile is 1, the 90th percentile is 2, and the arithmetic mean is inflated to 14.05 by rare large programs.
- I queried `training_de_all_cell_groups.parquet` only in the focal `151 TH Prkcd Grin2c Glut` context for broad cation-channel and solute-carrier training perturbations. The true `Slc*` transporter rows, excluding the opposite-strand `Slc7a6os` naming case, were 14/22 at 0 DEGs, 7/22 at exactly 1 DEG, and 1/22 at 4 DEGs. The one-DEG `Slc` cases were self-transcript calls: `Slc1a1`, `Slc1a2`, `Slc22a17`, `Slc25a12`, `Slc25a4`, `Slc25a46`, and `Slc9a7` each had only the targeted transcript passing adjusted `p < 0.05`; `Slc6a17` had its own transcript plus three other genes.
- Nearby broad ion-channel families were similarly sparse in the same training count table and focal Parquet rows: 14/20 `Kcn*` perturbations were 0 and the remaining six were self-transcript-only 1-DEG calls; 7/10 `Cacn*` perturbations were 0, two were self-transcript-only 1-DEG calls, and only `Cacna1g` reached 12 DEGs. `Grin1` was a larger exception at 89 DEGs, but the NMDA-receptor core operation is much closer to excitatory thalamic neuronal physiology than Slc24a5 pigment-organelle cation exchange.

## Reasoning

`Slc24a5` should sit at the bottom of the 151-class response distribution. The generic prior in this cell class is already zero, and the biologically closer transporter/channel training perturbations show that weak ion-transport targets usually produce no detectable aggregate program; when they produce a single call, that call is commonly the knocked-down target transcript itself. Slc24a5 is far less visible in the focal nuclei than those self-hit donors and has its best-established biology outside NeuN-positive thalamic neurons, so even a self-transcript hit is unlikely. I therefore round the forecast to the floor rather than to the 1-4 DEG tail of expressed SLC donors.

I used only the declared biology bundle, training count table, and training Parquet-derived profiles. I did not use a Slc24a5 expression signature or Slc24a5 endpoint count.
