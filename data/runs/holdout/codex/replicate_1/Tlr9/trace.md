# Direct DEG-count forecast for Tlr9

## Task and endpoint

- Target from the declared one-row holdout manifest: `Tlr9`.
- Cell class: `151 TH Prkcd Grin2c Glut`.
- Endpoint: `n_degs`, the number of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05` in the held-out `Tlr9` perturbation profile.

## Evidence used

1. Exact focal-population reach from the declared biology bundle:
   - `Tlr9` was detected in 35 of 23,679 non-target nuclei from `151 TH Prkcd Grin2c Glut`.
   - `pct_cells_expressing = 0.147810296%`.
   - `mean_raw_umi = 0.001478103`, `mean_cp10k = 0.001019532`, and `pseudobulk_cpm = 0.092637954`.
   - The target is therefore technically measurable but essentially absent in the focal thalamic glutamatergic population.

2. Biology-prior interpretation from the same canonical `Tlr9` bundle:
   - TLR9 is a trafficked, proteolytically processed endolysosomal CpG-DNA receptor.
   - The curated stock adjudication judged 21-28 days after P16 editing likely sufficient for substantial functional depletion.
   - Direct postnatal neuronal evidence exists in adult hippocampal CA1 neurons, but the timing and region are not matched to juvenile thalamic neurons.
   - This supports the possibility of a neuronal TLR9 phenotype in a receptive population, but it does not overcome the exact near-zero thalamic RNA reach.

3. Training DEG-count distribution in the declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`:
   - `Tlr9` was absent from the 1,674 visible training targets, as required for the holdout.
   - Median `n_degs` was 0.
   - 1,205/1,674 targets, or 71.98%, had 0 DEGs.
   - 1,481/1,674 targets, or 88.47%, had at most 1 DEG.
   - 1,546/1,674 targets, or 92.35%, had at most 5 DEGs.

4. Same-family and nearby innate/endolysosomal comparators selected from the visible training table:
   - Toll-like receptor perturbations in this cell class were uniformly silent: `Tlr2 = 0`, `Tlr3 = 0`, `Tlr4 = 0`, `Tlr5 = 0`, `Tlr7 = 0`, `Tlr8 = 0`.
   - The closest declared paralog in the `Tlr9` biology bundle, `Tlr7`, was among these 0-DEG profiles.
   - Additional visible innate/endolysosomal comparators checked as directional controls were also silent: `Traf3 = 0`, `Nfkb1 = 0`, `Atg5 = 0`, `Atg16l1 = 0`.

5. Matched Parquet profile check:
   - In the exact `151 TH Prkcd Grin2c Glut` slice of `training_de_all_cell_groups.parquet`, each checked comparator had zero rows with `pvals_adj < 0.05`.
   - Minimum adjusted p-values were 1.0 for `Tlr2`, `Tlr3`, `Tlr4`, `Tlr5`, `Tlr7`, `Tlr8`, `Traf3`, `Nfkb1`, and `Atg16l1`; `Atg5` had one near-leading but nonsignificant row with minimum `pvals_adj = 0.104666435`.
   - The zero DEG counts for the visible TLR/innate comparators therefore did not hide a broad near-threshold program after BH correction.

## Synthesis

The biology bundle argues that a disruptive `Tlr9` edit can deplete the receptor by harvest and that neuronal TLR9 biology is real in at least adult hippocampus. For the requested thalamic endpoint, however, the exact in-assay expression reach is the dominant constraint: only 0.148% of matched non-target nuclei contained any `Tlr9` transcript, with just 35 total target UMIs across the whole focal non-target population. A perturbation whose functional substrate is present in such a tiny fraction of assayed thalamic nuclei is unlikely to create a Wilcoxon-detectable survivor-state expression shift across many measured genes.

The quantitative training context points the same way. The endpoint is zero-inflated even before applying biology, and every visible Toll-like receptor family perturbation was a 0-DEG thalamic profile. `Tlr7`, the closest bundle-named paralog and also an endosomal nucleic-acid receptor, was flat in both the count table and the matched Parquet rows. I therefore treated `Tlr9` as more likely to land in the large silent/near-silent mass than in the small high-response tail.

Point forecast:

```tsv
target_name	predicted_n_degs
Tlr9	0
```
