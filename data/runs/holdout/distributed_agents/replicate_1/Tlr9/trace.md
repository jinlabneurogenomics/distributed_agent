# Reasoning trace

## Question and endpoint

I interpreted the task as a scalar prediction for one held-out perturbation,
`Tlr9`, in `151 TH Prkcd Grin2c Glut` cells.  The requested value is the number
of measured genes with `pvals_adj < 0.05` in the focal thalamic glutamatergic
neuronal group.  The `Tlr9` knockout signature and its true count are absent
from both supplied training inputs, so the endpoint is directly observed only
for related non-held-out perturbations.  I preserved the requested-target order
from `the single-target request`; the set contains only `Tlr9`.

## Sources used

- Declared focal training endpoint:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared differential-expression Parquet:
  `training differential-expression dataset`.
- Run-local dataset portrait and measurement registry in
  `codex_runtime/pipeline/`, which define the PerturbAI postnatal mouse
  neuronal AAV-CRISPR design, the focal-cell label, and the limits of recovered
  snRNA-seq differential expression.
- Same-experiment semantic corpus: PerturbAI July 260713 sourceguard 1773 v1
  Findings ledger, queried for `Tlr2`, `Tlr3`, `Tlr4`, `Tlr7`, `Tlr8`, and
  `Nfkb1` as bounded report-level summaries of receptor and NF-kB behavior.
  I used it as packaged interpretation of the same Perturb-seq experiment, not
  as independent replication.
- PubMed literature for external mechanism: Hemmi et al. 2000,
  DOI:10.1038/35047123, PMID:11130078; Kim et al. 2008,
  DOI:10.1038/nature06726, PMID:18305481; Kaul et al. 2012,
  DOI:10.1371/journal.pone.0037767, PMID:22666391; Suriano et al. 2024,
  DOI:10.1016/j.ymthe.2024.03.036, PMID:38566414.

## Computational checks over the supplied data

The focal training-count table contains 1,674 non-held-out perturbations; 1,205
have `n_degs = 0`, the median is 0, the 75th percentile is 1, and the largest
responses are broad core regulators such as `Uba5` at 2,677 DEGs, `Tpr` at
1,768, `Sin3a` at 1,433, spliceosome/proteostasis/chromatin targets, and other
housekeeping regulators.  That establishes that a zero prediction is common but
not a consequence of the assay being unable to produce large focal-cell counts.

For `Tlr9`, the most relevant trained perturbations in the focal count table
were quiet:

| training perturbation | relationship to Tlr9 | observed `n_degs` in 151 TH Prkcd Grin2c Glut |
| --- | --- | ---: |
| `Tlr7` | endosomal nucleic-acid-sensing TLR; uses UNC93B1/MYD88 trafficking and signaling logic | 0 |
| `Tlr8` | close endosomal ssRNA TLR paralog | 0 |
| `Tlr3` | endosomal nucleic-acid TLR; TRIF rather than MyD88 branch | 0 |
| `Tlr2` | MyD88/TIRAP cell-surface inflammatory TLR | 0 |
| `Tlr4` | MyD88/TRIF inflammatory TLR and AAV-irrelevant counterexample | 0 |
| `Tlr5` | flagellin TLR, useful as another receptor-family basal control | 0 |
| `Cd14` | TLR4/TLR innate co-receptor | 0 |
| `Traf3` | shared innate adaptor downstream of TRIF and antiviral signaling | 0 |
| `Ifih1` | cytosolic dsRNA sensor, interferon-pathway comparator | 0 |
| `Nod2` | innate immune pattern-recognition receptor | 0 |
| `Nfkb1` | NF-kB transcription factor downstream of TLRs | 0 |
| `Chuk` | IKK-alpha / NF-kB-pathway kinase | 0 |
| `Map3k7` | TAK1 kinase upstream of NF-kB/MAPK inflammatory signaling | 0 |
| `Rel` | NF-kB-family transcription factor | 0 |
| `Irf1`, `Irf2`, `Irf3`, `Irf5`, `Irf8`, `Irf9` | interferon-regulatory factors | 0 |

I then read the corresponding rows from the focal-cell Parquet rather than only
using the precomputed counts.  Each of `Tlr2`, `Tlr3`, `Tlr4`, `Tlr5`, `Tlr7`,
`Tlr8`, `Cd14`, `Ifih1`, `Nfkb1`, `Nod2`, and `Traf3` had 17,259 measured-gene
rows in the focal cell group, zero genes at `pvals_adj < 0.05`, and minimum
adjusted p-value 1.0.  `Irf3` and `Map3k7` likewise had minimum adjusted
p-value 1.0; `Chuk` and `Rel` had no FDR-significant gene, with their best
adjusted p-values still nonsignificant at 0.727 and 0.140.  The same rows showed
the same control depth for these contrasts, `n_ctrl_matched = 23679`, with
113 to 211 matched perturbed nuclei for the inspected receptor/adaptor
perturbations.  This was enough power to detect strong focal-cell responses in
other targets, but no trained TLR or NF-kB perturbation had even a near-threshold
canonical inflammatory response in this cell group.

I also checked whether TLR9-pathway and interferon-response transcripts were
themselves responsive in the focal cell group under other knockouts.  `Tlr9` as
a measured gene was present for all 1,674 training perturbations but always had
`pvals_adj = 1.0`; its top signed scores were near zero.  Measured `Unc93b1`,
`Myd88`, and `Irak4` were also FDR-null across the focal training set, with the
only moderate deviations coming from broad perturbations such as `U2af2`.
Sentinel antiviral genes such as `Ifit1`, `Isg15`, `Bst2`, and the inflammatory
gene `Lcn2` were not generally induced except as isolated outputs of very broad
stress perturbations (`Uba5`, `Psmb4`, `Cdc40`, `Tpr`).  Thus the held-out Tlr9
signature is not expected to be a hidden member of a constitutive interferon or
NF-kB module.

## Target-specific reasoning for Tlr9

`Tlr9` encodes an endosomal Toll-like receptor that recognizes unmethylated CpG
DNA and signals through MYD88 to inflammatory and type-I-interferon response
programs; Hemmi et al. showed that TLR9-deficient mice fail to respond to CpG
DNA, and Kim et al. showed that UNC93B1 delivers TLR7 and TLR9 from the ER to
endolysosomes.  A simple obligate-complex analog was unavailable in the training
set because `Myd88`, `Unc93b1`, `Irak1`, `Irak4`, and `Traf6` were not
non-held-out perturbations.  The best in-dataset analogs are therefore
endosomal `Tlr7`/`Tlr8`, ligand-gated inflammatory `Tlr2`/`Tlr4`, and the
represented NF-kB/IRF nodes listed above.

Those analogs are appropriate because a tonic TLR9-to-MYD88 program in the
assayed neurons should have propagated into NF-kB, AP-1, cytokine, chemokine, or
interferon-stimulated transcripts.  The Parquet showed no such propagation:
focal `Tlr7`, `Tlr8`, `Tlr3`, `Tlr2`, `Tlr4`, `Tlr5`, `Nfkb1`, `Chuk`,
`Map3k7`, `Rel`, and `Irf3/5` perturbations were all zero; the internal July
Findings ledger summarized the same result more broadly, reporting that `Tlr7`
loss was transcriptionally silent in all measured neuronal groups, `Tlr2` and
`Tlr4` were pan-neuronal basal nulls, `Tlr3` produced only one noncanonical
`Rgs4` hit outside the focal group, and the represented NF-kB/TNF/TLR
comparators phenocopied the flat `Nfkb1` state rather than revealing an inducible
neuronal module.

There is one real counterargument.  The screen used AAV delivery, and AAV
genomes are CpG-rich; Suriano et al. 2024 reported in mouse somatosensory cortex
that a TLR9-dependent innate response to recombinant AAV genomes decreased
dendritic complexity and changed synaptic transmission.  That makes `Tlr9` a
more plausible nonzero candidate than unrelated TLRs.  I still predict zero
because the causal chain is poorly aligned with this endpoint: AAV entry and
initial TLR9 sensing occur before Cas9 has edited `Tlr9`; all cells, including
controls, receive the same vector backbone; the assay recovers NeuN-positive
nuclei weeks later rather than dendrites or synaptic physiology; microglia and
astrocytes that normally amplify innate TLR signals are under-sampled; and the
focal expression data show no stable TLR9, MYD88, NF-kB, or interferon
transcriptional surface in the recovered thalamic glutamatergic nuclei.  Kaul
et al. 2012 supports that neuronal TLR7/TLR9 expression can occur during mouse
brain development, but it does not establish a tonic postnatal transcriptional
requirement in this thalamic class.

The predicted intervention chain is therefore: sparse AAV guide delivery ->
delayed partial `Tlr9` loss in postmitotic recovered neurons -> no obligate
loss of a constitutively active endosomal CpG/MYD88 signal in the focal cell
state -> no broad NF-kB/IRF/ISG propagation -> no FDR-significant genes at the
Wilcoxon threshold.  The closest in-dataset perturbations are all at zero, so
the final point estimate is:

| target | predicted `n_degs` |
| --- | ---: |
| `Tlr9` | 0 |

## Limits and uncertainty

This is a zero-boundary extrapolation for a held-out gene, not a measured Tlr9
result.  The exact TLR9 trafficking and MYD88 kinase module was mostly absent
from the training perturbation set, so I had to transfer from paralogous
receptors and downstream pathway nodes.  The all-zero TLR/NF-kB training
surface is strong evidence for no basal neuronal transcriptomic effect but
would miss morphology, electrophysiology, early AAV sensing before editing,
ligand-challenge phenotypes, non-neuronal innate amplification, and severe
selection that occurred before nuclei were recovered.  The AAV-specific TLR9
literature raises the chance of a small effect, but there was no focal
within-dataset signal suggesting enough sustained downstream transcription to
cross FDR 0.05 for any gene.
