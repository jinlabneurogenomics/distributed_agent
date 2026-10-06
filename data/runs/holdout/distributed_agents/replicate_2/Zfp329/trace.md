# Question

The manifest contains one held-out perturbation, `Zfp329`.  I interpreted the task as asking for a single integer point prediction of the number of genes that would have `pvals_adj < 0.05` in `151 TH Prkcd Grin2c Glut` nuclei after acute AAV/CRISPR loss of `Zfp329`.

The important ambiguities I resolved were:

- A prediction of `0` means no assayed transcript crosses the focal Wilcoxon BH FDR threshold; it is not a statement that Zfp329 is biologically unimportant or that the perturbation failed to edit DNA.
- The held-out target has no observed Zfp329 perturbation signature in the parquet or the training-count CSV, so the decision must be transferred from training perturbations and external Zfp329 biology.
- Zfp329's biology is sparsely annotated, so I treated broad zinc-finger membership as weak evidence unless it was backed by a mouse paralog, same-assay expression pattern, or a corpus-supported mechanistic comparison.

# Sources Used

- `[local file: training_de_all_cell_groups.parquet]`, filtered to `group_name == "151 TH Prkcd Grin2c Glut"`.
- `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- `[local file: 269_Zfp329.csv]`.
- Distributed Agents same-experiment corpus, release `perturbai-july-260713-sourceguard-1773-v1`, queried for `Zfp329`, `Zfp148`, `Zfp236`, `Zfp322a`, `Zfp423`, and `Zfp536`.
- Distributed Agents run-local profile tooling for a focal zinc-finger/repressive-chromatin cohort.
- UniProtKB release `2026_03`.
- Ensembl REST, release 116.
- NCBI PubMed E-utilities for ZFP329/ZNF329 literature.

# Dataset Checks and Computations

I read the manifest and found exactly one requested target:

- `Zfp329`

I then filtered the large parquet down to the focal cell group, retaining `gene_target`, measured `names`, `logfoldchanges`, `pvals_adj`, `n_pert_matched`, and `n_ctrl_matched`.  The focal slice has 28,891,566 rows: 1,674 training targets times 17,259 measured genes.  Recomputing `sum(pvals_adj < 0.05)` for every `gene_target` reproduced the supplied training-count CSV exactly, with a maximum absolute count difference of 0.

The training endpoint is strongly zero-inflated in this cell type:

- 1,674 total training perturbations
- 469 nonzero perturbations
- median `n_degs = 0`
- 75th percentile `n_degs = 1`
- 95th percentile `n_degs = 18`
- maximum `n_degs = 2677`

I next enumerated all assayed `Zfp*`/`Zfpm2` targets in the training counts:

| training perturbation | focal n_degs | largest FDR<0.05 genes when nonzero |
| --- | ---: | --- |
| Zfp1 | 0 | |
| Zfp106 | 0 | |
| Zfp148 | 8 | Rasgrp2, Cacnb3, Slitrk5, Plekhj1, Srsf9, Ypel4, Ptprn, Srrm2 |
| Zfp160 | 0 | |
| Zfp182 | 0 | |
| Zfp236 | 19 | Kmt5b, Ogt, Eif4a2, Phip, Rreb1, Sesn1, Cpt1c, Lrp6 |
| Zfp266 | 0 | |
| Zfp280c | 0 | |
| Zfp280d | 0 | |
| Zfp292 | 0 | |
| Zfp322a | 0 | |
| Zfp341 | 0 | |
| Zfp397 | 0 | |
| Zfp423 | 150 | Ntsr1, Col27a1, Slc16a11, Niban2, Drd2, Herc6, Pxdn, Tspear |
| Zfp451 | 0 | |
| Zfp462 | 0 | |
| Zfp521 | 0 | |
| Zfp536 | 0 | |
| Zfp609 | 0 | |
| Zfp612 | 1 | Notum |
| Zfp644 | 0 | |
| Zfp654 | 0 | |
| Zfp664 | 0 | |
| Zfp692 | 1 | Zfp692 |
| Zfp804a | 0 | |
| Zfp846 | 0 | |
| Zfp949 | 0 | |
| Zfp950 | 0 | |
| Zfp961 | 0 | |
| Zfpm2 | 0 | |

I used exact overlap of the FDR<0.05 gene sets to check whether the active `Zfp*` targets represented a reusable module:

- `Zfp148` and `Zfp236`: 0 shared focal DEGs.
- `Zfp148` and `Zfp423`: 0 shared focal DEGs.
- `Zfp236` and `Zfp423`: 3 shared focal DEGs, `Ache`, `Ogt`, and `Tspan17`.
- `Zfp236` and `Setdb1`: 0 shared focal DEGs.
- `Zfp423` and `Zfp521`: 0 shared focal DEGs.
- `Zfp266` and `Zfp236`: 0 shared focal DEGs, with `Zfp266` itself having no focal DEGs.

The run-local profile comparison over `Zfp148`, `Zfp236`, `Zfp423`, `Zfp266`, `Zfp322a`, `Zfp536`, `Zfp521`, `Setdb1`, and `Zkscan1` gave the same activity classes: `Zfp266`, `Zfp322a`, `Zfp536`, `Zfp521`, and `Zkscan1` were in the no-significant-feature class; `Zfp148` was in the 1-9 class; `Zfp236` and `Setdb1` were in the 10-49 class; and only `Zfp423` exceeded 50 focal significant features.  I did not use raw whole-profile correlations as weights because mostly flat vectors can look similar over thousands of non-FDR background genes.

# Target-specific Reasoning

## Zfp329

### External target biology

UniProtKB release 2026_03 annotates mouse Zfp329/ZNF329 as zinc finger protein 329, a reviewed protein with C2H2 zinc-finger Pfam/InterPro domains and only a generic predicted role in transcriptional regulation.  I did not find curated UniProt evidence for a neuronal complex, signaling pathway, chromatin complex, or stress pathway that could be mapped to a represented training perturbation.

Ensembl release 116 maps mouse `Zfp329` to `ENSMUSG00000057894` and lists 18 mouse paralogs.  The only Ensembl-called Zfp329 paralog that appeared in the 1,674 training targets was `Zfp266`; the rest of the detected mouse paralogs, including `Zfp566`, `Zfp180`, `Zfp69`, `Zfp9`, `Zfp78`, `Zfp763`, `Zfp90`, `Zfp248`, `Zfp169`, `Zfp558`, `Zfp37`, `Zfp105`, and `Zfp582`, were absent from the training-count CSV.

The direct ZNF329 literature I found is non-neuronal and thin.  Dong et al. 2021 showed allele-specific binding of human ZNF329 to a BCL2 enhancer at the central-obesity GWAS variant rs12454712 in adipocyte-related assays, supporting that ZNF329 can bind DNA regulatory sequence and alter enhancer output, but not establishing a postmitotic neuronal program (Diabetes, DOI `10.2337/db20-1151`, PMID 34035043).  Zhang et al. 2016 inferred, from expression-only directed network reconstruction, that ZNF329 and RB1 may regulate a mesenchymal brain-tumor signature, but that was computational, disease-associated, and not a mouse neuronal loss-of-function experiment (BMC Genomics, DOI `10.1186/s12864-016-2791-2`, PMID 27556418).

The Distributed Agents same-experiment corpus had no `Zfp329` findings or claims, so there was no internal held-out-neighborhood writeup to reuse directly.

### Relevant training perturbations

`Zfp266` is the key in-dataset analog because it is the only Ensembl release 116 mouse paralog of Zfp329 that was actually perturbed in the training set.  Its observed focal count was:

- `Zfp266`: `n_degs = 0`

That makes it a closer comparator than the active `Zfp236` or `Zfp423` examples, which share only the broad Zfp symbol prefix and C2H2-like DNA-binding architecture.  I also treated `Zfp322a`, `Zfp341`, and `Zfp397` as same-assay C2H2 zinc-finger counterexamples because all were assayed and all had:

- `Zfp322a`: `n_degs = 0`
- `Zfp341`: `n_degs = 0`
- `Zfp397`: `n_degs = 0`

The Distributed Agents corpus strengthens the flat interpretation for `Zfp322a`: its report states that Zfp322a loss gave an all-null downstream transcriptome across recovered NeuN+ neuronal groups and that its expected embryonic stem-cell program was absent after P16 perturbation in postmitotic neurons.  That is an imperfect analogy to Zfp329, but it supports the broader pattern that C2H2 developmental/pluripotency zinc-finger programs are frequently dormant or buffered in the juvenile neuronal assay.

The active `Zfp*` perturbations were useful counterexamples:

- `Zfp148`: `n_degs = 8`, mostly down in 151 TH Prkcd Grin2c Glut, including `Rasgrp2`, `Cacnb3`, `Slitrk5`, `Srsf9`, `Ptprn`, and `Srrm2`.
- `Zfp236`: `n_degs = 19`, with a small thalamic metabolic/translation signature including `Kmt5b`, `Ogt`, `Eif4a2`, `Cpt1c`, and `Lrp6`.
- `Zfp423`: `n_degs = 150`, a much broader thalamic state involving `Ntsr1`, `Drd2`, `Col27a1`, `Pxdn`, `Ogt`, adhesion/ECM transcripts, and receptor/synaptic marker changes.

I did not transfer the `Zfp423` magnitude to `Zfp329`.  The corpus reports that Zfp423 loss in this assay is sharply cell-type restricted and that obvious relatives did not phenocopy it: `Zfp521`, EBF factors, BMP-SMAD factors, retinoic-acid receptors, Zic factors, and `Chd4` were nonconvergent in the matched response.  `Zfp521`, a closer literature partner of Zfp423 than Zfp329 is, had `n_degs = 0` in the focal endpoint.

I also did not transfer the `Zfp236` or `Zfp148` responses.  `Zfp236` was not phenocopied by `Setdb1` or the brain ZFP comparator `Zfp536` according to the Distributed Agents corpus, and it had zero exact focal FDR<0.05 overlap with `Zfp148`.  `Zfp148` has a small thalamus-restricted splicing/synaptic signature in the corpus, but that signature had zero exact focal overlap with both `Zfp236` and `Zfp423`.

Finally, `Zfp612` and `Zfp692` only reached one FDR<0.05 gene each in the focal group.  I treated those as singleton boundary cases rather than evidence for a broad Zfp329 response, especially because `Zfp692`'s singleton was the perturbed transcript itself.

### Zero/nonzero and count choice

The weight of the evidence points to no detectable focal response:

- Direct paralog evidence: the only assayed Ensembl paralog, `Zfp266`, had `0` focal DEGs.
- Family/background evidence: 25 of the 30 assayed `Zfp*`/`Zfpm2` perturbations had `0`; two more had only one focal DEG.
- Expression-pattern evidence: the active `Zfp148`, `Zfp236`, and `Zfp423` signatures were largely non-overlapping rather than one shared zinc-finger module.
- Corpus evidence: active ZFP cases were idiosyncratic and not reproduced by closer same-assay partner or pathway perturbations such as `Zfp521`, `Zfp536`, or `Setdb1`.
- External biology: Zfp329 has evidence compatible with sequence-specific transcriptional regulation, but no established postnatal thalamic neuron maintenance role, complex membership, or pathway that nominates an active training analog.

I therefore predict `Zfp329` to fall on the zero side of the FDR endpoint:

- `predicted_n_degs = 0`

# Limits

This is an extrapolation from absence and boundary evidence, not from a direct Zfp329 profile.  The closest Ensembl paralog represented in the training data was only `Zfp266`; most other mouse Zfp329 paralogs were not assayed, so a hidden paralog-specific thalamic program could be missed.  Zfp329 is poorly studied, and the main PubMed evidence I found is from human adipocyte or tumor-expression contexts, not acute mouse neuronal loss of function.

The assay also observes a single time window after sparse AAV CRISPR in NeuN+ nuclei.  A target may affect protein state, chromatin binding, electrophysiology, development before P16, or non-neuronal compartments without producing any BH-significant nuclear mRNA changes in this endpoint.  Conversely, a zero prediction is sensitive to the exact cell counts, effect sizes, and Wilcoxon/BH power in `151 TH Prkcd Grin2c Glut`.
