# Mapk8 DEG-count forecast

Target and endpoint:

- The declared one-row holdout manifest names `Mapk8`.
- The endpoint is the number of measured genes in `151 TH Prkcd Grin2c Glut` with BH-adjusted Wilcoxon `pvals_adj < 0.05`.
- I used the Mapk8 biology-only bundle for the held-out target itself. I used same-experiment count/profile measurements only for training perturbations, not for the held-out Mapk8 profile.

Mapk8 biology bundle:

- Exact focal-population expression reach supports the possibility of observing an edit: Mapk8 was detected in 18,740 of 23,679 matched non-target nuclei in `151 TH Prkcd Grin2c Glut`, or 79.14185565268804%, with mean CP10K 1.1758438327600353.
- The functional-stock card classifies MAPK8/JNK1 as a soluble catalytic kinase whose new supply should stop after a disruptive P16 edit; across the 21-28 days to P37-P44 harvest, the stock is expected to be `likely_substantially_depleted`.
- The same card leaves important uncertainty: no Mapk8-specific mature neuronal half-life or residual-activity threshold was available, and Mapk9/Mapk10 paralogs can buffer JNK-family operations.
- The positive external phenotype in the card is adult hippocampal spine and learning biology after constitutive Mapk8 loss, not an acute P16 thalamic basal-snRNA phenotype. I therefore treated it as evidence that Mapk8 can matter in neurons, but not as evidence for a large focal thalamic DEG burden.

Training-count anchors in the exact focal class:

- The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` table contains 1,674 training targets and excludes `Mapk8`.
- Its DEG-count distribution is zero-heavy: 1,205/1,674 targets have `n_degs = 0`; the median is 0, the 75th percentile is 1, and the 90th percentile is 2.
- Directly queried MAPK/JNK/AP-1/p38-adjacent training perturbations were almost all silent in `151 TH Prkcd Grin2c Glut`:
  - close or pathway kinases: `Mapk9 = 0`, `Mapk1 = 0`, `Map2k2 = 0`, `Map2k6 = 0`, `Map3k7 = 0`, and `Map2k1 = 4`;
  - AP-1 or related transcriptional nodes: `Jund = 0`, `Fosl2 = 0`, `Atf6 = 0`;
  - p38/MEF2-linked comparators: `Mef2d = 0`, `Mef2c = 1`.
- ERK-pathway neighbors named in the Map2k1 corpus report also stayed very small in this focal count table: `Braf = 4`, `Shoc2 = 1`, `Ptpn11 = 0`, `Raf1 = 0`, `Hras = 0`, `Kras = 0`, `Rasa2 = 0`, `Sos1 = 0`, and `Lztr1 = 1`.
- Broader stress/NF-kB/TGF-beta neighbors named around `Map2k6` and `Map3k7` were likewise null or singletons in this class: `Taok1 = 0`, `Tlr7 = 0`, `Chuk = 0`, `Nfkb1 = 0`, `Rel = 0`, `Acvr1 = 0`, `Bmpr1a = 0`, `Tgfbr1 = 0`, `Tgfbr2 = 0`, `Smad1 = 0`, `Smad2 = 1`, `Smad3 = 0`, and `Smad4 = 0`.

Profile checks from the declared Parquet:

- I recomputed the exact 151-class Parquet profiles for the selected cohort `Mapk9, Mapk1, Map2k1, Map2k2, Map2k6, Map3k7, Jund, Fosl2, Mef2c, Mef2d`. Each had 17,259 measured rows in the focal class.
- The exact FDR<0.05 counts in those Parquet rows matched the count table: eight of the ten nodes had zero significant genes, `Mef2c` had one, and `Map2k1` had four.
- The only significant `Map2k1` genes were the small all-down ERK-linked module `Vgf`, `Ptpn5`, `Etv5`, and `Unc13a`; the only significant `Mef2c` gene was `Mef2c` itself. Those do not look like a reusable basal JNK/AP-1 module.
- Whole-profile similarities across the cohort were weak. Pairwise cosines in the inspected kinase/AP-1/p38 cohort were near zero, with the largest cross-family values around 0.09, and no pair shared a significant FDR<0.05 feature. Thus the low counts were not hiding a coherent subthreshold JNK-like expression state.

Packaged same-experiment interpretation of the training anchors:

- The released training reports call `Mapk9` FDR-silent in every recovered neuronal class, including absence of canonical AP-1/immediate-early, apoptosis, and FoxO/autophagy transcripts.
- They interpret `Map2k6` and `Map3k7` as basal postmitotic-neuron nulls for stress-coupled p38/JNK/NF-kB axes rather than broad failures of the expected stress modules.
- They describe `Jund` and `Fosl2` as buffered AP-1/bZIP losses in unchallenged juvenile postmitotic neurons.
- They describe `Mapk1` as an ERK2-only null despite sparse upstream `Map2k1`/`Braf` activity in the same focal class, consistent with single-kinase or single-paralog buffering.

Synthesis:

Mapk8 is reachable and probably functionally depleted enough that a nonzero self-transcript or very sparse downstream call is plausible. The dominant quantitative evidence, however, is that isolated kinase and AP-1 perturbations sitting closest to JNK signaling are null or nearly null in this exact basal thalamic snRNA context. The closest assayed paralog, `Mapk9`, is exactly zero in the focal class and reported to be silent brain-wide; the represented upstream stress-JNK/p38/NF-kB and AP-1 nodes are also zero; and the only nearby MAPK responses top out at 1-4 genes through an ERK-specific Vgf/Ptpn5/Etv5/Unc13a module that I did not transfer to JNK1.

I therefore forecast Mapk8 as another buffered, cue-gated single-JNK perturbation in recovered `151 TH Prkcd Grin2c Glut` nuclei, with the point estimate at the modal and median training value:

`predicted_n_degs = 0`
