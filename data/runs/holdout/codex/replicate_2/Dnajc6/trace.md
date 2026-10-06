# Dnajc6 n_degs forecast

## Target and endpoint

Target: `Dnajc6`

Focal population: `151 TH Prkcd Grin2c Glut`

Endpoint: number of measured genes in the focal population with BH-adjusted Wilcoxon `p < 0.05`.

## Evidence used

- The declared holdout manifest names `Dnajc6`.
- Exact focal-population reach from the outcome-blind `Dnajc6` biology bundle shows that `Dnajc6` is measured in `151 TH Prkcd Grin2c Glut` non-target cells: 21,198 of 23,679 nuclei express it, 89.52% of nuclei, with mean raw UMI 3.06 and pseudobulk CPM 191.85. This supports a plausible focal edit target but does not determine self-knockdown or downstream effect size.
- The same bundle places Dnajc6/auxilin directly in presynaptic clathrin uncoating: auxilin recruits HSPA8/Hsc70 to clathrin-coated vesicles and is reused after cage disassembly. It also records mouse loss phenotypes in postnatal synapses, likely auxilin stock depletion over the P16-to-P37/P44 interval, and partial GAK compensation after Dnajc6 loss.
- The focal 151-TH training count table has a zero-heavy endpoint distribution: 1,205/1,674 training perturbations have `n_degs = 0`, the median is 0, the 75th percentile is 1, the 90th percentile is 2, and the 95th percentile is 18.
- Directly relevant observed synaptic and clathrin-adjacent perturbations are sparse in the same count table:
  - `Cltc`: 3 DEGs in 151 TH.
  - `Hspa8`: 9 DEGs in 151 TH.
  - `Dnm1`: 1 DEG, the self transcript.
  - `Synj1`: 1 DEG, the self transcript.
  - `Syp`: 1 DEG, the self transcript.
  - `Syn1`: 1 DEG, the self transcript.
  - `Unc13a`, `Unc13b`, `Unc13c`: 0 DEGs.
- Direct Parquet checks in the focal population show that `Cltc` had only three downstream significant genes and `Hspa8` had nine downstream significant genes at the task's `pvals_adj < 0.05` threshold. The one-gene calls for `Dnm1`, `Synj1`, `Syp`, and `Syn1` were self-transcript calls rather than broad downstream programs.
- The same-experiment Finding layer agrees with those exact counts at a qualitative level: `Cltc` is a selective clathrin response, `Hspa8` is a small HSP/co-chaperone response, and the canonical synaptic endocytosis perturbations `Dnm1` and `Synj1` do not phenocopy `Cltc` and are downstream-flat in the recovered nuclear-RNA endpoint.

## Synthesis

The target is reachable in the focal thalamic cells and the loss should matter biochemically: auxilin is a dynamic clathrin-uncoating co-chaperone, not a one-time developmental product, so an acute P16 disruptive edit has a credible route to deplete functional stock by harvest.

The quantitative endpoint is nevertheless expected to sit at the floor. The best matched observed nodes show that perturbing synaptic endocytosis machinery often produces no downstream focal signature at all, and even core `Cltc` and constitutive `Hspa8` give small 151-TH signatures. Dnajc6 is narrower than either core clathrin or HSPA8 and has explicit partial buffering by GAK, so I down-weighted the mouse auxilin-loss phenotype as evidence for a large survivor nuclear-RNA footprint.

Given high focal expression, I left room for one detected gene, most likely the target transcript itself or a single secondary thalamic transcript, rather than forecasting a complete null. The point forecast is:

`predicted_n_degs = 1`
