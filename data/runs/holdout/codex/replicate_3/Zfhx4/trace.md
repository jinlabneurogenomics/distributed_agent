# Zfhx4 n_degs forecast

Target and endpoint:

- Holdout manifest target: `Zfhx4`.
- Endpoint: number of measured genes in `151 TH Prkcd Grin2c Glut` with Wilcoxon `pvals_adj < 0.05`.
- The target report/claim lookup for `Zfhx4` in the selected same-experiment corpus returned no target record, Findings, Claims, or explicit references, so no same-experiment target outcome was exposed there.

Declared target biology:

- The exact in-assay reach card reports `Zfhx4` expression in the focal non-targeting cells: 13,397 of 23,679 cells expressing, 56.58% expressing, mean CP10K 0.708, and pseudobulk CPM 69.89.
- The perturbation should stop new ZFHX4 synthesis, and because ZFHX4 is a renewable nuclear DNA-binding transcription factor, its functional stock is likely substantially depleted by the P37-P44 harvest after a P16 edit.
- That realizability evidence is low-confidence for magnitude: no ZFHX4-specific protein half-life was available, and the closest mouse neural loss evidence is germline embryonic/neonatal brainstem respiratory-center development, not postnatal thalamic maintenance.
- `Zfhx3` is a close paralog but is not a tested postnatal thalamic compensator.

Training counts in the requested class:

- The declared count table contains 1,674 training targets.
- It is strongly zero-inflated: 1,205 / 1,674 targets have `n_degs = 0`; median is 0, 75th percentile is 1, 90th percentile is 2, and the mean of 14.05 is driven by rare large tails.
- Only 78 / 1,674 targets have more than 20 DEGs and 43 / 1,674 have at least 100 DEGs.

Comparator evidence:

- Annotation-based nomination against the exact training universe found no exact paralog/complex, narrow module, direct interaction, dependency, or bidirectional corpus-comparator candidate for `Zfhx4`; all 770 available nominees were broad functional fallbacks such as DNA-binding and RNA polymerase II transcription-factor annotations.
- The leading broad nominees were mostly transcriptionally silent in `151 TH Prkcd Grin2c Glut`: among the top 100 nominated training genes, 80 had zero DEGs. Leading nominees including `Zfhx2`, `Hivep1`, `Pparg`, `Ets1`, `Foxa2`, `Kdm5b`, and `Nfx1` all had `n_degs = 0`.
- `Zfhx2`, the most biologically interpretable available ZFHX-family comparator, had `n_degs = 0` in `151 TH Prkcd Grin2c Glut`. The same-experiment corpus described its central-neuron screen response as essentially sparse, with its only FDR<0.10 hit in a different 009 glutamatergic class.
- A symmetric measured-profile comparison of 20 transcription-factor/chromatin-like training profiles in the focal class confirmed that the `Zfhx2` profile had 17,259 measured features and no BH<0.05 features. Its correlations to high-burden TF outliers were tiny: in the inspected set the largest Zfhx2 pair was `Rora`, with Pearson 0.0706 and cosine 0.0644, and it had zero significant-feature intersections with `Rora`, `Zfp423`, `Zbtb7a`, `Sin3a`, `Yy1`, `Thap11`, and other broad TF comparators.

Synthesis:

The biology makes a realized perturbation plausible because `Zfhx4` is present in the focal thalamic population and encodes a renewable nuclear regulator. I still put most of the mass at zero: the direct postnatal thalamic demand is unproven, the closest neural phenotypes are developmental and in brainstem, no narrow training analogue exists, broad DNA-binding TFs in this class are mostly silent, and the same-family observed `Zfhx2` profile is a focal-class null rather than a scale donor for the rare large TF/chromatin signatures.

Prediction:

- `predicted_n_degs = 0`
