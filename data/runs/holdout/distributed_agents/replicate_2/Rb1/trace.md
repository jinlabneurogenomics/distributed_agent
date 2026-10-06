# Prediction trace

## Question and resolved ambiguities

The held-out manifest for this run contains one target, `Rb1`. I interpreted the
task as a point prediction of `n_degs` for `Rb1` loss in `151 TH Prkcd Grin2c
Glut`, where `n_degs` is the number of measured genes with Wilcoxon
Benjamini-Hochberg adjusted `pvals_adj < 0.05` in the perturbed-vs-control
comparison. `Rb1` itself is absent from the training-count CSV and from the
Parquet `gene_target` universe, so no direct `Rb1` signature or count was used.

Two ambiguities matter biologically.

- `Rb1` loss should derepress activator E2F transcription through the
  CDK-RB-E2F axis in cycling cells, but the assay is acute, sparse,
  postnatal, NeuN-enriched neuronal CRISPR rather than embryonic progenitors,
  germline deletion, tumor cells, or DNA-damage/toxin challenge.
- A zero prediction means "no transcript passes FDR 0.05 in this powered
  snRNA-seq endpoint", not "RB1 has no neuronal biology".

## Sources

- Input DE statistics:
  `[local file: training_de_all_cell_groups.parquet]`
- Input training endpoint:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- Requested-target manifest:
  `[local file: 195_Rb1.csv]`
- Internal same-experiment knowledge layer: Distributed Agents corpus release
  `perturbai-july-260713-sourceguard-1773-v1`, especially the E2F/DP-family
  claim `claim:e16a32bdeefb0be7da9d` and its `E2f1`, `E2f5`, `Tfdp1`, and
  `Tfdp2` findings.
- External literature on RB/E2F and postmitotic neurons:
  Attwooll et al. 2004, PMID 15538380; Ren et al. 2002,
  DOI 10.1101/gad.949802 / PMID 11799067; Sadasivam and DeCaprio 2013,
  DOI 10.1038/nrc3558 / PMID 23842645; Fischer and Muller 2017,
  DOI 10.1080/10409238.2017.1360836; Gaubatz et al. 2000, PMID 11030352;
  Hou et al. 2000, DOI 10.1046/j.1471-4159.2000.0750091.x / PMID 10854251;
  Saavedra et al. 2002, PMID 12065245; Hoglinger et al. 2007,
  DOI 10.1073/pnas.0611671104 / PMID 17360686; Wirt et al. 2010,
  DOI 10.1083/jcb.201003048 / PMID 21059851.

## Computation over the training data

The Parquet file is sorted by `group_name`; its metadata placed
`151 TH Prkcd Grin2c Glut` in row groups 546-580. I streamed only those row
groups, filtered exactly to `group_name == "151 TH Prkcd Grin2c Glut"`, and
materialized:

- all rows with `pvals_adj < 0.05`, to recover the focal DEG sets;
- complete focal signatures for the mechanistic comparator targets
  `E2f1`, `E2f5`, `Tfdp1`, `Tfdp2`, `Myc`, `Mycn`, `Mnt`, `Mlxip`, `Mga`,
  `Trp53`, `Cdkn2a`, `Rb1cc1`, and nearby cell-cycle or chromatin targets that
  existed in training.

Counting significant rows by `gene_target` reproduced the supplied training CSV
with zero mismatches. The 1,674 training targets in this focal group are sparse:
1,205 had no DEG, the median was 0, the 75th percentile was 1, the 95th
percentile was 18, and only 15 targets exceeded 500 DEGs.

I also computed Pearson and Spearman correlations of Wilcoxon `scores` across
the 17,259 measured genes for the RB/E2F/MYC/TRP53 comparator set. The
immediate E2F/DP surfaces were essentially uncorrelated in this focal group:
`E2f1` vs `E2f5` Pearson 0.028, `E2f1` vs `Tfdp1` 0.004, `E2f1` vs `Tfdp2`
0.031, `E2f5` vs `Tfdp1` 0.050, `E2f5` vs `Tfdp2` -0.006, and `Tfdp1` vs
`Tfdp2` 0.064. The same near-zero pattern held against `Myc`, `Mycn`, `Mnt`,
`Mlxip`, `Mga`, `Trp53`, and `Cdkn2a`.

## Target-specific reasoning for Rb1

RB1 is a pocket protein that restrains E2F-dependent G1/S transcription; loss of
RB function in dividing cells can induce DNA-replication, mitotic, and
apoptotic programs through E2F activators and through the DREAM/RB-E2F network
(Ren et al. 2002; Attwooll et al. 2004; Sadasivam and DeCaprio 2013; Fischer
and Muller 2017). Forced E2F1 is sufficient to kill cultured postmitotic
neurons, and Rb/E2F signaling participates in several stressed-neuron death
paradigms (Hou et al. 2000; Hoglinger et al. 2007). Embryonic `Rb`-deficient
CNS phenotypes depend strongly on E2F1/E2F3 (Saavedra et al. 2002).

Those external facts make RB1 a plausible positive-control node in cycling
lineages or stress, but the training data argue that the pathway is not easily
activated at the mRNA level by one acute sparse perturbation in the P16-P37/44
postmitotic neuronal assay:

| training target | 151 TH `n_degs` | why it is relevant to `Rb1` | 151 TH expression evidence |
| --- | ---: | --- | --- |
| `E2f1` | 0 | Direct activator E2F downstream of RB; an E2F1-dependent program is the most expected consequence of losing RB repression. | No gene reached FDR 0.05. All queried RB/E2F, MCM, PCNA, cyclin-E/A, RRM, POLA1, MYBL2, and apoptosis markers had adjusted P = 1.0 in this focal signature. Distributed Agents also reports `E2f1` as FDR-null at FDR 0.10 in 23/23 assayed neuronal groups. |
| `E2f5` | 0 | Repressive E2F that works with pocket-protein/DREAM quiescence machinery; loss could expose an E2F/DREAM derepression state if that circuit were RNA-active here. | No 151 TH DEGs. The Distributed Agents E2F5 finding found 0/286 E2F/cell-cycle marker tests at FDR 0.10 across 22 neuronal groups. |
| `Tfdp1` | 2 | DP1 is the obligate E2F dimerization partner most directly represented in training. | The only 151 TH hits were `Cntrob` logFC 0.663, FDR 0.011 and `Dcaf15` logFC 0.534, FDR 0.035. The 21 tested E2F/G1-S markers were all FDR 1.0, so the two hits are not an S-phase or apoptotic module. |
| `Tfdp2` | 0 | DP2 is the paralogous E2F dimerization partner. | No 151 TH DEGs and no G1/S or E2F-family marker at FDR 0.10 in the Distributed Agents aggregate over 21 neuronal groups. |
| `Cdkn2a` | 0 | Upstream CDK4/6-RB and ARF-p53 tumor-suppressor node. | No 151 TH DEGs; the strongest 151 TH adjusted P was 0.539. It did not derepress an RB/E2F or p53-effector state. |
| `Trp53` | 0 | Candidate apoptosis relay if Rb/E2F stress activates p53-family death responses. | No 151 TH DEGs; `Bax`, `Apaf1`, `Casp3`, and `Cdkn1a` were not corrected hits. |
| `Myc`, `Mycn`, `Mnt`, `Mlxip`, `Mga` | 0, 0, 0, 0, 2 | MYC/MAX and E2F-side growth regulators are cell-cycle-adjacent counterexamples. | `Myc`, `Mycn`, `Mnt`, and `Mlxip` were zero-DEG in 151 TH. `Mga` had two large positive hits, `Obscn` and `Stag3`, but no overlap with E2F, DP, MYC, or p53 outputs, and the Distributed Agents corpus reports no shared MAX/MYC/E2F FDR signature. |
| `Atr`, `Pola1` | 0, 0 | Replication-fork and DNA-polymerase nodes that would become relevant if Rb loss were causing S-phase stress. | Both were flat in 151 TH. |
| `Sin3a` | 1433 | Boundary case: SIN3/HDAC can be recruited by RB-family repressors, but `Sin3a` is a broad chromatin corepressor. | Its massive 1,433-gene 151 TH signature is not an E2F-specific signature and is not a good point estimate for `Rb1`. |
| `Rb1cc1` | 4 | Name-based counterexample; `Rb1cc1/Fip200` is an autophagy gene, not the retinoblastoma pocket protein. | Its 151 TH hits were ER/proteostasis genes (`Calr`, `Hspa5`, `Pdia6`) plus its own transcript, matching the Distributed Agents autophagy module rather than RB/E2F biology. |

Distributed Agents graph expansion from the represented E2F/DP nodes against the 1,674
eligible training targets returned only `Fbxo11` as a recurring extra
candidate. I rejected it: the two inbound paths were explicitly weak
"no robust convergence" or "no strong global convergence" neighbor findings
from near-null E2F/DP signatures, not biological RB/E2F evidence.

The zero/nonzero decision is therefore driven primarily by within-dataset
evidence. The most direct measurable nodes on either side of RB/E2F - the
activator `E2f1`, the DP cofactors `Tfdp1` and `Tfdp2`, the repressive pocket
partner `E2f5`, upstream `Cdkn2a`, and downstream/stress-side `Trp53` - all
lacked a coordinated G1/S, replication, mitotic, or apoptotic RNA response in
the focal cell group. The only nonzero direct-family endpoint, `Tfdp1`, was a
two-gene outlier with `Cntrob`/`Dcaf15` rather than a broad program. Because
single-node perturbations in this screen commonly produce zero DEGs, and
because even pathway nodes expected to be highly diagnostic of an E2F state
were flat, I predict that acute mosaic `Rb1` loss will not push any measured
gene past FDR 0.05 in `151 TH Prkcd Grin2c Glut`.

Final point prediction for `Rb1`: 0 DEGs.

## Limits

The comparison is imperfect because `Rbl1`, `Rbl2`, `E2f2`, `E2f3`, `E2f4`,
`E2f6`, DREAM/MuvB core subunits, `Cdk4`, `Cdk6`, and cyclin-D genes were not
represented as training perturbations in this focal readout. RB1 loss has the
opposite sign from loss of an activator E2F or DP cofactor, so the flat E2F/DP
loss signatures are evidence that the module is quiet or buffered, not a direct
phenocopy. The P16 AAV CRISPR platform has modest average target-RNA knockdown
and did not assay protein depletion or DNA indels. Stronger biallelic RB-family
loss, combined pocket-protein perturbation, embryonic progenitors, damaged or
toxin-stressed neurons, or NeuN-negative proliferative/choroid/ependymal
lineages could expose canonical RB/E2F biology that is absent from this
homeostatic juvenile neuronal endpoint.
