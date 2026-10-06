# Prediction trace for Hsf4

## Question and endpoint

I interpreted the task as a count prediction for the held-out perturbation
`Hsf4` in `151 TH Prkcd Grin2c Glut` neurons.  The endpoint is the number of
measured genes whose Wilcoxon `pvals_adj` is below 0.05 in the focal cell group.
The held-out perturbation itself is absent from both the training count table and
the differential-expression Parquet, so the count has to be inferred from
training perturbations and external gene-function evidence.

There is one ambiguity: a heat-shock factor could be scored either as another
member of the mammalian heat-shock transcription-factor family or as a
cell-type-specific lens/retina developmental regulator.  I used the second
interpretation for `Hsf4`, because the neuronal training screen directly shows
that basal Hsf1 loss produces only a small constitutive chaperone signature, and
the HSF4 literature assigns most Hsf4 loss-of-function transcriptional effects
to lens epithelial/fiber differentiation rather than to the basal neuronal
Hsf1-driven heat-shock response.

## Sources

- Declared training counts:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared differential-expression table:
  `training differential-expression dataset`.
- Requested target manifest:
  `single-target request for Hsf4`.
- Internal same-experiment semantic corpus:
  `perturbai-july-260713-sourceguard-1773-v1`; specifically the Hsf1 Findings,
  Evidence, and References resolved with `corpus.findings` and
  `corpus.report_evidence`.
- External biological literature from PubMed:
  - Pincus 2020, `doi:10.1007/978-3-030-40204-4_3`, for HSF1 regulation of the
    heat-shock response.
  - Trinklein et al. 2004, `doi:10.1091/mbc.E03-10-0738`, for mammalian
    HSF1-dependent heat-shock target genes.
  - Shi et al. 2009, `doi:10.1186/1471-2199-10-10`, for mouse Hsf4 loss causing
    cataracts through down-regulation of Crygs and Bfsp lens genes.
  - Cui et al. 2016, `doi:10.1016/j.biocel.2016.08.022`, for HSF4 control of
    small heat-shock proteins including HSP25 and alpha B-crystallin in mouse
    lens epithelial cells.
  - Cui et al. 2019, `doi:10.1016/j.bbagen.2019.129496`, and Zhang et al. 2023,
    `doi:10.1167/iovs.64.7.5`, for HSF4-linked lysosomal and autophagy programs
    during lens development.

The Parquet and the July corpus are different representations of the same
Perturb-seq experiment; I did not treat agreement between them as independent
replication.

## Dataset calculations

I first summarized the focal training count table.  It contained 1,674
non-held-out perturbations, of which 1,205 had `n_degs=0`.  The median count was
0 and the 75th percentile was 1, so a held-out gene needs a close, active
neuronal analog to justify moving above zero.  The Hsf/chaperone-axis training
counts in the focal group were:

| training target | observed n_degs |
| --- | ---: |
| Hsf1 | 6 |
| Hspa8 | 9 |
| Hspa5 | 5 |
| Hsp90ab1 | 1 |
| Dnajc13 | 1 |
| Dnajc5 | 1 |
| Dnajb4 | 0 |
| Dnajb6 | 0 |
| Dnajc19 | 0 |

For the signature check I filtered the Parquet to
`group_name = '151 TH Prkcd Grin2c Glut'` and counted
`pvals_adj < 0.05`; for mechanistic comparisons I also listed the exact
significant genes for the Hsf/chaperone perturbations.  The relevant query was:

```sql
SELECT gene_target, names, logfoldchanges, scores, pvals_adj,
       n_pert_matched, n_ctrl_matched
FROM read_parquet('training_de_all_cell_groups.parquet')
WHERE group_name = '151 TH Prkcd Grin2c Glut'
  AND gene_target IN ('Hsf1','Hsp90ab1','Hspa8','Hspa5',
                      'Dnajc5','Dnajc13','Dnajb4','Dnajb6')
  AND pvals_adj < 0.10
ORDER BY gene_target, pvals_adj, names;
```

The closest represented transcription-factor analog was `Hsf1`, not `Hsf4`.
`Hsf1` had 6 genes below FDR 0.05 in 151 TH cells, all down:
`Hsph1` logFC -0.484, `Hsp90aa1` -0.282, `Rsrp1` -0.175, `Hsp90ab1`
-0.345, `Mat2a` -0.234, and `Ahsa2` -0.294.  The July Hsf1 report interprets
that as a restricted basal HSP90/HSP110 co-chaperone module rather than a broad
heat-shock, unfolded-protein-response, proteasome, apoptosis, or mitochondrial
stress cascade; its canonical inducible HSR and UPR sentinels such as `Hspa1a`,
`Hspa1b`, `Hspa5`, `Hsp90b1`, `Atf3`, `Atf4`, `Ddit3`, `Xbp1`, `Herpud1`, and
`Ppp1r15a` were not FDR-significant in the Hsf1 responder groups.

The chaperone perturbations did not support a broad stress phenotype either.
`Hsp90ab1` had a single FDR<0.05 focal hit, its own transcript; `Hspa8` had nine
hits and induced `Dnaja1`, `Hspa4l`, `Syt4`, `Hsp90aa1`, and `Cct6a`, opposite
to Hsf1 on the HSP90 arm; `Hspa5`, an ER Hsp70, had five FDR<0.05 hits and an
UPR-like increase of `Hsp90b1`, `Nfe2l1`, `Pdia4`, and `Derl3`; and the two
represented Dnaj perturbations with focal effects, `Dnajc5` and `Dnajc13`, were
self-transcript-only 1-DEG hits.

The same-experiment Hsf1 report also recorded a full-Parquet availability
check: `Hsf2`, `Hsf4`, `Hspa1a`, `Hspa1b`, `Hsp90aa1`, `Hsph1`, `Ahsa2`,
`Stip1`, `Rsrp1`, and `Mat2a` had zero rows as `gene_target` perturbations.
Thus there was no directly measured `Hsf4` or `Hsf2` signature available for
interpolation.

## Hsf4 reasoning

The mechanistic transfer chain I used was:

`Hsf4` CRISPR loss of function -> reduced HSF4 transcription-factor output ->
only genes under constitutive HSF4 control in young thalamic neurons can change
3-4 weeks later -> the recovered NeuN-positive nuclei are tested by snRNA-seq
against non-targeting controls -> the point prediction is the number of genes
that cross BH FDR 0.05.

The positive analog is weak.  HSF1 and HSF4 are both heat-shock-factor DNA
binding proteins, but the training screen says that even loss of the canonical
neuronal HSF1 stress-response factor reaches only six focal DEGs and those are
all a constitutive HSP90/HSP110 co-chaperone output.  That places an upper
anchor for a basal heat-shock transcription factor in this postnatal neuronal
assay near the single-digit DEG range.  `Hspa8`, `Hspa5`, and `Hsp90ab1` are
nearby proteostasis counterexamples: perturbing important chaperones produced
small, different signatures and did not recreate the Hsf1 loss program.

The causal sign is also not transferable from Hsf1 to Hsf4.  HSF4 is best
established as a lens differentiation factor: Hsf4 knockout mice develop
cataracts and down-regulate lens structural targets such as `Crygs`, `Bfsp1`,
and `Bfsp2` (Shi et al. 2009), HSF4 regulates small heat-shock/lens
proteostasis genes including alpha B-crystallin in lens epithelial cells (Cui
et al. 2016, 2019), and more recent work links HSF4 to lens autophagy and
organelle-clearance targets such as `Atg9a` (Zhang et al. 2023).  Those
transcriptional consequences sit in eye lens cells and are coupled to lens
terminal differentiation and organelle clearance.  The assayed population here
is postmitotic NeuN-positive thalamic glutamatergic neurons harvested after a
juvenile acute brain CRISPR perturbation, so the key HSF4 lens/retina module is
not an obligate or directional dependency in the relevant context.

I therefore used the six-DEG `Hsf1` result only as a ceiling for the closest
available family member, and then down-weighted from it because Hsf4 is less
likely than Hsf1 to carry basal HSP90/HSP110 transcription in thalamic neurons.
With the focal training distribution dominated by exact zeros, and with
`Hsp90ab1`, `Dnajc5`, `Dnajc13`, `Dnajb4`, and `Dnajb6` showing that
proteostasis-related perturbations often produce either a self hit or no focal
DEGs, my point prediction for `Hsf4` is:

| target | predicted n_degs |
| --- | ---: |
| Hsf4 | 0 |

## Limits

This is extrapolation from a held-out gene with no direct Parquet signature.
The strongest internal evidence is the small `Hsf1` signature; that is family
and pathway evidence, not an obligate same-gene or same-complex transfer.  HSF4
could have unannotated basal targets in thalamic neurons, and a single very
strong self-transcript change would be counted if it crossed FDR, but there was
no within-dataset support for a broad HSF4-like state.  The external HSF4
literature is concentrated in lens and, to a lesser extent, retina biology, so
its main contribution here is negative context: it explains why the known
loss-of-function module is unlikely to be exposed in the sampled postnatal
brain nuclei.
