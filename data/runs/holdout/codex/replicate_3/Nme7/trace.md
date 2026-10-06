## Evidence

Target and endpoint:

- The held-out manifest contains the single target `Nme7`.
- The endpoint is `n_degs` in `151 TH Prkcd Grin2c Glut`: the count of measured genes with BH-adjusted Wilcoxon `p < 0.05`.
- I treated the training count table and `training_de_all_cell_groups.parquet` as the direct measurements and did not use an Nme7 held-out expression signature or Nme7 outcome.

Focal-class training distribution:

- The focal count table has 1,674 training perturbations.
- It is heavily zero-inflated: 1,205/1,674 are `0`, the median is `0`, the 75th percentile is `1`, the 90th percentile is `2`, and the 95th percentile is `18`.
- The upper tail is real but sparse: the maximum is `2,677`, and the largest targets are broad cell-state regulators such as `Uba5`, `Tpr`, `Sin3a`, `Rnpc3`, and `Zbtb7a`, not ciliary NME-family genes.

Nme7 biology and expression:

- The declared biology bundle gives exact focal-population Nme7 expression in the non-target nuclei: 10,333/23,679 nuclei expressing, 43.64% expressing, mean raw UMI 0.628, mean cp10k 0.396, and pseudobulk CPM 39.38.
- The curated biology supports an operative role for NME7 in gamma-tubulin-ring-complex-associated microtubule nucleation and basal-body/primary-cilium stability, supported mainly by cultured-cell evidence and mouse germline ciliary phenotypes.
- The same bundle flags the decision-relevant postnatal neuronal timing as unresolved: existing soluble, gammaTuRC-bound, basal-body, or ciliary NME7-associated pools would not be instantly removed by a P16 disruptive edit, and no transferable NME7 or ciliary-carrier turnover measurement was available for postmitotic thalamic neurons at P37-P44.
- Nme5, Nme6, and Nme8 are the closest declared group-II paralogs, but none were present in the focal training count table, so they could not be used as observed analogs.

Training perturbations closest to the available cilium/microtubule prior were quiet in the same focal contrast:

| perturbation group | training perturbations | focal `n_degs` |
| --- | --- | --- |
| intraflagellar transport / ciliopathy / centrosome | `Ift88`, `Ift81`, `Ift43`, `Bbs5`, `Kif3b`, `Cep290`, `Cep112`, `Cep120`, `Cep85l`, `Cfap69`, `Nek1`, `Nek9`, `Ttll5` | all `0` |
| tubulin structural targets | `Tuba1a`, `Tuba4a`, `Tubb4b`, `Tubb5` | `7`, `2`, `1`, `1` |

Direct Parquet checks in `151 TH Prkcd Grin2c Glut` confirmed 17,259 measured genes per analog target and the same 23,679 matched control nuclei. The tubulin hits were small and mostly self-family changes: for example, `Tuba1a` had 7 significant genes dominated by down-regulated `Tuba1a` plus up-regulation of other tubulin transcripts; `Tuba4a` had 2, and `Tubb4b` and `Tubb5` had only their self transcripts at FDR < 0.05.

The matched profile comparison of `Ift88`, `Ift81`, `Ift43`, `Bbs5`, `Cep290`, `Kif3b`, `Tuba1a`, `Tuba4a`, `Tubb4b`, and `Tubb5` did not reveal a hidden coherent response module. Six of the ten had no significant focal features, four had 1-9 significant features, mean positive-tail overlap across the 45 pairwise comparisons was 0.0278, mean negative-tail overlap was 0.0309, and the significant-program overlap was zero.

## Synthesis

Nme7 is not an assay-absent gene in the focal population, so an edited transcript or a genuine downstream response is possible. The biology, however, points to a cilium/gammaTuRC maintenance function with uncertain depletion kinetics after a postnatal edit rather than to an acute transcriptional regulator. The most interpretable observed training analogs for that biology were exact zeros, and the broader ciliary/centrosomal set gave no evidence for a reproducible thalamic glutamatergic transcriptional state.

The base rate also favors zero: three quarters of training targets have at most one DEG in this class. I therefore placed Nme7 in the near-null ciliary group and used `0` as the integer point forecast rather than rounding upward for expression alone.

## Prediction

`predicted_n_degs = 0`
