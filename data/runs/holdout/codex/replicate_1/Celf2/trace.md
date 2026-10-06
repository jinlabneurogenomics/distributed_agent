# Trace

## Target and endpoint

- Target: `Celf2`, the single row in the declared holdout manifest
  `[local file: Celf2.csv]`.
- Cell population: `151 TH Prkcd Grin2c Glut`.
- Endpoint: `n_degs`, the count of measured genes with BH-adjusted Wilcoxon
  `pvals_adj < 0.05` for the held-out Celf2 perturbation in that population.

## Evidence used

- The declared Celf2 biology bundle
  `[local file: Celf2.json]`,
  SHA256 `c2628811e3ffe504f1948eb3a99894c78d0afd29fe0846bfcdc77a0c7632485f`,
  reports exact focal-population expression for Celf2: 23,453 of 23,679
  non-target nuclei express the feature, 99.05% expressing, mean log1p(CP10K)
  1.6265, and mean raw UMI 7.1081.
- The same bundle classifies the Celf2 product as a nucleocytoplasmic
  RNA-binding and alternative-splicing regulator whose new supply should stop
  after a disruptive edit. It adjudicates Celf2 as likely substantially
  depleted by the 21-28 day harvest, but only with partial evidence because no
  target-specific endogenous neuronal half-life was found.
- Mouse neural Celf2 loss has direct phenotypic and transcript-processing
  support in the bundle, but the closest evidence is developmental cortex or
  whole neonatal brain rather than an acute P16 thalamic perturbation. I
  treated that as support for functional relevance, not as proof of a large
  postnatal whole-gene response.
- The declared training count table
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
  contains 1,674 measured training perturbations for this endpoint. Its
  distribution is highly zero-inflated: 1,205 targets have `n_degs = 0`, the
  median is 0, the 75th percentile is 1, the 90th percentile is 2, the 95th
  percentile is 18, the 99th percentile is 430, and the maximum is 2,677.
- In the training table, matched RNA-processing perturbations showed a wide
  range in `151 TH Prkcd Grin2c Glut`: `Rnpc3` 868, `U2af2` 828, `Hnrnpu` 733,
  `Tnpo3` 618, `Thoc1` 303, `Snrnp70` 213, `Tardbp` 210, `Matr3` 149,
  `Hnrnpc` 122, but also `Hnrnpa2b1` 11, `Ddx3x` 8, `Adarb1` 4, `Upf3b` 1,
  and `Fmr1`, `Tia1`, `Ago2`, and `Adar` 0.
- Direct aggregation of the training expression Parquet
  `[local file: training_de_all_cell_groups.parquet]`
  in this same cell class reproduced those comparator counts from
  `pvals_adj < 0.05` and showed comparable matched perturbation-cell counts for
  the strongest RNA-processing comparators: for example, `Rnpc3` had 149
  perturbed nuclei, `U2af2` 222, `Hnrnpu` 163, `Tardbp` 153, `Matr3` 130, and
  `Hnrnpc` 196, all against 23,679 matched controls.
- Packaged same-experiment Findings from release
  `perturbai-july-260713-sourceguard-1773-v1` describe `Rnpc3`, `U2af2`,
  `Hnrnpu`, `Tardbp`, `Matr3`, `Hnrnpc`, `Snrnp70`, and `Thoc1` as recurrent
  RNA-processing or spliceosome/TREX-like responses whose largest or
  repeatedly major signatures include `151 TH Prkcd Grin2c Glut`. They also
  separate this broad class from flat or weak RNA-binding perturbations such as
  `Hnrnpa2b1`, `Tia1`, and `Upf3b`.

## Synthesis

Celf2 is unlikely to be a technical or expression null in the focal thalamic
population: the feature is detected in nearly every non-target nucleus, and
the declared functional-stock card favors loss of an actively renewed
RNA-processing activity within the screen window. That moved the forecast away
from the large zero pileup in the empirical count table.

I nevertheless discounted Celf2 from the several-hundred-DEG tier occupied by
core RNA biogenesis, minor-spliceosome, hnRNP stress, nuclear-export, and
proteasome-coupled perturbations. CELF2's best-supported operation is regulated
alternative splicing and post-transcriptional control; many primary isoform
defects would be invisible to a whole-gene Wilcoxon count, and the direct mouse
phenotypes in the Celf2 bundle are developmental or cortical rather than a
matched acute P16 thalamic test.

The nearest quantitative bracket was therefore below the `Hnrnpc`/`Matr3`/
`Tardbp` range of 122-210 significant genes, but above the flat RBP controls and
above the 95th percentile of the full training distribution. I set the point
prediction to 64 significant genes.
