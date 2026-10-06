# Satb1 151 TH Prkcd Grin2c Glut forecast

## Endpoint and declared inputs

- Target: `Satb1` from the declared one-row holdout manifest.
- Endpoint: `n_degs`, the count of measured genes in `151 TH Prkcd Grin2c Glut` with BH-adjusted Wilcoxon `p < 0.05`.
- Direct training surface: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Differential-expression surface: `[local file: training_de_all_cell_groups.parquet]`.
- Target biology bundle: `[local file: Satb1.json]`, served through `distributed_agents_runtime.characterization_bundle(target="Satb1", view="biology")`; the bundle reports `target_outcome_exposed=false` and was built with `endpoint_values_used=false`.

## Evidence Used

The focal count table contains 1,674 training perturbations and excludes `Satb1`. It is highly zero-inflated: 1,205 perturbations have `n_degs=0`, the median is 0, the 75th percentile is 1, and only 103/1,674 exceed 10 DEGs. A positive Satb1 forecast therefore needs perturbation-specific support rather than a generic nonzero prior.

The Satb1 biology bundle supports real target engagement within the P16 to P37-P44 interval. SATB1 is a renewable nuclear chromatin organizer/transcriptional regulator; successful editing should stop new SATB1 production while leaving pre-existing SATB1-shaped RNA, protein, and morphology to decay. The bundle adjudicates `functional_stock_by_harvest=likely_substantially_depleted`, based in part on direct adult postmitotic-neuron knockdown in which SATB1 became undetectable and neuronal state changed by 14 days. The bundle also reports partial but material in-assay focal expression reach: 10,806 of 23,679 matched non-target nuclei in `151 TH Prkcd Grin2c Glut` expressed Satb1, `pct_cells_expressing=45.635%`, with `mean_log1p_cp10k=0.297`.

Those same biology facts limit the expected scale. SATB1-positive thalamic cells are only a subset of the aggregated 151 class; no direct Satb1 loss experiment in thalamic neurons was located by the bundle; and survivor conditioning can attenuate a 21-28 day snRNA-seq signature if effective loss removes the most vulnerable SATB1-positive cells before harvest.

I used same-experiment corpus Findings for training perturbations only as semantic context, not as independent replication. They place active chromatin regulators in this focal class but also show non-interchangeability: `Ctcf` produced a broad thalamic/midbrain response with a CTCF-dominant protocadherin module, `Chd4` produced a concentrated 151 response, `Bptf` shared only a partial same-direction module with `Ctcf`, and `Arid2` participated in a 151 BAF/mSWI/SNF branch. By contrast, the close SATB-family paralog `Satb2` was completely flat after juvenile perturbation in the same experiment.

Exact FDR<0.05 focal counts from the declared training table for the most informative comparators were:

| training target | `n_degs` in 151 |
|---|---:|
| `Ctcf` | 270 |
| `Chd4` | 100 |
| `Bptf` | 65 |
| `Arid2` | 56 |
| `Arid1a` | 22 |
| `Smarce1` | 11 |
| `Adnp` | 25 |
| `Atrx` | 8 |
| `Crebbp` | 8 |
| `Arid1b` | 1 |
| `Ep300` | 0 |
| `Bcl11b` | 0 |
| `Satb2` | 0 |

I also compared 38 chromatin/postnatal-TF training signatures in the 151 parquet rows with `distributed_agents_runtime.profile_compare`, writing `workbench/chromatin_tf_profile_compare.json`, and inspected `workbench/chromatin_tf_profile_inspect.json` via `profile_table`. This recovered the exact FDR<0.05 activity levels above for `Ctcf`, `Chd4`, `Bptf`, `Arid2`, and `Satb2`, and showed that the active chromatin branches do not share a single dense focal DE module. For example, the selected-pair FDR intersections around `Arid2`, `Bptf`, `Chd4`, and `Ctcf` versus BAF/chromatin peers were small relative to each source count and often had some direction conflicts.

## Synthesis

Satb1 should not be treated as another flat cortical projection-identity TF: it is expressed in the focal thalamic class, has postnatal/postmitotic neuronal loss evidence, and the relevant SATB1 chromatin-regulatory stock should substantially decline inside the assay window. At the same time it is narrower than the large, broadly expressed chromatin hits. Its exact focal expression reaches about 46% of the assayed non-target population, the prior phenotype is not thalamic, and loss can be survivor-attenuated.

I therefore placed Satb1 below the direct active chromatin anchors `Bptf` and `Arid2` in this class, above the sparse `Adnp`/`Atrx`/`Crebbp` boundary, and far above the `Satb2`/`Bcl11b` flat developmental-axis boundary. The resulting point forecast is a modest but clearly nonzero response:

`predicted_n_degs = 32`
