# Direct n_degs forecast for Mboat7 in 151 TH Prkcd Grin2c Glut

Prediction: `Mboat7 -> 1` FDR<0.05 measured gene.

## Endpoint and declared target

- Target: `Mboat7`, the only row in the declared holdout manifest.
- Endpoint: `n_degs` in `151 TH Prkcd Grin2c Glut`, counting measured genes in the held-out perturbation contrast with BH-adjusted Wilcoxon `pvals_adj < 0.05`.
- Declared focal expression: Mboat7 was measured in the exact focal non-target population, with mean log1p CP10K 0.6183, mean raw UMI 1.6831, 105.48 pseudobulk CPM, and 17,659 / 23,679 non-target nuclei expressing it, or 74.58%.

## Biology prior from the Mboat7 card

The Mboat7 biology bundle supports material perturbation reach but not a large postnatal thalamic RNA program:

- MBOAT7/LPIAT1 transfers arachidonate from arachidonoyl-CoA to lysophosphatidylinositol in phosphatidylinositol remodeling.
- Mouse Mboat7 germline loss strongly affects arachidonoyl-containing PI species and causes developmental cortical/hippocampal abnormalities with early mortality, so the enzyme is not biologically inert.
- The assayed P16-to-P37/P44 postmitotic thalamic setting is a poor match to the strongest phenotype evidence, which is constitutive, developmental, and forebrain-focused.
- The functional-stock adjudication judged MBOAT7 activity likely substantially depleted by harvest because the lipid carrier pool is actively remodeled, but it also noted missing direct kinetics for neuronal MBOAT7 protein and arachidonoyl-PI carrier residence.

That combination argues against a pure no-op but also against importing the scale of a developmental structural phenotype into this sparse survivor-conditioned snRNA-seq endpoint.

## Same-experiment corpus context

The selected corpus release had no packaged `Mboat7` Findings, Claims, or explicit report references. This is absence of same-experiment semantic coverage for the target, not an observed null outcome.

For measured lipid and phosphoinositide training perturbations, the release repeatedly interpreted the same experimental surface as buffered or singleton-scale rather than convergent:

- `Pi4kb` showed only a tiny PI4P-loss RNA response; in 151 TH its FDR<0.10 calls were `Tmem50b` and `Rnf145`, with only `Tmem50b` passing 0.05.
- `Acsl4` produced only a restricted sterol-feedback hint outside 151 TH and did not phenocopy ferroptosis-axis perturbations in this basal neuronal screen.
- `Inpp5k`, `Pik3cb`, `Pik3r1`, `Pik3r2`, `Abhd2`, `Sphk1`, and `Ppip5k2` were flat in the 151 TH count table.
- `Mtor` was a useful upper scope reference for low-but-real metabolic signaling in this class: it had a small two-gene FDR<0.05 151 TH response, not a broad canonical mTORC1 RNA program.

## Training counts and exact Parquet checks

The declared 151 TH count table contains 1,674 training targets and is dominated by near-zero outcomes:

- 1,205 / 1,674 targets have `n_degs = 0`.
- 276 / 1,674 have `n_degs = 1`.
- 90.3% have `n_degs <= 2`.
- The mean is 14.05 but the median is 0, reflecting a long upper tail driven by stress/proteostasis, splicing, chromatin, and transcriptional outliers rather than by ordinary lipid enzymes.

In the exact 151 TH Parquet rows for lipid and PI-related references:

| target | FDR<0.05 rows in 151 TH | interpretation |
| --- | ---: | --- |
| `Abhd12` | 1 | self-transcript only |
| `Abhd2` | 0 | flat |
| `Acsl4` | 1 | self-transcript only |
| `Inpp5k` | 0 | flat |
| `Mtor` | 2 | two-gene downstream call |
| `Pi4kb` | 1 | one downstream call |
| `Pik3cb` | 0 | flat |
| `Pik3r1` | 0 | flat |
| `Pik3r2` | 0 | flat |
| `Ppip5k2` | 0 | flat |
| `Pld3` | 1 | self-transcript only |
| `Sphk1` | 0 | flat |
| `Sptlc2` | 1 | self-transcript only |

A run-local signed-profile comparison of these 13 rows in the same Parquet/context found no coherent shared lipid module: 7 nodes had no significant features, 6 had only 1-9, the mean positive and negative leading-tail overlaps were about 0.027 and 0.025, and significant-program overlap was 0 in both directions.

## Synthesis

I weighted the in-assay Mboat7 expression and functional-stock reach upward from the all-target mode of 0, because a high-expressed editable enzyme with a renewing lipid product is more likely to show at least its own transcript or a tiny compensation marker than a completely unexpressed or irrelevant target. I did not weight toward the high-count tail: the closest measurable biology in this assay consists of buffered phosphoinositide/lipid rows and isolated self-transcript calls, while the developmental knockout phenotype is not a matched postnatal thalamic RNA phenotype.

The resulting point estimate is a single FDR<0.05 measured gene, most plausibly the target transcript or one isolated compensation gene, with low support for a count greater than 2.
