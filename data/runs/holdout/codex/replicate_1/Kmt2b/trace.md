# Kmt2b DEG-count forecast

## Target and endpoint

- Target manifest row: `Kmt2b`.
- Endpoint: number of measured genes in `151 TH Prkcd Grin2c Glut` with BH-adjusted Wilcoxon `pvals_adj < 0.05`.
- The declared focal expression measurement reports Kmt2b as a measured feature in this class: 19,448 of 23,679 non-target nuclei expressed it, `pct_cells_expressing = 82.13184678407028`, `mean_raw_umi = 1.9950166814476962`, `pseudobulk_cpm = 125.03477000180938`.

## Kmt2b biology used

The biology bundle argues that KMT2B is a neuronal H3K4 methyltransferase and that the assayed edit should stop production of new KMT2B. It also argues against expecting a fully acute, enzyme-null state by P37-P44:

- H3K4me2/3 chromatin states and KMT2B protein already present before P16 are not directly erased by a disruptive edit.
- More than 30% H3.3 replacement over four weeks in postmitotic neurons makes a new-histone leading edge plausible during the 21-28 day assay window, but the relevant KMT2B protein lifetime and locus occupancy were not measured.
- Postnatal mouse forebrain Kmt2b loss produced memory and chromatin phenotypes, supporting an adult/postnatal neuronal requirement despite Kmt2a/Kmt2c family expression, but that evidence is hippocampal/forebrain and later than the exact thalamic assay window.

I therefore treated Kmt2b as likely engaged and observable in the assayed cell class, but with partial functional realization. That pushed the prediction above the global zero-inflated prior, but below the broadest acute chromatin regulators.

## Training measurements used

The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` table contains 1,674 visible training perturbations and excludes `Kmt2b`. It is very zero-heavy in the requested endpoint:

- 1,205/1,674 targets have `n_degs = 0`.
- Median `n_degs = 0`.
- 90th percentile `n_degs = 2`.
- 95th percentile `n_degs = 18`.
- 97.5th percentile `n_degs = 100.525`.

Visible chromatin and H3K4/SET-family measurements in the focal class gave a sparse, mixed calibration band rather than one obvious analog:

| target | n_degs in 151 TH Prkcd Grin2c Glut | role in forecast |
|---|---:|---|
| `Kmt2a` | 24 | closest KMT-family positive anchor |
| `Kmt2c` | 0 | closest KMT-family silent anchor |
| `Kdm5c` | 18 | modest H3K4-axis responder |
| `Setdb1` | 22 | modest histone-methylation responder |
| `Setd5` | 9 | weak/modest chromatin responder |
| `Brd1` | 4 | weak chromatin responder |
| `Ash1l` | 1 | buffered histone-methylation responder |
| `Setd2` | 1 | single-gene H3K36 responder |
| `Kdm5b` | 0 | silent H3K4-axis responder |
| `Setd1a` | 368 | H3K4 writer, but broad and biologically too large for direct transfer |
| `Phf12` | 403 | broad caudal chromatin/proteostasis state; off-axis upper reference |
| `Brd4` | 311 | broad BRD4 state; off-axis upper reference |

Direct Parquet aggregation over these visible targets showed that Kmt2a, Kdm5c, Ash1l, Setd2, Setd5, Brd1, Kdm5b, and Kmt2c were all focal or nearly focal in their FDR<0.05 counts, whereas Setd1a, Setdb1, Phf12, Brd4, Chd4, and Chd8 also had nonzero responses elsewhere. Kmt2a had 24 focal DEGs and only five FDR<0.05 genes across the remaining groups combined; Kmt2c had only one FDR<0.05 gene in any queried group and zero in the focal class.

## Same-experiment report context

I used the same-experiment corpus only for the visible comparators above, not for `Kmt2b`.

- The Kmt2a report describes a sparse, glutamatergic-biased response, with most of its FDR<0.10 downstream surface in `151 TH Prkcd Grin2c Glut`, and says it did not phenocopy represented H3K4 writer relatives.
- The Kmt2c report describes acute P16 Kmt2c loss as broadly buffered at the mature-neuron transcriptome, with no FDR<0.10 genes in the focal thalamic class.
- The Setd1a report describes broad, recurrent down-regulation of mitochondrial, GPI-anchor, ER proteostasis, ciliary, lysosomal/autophagy, and RNA-biogenesis genes, but explicitly notes that measured KMT2 and chromatin-disorder comparators did not phenocopy Setd1a.
- The Kdm5b/Kdm5c reports separate a silent Kdm5b perturbation from a small, restricted Kdm5c thalamic response and report that Kdm5c was sparse and non-convergent relative to Setd1a/Sin3a.
- The Ash1l and Setd2 reports mark H3K36-adjacent perturbations as weak, null, or single-gene under this acute neuronal design.
- The Setdb1 report describes a sparse coding-gene response strongest in 151 and centered on H3K9/protocadherin or HUSH axes, not an H3K4-like response.

Those report summaries made the very large Setd1a/Phf12/Brd4 counts usable only as evidence that chromatin factors can be visible in this class, not as magnitude analogs for KMT2B.

## Profile evidence

The symmetric focal-class profile comparison across 20 visible chromatin nodes confirmed that the H3K4/SET neighborhood was not a coherent shared FDR module:

- The H3K4/SET/Ash/Brd1 cohort had very low significant-program sharing; most pairs had zero same-direction FDR intersections.
- `Kmt2a` shared no FDR<0.05 genes with `Kmt2c`, `Setdb1`, `Kdm5b`, `Kdm5c`, `Ash1l`, `Setd2`, `Setd5`, or `Brd1`; it shared only one positive significant gene with `Setd1a`.
- `Setd1a`, despite its 368 focal DEGs, had zero to two same-direction significant intersections with the weak/moderate H3K4/SET peers in the inspected pairs.

That made a straight arithmetic transfer from any one profile inappropriate. I instead put the Kmt2b point near the log-scale center of the closest weak-to-moderate H3K4/SET references, with an upward nudge from its strong target reach and the postnatal neuronal Kmt2b phenotype, and a downward nudge from partial functional-stock depletion by harvest.

## Prediction

The resulting point forecast is **8** FDR<0.05 genes in `151 TH Prkcd Grin2c Glut`.
