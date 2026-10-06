# Srgap3 direct DEG-count forecast

## Target and endpoint

- Target from the one-row holdout manifest: `Srgap3`
- Focal population: `151 TH Prkcd Grin2c Glut`
- Endpoint: number of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`; the self transcript is counted if significant
- Predicted `n_degs`: `0`

## Evidence used

### Target biology and focal reach

The prediction-safe Srgap3 biology bundle resolves the packet to current mouse
`Srgap2`, with `srGAP3` as a historical alias, rather than the distinct current
mouse `Srgap3` locus. The encoded molecular prior is a postsynaptic and
membrane-remodeling F-BAR/RhoGAP/SH3 protein whose acute loss in postmitotic
mouse cortical neurons alters dendritic spines within 9-10 days. The functional
stock card therefore calls target-dependent stock likely substantially depleted
by the P37-P44 harvest after a P16 edit, but with partial evidence: the
sub-window phenotype is cortical, the target-specific neuronal protein
half-life was not found, and transfer to thalamic neurons is unresolved.

The exact focal-population reach is real but diluted. In matched non-target
`151 TH Prkcd Grin2c Glut` nuclei, `Srgap3` was detected in 7,313 of 23,679
nuclei, or 30.8839%, with mean raw UMI 0.4431, mean CP10K 0.2708, mean
log1p(CP10K) 0.1847, pseudobulk CPM 27.7729, and total target UMI 10,493.
That supports target availability in this cell class, but not a strong,
class-wide transcriptomic response.

### Training count scale in the matched endpoint

The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` table contains
1,674 training perturbations and excludes `Srgap3`. It is strongly concentrated
at the bottom:

| range of `n_degs` | training perturbations |
| --- | ---: |
| 0 | 1,205 |
| 1 | 276 |
| 2-3 | 46 |
| 4-10 | 44 |
| 11-100 | 61 |
| >100 | 42 |

The median training count is 0, the 75th percentile is 1, the 90th percentile
is 2, and the mean is pulled up to 14.05 by a small high-response tail.

### Mechanism-matched training perturbations

I treated perturbations in the Rho/Rac/Cdc42, actin-spine, postsynaptic
scaffold, Slit/Robo, and related growth-factor signaling neighborhoods as the
closest quantitative training analogs. In the same focal population, a regex
panel of 59 such cytoskeleton/synapse/guidance/NMDAR-neighbor genes had median
0; 43 of 59 had no significant gene, 52 of 59 had at most one significant gene,
57 of 59 had at most three, and only `Grin1` exceeded 10.

Direct checks against the declared Parquet in `151 TH Prkcd Grin2c Glut`
confirmed that this was not solely a precomputed-count artifact. Representative
matched perturbation counts were in the usual range, but their RNA outputs were
flat or nearly flat:

| training perturbation | `n_degs` in count table | selected interpretation |
| --- | ---: | --- |
| `Arhgap18` | 0 | RhoGAP-family neighbor, no focal DEG |
| `Arhgap32` | 0 | RhoGAP-family spine regulator, no focal DEG |
| `Arhgef9` | 1 | self-transcript only |
| `Cdc42` | 1 | self-transcript only |
| `Rac1` | 0 | no focal DEG |
| `Pak1` | 1 | self-transcript only |
| `Pak2` | 0 | no focal DEG |
| `Pak3` | 0 | no focal DEG |
| `Dock3` | 0 | no focal DEG |
| `Kalrn` | 0 | no focal DEG |
| `Dlg4` | 1 | self-transcript only |
| `Shank2` | 0 | no focal DEG |
| `Shank3` | 2 | self-transcript plus one additional hit |
| `Robo1` | 1 | self-transcript only |
| `Robo2` | 0 | no focal DEG |
| `Slit2` | 0 | no focal DEG |
| `Ntrk2` | 3 | sparse TrkB response |
| `Grin1` | 89 | clear thalamic outlier, not shared by other NMDAR or Rho/spine perturbations |

The same-experiment corpus packages the same surfaces, so it is not independent
replication, but its Claims help guard the analog interpretation: represented
Rac/Cdc42-linked actin-cytoskeleton perturbations are reported as
transcriptionally buffered rather than a recurrent nuclear mRNA module;
represented postsynaptic scaffold and synaptic adhesion perturbations generally
do not induce a shared steady-state RNA module; and represented Slit/Robo and
other axon-guidance ligand/receptor perturbations do not produce a robust
neuronal soma transcriptomic module.

## Numeric synthesis

The biology bundle makes an effective perturbation plausible: new Srgap2 supply
should be blocked, the stock is expected to clear enough by harvest, and the
target transcript is present in the focal thalamic class. The endpoint-specific
training data nevertheless place this molecular family at the bottom of the
focal-count distribution. Close Rho-family, PAK, actin-spine, and PSD
perturbations are mostly 0, and the few one-count cases are usually the target
self transcript rather than a downstream module. Because this target is
expressed in only about one third of focal non-target nuclei and no
Srgap2-specific thalamic RNA state or recurrent training analogue supported a
Grin1-like response, the most defensible point estimate is the low-end value:
`0` BH-significant genes.
