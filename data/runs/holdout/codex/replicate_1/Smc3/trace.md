# Smc3 n_degs forecast

## Target and endpoint

- Target: `Smc3`
- Population: `151 TH Prkcd Grin2c Glut`
- Endpoint: count of measured genes with Wilcoxon `pvals_adj < 0.05`
- Held-out setup: the declared training count table contains 1,674 targets and no `Smc3` row; the declared Parquet is a training-only differential-expression table for observed non-target perturbations.

## Evidence used

### Smc3 biology prior

The canonical Smc3 bundle supports a realized perturbation in the assayed population:

- SMC3 is an obligate ATPase-core subunit of cohesin with SMC1, and no replaceable SMC3 paralog was identified in mouse neurons.
- Disruptive editing is expected to stop new functional SMC3 supply. Existing cohesin rings are not instantly destroyed, but cohesin has dynamically exchanged chromatin-bound pools, so assembly-competent SMC3/cohesin stock is expected to be substantially depleted over the 21-28 days between P16 editing and P37-P44 harvest.
- Exact focal-population reach is strong: non-target `151 TH Prkcd Grin2c Glut` nuclei express `Smc3` in 17,963 / 23,679 cells, or 75.9%, with mean expression 1.0186 CP10k.
- The main downward uncertainties are survivor conditioning and the absence of a postmitotic thalamic-neuron SMC3 clearance curve. The card supports biological effect, but not a very large count in recovered survivor nuclei.

### Training count scale

The exact `151 TH Prkcd Grin2c Glut` training count table is sparse and right-skewed:

- `n = 1674`
- median `n_degs = 0`
- mean `n_degs = 14.05`
- 75th percentile `= 1`
- 90th percentile `= 2`
- 95th percentile `= 18`
- 59 / 1,674 targets have at least 50 DEGs

That background makes Smc3 likely non-null but argues against inflating the point into the several-hundred DEG regime without a matched observed analog.

### Cohesin and chromatin comparators in the training table

Closest directly measured cohesin perturbations in the same focal population:

| comparator | focal `n_degs` |
|---|---:|
| `Smc1a` | 24 |
| `Stag2` | 37 |
| `Stag1` | 0 |
| `Pds5a` | 0 |
| `Hdac8` | 0 |

Other broader chromatin comparators were not used as direct scale anchors:

| comparator | focal `n_degs` | reason |
|---|---:|---|
| `Ctcf` | 270 | only a partial Smc1a/Stag2 subset inside a larger CTCF-dominant response |
| `Smarcc2` | 185 | SWI/SNF thalamic program, not cohesin-core loss |
| `Kmt2a` | 24 | chromatin regulator with a sparse thalamic identity response, useful only as background scale |

The packaged same-experiment findings report that `Smc1a` and `Stag2` share a restricted same-direction thalamic module, whereas `Stag1`, `Pds5a`, `Hdac8`, `Ncapd3`, `Prr12`, `Zfp609`, and `Smchd1` do not reproduce it. Direct Parquet remeasurement at the requested FDR threshold found:

- `Smc1a`: 24 significant genes
- `Stag2`: 37 significant genes
- 9 genes significant in both, all same-direction
- profile-wide `Smc1a`/`Stag2` log-fold-change correlation `r = 0.658`, cosine `= 0.720`

I therefore treated `Smc1a` and `Stag2` as the only close scale-bearing anchors. The flat `Stag1`/`Pds5a`/`Hdac8` outcomes temper certainty but are not equal direct analogs for SMC3, because SMC3 is the shared core SMC partner rather than a regulatory or variant subunit.

## Forecast

The log-scale midpoint of the two close nonzero anchors is:

```text
exp(mean(log1p([24, 37]))) - 1 = sqrt(25 * 38) - 1 = 29.8
```

Rounded to an integer and nudged neither toward the Ctcf/Smarcc2 high-count chromatin tails nor toward the non-core flat cohesin regulators, my prediction is:

```text
Smc3 -> 30
```
