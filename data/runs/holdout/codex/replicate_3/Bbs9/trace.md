# Bbs9 `n_degs` forecast for `151 TH Prkcd Grin2c Glut`

## Evidence used

- The declared holdout manifest names one target, `Bbs9`.
- The endpoint is the count of measured genes in `151 TH Prkcd Grin2c Glut` with Wilcoxon BH-adjusted `p < 0.05` in the declared PerturbAI atlas training surface.
- In the `Bbs9` biology bundle, the exact in-assay non-target expression reach for the requested class is:
  - mean CP10K: `0.2813`
  - mean raw UMI: `0.4284`
  - pseudobulk CPM: `26.8518`
  - expressing nuclei: `7,699 / 23,679 = 32.51%`
  This establishes that `Bbs9` is measurable in the focal population, but it is still a low-abundance, minority-cell transcript.
- The same bundle adjudicates BBS9 as a renewable BBSome cargo-adaptor subunit whose functional stock is likely substantially depleted by the P37-P44 harvest after a P16 edit. The counterweights are that no target-specific BBS9 degradation clock or acute postnatal mouse thalamic loss phenotype was found, and the best disease evidence is congenital human Bardet-Biedl syndrome rather than a matched 21-28 day neuronal transcriptional endpoint.
- The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` table is zero-heavy: `1,205 / 1,674` training perturbations have `n_degs = 0`, the median is `0`, the 75th percentile is `1`, and only `469 / 1,674` are nonzero.
- The BBSome/ciliary training perturbations represented in the same count table are nearly all null in the requested class:
  - `Bbs5 = 0`
  - `Ttc8 = 1`
  - `Cep290 = 0`
  - `Ift43 = 0`
  - `Ift81 = 0`
  - `Ift88 = 0`
  - `Cep112 = 0`
  - `Cep120 = 0`
  - `Cep85l = 0`
- Direct aggregation of the declared all-cell-group parquet gave the same near-null pattern outside this class. Across all measured neuronal classes for that ciliary cohort:
  - `Bbs5` had one FDR-significant row, in `046 CTX-CGE GABA`.
  - `Ttc8` had one FDR-significant row, in `151 TH Prkcd Grin2c Glut`.
  - `Ift88` had one FDR-significant row, in `155 MB Glut`.
  - `Cep112`, `Cep120`, `Cep290`, `Cep85l`, `Ift43`, and `Ift81` had zero FDR-significant rows.
- The single `Ttc8` significant row in the requested class was `Ttc8` itself (`logfoldchange = -0.6631`, `p_adj = 3.07e-05`), so the closest available BBSome target had zero significant downstream genes.
- A matched profile comparison over `Bbs5`, `Ttc8`, `Cep290`, `Ift88`, `Ift43`, `Ift81`, `Cep112`, `Cep120`, and `Cep85l` in `151 TH Prkcd Grin2c Glut` found eight no-significant-feature profiles and one 1-to-9-feature profile. Whole-profile Pearson/cosine similarities within the inspected ciliary cohort were positive and moderate, while significant-gene intersections were zero because the profiles were FDR-null or self-only.
- Same-experiment corpus reports for `Bbs5`, `Ttc8`, `Ift43`, `Ift81`, `Ift88`, and `Cep290` summarize the ciliary/BBSome/IFT axis as flat, singleton-only, or orthogonal in basal postnatal neuronal nuclear RNA, with the likely effects displaced to ciliary morphology, cargo localization, evoked signaling, photoreceptor/olfactory biology, or other off-assay physiology rather than to a shared snRNA-seq program.
- I separately checked self-transcript behavior in the requested class because total `n_degs` can include the perturbed transcript. Among 1,642 training targets with a self row in `151 TH Prkcd Grin2c Glut`, `319` were self-significant at `p_adj < 0.05` (`19.4%`). Within the nine ciliary rows above, only `Ttc8` had a significant self row; `Bbs5`, `Cep112`, `Cep120`, `Cep290`, `Cep85l`, `Ift43`, `Ift81`, and `Ift88` had adjusted self p-values of `1.0` in this class.

## Forecast

`Bbs9` is a bona fide BBSome component and is detectably expressed in the focal thalamic class, so the guide should often make a molecular lesion by the harvest window. The matched training evidence nevertheless argues that this lesion is usually not visible as a basal postnatal neuronal nuclear-RNA response: the available BBSome/IFT/centrosomal ciliary comparators are almost all total-count null in `151 TH Prkcd Grin2c Glut`, remain singleton or null across the rest of the atlas, and the most direct BBSome comparator, `Ttc8`, contributes only its own self transcript.

The only plausible upward adjustment is a `Bbs9` self-transcript hit. I did not treat measured self-RNA loss as functional engagement, but for this endpoint it could add one counted gene. The training self-hit background in the focal class is only about one in five, and the ciliary analogs show one self-only singleton among nine matched targets despite several nominal negative self log-fold changes. That leaves the point expectation below one DEG.

Predicted `n_degs`: `0`
