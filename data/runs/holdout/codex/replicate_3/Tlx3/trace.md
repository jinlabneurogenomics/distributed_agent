# Tlx3 n_degs forecast

## Prediction

`target_name = Tlx3`, predicted `n_degs = 0` in `151 TH Prkcd Grin2c Glut`.

## Evidence used

- **Declared target and endpoint.** The one-row manifest names `Tlx3`. The requested endpoint is the number of measured genes in `151 TH Prkcd Grin2c Glut` with BH-adjusted Wilcoxon `pvals_adj < 0.05` after the P16-to-P37/P44 postnatal mosaic CRISPR loss-of-function screen.
- **Target biology bundle.** The canonical `Tlx3` bundle is endpoint-blind and reports very weak exact reach in the focal assayed population: 44 of 23,679 non-target nuclei expressed `Tlx3` in `151 TH Prkcd Grin2c Glut`, i.e. 0.1858186579% of cells, with 44 total target UMIs, mean raw UMI 0.001858, mean log1p CP10k 0.000931, and pseudobulk CPM 0.116459. This exact in-assay measurement supersedes the discordant external adult-thalamus expression evidence for the purpose of reach.
- **Functional-stock prior.** The same bundle identifies TLX3 as a nuclear homeodomain transcription factor. A disruptive edit should halt new TLX3 synthesis but does not instantly erase pre-existing protein or an already specified transcriptional state; no quantitative TLX3 protein half-life, chromatin residence time, or post-P16 thalamic dependency clock was found. The strong mouse phenotypes in the source card are embryonic/perinatal spinal, brainstem, cerebellar, or DRG contexts, so they do not establish a mature thalamic response over 21-28 days.
- **Same-experiment corpus.** `Tlx3` has no selected-release target-context Findings, Claims, or explicit comparator references. Therefore the corpus supplied no direct `Tlx3` same-experiment response interpretation to transfer; absence of that target from the corpus is just missing packaged interpretation, not a measured null.
- **Focal training counts.** The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` has 1,674 training perturbations. The distribution is heavily zero-inflated: 1,205/1,674 targets have `n_degs = 0`, the median is 0, the 75th percentile is 1, and only 106/1,674 have at least 10 DEGs. Thus a low-reach target with no direct postnatal thalamic dependency evidence should default near zero unless a closer biology-matched comparator argues otherwise.
- **Biological analogs.** Deterministic typed analog nomination found no available exact-complex/paralog, no reciprocal same-experiment corpus comparator, no narrow module, and no direct-interaction nominee for `Tlx3`; all 1,258 available nominees were broad functional fallback annotations. Among the leading 20 broad developmental/neural transcriptional nominees, focal counts from the declared training table and Parquet were:

  `Phox2b=0, Pbx3=0, Mbd5=0, Mecp2=16, Foxa2=0, Ndn=1, Isl1=0, Nfix=0, Sox2=2, Ctnnb1=383, Pax6=0, Otx2=0, Tbx19=0, Sox9=0, Pax8=0, Notch1=0, Tbr1=0, Smad4=0, En1=0, Smad3=0`.

  A symmetric profile comparison over those 20 genes in the exact focal class found 16 with no significant features, 2 with 1-9, 1 with 10-49, and only the broad Wnt effector `Ctnnb1` with at least 50. The high `Ctnnb1` footprint is a broad signaling outlier rather than a close homeodomain/postnatal-thalamus analogue for `Tlx3`.

## Synthesis

The decisive signal is low functional reach. `Tlx3` is almost absent in the exact non-target focal nuclei, its strong literature phenotypes are developmental and outside thalamus, and the stock card leaves mature-neuron TLX3 persistence unresolved rather than supplying a reason for a large delayed response. Broadly related developmental TF perturbations in the same focal class are mostly silent even when they were assayed. I therefore place `Tlx3` at the zero mode of the training distribution rather than the outlier tail driven by broadly active regulators.
