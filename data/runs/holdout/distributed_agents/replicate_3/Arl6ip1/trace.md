## Question and resolved ambiguities

The requested held-out perturbation set contains one gene:

| target_name |
|---|
| Arl6ip1 |

For this target I predicted the number of genes in `151 TH Prkcd Grin2c Glut` whose Wilcoxon `pvals_adj` would be below 0.05 after the acute AAV CRISPR perturbation. I treated target self-repression as eligible for `n_degs`, because the training endpoint counts the perturbed transcript when it is significant: in this focal group `Atl1`, `Reep1`, `Reep2`, `Bcap31`, and `Ssr4` each had exactly one DEG and it was the target mRNA itself.

The main ambiguity is biological, not file format: `Arl6ip1` is an endoplasmic-reticulum membrane-shaping and ER-phagy gene with strong phenotypes in chronic organismal models, but this assay reads out nuclear RNA from surviving young postmitotic central neurons only 3 to 4 weeks after sparse mosaic CRISPR. I therefore asked whether an acute partial loss of an ER-shaping protein should create a broad cell-body ER-stress signature in this exact screen, rather than whether complete germline loss can damage long axons or sensory neurons.

## Sources

### Input data

- `training_de_all_cell_groups.parquet`: the focal cell group was filtered from the parquet and candidate training perturbations were inspected for per-gene `logfoldchanges`, `pvals_adj`, and matched perturbed/control nucleus counts.
- `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`: used as the endpoint for all non-held-out targets in the focal group.
- `016_Arl6ip1.csv`: supplied the one held-out target and its required output order.

The focal training count table has 1,674 perturbations, median `n_degs = 0`, 75th percentile 1, 95th percentile 18, and 469/1,674 nonzero entries. Thus a one-gene call is not a trivial value: it means the perturbation is expected to be detectable only at the target transcript or an equivalently tiny downstream trace.

### Internal same-experiment resources

I queried the Distributed Agents corpus release `perturbai-july-260713-sourceguard-1773-v1`.

- `Arl6ip1` itself had no frozen target context in the corpus.
- `Atl1`, `Reep1`, `Spast`, and `Vcp` did have target contexts. The most relevant shared claim was that "Represented ER-shaping, HSP, and long-axon transport perturbations do not form a shared acute neuronal nuclear transcriptomic module in this assay." The Atl1 and Reep1 findings specifically report that ER-shaping/HSP comparators such as `Atl3`, `Reep1`, `Reep2`, and `Spast` were transcriptionally buffered or nonconvergent in the same screen, and the `Vcp` findings show that even a ubiquitous ER/proteostasis segregase gave only a sparse, cell-type-restricted RNA response rather than a pan-neuronal UPR.

I also used the Distributed Agents runtime profile comparison over the run-local parquet. A cohort of mechanistic comparators was compared with `value_column = logfoldchanges`, `significance_column = pvals_adj`, and `group_name = "151 TH Prkcd Grin2c Glut"`. The inspected cohort was `Atl1`, `Atl3`, `Reep1`, `Reep2`, `Spast`, `Vcp`, `Hspa5`, `Bcap31`, and `Ssr4`.

### External literature

- Yamamoto et al. 2014 showed that ARL6IP1 has reticulon-like short hairpin transmembrane domains, binds atlastin, shapes high-curvature ER tubules, and can tubulate liposomes, making the atlastin/REEP/reticulon ER-shaping neighborhood the closest assayed biology. DOI 10.1042/BJ20131186, PMID 24262037.
- Foronda et al. 2023 found that ARL6IP1 interacts with FAM134B and participates in ubiquitin-dependent ER-phagy clusters; Arl6ip1-deficient mice showed expanded ER sheets in sensory neurons and impaired ER-phagy flux. DOI 10.1038/s41586-023-06090-9, PMID 37225994.
- Byrne et al. 2022 generated Drosophila and human-cell ARL6IP1 loss models, connected the gene to tubular ER organization and lipid homeostasis, and rescued Drosophila phenotypes with liver X receptor agonism. DOI 10.1186/s40478-022-01343-6, PMID 35346366.
- Fowler and O'Sullivan 2016 showed that Drosophila Arl6IP1 knockdown disrupts smooth ER and mitochondrial organization in distal long motor axons; Lim et al. 2023 connected ARL6IP1 at mitochondria-associated membranes to LC3B/BCL2L13 and autophagy/mitochondrial homeostasis in an HSP model. DOIs 10.1093/hmg/ddw139 and 10.1084/jem.20230367; PMIDs 27170313 and 37934410.
- Akiduki and Ikemoto 2008 reported direct binding between ARL6IP1 and ARL6IP5/addicsin and modulation of EAAC1-mediated glutamate transport, but `Arl6ip5` was not present in the training perturbation endpoint table. DOI 10.1074/jbc.M801570200, PMID 18684713.

## Computation over the input tables

I first summarized the 1,674 training `n_degs` values in the focal cell group to calibrate the endpoint. I then selected training genes with plausible ER-shaping, ER-translocon, ER-stress, ERAD/autophagy, and HSP/axonopathy relevance and joined their observed focal counts to the per-gene parquet rows.

The parquet has 616,253,184 rows, so I used Arrow filtering rather than materializing the whole file:

1. Filter rows to `group_name == "151 TH Prkcd Grin2c Glut"`.
2. Keep only the comparator `gene_target` values.
3. Count `pvals_adj < 0.05` per target.
4. Inspect the significant rows and the matched perturbed/control nucleus counts.

The profile comparison tested whether these low-count targets nevertheless had the same ranked expression pattern. It found 17,259 measured features for every inspected comparator in this cell group, but no overlap among their significant positive or negative gene sets. The whole-profile correlations among the near-null direct HSP/ER-shaping targets were moderate because most features are close to zero, so I treated the absence of recurrent FDR genes as the stronger expression-pattern evidence.

## Arl6ip1-specific analogs and counterexamples

### Direct ER-shaping and HSP-like comparators

| training perturbation | focal `n_degs` | matched perturbed nuclei | expression evidence | relevance to Arl6ip1 |
|---|---:|---:|---|---|
| `Atl1` | 1 | 138 | the only significant gene was `Atl1` itself, log2FC -0.494, FDR 0.00398 | ARL6IP1 binds atlastin and shapes ER tubules in a reticulon-like manner; `Atl1` is therefore a direct pathway comparator |
| `Atl3` | 0 | 82 | no significant genes | atlastin paralog; useful as a flat ER-fusion counterexample |
| `Reep1` | 1 | 123 | the only significant gene was `Reep1` itself, log2FC -0.771, FDR 3.2e-7 | HSP-associated tubular-ER shaping gene; close to the phenotype class invoked for ARL6IP1/SPG61 |
| `Reep2` | 1 | 169 | the only significant gene was `Reep2` itself, log2FC -0.634, FDR 2.4e-18 | REEP family ER-shaping comparator |
| `Spast` | 0 | 141 | no significant genes | canonical HSP/ER-endosome/microtubule severing gene; tests whether an axonopathy gene evokes the shared nuclear response that `Arl6ip1` might have joined |

These five are the most informative within-dataset anchors. Their 151-cell-group counts are 0 or 1, and the nonzero calls are self-transcript only. Distributed Agents corpus findings for `Atl1`, `Reep1`, and `Spast` also showed that the absence of downstream DE was a broader property of the represented ER-shaping/HSP neighborhood, not just a peculiarity of this one thalamic group. That argues strongly against giving `Arl6ip1` a many-gene stress or neurodegeneration signature in this endpoint.

### ER homeostasis and proteostasis boundaries

| training perturbation | focal `n_degs` | expression evidence | interpretation for Arl6ip1 |
|---|---:|---|---|
| `Hspa5` | 5 | included `Hsp90b1`, `Pdia4`, and `Derl3` up-regulation | BiP loss can evoke a small UPR/ERAD trace in this cell group; `Arl6ip1` should not simply be equated with chaperone depletion |
| `Sec63` | 11 | included `Hspa5`, `Rtn1`, `Canx`, `Hyou1`, and `Chac1` | translocon/protein-folding stress is visible when directly perturbed, but its count remains only low double digits |
| `Vcp` | 2 | `Rasgef1b` up and `Nsmf` down; no shared significant genes with the ER-shaping cohort | broad proteostasis/ERAD/autophagy adjacency alone gave a sparse response here |
| `Bcap31` | 1 | the only significant gene was `Bcap31` | ER membrane/apoptosis and VCP-linked literature are not sufficient for a downstream neuronal signature |
| `Ssr4` | 1 | the only significant gene was `Ssr4` | another ER-translocon membrane component with a target-only endpoint |
| `Uba5` | 2677 | broad UFMylation/proteostasis response | positive control showing this thalamic group can produce thousands of DEGs after an ER-quality-control perturbation |
| `Ufc1` | 572 | broad UFMylation/proteostasis response | another positive control showing that a strong ER-proteostasis state is recoverable |
| `Opa1` | 37 | ATF4/CHOP-associated genes including `Asns`, `Chac1`, and `Ddit3` | mitochondrial-organelle stress can give tens of DEGs; `Arl6ip1` is ER-mitochondria adjacent but its closest ER-shaping comparators are far weaker |

This boundary set is the main reason I did not call zero solely because most HSP genes are flat. The focal readout can detect ER/proteostasis stress when the lesion enters a canonical nuclear stress state (`Hspa5`, `Sec63`, `Uba5`, `Ufc1`) and can detect mitochondrial stress (`Opa1`). However, `Arl6ip1` is predicted to behave more like a structural ER-shaper than like a core UFMylation, proteasome, or chaperone perturbation under an acute partial neuronal knockout.

## Prediction

`Arl6ip1` should be nonzero but only barely so.

The external biology puts ARL6IP1 in the tubular ER/ER-phagy/HSP axis through atlastin binding, ER membrane shaping, interaction with FAM134B, and SPG61 models. The same-experiment evidence says that this axis is transcriptionally buffered in juvenile NeuN+ somata: `Atl1`, `Reep1`, and `Reep2` each contributed only self knockdown in `151 TH Prkcd Grin2c Glut`; `Atl3` and `Spast` were completely FDR-silent; and `Vcp`, despite much more general proteostasis roles, had only two FDR genes in the focal group.

I therefore expect the CRISPR perturbation of `Arl6ip1` to register if its own transcript is measured and depleted, but I do not expect a multi-gene UPR, ISR, lipid, autophagy, mitochondrial, or neuronal-identity program at FDR 0.05.

Point prediction:

| target_name | predicted_n_degs |
|---|---:|
| Arl6ip1 | 1 |

## Limits

- There is no direct `Arl6ip1` profile in the supplied training data or the same-experiment Distributed Agents corpus; the final count is an extrapolation from ER-shaping and ER/proteostasis comparators.
- The best same-complex paralog, `Arl6ip5`, was absent from the training count table, so the ARL6IP1-ARL6IP5/Addicsin interaction could not be tested directly.
- Chronic SPG61 and sensory/motor-axon phenotypes involve cell types, distal axonal compartments, organismal loss, and time scales outside this P16-to-P37/44 sparse central-neuron snRNA-seq design.
- Several training analogs were themselves near-null; whole-profile cosine/pearson values are consequently dominated by shared absence of signal, not by a reusable positive expression signature.
- Predicting 1 rather than 0 hinges on target self-detection. If the `Arl6ip1` gRNAs failed to reduce recoverable nuclear mRNA, or if the gene's focal expression was too low for the Wilcoxon test, the same reasoning would collapse to zero downstream DEGs.
