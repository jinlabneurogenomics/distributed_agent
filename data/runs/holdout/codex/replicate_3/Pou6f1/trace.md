# Pou6f1 n_degs forecast

## Target and endpoint

- Exact manifest target: `Pou6f1`.
- Focal population: `151 TH Prkcd Grin2c Glut`.
- Endpoint to predict: `n_degs`, the number of measured genes in this target/population contrast with BH-adjusted Wilcoxon `p < 0.05`.

The held-out `Pou6f1` signature and count were not used.

## Biology bundle evidence

The declared `Pou6f1` bundle supports real but only partially localized assay observability:

- exact focal reach: `Pou6f1` was detected in `10,239 / 23,679` non-target nuclei in `151 TH Prkcd Grin2c Glut`, `43.240846%`, with mean CP10K `0.413999` and mean raw UMI `0.646227`;
- molecular operation: POU6F1 is a nuclear, sequence-specific POU-domain transcriptional regulator;
- functional stock: a disruptive edit should stop synthesis of intact DNA-binding protein and the soluble nuclear protein stock is expected to be substantially depleted after the 21-28 day P16-to-P37/P44 window, but the card found no target-specific neuronal half-life or residence time;
- prior phenotype: adult neural conditional `Pou6f1` loss has a phenotype in olfactory-bulb CRHR1-positive granule neurons, not in matched thalamic postmitotic neurons;
- redundancy/context uncertainty: `Pou6f2` is the closest class-6 POU family member, but same-context buffering is unresolved.

I read those fields as making a focal transcriptional response plausible, but not enough to expect a large count: target expression is real in the assayed population, while the strongest functional prior is from a different postnatal neural context and has no transferable onset clock for this thalamic aggregate.

## Focal training count table

The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` table contains 1,674 training targets.

| Quantity | Value |
|---|---:|
| zero-count targets | 1,205 |
| positive-count targets | 469 |
| zero fraction | 0.719833 |
| median `n_degs` | 0 |
| 75th percentile | 1 |
| 90th percentile | 2 |
| 95th percentile | 18 |
| mean `n_degs` | 14.0538 |
| maximum `n_degs` | 2677 |

Thus the direct local prior is a point mass at zero with a long high-count tail; the mean is not a typical perturbation scale in this cell class.

## POU-family training analogs

I used the training count table to inspect the represented POU-family perturbations and then read their exact focal Parquet rows in `training_de_all_cell_groups.parquet`.

| training target | focal `n_degs` | focal measured genes | min adjusted p | matched perturbed nuclei |
|---|---:|---:|---:|---:|
| `Pou2f1` | 0 | 17,259 | 0.368918 | 173 |
| `Pou2f2` | 0 | 17,259 | 1.0 | 166 |
| `Pou3f3` | 0 | 17,259 | 0.849340 | 419 |
| `Pou3f4` | 0 | 17,259 | 0.758616 | 220 |
| `Pou4f3` | 0 | 17,259 | 1.0 | 241 |
| `Pou5f1` | 0 | 17,259 | 1.0 | 143 |
| `Pou6f2` | 0 | 17,259 | 1.0 | 182 |

These were not merely threshold rounding cases. The closest family member in the table, `Pou6f2`, had no gene close to focal BH significance, and all six assayed POU relatives had `n_degs = 0` in the exact target population.

The same-experiment corpus, which is a curated interpretation of the same screen rather than an independent replication, agreed with this low-response read:

- `Pou6f2:F001`: `Pou6f2` had no FDR < 0.10 downstream genes in any of 23 measured neuronal cell groups after P16 loss of function.
- `Pou6f2:F003` and its POU-family Claim: the represented POU targets did not reveal a generic acute POU-family response in P16 brain neurons; shared POU-homeodomain membership was insufficient to produce interchangeable acute neuronal CRISPR transcriptional phenotypes.

## Synthesis

The exact focal expression bundle prevents treating `Pou6f1` as a pure no-reach null, and its functional-stock card argues that intact POU6F1 should decline by harvest. Those upward bearings are weakly to moderately favorable for at least a tiny response.

The quantitative analog evidence points lower. In the same focal endpoint, the closest assayed family member `Pou6f2` and every other represented POU factor were FDR-level zeros, with `Pou6f2` flat even across the full assayed neuronal taxonomy. The corpus interpretation also found no generic POU-family acute response after P16 editing. Against the 1,674-target focal distribution, the modal/median response is zero and only 28.0% of training perturbations have even one focal DEG.

I therefore put `Pou6f1` in the low-burden class and round the expected count down to the POU-analog modal value:

`predicted_n_degs = 0`
