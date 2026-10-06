# Avpr2 direct DEG-count forecast

## Target and endpoint

- Target perturbation: `Avpr2`
- Focal population: `151 TH Prkcd Grin2c Glut`
- Endpoint: number of measured genes with BH-adjusted Wilcoxon `p < 0.05`

## Evidence used

The canonical Avpr2 biology bundle made target reach the decisive feature. In the exact focal-population measurement, `Avpr2` had only 1 target UMI across 23,679 non-target nuclei:

- `n_cells_expressing = 1`
- `pct_cells_expressing = 0.004223151315511635`
- `mean_raw_umi = 4.223151315511635e-05`
- `pseudobulk_cpm = 0.0026467986875912232`

The same bundle adjudicates functional stock as likely to clear within the P16-to-P37/P44 window if the receptor is actually present: Avpr2 is a dynamic membrane GPCR, and heterologous pulse-chase measurements put V2 receptor turnover on an hours-scale clock. I therefore did not treat stock persistence as a reason for a false null. The limiting biology is instead that the assayed thalamic NeuN-positive nuclei essentially do not express the receptor.

The external biology summarized in the Avpr2 source card also points away from a thalamic neuronal transcriptional footprint. Functional-null mouse phenotypes are renal/systemic nephrogenic diabetes insipidus, kidney is the strong expression context, and regional assays did not detect Avpr2 in mouse thalamus or an assayed whole-brain sample. Those priors are weaker than the exact in-assay expression measurement, but they agree with it.

The declared `151 TH Prkcd Grin2c Glut` training count table is sparse: 1,205 of 1,674 training targets have `n_degs = 0`. More specifically, focal-class losses of close receptor or receptor-proximal analogues were all zero:

| training target | `n_degs` in `151 TH Prkcd Grin2c Glut` |
| --- | ---: |
| `Avpr1a` | 0 |
| `Avpr1b` | 0 |
| `Oxtr` | 0 |
| `Crhr1` | 0 |
| `Gnas` | 0 |
| `Adra1a` | 0 |
| `Adra2a` | 0 |
| `Agtr1a` | 0 |
| `Plcb1` | 0 |
| `Prkca` | 0 |
| `Mapk1` | 0 |

A filtered read of the focal Parquet rows for the same GPCR/signaling cohort confirmed those zero counts across 17,259 measured features per selected perturbation. The zero receptor-side results were not just because the thalamic class is unable to show DE: in the same focal count table and Parquet check, `Grin1` had 89 BH<0.05 genes, `Creb1` had 10, and the nearby `Camk2b` and `Prkcg` perturbations each had 1.

Same-experiment corpus context supported the same interpretation without exposing Avpr2 outcome data. The selected release had no Avpr2 findings or explicit Avpr2 related-target records. For the visible vasopressin/oxytocin receptors, it instead described `Avpr1b` as flat across all measured neuronal groups, `Oxtr` as mostly flat with only three isolated all-brain hits, and the `Avpr1a`/`Avpr1b`/`Oxtr` family as non-convergent rather than a shared basal GPCR transcriptional module.

## Synthesis

Avpr2 is a rapidly renewable receptor if expressed, so an edited Avpr2-expressing neuron should eventually lose functional V2R during the 21-28 day assay window. But in the exact focal population there is essentially no Avpr2 transcript to support a direct cell-autonomous perturbation: one expressing nucleus out of 23,679 is below a plausible reach for a recovered-population FDR-level signature. The most relevant visible receptor perturbations are also zero in this thalamic class, while stronger synaptic/signaling targets show the class has statistical visibility when biology creates a response.

Those upward and downward bearings put the best integer forecast at the modal floor:

`predicted_n_degs = 0`
