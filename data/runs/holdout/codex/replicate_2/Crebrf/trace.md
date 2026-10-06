# Crebrf DEG-count forecast

Endpoint: number of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`
for `Crebrf` in `151 TH Prkcd Grin2c Glut`.

## Evidence used

- The one-row holdout manifest names `Crebrf`.
- The declared `Crebrf` biology bundle places the perturbation in juvenile
  postmitotic thalamic NeuN-positive neurons, P16 edit to P37-P44 harvest. The
  exact in-assay focal expression reach is real but moderate:
  mean CP10K `0.867586`, mean raw UMI `1.351028`, and `16464/23679`
  non-target cells expressing `Crebrf` (`69.53%`). The functional-stock card
  calls CREBRF a soluble nuclear CREB3/glucocorticoid-associated
  transcriptional coregulator and adjudicates pre-edit stock as likely
  substantially depleted by harvest, but with no matched thalamic neuronal
  depletion time course and only partial observability evidence.
- The exact 151 training count table has 1,674 targets; 1,205 are zero,
  median `n_degs = 0`, 75th percentile `1`, 90th percentile `2`, 95th
  percentile `18`, and the mean is inflated to `14.05` by a long broad-response
  tail.
- Pathway-proximal training counts in the same 151 endpoint were low:
  `Creb1 = 10`, `Crebbp = 8`, `Hspa8 = 9`, `Hsf1 = 6`, `Hspa5 = 5`,
  `Sec63 = 11`, while `Atf6 = 0`, `Nfe2l1 = 0`, `Nfe2l2 = 0`, `Nr3c1 = 0`,
  and `Nr3c2 = 0`.
- Exact Parquet rows confirmed that the nonzero CREB/CBP and ER/chaperone
  comparators were small 151 programs rather than broad state changes:
  `Creb1` had 10 FDR<0.05 genes, led by `Crem` up and a short mostly-down
  ER/lipid/lysosomal set; `Crebbp` had 8; `Hspa5` had 5; `Sec63` had 11.
  `Atf6`, `Nfe2l2`, `Nr3c1`, `Nr3c2`, and `Nfe2l1` had no FDR<0.05 row in
  the same cell class.
- Same-experiment corpus Findings for the visible analogs reinforced the exact
  counts: basal `Creb1` and `Crebbp` loss are detectable but restricted in
  thalamic glutamatergic neurons and do not phenocopy one another broadly;
  basal `Atf6` and `Nfe2l2` loss are corrected-transcriptome nulls in neuronal
  groups despite the assay being able to recover ER-stress RNA after `Hspa5`;
  `Nr3c1`/`Nr3c2` and nearby steroid receptor perturbations are weak to silent
  without a ligand challenge.
- Treating `Crebrf` only as a measured downstream gene in the 151 training
  Parquet, its transcript reached FDR<0.05 after just three very broad
  high-burden perturbations, `Tpr`, `Tnpo3`, and `Uba5`. That shows `Crebrf`
  can move inside large global signatures but did not identify a narrow
  Crebrf-like comparator.

## Synthesis

The forecast is above a strict null because `Crebrf` is expressed in most
focal nuclei and a successful edit should deplete an unstable soluble nuclear
coregulator during the 21-28 day window. I discounted large thalamic programs
from proteasome, RNA-processing, and chromatin hits: they can move `Crebrf` as a
downstream readout, but CREBRF loss is not a direct perturbation of those core
machines.

The closest interpretable scale is the small basal nuclear-transcription
neighborhood. Direct `Creb1`/`Crebbp` perturbation produced only 8-10 exact
FDR<0.05 genes, and several stimulus/stress-regulated transcription factors
that looked at least as canonical on paper were zero in 151. CREBRF is less
central than CREB1 or CBP for basal neuronal transcription and lacks matched
evidence for a maintained thalamic requirement, so I placed it below those
small positive comparators but not all the way at the zero mode.

Predicted `n_degs`: `2`
