# Direct n_degs forecast for Nrl

## Target and declared endpoint

- Target: `Nrl`
- Endpoint: `n_degs` in `151 TH Prkcd Grin2c Glut`, the number of measured genes with BH-adjusted Wilcoxon `p < 0.05`.
- The declared focal training count table has 1,674 visible targets and does not contain `Nrl`.
- The declared focal Parquet aggregation reproduced those 1,674 count-table values exactly and had no `gene_target = 'Nrl'` rows, so the held-out Nrl differential-expression profile was not available in the training measurement table.

## Evidence used

1. Exact focal target reach was essentially absent. In non-target nuclei from `151 TH Prkcd Grin2c Glut`, the Nrl feature had:
   - `n_non_target_cells = 23679`
   - `n_cells_expressing = 4`
   - `pct_cells_expressing = 0.01689260526204654`
   - `total_target_umi = 4`
   - `pseudobulk_cpm = 0.010587194750364893`
   - `mean_raw_umi = 0.0001689260526204654`

2. The visible focal profiles were measured with 23 to 419 matched perturbation nuclei, with median `n_pert_matched = 177`. Applying the Nrl non-target expression fraction to that matched-cell scale gives roughly 0.03 Nrl-expressing cells at the visible median and only 0.07 at the visible maximum. Thus even a fully effective DNA edit would be expected to remove the assayed product from far less than one expressing thalamic nucleus per profile under baseline reach.

3. The biology bundle supports multi-week realization if the target product is supplied: the curated functional-stock call for the identifier-backed NRL/LCN2 product was `likely_substantially_depleted` by the P37-P44 harvest after a P16 edit. Its thalamic-context evidence was weak, however, and the bundle explicitly applied exact-reach supersession; the exact in-assay focal expression measurement is therefore the decisive context constraint.

4. The focal count table was highly zero-inflated: 1,205 of 1,674 visible targets had `n_degs = 0`; 363 had 1-9; 63 had 10-99; and 43 had at least 100. The median was 0, the 75th percentile was 1, and the 90th percentile was 2. A target expressed in only 4 of 23,679 matched-context non-target nuclei is much closer to the empirical null mass than to the sparse large-response tail.

5. Training-available analog nomination found no specific comparator. Nrl was absent from the training universe, and every nominated available candidate fell only in the `broad_functional_fallback` tier, with no exact paralog or complex member, reciprocal corpus comparator, narrow module member, or direct interaction/dependency candidate. The highest-priority broad fallbacks were themselves null or weak in the focal count table: `Mtor` 2, `Nfkb1` 0, `Park7` 1, `Becn1` 0, `Ahrr` 0, `Ntrk2` 3, `Adipor2` 0, `Tlr4` 0, `Trp53` 0, `Gsk3b` 6, `Crebbp` 8, and `Ep300` 0.

## Synthesis

The main upward prior is that realized loss of a short-lived secreted NRL/LCN2 product could matter biologically in a source-positive postnatal neural context. The focal Perturb-seq endpoint is an aggregate thalamic neuronal nuclear-RNA contrast, though, and the exact same-assay expression reach says this target was virtually absent from the assayed baseline population. With an expected fraction of a single Nrl-positive matched perturbed nucleus and no close measured analogue to justify a broad population state, a count above the BH threshold would require an implausibly large non-cell-autonomous or stress-induced effect.

I therefore place the forecast at the zero point mass of the visible training distribution.

Predicted `n_degs`: 0
