# Pdss1 n_degs prediction

## Target and endpoint

- Target: `Pdss1`.
- Cell class: `151 TH Prkcd Grin2c Glut`.
- Endpoint: `n_degs`, the number of measured genes with BH-adjusted Wilcoxon `p < 0.05` in this cell class.
- The declared focal count table and Parquet omit the `Pdss1` perturbation outcome, so the forecast below uses the target biology bundle plus held-in training perturbations only.

## Biology prior from the declared target bundle

The target bundle makes `Pdss1` biologically reachable in the focal cells:

- Exact in-assay focal expression was present in 19,123 / 23,679 non-target nuclei, 80.759% of cells, with mean raw UMI 2.033, mean log1p CP10K 0.720, and pseudobulk CPM 127.43.
- PDSS1 is an obligate PDSS1/PDSS2 long-chain polyprenyl-diphosphate synthase subunit for CoQ side-chain synthesis, not a redundant paralog.
- Loss of new PDSS1 activity should initially spare pre-existing PDSS enzyme and installed ubiquinone, but the product pool is expected to turn over substantially within the P16-to-P37/P44 assay window. The card therefore adjudicates functional stock by harvest as `likely_substantially_depleted`, with uncertainty from the unmeasured neuronal PDSS1 protein half-life and unknown reserve threshold.

That evidence argues against treating `Pdss1` as unreachable, but it does not imply that CoQ depletion must exceed a nuclear snRNA-seq FDR threshold in recovered postmitotic neurons.

## Held-in measurements used

The closest direct same-pathway held-in target was `Coq5`, another CoQ-biosynthesis perturbation:

- `Coq5` had `n_degs = 0` in the exact `151 TH Prkcd Grin2c Glut` training count table.
- Its packaged same-experiment findings describe a pan-neuronal buffered RNA surface: zero downstream genes at FDR < 0.10 in 22 measured neuronal groups, absent ATF4/CHOP mitochondrial ISR despite that program being detectable for other perturbations, and no meaningful convergence with UQCRC/CYC1/NDUF/LONP1/CLPP comparators.
- In a fresh focal profile comparison over 53 mitochondrial, TCA, and respiratory-chain held-in targets, `Coq5` had 0 significant features; its ten strongest positive and ten strongest negative focal Wilcoxon ranks all had `pvals_adj = 1.0`.

The wider mitochondrial/respiratory-chain focal count set was also near-null:

- 53 selected held-in mitochondrial, TCA, CoQ, and ETC-related targets in `151 TH Prkcd Grin2c Glut` had 32 zeros, 20 singletons, and only one target above one DEG.
- The main outlier was `Opa1` with 37 DEGs. `Opa1` is real positive evidence that this cell class can show an ATF4/ISR-like mitochondrial stress state, but the same corpus repeatedly separates `Opa1` from generic ETC or CoQ loss: `Sdha` was broadly buffered with only one focal DEG, `Clpp` had 0 focal DEGs, `Park7` had 1, and represented Complex I/III/IV/TCA targets were almost all 0 or 1.
- In the 53-node focal profile comparison, 32 nodes had no significant features, 20 had 1-9, and only `Opa1` fell in the 10-49 bin. Whole-profile correlations around `Coq5` were essentially noise-scale; its best Pearson neighbor among those 53 was `Opa1` at 0.032, followed by `Cox8a` at 0.028.

## Synthesis

`Pdss1` has enough focal expression and no direct redundancy, so a small response is plausible if the CoQ pool falls far enough after P16 editing. The actual observed neighborhood nevertheless centers on zero: the one direct CoQ-biosynthesis comparator, `Coq5`, was completely silent in the focal class and across the corpus report; broad ETC and TCA perturbations usually gave 0 or 1 focal genes; and the `Opa1` stress outlier was profile-distant and mechanistically branch-specific rather than a generic mitochondrial-loss scale donor.

I therefore predict that `Pdss1` most likely stays below the focal FDR < 0.05 threshold and assign the integer point estimate:

```tsv
target_name	predicted_n_degs
Pdss1	0
```
