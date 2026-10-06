# Direct forecast trace

## Target and endpoint

- **Target:** `Clip2`
- **Focal population:** `151 TH Prkcd Grin2c Glut`
- **Endpoint:** `n_degs`, the number of measured genes with BH-adjusted Wilcoxon `p < 0.05` in the focal population.
- **Training endpoint table:** `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- **Training expression parquet:** `[local file: training_de_all_cell_groups.parquet]`
- **Target biology bundle:** `[local file: Clip2.json]`

The task target was read from the declared one-row manifest as `Clip2`. The target outcome and target differential-expression profile were not read or reconstructed.

## Clip2 biology used

The canonical biology bundle supports substantial but not perfectly certain CLIP2 loss by harvest:

- CLIP2 is a neuronal cytoplasmic linker associated with microtubules, growing plus ends, and dendritic lamellar bodies.
- A P16 disruptive edit should stop new CLIP2 synthesis but existing protein has to exchange or degrade; the bundle adjudicates the functional stock as `likely_substantially_depleted` over the P37-P44 harvest window.
- Exact in-assay reach is good in the focal population: `Clip2` was detected in `18,303 / 23,679` non-target nuclei, or `77.296%`, with mean `1.096` CP10K and pseudobulk `108.799` CPM.
- The main downward uncertainties are partial CLIP1/CLIP-170 buffering and no matched postnatal thalamic-neuron Clip2 time course or phenotype.

This made a fully inert zero possible but not the central expectation: the target is expressed in most assayed cells and should have lost a dynamic protein pool by 3-4 weeks.

## Same-experiment corpus

The selected same-experiment corpus had no direct `Clip2` Findings, Claims, or explicit references. I therefore used related microtubule/dynactin/tubulin findings as context, not as direct replication.

Two corpus claims were decision-relevant:

- `claim:edf51d701dda34edf161` reports that represented MAP, tubulin, EB, dynactin, kinesin, CAMSAP, and MARK-related perturbations generally **do not form a coherent shared postnatal neuronal mRNA compensation or cytoskeletal-stress module**, except for a restricted `Tuba1a` tubulin-isotype response.
- `claim:ca803b2ea88defcf5d1a` reports that `Tuba1a`, not other measured tubulin/microtubule-related targets, uniquely elicits the small tubulin-paralog RNA module in the two responsive groups including `151 TH Prkcd Grin2c Glut`.

I treated these as evidence against assigning `Clip2` a broad cytoskeletal transcriptional program merely because it sits on microtubules. `Dctn1` was also useful as a boundary: its corpus record describes a detectable SREBF2-like sterol/cholesterol module, but explicitly distinguishes that module from generic sampled cytoskeletal or trafficking-neighborhood perturbations.

## Training measurements

The focal count table is very sparse:

- `n = 1,674` training targets
- `1,205` have `n_degs = 0`
- `1,481` have `n_degs <= 1`
- median `0`, 75th percentile `1`, 90th percentile `2`
- mean `14.054`, driven by a small number of very broad responses

Biology-selected cytoskeletal and microtubule-neighborhood counts in the same table were:

| target | n_degs |
|---|---:|
| Camsap1 | 0 |
| Dctn1 | 75 |
| Dpysl5 | 0 |
| Kif1a | 1 |
| Kif2a | 0 |
| Kif5a | 1 |
| Kif5c | 1 |
| Map1b | 1 |
| Map6 | 0 |
| Mapre2 | 1 |
| Mapt | 1 |
| Mark3 | 0 |
| Nin | 0 |
| Ttll5 | 0 |
| Tuba1a | 7 |
| Tuba4a | 2 |
| Tubb4b | 1 |
| Tubb5 | 1 |

I then compared observed log-fold-change profiles from the declared parquet for a compact mechanistic panel in the exact focal population. The comparison artifact was `workbench/cytoskeleton_profile_compare.json`; the bounded inspection was `workbench/cytoskeleton_profile_inspect.json`.

The profile activity calls matched the count-table picture:

- `Dctn1`: `75` significant features, the only broad profile in the supplied cytoskeletal panel.
- `Hspa8`: `9` significant features.
- `Tuba1a`: `7` significant features.
- `Tuba4a`: `2` significant features.
- `Kif5a`, `Kif5c`, `Mapre2`, and `Mapt`: `1` significant feature each.

Thus the observed local magnitudes around CLIP2-like cytoskeletal biology concentrate at 0-2 DEGs, with `Dctn1` and its sterol-feedback state too central and too biologically different to transfer as a numeric donor.

## Point synthesis

The forecast balances three bearings:

- Upward from strict zero: `Clip2` has broad exact expression reach in `151`, and the edit-to-harvest interval should deplete a dynamic microtubule-associated CLIP2 pool.
- Downward from a moderate or broad response: this is not a transcription factor, core proteostasis gene, spliceosome, ubiquitin, mediator, or sterol-regulating node, and the same-experiment microtubule neighborhood is mostly transcriptionally buffered.
- Toward a singleton: `Mapre2` and `Mapt` are the closest postnatal microtubule/plus-end or MAP-like comparators in the count table and each has one focal DEG; the count table's 75th percentile is also exactly one.

I therefore predict a singleton significant feature, most likely either the self transcript or a small private downstream call, rather than a robust multi-gene response.

**Predicted `n_degs`: 1**
