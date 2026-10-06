# Direct forecast trace

## Target and endpoint

- Manifest target: `Epha7`
- Cell class: `151 TH Prkcd Grin2c Glut`
- Endpoint: number of measured genes with BH-adjusted Wilcoxon `p < 0.05`
- Prediction: `1`

I used the one-row manifest, the canonical `Epha7` biology bundle, the declared
training count table
`151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`, and filtered rows from the
declared `training_de_all_cell_groups.parquet`. I did not use an `Epha7`
Perturb-seq signature, an `Epha7` endpoint count, labeled-neighbor outcomes, or
any calibration artifact.

## Biology bearing

The canonical bundle places `Epha7` in a plausible but local receptor-signaling
category. EphA7 is a membrane Eph receptor with both full-length kinase-positive
and kinase-negative neuronal pools; the functional-stock card judged a P16 edit
likely to substantially deplete affected renewable receptor pools by the
P37-P44 harvest, with uncertainty from the unspecified edit site and missing
EphA7 isoform turnover measurements.

The exact focal-population reach argues that `Epha7` is technically observable
in this class: 19,764 of 23,679 non-target nuclei expressed it
(`83.47%`), with mean raw UMI `3.206`, mean log1p CP10K `0.928`, and
pseudobulk CPM `200.945`. That supports the possibility of one self-feature
call if the edited alleles yield visible transcript loss, but it does not prove
editing strength or a downstream transcriptional state.

The phenotype evidence is weaker for a broad acute thalamic RNA response:
postnatal cortical phenotypes and embryonic thalamic patterning establish neural
function, but not a matched juvenile thalamic loss phenotype after a P16 sparse
edit. Possible `Epha4` overlap in developing thalamus also leaves redundancy
unresolved.

## Training measurements

The full target training table for this cell class is very zero-heavy:

- 1,205 of 1,674 training perturbations have `n_degs = 0`.
- The median is `0`; the 75th percentile is `1`.
- 1,571 of 1,674 perturbations have `n_degs <= 10`.
- The large tail consists of broad regulators rather than cell-surface axon
  guidance receptors.

The closest visible Eph-receptor perturbations are almost all null in the same
count table and in a direct Parquet check over 17,259 measured genes per target:

| target | n_degs | significant measured genes |
|---|---:|---|
| `Epha10` | 0 | none |
| `Epha2` | 0 | none |
| `Epha3` | 0 | none |
| `Epha4` | 1 | `Epha4` |
| `Epha5` | 0 | none |
| `Ephb1` | 0 | none |
| `Ephb2` | 0 | none |
| `Ephb4` | 0 | none |

I broadened the check to 25 visible surface receptor, axon-guidance, and
synaptic adhesion perturbations: `Epha2`, `Epha3`, `Epha4`, `Epha5`, `Epha10`,
`Ephb1`, `Ephb2`, `Ephb4`, `Dcc`, `Robo1`, `Robo2`, `Robo4`, `Unc5c`, `Unc5d`,
`Plxna1`, `Plxna2`, `Plxna4`, `Plxnd1`, `Nrp1`, `Nrp2`, `Ntrk2`, `Ntrk3`,
`Lrrtm1`, `Lrrtm3`, and `Lrrtm4`. Nineteen had zero significant genes; five
had one; only `Ntrk2` was larger, at three. Four of the one-gene calls were
the target transcript itself: `Epha4`, `Plxna2`, `Robo1`, and `Unc5c`.

A symmetric observed-profile comparison of those 25 perturbations in
`151 TH Prkcd Grin2c Glut` did not reveal a shared, scalable response program:
all pairwise significant-program overlaps in the cohort were zero where they
were defined, and the median top-tail overlap coefficients were only `0.02` for
the positive tail and `0.04` for the negative tail.

## Synthesis

`Epha7` is better expressed in the focal population than a pure absent-target
null, and its receptor stock is likely at least partly depleted by harvest, so
I round the Eph-family zero/one expectation upward rather than to a hard zero.
The training data for closely related Eph receptors and for broader guidance
receptors argue against anything beyond an isolated self-feature or singleton
response: the direct Eph cohort is `7/8` null with only `Epha4 = 1`, and the
expanded receptor cohort stays in the `0-3` range. I therefore predict a
single significant measured gene.
