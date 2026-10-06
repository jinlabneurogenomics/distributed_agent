# Direct forecast for Pum1 in 151 TH Prkcd Grin2c Glut

## Declared target and endpoint

- Target: `Pum1`, from the one-row holdout manifest `Pum1.csv`.
- Endpoint: `n_degs`, the number of measured genes in `151 TH Prkcd Grin2c Glut` with BH-adjusted Wilcoxon `pvals_adj < 0.05`.
- Training endpoint table: `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`, 1,674 training targets after the `Pum1` holdout; `Pum1` is absent.
- Matched DE profiles: `training_de_all_cell_groups.parquet`; I used only training perturbations and the `151 TH Prkcd Grin2c Glut` context for observed-profile comparisons.
- Canonical target biology: `biology_bundles/Pum1.json` / `characterization_bundle(view="biology")`, with `target_outcome_exposed=false`, `labeled_neighbors_exposed=false`, and endpoint values excluded from the biological cards.

## Target biology used

The exact in-assay reach argues that the 151 thalamic class can express the target: among non-target nuclei, `Pum1` was detected in 17,156 / 23,679 nuclei, or 72.45%, with mean CP10k 0.906 and pseudobulk CPM 89.39.

The functional-stock card makes a P16 edit biologically plausible by P37-P44 rather than simply too late: Pum1 is a free, renewable cytoplasmic RNA-binding regulator, disruptive editing stops new functional protein production but leaves existing protein transiently active, and a generic mouse-brain proteome turnover proxy favors substantial replacement over the 21-28 day window. Confidence is limited because no Pum1-specific neuronal protein half-life was found.

The same bundle keeps the expected RNA effect modest. Pum1 represses many bound mRNAs, but published mouse neural data report translational effects with many target transcripts unchanged; Pum2 shares many Pum1 targets and is a credible partial buffer. The strongest mouse loss phenotype is postnatal and neural, but it is cerebellar/progressive and is not a matched acute thalamic snRNA-seq effect.

## Training scale and comparator measurements

The 151 training count table is extremely zero-heavy:

- median `n_degs`: 0
- 75th percentile: 1
- 90th percentile: 2
- 95th percentile: 18
- 99th percentile: 430
- 469 / 1,674 training perturbations had at least one significant gene
- 106 / 1,674 reached at least 10 significant genes

For biologically closer post-transcriptional or translation-linked training perturbations in the same 151 class, the observed counts were low:

| comparator | 151 `n_degs` | interpretation |
| --- | ---: | --- |
| `Ago2` | 0 | miRNA/post-transcriptional machinery |
| `Dicer1` | 0 | miRNA biogenesis |
| `Fmr1` | 0 | neuronal cytoplasmic translational repressor |
| `Fxr1` | 0 | FMRP-family RNA regulator |
| `Ago1` | 1 | miRNA/post-transcriptional machinery |
| `Mtor` | 2 | translation-growth signaling |
| `Ddx3x` | 8 | RNA helicase/translation-linked RBP |
| `Hnrnpa2b1` | 11 | RBP, still only a small 151 response |

Several other RNA-processing genes showed much larger signatures, but their biology is a poor scale match for Pum1 because they perturb core nuclear RNA processing or broad hnRNP state rather than Pumilio cytoplasmic target repression:

| comparator | 151 `n_degs` |
| --- | ---: |
| `Tardbp` | 210 |
| `Snrnp70` | 213 |
| `Prpf6` | 454 |
| `Hnrnpu` | 733 |
| `U2af2` | 828 |

The profile comparison among these RNA regulators in the 151 Parquet rows gave the same separation. The high-count nuclear/spliceosomal nodes clustered with one another, for example `Prpf6`-`U2af2` had Pearson 0.345 and `Prpf6`-`Snrnp70` had Pearson 0.334, while low-count post-transcriptional nodes had weak whole-profile similarity to that high-count cluster. I therefore used the high-count nuclear RNA-processing profiles only as upper-bound context, not as direct analogues.

## Synthesis

I expect successful Pum1 loss in many recovered 151 neurons, so a strict accessibility-driven zero is too low. But the response should be much closer to translational/miRNA/RBP comparators with 0-11 DEGs than to spliceosome or broad nuclear hnRNP failures with hundreds of DEGs, because Pum1's immediate activity is mostly post-transcriptional protein repression, Pum2 can buffer part of the program, and the measured endpoint is survivor-conditioned nuclear mRNA.

I placed `Pum1` just above the 90th percentile of the full 151 training table and below the small positive RNA-regulator donors `Ddx3x` and `Hnrnpa2b1`.

Point prediction: 3
