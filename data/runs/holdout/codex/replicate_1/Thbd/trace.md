# Direct Thbd forecast trace

## Target and endpoint

- **Target:** `Thbd`
- **Focal population:** `151 TH Prkcd Grin2c Glut`
- **Endpoint:** `n_degs`, the number of measured genes with BH-adjusted Wilcoxon `p < 0.05` for that perturbation in the focal population.
- **Predicted `n_degs`:** **0**

## Evidence that determined the forecast

### Canonical Thbd biology bundle

The declared `Thbd` biology bundle was the primary target-specific evidence. Its exact focal-population expression measurement shows that `Thbd` is essentially absent from the assayed thalamic NeuN-positive nuclei:

| quantity | value |
|---|---:|
| non-target nuclei in `151 TH Prkcd Grin2c Glut` | 23,679 |
| nuclei expressing `Thbd` | 50 |
| percent nuclei expressing `Thbd` | 0.2111575658 |
| mean raw UMI | 0.0022805017 |
| mean CP10K | 0.0014811685 |
| pseudobulk CPM | 0.1429271291 |

That exact in-assay reach superseded qualitative expression priors for prediction. The same bundle identified THBD's established operation as a vascular endothelial type-I membrane receptor that binds thrombin and redirects it toward protein-C activation and related anticoagulant or fibrinolytic substrates. Mouse loss evidence supports severe endothelial/systemic coagulation phenotypes, including postnatal fatal coagulopathy, but the bundle found no postnatal neuronal Thbd-loss context and placed the available brain signal in vasculature rather than thalamic projection neurons.

The functional-stock adjudication did not rescue a large predicted neuronal response. It concluded that a disruptive edit should stop new receptor supply in a truly `Thbd`-expressing cell, but basal thrombomodulin clearance through 21-28 days was not established and the main limiting point for this endpoint was that the assayed postmitotic thalamic neurons have almost no target expression or known cell-intrinsic THBD function to remove.

The selected same-experiment corpus release had no packaged Thbd Findings, Claims, or explicit target references, so there was no same-corpus perturbation report that added a neuronal mechanism or a measured profile analogue for `Thbd`.

### Declared training counts in the same focal population

The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` table contains 1,674 training perturbations for the exact focal population. It is highly zero-skewed:

| summary | value |
|---|---:|
| training perturbations | 1,674 |
| `n_degs = 0` | 1,205 |
| `n_degs > 0` | 469 |
| median `n_degs` | 0 |
| 75th percentile | 1 |
| 90th percentile | 2 |

I used vascular, coagulation, and non-neuronal surface/secreted perturbations present in the declared table as quantitative anchors because they are closer to `Thbd` than housekeeping or neuronal genes:

| training target | same-class `n_degs` |
|---|---:|
| `Acvrl1` | 0 |
| `C3` | 0 |
| `Eng` | 0 |
| `F2` | 0 |
| `Flt4` | 0 |
| `Kdr` | 0 |
| `Tek` | 0 |

Querying the declared `training_de_all_cell_groups.parquet` for those same perturbations in `151 TH Prkcd Grin2c Glut` confirmed that each had 17,259 assayed gene-level rows and zero genes with `pvals_adj < 0.05`; their matched recovered perturbed-nucleus counts were in the same low-hundreds range:

| training target | assayed rows in parquet | rows with `pvals_adj < 0.05` | matched perturbed nuclei |
|---|---:|---:|---:|
| `Acvrl1` | 17,259 | 0 | 208 |
| `C3` | 17,259 | 0 | 231 |
| `Eng` | 17,259 | 0 | 171 |
| `F2` | 17,259 | 0 | 239 |
| `Flt4` | 17,259 | 0 | 235 |
| `Kdr` | 17,259 | 0 | 167 |
| `Tek` | 17,259 | 0 | 184 |

## Reasoning

The focal atlas class is a high-yield class, so a biologically engaged perturbation can be visible there. `Thbd` is nevertheless a poor candidate for a focal neuronal transcriptional response: its canonical biology is endothelial and extracellular, the severe prior phenotypes are vascular/systemic rather than neuronal, and the exact focal expression measurement leaves only 50 of 23,679 non-target nuclei with any `Thbd` UMI. Sparse CRISPR editing of a locus that has essentially no transcript or cell-intrinsic role in the recovered thalamic neurons should usually leave no detectable survivor-conditioned nuclear RNA program.

The training distribution agreed with that interpretation. Perturbations of several vascular or coagulation-associated targets that are much closer to THBD's biology than neuronal regulators all had exact zero DEG counts in the same population and zero significant rows when checked directly in the Parquet. The low target-expression measurement therefore was not treated as a generic weak-response prior; it specifically pushed the forecast to the point mass already occupied by the matched non-neuronal vascular/coagulation training analogues.

I did not use the withheld `Thbd` perturbation signature or target DEG count. Given the tiny neuronal reach and zero-count behavior of the closest available training anchors, the endpoint-specific point prediction is:

```tsv
target_name	predicted_n_degs
Thbd	0
```
