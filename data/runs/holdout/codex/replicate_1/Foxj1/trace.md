# Direct n_degs forecast: Foxj1 in 151 TH Prkcd Grin2c Glut

## Evidence used

- Target: the one-row holdout manifest declares `Foxj1`.
- Biology bundle: `[local file: Foxj1.json]`, checksum `e11d6b9cf5bafa7fc21996189be1f28f431da5b8b1047e6deeadf7e413c3cfff`, biology-only view.
- Count endpoint: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Profile endpoint rows: `[local file: training_de_all_cell_groups.parquet]`, filtered to `group_name == "151 TH Prkcd Grin2c Glut"`.

## Determining observations

- The Foxj1 card calls the perturbation molecularly realizable in an expressing postmitotic cell: Foxj1 is a rapidly turned-over transcription factor, and loss in mature postnatal ependymal cells destabilized the Foxj1-dependent multiciliated state within the 21-28 day assay interval.
- That realized biology is mainly outside this endpoint's cell pool. The card places Foxj1 function in ventricular ependymal and other motile-ciliated cells rather than broadly in NeuN-positive thalamic neurons.
- The exact focal-population expression measurement is very low: in matched non-target `151 TH Prkcd Grin2c Glut` nuclei, Foxj1 had 780 total UMIs among 23,679 nuclei, 718 expressing nuclei, 3.032% expressing cells, mean raw UMI 0.03294, mean CP10K 0.02090, and pseudobulk CPM 2.0645. Because the perturbation contrast aggregates the whole thalamic neuronal class, a response restricted to this rare Foxj1-positive fraction would be highly diluted.
- The declared training count table is strongly sparse in this class: 1,205 of 1,674 training perturbations, or 71.98%, have `n_degs = 0`; the median is 0 and the 75th percentile is 1.
- Available nearby biology in the training endpoint did not reveal a broad cilia-program signal in these thalamic neurons. The count table gives `n_degs = 0` for `Foxj3`, `Rfx3`, `Rfx7`, `Trp73`, and `Ift88`. In the expression Parquet, each of those profiles had 17,259 measured focal-class gene rows and no BH-adjusted Wilcoxon `p < 0.05`.

## Synthesis

Foxj1 loss should clear functional target stock in cells that actually depend on Foxj1, but the exact atlas expression measurement makes that dependent population a small minority of the recovered `151 TH Prkcd Grin2c Glut` nuclei. The thalamic neuronal assay therefore mismatches the known ependymal Foxj1 biology, and the class-specific training data show that both the generic prior and the available cilia/Forkhead/RFX perturbations are concentrated at zero DEGs. I therefore forecast no FDR-significant downstream genes in the held-out Foxj1 contrast.

Prediction: `n_degs = 0`
