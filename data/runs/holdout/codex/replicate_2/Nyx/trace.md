# Direct DEG-count forecast for 151 TH Prkcd Grin2c Glut

## Target and endpoint

- Manifest target: `Nyx`, from the declared one-row holdout manifest
  `manifests/Nyx.csv`.
- Endpoint: `n_degs`, the number of measured genes in `151 TH Prkcd Grin2c Glut`
  with BH-adjusted Wilcoxon `pvals_adj < 0.05`.
- I used the declared biology bundle
  `biology_bundles/Nyx.json`, the training count table
  `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`, and the declared
  training-only Parquet for the selected visible comparators. The bundle reports
  `serving.target_outcome_exposed = false` and `serving.labeled_neighbors_exposed = false`;
  no `Nyx` endpoint or `Nyx` expression signature was used.

## Biology of Nyx in the assayed thalamic class

The exact in-assay focal-population reach is very small:

- `Nyx` is detected in 738 of 23,679 matched non-target nuclei in
  `151 TH Prkcd Grin2c Glut`, or 3.1167% of the population.
- Mean expression is `0.0333` raw UMI per nucleus, `0.0157` mean log1p CP10K,
  and `2.0857` pseudobulk CPM.

That supersedes the qualitative low-brain-expression prior: most nuclei in the
targeted thalamic glutamatergic class have little or no measurable `Nyx` target
to perturb, so even effective edits should be confined to a very sparse
subpopulation.

The biological evidence also does not point to a broad thalamic transcriptional
state. The established function is retinal: GPI-linked extracellular nyctalopin
supports TRPM1 channel localization at ON/depolarizing bipolar-cell dendritic
tips. Nyx loss disrupts young-adult mouse retinal bipolar-cell signaling, but
that is a different neural tissue and a constitutive lesion. For the P16 to
P37-P44 Perturb-seq design, the stock card concludes that editing stops new
Nyx supply while leaving an installed pre-edit membrane pool initially
functional; generic turnover favors partial replacement within 21-28 days, but
synaptic localization and absent Nyx-specific kinetics leave the amount of
functional stock lost by harvest unresolved.

## Training counts and selected visible comparators

The declared training table for this focal class is heavily concentrated at
zero:

- 1,674 training targets total.
- 1,205 targets, 72.0%, have `n_degs = 0`.
- 1,481 targets, 88.5%, have `n_degs <= 1`.
- 1,546 targets, 92.4%, have `n_degs <= 5`.
- The median is 0 and the 75th percentile is 1.

For a biology-matched visible comparator set, I used genes from the ON-bipolar
mGluR6/TRPM1 signaling neighborhood that were present in the training table.
The closest direct partner, `Trpm1`, was absent from the training count table.
The visible members were transcriptionally quiet in the focal class:

| training target | count-table `n_degs` | Parquet significant features |
| --- | ---: | ---: |
| `Grm6` | 0 | 0 |
| `Gpr179` | 0 | 0 |
| `Gnao1` | 1 | 1 |

The profile inspection over the declared Parquet found no missing profiles for
these three genes. Their thalamic signatures were mutually positively
correlated at whole-profile scale, but the absolute significant-feature burden
was still nil or one, which is the informative quantity for this endpoint.

## Forecast

The point forecast is:

```text
Nyx: 0
```

Rationale: `Nyx` has an extremely narrow measured reach in
`151 TH Prkcd Grin2c Glut`; its strong loss-of-function evidence is retinal
rather than thalamic; its installed synaptic membrane stock may be only
partially depleted in a 21-28 day post-P16 window; and the available same-pathway
training perturbations were all silent or nearly silent in the same focal
population. Nonzero expression in 3.1% of nuclei and a postnatal retinal
phenotype keep a tiny response possible, but the best direct forecast is no
BH-significant genes.
