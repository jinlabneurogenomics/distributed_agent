# Cc2d1a direct n_degs forecast

Prediction target: `Cc2d1a` in `151 TH Prkcd Grin2c Glut`.

Endpoint: number of measured genes with BH-adjusted Wilcoxon `p < 0.05` in the
same focal class.

Evidence used:

- The one-row holdout manifest declares `Cc2d1a` as the only target.
- The canonical `Cc2d1a` biology bundle was endpoint-blind. It reports direct
  focal-population reach for `Cc2d1a` in non-target nuclei:
  12,152/23,679 nuclei expressing the feature, 51.3197% expressing,
  mean raw UMI 0.786, mean CP10k 49.283.
- The same bundle adjudicates functional CC2D1A stock as likely substantially
  depleted by the P37-P44 harvest. That rests mainly on CC2D1A acting as a
  dynamic scaffold/endosomal regulator, a direct CC2D1A-CHMP4B interaction, and
  adult CA1 AAV-Cre deletion that removed detectable CC2D1A protein and gave a
  neuronal phenotype after three weeks. The support is positive but in
  hippocampal/forebrain neurons rather than the exact assayed thalamic class.
- The `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` table contains 1,674
  training targets. Its focal-count distribution is extremely sparse: median 0,
  75th percentile 1, 90th percentile 2, 95th percentile 18, mean 14.05, and
  1,205/1,674 targets equal 0.
- Mechanistically adjacent measured perturbations in the focal count table were
  quiet: the direct ESCRT partner `Chmp4b` had 0 DEGs, `Dnm1` had 1, and `Cltc`
  had 3. A scan of the declared expression Parquet for those observed profiles
  recounted the same focal-significant-gene totals and showed that `Chmp4b` was
  essentially quiet across the assayed classes, while `Dnm1` and `Cltc` were
  sparse in `151 TH Prkcd Grin2c Glut`.

Synthesis:

`Cc2d1a` is genuinely expressed and the perturbation should have time to reduce
functional protein in successfully edited cells, so I did not treat it as an
unexpressed or unrealized knockout. But its best-matched measured biology is a
local endosomal/ESCRT scaffold class rather than a broad chromatin,
proteostasis, mitochondrial, or mTOR regulator, and the directly related
training perturbations sit at 0-3 DEGs in the requested thalamic population.
Given the focal training distribution's heavy zero inflation, I place the
forecast just above the direct `Chmp4b` null and at the center of the
`Chmp4b`/`Dnm1`/`Cltc` local evidence.

Predicted `n_degs`: 1
