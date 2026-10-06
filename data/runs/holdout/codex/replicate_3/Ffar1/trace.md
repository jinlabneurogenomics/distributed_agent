# Ffar1 forecast for `151 TH Prkcd Grin2c Glut`

## Target and endpoint

- Target: `Ffar1`, the single row in the declared holdout manifest
  `[local file: Ffar1.csv]`.
- Endpoint: `n_degs`, the number of measured genes in `151 TH Prkcd Grin2c Glut`
  with BH-adjusted Wilcoxon `pvals_adj < 0.05`.
- Point forecast: `0`.

## Evidence

1. **Exact focal-population target reach is zero.** The prediction-safe
   `Ffar1` biology bundle reports the requested cell group exactly:
   `n_non_target_cells = 23679`, `n_cells_expressing = 0`,
   `pct_cells_expressing = 0.0`, `total_target_umi = 0.0`,
   `mean_cp10k = 0.0`, and `pseudobulk_cpm = 0.0`. Its own precedence note
   says this exact in-assay expression supersedes qualitative context-reach
   estimates while not being used as an editing-efficiency readout.

2. **FFAR1 loss is plausible only where the receptor is present.** The same
   endpoint-blind bundle places FFAR1/GPR40 as a cell-surface fatty-acid GPCR.
   It judged that signaling-competent receptor stock would likely decline over
   the 21-28 day P16-to-P37/P44 editing window, but the neural functional
   evidence is hypothalamic or systemic, not thalamic. That makes expression
   reach the limiting factor for this aggregated thalamic glutamatergic
   population.

3. **The held-in thalamic count table is mostly null, and curated GPCRs are
   even quieter.** In
   `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`,
   `Ffar1` is absent as intended. Among all 1674 training targets, 1205 have
   `n_degs = 0`. Using the deterministic annotation store's
   `functional_class:gpcr` membership, 95 GPCR targets are in this training
   table; 85/95 have `n_degs = 0`, and the remaining 10 all have exactly
   `n_degs = 1`.

4. **The GPCR nonzero rows are not broad downstream programs.** I filtered the
   declared expression Parquet
   `[local file: training_de_all_cell_groups.parquet]`
   to `group_name = '151 TH Prkcd Grin2c Glut'`,
   curated training GPCR targets, and `pvals_adj < 0.05`. It returned only
   ten significant rows across the 95 held-in GPCRs. Nine were self-transcript
   decreases for `Adgrl1`, `Adgrl2`, `Adgrl3`, `Celsr2`, `Gabbr1`, `Gabbr2`,
   `Gpr158`, `Grm1`, and `Grm7`; the only non-self singleton was
   `Tm2d1 -> R3hdm2`.

## Synthesis

`Ffar1` has no same-ligand held-in perturbation: the Reactome free-fatty-acid
receptor set contributes only `Ffar1` among perturbed screen targets. The best
available quantitative analogue is therefore the wider GPCR class, and in the
exact requested thalamic class those receptors almost always produce no
significant downstream genes; when they are nonzero, the signal is usually only
their own expressed receptor transcript.

The exact `0/23679` baseline expression result is stronger than the broad GPCR
class prior. It argues that this thalamic population has no detectable FFAR1
transcript and therefore little or no FFAR1 protein stock for a P16 disruptive
edit to remove in recovered P37-P44 thalamic nuclei. It also removes the common
singleton path in the GPCR controls: with no focal-population `Ffar1` RNA, a
significant self-transcript decrease is not expected.

The residual uncertainty is that very rare expressing thalamic cells or
non-cell-autonomous effects could be below the baseline-expression measurement.
Those are outweighed by complete absence of focal expression, the off-thalamus
biology of known FFAR1 neural phenotypes, and the held-in receptor count
distribution. I therefore forecast no FDR-significant genes.
