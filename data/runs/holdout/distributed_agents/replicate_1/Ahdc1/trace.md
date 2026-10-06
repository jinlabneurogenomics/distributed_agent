# DEG-count prediction trace

## Question and endpoint

The requested target set contains one held-out perturbation, `Ahdc1`. I interpreted
the task as a point prediction of `n_degs` in `151 TH Prkcd Grin2c Glut`, where
`n_degs` is the number of measured genes with a Scanpy Wilcoxon
Benjamini-Hochberg adjusted p-value below 0.05 after the acute P16 AAV-CRISPR
loss-of-function perturbation. `151 TH Prkcd Grin2c Glut` is the focal thalamic
glutamatergic neuronal class, not a TH/dopamine label.

The held-out endpoint for `Ahdc1` is absent from the supplied inputs by design:
`Ahdc1` occurs in the requested-target CSV, but not in the
`151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` endpoint table and not as a
`gene_target` in `training_de_all_cell_groups.parquet`.

## Sources used

- Declared training endpoint:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
  This directly measures the focal-cell `n_degs` endpoint for 1,674
  non-held-out targets.
- Declared differential-expression parquet:
  `training differential-expression dataset`.
  I read rows for `151 TH Prkcd Grin2c Glut` and selected training analogs to
  check their significant genes, effect directions, and FDR-level overlap.
- Same-experiment internal corpus:
  `perturbai-july-260713-sourceguard-1773-v1`. I used bounded Finding
  inventories and the summary-first `corpus.direct_evidence` index to interpret
  training perturbations that were already visible in the supplied experiment.
  These reports are alternate annotations of the same experiment, not
  independent replication.
- External mechanism sources: NCBI PubMed; MyGene.info, queried on 2026-09-02,
  for the RefSeq/Gene Ontology/InterPro summary of mouse and human AHDC1; and
  STRING-DB functional-network lookup for mouse Ahdc1, queried on 2026-09-02.
  STRING returned only weak text-mining neighbors, so I did not use it as a
  quantitative or causal anchor.

External citations used:

- Khayat et al. 2021, HGG Advances, doi:10.1016/j.xhgg.2021.100049,
  PMID:34950897: de novo AHDC1 missense variants in patients with Xia-Gibbs-like
  neurodevelopmental phenotypes, with several variants mapping to conserved
  AHDC1 regions.
- Khayat et al. 2021, Human Mutation, doi:10.1002/humu.24190, PMID:33644933:
  phenotypic heterogeneity of Xia-Gibbs syndrome caused by pathogenic
  truncating AHDC1 alleles and altered nuclear localization of truncated AHDC1
  forms.
- Chander et al. 2022, Human Mutation, doi:10.1002/humu.24461, PMID:36054313:
  contiguous-deletion and long-read analysis of the AHDC1 locus, supporting
  locus-specific regulatory complexity.
- Romano et al. 2022, Birth Defects Research, doi:10.1002/bdr2.2058,
  PMID:35716097: Xia-Gibbs syndrome review and five additional cases; the paper
  frames AHDC1 as an AT-hook protein involved in transcription/epigenetic
  regulation, axonogenesis, brain function, and possibly DNA repair.
- Carvalho et al. 2023, Gene, doi:10.1016/j.gene.2023.147424, PMID:37054903:
  establishment of AHDC1 loss-of-function iPSC lines and an ahdc1
  CRISPR-edited zebrafish model for Xia-Gibbs syndrome.
- Li et al. 2023, American Journal of Physiology - Endocrinology and
  Metabolism, doi:10.1152/ajpendo.00048.2023, PMID:37819197: a survivable mouse
  Ahdc1-deficiency model with post-weaning metabolic phenotypes, confirming
  mammalian Ahdc1 activity but in peripheral/metabolic endpoints rather than
  this thalamic neuronal snRNA-seq endpoint.

## Internal quantitative calibration

The endpoint table is strongly sparse. Among 1,674 training targets in the
focal cell group, 1,205 had `n_degs = 0`; the median was 0, the 75th percentile
was 1, the 90th percentile was 2, the 95th percentile was 18, and the maximum
was 2,677. A positive held-out prediction therefore needs target-specific
support.

The nearest useful within-dataset anchors were not paralogs or obligate complex
partners of Ahdc1, because none are known in the training data. I treated
neurodevelopmental nuclear/chromatin regulators as imperfect analogs and
counterexamples:

| training target | observed `n_degs` at FDR 0.05 | focal expression evidence |
|---|---:|---|
| `Setd5` | 9 | Significant `Adarb1`, `Rgs4`, `Prkcd`, `Lrrc7`, `Ptpn4`, `Ntng1`, `Ndrg4`, `Cacna1g`, and `Kat6b`. |
| `Ankrd11` | 20 | Mostly up-regulated receptor/synaptic modulators including `Grin2b`, `Grm1`, `Lrrc7`, `Gabbr2`, `Ntng1`, `Adarb1`, and `Kcnc2`; six FDR 0.05 genes overlapped `Setd5` in the same direction (`Adarb1`, `Lrrc7`, `Ntng1`, `Prkcd`, `Ptpn4`, `Rgs4`). |
| `Arid1a` | 22 | A distinct mSWI/SNF thalamic scaffold/signaling response, with `Begain`, `Kcnq2`, `Ptpn3`, `Lrrc7`, `Rasa4`, `Lef1` down and `Clstn2`, `Slc25a23`, `Ppp2r5d` up; overlapped strongly with the mSWI/SNF core perturbation `Smarcc2` but not with `Ankrd11`. |
| `Kmt2a` | 24 | A small H3K4-writer response dominated by `Nr2f1`, `Pcdh7`, `Lhx9`, `Kmt2a`, `Camk2d`, `Grik2`, and `Pcdh10` down-regulation, with no FDR 0.05 overlap with `Ankrd11`, `Setd5`, or `Arid1a`. |
| `Chd2` | 34 | A sparse but real response led by `Snhg11`, `Plekhg1`, and `Ptpn3` down-regulation; its corpus comparison reported that BAF/PBAF and CHD relatives did not phenocopy it. |
| `Arid2` | 56 | A larger PBAF response with cell-adhesion, axon-guidance, excitability, cytoskeletal, and extracellular genes; useful mainly as an upper counterexample because Ahdc1 is not an established PBAF subunit. |
| `Chd8` | 61 | A broader subcortical RNA-processing/chromatin-maintenance signature, including strong `Pnisr`, `Tmem50a`, `Chd8`, `Man2c1`, and `Usp11` down-regulation; not treated as a close Ahdc1 analog because represented CHD, Wnt/beta-catenin, BAF, and other ASD chromatin genes did not phenocopy it in the same-experiment corpus. |
| `Arid1b`, `Pogz`, `Ep300`, `Smarca4` | 1, 0, 0, 0 | Disease-relevant or chromatin-adjacent perturbations that were essentially silent in this mature thalamic neuronal endpoint. |

These anchors show that even well-established NDD/chromatin genes range from
flat to hundreds of DEGs in this assay. Specific complex membership predicted
some local behavior, for example `Arid1a` with `Smarcc2/Smarce1`, but AHDC1 does
not have an analogous assayed obligate partner. Direct same-experiment evidence
also showed that label-neighbor comparisons were often false friends:
`Ankrd11` did not phenocopy `Ep300`, `Ncoa1`, `Ncoa3`, or `Hdac8`;
`Chd2` did not phenocopy other CHD-family genes; and `Arid1b` was buffered even
though `Arid1a`, `Arid2`, and `Smarcc2` were active.

## Ahdc1-specific prediction

AHDC1 is a large nuclear AT-hook DNA-binding protein. Human heterozygous
pathogenic variants cause Xia-Gibbs syndrome, whose recurrent features include
developmental delay, intellectual disability, hypotonia, and speech delay
(Khayat et al. 2021, PMID:33644933; Faergeman et al. 2021,
doi:10.1016/j.ejmg.2021.104280; Romano et al. 2022, PMID:35716097). MyGene.info
annotates mouse Ahdc1 with regulation of DNA-templated transcription by
electronic inference and with InterPro domains `IPR032757` and `IPR039225`.
Those annotations justify considering transcriptional-regulatory anchors such
as `Setd5`, `Ankrd11`, `Kmt2a`, `Kdm5c`, `Adnp`, `Chd2`, and BAF/PBAF
perturbations.

I did not transfer a broad outcome from those anchors. The causal chain in this
screen is:

`Ahdc1` CRISPR allele induction in a P16 postmitotic thalamic glutamatergic
neuron -> acute impairment of AHDC1 nuclear DNA/chromatin binding -> possible
changes in transcriptional regulation, axon/connectivity genes, or DNA-repair
programs -> survival and class recovery 3-4 weeks later -> Wilcoxon DEGs among
surviving assayed nuclei.

The external literature establishes the first two links only at a coarse
level. It does not identify an obligate AHDC1-containing complex that maps onto
a visible high-count perturbation, nor does it show a postnatal thalamic neuron
maintenance program with the same timing and partial mosaic dose used here.
Disease causation in heterozygous germline humans and a survivable mouse
Ahdc1-deficiency model indicate biological relevance, but they are not direct
evidence that the P16-P37 recovered-nucleus endpoint should be broad.

My estimate is therefore just above the assay's zero mode: I predict one FDR
0.05 DEG for `Ahdc1`. This preserves the strong prior from the training table
that many postmitotic perturbations are transcriptionally quiet in this exact
endpoint, while allowing a minimal nonzero response because AHDC1 is a nuclear
NDD gene with transcriptional and neurodevelopmental annotations rather than a
completely unrelated target.

## Limits

This is a weak extrapolation. `Ahdc1` itself has no supplied expression
signature or DEG count, and the internal July corpus did not contain a packaged
`Ahdc1` report in the visible same-experiment release. STRING-DB did not expose
a credible Ahdc1 interactor among the training perturbations. The selected
comparators are functional analogs, not paralogs or obligate complex partners,
and their endpoint counts are highly heterogeneous. The prediction could
therefore be wrong in either direction: `Ahdc1` could be flat like `Pogz`,
`Ep300`, or `Smarca4`, or it could have a broader unanticipated signature like
`Chd8` or `Wac` if its acute neuronal function couples to RNA-processing or
maintenance modules that are not apparent from current external annotation.

