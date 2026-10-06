# Pum1 DEG-count prediction

## Question and endpoint

I interpreted the task as a point prediction of `n_degs` for the requested held-out perturbation `Pum1` in `151 TH Prkcd Grin2c Glut` cells. The endpoint is the count of measured genes with Wilcoxon Benjamini-Hochberg `pvals_adj < 0.05` in the focal cell group. `Pum1` itself was absent from both supplied inputs, so I treated the supplied Parquet and the focal-cell training-count CSV as direct measurements for non-held-out perturbations only and used them to calibrate analogous visible perturbations.

The focal readout is direct for training genes and absent for `Pum1`; the training signatures are same-experiment measurements, the packaged July 260713 same-experiment corpus is a literature-grounded interpretation of those same measurements rather than independent replication, and PubMed literature is external prior knowledge.

## Sources used

- Declared focal training counts: `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared DE Parquet: `training differential-expression dataset`, queried only for the focal group and visible mechanistic comparators.
- Requested target manifest: `single-target request for Pum1`.
- Run-local dataset portrait, task bindings, coverage, capabilities, and measurement registry under `codex_runtime/pipeline`.
- Internal same-experiment corpus: `perturbai-july-260713-sourceguard-1773-v1`, via bounded Finding inventories for Atxn1, Fmr1, Tardbp, Cnot1, Hnrnpc, Hnrnpu, and Xrn1.
- External literature from PubMed:
  - Gennarino et al. 2015, Cell, "Pumilio1 haploinsufficiency leads to SCA1-like neurodegeneration by increasing wild-type Ataxin1 levels", DOI `10.1016/j.cell.2015.02.012`, PMID `25768905`.
  - Gennarino et al. 2018, Cell, "A Mild PUM1 Mutation Is Associated with Adult-Onset Ataxia, whereas Haploinsufficiency Causes Developmental Delay and Seizures", DOI `10.1016/j.cell.2018.02.006`, PMID `29474920`.
  - Zhang et al. 2017, Genes & Development, "Post-transcriptional regulation of mouse neurogenesis by Pumilio proteins", DOI `10.1101/gad.298752.117`, PMID `28794184`.
  - Van Etten et al. 2012, Journal of Biological Chemistry, "Human Pumilio proteins recruit multiple deadenylases to efficiently repress messenger RNAs", DOI `10.1074/jbc.M112.373522`, PMID `22955276`.
  - Goldstrohm et al. 2018, Trends in Genetics, "Post-transcriptional Regulatory Functions of Mammalian Pumilio Proteins", DOI `10.1016/j.tig.2018.09.006`, PMID `30316580`.
  - Bohn et al. 2018, Nucleic Acids Research, "Identification of diverse target RNAs that are functionally regulated by human Pumilio proteins", DOI `10.1093/nar/gkx1120`, PMID `29165587`.
  - Enwerem et al. 2021, RNA, "Human Pumilio proteins directly bind the CCR4-NOT deadenylase complex to regulate the transcriptome", DOI `10.1261/rna.078436.120`, PMID `33397688`.

## Computational calibration

The requested-target CSV had exactly one row:

```tsv
target_name
Pum1
```

The focal training-count file had 1,674 visible perturbations. It was strongly zero inflated: 1,205 had `n_degs=0`, the median count was 0, the 75th percentile was 1, the 90th percentile was 2, and the mean was 14 because a small tail of broad perturbations reached hundreds to thousands of genes. Thus a held-out post-transcriptional regulator needed evidence for a broad steady-state nuclear RNA response before assigning a high positive count.

I then queried the training counts for visible genes that sit near PUM1 biology: sequence-specific cytoplasmic RNA repressors, the miRNA/CCR4-NOT/5-prime-to-3-prime decay route used by PUM proteins, PUM1's Atxn1/Scn8a disease targets, and RNA-binding counterexamples. Counts in `151 TH Prkcd Grin2c Glut` were:

```tsv
target	n_degs	relevance_to_Pum1
Fmr1	0	translational repressor, neuronal RBP, external PUM partner in mouse neural cells
Msi1	0	sequence-specific translational repressor RBP
Tia1	0	stress-granule/RBP comparator
Ago2	0	miRNA slicer/repressor upstream of TNRC6/CCR4-NOT deadenylation
Dicer1	0	miRNA biogenesis enzyme
Ago1	1	Argonaute family miRNA effector
Cnot1	0	core scaffold of the CCR4-NOT deadenylase recruited by PUM proteins
Eif4a2	2	translation-initiation helicase
Ddx3x	8	RNA helicase/translation-linked RBP
Atxn2	8	RBP/ataxia gene, weak ALS-family comparator in the same corpus
Xrn1	20	cytoplasmic 5-prime-to-3-prime exonuclease downstream of decapping
Hnrnpc	122	nuclear hnRNP with splice/3-prime-end compensation
Atxn1	187	direct PUM1-repressed disease target, but Atxn1 perturbation is loss of function
Tardbp	210	nuclear RBP whose loss propagates into spliceosome and ER/lysosomal programs
Hnrnpu	733	chromatin/pre-mRNA hnRNP with ISR, proteostasis, and spliceosome programs
```

For the focal-cell DE rows of these comparators I checked the leading adjusted p-values and log fold changes in the Parquet. The flat PUM-near mechanisms were genuinely flat after FDR correction rather than simply missing from the count CSV: `Fmr1` had no `pvals_adj < 0.05` genes, `Dicer1` had none, `Ago2` had none, `Cnot1` had none, `Ago1` had only `Kif13b`, and `Msi1`/`Tia1` had none. `Xrn1` had 20 genes headed by `Psap`, `Adgrb1`, `Gpatch8`, `Unc45a`, and `Enpp5`, a mixed secondary endomembrane/synaptic state rather than a PUM-like direct target accumulation. In contrast, `Tardbp`, `Hnrnpc`, and `Hnrnpu` had broad focal signatures with RNA-processing, splicing, proteostasis, or ISR layers that are not expected outputs of weakening a PUM-CNOT cytoplasmic repression branch.

## Target-specific reasoning

### Pum1

**Direct molecular consequence.** PUM1 is a sequence-specific PUF-family RNA-binding protein. Human PUM1 and PUM2 can repress target mRNAs through CCR4-NOT recruitment and decapping-dependent decay (Van Etten et al. 2012; Enwerem et al. 2021), and human perturbation studies identified many direct and indirect abundance changes after PUM knockdown (Bohn et al. 2018). That makes some positive whole-gene mRNA response plausible in an assay that counts nuclear steady-state DEGs.

**Neuronal propagation expected in this assay.** The strongest neuronal external evidence did not point to a large acute PUM1-specific nuclear RNA program in postmitotic thalamic neurons. Neural Pum1/Pum2 deletion in mouse dentate gyrus bound many RNAs, but depleting PUM proteins did not change most target mRNA abundances and instead increased their protein abundance (Zhang et al. 2017). PUM1 haploinsufficiency causes SCA1-like neurodegeneration and human PADDAS/PRCA through increased wild-type ATXN1 and other PUM targets (Gennarino et al. 2015, 2018), again consistent with dosage-sensitive target derepression but not with a universal transcriptional stress state within three to four weeks of mosaic postnatal CRISPR.

**Visible analogs and counterexamples.**

- `Fmr1`, the closest visible translational-neuronal RBP counterexample from the same experiment, had `n_degs=0` in `151 TH Prkcd Grin2c Glut`. Its corpus report found a nearly orthogonal whole response and no robust compensatory UPR, ISR, heat-shock, autophagy, proteasome, or canonical FMRP-target mRNA-abundance program. Zhang et al. 2017 also reported RNA-dependent interactions between Pum1/Pum2 and FMRP, making this a functionally relevant negative comparator rather than an arbitrary flat target.
- `Cnot1` had `n_degs=0` in the focal cell group. PUM proteins use CCR4-NOT for deadenylation, so the CNOT1 result tested a core effector branch. The same-experiment Cnot1 report showed sparse responses restricted mostly to `155 MB Glut` and emphasized buffering rather than a universal mRNA-decay-collapse signature. Its report also noted that `Ago1`, `Ago2`, TNRC6, and `Xrn1` did not phenocopy Cnot1. This argues against assuming that loss of one upstream sequence-specific CNOT recruiter, `Pum1`, will create a broad focal DEG count.
- `Ago1`, `Ago2`, and `Dicer1` had 1, 0, and 0 focal DEGs. These are not direct PUM analogs, but they weaken miRNA-linked post-deadenylation repression in the same cytoplasmic decay neighborhood. Their near-null readout is a pathway counterexample to a generic "mRNA repression factor loss equals many nuclear DEG calls" rule.
- `Xrn1` had a small positive count, 20, in the focal group. The corpus showed that its 151/155 signatures were mixed up and down and did not converge with `Dicer1`, `Ago2`, `Tnrc6a`, `Tnrc6b`, `Cnot1`, or `Upf3b`. Because PUM-dependent mRNAs are deadenylated before decapping and XRN1-mediated decay, this is at most a weak lower-bound analog, and the expression pattern does not look like direct PUM target accumulation.
- `Atxn1` had a robust focal count, 187, and the corpus showed a 151-TH ATXN1-CIC state with 177 of 256 FDR<0.10 Atxn1 genes also significant under `Cic` in the same direction. But PUM1 loss is predicted to increase ATXN1, while the visible `Atxn1` perturbation is Atxn1 loss of function. The causal sign is therefore opposite or at least indeterminate: PUM1 impairment may increase Atxn1 mRNA/protein, not phenocopy an Atxn1 knockout. `Scn8a`, another PUM1-repressed neuronal target in the literature-prior model, had only a singleton focal response. The ATXN1 axis therefore supports PUM1 relevance but does not justify copying the 187-count Atxn1 knockout signature.
- Broad visible nuclear RBP responses were mechanistically different. `Tardbp` had 210 focal DEGs through RNA-processing, ER/lysosomal, and mitochondrial compensation; `Hnrnpc` had 122 with a splice/3-prime-end and stress-granule-clearance response; `Hnrnpu` had 733 with spliceosome, ISR-like, proteostasis, and chromatin modules. Their corpus reports repeatedly showed that RBP family membership was not interchangeable: Hnrnpc-family comparators and ALS/FTD RBP relatives of Tardbp were often flat or weak. I therefore treated these as upper-tail counterexamples, not as the numerical prior for a cytoplasmic Pumilio perturbation.

**Prediction.** The most causally local visible mechanisms for PUM1 - FMRP-linked translational repression and CCR4-NOT/Ago mRNA repression - were flat in the focal group, while the high-count visible RBP perturbations acted through nuclear spliceosome/chromatin or proteotoxic programs that PUM1 loss should not automatically engage. The direct Atxn1 connection is biologically strong but sign-mismatched for an Atxn1 knockout analog. Given the zero-inflated focal distribution and lack of a same-direction visible PUM paralog, I predict that acute mosaic `Pum1` loss will have no genes passing FDR 0.05 in `151 TH Prkcd Grin2c Glut`.

## Limits and uncertainty

The largest gap is the absence of visible `Pum2`, the best paralogous perturbation. Redundancy between PUM1 and PUM2, cell-type differences between postnatal dentate neurogenesis and thalamic postmitotic neurons, and the fact that snRNA-seq measures steady-state nuclear whole-gene abundance rather than translation, RNA half-life, local dendritic protein synthesis, or isoforms all make the transfer indirect. Conversely, PUM1 can destabilize some mRNAs through CCR4-NOT, so a small positive count would also be plausible. I assigned zero because the focal assay was strongly sparse and every visible comparator closest to the PUM-CNOT and translational-repressor mechanism was zero or nearly zero, not because PUM1 is biologically unimportant.
