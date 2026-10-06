# Kmt2e DEG-count prediction

## Question and endpoint

The requested prediction is the number of measured genes whose Wilcoxon
Benjamini-Hochberg adjusted p-value is below 0.05 after acute sparse CRISPR
loss of each held-out perturbation in `151 TH Prkcd Grin2c Glut` thalamic
glutamatergic neurons.  The supplied held-out manifest contains one target,
`Kmt2e`, and it is not present in the focal training-count CSV or as a
`gene_target` in the differential-expression Parquet.

I treated `n_degs` as an assay- and power-dependent FDR count in recovered
nuclei, not as a direct effect-size, viability, editing-efficiency, or target
self-knockdown measurement.  File order has no training semantics here because
there is a single unranked requested target.

## Sources used

- Direct training endpoint: `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`,
  containing the observed focal-cell `n_degs` for 1,674 non-held-out targets.
- Direct expression data: `training_de_all_cell_groups.parquet`, queried only
  for the visible KMT2/chromatin comparators named below.
- Run-local measurement and coverage metadata:
  `codex_runtime/pipeline/measurement_registry.json`,
  `task_bindings.json`, `coverage.json`, and `capabilities.json`.
- Same-experiment July 260713 sourceguard internal corpus:
  `corpus.findings`, `corpus.calibration`, `corpus.graph`, and
  `corpus.report_evidence`.  These reports are a curated interpretation layer
  over the same Perturb-seq experiment rather than an independent replicate.
- External PubMed literature for target biology, used only as a prior for which
  visible perturbations are mechanistically interpretable:
  - O'Donnell-Luria et al. 2019, American Journal of Human Genetics,
    DOI 10.1016/j.ajhg.2019.03.021, PMID 31079897: heterozygous KMT2E variants
    cause a neurodevelopmental disorder with intellectual disability, autism
    risk, macrocephaly, hypotonia, and epilepsy.
  - Velmans et al. 2021, Journal of Medical Genetics,
    DOI 10.1136/jmedgenet-2020-107470, PMID 34321323: a second multinational
    KMT2E/ODLURO cohort refined the mostly truncating, autosomal-dominant
    neurodevelopmental syndrome.
  - Lee et al. 2021, Nature Communications 12:2953,
    DOI 10.1038/s41467-021-23268-9: biochemical evidence that WRAD subunits
    modulate MLL/SET1 activity on chromatin; this supports treating KMT2A and
    SETD1A as core H3K4-writer comparators, but it does not make KMT2E a direct
    substitute for either complex.
  - Kerimoglu et al. 2017, Cell Reports 20:538-548, PMID 28723559: KMT2A and
    KMT2B regulate partly distinct neuronal genomic regions, cautioning against
    paralog transfer across KMT2 enzymes.
  - Singh et al. 2016, Nature Neuroscience 19:571-577, PMID 26974950: SETD1A
    loss-of-function is associated with schizophrenia and developmental
    disorders, but this clinical relatedness does not imply an identical acute
    postmitotic DEG footprint.

## Training-count calibration

The focal training endpoint is highly zero-inflated.  Among 1,674 visible
targets the median count was 0, the 75th percentile was 1, the 90th percentile
was 2, the 95th percentile was 18, and only 106 targets had at least 10 DEGs.
This makes a low integer the prior unless the target has a same-complex or
same-state visible analog with a large FDR signature.

For KMT2E, the closest visible training perturbations were all imperfect:

| training target | focal `n_degs` | matched perturbed nuclei in 151 | expression/corpus evidence | use for Kmt2e |
| --- | ---: | ---: | --- | --- |
| `Kmt2a` | 24 | 161 | Focal response centered on down-regulated `Nr2f1`, `Pcdh7`, `Lhx9`, `Pcdh10`, `Camk2d`, and `Grik2` plus an induced secondary module. The internal Kmt2a report found that the represented H3K4 writers diverged: `Setd1a` was broad while `Kmt2c` was nearly flat, with only one same-direction overlap across the 30 Kmt2a FDR<0.10 coordinates. | Best positive KMT-family comparator, but it is a KMT2A/MLL1 writer phenotype rather than a direct KMT2E complex. |
| `Kmt2c` | 0 | 55 | Essentially buffered: no focal DEGs and only one FDR<0.10 downstream gene in all recovered groups in the internal report. | Strong counterexample to "KMT2 family implies many DEGs" in post-P16 neurons. |
| `Setd1a` | 368 | 154 | Large down-regulated mitochondrial, GPI-anchor, ER/Golgi, ciliary, lysosomal, and RNA-biogenesis response. Its internal report noted that Kmt2a, Kmt2c, Chd8, Ep300, Crebbp, Setd2, Setd5, and Setdb1 did not phenocopy Setd1a. | High-tail upper bound, not a direct analog. |
| `Ogt` | 4 | 71 | Highly cell-type-uneven response; only four focal DEGs despite hundreds in MB Glut and HYa/Pvalb groups. OGT-associated chromatin comparators did not strongly phenocopy Ogt. | Weak nuclear chromatin-modification prior; not a same-complex transfer. |
| `Setd5` | 9 | 148 | Small, mostly up-regulated TH signaling module, convergent with `Ankrd11` rather than KMT/SET/CBP comparators. The Setd5 report explicitly found no exact FDR overlap with represented SET-family or chromatin-NDD comparators. | Low-positive chromatin-NDD comparator; useful mainly as evidence that a disease chromatin regulator can produce a 5-10 DEG thalamic footprint. |
| `Crebbp` | 8 | 61 | Small focal-only CBP signature; its KAT3 paralog `Ep300` had 0 focal DEGs. | Counterexample showing that even ubiquitous chromatin coactivators can be weak and paralog-specific in this assay. |
| `Ep300`, `Kat6a`, `Kat6b`, `Kdm6b`, `Nsd2` | 0 each | 141-203 for most | Visible chromatin regulators with no focal FDR<0.05 response. | Null controls against a generic chromatin-writer rule. |

The key Parquet query was:

```sql
SELECT gene_target, group_name,
       count(*) FILTER (WHERE pvals_adj < 0.05) AS n_degs,
       min(n_pert_matched) AS n_pert,
       min(n_ctrl_matched) AS n_ctrl
FROM read_parquet('training_de_all_cell_groups.parquet')
WHERE gene_target IN (...KMT/SET/chromatin comparators...)
GROUP BY 1, 2
```

Raw 17,994-gene focal log-fold-change vectors among several chromatin
perturbations had moderate positive correlations, for example `Kmt2a` vs
`Setd1a` at 0.61 and `Kmt2a` vs `Ogt` at 0.61, but the FDR endpoints separated
sharply.  I therefore treated whole-vector correlation as permissive evidence
that these perturbations sit in a related low-amplitude nuclear space, not as
evidence for a `Setd1a`-scale FDR count.

## Target-specific prediction

### Kmt2e

KMT2E is an established neurodevelopmental-disease gene: heterozygous truncating
variants and deletions cause O'Donnell-Luria-Rodan syndrome in humans
(O'Donnell-Luria 2019; Velmans 2021).  That supports a nonzero biological prior
for neurons.  However, the requested endpoint is acute P16 mosaic loss in
already postmitotic recovered nuclei.  The screen repeatedly shows that broad
chromatin or developmental importance transfers poorly into this endpoint:
`Kmt2c`, `Ep300`, `Kat6a`, `Kat6b`, `Kdm6b`, and `Nsd2` were flat in the focal
class, whereas `Setd1a` and `Sin3a` were very large but mechanistically
different outliers.

The closest within-dataset anchor is the modest `Kmt2a` response at 24 DEGs,
because it is a KMT2-family H3K4 writer with a real thalamic signature.
Transfer from `Kmt2a` to `Kmt2e` is weak rather than obligate: core MLL/SET1
WRAD subunits were not available as perturbations, KMT2-family enzymes have
documented nonredundant neuronal functions, and the measured `Kmt2a`, `Kmt2c`,
and `Setd1a` surfaces themselves were nonconvergent.  The better numerical
bracket is therefore the low-positive chromatin/NDD region represented by
`Ogt` at 4, `Crebbp` at 8, and `Setd5` at 9, with `Kmt2a` at 24 as an upper
edge and `Kmt2c` at 0 as a null counterexample.

I predict that `Kmt2e` will be nonzero but small: enough FDR-supported change
to reflect a postmitotic chromatin-regulatory perturbation in this high-yield
thalamic class, but far below the `Setd1a` broad organelle-maintenance program
and below the 24-DEG `Kmt2a` footprint because no visible evidence establishes
shared direct targets.

Final point prediction: **6 DEGs**.

## Limits

- No KMT2E expression signature or count is present in the declared inputs, so
  the requested endpoint is absent for the held-out target and the estimate is
  a transfer from imperfect visible analogs.
- The strongest exact same-family perturbations in the training set were
  `Kmt2a`, `Kmt2c`, and `Setd1a`; the closest KMT2E paralogs or complex partners
  such as `Kmt2b`, `Kmt2d`, `Setd1b`, `Wdr5`, `Rbbp5`, `Ash2l`, `Dpy30`,
  `Men1`, `Hcfc1`, and `Kdm6a` were not represented as training targets.
- The PubMed KMT2E evidence is mostly human developmental genetics, not mouse
  P16 sparse neuronal CRISPR, so it supports disease relevance but not FDR
  breadth.
- Same-experiment reports were used to interpret visible comparator structure.
  They are not independent replication of the Parquet-derived counts.
- The exact boundary between 0 and a few DEGs is the main uncertainty.  With
  focal training counts this sparse, a prediction of 6 should be read as
  low-positive rather than as a precise mechanistic module size.
