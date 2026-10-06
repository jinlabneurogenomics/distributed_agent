# Pafah1b1 n_degs forecast

## Target and endpoint

- Target: `Pafah1b1`, the one row in the declared holdout manifest.
- Focal population: `151 TH Prkcd Grin2c Glut`.
- Endpoint: `n_degs`, the number of measured genes with Wilcoxon `pvals_adj < 0.05` in the matched focal-population perturbation contrast.

## Evidence used

- The declared characterization bundle for `Pafah1b1` is biology-only and endpoint-excluded. It reports exact in-assay target reach in `151 TH Prkcd Grin2c Glut`: `Pafah1b1` was detected in 20,713 of 23,679 non-target nuclei, 87.474% of cells, with mean raw UMI 2.714 and mean log1p CP10k 0.876. This made failed focal expression an unlikely explanation for a null but did not quantify editing efficiency or the held-out response.
- The same bundle places LIS1/Pafah1b1 in two functional pools: cytoplasmic-dynein regulation and the cytosolic PAF-AH(I) complex. It judges the operative stock at P37-P44 as indeterminate because a P16 DNA edit stops new synthesis but does not acutely remove pre-existing LIS1 molecules and no endogenous mouse postmitotic-neuron LIS1 half-life was identified.
- The selected same-experiment corpus release had no `Pafah1b1` report, Finding, Claim, or explicit target relation, so it did not provide report-level Pafah1b1 outcome evidence or comparators.
- I nominated training-available biological analogs from the explicit 1,674-gene training universe using curated annotations and selected-release graph context. The biologically specific, non-broad tranche contained 18 genes. Their `151 TH Prkcd Grin2c Glut` training counts were:

  `Lrp8` 0, `Reln` 0, `Dctn1` 75, `Tuba1a` 7, `Tubb4b` 1, `Ywhae` 0, `Kif5a` 1, `Tuba4a` 2, `Kif5c` 1, `Kif3b` 0, `Klc1` 1, `Klc2` 1, `Rab3gap1` 0, `Rab3gap2` 0, `Rab18` 0, `Pld3` 1, `Selenoi` 5, `Agps` 1.

- Those 18 specific analogs had a median of 1 DEG and an arithmetic mean of 5.33 DEGs. Seven were completely quiet, ten had 1-9 significant genes, and only `Dctn1`, the closest measured dynein/dynactin analog, had a moderate response at 75 DEGs.
- A symmetric profile comparison over those same 18 analogs in `151 TH Prkcd Grin2c Glut` found no coherent high-count subcluster: the response-activity strata were 7 `no_significant_features`, 10 `1_to_9_significant_features`, and 1 `at_least_50_significant_features`.
- The full training count table is zero-inflated in this cell class: 1,205 of 1,674 targets are zero, the median is 0, the 90th percentile is 2, the 95th percentile is 18, and the largest values come from a long tail.

## Synthesis

High focal expression and an ongoing LIS1 dynein-regulatory role argue against treating `Pafah1b1` as a pure expression-missed null. However, the direct focal analog evidence is mostly much quieter than `Dctn1`: the LIS1/Reelin, KIF/KLC, tubulin, and Golgi-to-ER analogs are concentrated at 0-7 DEGs, and the biology card leaves residual LIS1 protein/function at 21-28 days unresolved. I therefore placed `Pafah1b1` above the 1-DEG center of its most specific measured analogs but far below the single `Dctn1` outlier.

Point forecast: `8` DEGs.
