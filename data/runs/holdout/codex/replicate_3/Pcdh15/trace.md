# Pcdh15 DEG-count forecast

Target and context:

- Target: `Pcdh15`
- Cell group: `151 TH Prkcd Grin2c Glut`
- Forecasted endpoint: number of measured genes with Wilcoxon BH-adjusted `p < 0.05`
- Point prediction: `0`

Evidence used:

- The run manifest names only `Pcdh15` as the holdout target for this forecast.
- The biology-only bundle for `Pcdh15` reports exact in-assay expression in the focal class: the feature is available, 10,132 of 23,679 non-target nuclei express the gene, `pct_cells_expressing = 42.78896912876388`, `mean_cp10k = 0.48773200157436514`, and `mean_log1p_cp10k = 0.301135787568729`. This makes Pcdh15 observable in the assayed class, but the bundle explicitly does not treat target transcript abundance as editing efficiency or a downstream effect size.
- The same bundle adjudicates functional stock by harvest as `indeterminate`: editing should stop new PCDH15 supply, but existing membrane or complex-associated PCDH15 is not directly removed by the edit, and the relevant thalamic neuronal pool and clearance rate are not measured.
- In the declared 151-class training count table, 1,205 of 1,674 training targets have `n_degs = 0`; the median is 0, the 75th percentile is 1, and only 132 training targets reach at least 5 DEGs. Large responses in this class are concentrated in RNA-processing, proteasome, chromatin, and broad regulatory perturbations rather than cell-adhesion perturbations.
- I used the training count table to select a biologically close adhesion/synapse membrane set present in the declared training universe: `Celsr2`, `Cntnap1`, `Cntnap2`, `Dscam`, `Lrrtm1`, `Lrrtm3`, `Lrrtm4`, `Nlgn3`, `Nrxn1`, `Nrxn2`, `Nrxn3`, and `Pcdh19`. Their 151-class counts were six total DEGs across 12 targets, with no target above 1 DEG; the only protocadherin-family member in this table, `Pcdh19`, had 0.
- I inspected the declared differential-expression Parquet for those 12 selected training perturbations in `151 TH Prkcd Grin2c Glut`. The six one-DEG cases were isolated calls: five were the perturbed transcript itself (`Celsr2`, `Cntnap1`, `Cntnap2`, `Nlgn3`, `Nrxn1`), and the only non-self isolated call was `R3hdm2` after `Lrrtm1` perturbation. `Dscam`, `Lrrtm3`, `Lrrtm4`, `Nrxn2`, `Nrxn3`, and `Pcdh19` had no BH<0.05 genes.

Reasoning:

Pcdh15 has enough baseline expression in the focal thalamic class that a direct target-transcript change could in principle be counted, so I did not treat the target as unexpressed or uneditable. The endpoint, however, counts significant DE genes rather than presence of a transcript, and the local training data put the closest membrane adhesion and synaptic organizing perturbations in the 0 to 1 range. The Parquet rows show that even their one-count outcomes usually come from the self transcript, not from a reproducible downstream thalamic response program.

The Pcdh15 biology bundle points in the same low-burden direction. PCDH15 is a membrane cadherin with an established installed-complex role in sensory hair cells and some adult-brain relevance, but existing protein pools may persist after a P16 edit and no thalamic-neuron turnover clock is known. That makes a broad postmitotic survivor-state signature by P37-P44 biologically possible but weakly supported. I therefore put the forecast at the lower side of the 0-or-1 adhesion-family regime rather than assigning a self-transcript-only count.
