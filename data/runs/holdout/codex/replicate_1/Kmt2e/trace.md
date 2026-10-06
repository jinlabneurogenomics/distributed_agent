# Kmt2e direct n_degs forecast

## Target and endpoint

The declared one-row holdout target is `Kmt2e`, and the requested endpoint is
the number of measured genes in `151 TH Prkcd Grin2c Glut` with BH-adjusted
Wilcoxon `pvals_adj < 0.05`.

The prediction used only the declared biology card, the declared training count
table, the declared differential-expression parquet for training targets, and
same-experiment corpus summaries for measured comparator perturbations.

## Kmt2e biology

The biology card places KMT2E as a chromatin-associated H3K4me3 reader and
transcriptional regulator rather than as a demonstrated intrinsic H3K4
methyltransferase. It is a dynamic protein/complex component: a productive P16
edit should stop new KMT2E supply, and generic mouse-brain protein turnover
supports substantial stock decline over the 21-28 day experimental window, but
the card grades this conclusion as partial because no KMT2E-specific neuronal
half-life was found and an OGT/USP7-stabilized pool could persist.

The exact focal-population expression measurement argues against a simple
no-reach null: `Kmt2e` was detected in 20,409 of 23,679 non-target 151-class
nuclei, with 86.19% of cells expressing it, mean raw UMI 2.309, and pseudobulk
144.7 cpm. This establishes transcript reach in the assayed thalamic
glutamatergic population, not editing efficiency.

The neural phenotype prior is weaker than the expression/stock prior. The mouse
loss evidence is constitutive haploinsufficiency with behavioral, amygdala
metabolic, and amygdala morphology phenotypes; it does not show that acute
postnatal loss in thalamic neurons has a large 3-4 week cell-autonomous mRNA
footprint. SETD5 is KMT2E's closest named noncanonical SET-domain relative in
the card, but no acute thalamic compensation test exists.

## Matched training measurements

The 151-class training count table contains 1,674 biological targets. Its
distribution is heavily zero-inflated: 1,205 targets have zero BH<0.05 DEGs,
the median is 0, the 75th percentile is 1, the 90th percentile is 2, and the
95th percentile is 18.

The most relevant mechanistic comparators were small rather than massive in the
same focal class:

| training target | 151-class BH<0.05 `n_degs` |
| --- | ---: |
| `Kmt2c` | 0 |
| `E2f1` | 0 |
| `Ash1l` | 1 |
| `Setd2` | 1 |
| `Ogt` | 4 |
| `Setd5` | 9 |
| `Kmt2a` | 24 |
| `Setdb1` | 22 |
| `Chd8` | 61 |
| `Setd1a` | 368 |

The same-experiment corpus gives the same scale interpretation. `Setd5`, the
closest KMT2E family comparator with measurements, produced only two
FDR-positive cell groups; its main signal was a compact
`151 TH Prkcd Grin2c Glut` module with 13 genes at FDR<0.10 and 9 genes at the
task threshold. Its positive profile neighbor was `Ankrd11`, not a generic
SET-family or MLL/COMPASS perturbation, and represented SET-family,
MLL/COMPASS-related, CBP/p300, and chromatin-NDD perturbations failed to
phenocopy its exact FDR signature.

The represented KMT2-family and H3K4-axis measurements also cautioned against
simple paralog extrapolation. `Kmt2a` gave a sparse 151-biased response, with
24 genes at BH<0.05 in the count table. `Kmt2c`, despite being a developmental
enhancer methyltransferase, was completely flat in 151. `Ogt` is a curated
KMT2E stabilizing partner but is a broader O-GlcNAc enzyme with only 4
BH<0.05 genes in the focal thalamic class, so its much larger effects in other
classes were not transferred to `Kmt2e`.

## Synthesis

The exact target expression and favored stock depletion make a strict zero
less plausible for `Kmt2e` than for low-reach or long-lived installed products.
At the same time, KMT2E is a noncatalytic reader/regulator with unresolved
acute postnatal thalamic requirement, and the matched chromatin measurements
show that broad gene-family labels routinely fail to transfer in this screen.

I therefore placed `Kmt2e` in the small nonzero chromatin/NDD regime, slightly
below `Setd5` because SETD5 has a measured compact TH module and KMT2E lacks
direct postnatal thalamic phenotype evidence. The resulting point forecast is
7 DEGs at BH<0.05.
