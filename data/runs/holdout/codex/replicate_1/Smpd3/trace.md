# Smpd3 DEG-count forecast

Endpoint: number of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05` for `Smpd3` in `151 TH Prkcd Grin2c Glut`.

Prediction: `1`

## Evidence used

- The manifest and canonical biology bundle both identified the target as `Smpd3`.
- Exact focal-population reach was nonzero but partial: in non-target `151 TH Prkcd Grin2c Glut` nuclei, `Smpd3` was detected in 9,214 of 23,679 cells, or 38.912%, with mean raw UMI 0.5906 and mean CP10K 0.3708. This makes the target transcript observable in the assay, while still leaving strong dilution from cells without measurable `Smpd3`.
- The biology bundle supported functional depletion by harvest but not a rapid matched thalamic response: SMPD3/nSMase2 is a renewable membrane neutral sphingomyelinase that hydrolyzes sphingomyelin to ceramide, heterologous chase data support hours-scale protein turnover, and germline mouse loss causes hypothalamic/postnatal and late neuronal phenotypes. The unresolved parts were exactly the acute P16-to-P37/P44 thalamic-neuron timing and the degree of buffering by related sphingomyelinase activity.
- The declared focal training count table was very zero-heavy: 1,205 of 1,674 training targets had `n_degs = 0`, the median was 0, the 75th percentile was 1, and only 43 reached at least 100 DEGs.
- The closest available lipid, sphingolipid, lysosomal, and Golgi/trafficking training perturbations were mostly silent or self-only in the focal class:
  - `Asah1`: 0
  - `Sphk1`: 0
  - `Sptlc2`: 1
  - `Psap`: 1
  - `Ppt1`: 1
  - `Abhd12`: 1
  - `Acsl4`: 1
  - `Cert1`: 0
  - `Lamp2`: 0
  - `Tmem106b`: 1
  - `Vps41`: 0
  - `Vps53`: 0
  - `Tmem165`: 0
  - `Atg5`: 0
  - `Atg16l1`: 0
  - `Vps35`: 17
  - `Vps54`: 31
  - `Rab7`: 501
- Parquet inspection of the one-DEG comparators showed that `Abhd12`, `Acsl4`, `Ppt1`, `Psap`, `Sptlc2`, and `Tmem106b` each had only its own target transcript significant at `pvals_adj < 0.05`. In the whole focal training table, 237 targets were self-only responders with no significant non-self gene, larger than the 105 targets with one to five non-self DEGs.
- A focal matched profile comparison of the 18 lipid/lysosomal/Golgi candidates did not reveal a coherent broad shared signature among them: 9 of the 18 had no significant genes, the cohort median top-tail overlap was 0.01 to 0.02 by direction, and the only very large profile was the outlying `Rab7` perturbation.

## Reasoning

`Smpd3` should be functionally perturbed by 21-28 days when an edit lands in an expressing cell, and its transcript is measurable in this thalamic population. That argues against treating it as an unexpressed or fully buffered target. However, the matched biology points to membrane lipid flux, developmental hypothalamic phenotypes, and months-late neuronal proteostasis rather than to an acute high-penetrance transcriptional program in recovered juvenile thalamic nuclei.

The count table pushed the quantitative estimate down: close lipid/sphingolipid targets cluster at 0-1 DEGs, and their single calls are often self-transcript calls rather than downstream programs. Vesicle-trafficking perturbations such as `Vps35`, `Vps54`, and especially `Rab7` can be active, but those are stronger core trafficking failures than SMPD3 loss and were treated as upper-side boundary cases rather than direct analogs.

I therefore forecast a detectable but minimal response, with one significant measured gene the most likely integer point.
