# Ap2s1 DEG-count forecast

## Target and endpoint

- Target: `Ap2s1`.
- Focal class: `151 TH Prkcd Grin2c Glut`.
- Endpoint: `n_degs`, the count of measured genes with BH-adjusted Wilcoxon `p < 0.05`.
- Declared quantitative training table: `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`, 1,674 perturbations, excluding `Ap2s1`.
- Declared profile table: `training_de_all_cell_groups.parquet`, filtered to `group_name == "151 TH Prkcd Grin2c Glut"`.
- Declared target biology bundle: `Ap2s1.json`, checksum `b050740f36cbc0984347a05e1bfee962de358185c896af23386fab9708ac4fd4`.

I used no Ap2s1 differential-expression signature, no Ap2s1 DEG count, and no Ap2s1 same-experiment corpus Findings. Same-experiment corpus records below were used only for measured training perturbations and treated as interpretations of the same PerturbAI atlas, not as independent validation.

## Biology that moved the estimate

The canonical biology bundle argues that the perturbation should be functionally realized by harvest but should not be assumed to create a large survivor-cell transcriptome:

- AP2S1 is the sole sigma subunit of the heterotetrameric AP-2 clathrin adaptor, with AP-2 acting in clathrin-dependent cargo capture and synaptic-vesicle membrane recycling.
- The exact in-assay reach is moderate: in matched non-target 151 TH nuclei, `Ap2s1` is detected in 13,203 of 23,679 nuclei, or 55.76%, with mean log1p CP10K 0.367.
- The functional-stock card calls harvest-time AP-2 sigma-dependent capacity `likely_substantially_depleted`: a P16 disruptive edit should stop AP2S1 resupply, and the 21-28 day interval exceeds a roughly 9 day whole-brain protein lifetime proxy plus a days-scale same-complex AP-2 neuronal failure anchor.
- The strongest neural phenotype evidence is not direct Ap2s1 loss. It comes from conditional Ap2m1 loss in mouse neurons, which supports AP-2 demand in postnatal thalamic neurons but does not quantify a P16 Ap2s1 151 TH nuclear-RNA effect.
- The bundle explicitly leaves same-context compensation and Ap2s1-specific protein kinetics unresolved, and marks survivor conditioning as a possible attenuator of the observed RNA signature.

Net effect: the target is plausibly engaged in about half of this class, and loss of the sole AP-2 sigma subunit is not a biological null; however, the evidence supports a low to modest acute snRNA-seq response rather than a guaranteed high-DEG stress state.

## Training counts used as scalar anchors

The training endpoint distribution in 151 TH is very sparse: median 0, mean 14.1, 1,205/1,674 perturbations at zero, 337 at 1-4, 52 at 5-19, 37 at 20-99, and 43 at >=100. The high tail is driven by broad nuclear/proteostasis/transcriptional regulators such as `Uba5` 2677, `Tpr` 1768, `Sin3a` 1433, `Psmb4` 742, and `Rab7` 501, not by generic vesicle coat perturbations.

The most relevant measured AP/adaptor, clathrin, dynamin, synaptojanin, and adjacent endocytic rows were:

| Training perturbation | 151 TH `n_degs` |
| --- | ---: |
| `Ap1b1` | 1 |
| `Ap1s2` | 0 |
| `Ap3b1` | 0 |
| `Ap4s1` | 0 |
| `Bin1` | 1 |
| `Cltc` | 3 |
| `Dnm1` | 1 |
| `Synj1` | 1 |
| `Atp6v0a1` | 1 |
| `Atp6v1a` | 0 |
| `Atp6v1b2` | 0 |
| `Atp6v1e1` | 0 |
| `Rab18` | 0 |
| `Rab27a` | 0 |
| `Rab3gap1` | 0 |
| `Rab3gap2` | 0 |
| `Vps35l` | 0 |
| `Vps41` | 0 |
| `Vps53` | 0 |

Endolysosomal and Golgi trafficking gave bounded higher examples but with less proximal biology:

| Training perturbation | 151 TH `n_degs` |
| --- | ---: |
| `Vps35` | 17 |
| `Vps54` | 31 |
| `Rab7` | 501 |

## Profile and corpus checks on those anchors

I ran `dataset.candidate_profile_review.profile_compare` on the focal Parquet rows for the 22 trafficking candidates above. The profile-comparison receipt reported 13 nodes with no significant features, 6 with 1-9, 2 with 10-49, and 1 with at least 50. `profile_inspect` confirmed that the immediate AP-2-adjacent nodes were tiny at the FDR<0.05 endpoint: `Bin1` 1, `Cltc` 3, `Dnm1` 1, `Synj1` 1, all with only negative significant genes in this class. `Vps35` and `Vps54` were modest mixed signatures, and `Rab7` was qualitatively different at 501 DEGs.

The selected same-experiment corpus release gave the same qualitative boundary:

- `Cltc` Claim `claim:491c5c6eb002662cbefd` states that core `Cltc` perturbation produced a restricted nuclear transcriptional response that was not phenocopied by represented adaptor-tier, `Dnm1`, `Synj1`, `Bin1`-like, or presynaptic/endocytic neighbors.
- `Cltc:F001` and linked Findings describe multi-class Cltc activity, but the 151 TH count itself remained only 3 at the requested FDR<0.05 threshold.
- `Rab7:F002`/`Rab7:F003` describe late-endosomal/lysosomal and sterol compensation, explaining why `Rab7` is a high-count outlier rather than an AP-2-magnitude donor.
- `Vps35:F004` explicitly separates the sparse Vps35 retromer signature from the larger Rab7 lysosome/proteasome program.
- `Vps54:F004` reports that `Vps54` lacked the UPR/ISR, proteasome, lysosomal-hydrolase, and sphingolipid induction expected from a severe generic trafficking collapse.

Together these records argue against scaling `Ap2s1` to the hundreds-DEG `Rab7` state. They also argue against automatically copying the 17-31 DEG `Vps35`/`Vps54` retromer/GARP branches, because AP-2 is a clathrin plasma-membrane adaptor and the observed same-assay clathrin/endocytic rows remain at 1-3.

## Forecast

I set the point estimate at **3**.

That value is the high end of the directly adjacent `Bin1`/`Cltc`/`Dnm1`/`Synj1` group and above the zero-heavy AP-family rows, reflecting that `Ap2s1` has exact 151 TH expression and is the sole AP-2 sigma subunit with likely harvest-time stock depletion. I did not move the estimate into the tens because represented adaptor-family perturbations were mostly 0-1, core `Cltc` itself was only 3 in this exact focal class, and the larger `Vps35`, `Vps54`, and especially `Rab7` states map to later endosomal/Golgi or lysosomal compensation programs rather than to AP-2 loss.
