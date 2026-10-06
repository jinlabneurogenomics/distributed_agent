# Foxj1 forecast for `151 TH Prkcd Grin2c Glut`

## Declared target and focal population

- Target manifest: `Foxj1`.
- Requested focal population: `151 TH Prkcd Grin2c Glut`.
- Endpoint: number of measured focal-population genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`.
- The training Parquet has no `gene_target = 'Foxj1'` rows, so the held-out differential-expression surface was not consulted.

## Evidence used

1. The canonical `Foxj1` biology bundle supports rapid functional depletion after editing in cells that actually depend on Foxj1: Foxj1 is a short-lived nuclear transcription factor continuously maintaining the postnatal ependymal multiciliated state, and P14 inducible loss in mature mouse ependyma produced state loss by P28. This argues against a long-lived-protein explanation for a null.

2. The same bundle makes the assay reach very small. In the exact non-target focal population, Foxj1 was detected in only 718 of 23,679 nuclei:

   - `pct_cells_expressing = 3.0322226445373537`
   - `mean_raw_umi = 0.032940580260990754`
   - `mean_cp10k = 0.02090257146304476`
   - `pseudobulk_cpm = 2.064502976321154`

   The literature side of the bundle places the strong Foxj1 program in ventricular ependymal / multiciliated cells rather than broadly in NeuN-positive thalamic neurons. Thus most assayed focal nuclei are unlikely to contain a relevant Foxj1-dependent program for a P16 edit to perturb.

3. The declared focal training count table is zero-inflated:

   - 1,674 training targets
   - 1,205 with `n_degs = 0`
   - median `n_degs = 0`
   - 75th percentile `n_degs = 1`
   - 95th percentile `n_degs = 18`

   Low or off-lineage target reach should therefore be interpreted on the zero/singleton part of the distribution, not near the skewed mean of 14.054.

4. Ciliogenesis and ciliary-machinery comparators in the exact count table were nearly all null in this same focal population. The represented RFX/IFT/BBS/dynein/transition-zone set named by the same-experiment `Rfx3` and `Trp73` corpus Findings had:

   - `Trp73 = 0`
   - `Rfx3 = 0`
   - `Bbs5 = 0`
   - `Cep290 = 0`
   - `Cfap69 = 0`
   - `Cplane1 = 0`
   - `Cspp1 = 0`
   - `Dnal1 = 0`
   - `Dync2h1 = 0`
   - `Dync2i1 = 0`
   - `Ift43 = 0`
   - `Ift81 = 0`
   - `Ift88 = 0`
   - `Kif3b = 0`
   - `Lztfl1 = 0`
   - `Rpgrip1l = 0`
   - `Ttc21b = 0`
   - `Armc9 = 0`
   - `Arl3 = 1`
   - `Ttc8 = 1`

   Additional developmental transcription-factor checks were also quiet: `Atoh1 = 0`, `Zic2 = 0`, `Zic3 = 0`, `Zic4 = 0`, with only `Zic1 = 2`.

5. Re-querying the declared expression Parquet for those comparators confirmed the count-table values in `151 TH Prkcd Grin2c Glut`. Directly relevant anchors were completely flat at the endpoint:

   - `Trp73`: 17,259 measured rows, `n_degs = 0`, minimum focal `pvals_adj = 1.0`, 236 recovered perturbed nuclei versus 23,679 controls.
   - `Rfx3`: 17,259 measured rows, `n_degs = 0`, minimum focal `pvals_adj = 1.0`, 151 recovered perturbed nuclei versus 23,679 controls.

   The rare nonzero ciliary counts were isolated self-target effects rather than a Foxj1-like multiciliogenesis signature: `Arl3` had only self `Arl3` significant, and `Ttc8` had only self `Ttc8` significant.

6. A profile comparison over 25 selected ciliary / developmental comparators in the focal class found 22 targets with no significant features and only 3 with 1-9 significant features. Inspection of `Trp73` and `Rfx3` against direct ciliary peers showed no significant-feature intersections; their whole-profile cosines to inspected peers were near zero, with the largest observed `Trp73` pair at 0.0819608 and `Rfx3` pairs even smaller. This supported the count-level readout: the pathway is not forming a recurrent thalamic neuronal transcriptional module.

7. Same-experiment corpus context agreed with the measured training rows, while remaining only an interpreted view of the same experiment:

   - `Trp73:F003` reported that the p73-Foxj1 multiciliogenesis program was absent from Trp73-edited NeuN-positive brain nuclei.
   - `Trp73:F004` reported that `Rfx3` and other textbook p73 comparators were flat in assayed neuronal groups.
   - `Rfx3:F001`/`Rfx3:F002` reported no basal neuronal FDR response for `Rfx3` and absence of an expected RFX/ciliary target panel.
   - `Rfx3:F004` reported that represented RFX-family and ciliary effector comparators failed to reveal a shared acute neuronal ciliary signature.
   - The selected corpus release had no `Foxj1` Claims, Findings, or explicit references.

## Synthesis

Foxj1 is not predicted to be protected by persistent functional stock once edited, but in this endpoint the limiting factor is reach: only about 3% of the relevant non-target thalamic neuronal nuclei express Foxj1 at all, and the strong prior Foxj1 biology is in non-neuronal multiciliated/ependymal cells excluded or depleted by NeuN-positive sorting. In the focal training table, the closest p73/RFX/ciliary machinery perturbations were measured and were essentially all zero, with direct `Trp73` and `Rfx3` anchors having no FDR-significant focal genes and no coherent low-level profile similarity.

Those observations put Foxj1 on the off-lineage, low-reach side of a highly zero-inflated count distribution. I therefore forecast no BH-significant focal genes.

Predicted `n_degs`: **0**
