# Hes7 n_degs forecast

## Target and endpoint

The declared one-row holdout manifest names `Hes7`. The requested endpoint is
the count of measured genes in `151 TH Prkcd Grin2c Glut` with
BH-adjusted Wilcoxon `pvals_adj < 0.05`.

## Evidence used

- The target biology bundle reports exact non-target expression reach for
  `Hes7` in the focal population: 102 of 23,679 nuclei had any `Hes7` UMI
  signal, for 0.430761% expressing cells; the total was 106 target UMIs among
  377,814,907 total UMIs, mean raw UMI was 0.0044765, mean CP10k was
  0.0026942, and pseudobulk CPM was 0.28056.
- The same bundle assigns the HES7 functional stock as likely depleted by the
  P37-P44 harvest if a cell is successfully edited and expressing the target:
  HES7 is a free, short-lived nuclear bHLH transcriptional repressor with a
  measured mouse half-life of roughly 22 minutes in the segmentation-clock
  system. This supports lesion realization only in the small subset of cells
  that actually make functional HES7.
- The source card places established HES7 biology in embryonic presomitic
  mesoderm/somitogenesis, not in postmitotic postnatal thalamic neurons, and
  found no direct P16-P44 thalamic-neuron loss evidence.
- The declared `151 TH Prkcd Grin2c Glut` training count table is heavily
  concentrated at zero: 1,205 of 1,674 training targets had `n_degs = 0`;
  the median was 0, the 75th percentile was 1, and the 90th percentile was 2.
- I used the focal-population Parquet to inspect visible developmental or
  Notch/segmentation-neighbor perturbations that are poor matches to
  postnatal thalamic function. `Atoh1`, `Dll1`, `Gli1`, `Gli2`, `Hesx1`,
  `Neurod1`, `Notch1`, `Notch2`, `Notch4`, and `Pax6` each had 0 genes with
  `pvals_adj < 0.05` in `151`; `Mesp2` had 1. The minimum adjusted p-values
  for the zeros were also not borderline for most of that set:
  `Atoh1`, `Gli1`, `Gli2`, `Hesx1`, `Neurod1`, `Notch1`, `Notch2`, and `Pax6`
  had minimum adjusted p-value 1.0, while `Dll1` and `Notch4` had minima
  0.67756 and 0.49020.

## Synthesis

The decisive feature is focal-population reach. HES7 would be an acute
functional knockout where it is actively produced, because pre-edit protein
cannot last for the 21-28-day edit-to-harvest window, but the assayed thalamic
neurons barely transcribe `Hes7` and there is no evidence for a postnatal
thalamic HES7 circuit. A perturbation present in less than 0.5% of non-target
focal nuclei is unlikely to generate a recovered-population Wilcoxon signature
unless it couples to a broad cell-state change, and the relevant developmental
Notch/segmentation training perturbations overwhelmingly sit at the zero floor
in this same cell class.

I therefore predicted the mode of the local null distribution rather than a
one-off marginal DEG:

`predicted_n_degs = 0`
