# Cacna1c DEG-count forecast

Target: `Cacna1c`

Endpoint: `n_degs` in `151 TH Prkcd Grin2c Glut`, i.e. the count of measured genes with Wilcoxon BH-adjusted `pvals_adj < 0.05`.

## Evidence used

- The declared holdout manifest contains the single target `Cacna1c`.
- The exact Cacna1c biology bundle reports strong focal expression in the matched non-target population: 23,322 / 23,679 `151 TH Prkcd Grin2c Glut` nuclei express the feature, or 98.49%, with mean log1p(CP10K) = 1.565. This makes lack of substrate unlikely to be the main limiting factor.
- The same bundle adjudicates Cacna1c as the CaV1.2 pore-forming L-type calcium-channel alpha subunit and calls functional stock at harvest `likely_substantially_depleted`, but only with partial evidence because the kinetic anchor is non-neural and no exact juvenile-thalamic depletion curve was available.
- The full `151 TH Prkcd Grin2c Glut` training count table is highly zero-inflated: among 1,674 observed training perturbations, 1,205 have 0 DEGs, 1,481 have 0 or 1 DEG, the median is 0, and the long-tail mean is 14.05 because a small number of splicing/proteostasis/transcriptional regulators are very large.
- Close calcium-channel perturbations in the count table were small: pore-forming voltage-gated alpha1 genes were `Cacna1a` 0, `Cacna1d` 0, `Cacna1e` 0, and `Cacna1g` 12; auxiliary channel genes were `Cacna2d1` 1, `Cacna2d2` 0, `Cacnb2` 0, `Cacnb4` 1, `Cacng2` 0, and `Cacng3` 0.
- A direct Parquet aggregation over those same training targets showed that the nearest L-type and high-voltage calcium-channel perturbations were not merely missing focal signal while being strong elsewhere. `Cacna1a`, `Cacna1e`, `Cacna2d2`, `Cacnb2`, `Cacng2`, and `Cacng3` had no BH 0.05 DEGs in any measured group queried; `Cacna1d` had only two one-gene hits outside `151`; `Cacna2d1` and `Cacnb4` were one-gene focal responses. `Cacna1g` was the main calcium-channel exception, with 12 DEGs in `151` and one additional DEG in a cerebellar GABA class.
- Focal Parquet rows confirmed that the one-gene `Cacna2d1` and `Cacnb4` responses were self-transcript events, while the quiet calcium-channel alpha perturbations had the following focal self rows: `Cacna1a` logFC -0.365, adjusted p = 1; `Cacna1d` logFC -0.033, adjusted p = 1; `Cacna1e` logFC 0.473, adjusted p = 1; `Cacna2d2` logFC -0.113, adjusted p = 1.

## Synthesis

Cacna1c has enough focal expression and stock turnover that I would not treat it as an unexpressed or unrealized perturbation. The count-scale analogs still point to a near-null rather than a broad calcium-homeostasis state: the closest pore-forming L-type paralog, `Cacna1d`, is 0 in the focal class and only two DEGs across all queried groups; the other high-voltage alpha subunits `Cacna1a` and `Cacna1e` are also 0. The modest Cacna1g response shows that this thalamic class can report a calcium-channel loss, but Cacna1g is a T-type thalamic excitability gene and is not as close a functional match to CaV1.2 as `Cacna1d`.

Balancing high Cacna1c reach and likely depletion against the very small local channel-family training counts, I predict a one-gene signature rather than a complete null or a Cacna1g-like multi-gene response.
