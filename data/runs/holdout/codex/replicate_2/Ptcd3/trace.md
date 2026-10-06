# Ptcd3 n_degs forecast for 151 TH Prkcd Grin2c Glut

## Declared target and target-side biology

- The one-row holdout manifest names `Ptcd3`.
- The canonical biology bundle reports exact focal-population reach for `Ptcd3` in `151 TH Prkcd Grin2c Glut`: the feature is present in the assay, with 20,854/23,679 non-target cells expressing `Ptcd3` RNA, 88.07% expressing, mean raw UMI 2.71, and mean log1p CP10k 0.884. I used this only as target reach, not as editing efficiency.
- The same bundle identifies PTCD3 as mS39, an rRNA-binding mitochondrial small-ribosomal-subunit component required for mitochondrial translation. PTCD3 loss is therefore close to a general mitochondrial-translation lesion, and strong depletion in human cells reduced mitochondrial protein synthesis and respiration.
- The functional-stock card weakens transfer to this acute neuronal CRISPR assay: a P16 edit should stop new PTCD3 production but does not directly remove pre-existing mS39-containing mitoribosomes, and no PTCD3 half-life, assembled-mitoribosome residence time, or direct post-edit neuronal timing anchor was found for the 21-28 day edit-to-harvest window.

## Training endpoint scale

The focal count table contains 1,674 training perturbations for this same cell class and is heavily concentrated at zero:

- 1,205/1,674 training targets have `n_degs = 0`.
- The median is 0 and the 75th percentile is 1.
- The 90th percentile is 2, while the broad responders are rare outliers.

I treated mitochondrial translation and OXPHOS perturbations as the main scale references rather than genome-wide broad responders. The most relevant same-experiment counts were:

| set | focal 151-class n_degs |
| --- | --- |
| `Dap3`, the available structural small-mitoribosomal comparator | 1 |
| mt-aaRS / mitochondrial-translation-adjacent `Fars2`, `Gfm2`, `Lars2`, `Rars2` | 0, 0, 0, 0 |
| mt-mRNA / OXPHOS-maintenance `Lrpprc` | 0 |
| core respiratory-chain comparators `Cox11`, `Cox4i1`, `Ndufs4`, `Ndufv1` | 0, 0, 0, 0 |
| core respiratory-chain comparators `Ndufs8`, `Ndufa10` | 1, 1 |

Across the 12 selected mitochondrial translation/OXPHOS anchors above, the sum was 3, the median was 0, and no target exceeded 1 DEG in the requested cell class. Across 35 represented `Cox*`, `Nduf*`, `Uqcr*`, and `Sdha` OXPHOS-related perturbations in the table, the median was also 0 and the mean was 0.43.

`Opa1` was kept as a positive mitochondrial contrast rather than as a Ptcd3 scale donor: it produced 37 DEGs in the requested cell class and the corpus reports an ATF4/mitochondrial-stress program for `Opa1` that was absent from `Dap3` and `Gfm2`.

## Same-experiment corpus checks on training targets

The packaged reports and Claims around the training comparators support interpreting the small counts as a pathway-level feature of this assay, not a failure of my symbol filter.

- `Dap3` produced no robust downstream transcriptome in any neuronal group; the same report explicitly contrasts its flat surface with the readily detected `Opa1` ISR-like mitochondrial-stress module.
- `Gfm2` produced no robust downstream response in any measured neuronal class, and a high-confidence Claim states that `Opa1` activates an ATF4/mitochondrial ISR-like amino-acid stress program whereas mitochondrial comparators including `Gfm2`, `Ndufs2`, `Ndufv1`, and `Ndufa4` do not cross that response threshold.
- A moderate-confidence Claim over `Aimp1`, `Fars2`, `Gfm2`, `Lars2`, and `Rars2` states that represented mitochondrial aaRS and protein-synthesis perturbations were transcriptionally buffered or nonconvergent rather than forming a shared acute mitochondrial stress or translation RNA module.
- `Lrpprc` had 0 downstream FDR genes in all recovered cell groups and lacked both the expected mtDNA mRNA response and secondary ISR/UPRmt markers.

## Focal profile checks

I compared 13 observed mitochondrial references in `151 TH Prkcd Grin2c Glut` directly from the training Parquet using signed Wilcoxon scores and the task's `pvals_adj < 0.05` threshold. In that profile cohort:

- 9/13 targets had no significant feature.
- 3/13 had 1 to 9 significant features.
- `Opa1` was the only 10 to 49 feature responder, with 37 DEGs.

The 12-node mitochondrial translation/OXPHOS cohort had no shared positive significant program, and its tail overlap was tiny: mean positive top-tail overlap coefficient 0.023 and mean negative top-tail overlap coefficient 0.026 across 66 available pairs. The self-row check also showed that `Dap3`, `Ndufs8`, and `Ndufa10` each crossed FDR only on their own transcript in this selected mitochondrial block:

- `Dap3` self row: adjusted p = 3.95e-6; all other selected mitochondrial-gene cross-rows nonsignificant.
- `Ndufs8` self row: adjusted p = 3.06e-8; all other selected mitochondrial-gene cross-rows nonsignificant.
- `Ndufa10` self row: adjusted p = 4.84e-7; all other selected mitochondrial-gene cross-rows nonsignificant.

Thus the closest structural comparator, `Dap3`, points to an otherwise flat profile with one observable self-transcript hit, not to a real multi-gene downstream mitochondrial program.

## Forecast

The biological prior says `Ptcd3` loss can matter if PTCD3 stock is renewed, because it removes a nonredundant small-mitoribosomal component. The training measurements say that this acute recovered-neuron snRNA-seq endpoint usually does not convert mitochondrial translation, mt-aaRS, mt-mRNA maintenance, or single OXPHOS-subunit disruption into a multi-gene response in `151 TH Prkcd Grin2c Glut`. The main remaining way to get above zero is a self-transcript event; `Ptcd3` is well expressed in this focal population, and the closest structural training anchor, `Dap3`, landed at exactly one count through its own transcript.

I therefore predict a flat downstream profile plus one significant `Ptcd3` self-feature:

`predicted_n_degs = 1`

I did not query or use the held-out `Ptcd3` expression signature or DEG count, and I did not use relationship-review, branch-calibration, terminal-prediction, scalar-prior, or calibrated-probability artifacts.
