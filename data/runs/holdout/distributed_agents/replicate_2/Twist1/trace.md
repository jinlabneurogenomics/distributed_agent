# Twist1 DEG-count prediction for `151 TH Prkcd Grin2c Glut`

## Question and interpretation

The held-out target list for this run contained one mouse perturbation, `Twist1`. I interpreted the requested endpoint as the integer number of measured genes with `pvals_adj < 0.05` in the matched `151 TH Prkcd Grin2c Glut` differential-expression table that would have been observed if `Twist1` had not been held out. `Twist1` was absent from both the parquet and the training-count CSV, so no row from the target itself was used.

I treated zero as "no gene passes the exact Scanpy/Wilcoxon BH-adjusted cutoff in the focal cell group", not as a statement that CRISPR failed or that TWIST1 lacks function in every tissue. The experiment is acute, sparse P16 AAV-CRISPR in recovered NeuN+ postnatal brain nuclei; embryonic cranial mesenchyme, calvarial sutures, neural crest, endothelial, fibroblast, and glial contexts are largely out of scope.

## Sources used

- `training_de_all_cell_groups.parquet`: exact signed log2 fold changes and adjusted p-values for candidate analog perturbations, filtered to `group_name == "151 TH Prkcd Grin2c Glut"`.
- `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`: exact focal-cell DEG counts for all 1,674 non-held-out training targets. In this file, 1,205/1,674 targets, or 72.0%, were zero; 363 had 1-9 DEGs; 63 had 10-99; and 43 had at least 100.
- Distributed Agents corpus release `perturbai-july-260713-sourceguard-1773-v1`, the same-experiment interpreted ledger. `Twist1` itself had no target report, as expected for a held-out gene. I used target reports and claims for `Tcf3`, `Tcf4`, `Tcf12`, `Atoh1`, `Neurod1`, `Neurod2`, and `Runx2`, especially the high-confidence claim that represented developmental bHLH and class-I E-protein perturbations largely fail to form a shared acute transcriptional module in mature postnatal neuronal nuclei, apart from a narrow `Tcf4` Pvalb response.
- Distributed Agents runtime profile comparison over focal-class log-fold-change vectors. I compared the candidate analogs `Twist2`, `Tcf3`, `Tcf4`, `Tcf12`, `Atoh1`, `Neurod1`, `Neurod2`, `Snai2`, `Zeb1`, `Zeb2`, `Runx2`, `Meox1`, and `Tcf7l2`.
- PubMed literature for TWIST1 biology: Fan et al. 2020, DOI 10.1128/MCB.00663-19, PMID 32179550; Soo et al. 2002, DOI 10.1006/dbio.2002.0699, PMID 12086465; O'Rourke et al. 2002, DOI 10.1006/dbio.2002.0730, PMID 12142027; Firulli et al. 2005, DOI 10.1038/ng1525, PMID 15735646; Gitelman 1997, DOI 10.1006/dbio.1997.8614, PMID 9299114.

## Computation over the supplied tables

I first loaded the requested-target CSV and confirmed that `Twist1` was the only requested held-out target. I summarized the focal training-count CSV to calibrate the baseline distribution of `n_degs`: the median was 0, the 75th percentile was 1, the 95th percentile was 18, and the maximum was 2,677. That skew makes a nonzero prediction appropriate only when a held-out target has a close active analog in the same assay.

I then selected literature-obvious `Twist1` comparators from the training targets:

| Training target | Rationale | Focal `n_degs` |
|---|---:|---:|
| `Twist2` | closest measured TWIST-family paralog | 0 |
| `Tcf3` | class-I E-protein TWIST1 heterodimer partner | 0 |
| `Tcf4` | class-I E-protein TWIST1 heterodimer partner | 0 |
| `Tcf12` | class-I E-protein TWIST1 heterodimer partner | 0 |
| `Atoh1`, `Neurod1`, `Neurod2` | class-II/proneural bHLH factors that test whether bHLH loss generally exposes a postnatal neuronal RNA module | 0, 0, 0 |
| `Snai2`, `Zeb1`, `Zeb2` | EMT/neural-crest-associated transcription factors; mechanistically more distant than TWIST bHLH/E-proteins | 0, 15, 0 |
| `Runx2`, `Meox1` | cranial mesenchyme/osteogenic-development counterexamples with developmental lineages closer to canonical TWIST1 biology than to thalamic neurons | 0, 0 |
| `Tcf7l2` | Wnt/HMG thalamic transcription factor, useful as a name-family and developmental-TF counterexample rather than a TWIST analog | 106 |

For the same targets, I scanned the parquet for the focal group and counted rows with `pvals_adj < 0.05`. The exact counts matched the CSV. I also inspected the most significant focal-class rows for the closest analogs. `Twist2`, `Tcf4`, `Tcf12`, `Atoh1`, `Neurod1`, `Neurod2`, `Snai2`, `Zeb2`, `Runx2`, and `Meox1` had `pvals_adj == 1` for their top rows; `Tcf3` had two nominal leading rows but still no FDR hit (`Rusc1`, adjusted p = 0.884; `Akt1`, adjusted p = 0.884). By contrast, the more distant boundary genes were genuinely detectable in this cell class: `Zeb1` had 15 FDR-significant genes, led by `Stxbp2`, `Ap1m2`, and `F11r`, and `Tcf7l2` had 106, led by `Ramp3`, `Cck`, `Spock3`, `Kcnc2`, and `Pcsk2`.

The runtime profile comparison used 17,259 shared measured genes per perturbation in `151 TH Prkcd Grin2c Glut`. Eleven of the thirteen inspected analogs had no significant features. `Zeb1` had 15 significant positive genes, and `Tcf7l2` had 39 positive and 67 negative significant genes. Whole-vector correlations among the flat bHLH perturbations were moderate only in weak all-gene logFC background; the FDR-level evidence remained empty for the TWIST/E-protein core, so I did not treat those background correlations as an active module.

## Target-specific reasoning

### `Twist1`

`Twist1` encodes a basic helix-loop-helix transcription factor. Fan et al. showed that TWIST1 predominantly forms homodimers and heterodimers with the class-I E-proteins TCF3, TCF4, and TCF12, and that TWIST1/E-protein heterodimers can drive mesoderm and neural-crest differentiation with EMT-like programs in stem-cell and cranial mesenchyme systems. Mouse loss-of-function work places Twist activity in embryonic cranial mesenchyme, cranial neural-crest migration, branchial arches, and limb FGF/SHH signaling rather than in maintenance of juvenile thalamic glutamatergic neurons (Soo et al. 2002; O'Rourke et al. 2002; Gitelman 1997). Firulli et al. further showed that Twist1/Hand2 dimerization balance is important for limb and craniofacial phenotypes.

That biology nominated `Twist2`, `Tcf3`, `Tcf4`, and `Tcf12` as the closest represented training perturbations. All four had zero DEGs in the focal held-out readout's training endpoint:

- `Twist2`: 0 DEGs; leading focal rows `Lca5`, `Me2`, and `Mtpap` all had adjusted p = 1.
- `Tcf3`: 0 DEGs; leading rows had adjusted p = 0.884 or 1.
- `Tcf4`: 0 DEGs in this focal class; leading rows all had adjusted p = 1. The same-experiment corpus notes that `Tcf4` has only a narrow two-gene Pvalb response elsewhere, not a broad bHLH/E-protein program.
- `Tcf12`: 0 DEGs; leading focal rows all had adjusted p = 1. Distributed Agents `Tcf12:F004` explicitly frames `Twist1`/craniosynostosis-related biology as displaced to embryonic suture, GnRH, or olfactory-axis contexts absent from the NeuN+ brain assay.

The next bHLH/proneural comparators reinforced the same call. `Atoh1`, `Neurod1`, and `Neurod2` each had zero focal DEGs, and the Distributed Agents corpus claim over `Atoh1`, `Neurod1`, `Neurod2`, `Ptf1a`, `Tcf3`, `Tcf4`, and `Tfap4` concluded that represented developmental bHLH and E-protein perturbations mostly do not create a shared mature-neuronal acute transcriptional module in this experiment. This is the dataset-local evidence that kept me from assigning `Twist1` a small positive count merely because it is a DNA-binding transcription factor.

I treated the active distant targets as boundaries rather than positive analogs. `Zeb1` had 15 DEGs and is an EMT/neurodevelopmental zinc-finger factor, but `Zeb2`, `Snai2`, and `Twist2` were flat, so the focal `Zeb1` response is not enough to transfer an EMT signature to `Twist1`. `Tcf7l2` had 106 DEGs in the same thalamic class, showing that Wnt/HMG thalamic transcription factors can be visible, but it is not a class-I E-protein despite the `Tcf` name and it is not a TWIST1 dimer partner. `Runx2` and `Meox1` were also flat, consistent with the corpus observation that canonical osteogenic/cranial-mesenchymal programs are not detectably engaged in NeuN-enriched postnatal nuclei.

The zero/nonzero decision is therefore driven mostly by within-dataset evidence: the closest measured paralog and all measured E-protein partners were exactly zero in the focal endpoint. External biology was used to decide that those zeroes are the right comparators for `Twist1`, and to mark the mesenchymal/neural-crest TWIST1 literature as an off-assay developmental program rather than as evidence for a broad thalamic neuronal response.

I predict `Twist1` will also have no genes passing BH FDR 0.05 in `151 TH Prkcd Grin2c Glut`.

## Limits and extrapolation

This is still an extrapolation from analogs: `Twist1` itself was held out, and I did not observe its target RNA, indel rate, protein loss, or focal-class signature. Some plausible partners were not represented as training perturbations, including `Hand2` and the `Id` genes. The parquet also does not test calvarial suture, embryonic cranial neural crest, fibroblast, endothelial, or olfactory/GnRH developmental settings where TWIST1-family biology is strongest. Finally, the assay reads nuclear RNA from recovered NeuN+ nuclei 3-4 weeks after sparse CRISPR; it can miss protein-localization, chromatin-priming, rare-cell, survival-selection, and developmental phenotypes.

Those caveats could hide a tiny one- or two-gene effect, but the nearest observed family and dimerization partners all fell below the focal FDR threshold. Under squared log1p count loss, an exact zero is the most defensible point prediction.
