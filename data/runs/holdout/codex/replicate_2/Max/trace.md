# Direct n_degs forecast for Max

Target: `Max`
Cell class: `151 TH Prkcd Grin2c Glut`
Endpoint: measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`

## Evidence used

The declared biology-only Max bundle was endpoint-blind: `target_outcome_exposed`
was false in the runtime `biology` view. It says Max is a dynamic nuclear bHLHZip
component of MYC-MAX and MAX-repressor E-box transcription-factor complexes.
The exact in-assay reach for the focal cell class is detectable but not
ubiquitous: in matched non-target nuclei, `Max` had mean cp10k 0.4517 and was
detected in 11,468 of 23,679 nuclei, or 48.43%. The functional-stock card argues
that a disruptive edit should substantially deplete dimerization-competent MAX
over the 21-28 day P16-to-P37/P44 window, because MAX is a soluble renewed
complex component rather than an installed durable structure. The same bundle
also leaves the major endpoint extrapolation unresolved: clean loss evidence is
from early mouse embryos and conditional B cells, and no matched P16-like
postnatal thalamic neuronal Max deletion clock or phenotype was identified.

The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` count table has
1,674 visible training targets. Its response-count distribution is strongly
zero-inflated in this class:

- 1,205 / 1,674 targets have `n_degs = 0`.
- 469 / 1,674 have a nonzero count.
- The median is 0; the 75th percentile is 1; the 90th percentile is 2; the 95th
  percentile is 18.
- The mean is 14.05 only because of a narrow heavy tail; just 43 targets reach
  at least 100 DEGs.

I chose training perturbations from the biology of the Max bundle rather than
from outcome proximity. The visible direct MAX-network perturbations in the
count table were:

| comparator | rationale | n_degs |
| --- | --- | ---: |
| `Myc` | MYC-family MAX partner | 0 |
| `Mycn` | MYC-family MAX partner | 0 |
| `Mnt` | MAX/MXD/MNT repressor arm | 0 |
| `Mga` | MAX-associated repressor arm | 2 |

`Mycl` and `Mlx` were not present in the declared training count table. I also
checked two broader E-box/bHLH perturbations present in training, `Clock` and
`Tfap4`; these had 3 and 0 DEGs, respectively.

The matched expression parquet was then used to compare the six visible
MAX/MYC-side training profiles in `151 TH Prkcd Grin2c Glut`. The profile tool
recomputed their focal profiles from the Parquet and reported four nodes with
no significant features and two with only `1_to_9_significant_features`:

- `Myc`: 0 significant features
- `Mycn`: 0 significant features
- `Mnt`: 0 significant features
- `Mga`: 2 significant features
- `Clock`: 3 significant features
- `Tfap4`: 0 significant features

This confirmed that the quiet count-table values were not a sorting or manifest
artifact. The pairwise profile view linked these low-count profiles to each
other through broad, non-significant log-fold patterns, but the significant
programs themselves remained essentially absent.

## Synthesis

MAX is reachable and should lose functional stock by harvest, so I did not
forecast a hard technical null. But the relevant training evidence points
tightly toward a near-null recovered-neuron signature: loss of the assayed MYC
activator partners was silent, loss of Mnt was silent, and loss of Mga produced
only 2 DEGs in the same cell class. That argues that the MYC/MAX and
MAX-repressor circuit is either weakly used in these postmitotic thalamic
neurons, buffered at the transcriptome level, or diluted by the approximately
48% target-expression reach and sparse editing design. The direct comparator
mean was 0.5 DEGs, the broader six-comparator mean was 0.83 DEGs, and the
training distribution places counts of 0-1 below the 75th percentile but still
in the dominant response regime.

I therefore place `Max` just above the all-zero partner null to acknowledge that
MAX is the common dimerization component for several complexes, while keeping
the forecast at the near-null scale set by the observed partner perturbations.

Predicted `n_degs`: 1
