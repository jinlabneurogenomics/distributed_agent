# Hnrnpa1 DEG-count prediction

## Question and endpoint

I interpreted the task as one scalar point prediction: estimate the number of measured
genes that would have `pvals_adj < 0.05` after acute AAV-CRISPR loss of
`Hnrnpa1` in `151 TH Prkcd Grin2c Glut` thalamic glutamatergic neurons.
`Hnrnpa1` was the only requested held-out target:

```text
target_name
Hnrnpa1
```

The held-out `Hnrnpa1` perturbation is absent from the declared differential
expression Parquet and from the focal training-count CSV. I therefore treated
the focal training counts as direct endpoint observations for non-held-out
analogs and the same-experiment report corpus as packaged interpretation of
those same measurements, not as independent replication. I did not use measured
self-target mRNA loss as editing-efficiency evidence.

## Sources used

- Declared focal training counts:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`
- Declared differential-expression Parquet:
  `training differential-expression dataset`
- Run-local requested targets:
  `single-target request for Hnrnpa1`
- Internal corpus: `perturbai-july-260713-sourceguard-1773-v1`, queried with
  `corpus.findings`, `corpus.direct_evidence`, and `corpus.report_evidence`.
- External literature from PubMed:
  - Kim et al. 2013, Nature, doi:10.1038/nature11922, PMID:23455423.
  - Levengood and Tolbert 2018, Semin Cell Dev Biol,
    doi:10.1016/j.semcdb.2018.04.001, PMID:29625167.
  - Tilliole, Fix and Godin 2024, Front Mol Neurosci,
    doi:10.3389/fnmol.2024.1411639, PMID:39086926.
  - Dargan et al. 2025, Nucleic Acids Res, doi:10.1093/nar/gkaf709,
    PMID:40737092.

## Dataset checks and computed quantities

The focal training endpoint table contained 1,674 non-held-out targets. The
distribution was strongly zero-inflated and right-skewed: median `n_degs = 0`,
75th percentile `= 1`, 90th percentile `= 2`, 95th percentile `= 18`, and
maximum `= 2677`.

I filtered the Parquet to `group_name == "151 TH Prkcd Grin2c Glut"` and
candidate RNA-binding or spliceosome perturbations, then counted
`pvals_adj < 0.05` per `gene_target`. These Parquet-derived focal counts
matched the training-count CSV for the analogs below:

| training perturbation | focal `n_degs` | reason considered |
| --- | ---: | --- |
| `Hnrnpa2b1` | 11 | closest measured paralog/functionally paired A/B hnRNP |
| `Hnrnpdl` | 1 | measured hnRNP-family weak counterexample |
| `Hnrnph2` | 4 | measured hnRNP-family weak counterexample |
| `Hnrnpc` | 122 | hnRNP-family but C-tetramer, much broader and mechanistically less direct |
| `Matr3` | 149 | disease-linked nuclear RBP, broader ER/RNA-processing state |
| `Tardbp` | 210 | disease-linked RBP, broader ER/RNA-processing state |
| `Hnrnpu` | 733 | hnRNP-family but SAF-A/chromatin-associated, very broad |
| `Prpf6` | 454 | spliceosome tri-snRNP perturbation, high-count RNA-processing counterexample |
| `Cdc40` | 624 | spliceosome assembly perturbation, high-count counterexample |
| `U2af2` | 828 | core splice-site factor, high-count counterexample |
| `Rnpc3` | 868 | minor spliceosome factor, high-count counterexample |

The exact focal DE rows also showed that `Hnrnpa2b1` was not just a generic
flat target: its strongest significant changes included `Rbm25` up
(`logFC = 0.369`, FDR `1.13e-5`) and `Hnrnpa1` up (`logFC = 1.080`,
FDR `2.98e-5`), with only 11 total focal FDR<0.05 genes. That is evidence for
a small but detectable RNP rebalancing state around the A/B hnRNP subfamily.

Packaged same-experiment evidence refined the comparison:

- The Hnrnpa2b1 report stated that the strongest Hnrnpa2b1-responsive RNP genes
  point to compensatory RNP-family rebalancing: `Hnrnpa1` was up in both main
  glutamatergic responders, `Hnrnpu` was down in two responders, and `Rbm25`,
  `Tcerg1`, and `Drosha` rose in the thalamic responder.
- The same report found that Hnrnpa2b1 had no robust whole-transcriptome
  signature neighbor; its top positive and negative cosine similarities were
  only +0.0358 and -0.0226.
- Hnrnpa2b1 was far weaker than `Hnrnpu`, `Tardbp`, `Matr3`, and `Hnrnpc`:
  within Hnrnpa2b1-matched groups those perturbations generated 2096, 670,
  555, and 260 FDR<0.10 downstream calls, respectively.
- The Hnrnpc report explicitly treated measured hnRNP-family perturbations as
  non-interchangeable: `Hnrnpa2b1`, `Hnrnph2`, and `Hnrnpdl` were almost flat,
  while `Hnrnpu` was broad but directionally mixed relative to `Hnrnpc`.

## Target-specific reasoning

### Hnrnpa1

`Hnrnpa1` encodes the abundant hnRNP A1 RNA-binding protein. It shares an
A/B-subfamily architecture and low-complexity prion-like biology with
HNRNPA2B1; pathogenic low-complexity-domain variants in both HNRNPA1 and
HNRNPA2B1 can drive multisystem proteinopathy/ALS-like RNP aggregation
(Kim et al. 2013). HnRNP A1 itself binds many RNA sequences and participates in
alternative splicing, RNA stability, export, and translation control
(Levengood and Tolbert 2018), and hnRNP-family proteins have important but
divergent neural roles (Tilliole et al. 2024).

The causal transfer I used was:

1. The intervention is acute mosaic loss of `Hnrnpa1`.
2. The direct consequence should be reduced HNRNPA1 function in postmitotic
   neurons, not a clean knockout of every cell and not necessarily a visible
   drop in nuclear `Hnrnpa1` RNA.
3. Loss should propagate mainly through A/B-subfamily RNA binding and splicing
   programs, with compensation by related hnRNPs expected to blunt many
   transcript-abundance changes.
4. The endpoint is survivor-conditioned whole-gene DE after 3-4 weeks, so
   isoform or local-translation effects can occur without producing many
   whole-gene FDR calls.

The closest endpoint-bearing training perturbation is `Hnrnpa2b1`, not the
large-count core spliceosome genes. `Hnrnpa2b1` knockout directly induced
`Hnrnpa1` in the same focal cells and produced a compact RNA/RNP compensation
signature, but only 11 FDR<0.05 DEGs. That makes a zero prediction too
pessimistic for `Hnrnpa1`; however, it argues against projecting the hundreds
of DEGs seen for `Hnrnpc`, `Hnrnpu`, `Tardbp`, `Matr3`, `U2af2`, `Prpf6`,
`Cdc40`, or `Rnpc3`. Those counterexamples either are different hnRNP
subfamilies with different binding and chromatin/particle roles or core
spliceosome factors whose perturbation changes the focal transcriptome much
more broadly.

External neuronal loss-of-function evidence also points to a real but
moderate effect rather than a broad spliceosome-like shock: Dargan et al. 2025
found that hnRNPA1 knockdown in iPSC-derived neurons altered neuritic mRNA and
protein localization more modestly than TDP-43 loss, plausibly because of
compensation by HNRNPA3. This is not the same assay or cell type, so I used it
only to support the expectation that Hnrnpa1 loss can be buffered at the
whole-gene level.

I therefore predicted a low positive focal response, close to the observed
`Hnrnpa2b1` count but slightly above it because HNRNPA1 is the abundant,
prototypic A/B hnRNP and direct perturbation should not require the reciprocal
compensation seen when `Hnrnpa2b1` is lost.

Final point prediction: `14` DEGs.

## Limitations

This prediction is an extrapolation because `Hnrnpa1` itself was completely
held out; there is no `Hnrnpa1` signature to correlate with visible
perturbations. The strongest within-family anchor is `Hnrnpa2b1`, but it is not
an obligate complex partner, and A/B-subfamily redundancy means reciprocal
compensation need not be symmetric. The available Parquet endpoint is
whole-gene differential expression in recovered nuclei, so it will miss
isoform changes, RNA localization, local translation, stress-granule dynamics,
or selection before nuclear capture unless those processes become detectable
gene-abundance shifts in `151 TH Prkcd Grin2c Glut` cells.
