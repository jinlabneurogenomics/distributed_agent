# Cntn1 direct DEG-count forecast

## Target and endpoint

- Target: `Cntn1`
- Cell class: `151 TH Prkcd Grin2c Glut`
- Endpoint: `n_degs`, the number of measured genes with BH-adjusted Wilcoxon `p < 0.05`
- Declared training table: 1,674 `151 TH Prkcd Grin2c Glut` targets; `Cntn1` was absent.

## Biology used

The canonical Cntn1 bundle supports real focal exposure but incomplete acute
functional realization.

- Exact in-assay Cntn1 reach was broad in non-target thalamic nuclei:
  23,335 / 23,679 cells expressing, 98.547%, with mean CP10K 4.4777.
  This made a pure no-reach zero less plausible, but I did not treat
  self-expression as a knockout-efficiency measurement.
- Contactin-1 acts through multiple installed pools: the axonal
  Contactin-1/Caspr1/NF155 paranodal complex and a neuronal-surface
  Tnr/RPTPz perineuronal-net anchoring complex.
- The P16 edit should stop new functional Contactin-1 supply, but existing
  GPI-anchored Contactin-1 in surface and paranodal structures is not directly
  removed. The functional-stock card therefore calls the P37-P44 harvest state
  `partially_depleted_or_leading_edge`: partner-loss kinetics show a leading
  edge of paranodal disruption within 10-20 days, while substantial residual
  installed complex material can persist and no target-specific Contactin-1
  clearance series was available.
- Germline Cntn1 loss is severe, but the card flags that phenotype as
  developmental and cerebellar/myelination dominated rather than a matched
  post-P16 thalamic neuronal loss. I therefore used it as evidence that Cntn1
  is functional in neural cells, not as a high-count magnitude prior.

## Training perturbations that set the scale

The curated biology points most directly to Contactin/Caspr/paranodal or
nearby adhesion perturbations, but most named Cntn1 partners in the source
card were unavailable in the declared count table: `Nfasc`, `Cntn2`, `Tnr`,
and `Ptprz1` had no training row. The closest declared rows were quiet:

| comparator | reason retained | observed `n_degs` |
| --- | --- | ---: |
| `Nrcam` | top typed nominator hit; exact mouse CORUM `Cntn1-Nrcam-Ptprb` complex | 2 |
| `Cntnap1` | Caspr1 paranodal partner named by the Cntn1 biology bundle; training-available STRING physical hit | 1 |
| `Cntnap2` | contactin-family physical-neighborhood nominee | 1 |

For a wider check, I profiled the top 20 training-available Cntn1 nominees
from the typed gene-analog nominator in the same `151 TH Prkcd Grin2c Glut`
Parquet context. Their significant-feature counts were:

`Nrcam 2`, `Dscam 0`, `Bsg 1`, `Tlr2 0`, `Cd47 1`, `Scn1b 2`,
`Tenm4 0`, `Cntnap2 1`, `Itgb1 0`, `Adgrl1 1`, `Fyn 0`,
`Adgrl3 1`, `Psen1 0`, `Tenm3 1`, `Fgfr1 0`, `Nrg1 0`, `Prnp 1`,
`Mapk1 0`, `Fbxo11 1`, `Cntnap1 1`.

That cohort had 9 zero-count, 9 one-count, and 2 two-count profiles, with
median 1. The three most source-proximal observed rows had a log1p center of
`expm1(mean(log1p([2, 1, 1]))) = 1.29`; the broader 20-node Cntn1-biased
cohort had a log1p center of 0.52.

## Forecast

I forecast a small nonzero response. The broad Cntn1 expression in the focal
population and the ongoing postnatal renewal demand argue against treating
the perturbation as completely unreachable by P37-P44. The low direct-comparator
counts, partial persistence of installed Contactin-1 pools, and the
survivor-conditioned soma/nuclear RNA endpoint argue against borrowing scale
from the severe developmental Cntn1-null phenotype.

The point estimate is therefore the rounded low direct-analog center:

`predicted_n_degs = 1`
