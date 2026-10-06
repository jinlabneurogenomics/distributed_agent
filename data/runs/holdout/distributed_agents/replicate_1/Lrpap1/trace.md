# Lrpap1 held-out DEG-count prediction

## Question and endpoint alignment

I interpreted the requested endpoint as the exact focal-cell scalar used in
`151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`: the number of measured
transcripts with `pvals_adj < 0.05` after BH correction for a given knockout in
`151 TH Prkcd Grin2c Glut` nuclei. `Lrpap1` was held out as a perturbation, so
its own signature and count are absent from both the differential-expression
Parquet and the training-count table. The endpoint for the visible perturbations
is directly observed by the training count CSV; for `Lrpap1` it is absent and
must be predicted from within-dataset analogs plus external gene-function
knowledge.

The atlas Parquet, the PerturbAI July release
`perturbai-july-260713-sourceguard-1773-v1`, and its Findings reports are
different representations of the same Perturb-seq experiment. I used the
Parquet/count CSV for numerical calibration and the packaged corpus only as a
same-experiment interpretive layer, not as independent replication.

## Sources used

- Declared focal training counts:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared all-cell differential-expression Parquet:
  `training differential-expression dataset`.
- Internal same-experiment corpus: PerturbAI July release
  `perturbai-july-260713-sourceguard-1773-v1`, queried for visible `Lrp1`,
  `Lrp6`, `Vldlr`, and `Lrpap1` Findings. `Lrpap1` had no visible report;
  `Lrp1:F005`, `Lrp6:F001-F004`, and `Vldlr:F001-F002` were the most relevant
  receptor-family comparisons.
- PubMed through NCBI E-utilities, queried on 2026-09-03, for external
  molecular priors:
  - Willnow et al. 1995, PMID 7538675, DOI 10.1073/pnas.92.10.4537:
    gene-targeted RAP-deficient mice have reduced mature processed LRP in liver
    and brain.
  - Bu et al. 1995, PMID 7774585, DOI 10.1002/j.1460-2075.1995.tb07221.x:
    RAP is retained in the ER and transiently complexes with LRP during
    biosynthesis.
  - Willnow et al. 1996, PMID 8654360: RAP acts as a specialized chaperone that
    prevents ligand-induced ER retention and degradation of LDL
    receptor-related endocytic receptors.
  - Bu and Rennke 1996, PMID 8703036, DOI 10.1074/jbc.271.36.22218: RAP promotes
    folding of LRP ligand-binding domains and prevents improper intermolecular
    disulfide-linked aggregation.
  - Benhayon et al. 2003, PMID 12670700, DOI 10.1016/s0169-328x(03)00032-9:
    Reelin binding to the LDL-receptor-family members ApoER2/LRP8 and VLDLR
    mediates DAB1 phosphorylation in cortical neurons.

## Quantitative calibration and analog search

I first read the 1,674 visible focal perturbations in the training count CSV.
The response was extremely sparse:

| focal training distribution | value |
| --- | ---: |
| `n_degs = 0` | 1,205 / 1,674 |
| median | 0 |
| 75th percentile | 1 |
| 90th percentile | 2 |
| 95th percentile | 18 |
| maximum | 2,677 |

Then I queried the focal-cell Parquet rows for receptor and endocytic analogs
of RAP/LRPAP1. The relevant filter was simply:

```python
(group_name == "151 TH Prkcd Grin2c Glut") &
gene_target.isin(["Lrp1","Lrp2","Lrp4","Lrp5","Lrp6","Lrp8","Vldlr",
                  "Reln","Dab1","Sorl1","Sort1","Cltc","Rab7",
                  "Vps35","Vps54","Ap1b1","Atp6v0a1","Scarb2"])
```

This pulled 17,259 measured genes per visible perturbation. The focal
FDR<0.05 counts that entered the `Lrpap1` decision were:

| visible perturbation | focal `n_degs` | relationship to `Lrpap1` |
| --- | ---: | --- |
| `Lrp1` | 0 | canonical RAP client LDL-receptor-family endocytic receptor |
| `Lrp2` | 0 | megalin/LRP2, another LDL-receptor-family RAP client |
| `Lrp8` | 0 | ApoER2, Reelin receptor and LDLR-family member |
| `Vldlr` | 0 | Reelin receptor and LDLR-family member |
| `Lrp4` | 0 | LDLR-family receptor |
| `Lrp5` | 0 | Wnt co-receptor paralog of `Lrp6` |
| `Lrp6` | 4 | LDLR-family Wnt co-receptor; small Wnt-flavored focal response |
| `Reln` | 0 | upstream ligand for VLDLR/LRP8-DAB1 signaling |
| `Dab1` | 0 | receptor-proximal Reelin adaptor |
| `Sorl1` | 0 | neuronal sorting receptor linked to LRP1/APP biology |
| `Sort1` | 0 | related sorting receptor |
| `Ap1b1` | 1 | adaptor-mediated receptor sorting control |
| `Cltc` | 3 | general clathrin-mediated endocytosis control |
| `Vps35` | 17 | retromer trafficking positive counterexample |
| `Vps54` | 31 | GARP/endosomal trafficking positive counterexample |
| `Rab7` | 501 | late endosome/autophagosome-lysosome positive counterexample |

The score-vector correlations among the receptor-proximal perturbations were
also near zero in this cell group: for example `Vldlr` versus `Lrp8` was 0.015,
`Vldlr` versus `Reln` was 0.022, `Vldlr` versus `Dab1` was 0.001, `Lrp1` versus
`Lrp8` was -0.018, and `Lrp5` versus `Lrp6` was -0.006 by Spearman correlation
over Wilcoxon scores for all 17,259 focal measured genes. Thus the zero counts
were not hiding a shared weak receptor-family signature just below the
BH-threshold. By contrast, the assay did detect broad trafficking-associated
states when a perturbation affected a limiting endosomal function: `Rab7`,
`Vps54`, and `Vps35` generated 501, 31, and 17 focal DEGs respectively.

## Lrpap1-specific reasoning

`Lrpap1` encodes RAP, an ER-resident chaperone for LDL receptor-related proteins.
The primary intervention expected from acute Cas9 disruption is loss of RAP
protein, followed by less efficient folding/export and lower mature surface
abundance of a subset of LRP-family receptors. Willnow et al. showed that
RAP-deficient mice have reduced mature LRP in brain and liver, while Bu et al.
and Willnow et al. showed mechanistically that RAP binds nascent LRP-class
receptors in the secretory pathway and prevents premature ligand-triggered
aggregation or degradation.

That biology makes the visible LRP-family receptors the closest same-assay
analogs. In the exact focal group, however, every single-receptor perturbation
expected to capture the main RAP-dependent pathways was transcriptionally quiet
or nearly quiet: `Lrp1`, `Lrp2`, `Lrp8`, and `Vldlr` each had 0 DEGs at
FDR<0.05, and the upstream/adaptor Reelin pathway controls `Reln` and `Dab1`
also had 0. The internal `Vldlr` report reached the same conclusion at the
broader FDR<0.10 level: acute P16 `Vldlr` loss, `Reln`, `Lrp8`, and `Dab1`
did not form a shared postmitotic juvenile snRNA transcriptional module. The
internal `Lrp1` report similarly found only sparse, non-focal `Vgf` effects and
explicitly noted that `Lrp2`, `Lrp4`, `Lrp5`, `Lrp6`, `Lrp8`, `Vldlr`, `Sorl1`,
and `Sort1` did not phenocopy `Lrp1`.

I treated `Lrp6` as a counterexample rather than a reason to make a larger
`Lrpap1` prediction. `Lrp6` had 4 FDR<0.05 focal DEGs and a curated small
151-restricted Wnt/beta-catenin signature, including `Axin2` down-regulation,
whereas its paralog `Lrp5` was flat. That signature depends on an LRP5/6-Frizzled
canonical Wnt receptor complex and does not imply that loss of the ER chaperone
for LRP endocytic receptors will recreate the same thalamic response.

I also treated `Rab7`, `Vps35`, `Vps54`, and `Cltc` as falsifying controls for
over-generalization. Their positive counts show that perturbing trafficking can
be visible in `151 TH Prkcd Grin2c Glut`, but they act downstream or broadly
across late endosomes, retromer, GARP, and clathrin-coated vesicles. RAP loss is
upstream and receptor-selective. Because its closest visible client receptors
were silent, broad trafficking knockouts do not predict a late-endosomal stress
program for `Lrpap1`.

The resulting causal transfer chain was:

`Lrpap1` knockout -> impaired RAP chaperoning in the ER -> reduced functional
LRP/VLDLR/LRP8/LRP2-family receptor trafficking rather than direct disruption
of late endosomes -> limited exposure of these receptor pathways in recovered
postmitotic thalamic glutamatergic nuclei -> no broad survivor-state DEG
program sampled at P37-P44.

Given the 72% zero rate across all training perturbations, zero DEG counts for
the most direct receptor clients, zero counts for the Reelin ligand/adaptor
axis, and only tiny counts for receptor sorting controls, I predict that
`Lrpap1` will also have no measured focal gene passing BH FDR 0.05.

## Final point prediction

| target | predicted `n_degs` |
| --- | ---: |
| `Lrpap1` | 0 |

## Limits and uncertainty

The largest uncertainty is that `Lrpap1` itself was unobserved. RAP loss can
simultaneously reduce several receptors, so the perturbation is not identical
to `Lrp1`, `Vldlr`, or `Lrp8` loss one at a time. The Parquet also reports
nuclear mRNA among recovered nuclei, not mature receptor protein, ligand
binding, Dab1 phosphorylation, Reelin-dependent migration, lipid uptake, or
pre-assay selection. Most external RAP evidence came from germline animals,
non-neuronal tissues, or biochemical systems with stronger and longer target
loss than the AAV mosaic juvenile CRISPR design. Therefore the zero prediction
means "no focal postmitotic snRNA DEG is expected to clear FDR 0.05 in this
assay"; it does not mean that LRPAP1 is biologically inert or that receptor
trafficking would be normal at the protein level.
