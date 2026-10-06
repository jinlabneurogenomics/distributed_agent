# Tbk1 DEG-count forecast

## Target and endpoint

- Target: `Tbk1`
- Focal population: `151 TH Prkcd Grin2c Glut`
- Endpoint: `n_degs`, the count of measured genes with BH-adjusted Wilcoxon `p < 0.05`
- Prediction: 1

## Evidence used

The declared biology bundle reports exact in-assay focal expression for `Tbk1` in matched non-target cells: the feature is available, `Tbk1` is detected in 19,805 of 23,679 non-target nuclei, or 83.64%, with mean raw UMI 2.50, mean CP10k 1.53, and mean log1p(CP10k) 0.814. This supports good thalamic reach for a disruptive edit, but expression was used only as target presence, not as a target-transcript knockdown surrogate.

The same bundle adjudicates TBK1 as a diffusible serine/threonine kinase whose functional stock should likely be substantially depleted by the P37-P44 harvest after a P16 edit. The supporting card is still partial: no TBK1-specific protein half-life in postmitotic neurons was found, postnatal mouse phenotypes come from motor-neuron or microglial deletion rather than this thalamic neuronal population, the closest reported in-vivo findings occurred months rather than 21-28 days after onset, and Ikbke-family buffering is unresolved in thalamic neurons.

The declared 151-class training count table contains 1,674 observed targets and does not contain `Tbk1`. Counts are extremely sparse: 1,205 of 1,674 targets have zero DEGs, the median is 0, the 75th percentile is 1, the 90th percentile is 2, and the 95th percentile is 18.

I used training perturbations in TBK1-adjacent innate-signaling, selective-autophagy, lysosomal, and autophagy-regulatory biology:

| Perturbation group | Training counts in `151 TH Prkcd Grin2c Glut` |
|---|---|
| TLR/NF-kB signaling | `Chuk` 0; `Map3k7` 0; `Nfkb1` 0; `Rel` 0; `Tlr3` 0; `Tlr4` 0; `Traf3` 0 |
| selective autophagy / lysosomal stress | `Atg5` 0; `Becn1` 0; `Grn` 1; `Rb1cc1` 4; `Sqstm1` 1; `Tmem106b` 1; `Vcp` 2 |
| nutrient/autophagy control | `Mtor` 2; `Prkaa2` 0; `Rptor` 0; `Tsc2` 86 |

The matched Parquet profile comparison over those 17 training nodes found 10 with no significant 151-class features, 6 with 1-9 significant features, and a single high-response outlier, `Tsc2`. A cohort diagnostic over the complete selected set also showed weak transcriptional recurrence rather than a common TBK1-like state: across all 136 target pairs, the median signed top-tail overlap coefficient was 0.02 for the positive tail and 0.04 for the negative tail, with mean significant-program overlap of 0 in both directions.

## Synthesis

The exact focal expression and likely loss of renewable kinase stock argue against treating `Tbk1` as an inaccessible perturbation. The endpoint-matched training data push the count sharply downward: direct NF-kB/TLR components are all silent, core autophagy/lysosomal perturbations are 0-4 DEGs, and the one larger mTOR-family count belongs to `Tsc2`, a broader growth-control perturbation whose profile was not recurrent across the selected TBK1-adjacent cohort. Because the biology supports some chance of a real recovered-neuron state but the matched analogues concentrate at zero or one, my point forecast is a very small nonzero response: 1 DEG.
