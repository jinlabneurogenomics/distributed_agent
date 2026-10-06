# DEG-count prediction trace

## Question and resolution

The task asks for a point prediction of `n_degs` for each requested held-out
perturbation in the `151 TH Prkcd Grin2c Glut` focal cell group. I interpreted
`n_degs` exactly as the supplied focal training table defines it: the count of
measured genes with Scanpy/Wilcoxon Benjamini-Hochberg adjusted `pvals_adj <
0.05` in perturbed nuclei versus matched non-targeting controls. The requested
manifest has one held-out target, in order:

```text
Fnip1
```

This is a scalar held-out DEG-count prediction, not a ranking problem. `Fnip1`
is absent from the training focal count table and absent as a `gene_target` in
the supplied differential-expression parquet, so its own expression signature
and true DEG count were not used.

## Sources used

- Declared training DEG counts:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
  The file has 1,674 non-held-out perturbations; the focal endpoint is sparse
  with median 0 DEGs, mean 14.05, maximum 2,677, and 469/1,674 nonzero
  perturbations.
- Declared differential-expression parquet:
  `training differential-expression dataset`.
  I filtered this file to `group_name == "151 TH Prkcd Grin2c Glut"` and to
  mechanistically relevant training perturbations to inspect the actual
  FDR-significant genes, log2 fold changes, Wilcoxon scores, and matched-cell
  counts.
- Internal corpus: July PerturbAI same-experiment report corpus,
  `july_260713_sourceguard_1773_v1`, via `corpus.report_evidence` and bounded
  Finding/report lookups for measured anchors such as `Depdc5`, `Tsc2`, `Mtor`,
  `Prkaa2`, and `Rab7`. These reports are interpretations of the same training
  experiment, not independent replication.
- External mechanism priors from PubMed:
  Baba et al. 2006, PNAS, DOI `10.1073/pnas.0603781103`, PMID `17028174`;
  Tsun et al. 2013, Molecular Cell, DOI `10.1016/j.molcel.2013.09.016`,
  PMID `24095279`; Ramirez et al. 2019, Journal of Immunology, DOI
  `10.4049/jimmunol.1900395`, PMID `31676673`; Ramirez Reyes et al. 2021,
  Frontiers in Cell and Developmental Biology, DOI `10.3389/fcell.2021.667311`,
  PMID `33981707`. I also used the Reactome "Energy dependent regulation of
  mTOR by LKB1-AMPK" pathway definition as referenced in the internal
  `Prkaa2` report.

## Computation over the training data

The parquet is row-grouped by cell class, so I read only focal rows for a small
mechanistic panel:

```python
tbl = ds.dataset(parquet, format="parquet").to_table(
    columns=[
        "names", "scores", "logfoldchanges", "pvals", "pvals_adj",
        "group_name", "gene_target", "n_pert_matched", "n_ctrl_matched",
    ],
    filter=(ds.field("group_name") == "151 TH Prkcd Grin2c Glut")
           & ds.field("gene_target").isin(targets),
)
```

For each analog I then counted focal rows with `pvals_adj < 0.05` and inspected
the significant genes and selected mTOR/FLCN/Rag/sterol coordinates.

## Target-specific reasoning

### Fnip1

**Mechanism prior.** `Fnip1` encodes folliculin-interacting protein 1. FNIP1 was
identified as an FLCN-binding AMPK interactor by Baba et al. 2006. The
FLCN-FNIP1/FNIP2 complex is a GAP for RagC/D and links amino-acid sensing at
lysosomes to mTORC1 activation and to TFEB/TFE3 repression (Tsun et al. 2013;
Ramirez Reyes et al. 2021). In Fnip1-deficient B-cell progenitors, Ramirez et
al. 2019 observed abnormal mTOR lysosomal localization under nutrient stress,
increased TFE3 nuclear localization, induction of TFE3 target lysosomal genes,
and increased autophagic flux. That makes `Fnip1` a real nutrient-sensing and
lysosomal transcription candidate, but it does not make its acute partial loss
identical to removing every FLCN-FNIP function in postmitotic thalamic neurons:
FNIP2 can also bind FLCN, and the B-cell evidence is developmental and immune
rather than 3-4 week neuronal CRISPR loss of function.

**Closest measured same-assay analogs.**

- `Depdc5`, 13 DEGs in the focal training count table, is the closest measured
  same-direction mTORC1 amino-acid brake. The internal `Depdc5` report describes
  a `151 TH Prkcd Grin2c Glut`-restricted response in which loss of GATOR1
  induced sterol and PI3K-feedback genes. At FDR 0.05 in the focal parquet,
  `Depdc5` up-regulated `Pik3r1`, `Ldlr`, `Pik3r3`, `Tubb3`, `Tubb4b`,
  `Insig1`, `Hmgcs1`, and `Msmo1`, and down-regulated `Amy1`, `Rnpc3`, and
  `Snhg11`. Because DEPDC5 is an obligate GATOR1 subunit upstream of Rag
  signaling, a true FLCN/FNIP effect should touch a related amino-acid sensing
  branch; however `Fnip1` is an adaptor with a paralog and acts at FLCN/RagC-D
  rather than the GATOR1 brake, so the causal chain predicts a weaker or
  partially divergent response.
- `Tsc2`, 86 focal DEGs, is a broader same-sign negative-regulator anchor.
  The same-experiment corpus reports a caudal metabolic/lysosomal Tsc2-loss
  program with sterol and lysosomal transcripts. In the focal DE rows, `Tsc2`
  significantly induced `Cyp51`, `Pik3r3`, `Ldlr`, `Msmo1`, `Pik3r1`, `Ddit4`,
  and `Rragd`, and it shared eight FDR 0.05 genes with `Depdc5` in the same
  cell group: `Amy1`, `Ldlr`, `Msmo1`, `Pik3r1`, `Pik3r3`, `Rnpc3`, `Snhg11`,
  and `Tubb3`. `Tsc2` is not a direct count template for `Fnip1`, though,
  because TSC loss derepresses Rheb-mTORC1 and generated a much broader
  stress/metabolic state than the GATOR1 branch.
- `Rab7`, 501 focal DEGs, is an endolysosomal counterexample. The internal
  Rab7 report shows a dominant 151-cell lysosomal and sterol response and
  strong same-direction overlap with `Tsc2`. I used it to recognize that
  sterol/lysosome genes are detectable in this assay, not to set the `Fnip1`
  count, because Rab7 loss directly perturbs late-endosome trafficking and
  lysosomal positioning.
- `Srebf2`, 7 focal DEGs, gives a lower sterol-axis scale in the same training
  table and the `Depdc5` report treats it as the expected opposite-sign
  transcription factor for the Depdc5/Tsc2 sterol arm.
- Several obvious counterexamples were flat or nearly flat in the focal
  endpoint: `Mtor` had 2 DEGs (`Rims3` up and `Tmed8` down), `Rb1cc1` had 4,
  `Fkbp1a` had 1, and `Rptor`, `Akt3`, `Pik3r1`, `Pik3r2`, `Pik3cb`, `Prkaa2`,
  `Prkag2`, `Atg5`, `Atg16l1`, and `Becn1` had 0. The internal reports for
  `Mtor` and `Prkaa2` explicitly note that canonical mTOR/AMPK/autophagy
  pathway neighbors did not phenocopy the strong `Tsc2` or `Rab7` signatures
  in this P16 sparse neuronal assay.

**Expression-pattern evidence for the local mTOR/FNIP coordinates.** In the
focal cell group, `Depdc5` loss and `Tsc2` loss both lifted a sterol/PI3K
feedback subset, but only `Tsc2` detectably raised one Rag transcript:
`Rragd` was significant for `Tsc2` with log2 fold change 0.728 and FDR 0.029,
while `Fnip1`, `Fnip2`, `Flcn`, `Rraga`, `Rragb`, and `Rragc` were not
significant under either `Depdc5` or `Tsc2`. `Mtor`, `Rptor`, `Prkaa2`, `Atg5`,
`Becn1`, and `Rb1cc1` did not induce the sterol branch at FDR 0.05. This argues
against a large generic autophagy/mTOR count for `Fnip1`.

**Prediction.** I predict a small nonzero response, `Fnip1 -> 3 DEGs`.
The zero/nonzero call is driven by external FLCN/FNIP biology and by the
same-assay fact that `Depdc5` and `Tsc2` loss can expose an amino-acid,
sterol, and lysosomal response in exactly this cell group. The small magnitude
is driven by the stronger same-assay counterevidence: single perturbations of
several neighboring mTORC1, AMPK, and autophagy genes were FDR-flat, and
`Fnip1` loss is expected to be buffered by `Fnip2` more than DEPDC5 or TSC2
loss is buffered by same-complex paralogs.

## Limits and extrapolation

The major missing analogs are `Flcn` and `Fnip2`, which were not present as
focal training perturbations, so I could not observe the direct complex member
most likely to phenocopy `Fnip1` or the degree of FNIP paralog compensation in
this screen. The external FNIP1 papers measured biochemical, B-cell, muscle, or
reviewed cancer/metabolism settings; they establish the FLCN/FNIP/Rag/TFEB
chain but not its postnatal thalamic response breadth. The supplied data are
also survivor-conditioned single-nucleus RNA-seq after mosaic CRISPR, so a
flat or tiny count would not prove absent protein-level mTOR, AMPK, TFEB, or
autophagy effects. The final integer is therefore an extrapolation from
`Depdc5`, `Tsc2`, `Rab7`, and flat mTOR/autophagy counterexamples rather than a
validated proxy for Fnip1's exact endpoint.
