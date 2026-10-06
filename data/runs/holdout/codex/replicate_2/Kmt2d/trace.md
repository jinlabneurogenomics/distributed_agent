# Kmt2d forecast

## Declared target and endpoint

- Holdout target: `Kmt2d`.
- Cell group: `151 TH Prkcd Grin2c Glut`.
- Endpoint: `n_degs`, the count of measured genes with BH-adjusted Wilcoxon `p < 0.05` in this cell group.
- The declared training table contains 1,674 non-held-out targets and does not contain `Kmt2d`.

## Biology used

The canonical Kmt2d biology bundle supports target availability and partial activity by the harvest window, but not a broad unbuffered enhancer collapse.

- Exact focal expression is high: `Kmt2d` is available in the focal non-target nuclei, with mean log1p CP10K 0.857 and 20,842/23,679 cells expressing the transcript, or 88.0%.
- KMT2D is a KMT2C-related enhancer H3K4 mono-/di-methyltransferase and COMPASS scaffold. Existing enzyme and already installed histone marks could persist after editing, while KMT2C supplies partial redundancy.
- Adult mouse hippocampal shRNA evidence showed reduced Kmt2d RNA and an H3K4 mark by four weeks, and neuronal H3.3 carriers renew over the same interval. The stock card therefore calls the 21-28 day experiment likely to substantially deplete some KMT2D capacity, with incomplete resolution from KMT2C buffering and long-lived chromatin.

## Training measurements used

The direct thalamic count table is sparse:

| quantity | value |
|---|---:|
| training targets | 1,674 |
| median `n_degs` | 0 |
| zero-DEG targets | 1,205 |
| targets with `n_degs >= 100` | 43 |
| targets with `n_degs >= 500` | 15 |

Matched or nearby chromatin/H3K4 perturbations in the declared `151 TH Prkcd Grin2c Glut` table were:

| perturbation | `n_degs` |
|---|---:|
| Kmt2c | 0 |
| Ep300 | 0 |
| Ash1l | 1 |
| Setd2 | 1 |
| Crebbp | 8 |
| Setd5 | 9 |
| Mecp2 | 16 |
| Kdm5c | 18 |
| Setdb1 | 22 |
| Nsd1 | 23 |
| Kmt2a | 24 |
| Chd8 | 61 |
| Chd4 | 100 |
| Setd1a | 368 |
| Phf12 | 403 |
| Brd4 | 311 |
| Sin3a | 1,433 |

Direct parquet summaries for the focal group matched the training counts and showed that high-DEG chromatin targets were not a generic family baseline: `Kmt2c` had 0 DEGs with 55 matched perturbed nuclei; `Kmt2a` had 24 with 161 nuclei; `Setd1a` had 368 with 154 nuclei; `Brd4` had 311 with 93 nuclei. Across all assayed groups, `Kmt2c` had only one significant downstream gene in total, whereas `Kmt2a`, `Setd1a`, and `Brd4` were detectable but distinct.

Same-experiment Findings for released comparators were used as interpretation of those same measurements:

- `Kmt2c` was broadly buffered after acute P16 loss: 15 of 16 measured groups had zero downstream FDR<0.10 genes and the remaining group had a single `Prnp` hit.
- `Kmt2a` was sparse and thalamus-biased, with its represented H3K4 relatives diverging: `Setd1a` was broad and mostly non-overlapping, while `Kmt2c` was almost flat.
- `Setd1a` was a large response but did not phenocopy measured KMT2 or CBP/p300 comparators, so it is an upper bound for a different H3K4 writer branch rather than a point analog.

## Synthesis

The all-target prior in this group favors zero, but Kmt2d has stronger focal expression and stronger four-week postmitotic support than an arbitrary target. I therefore did not treat it as a median target. The closest measured enhancer paralog, Kmt2c, is a firm downward anchor at zero, and Ep300/Crebbp/Kat6a/Kat6b show that enhancer-chromatin components are often silent or single-digit in this assay. Kmt2d is nevertheless expected to exceed Kmt2c because the biology bundle assigns substantial KMT2D stock depletion despite partial KMT2C redundancy and because KMT2D was the major enhancer H3K4me1/2 enzyme in the curated KMT2C/D evidence.

The most compatible scale is the low thalamic chromatin band around `Mecp2`, `Setdb1`, `Nsd1`, and `Kmt2a`, rather than the `Setd1a`/`Brd4`/`Phf12` outlier band. I chose 22 DEGs, matching that low but detectable branch and staying below the 61-100 DEG CHD responses.

Final point forecast: `Kmt2d` = 22.
