# Direct forecast trace

## Target and endpoint

- Target perturbation: `Srrm2` in `151 TH Prkcd Grin2c Glut`.
- Endpoint: `n_degs`, the number of measured genes in this thalamic glutamatergic class with Wilcoxon BH-adjusted `pvals_adj < 0.05`.
- Declared measurement sources used:
  - holdout manifest: `[local file: Srrm2.csv]`;
  - biology-only target bundle: `[local file: Srrm2.json]`;
  - focal count table: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`;
  - declared training DE Parquet: `[local file: training_de_all_cell_groups.parquet]`.

## Biology carried forward

The target bundle places `Srrm2` well within the assayed focal population:
`Srrm2` was detected in 23,661 of 23,679 non-target `151 TH Prkcd Grin2c Glut`
nuclei, with mean 8.09 CP10K and mean 12.47 raw UMIs among non-target cells.
The perturbation should also be realized by harvest: the functional-stock card
adjudicates SRRM2 as a dynamic spliceosome-associated and nuclear-speckle
component, where P16 disruptive editing stops new intact SRRM2 production and
21-28 elapsed days are expected to substantially deplete the operative pool.

The endpoint is still survivor-conditioned expression rather than splicing.
That kept the prediction below the very largest core-spliceosome responses:
SRRM2 loss can be biologically consequential while much of its primary effect
is alternative-splicing or speckle organization that need not turn into a
genome-scale abundance program in the recovered nuclei.

## Training measurements interpreted

The focal training count table is extremely sparse overall: 1,205 of 1,674
training perturbations have zero DEGs, the median is zero, the 95th percentile
is 18 DEGs, and the 98th percentile is 150 DEGs. A simple all-target prior
would therefore be too low for a highly expressed RNA-processing scaffold, but
the observed distribution also argues for shrinking any mechanistic analogue.

RNA-processing and spliceosome perturbations in the same table occupy the high
tail in this class:

| target | `n_degs` |
|---|---:|
| `Rnpc3` | 868 |
| `U2af2` | 828 |
| `Hnrnpu` | 733 |
| `Cdc40` | 624 |
| `Prpf6` | 454 |
| `Thoc1` | 303 |
| `Snrnp70` | 213 |
| `Tardbp` | 210 |
| `Matr3` | 149 |
| `Hnrnpc` | 122 |
| `Hnrnpa2b1` | 11 |
| `Ddx3x` | 8 |
| `Son` | 0 |

Direct Parquet checks in the exact `151 TH Prkcd Grin2c Glut` context confirmed
that these are broad profiles over 17,259 measured genes per target, not count
rounding artifacts. Several high-response splicing and nuclear-transport
perturbations also significantly lowered measured `Srrm2` itself, including
`Rnpc3`, `Tpr`, `Tnpo3`, `Cdc40`, `U2af2`, `Thoc1`, and `Prpf6`. That recurrence
linked `Srrm2` to the high-count RNA-processing state rather than to the
screen-wide null majority.

The strongest boundary was `Son`: it is the closest named SRRM2 speckle partner
in the biology bundle and had zero significant genes in the training count
table. Its 51 recovered perturbed TH nuclei make it weaker than the higher-power
`U2af2`, `Hnrnpu`, `Rnpc3`, and `Cdc40` measurements, but it is still evidence
against treating an SRRM2 scaffold knockout as equivalent in scale to the
largest catalytic spliceosome perturbations.

## Point synthesis

I therefore forecast a clear nonzero response, but near the lower edge of the
RNA-processing high tail rather than around the 600-900 DEG core-spliceosome
cluster. The selected point, 150 DEGs, matches the empirical 98th percentile of
all training perturbations and sits at the moderate RNA-binding/splicing scale
marked by `Hnrnpc` at 122 and `Matr3` at 149, after upward adjustment for
near-universal `Srrm2` reach and downward adjustment for the quiet `Son`
boundary and endpoint mismatch.

Prediction: `Srrm2 -> 150`
