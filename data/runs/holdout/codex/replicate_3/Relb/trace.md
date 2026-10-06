# Relb DEG-count forecast

Endpoint: `n_degs` is the number of measured genes in `151 TH Prkcd Grin2c Glut`
with BH-adjusted Wilcoxon `pvals_adj < 0.05`.

## Evidence used

- Target and held-out scope: the one-row manifest names `Relb`; the declared
  training count table has 1,674 training targets and does not include `Relb`.
- Exact focal expression from the declared `Relb` biology bundle: in matched
  non-target `151 TH Prkcd Grin2c Glut` nuclei, `Relb` is detected in
  460/23,679 cells, 1.9426%, with mean raw UMI 0.02086, mean CP10K 0.0130, and
  pseudobulk CPM 1.3075. This is very small expression reach in the requested
  neuronal class.
- Functional-stock adjudication in the biology bundle says disruptive editing
  should stop new RelB supply but pre-existing RelB complexes are not directly
  disabled; free RelB is unstable while p100/p52 or p105/p50 binding may retain
  a partner-bound reserve. The expected harvest-time state is therefore
  `partially_depleted_or_leading_edge`, not clean rapid loss.
- The declared 151-class count table is zero-inflated overall: 1,205/1,674
  targets have `n_degs = 0`, the median is 0, and the 75th percentile is 1.
- Directly relevant represented NF-kappaB/TNF/TLR/IL-1 training perturbations
  in the same 151-class count table were flat:

| target | n_degs |
| --- | ---: |
| Cd40 | 0 |
| Chuk | 0 |
| Il1r1 | 0 |
| Il1rap | 0 |
| Map2k6 | 0 |
| Map3k7 | 0 |
| Mapk9 | 0 |
| Nfkb1 | 0 |
| Rel | 0 |
| Tlr2 | 0 |
| Tlr3 | 0 |
| Tlr4 | 0 |
| Tlr5 | 0 |
| Tlr7 | 0 |
| Tlr8 | 0 |
| Tnfrsf1a | 0 |
| Tnfrsf11a | 0 |
| Tnfrsf13c | 0 |
| Tnfrsf4 | 0 |
| Tnfrsf9 | 0 |
| Traf3 | 0 |
| Xiap | 0 |

- A same-experiment corpus Claim,
  `claim:778b2c45f226febe4372`, summarizes the represented receptor-side,
  adaptor/regulatory, kinase, and nuclear NF-kappaB perturbation reports as
  broadly transcriptionally silent in unchallenged postnatal NeuN-positive
  neurons. I treated this as semantic interpretation of the same experiment,
  not as an independent measurement.
- Parquet checks for the closest represented nodes in `151 TH Prkcd Grin2c Glut`
  found no hidden near-threshold effect: among `Cd40`, `Chuk`, `Nfkb1`, `Rel`,
  `Tlr2`, `Tlr4`, `Tlr7`, `Tnfrsf1a`, `Tnfrsf11a`, `Tnfrsf13c`, `Tnfrsf4`,
  `Tnfrsf9`, `Traf3`, and `Xiap`, every `n_sig` was 0 and the smallest adjusted
  p-value was 0.1402 for `Rel`.

## Synthesis

RelB is a sequence-specific NF-kappaB transcription factor, so an abundant,
tonically active RelB program could have given a strong DE footprint. The focal
population evidence points the other way: only about 2% of the relevant nuclei
carry detectable `Relb` RNA, the edit is expected to leave some partner-bound
pre-edit stock at harvest, and the measured basal neuronal training analogs
for the same receptor-to-NF-kappaB axis are uniformly zero in the exact
151-class endpoint.

The most defensible point estimate is therefore the zero mode of the matched
training distribution rather than a small nonzero count.

Predicted `n_degs`: 0
