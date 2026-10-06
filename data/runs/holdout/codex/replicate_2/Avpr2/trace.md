# Avpr2 direct n_degs forecast

## Requested endpoint

- Target: `Avpr2`
- Cell group: `151 TH Prkcd Grin2c Glut`
- Endpoint: number of measured genes with BH-adjusted Wilcoxon `p < 0.05` in the held-out focal perturbation.
- Prediction: `0`

## Evidence used

### Declared target biology bundle

The exact in-assay focal-population reach for `Avpr2` was essentially absent:

- `group_name`: `151 TH Prkcd Grin2c Glut`
- `n_non_target_cells`: 23,679
- `n_cells_expressing`: 1
- `pct_cells_expressing`: 0.004223151315511635
- `total_target_umi`: 1 across 377,814,907 total non-target RNA UMI
- `mean_cp10k`: 0.000014371792804191373
- `mean_raw_umi`: 0.00004223151315511635

The same bundle adjudicated Avpr2 as a dynamic membrane GPCR whose pre-edit functional stock should clear within the 21-28 day P16-to-P37/P44 editing window if a cell actually expresses it. That stock conclusion prevents discounting `Avpr2` merely because the receptor is pre-existing protein, but it is conditional on a receptor pool being present. The observability card found the established loss phenotype to be neonatal renal nephrogenic diabetes insipidus/systemic lethality rather than a matched postnatal thalamic-neuron requirement, and the source card recorded kidney-biased expression plus regional non-detection in mouse thalamus or assayed whole brain.

### Same-experiment corpus

The selected same-experiment corpus had no packaged bottom-up Findings, Claims, or explicit comparator references for `Avpr2`. I treated this as absence of curated same-experiment semantic evidence, not as an independent measurement or as proof of no effect.

### Declared focal count table

The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` table contained 1,674 non-held-out targets. Its count distribution was sparse:

- 1,205 / 1,674 training perturbations had `n_degs = 0`.
- Median `n_degs` was 0.
- 75th percentile was 1.
- 90th percentile was 2.

Thus a zero count is the modal outcome even in this high-yield thalamic class; a nonzero point needs target-specific or process-specific reason to expect a focal transcriptional response.

### Biology-selected training perturbations from the declared Parquet

I queried the focal `151 TH Prkcd Grin2c Glut` rows of the declared training Parquet for vasopressin-family and proximal cAMP-signaling comparators available in training:

| training target | basis for using as weak comparator | focal n_degs |
| --- | --- | ---: |
| `Avpr1a` | related vasopressin receptor named in the Avpr2 card | 0 |
| `Avpr1b` | related vasopressin receptor named in the Avpr2 card | 0 |
| `Oxtr` | same vasopressin/oxytocin GPCR family | 0 |
| `Gnas` | Gs alpha signaling immediately downstream of V2R | 0 |
| `Adcy1` | adenylyl-cyclase/cAMP effector downstream of Gs | 0 |
| `Adcy3` | adenylyl-cyclase/cAMP effector downstream of Gs | 0 |
| `Adcy5` | adenylyl-cyclase/cAMP effector downstream of Gs | 0 |

The exact Parquet query found 17,259 measured-gene rows per comparator in this focal class and no BH-adjusted `p < 0.05` genes for any of these seven targets. Their minimum adjusted p-values were all nonsignificant: 0.112 for `Adcy3`, 0.139 for `Adcy1`, 0.569 for `Avpr1b`, 0.841 for `Avpr1a`, 0.912 for `Adcy5`, and 1.0 for `Gnas` and `Oxtr`.

## Synthesis

`Avpr2` should be a real, fast-turnover CRISPR loss of V2-receptor function in cells that depend on V2R. The focal population, however, provides almost no substrate for that operation: only one non-target nucleus among 23,679 expressed even one Avpr2 UMI, and the card's positive phenotype evidence is renal/systemic rather than postnatal thalamic. Same-pathway and same-family training perturbations in the exact requested cell group were all transcriptionally quiet. Against a training distribution whose median and mode are already zero, the most biologically supported forecast is therefore no FDR-significant measured genes.

Residual uncertainty is that rare expression, circuit effects, guide-specific DNA damage, or survivor-conditioned sampling could in principle create a small idiosyncratic signature, but no declared evidence pushed the expected count above the zero bin.
