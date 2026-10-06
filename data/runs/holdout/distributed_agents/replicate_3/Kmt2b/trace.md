# Kmt2b held-out DEG-count prediction

## Question interpreted

The requested readout is the integer number of measured genes that would pass
Benjamini-Hochberg FDR 0.05 after acute AAV CRISPR loss of each held-out target
in `151 TH Prkcd Grin2c Glut` nuclei.  In this run the manifest contains one
held-out perturbation:

```tsv
target_name
Kmt2b
```

I treated the endpoint as the assay-specific breadth of the `151 TH Prkcd
Grin2c Glut` single-nucleus differential-expression response, not as a direct
measure of target importance, guide activity, viability, or developmental
phenotype severity.  Kmt2b itself was absent from both the training count CSV
and the DE parquet as a perturbation target, as expected for a held-out target.

## Sources used

- Training endpoint:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Training differential-expression parquet:
  `[local file: training_de_all_cell_groups.parquet]`.
- Held-out manifest:
  `[local file: 121_Kmt2b.csv]`.
- Distributed Agents corpus MCP, release
  `perturbai-july-260713-sourceguard-1773-v1`.  This corpus had same-experiment
  findings for Kmt2a, Kmt2c, Setd1a, Setd5, Kdm5c, Ep300, Chd8, and related
  chromatin regulators; it had no direct Kmt2b entry because Kmt2b was held out.
- Distributed Agents runtime `profile_compare` / `profile_cohort` over the focal-cell
  log fold-change profiles for a declared chromatin panel
  `{Kmt2a, Kmt2c, Setd1a, Setd5, Setdb1, Nsd1, Kdm5c, Ash1l, Ep300, Chd8}`.
  These profiles used `logfoldchanges` as signed values and `pvals_adj < 0.05`
  to mark significant genes.
- External literature was retrieved from NCBI PubMed through the filtered
  literature gateway:
  - Ladopoulos et al. 2013, PMID: 23358417, DOI: 10.1128/MCB.01721-12.
  - Jakovcevski et al. 2015, PMID: 25834037,
    DOI: 10.1523/JNEUROSCI.3004-14.2015.
  - Hu et al. 2017, PMID: 28157506, DOI: 10.1016/j.molcel.2017.01.013.
  - Kerimoglu et al. 2017, PMID: 28723559,
    DOI: 10.1016/j.celrep.2017.06.072.
  - Zech, Lam and Winkelmann 2019, PMID: 31768667,
    DOI: 10.1007/s11910-019-1007-y.

## Computational checks on the supplied training data

I first loaded the focal training-count CSV and summarized all 1,674 observed
perturbations.  The endpoint is sparse in this cell group: the median was 0
DEGs, the 75th percentile was 1, the 90th percentile was 2, the 95th percentile
was 18, and a small number of broad responders drove the mean to 14.1.

I then extracted the focal-cell rows from the parquet for KMT2-family and
chromatin regulators that could calibrate Kmt2b.  For each target I counted rows
with `pvals_adj < 0.05`, checked the matched perturbed-cell count, and inspected
the most significant genes.  The most relevant focal-cell DEG counts were:

```tsv
training_target	n_degs	n_pert_matched	relevance_to_Kmt2b
Kmt2a	24	161	closest represented KMT2A/B Trithorax paralog
Kmt2c	0	55	KMT2 family boundary; MLL3/Trr enhancer subfamily
Setd1a	368	154	H3K4 writer but SET1A subfamily and much broader state
Setdb1	22	113	non-H3K4 chromatin methyltransferase with similar-sized response
Nsd1	23	136	H3K36 methyltransferase with similar-sized response
Kdm5c	18	184	H3K4me eraser with similar-sized but opposite-axis response
Setd5	9	148	SET-domain neurodevelopmental regulator; smaller response
Ash1l	1	130	H3K36/MLL-linked regulator; essentially flat
Ep300	0	155	CBP/p300 enhancer acetyltransferase boundary
Chd8	61	197	active chromatin-NDD comparator, larger than Kmt2a
Crebbp	8	61	CBP/p300 paralog, small positive response
```

The Kmt2a focal signature was the cleanest within-dataset anchor.  It had 24
FDR<0.05 genes in 161 matched nuclei.  The strongest significant changes were
down-regulation of `Nr2f1`, `Pcdh7`, `Lhx9`, the target `Kmt2a`, `Camk2d`,
`Pcdh10`, `Grik2`, `Map1b`, and `Sox2`, plus a smaller induced branch including
`Igfbp5`, `Tnr`, `Cx3cl1`, `Atxn2l`, `Luc7l`, `Txndc5`, and `Gabrd`.  That
pattern is consistent with a selected thalamic identity/connectivity response
to loss of a promoter H3K4 writer.

I also compared the signed focal profiles of the chromatin panel.  The median
FDR-level significant-program overlap among the 45 selected pairs was zero.
Kmt2a shared only one positive FDR feature with Setd1a and none with Kmt2c,
Setd5, Setdb1, Nsd1, Kdm5c, Ash1l, Ep300, or Chd8.  This argues against pooling
all chromatin or H3K4-associated genes as one response class.  The Distributed Agents
same-experiment corpus reached the same conclusion for the measured H3K4
writers: Kmt2a did not phenocopy Setd1a or the nearly flat Kmt2c surface, and
Setd1a's closest data-driven neighbors were RNA-processing and
organelle-maintenance perturbations rather than Kmt2a/Kmt2c.

## Kmt2b-specific biological reasoning

KMT2B is a SET1/MLL, Trithorax-class H3K4 methyltransferase and a much closer
biochemical and evolutionary relative of KMT2A than of KMT2C/KMT2D or SETD1A.
Ladopoulos et al. showed that mouse KMT2B/MLL2 maintains active H3K4me3 and
RNA polymerase II association at a CpG-island promoter and protects that
promoter from DNA methylation.  Hu et al. showed that KMT2B/MLL2-COMPASS can
install H3K4me3 at promoters and a subset of non-TSS regulatory elements in
developmental contexts.  Those mechanisms make a nonzero RNA response plausible
after Kmt2b loss, especially in the `151 TH Prkcd Grin2c Glut` population where
the screen detected Kmt2a, Setd1a, Setdb1, Nsd1, Kdm5c, Setd5, Chd8, Crebbp,
Brd4, and Wac responses.

The closest observed perturbation is therefore Kmt2a rather than Setd1a or
Kmt2c.  Kmt2a produced a modest 24-gene focal response, not a hundreds-of-genes
collapse, and its Distributed Agents corpus entry described a sparse, glutamatergic-
biased surface concentrated in this TH group.  External postmitotic-neuron data
also favor treating Kmt2a and Kmt2b as related but not interchangeable:
Jakovcevski et al. found strong mature prefrontal phenotypes after neuronal
Kmt2a/Mll1 ablation, while the Kmt2b/Mll2 ortholog produced milder behavioral
phenotypes in that setting; Kerimoglu et al. directly compared hippocampal
Kmt2a and Kmt2b knockdown and found that both affect memory-related H3K4
methylation and gene expression, but at largely distinct genomic regions and
pathways.

The main counterexample is Kmt2c: it is in the KMT2 family, but it had zero
DEGs in `151 TH Prkcd Grin2c Glut` and only one robust FDR<0.10 gene across
the same-experiment Kmt2c surface.  Because KMT2C is in the MLL3/Trr
enhancer-H3K4me1 branch rather than the KMT2A/KMT2B Trithorax branch, I used it
as evidence that KMT2-family membership alone is insufficient, not as the
primary quantitative template.  Ep300, Kat6a, Kat6b, Dnmt3a, Ash1l, and Pogz
were additional flat or almost-flat chromatin counterexamples in the focal
group.  Conversely, Setd1a, Brd4, Wac, and Sin3a had 311 to 1,433 DEGs and
show that this cell group can mount very broad nuclear-factor signatures, but
their expression programs were not Kmt2a-like and they would overpredict a
Kmt2b effect.

Human KMT2B haploinsufficiency causes DYT-KMT2B childhood-onset dystonia with
epigenetic dysregulation, often from de novo truncating, frameshift, splice, or
deletion alleles, as summarized by Zech, Lam and Winkelmann.  That phenotype
supports KMT2B as a neuronal disease gene, but it is only indirect calibration
for this readout: germline human haploinsufficiency through development is not
the same as mosaic P16 CRISPR loss followed by basal snRNA-seq three to four
weeks later.

## Prediction

I predict a positive but narrow focal-cell response for Kmt2b.

- Zero/nonzero decision: nonzero.  KMT2B's direct Trithorax/H3K4 biology and
  the positive Kmt2a response make a flat result less likely than for Kmt2c or
  Ep300.
- Count calibration: just below the Kmt2a count of 24, in the same range as
  the measured Setdb1, Nsd1, and Kdm5c 18-23 DEG chromatin responses, and far
  below the Setd1a/Brd4/Wac/Sin3a outlier class.
- Point estimate: 20 FDR<0.05 DEGs.

## Limits

This is extrapolation from paralogs and pathway neighbors; Kmt2b itself has no
observed training signature and no Distributed Agents target-context entry in the
same-experiment corpus.  The exact KMT2B COMPASS subunits most informative for
acute loss, such as Wdr5, Rbbp5, Ash2l, Dpy30, Cxxc1/CFP1, Wdr82, Men1, or
Pagr1, were not represented in the training count table, and Kmt2d and Setd1b
were also absent.  KMT2A/KMT2B functions diverge by locus and neuronal context,
so even a Kmt2a-calibrated prediction could miss a TH-specific Kmt2b program.
Finally, the focal Wilcoxon DEG count is sensitive to matched nucleus counts,
guide performance, transcript detectability, and secondary states; a 20-gene
prediction should be read as "small but detectable", not as a claim that KMT2B
is biologically weak.
