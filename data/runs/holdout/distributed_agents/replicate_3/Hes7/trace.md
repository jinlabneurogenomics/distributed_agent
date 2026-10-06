## Question interpreted

The requested held-out target list contains one gene, `Hes7`. I interpreted the task as a point prediction of the number of measured genes that would have `pvals_adj < 0.05` after acute sparse CRISPR loss of `Hes7` in `151 TH Prkcd Grin2c Glut` neurons, using only non-held-out Perturb-seq differential-expression data plus external biology.

Two ambiguities I resolved:

- A prediction of `0` means that no assayed transcript is expected to pass the screen's FDR 0.05 cutoff in this one focal cell group. It does not mean the gene has no biological role in its normal developmental tissue.
- Because direct `Hes7` DE rows were held out, I did not use any `Hes7` perturbation signature. `Hes7` was present only as a measured transcript in other perturbations, where it provided a negative readout of whether a Notch/HES module was active.

## Sources used

- `training_de_all_cell_groups.parquet`: per-gene Wilcoxon differential-expression statistics for non-held-out perturbations.
- `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`: observed `n_degs` for non-held-out perturbations in the focal cell group.
- `104_Hes7.csv`: the held-out manifest; it contains only `Hes7`.
- Distributed Agents corpus MCP, release `perturbai-july-260713-sourceguard-1773-v1`, for same-experiment claims around Dll1/Mib1/Tm2d1, Notch1/Notch2/Notch4, and Mesp2/Tbx6.
- Distributed Agents runtime profile-comparison tools, used to compare focal-cell expression profiles of hand-selected Notch and somitogenesis analogs.
- PubMed-indexed literature for `Hes7` biology:
  - Bessho et al. 2001, *Genes to Cells*, DOI `10.1046/j.1365-2443.2001.00409.x`, PMID `11260262`: identified mouse `Hes7` as a bHLH repressor under Notch control, dynamically and specifically expressed in presomitic mesoderm.
  - Bessho et al. 2001, *Genes & Development*, DOI `10.1101/gad.930601`, PMID `11641270`: `Hes7` null mice have disrupted somite segmentation and continuous `Lfng` expression.
  - Bessho et al. 2003, *Genes & Development*, DOI `10.1101/gad.1092303`, PMID `12783854`: periodic repression by HES7 controls cyclic `Hes7`/`Lfng` transcription.
  - Hayashi et al. 2018, *JBC*, DOI `10.1074/jbc.RA118.003728`, PMID `29895619`: presomitic-mesoderm-specific `Hes7` expression depends on E-box, T-box/Tbx6, and RBPJ/Notch inputs and is repressed by HES7.
  - Sparrow et al. 2008, *Human Molecular Genetics*, DOI `10.1093/hmg/ddn272`, PMID `18775957`: human HES7 is a bHLH-Orange Notch-pathway transcriptional repressor; loss-of-function mutations cause spondylocostal dysostosis.

## Computational checks

I first read `104_Hes7.csv` and confirmed that `Hes7` is the only requested target.

From the focal training-count CSV, direct Notch or HES-related training perturbations in `151 TH Prkcd Grin2c Glut` were sparse and inactive:

| training target | observed n_degs |
|---|---:|
| `Dll1` | 0 |
| `Hesx1` | 0 |
| `Notch1` | 0 |
| `Notch2` | 0 |
| `Notch4` | 0 |

No non-held-out `Hes1`, `Hes5`, `Hey1`, `Hey2`, `Heyl`, `Rbpj`, `Maml1`, `Lfng`, `Mfng`, or `Rfng` perturbation was present in the focal count table. I therefore expanded to upstream or developmental-context comparators:

| training target | reason for checking | observed n_degs |
|---|---|---:|
| `Adam10` | Notch receptor cleavage / APP-processing comparator | 0 |
| `Psen1` | gamma-secretase / Notch receptor cleavage comparator | 0 |
| `Mib1` | Notch-ligand E3 ligase; useful counterexample | 27 |
| `Tm2d1` | TM2D/gamma-secretase/Notch-related comparator | 1 |
| `Mesp2` | presomitic mesoderm segmentation-clock output | 1 |
| `Tbx6` | upstream T-box regulator of `Hes7` in PSM | 0 |
| `Fgf1`, `Fgf12`, `Fgfr1`, `Fgfr2`, `Fgfr3`, `Fgfrl1` | FGF-side somitogenesis signaling | all 0 |
| `Fgf13` | FGF-family, weak non-core counterexample | 2 |

I then filtered the parquet to `group_name = '151 TH Prkcd Grin2c Glut'` for selected analogs. This verified that the zero-count analogs were not hiding canonical Notch outputs just below threshold:

- `Dll1`, `Notch1`, `Notch2`, `Notch4`, `Adam10`, `Psen1`, `Hesx1`, and `Tbx6` each had 0 significant focal features at FDR 0.05.
- `Mesp2` had exactly 1 significant focal feature, `Arih2`, down at log2FC `-0.424`, `p_adj = 0.04496`.
- `Tm2d1` had exactly 1 significant focal feature, `R3hdm2`, up at log2FC `0.408`, `p_adj = 0.00207`.
- `Mib1` had 27 significant focal features; 26 were up-regulated and the leading hits were cholesterol/SREBF2 genes such as `Insig1`, `Fdft1`, `Dhcr24`, `Ldlr`, `Msmo1`, `Hmgcs1`, `Hmgcr`, `Cyp51`, `Lss`, and `Idi1`.

The Distributed Agents runtime profile comparison of

`Dll1, Notch1, Notch2, Notch4, Hesx1, Mesp2, Tbx6, Mib1, Tm2d1, Adam10, Psen1`

in the focal cell group reported 8 of 11 nodes with no significant features, two nodes with only 1 to 9 significant features, and only `Mib1` in the 10 to 49 feature bin. Pairwise significant-feature intersections between `Mesp2`, `Tm2d1`, or `Mib1` and the Notch receptor/ligand/protease nodes were zero. This supports the qualitative interpretation that the one broad counterexample, `Mib1`, is not a Notch-effector or segmentation-clock state.

As measured output genes, canonical HES/HEY/segmentation-clock transcripts were also quiescent across all 1,674 non-held-out focal perturbations:

| measured transcript in focal DE table | minimum adjusted p-value across training perturbations |
|---|---:|
| `Hes1` | 0.358 |
| `Hes5` | 1.000 |
| `Hes7` | 1.000 |
| `Hey1` | 0.063 |
| `Hey2` | 0.516 |
| `Heyl` | 1.000 |
| `Lfng` | 1.000 |
| `Mesp2` | 1.000 |
| `Notch1` | 1.000 |
| `Notch2` | 1.000 |
| `Notch3` | 1.000 |
| `Dll1` | 0.894 |
| `Tbx6` | 0.430 |

## Target-specific reasoning

### `Hes7`

External biology places `Hes7` in a very specific embryonic presomitic-mesoderm program. It is a bHLH/WRPW transcriptional repressor induced by Notch-pathway input in the PSM, represses its own promoter and `Lfng`, and must turn over rapidly to sustain the segmentation clock that creates somites (Bessho et al. 2001, DOI `10.1046/j.1365-2443.2001.00409.x`; Bessho et al. 2001, DOI `10.1101/gad.930601`; Bessho et al. 2003, DOI `10.1101/gad.1092303`). Its upstream cis-regulatory logic uses PSM inputs from Tbx6, E-box factors, and RBPJ/Notch rather than a general postmitotic neuronal enhancer state (Hayashi et al. 2018, DOI `10.1074/jbc.RA118.003728`). Human recessive HES7 mutations disturb axial skeletal segmentation, again pointing to the same developmental compartment rather than to a juvenile thalamic neuronal transcriptome (Sparrow et al. 2008, DOI `10.1093/hmg/ddn272`).

The in-dataset analogs point the same way:

- `Dll1`, `Notch1`, `Notch2`, and `Notch4` are the most direct represented Notch ligand/receptor comparators. All had `0` observed DEGs in the focal cell group. The Distributed Agents corpus further summarizes the same-experiment evidence as: Dll1 was transcriptionally silent across 23 recovered neuronal groups; the canonical NICD/RBPJ/MAML program was not recovered for Notch1; Notch2 was flat across all 23 groups; and the Notch2/Notch4 surfaces lacked HES/HEY output.
- `Adam10` and `Psen1`, receptor-cleavage comparators for Notch signaling, also had `0` focal DEGs.
- `Hesx1` had `0` focal DEGs. It is not a true segmentation-clock paralog, but it is a developmental transcriptional repressor with HES-family naming and gave no support for a hidden HES-like response.
- `Mesp2` and `Tbx6` are closer to the embryonic PSM setting of `Hes7` than to neuronal Notch signaling. `Tbx6` had `0` focal DEGs; `Mesp2` had a single weak hit, `Arih2`, and did not move `Hes7`, `Lfng`, or Notch outputs. The Distributed Agents corpus claim `claim:23535ec03029dd5f870d` explicitly summarizes the Mesp2/Tbx6 evidence as a failure to engage the embryonic somitogenesis/Notch segmentation-clock program in postnatal neurons.
- `Mib1` had 27 focal DEGs, but it is a counterexample rather than a positive analog for `Hes7`: its response was dominated by SREBF2-like sterol/cholesterol biosynthesis genes and had no significant-feature overlap with the single-feature `Mesp2` or `Tm2d1` responses in the runtime comparison. Distributed Agents corpus claims `claim:db038dadc7590ad86758`, `claim:c95cd15bd33f161f05e7`, and `claim:30e9ce321c991e10e477` also distinguish the recurrent `Mib1` sterol state from canonical Dll1/Notch/HES/HEY transcription.
- `Tm2d1` had only one focal DEG, `R3hdm2`, so even a Notch-related processing factor that is not simply silent did not create a broad pathway state.

Because `Hes7` itself is a downstream PSM clock effector, I would expect its loss in P37-P44 `151 TH Prkcd Grin2c Glut` neurons to be at least as buffered as perturbing Notch receptors or `Tbx6`, not to phenocopy the off-pathway `Mib1` sterol response. The focal-cell data also show that `Hes7` mRNA was inert as a measured transcript under every training perturbation (`min p_adj = 1.0`), which is consistent with absent or extremely low expression of the HES7 clock in this cell state. My point prediction is therefore `0`.

## Limits

The held-out target has no direct in-dataset perturbation signature, and the training set lacks the closest possible paralog perturbations, `Hes1` and `Hes5`; the prediction necessarily extrapolates from upstream Notch receptors/ligand, Notch-processing relatives, and the embryonic PSM regulators `Mesp2` and `Tbx6`. Those are mechanistically informative but not equivalent to direct removal of a downstream bHLH repressor. The focal screen is also a mosaic, moderate-knockdown, single-timepoint snRNA-seq assay, so it would miss protein-only effects, subtle oscillatory dynamics, or an effect confined to rare unmodeled progenitor/non-neuronal cells. Within those constraints, the within-dataset evidence and the external developmental biology both argue for no FDR 0.05 response in the assayed thalamic glutamatergic nuclei.
