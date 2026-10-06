# Direct Atf2 forecast trace

## Target and endpoint

- Target: `Atf2`
- Cell group: `151 TH Prkcd Grin2c Glut`
- Endpoint: number of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05` in the held-out target profile.
- Prediction: `2`

## Declared target biology

The declared target bundle exposed biology and focal-population reach, not the held-out `Atf2` endpoint.

The exact non-target focal expression measurement makes failed reach unlikely as a dominant prior: in `151 TH Prkcd Grin2c Glut`, `Atf2` was detected in 20,531 of 23,679 non-target cells, or 86.71%, with mean CP10k 1.499 and mean raw UMI 2.365. The target feature was therefore available and broadly sampled in the exact assay population.

The functional-stock card also argues that a P16 disruptive edit should matter by the P37-P44 harvest. ATF2 is a dynamic nuclear CRE/AP-1 bZIP transcriptional regulator; its pre-edit protein pool is not an installed long-lived structure, and the card adjudicated its functional stock as likely substantially depleted across the 21-28 day window.

The same card kept the postnatal transcriptional requirement uncertain. The direct neural mouse phenotype was embryonic brainstem motor-neuron loss rather than post-P16 thalamic loss, no comparable postnatal latency was reported, ATF7 redundancy was demonstrated only outside neurons, and survivor-conditioned sampling could attenuate a lesion that harms a subset of cells. I therefore treated target engagement as plausible, but not as evidence for a broad maintained thalamic expression program.

## Training measurements used

The focal-class training count table contains 1,674 measured training perturbations and excludes `Atf2`. Its distribution is heavily zero-inflated: 1,205 targets had 0 DEGs, 1,481 had at most 1 DEG, the median was 0, the 75th percentile was 1, the 90th percentile was 2, the 95th percentile was 18, the mean was 14.05, and only 43 training targets reached at least 100 DEGs.

The closest direct ATF2 partner and paralog named in the biology bundle, `Jun` and `Atf7`, were not in the training count table. I therefore used represented CREB/AP-1/bZIP and stress-responsive transcriptional comparators:

| training target | focal `n_degs` |
|---|---:|
| Atf6 | 0 |
| Bach2 | 0 |
| Creb1 | 10 |
| Crebbp | 8 |
| Fosl2 | 0 |
| Jund | 0 |
| Maf | 0 |
| Mafb | 0 |
| Mafg | 1 |
| Nfe2l2 | 0 |
| Smad3 | 0 |

Those 11 comparators had a mean focal count of 1.73 and a median of 0. A profile comparison over their focal Parquet rows confirmed the count-table picture directly from `pvals_adj`: 8 of 11 had no significant focal features, `Mafg` had 1, `Crebbp` had 8, and `Creb1` had 10. A filtered Parquet read of the same cohort found only 19 significant target-gene rows in total, all from `Creb1`, `Crebbp`, or `Mafg`.

The same-experiment corpus had no `Atf2` Finding or Claim. For measured comparators, it supported the small-count interpretation: `Creb1` made a restricted thalamic CREM-centered response; `Crebbp` made a small thalamus-restricted response that did not phenocopy `Creb1`; `Jund` was buffered in 22 of 23 cell groups; and `Fosl2` was almost completely buffered. Corpus Claims around `Jund`/`Fosl2` also stated that represented CREB/AP-1/EGR/bZIP/MAPK perturbations did not form a shared postnatal neuronal loss-of-function transcriptomic module.

## Synthesis

The upward evidence is that `Atf2` is well expressed in the exact focal class and should not retain a month-long pre-edit ATF2 protein stock. A zero is therefore possible but not forced by lack of reach.

The stronger quantitative evidence is downward. In basal survivor snRNA-seq, single AP-1/bZIP perturbations near ATF2 were flat or singleton, and even the measurable nuclear CREB/CBP arm stopped at 8-10 focal DEGs. The corpus summaries show that those perturbations did not recover a broad immediate-early, AP-1, UPR, redox, or generic stress module under the P16-to-P37/P44 design. ATF2's closest developmental phenotype is from embryonic motor neurons, not juvenile thalamus, and ATF7-family buffering remains a live explanation for a mild single-gene loss-of-function signature.

I therefore placed `Atf2` just above the null mode and near the quiet comparator mean, below `Creb1`/`Crebbp` but above the many represented AP-1/bZIP zeros.
