# Direct n_degs forecast for Zfp799

## Target and endpoint

- Target manifest gene: `Zfp799`.
- Requested context: `151 TH Prkcd Grin2c Glut`.
- Endpoint: integer count of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05` in the held-out target profile.

The held-out `Zfp799` differential-expression signature and its DEG count were not used. Evidence came from the declared one-row manifest, the training `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`, the declared training Parquet filtered to the same cell group for visible training perturbations, the canonical `Zfp799` biology bundle, and same-experiment corpus summaries for measured training exceptions.

## Training-count scale

The `151 TH Prkcd Grin2c Glut` training count table contains 1,674 visible training targets. It is dominated by null or near-null responses:

- 1,205 / 1,674 targets have `n_degs = 0`.
- 469 / 1,674 have any DEG.
- The median is 0, the 75th percentile is 1, the 90th percentile is 2, the 95th percentile is 18, and the 99th percentile is 430.
- The arithmetic mean is 14.05, but this is tail-driven; only 43 / 1,674 targets have at least 100 DEGs.

Within the visible `Zfp`-numbered training perturbations, 20 / 25 are exactly zero in the count table and in a direct re-count of `pvals_adj < 0.05` rows from the declared Parquet restricted to `151 TH Prkcd Grin2c Glut`. The nonzero entries are sparse except for `Zfp423`:

| training group | n_degs in 151 |
|---|---:|
| `Zfp1`, `Zfp106`, `Zfp160`, `Zfp182`, `Zfp266`, `Zfp292`, `Zfp341`, `Zfp397`, `Zfp451`, `Zfp462`, `Zfp521`, `Zfp536`, `Zfp609`, `Zfp644`, `Zfp654`, `Zfp664`, `Zfp846`, `Zfp949`, `Zfp950`, `Zfp961` | 0 |
| `Zfp612`, `Zfp692` | 1 |
| `Zfp148` | 8 |
| `Zfp236` | 19 |
| `Zfp423` | 150 |

The same-experiment reports make the largest `Zfp`/BTB outliers look target-specific rather than a generic rule for zinc-finger genes: `Zfp423` had a distinctive thalamic/cerebellar response and did not phenocopy its close paralog `Zfp521`; `Zfp148` had a small, sharply thalamic signature; and `Zbtb7a` was a broad neuronal transcription-factor perturbation tied to a recurrent trafficking/proteostasis state. Those measured exceptions are therefore weak quantitative donors for a sparsely annotated KRAB/C2H2 factor.

## Zfp799 biology

The canonical biology bundle says:

- `Zfp799` encodes a predicted nuclear KRAB/C2H2 zinc-finger transcription regulator.
- In non-target `151 TH Prkcd Grin2c Glut` nuclei, the target transcript is measurable in 19,788 / 23,679 cells, with 83.57% expressing, mean raw UMI 2.13, mean CP10k 1.37, and pseudobulk CPM 133.62. Context reach is therefore not the limiting concern.
- Functional stock is expected to be at least directionally affected by P16 editing before the P37-P44 harvest: editing stops new protein supply, and a soluble nuclear regulator should undergo renewal over 21-28 days.
- The target-specific biology is otherwise sparse. No direct acute postnatal thalamic loss experiment, ZFP799-specific protein half-life, postnatal neural phenotype, or tested compensating paralog was found.

That evidence supports possible target engagement, but it does not supply a positive thalamic response program comparable to the large `Zfp423` or `Zbtb7a` training signatures.

## Numeric synthesis

I treated broad expression and plausible stock depletion as enough to avoid assuming assay failure, but not enough to overcome the null-heavy empirical prior. The closest simple training stratum, visible `Zfp`-numbered perturbations in the same focal cell group, has an 80% zero rate and a median of 0. The nonzero tail is concentrated in better-established developmental or regulatory factors with explicit same-experiment programs, whereas `Zfp799` has only official annotation and bounded-unknown phenotype/redundancy evidence.

The most likely integer is therefore a null FDR count. I assign:

`Zfp799 -> predicted_n_degs = 0`
