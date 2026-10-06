# Twist1 direct n_degs forecast

Endpoint: number of measured genes in `151 TH Prkcd Grin2c Glut` with BH-adjusted Wilcoxon `pvals_adj < 0.05`.

Prediction:

```tsv
target_name	predicted_n_degs
Twist1	0
```

## Evidence Used

- The one-row declared holdout manifest names `Twist1`; `Twist1` was absent from the declared 1,674-row training count table.
- The declared biology bundle reports that Twist1 is a nuclear bHLH sequence-specific transcription factor. Existing Twist1 protein is not inactivated instantly by the edit, but available half-life evidence is on an hour scale, so functional stock should be substantially depleted during the 21-28 day P16-to-P37/P44 window if an edited cell was actually producing Twist1.
- The same bundle gives exact expression reach in the focal non-target population: `104 / 23679` nuclei expressed any Twist1 UMI, `pct_cells_expressing = 0.43920773681321`, `mean_cp10k = 0.0037423180819582593`, `mean_raw_umi = 0.005405633683854893`, and `pseudobulk_cpm = 0.3387902320116766`. This superseded the qualitative outside-brain annotations and made Twist1 a very low-reach target in the assayed thalamic NeuN-positive class.
- The biology bundle found no matched postnatal thalamic-neuron Twist1 loss experiment. The strongest direct mouse phenotype is embryonic and neural-adjacent but not transferable to postmitotic P16 thalamic neurons; Twist2 paralogy is also unresolved rather than a demonstrated buffer here.
- The declared 151-class count table is zero centered: among 1,674 training perturbations, 1,205 had `n_degs = 0`; the median was 0, the 75th percentile was 1, the 90th percentile was 2, and the 95th percentile was 18.
- In the same count table, selected developmental/bHLH/E-protein comparators were essentially flat in the focal class:

```tsv
target_name	n_degs
Atoh1	0
Neurod1	0
Neurod2	0
Ptf1a	0
Tcf3	0
Tcf4	0
Tcf12	0
Tfap4	0
Zic2	0
Zic1	2
Sox5	2
```

- The matched Parquet rows for those selected profiles showed ordinary cell recovery in the focal class, e.g. `Tcf3` had 152 perturbed nuclei, `Tcf12` 167, `Atoh1` 204, `Ptf1a` 231, `Tfap4` 238, `Tcf4` 250, `Neurod2` 260, and `Zic2` 260, all against 23,679 matched non-target nuclei. Their zero DEG calls therefore gave a better local scale than embryonic essentiality alone.
- Packaged Findings for training genes supported the same boundary. `Atoh1` had zero FDR<0.10 genes in 22 of 22 measured groups, and its report explicitly checked canonical bHLH/E-protein/Notch/SHH/Zic neighbors without finding a shared postnatal Atoh1-like response. `Tcf4` had a narrow Pvalb-only response outside this focal class, and the corpus Claim over Atoh1/Neurod1/Neurod2/Ptf1a/Tcf3/Tcf4/Tcf12/Tfap4 states that represented developmental bHLH and class-I E-protein perturbations largely failed to form a shared acute transcriptional module in mature postnatal neuronal nuclei.
- I treated high-count thalamic transcription factors as a scale-bearing upper boundary, not as close Twist1 analogues. `Tcf7l2` had 106 FDR<0.05 genes and `Ctnnb1` had 383 in the count table, and their reports describe a specific Wnt/TCF-associated 151 TH response. The selected low-reach bHLH/developmental factors do not show that response.
- A profile comparison over `Atoh1`, `Neurod1`, `Neurod2`, `Ptf1a`, `Tcf3`, `Tcf4`, `Tcf12`, `Tfap4`, `Zic1`, `Zic2`, `Tcf7l2`, `Ctnnb1`, `Foxp2`, and `Sox5`, restricted to `group_name == "151 TH Prkcd Grin2c Glut"`, found no missing profiles. Ten of the 14 had no significant features, two had 1-9, and only `Tcf7l2`/`Ctnnb1` had at least 50. Across the 91 selected pairs, median significant-program overlap was 0 in both directions and median 1% tail overlap was only 0.02-0.03, so the cohort did not contain a hidden common developmental-TF program.

## Synthesis

The decisive quantities are the very low exact Twist1 focal expression and the flat matched developmental bHLH/E-protein training perturbations. Twist1 should lose functional protein in the rare cells where it is expressed, but only ~0.44% of matched non-target nuclei had detectable Twist1 RNA, and the canonical developmental phenotypes do not establish an ongoing P16-P37/P44 thalamic maintenance program. Training perturbations that better match the developmental-TF/bHLH side of Twist1 were zero or near zero in this cell class despite adequate recovered-cell counts, while the only large selected TF responses were Wnt/TCF-specific thalamic programs with no close Twist1 support.

I therefore forecast no BH-significant focal-class genes for held-out `Twist1`.
