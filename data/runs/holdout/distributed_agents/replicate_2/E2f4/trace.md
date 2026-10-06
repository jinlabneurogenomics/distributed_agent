# Reasoning trace

## Question and scope

The held-out readout to predict is `n_degs`: the number of measured genes in
`151 TH Prkcd Grin2c Glut` with Benjamini-Hochberg adjusted Wilcoxon
`pvals_adj < 0.05` after one acute AAV-CRISPR loss-of-function perturbation.
The requested manifest for this run contains exactly one held-out perturbation,
`E2f4`, so the final table has one row and preserves that spelling.

One typo-like ambiguity in the prompt is that the focal group is consistently
`151 TH Prkcd Grin2c Glut`; I used that label from the task and the focal
training-count filename.

## Sources used

- Requested target list: `064_E2f4.csv`; it contains only `E2f4`.
- Focal training endpoints:
  `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Full non-held-out DE table:
  `training_de_all_cell_groups.parquet`.
- Distributed Agents corpus MCP release
  `perturbai-july-260713-sourceguard-1773-v1`, especially its bottom-up claims
  and findings for `E2f1`, `E2f5`, `Tfdp1`, and `Tfdp2`.
- External literature found through NCBI PubMed:
  - Litovchick et al., 2007, Mol. Cell, DOI `10.1016/j.molcel.2007.04.015`,
    PMID `17531812`: identified the quiescent p130/RBL2-E2F4-DP-MuvB DREAM
    complex and its repression of E2F cell-cycle targets.
  - Sadasivam, Duan and DeCaprio, 2012, Genes Dev.,
    DOI `10.1101/gad.181933.111`, PMID `22391450`: showed that MuvB forms
    DREAM with p130, E2F4, and DP1 in quiescence and switches to B-Myb/FOXM1
    complexes for late cell-cycle gene expression.
  - Buck et al., 1995, Oncogene, PMID `7542760`: characterized E2F5 as an
    E2F4-like DP-binding E2F subfamily member.
  - Lindeman et al., 1998, Genes Dev., DOI `10.1101/gad.12.8.1092`,
    PMID `9553039`: showed that germline `E2f5` loss causes a choroid-plexus
    hydrocephalus phenotype rather than a generic proliferation failure.

## Computation over the supplied data

I first loaded the focal training-count CSV to calibrate response breadth. It is
zero-inflated: 469 of 1,674 training targets had any DEG at FDR 0.05, the
median and 75th percentile were 0 and 1 DEG, and the 90th percentile was 2
DEGs. A one- or two-gene call is therefore already a small but real responder in
this assay.

For the DE parquet, I inspected row-group metadata and found that the focal
population occupies row groups 547 through 580. I then read those focal row
groups and filtered to E2F/DP and nearby cell-cycle regulators. For each
training perturbation below I counted rows with `pvals_adj < 0.05` and checked
its top focal DE rows:

| training perturbation | focal `n_degs` | focal expression-pattern evidence |
| --- | ---: | --- |
| `E2f1` | 0 | 17,259 measured rows, no FDR 0.05 genes; all leading nominal genes had `pvals_adj = 1`, and `Cntrob`/`Dcaf15` did not move. |
| `E2f5` | 0 | 17,259 measured rows, no FDR 0.05 genes; the top nominal genes again corrected to `pvals_adj = 1`. |
| `Tfdp1` | 2 | exactly two focal FDR 0.05 hits, `Cntrob` up (`log2FC = 0.663`, `pvals_adj = 0.0114`) and `Dcaf15` up (`log2FC = 0.534`, `pvals_adj = 0.0346`). The next row, `Trrap`, was already nonsignificant (`pvals_adj = 0.118`). |
| `Tfdp2` | 0 | 17,259 measured rows, no FDR 0.05 genes; all leading nominal genes had `pvals_adj = 1`. |
| `Myc` | 0 | no broad growth or ribosome-biogenesis response in the focal group. |
| `Mycn` | 0 | no focal FDR 0.05 response. |
| `Cdkn2a` | 0 | no derepressed RB/E2F-like cell-cycle surface in the focal group. |
| `Trp53` | 0 | no focal apoptosis or cell-cycle arrest response. |

The closest untested genes in the direct DREAM complex were not available as
training perturbations in this focal count table: `Rb1`, `Rbl1`, `Rbl2`,
`Rbbp4`, `Lin9`, `Lin37`, `Lin52`, `Lin54`, `Mybl2`, and `Foxm1` were absent.
`E2f2`, `E2f3`, `E2f6`, `E2f7`, and `E2f8` were also absent as perturbation
targets.

I therefore performed one targeted expression-pattern check rather than relying
only on DEG totals: under `E2f1`, `E2f5`, `Tfdp1`, and `Tfdp2`, a canonical
G1/S and mitotic panel containing `Pcna`, `Mcm2`-`Mcm7`, `Cdc6`, `Cdc20`,
`Cdc25a`, `Ccna2`, `Ccnb1`, `Ccnb2`, `Ccne1`, `Ccne2`, `Rrm1`, `Rrm2`,
`Tyms`, `Pola1`, `Top2a`, `Plk1`, `Foxm1`, and `Mybl2` remained fully
FDR-null in `151 TH Prkcd Grin2c Glut`; the minimum adjusted p-value across
that panel was 1.0 for all four E2F/DP perturbations. Thus even `Tfdp1`'s
two-gene response was not an E2F cell-cycle program.

## Target-specific reasoning

### E2f4

**Biological role.** `E2f4` encodes a repressive pocket-protein-associated E2F
factor. In quiescent cycling cells it can bind DP proteins and the RBL2/p130
plus MuvB DREAM complex to repress hundreds of G1/S and mitotic genes
(Litovchick et al. 2007; Sadasivam et al. 2012). A naive cell-culture transfer
would therefore allow nonzero or even broad derepression after `E2f4` loss.

**Directly relevant training perturbations.**

`E2f5` is the closest represented E2F paralog and was a focal zero. Its
Distributed Agents corpus findings report no corrected downstream response in any of the
measured NeuN-enriched neuronal groups and specifically no derepression of the
canonical E2F/DREAM G1/S genes after `E2f5` perturbation. This is an
appropriate analog for the repressive E2F4/E2F5 side of the family, and it is a
stronger comparator than unrelated high-DE transcription factors because its
expected targets are exactly the genes that would have revealed DREAM
de-repression.

`Tfdp1` and `Tfdp2` encode the assayed DP partners needed by classical E2F DNA
binding. `Tfdp2` was a focal zero. `Tfdp1` was the only E2F/DP member with a
focal signal, but it produced only `Cntrob` and `Dcaf15`, not MCM, PCNA, CDC,
RRM, cyclin, B-Myb, or FOXM1 genes. The Distributed Agents corpus claim
`claim:e16a32bdeefb0be7da9d` summarizes the same cross-perturbation evidence:
single perturbations of represented E2F/DP family members did not engage a
coordinated canonical G1/S, replication, mitotic, or apoptotic nuclear
transcriptomic program in settled postnatal neurons.

`E2f1` is the represented activating E2F counterexample. It was also a focal
zero, and the corpus records that its loss did not move canonical E2F
DNA-replication, mitotic, or apoptotic genes across broad neuronal groups. That
argues that the pathway is not merely missing one repressor; the larger
E2F-dependent cycling axis is quiet in this P16 to P37-44 NeuN-positive assay.

`Myc`, `Mycn`, `Mnt`, `Mlxip`, `Cdkn2a`, and `Trp53` were additional
counterexamples rather than pooled analogs. They sit near proliferative,
growth, RB/E2F, MYC/MAX, or stress-apoptosis circuits but were flat in the
focal group (`Myc`, `Mycn`, `Mnt`, `Mlxip`, `Cdkn2a`, `Trp53` all at 0 DEGs).
`Mga` had only 2 DEGs and reflects an MGA/PRC1.6 surface rather than E2F4-DREAM
biology, so I did not transfer its count upward to `E2f4`.

**Zero/nonzero decision.** I predict a true zero. The direct DREAM core was not
itself in the perturbation universe, so `E2f4` is an extrapolation, but every
available same-family or DP-partner perturbation in the dataset points to
buffering or pathway inactivity in the focal postmitotic thalamic glutamatergic
neurons. The single nonzero same-neighborhood count, `Tfdp1 = 2`, is a
noncanonical two-gene idiosyncratic response absent from `E2f1`, `E2f5`, and
`Tfdp2`, so it is a poor reason to force `E2f4` above zero.

**Predicted count.** `0`.

## Limits of the reasoning

`E2f4` itself was held out and absent from the Distributed Agents target graph, so the
prediction is a transfer from neighboring perturbations rather than a
signature-match to `E2f4`. The most direct DREAM components, Rb-family pocket
proteins and MuvB subunits, were not perturbation targets, and this screen did
not assay double `E2f4`/`E2f5` or DP-combinatorial loss. The AAV-CRISPR design
measures surviving postnatal neuronal nuclei 3 to 4 weeks after sparse
perturbation and did not validate DNA indels or protein depletion per target.
Finally, snRNA-seq DEG counts are a thresholded, power-dependent endpoint; a
zero prediction only means no measured transcript is expected to pass
FDR 0.05 in `151 TH Prkcd Grin2c Glut`, not that E2F4 protein is irrelevant in
all neuronal, glial, developmental, damage, or proliferative contexts.
