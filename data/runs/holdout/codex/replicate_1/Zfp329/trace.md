# Direct forecast for Zfp329

## Endpoint

`n_degs` is the count of focal-class `151 TH Prkcd Grin2c Glut` measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`.

The declared one-row holdout manifest names `Zfp329`. `Zfp329` was absent from the declared focal training count table, and the corpus `target_context` lookup for the selected July 2026 PerturbAI corpus returned `target_found=false` with zero same-experiment Findings, Claims, or explicit references for `Zfp329`.

## Target biology

Evidence came from the canonical endpoint-blind bundle:

`[local file: Zfp329.json]`

Relevant target facts were:

- exact focal non-target expression is detectable: `Zfp329` was expressed in 16,911 of 23,679 non-target nuclei in `151 TH Prkcd Grin2c Glut`, `71.4177%`, with `mean_cp10k = 0.8912`;
- the source card places Zfp329 as a nuclear C2H2 zinc-finger protein predicted to bind RNA polymerase II regulatory DNA and regulate transcription, but with no known target-specific binding motif or direct thalamic neuronal targets;
- the functional-stock card concluded `functional_stock_by_harvest = likely_substantially_depleted`: a P16 edit should stop new Zfp329 protein supply and 21-28 days is long enough for substantial turnover of a typical renewable thalamic protein pool;
- the evidence for postnatal thalamic requirement is weak: the curated mouse loss phenotype is a germline retina and optic-disc phenotype, there is no transferable post-edit time course, and no experimentally supported same-context compensator or close mouse paralog was found.

This made the perturbation biologically reachable in the assayed population but did not supply a strong reason to expect a broad survivor-state transcriptional program.

## Training measurements

The declared focal count table:

`[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`

contains 1,674 observed training perturbations. Its focal-class DEG-count distribution is heavily zero-inflated:

- `n_degs = 0` for 1,205 / 1,674 training targets;
- median `n_degs = 0`;
- 75th percentile `n_degs = 1`;
- 90th percentile `n_degs = 2`;
- mean `n_degs = 14.05`, driven by a long high-count tail up to 2,677.

Because Zfp329's only concrete molecular placement was as a C2H2 zinc-finger transcription factor, I used the observed `Zfp[0-9]*` entries as the closest family-level training readout. Among 29 such focal training perturbations, 24 had `n_degs = 0`. The only nonzero rows were:

| target | focal `n_degs` |
|---|---:|
| `Zfp148` | 8 |
| `Zfp236` | 19 |
| `Zfp423` | 150 |
| `Zfp612` | 1 |
| `Zfp692` | 1 |

The raw declared expression Parquet:

`[local file: training_de_all_cell_groups.parquet]`

confirmed that the zero rows in that `Zfp[0-9]*` set had no focal measured genes with `pvals_adj < 0.05`; each queried family member contributed 17,259 focal measured-gene rows. The nonzero entries were sparse except for the `Zfp423` outlier. Their significant rows were also not a shared signature: for example, `Zfp692` had only its self row significant, `Zfp612` had only `Notum`, `Zfp236` was led by `Ogt`, `Eif4a2`, and `Gdi1`, and `Zfp423` was led by a separate `Grid2ip`/`Cd47`/`Ntsr1`/`Kcnab3` program.

## Synthesis

The exact expression reach argues against treating Zfp329 as completely inaccessible in thalamic glutamatergic nuclei, and the expected functional-stock depletion makes a real edit-to-readout effect possible by P37-P44. However, the biology bundle leaves the relevant dependency unresolved rather than established: no postnatal thalamic loss phenotype, no measured direct targets, no kinetic measurement for the target protein, and only a germline visual-system phenotype.

The focal endpoint itself is dominated by zeros, and the nearest measured Zfp-number training cohort is even more concentrated at zero than the full table. I therefore discounted the isolated `Zfp423` and `Zfp236` responses as gene-specific outliers and used the mode and median of the family-level observations as the best direct forecast.

Predicted `n_degs`: `0`.
