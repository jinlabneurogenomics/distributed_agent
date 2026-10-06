# DEG-count prediction for Zfp329

## Question and resolved ambiguities

The requested endpoint is the integer number of measured genes with
Benjamini-Hochberg-adjusted Wilcoxon `pvals_adj < 0.05` after acute CRISPR loss
of each held-out target in `151 TH Prkcd Grin2c Glut` thalamic glutamatergic
neurons.  The held-out target list for this run contains one mouse symbol:
`Zfp329`.  I treated zero as the prediction that no measured gene, including
the targeted transcript if measured, crosses FDR 0.05 in the held-out contrast.

The endpoint is directly observed only for the non-held-out training
perturbations in
`151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.  The held-out `Zfp329`
signature itself is absent from both that CSV and
`training_de_all_cell_groups.parquet`, so all `Zfp329` reasoning is transfer
from training perturbations plus outside functional annotation.

## Sources

- Declared Perturb-seq focal training counts:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared per-gene DE table:
  `training differential-expression dataset`.
- Run manifest of requested held-out perturbations:
  `single-target request for Zfp329`.
- Distributed Agents same-experiment July 260713 sourceguard corpus,
  release `perturbai-july-260713-sourceguard-1773-v1`, queried through the
  bounded `corpus.findings` ledger for packaged interpretation of the Zfp
  training perturbations and Setdb1.
- NCBI Gene 67230 and Alliance/MGI MGI:1921283, accessed through the Alliance
  gene API in September 2026, for the curated identity and automated functional
  summary of mouse `Zfp329`.
- Ensembl REST `ENSMUSG00000057894`, GRCm39, for the mouse protein-coding gene
  model of `Zfp329`.
- PubMed literature for the sparse human `ZNF329` record and for the positive
  Zfp counterexamples: Dong et al. 2021, Diabetes, DOI
  `10.2337/db20-1151`; Zhang et al. 2016, BMC Genomics, DOI
  `10.1186/s12864-016-2791-2`; Warming et al. 2006, Molecular and Cellular
  Biology, DOI `10.1128/MCB.02255-05`; Hong and Hamilton 2016, PLoS Genetics,
  DOI `10.1371/journal.pgen.1006357`; Casoni et al. 2020, Development, DOI
  `10.1242/dev.190173`; Sayin et al. 2013, PLoS ONE, DOI
  `10.1371/journal.pone.0055720`; Zou et al. 2020, Scientific Reports, DOI
  `10.1038/s41598-020-70824-2`.

## Dataset computations

I first read the requested-target CSV and the focal DEG-count training CSV.  The
run has exactly one requested target and the count table has 1,674 unique
training targets.  The focal endpoint is strongly zero-inflated: 1,205/1,674
training perturbations are zero, the median and 75th percentile are 0 and 1
DEG, and only the top 5% exceed 18 DEGs.

The task is a scalar count prediction with no supplied ranked or partially
ranked supervision, so the rank-calibration workbench, graph-review nomination,
and ordering validator were unavailable by manifest policy.  I therefore used
direct target-scoped PyArrow filters against the declared Parquet.  The main
query selected rows with

```
group_name == "151 TH Prkcd Grin2c Glut"
and gene_target in candidate_zinc_finger_or_chromatin_analogs
```

and then counted `pvals_adj < 0.05` and inspected the lowest-FDR measured genes.

## Training analogs and counterexamples

### Simple Zfp and Zscan perturbations

The most direct within-dataset transfer set was the Zfp/Zscan group available
in training.  In the focal training counts there were 31 such targets:

- `Zfp423`: 150 DEGs.  This is the major positive Zfp counterexample.
  Parquet inspection showed a coherent thalamic state with `Grid2ip`, `Cd47`,
  `Syt13`, and `Cnnm1` down and `Ntsr1`, `Nptxr`, and `Kcnab3` up.  The
  same-experiment corpus interprets it as a real but noncanonical mature
  thalamic program; known Zfp423 partners and pathways, including `Zfp521`,
  EBFs, BMP-SMADs, retinoic-acid receptors, Zics, and `Chd4`, did not
  phenocopy it.  Externally, Zfp423/OAZ is a 30-zinc-finger developmental
  cofactor with experimentally established EBF and BMP-Smad interactions,
  cerebellar requirements, and ciliary/Shh functions (Warming et al. 2006;
  Hong and Hamilton 2016; Casoni et al. 2020).
- `Zfp236`: 19 DEGs.  The focal signature was narrow and dominated by
  `Ogt`, `Eif4a2`, `Gdi1`, `Phip`, and `Cpt1c` down-regulation, with `Rreb1`
  up.  The same-experiment corpus notes a repeated `Ogt`/translation/nutrient
  axis and also records that the KRAB/heterochromatin comparator `Setdb1` and
  the brain-Zfp comparator `Zfp536` did not phenocopy the restricted
  `Zfp236` response.
- `Zfp148`: 8 DEGs.  Its focal genes included `Srrm2`, `Cacnb3`, `Srsf9`,
  `Slitrk5`, `Rasgrp2`, and `Ptprn`.  Published Zfp148 biology includes
  direct or indirect ARF/p53 stress and cell-cycle control in proliferative
  cells (Sayin et al. 2013; Zou et al. 2020), but the same-experiment corpus
  specifically found no p53-response or proliferation transcript among
  Zfp148 FDR genes in the postmitotic neuronal screen.
- `Zfp612`: 1 DEG, `Notum` up.
- `Zfp692`: 1 DEG, and the only FDR-significant row was the targeted
  transcript itself.
- The remaining simple Zfp/Zscan training perturbations had 0 DEGs:
  `Zfp1`, `Zfp106`, `Zfp160`, `Zfp182`, `Zfp266`, `Zfp280c`, `Zfp280d`,
  `Zfp292`, `Zfp322a`, `Zfp341`, `Zfp397`, `Zfp451`, `Zfp462`, `Zfp521`,
  `Zfp536`, `Zfp609`, `Zfp644`, `Zfp654`, `Zfp664`, `Zfp804a`, `Zfp846`,
  `Zfp949`, `Zfp950`, `Zfp961`, and `Zscan26`.

The Parquet top rows support the split between rare biologically specific
positive signatures and the common null class: `Zfp322a` and `Zscan26`, for
example, had 17,259 focal rows each but no FDR-significant measured genes, and
their best adjusted p-values were still 0.927 and 1.0.  Across the inspected
Zfp/chromatin set, pairwise focal Wilcoxon-score correlations were also weak:
`Zfp423` versus `Zfp236` was 0.105, `Zfp423` versus `Zfp148` was 0.077, and
`Zfp236` versus `Zfp148` was 0.043 on the low-FDR gene subset.  Thus even the
nonzero Zfp training perturbations do not form one common Zfp response that can
be assigned to `Zfp329`.

### Chromatin and KRAB-effector comparators

Because uncharacterized C2H2/KRAB-like zinc-finger proteins can work through
chromatin repression, I also inspected broad chromatin repressors and adjacent
ZBTB/KLF/PRDM/KDM transcription factors represented in the focal counts.

- `Setdb1`, an H3K9 methyltransferase and KRAB/HUSH effector, had 22 DEGs.
  Its thalamic signature induced `Tasor`, `Atf7ip`, and several
  gamma-protocadherin transcripts.  The same-experiment corpus recorded the
  expected Pcdh/H3K9 relationship but also emphasized that `Dnmt3a` and
  `Smchd1` were flat and that `Setdb1` did not produce a generic type-I
  interferon or pan-chromatin-collapse response.
- `Atrx` had 8 DEGs, led by `Resp18` down.  `Dnmt3a` had 0 DEGs.
- `Zbtb7a` was a broad outlier with 841 DEGs; `Zbtb18`, `Zbtb38`, and most
  other ZBTB-like entries were near zero at 5, 1, and 0 DEGs.
- `Prdm10`, `Klf9`, and `Kdm5c` sat near the upper shoulder of the ordinary
  focal distribution at 52, 19, and 18 DEGs.

These perturbations are counterexamples rather than direct Zfp329 analogs.  If
`Zfp329` were known to be a limiting Setdb1/KAP1 recruiter in postnatal
thalamic neurons, `Setdb1` would argue for a small but nonzero count.  No such
candidate-specific dependency is known from the external Zfp329 record, and
`Zfp236:F008` in the same-experiment corpus shows that at least one KRAB/Zfp
training target failed to transfer to `Setdb1` or `Zfp536`.

## Target-specific Zfp329 rationale

NCBI Gene/Alliance annotate mouse `Zfp329` as a protein-coding zinc-finger
protein, predicted to enable RNA-polymerase-II regulatory-region
sequence-specific DNA binding, predicted to regulate Pol II transcription,
predicted nuclear, expressed in the central nervous system and genitourinary
system, and orthologous to human `ZNF329`.  Alliance/MGI did not expose an
asserted mouse phenotype for `MGI:1921283`.  Ensembl GRCm39 agrees on the
protein-coding locus `ENSMUSG00000057894`.

PubMed did not return a mouse `Zfp329` experimental paper.  The exact human
`"ZNF329"` query returned three sparse records.  The only direct binding result
was in adipocytes, where ZNF329 bound the rs12454712-C enhancer allele and
increased `BCL2` enhancer activity in reporter assays (Dong et al. 2021).  A
separate liver caQTL/GWAS study mapped a regulatory variant near `ZNF329` but
did not establish ZNF329 as a liver effector gene (Pandey et al. 2024, HGG
Advances, DOI `10.1016/j.xhgg.2024.100275`).  A brain-tumor network paper
predicted a ZNF329/RB1 relation from expression data only (Zhang et al. 2016).
Those records support generic DNA-binding capacity but do not establish an
obligate partner, neuronal lineage-maintenance role, stress pathway, or
highly expressed postnatal thalamic target set.

The causal transfer model therefore ends early.  The intervention is acute,
mosaic loss of Zfp329; its direct consequence should be reduced Zfp329 protein
in edited postmitotic neurons.  There is no evidence that this impairs the same
limiting transcriptional machinery as Zfp423, Zfp236, Setdb1, or Zfp148 in
`151 TH Prkcd Grin2c Glut`, and the training perturbations show that most
simple Zfp losses leave zero FDR-significant genes under this assay and power.
The strongest mechanistically relevant prior is the local empirical null:
25/31 Zfp/Zscan training targets were exact zeros at FDR 0.05, and the two
one-DEG cases did not show a broad downstream state.

I therefore predicted no FDR-significant genes for held-out `Zfp329`:

| target_name | predicted_n_degs |
| --- | ---: |
| Zfp329 | 0 |

## Limits

This is an extrapolation for an understudied gene, not an expression-signature
match: the held-out Zfp329 perturbation has no rows in the supplied Parquet.
The zero prediction leans on the high background rate of exact-zero focal
responses among non-held-out Zfp perturbations and on absence of a known
Zfp329-specific neuronal program.  That absence is weaker than positive
biology: a private Zfp329 target set in the thalamic Prkcd/Grin2c population,
a guide design with unusually efficient protein disruption, or a single
self-transcript FDR hit like `Zfp692` could make the true count low but
nonzero.  Conversely, the assay observes only nuclei recovered 3-4 weeks after
P16 AAV CRISPR, so a survival or migration effect before snRNA-seq would not
necessarily appear as a large survivor-state DEG count.
