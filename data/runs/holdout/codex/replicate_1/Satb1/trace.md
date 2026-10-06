# Direct forecast trace

## Target and endpoint

- Held-out target: `Satb1`, from the one-row declared manifest.
- Cell population: `151 TH Prkcd Grin2c Glut`, exactly resolved as a thalamic glutamatergic neuronal class.
- Endpoint: `n_degs`, the number of measured genes with BH-adjusted Wilcoxon `p < 0.05` in the held-out `Satb1` perturbation profile.
- The target itself is absent from the declared 151-count training table: 1,674 training targets were present and `Satb1` was not among them.

## Target biology used

The declared `Satb1` biology bundle supports functional realization but not full-population reach:

- SATB1 is a nuclear DNA-binding genome organizer and context-specific transcriptional regulator, including recruitment of NuRD/HDAC and ACF/ISWI remodeling machinery.
- A successful P16 edit should substantially deplete functional SATB1 by the P37-P44 harvest in cells that actively express SATB1. The card's strongest timing anchor is adult postmitotic dopaminergic-neuron knockdown, where SATB1 and neuronal state changed by about 14 days, before this screen's 21-28 day interval.
- Exact focal-population expression is partial, not pan-class: in the `151 TH Prkcd Grin2c Glut` non-target nuclei, `Satb1` was detected in 10,806 of 23,679 cells, or 45.635%, with mean raw expression 0.716 UMI/cell and pseudobulk 44.895 CPM.
- Direct thalamic loss-of-function evidence was not located in the bundle, and survivor conditioning could attenuate the measured snRNA-seq response if the most affected cells were depleted before harvest.

## Training count scale

The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` table is very zero-inflated:

- `n = 1674` training perturbations.
- 1,205/1,674 had `n_degs = 0`.
- Median = 0, 75th percentile = 1, 90th percentile = 2, 95th percentile = 18, 99th percentile = 430.
- Only 106/1,674 had at least 10 DEGs, and 59/1,674 had at least 50.

Operation-related or adjacent transcription/chromatin regulators showed a wide but informative local scale at the same FDR threshold:

| target | `n_degs` |
|---|---:|
| `Satb2` | 0 |
| `Bcl11a` | 0 |
| `Bcl11b` | 0 |
| `Zbtb20` | 0 |
| `Arid1b` | 1 |
| `Smarca2` | 1 |
| `Mef2c` | 1 |
| `Crebbp` | 8 |
| `Mecp2` | 16 |
| `Setdb1` | 22 |
| `Arid1a` | 22 |
| `Adnp` | 25 |
| `Chd2` | 34 |
| `Arid2` | 56 |
| `Chd8` | 61 |
| `Chd4` | 100 |
| `Ctcf` | 270 |
| `Wac` | 384 |
| `Yy1` | 720 |
| `Zbtb7a` | 841 |

I used `Chd4`, `Ctcf`, and the broader `Wac`/`Yy1`/`Zbtb7a` group as proof that this thalamic class has power to detect chromatin-regulator responses, but discounted them as magnitude comparators because they are broader or more core than SATB1 and the corpus reports their programs as target-specific rather than generic chromatin phenocopies.

The closest family member in the training table, `Satb2`, was a null. I did not use that as a direct quantitative analog because the same-experiment corpus interprets the `Satb2` null as a juvenile/postmitotic buffering of the cortical projection-neuron identity axis, whereas the `Satb1` bundle supports continuing postnatal SATB1 function in expressing cells. I did use it, together with `Bcl11a`, `Bcl11b`, and `Zbtb20`, as a warning that famous developmental DNA-binding factors can be quiet after P16 editing.

## Profile check

I compared 28 observed transcriptional/chromatin perturbations in the exact `151 TH Prkcd Grin2c Glut` context with `dataset.candidate_profile_review.profile_compare`, then summarized that caller-declared cohort with `profile_cohort`.

- Missing profiles: 0/28.
- Response bins among these selected regulators: 9 no significant genes, 6 with 1-9, 5 with 10-49, and 8 with at least 50.
- The cohort had stronger shared negative-tail rank structure than positive-tail structure, but FDR-supported program overlap was mostly sparse. This supports treating the moderate chromatin perturbations as loose scale guides rather than averaging all of them into a single module.

## Numeric synthesis

My point estimate is above zero because SATB1 is not merely a preinstalled embryonic fate factor in the card: functional stock should be renewed, substantially depleted by harvest, and incompletely buffered in SATB1-positive cells. I kept it well below `Chd4` and `Ctcf` because the exact focal-population reach is only 45.6%, the thalamic loss prior is cross-context, and any severe effect could be survivor-conditioned out of the assayed nuclei.

The resulting scale is closest to the lower active chromatin/neuronal-regulator band: `Mecp2` 16, `Setdb1` 22, `Arid1a` 22, `Adnp` 25, and `Chd2` 34. I therefore predict a small-to-moderate response:

`predicted_n_degs = 25`
