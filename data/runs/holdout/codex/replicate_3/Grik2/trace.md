# Grik2 forecast for `151 TH Prkcd Grin2c Glut`

## Declared target and focal reach

- The one-row holdout manifest names `Grik2`.
- `Grik2` is absent from the declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`, so its held-out focal `n_degs` was not present in the count table.
- The biology bundle reports exact focal-population expression for `Grik2` in the non-target `151 TH Prkcd Grin2c Glut` cells: 23,374 / 23,679 nuclei expressing, 98.7119% expressing, mean raw UMI 7.1343, mean log1p CP10K 1.6235, and pseudobulk CPM 447.1316. That makes this a well-expressed target in the assayed thalamic class, while still not revealing editing efficiency or any held-out differential-expression result.
- The functional-stock card classifies GluK2 as a dynamic kainate-receptor complex component whose pre-edit protein should be substantially reduced over the 21-28 day P16-to-P37/P44 window, but the strongest loss phenotypes are germline hippocampal or adult behavioral observations rather than a matched acute thalamic lesion.

## Training comparators

The curated mouse annotation/analog nomination for `Grik2` placed the held-in kainate subunits first:

| comparator | nomination relation | focal n_degs |
|---|---:|---:|
| Grik3 | exact complex/paralog | 0 |
| Grik1 | exact complex/paralog | 0 |
| Grik5 | exact complex/paralog | 1 |
| Grik4 | narrow kainate module | 0 |

Broader ionotropic-glutamate and postsynaptic comparators in the same focal count table were also mostly silent:

| comparator group | focal training n_degs |
|---|---|
| AMPA receptor subunits `Gria1`, `Gria2`, `Gria3` | 0, 0, 0 |
| non-obligate NMDA subunits `Grin2a`, `Grin2b`, `Grin2d`, `Grin3a` | 1, 2, 0, 0 |
| related postsynaptic/scaffold genes `Dlg4`, `Grid1`, `Grid2`, `Shank2`, `Shank3` | 1, 1, 0, 0, 2 |
| obligate NMDA receptor subunit `Grin1` | 89 |

The exact Parquet rows showed that the isolated one-DEG hits for `Grik5`, `Grin2a`, `Dlg4`, and `Grid1` were each the perturbed transcript itself; `Grin2b` had its self transcript plus one downstream gene; `Grin1` was the lone receptor comparator with a broad 89-gene downstream program. Thus, held-in kainate/AMPA/non-obligate NMDA receptor subunits rarely produced more than their own transcript as an FDR-significant feature in this class.

## Profile and corpus checks

The packaged Finding topology over the 12 leading held-in receptor nominees was connected in the explicit-reference lane, so the cohort is report-represented and biologically coherent, but the topology was used only as provenance/context because it is the same experiment and is not an endpoint scale.

The direct profile comparison over those 12 nominees in `151 TH Prkcd Grin2c Glut` found seven nodes with no significant features, four with 1-9, and only `Grin1` with at least 50. Across the 66 pairwise receptor comparisons, the cohort projection had weak positive-tail sharing and no shared FDR-significant signed program, which argued against treating the whole receptor set as one large transferable response.

## Synthesis

The forecast should be above a hard zero because `Grik2` is strongly expressed in nearly every focal non-target nucleus and its receptor stock is plausibly depleted by harvest. The forecast should stay at the floor because the closest held-in kainate subunits had counts of 0, 0, 0, and 1, broader AMPA and kainate/NMDA subunit perturbations usually produced no downstream program, and the strong `Grin1` response is a poor scale donor because it removes the obligatory NMDA receptor subunit rather than one kainate-family subunit.

I therefore predict a single FDR-significant measured gene.
