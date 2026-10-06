# Pdhb forecast for 151 TH Prkcd Grin2c Glut

## Declared target and endpoint

- Target from the one-row holdout manifest: `Pdhb`.
- Endpoint: `n_degs`, the count of measured genes with BH-adjusted Wilcoxon `p < 0.05` in `151 TH Prkcd Grin2c Glut`.
- Target outcome use: none. `Pdhb` was absent from the declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`; the target biology bundle exposed exact focal expression but no `Pdhb` response count or expression signature.

## Evidence used

### Pdhb biology-only bundle

The canonical bundle identifies PDHB as an obligate beta subunit of the mitochondrial pyruvate dehydrogenase E1 alpha2-beta2 heterotetramer. A disruptive edit should stop new functional beta-subunit production, and no same-neural-context paralogous replacement was found, so a realized lesion is biologically reachable.

The same bundle also weakens a large short-window response forecast. The operative stock is pre-existing assembled PDH E1, not free transcript; editing does not instantly disable heterotetramers already assembled before P16. PDHB abundance can be proteasome-sensitive, but the bundle did not find a P16-P37/P44 postmitotic thalamic-neuron half-life or an acute postnatal loss clock, so it adjudicates functional stock at harvest as only `partially_depleted_or_leading_edge`. Germline mouse and zebrafish phenotypes establish developmental neural importance, not acute postnatal thalamic timing.

The exact focal-population expression reach is high: `Pdhb` is detected in 21,831 of 23,679 non-target nuclei in this class, 92.20% expressing, with mean raw UMI 3.46 and pseudobulk CPM 216.95. That makes the transcript itself well measured, but it does not prove either functional engagement or downstream response.

### Training count table

The focal-class training count table contains 1,674 targets. It is extremely sparse:

- 1,205/1,674 targets have 0 DEGs.
- Median `n_degs` is 0.
- The 75th percentile is 1.
- The 90th percentile is 2.
- Only 58 targets exceed 50 DEGs.

Closest observed mitochondrial carbon-metabolism perturbations were quiet in the same endpoint:

| comparator | `n_degs` |
|---|---:|
| `Pdha1` | 1 |
| `Dlat` | 1 |
| `Dld` | 0 |
| `Mpc1` | 0 |
| `Aco2` | 0 |
| `Mdh2` | 1 |
| `Ogdh` | 0 |
| `Dlst` | 0 |
| `Suclg1` | 0 |
| `Sucla2` | 1 |
| `Sdha` | 1 |
| `Ndufs4` | 0 |
| `Ndufv1` | 0 |

The two strongest same-operation comparators are `Pdha1`, the E1 alpha partner of PDHB, and `Dlat`, the PDH E2 component. Both have exactly one significant feature.

### Expression parquet check of the close comparators

Filtering `training_de_all_cell_groups.parquet` to `151 TH Prkcd Grin2c Glut` and the close PDH/TCA/OXPHOS comparators above showed that every significant feature among the one-DEG mitochondrial comparators was the self transcript:

| perturbation | significant feature | logFC | BH adjusted p |
|---|---|---:|---:|
| `Pdha1` | `Pdha1` | -1.039 | 1.31e-6 |
| `Dlat` | `Dlat` | -0.673 | 2.81e-7 |
| `Idh3a` | `Idh3a` | -0.817 | 9.27e-11 |
| `Mdh2` | `Mdh2` | -0.840 | 7.37e-5 |
| `Sdha` | `Sdha` | -0.781 | 2.11e-12 |
| `Sucla2` | `Sucla2` | -0.659 | 5.12e-5 |

Thus the local empirical pattern is not an adaptive mitochondrial transcriptome with dozens of downstream DEGs; it is usually no detectable downstream program, with the total count sometimes incremented by a directly targeted transcript.

## Synthesis

`Pdhb` has broad focal expression and an essential, nonredundant PDH E1 role, so I do not assign it to the many training targets that are completely out of reach. However, the training rows most similar to PDH E1/E2 disruption show 0 downstream DEGs in this thalamic class, and the biology bundle leaves enough pre-existing PDH E1 persistence that an acute broad metabolic survivor-state response is not well supported at 21-28 days.

The most likely integer is therefore the same scale as `Pdha1` and `Dlat`: one counted significant gene, attributed to a detectable `Pdhb` self-transcript effect rather than a broad trans response.

Predicted `n_degs`: 1
