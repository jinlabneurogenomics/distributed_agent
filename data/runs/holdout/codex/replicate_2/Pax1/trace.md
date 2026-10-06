# Pax1 n_degs forecast

## Target and endpoint

- Target: `Pax1`.
- Focal population: `151 TH Prkcd Grin2c Glut`.
- Endpoint: `n_degs`, the number of measured genes in this focal population with BH-adjusted Wilcoxon `p < 0.05`.
- I used the declared one-row manifest, the biology-only `Pax1` bundle, the declared 151 TH training count table, and focal-population slices from the declared training DE Parquet. The `Pax1` outcome and `Pax1` expression signature were not in those declared training inputs.

## Evidence that set the scale

1. The canonical `Pax1` bundle reports exact in-assay reach for the same class: among `23679` non-target nuclei in `151 TH Prkcd Grin2c Glut`, `Pax1` had `0` total UMIs, `0` expressing cells, `mean_raw_umi = 0.0`, `mean_log1p_cp10k = 0.0`, and `pseudobulk_cpm = 0.0`. That is stronger for this assay than the qualitative external thalamus priors and makes any post-edit molecular effect in the recovered focal population hard to realize.

2. The functional-stock card calls Pax1 a nuclear sequence-specific transcription factor whose acute P16 editing would stop new functional protein production from edited alleles, but whose pre-existing protein or chromatin-occupancy persistence is unknown through P37-P44. Its mouse loss-of-function phenotype evidence is embryonic axial skeleton and thymus rather than postnatal neurons, and Pax9 compensation is demonstrated in embryonic sclerotome, not in thalamic neurons. These facts left no matched postnatal thalamic mechanism strong enough to override the exact zero focal expression.

3. The same-experiment corpus release did not contain a `Pax1` target record, Claim, Finding, or explicit reference. I therefore did not have a packaged same-experiment Pax1 report to reinterpret; the corpus was silent rather than endpoint evidence for a nonzero response.

4. The declared count table for this focal class is very sparse: 1205 of 1674 training targets are zero, the median is zero, the 75th percentile is one, and 1512 of 1674 have at most two DEGs. Therefore a low-reach target is much closer to the modal outcome than to the long high-count tail.

5. The training paired-box family perturbations in the count table were all zero in the same endpoint:

   | target | n_degs |
   | --- | ---: |
   | Pax2 | 0 |
   | Pax3 | 0 |
   | Pax4 | 0 |
   | Pax6 | 0 |
   | Pax7 | 0 |
   | Pax8 | 0 |

   Direct Parquet slices for these six targets in `151 TH Prkcd Grin2c Glut` likewise had 17259 measured-gene rows per target and zero genes with `pvals_adj < 0.05`.

6. A broader count-table check of developmental transcription-factor families with obvious thalamic-context mismatch was also nearly all zero: `Alx`, `Dlx`, `Ebf`, `Fox`, `Hox`, `Lhx`, `Otx`, `Pax`, `Pou`, `Six`, `Sox`, `Tbx`, and `Zic` contributed 65 training targets, 62 of which had `n_degs = 0`. The three nonzero members were only `Sox2 = 2`, `Sox5 = 2`, and `Zic1 = 2`.

## Synthesis

`Pax1` is a real developmental transcription factor, but the exact focal-population expression measurement saw no `Pax1` molecules in the matched non-target thalamic nuclei. With no transferable postnatal neuronal loss phenotype, no established same-context Pax9 buffering or Pax1 turnover clock, no same-experiment Pax1 semantic record, and all observed paired-box family perturbations landing at `0`, the most defensible point forecast is the modal/no-detected-response count.

Predicted `n_degs`: `0`.
