# Direct forecast for Naa20 in 151 TH Prkcd Grin2c Glut

## Endpoint

The requested value is the number of measured genes in `151 TH Prkcd Grin2c Glut` with BH-adjusted Wilcoxon `p < 0.05` after P16 CRISPR loss of `Naa20`, assayed at P37-P44 in recovered thalamic NeuN-positive nuclei.

## Evidence used

- The declared one-row manifest and canonical biology bundle both name `Naa20`.
- The selected same-experiment corpus has no target report, Finding, Claim, or explicit same-experiment reference for `Naa20`, so no packaged `Naa20` response was available.
- The exact focal-population expression measurement in the `Naa20` bundle shows broad target reach before perturbation: `Naa20` was detected in 21,132 of 23,679 non-target nuclei in `151 TH Prkcd Grin2c Glut` (`89.24%`), with mean CP10K `1.78`, mean log1p CP10K `0.920`, and pseudobulk CPM `176.44`. Low baseline expression in the assayed population therefore was not the main reason to expect a null.
- The bundle's functional-stock adjudication calls `Naa20` a multi-pool perturbation: it supplies the catalytic `Naa20`-`Naa25` NatB complex, while already installed N-terminal acetylation remains on individual substrate molecules until those proteins turn over. The adjudicated harvest-window conclusion was `likely_substantially_depleted`, because Naa20 and Naa25 turn over on a days scale and most measured adult-thalamus proteins are projected to replace most of their pre-edit molecules over 21-28 days.
- The same bundle keeps target-context latency and phenotype transfer unresolved. The closest direct mouse loss experiments are fibroblast NatB-loss experiments, the human neuronal CRISPRi evidence was established before or during differentiation, and the bounded search did not find an acute Naa20-loss experiment initiated in postnatal mouse neurons or thalamus.
- In the declared focal-class training count table, 1,205 of 1,674 perturbations had `n_degs = 0`, the median was `0`, the 75th percentile was `1`, and only 132 perturbations had at least 5 DEGs. The unconditional focal-class prior from this table is therefore heavily concentrated at zero and low single-digit counts.
- The closest measured in-family comparator in the training table was `Naa10`, the NatA catalytic subunit, with `0` DEGs in `151 TH Prkcd Grin2c Glut`. Its same-experiment report interpreted the whole P16 postmitotic-neuron perturbation as a strong FDR-level null: 22 measured neuronal groups, 2,123 matched perturbed nuclei, and zero downstream genes at FDR < 0.10. A companion Finding found no NAT-family, integrated-stress, apoptosis, or proteasome/ubiquitin rebound program for `Naa10` at FDR < 0.10.
- The `Naa10` report also gave an assay-detectability contrast: proteostasis and translation comparators were readily detected in the same screen, whereas `Naa10` stayed flat. In the focal training table, `Psmb4`, `Psmc1`, and `Eef2` had 742, 430, and 9 DEGs respectively.
- The human neuronal bundle evidence links NatB perturbation to alpha-synuclein abundance, but direct `Snca` loss was also quiet in the focal training table (`0` DEGs) and was annotated as a near-pan-neuronal transcriptional buffer in the same-experiment corpus.

## Synthesis

The exact expression and functional-stock evidence argue against treating `Naa20` as an unreachable or unedited target: a successful edit should deplete the renewable NatB catalytic pool before harvest. The main downward evidence is instead endpoint specificity. NatB loss is a broad post-translational N-terminome perturbation with pre-edited substrate carryover, and the matched screen shows that acute loss of the related NatA catalytic subunit can be almost invisible to nuclear RNA despite biochemical plausibility and despite the assay detecting large proteostasis/translation states when they actually occur.

`Naa20` could be stronger than `Naa10` because NatB loss was adjudicated as likely to deplete much of the relevant functional stock and because the focal population expresses `Naa20` broadly. I therefore would not force a structural zero. But the absence of a matched postnatal mouse-neuron phenotype, the substrate-distributed rather than transcription-factor-like operation, survivor-conditioned readout, `Snca` quietness, and the highly zero-inflated focal training table make the most likely integer `0`, with the main alternative being a low single-digit count rather than a broad 50+ DEG state.

## Point prediction

`predicted_n_degs = 0`
