# Hmgb1 n_degs forecast

Target and endpoint:

- Target: `Hmgb1`.
- Cell class: `151 TH Prkcd Grin2c Glut`.
- Endpoint: number of measured genes with Wilcoxon BH-adjusted `pvals_adj < 0.05`.

Evidence used:

- The one-row holdout manifest and the canonical biology bundle both resolve the
  held-out perturbation to `Hmgb1`; `Hmgb1` is absent from the supplied 1,674
  row training count table.
- The declared Hmgb1 biology bundle reports exact in-assay expression in the
  matched non-target 151 thalamic population: `n_non_target_cells = 23679`,
  `n_cells_expressing = 13307`, `pct_cells_expressing = 56.1975`,
  `mean_raw_umi = 0.9907`, and `mean_cp10k = 0.6315`. Thus Hmgb1 is reachable
  in this assayed population, but the readout is still sparse nuclear RNA.
- The same bundle adjudicates the 21 to 28 day CRISPR window as
  `partially_depleted_or_leading_edge`: editing stops new HMGB1 supply, but
  pre-existing nuclear/cytoplasmic pools can persist and direct mouse-brain
  evidence only pins down near-complete protein loss later, at 6 to 7 weeks.
  The Hmgb2 redundancy facet is unresolved in juvenile thalamic neurons.
- The 151-class training count table is mostly null: among 1,674 observed
  targets, 1,205 have `n_degs = 0`, the median is 0, the 90th percentile is 2,
  the 95th percentile is 18, and only 43 perturbations have at least 100 DEGs.
- Counts for hand-selected chromatin and chromatin-remodeling comparators in
  the same count table span null through large responses rather than forming a
  single mechanistic scale: `Sin3a=1433`, `Ctcf=270`, `Smarcc2=185`,
  `Chd4=100`, `Chd8=61`, `Arid2=56`, `Chd2=34`, `Arid1a=22`, `Mecp2=16`,
  `Arid1b=1`, `Smarca2=1`, `Smarcd1=1`, and `Chd7`, `Dnmt3a`, `Hdac5`,
  `Kat6a`, `Kat6b`, `Set`, `Smarca4`, and `Smarcc1` at 0.
- A direct Parquet pass over those same comparators in `151 TH Prkcd Grin2c
  Glut` recovered the same endpoint strata and showed balanced signed programs
  in the active ARID/CHD/SWI-SNF examples; e.g. `Arid1a` had 22 DEGs,
  `Arid2` 56, `Chd2` 34, `Chd4` 100, `Chd8` 61, and `Smarcc2` 185 at
  `pvals_adj < 0.05`.
- Same-experiment Finding summaries for the training comparators also mark
  strong heterogeneity within obvious chromatin families: Arid1b and several
  mSWI/SNF relatives did not broadly phenocopy Arid1a; Smarca4, Smarca2,
  Smarcc1, and Smarcd1 did not reproduce the Arid2/Smarcc2 thalamic response;
  and Chd4, Chd7, and Chd8 did not phenocopy Chd2 in matched responder groups.

Synthesis:

Hmgb1 is clearly expressed in the focal thalamic nuclei and is a plausible
postnatal neural perturbation, so I did not treat it like an unexpressed or
irrelevant target. At the same time, the stock prior argues for incomplete
functional loss by P37-P44, and the direct training analogs show that broad
chromatin annotations are compatible with exact nulls or self-only effects in
this assay. I therefore placed Hmgb1 just above the all-target 90th percentile
and well below the active ARID/CHD/SWI-SNF middle band.

Predicted `n_degs`: 3
