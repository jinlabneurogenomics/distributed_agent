# Q3 literature specificity methods

## Eligibility and output scope

I used the manifest targets `Psmb4, Tpr, Ppp2r1a, Prpf6, Zbtb7a, Pomp, Ap2s1, Yy1, Snrnp70, Eef2` as the complete output scope and did not add rows for perturbations outside the sidecar. Eligibility was computed as:

```sql
gene_target IN manifest
AND group_name IN allowed_cell_groups
AND pvals_adj < 0.10
AND lower(names) != lower(gene_target)
```

Grouping that filtered table by `(gene_target, group_name)` gave 147 eligible pairs: Ap2s1 11, Eef2 14, Pomp 7, Ppp2r1a 22, Prpf6 11, Psmb4 18, Snrnp70 12, Tpr 12, Yy1 18, and Zbtb7a 22. The JSONL output emits exactly those 147 pairs and each pair has one data-derived evidence record.

## Phenotype characterization

For each eligible pair I sorted downstream genes by `pvals_adj`, counted significant up- and down-regulated genes, retained the matched perturbed/control nucleus counts, and used the top FDR-ranked genes plus recurrent genes across pairs from the same target to define the central module. Singletons and pairs with only a few significant genes were assessed on those observed genes directly. Target-transcript rows were not used to establish eligibility or to assign literature agreement.

`Psmb4` and `Pomp` were dominated by broad mixed proteostasis/stress and synaptic-neuronal programs in large neuronal pairs; `Tpr`, `Prpf6`, and `Snrnp70` showed RNA-processing/nuclear and synaptic modules; `Ap2s1` repeatedly involved endocytic/synaptic genes and `Tfrc`; `Eef2` mixed synaptic genes such as `Vgf` or `Syt4` with nuclear or idiosyncratic singletons; `Ppp2r1a`, `Yy1`, and `Zbtb7a` had reproducible but target-specific transcriptional modules centered on genes such as `Kifc2/Pabpn1/Rsrp1`, `Wsb1/Leng8/Drosha`, and `Gpc1/Pnma3/Atp1b2`.

## Literature searches and flag rules

I searched PubMed for each target by official symbol, common protein or complex name, and the dominant measured genes or modules. Queries included terms such as `POMP proteasome maturation protein knockdown`, `Psmb4 POMP proteasome IFN`, `TPR nucleoporin mRNA export splicing intron retention`, `PRPF6 spliceosome tri-snRNP splicing`, `SNRNP70 U1-70K knockdown splicing`, `adaptor protein complex 2 transferrin receptor internalization`, `Eef2 knockdown neuron`, and exact no-hit module searches such as `ZBTB7A GPC1 PNMA3 ATP1B2 PNCK neurons` and `PPP2R1A KIFC2 PABPN1 RSRP1 AMY1 JUN neurons transcriptome`. I reviewed roughly one to ten returned titles/abstracts for each positive mechanistic query and repeated exact target-plus-observed-gene searches for singleton or low-count pairs assigned `No Literature`.

`Inferred` was used when the literature made a target-specific or complex-level biological connection but stopped before the exact RNA direction measured in this acute mouse Perturb-seq assay. This applied to proteasome insufficiency for `Psmb4`/`Pomp`, AP-2-dependent transferrin uptake for most `Ap2s1` pairs, spliceosome or U1-snRNP biology for RNA-processing `Prpf6` and `Snrnp70` pairs, Tpr-dependent intron-retaining RNA surveillance for most `Tpr` pairs, and Eef2-dependent neuronal translation/synaptic phenotypes for Eef2 pairs with synaptic or peptide-response genes. Context labels record species, cell-type, modality, or mechanistic-indirect transfer when the cited work used human cells, non-neuronal cells, siRNA, inherited disease, or protein-trafficking/splicing assays rather than CRISPR snRNA-seq.

`No Literature` was used only after searching the target with the measured module and finding no biologically specific bridge. This included all `Ppp2r1a`, `Yy1`, and `Zbtb7a` pairs: each target has extensive signaling or transcription-factor literature, but I did not find direct links to the observed `Kifc2/Pabpn1/Rsrp1/Amy1`, `Wsb1/Leng8/Drosha`, or `Gpc1/Pnma3/Atp1b2/Pnck` modules. It also included low-count pairs such as `Ap2s1` in L5 ET, `Pomp` in CNU-MGE, `Psmb4` in CNU-LGE, `Tpr` in L2/3 ENT and CNU-MGE, and `Snrnp70` in L5/6 IT and CNU-MGE where the significant genes were not part of the target-supported machinery response.

## Multi-module reduction and difficult pairs

For large pairs with several FDR-supported modules I assigned the row on the best target-to-module bridge and stated when the cited bridge did not cover materially different synaptic, stress, or RNA-processing modules. The broadest reductions were the proteasome targets, where published PSMB4/POMP loss predicts proteasome insufficiency and inflammatory or UPR programs but not the mixed direction of thousands of neuronal transcripts, and the Tpr/Prpf6/Snrnp70 spliceosome/nuclear-pore targets, where the literature predicts RNA-processing disruption but not the specific postmitotic neuronal gene set. No eligible pair was left incompletely searched; total eligible = 147, emitted = 147, incompletely reviewed = 0.
