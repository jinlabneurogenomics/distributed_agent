# Direct DEG-count forecast for `Sry`

## Requested target

- Target manifest: one held-out perturbation, `Sry`.
- Focal population: `151 TH Prkcd Grin2c Glut`.
- Endpoint: `n_degs`, the number of measured genes with Wilcoxon BH-adjusted `p < 0.05`.

## Evidence used

- The biology bundle for `Sry`
  `[local file: Sry.json]`,
  SHA-256 `7e364f7874876ee3c9865ee129bccd3fa97e4c71a1e39f569be3440007b6ec1f`,
  is outcome-blind and exposes no target DEG count or labeled neighbor outcomes.
- Exact focal-population reach from the `Sry` bundle:
  - expression gene: `Sry`
  - group: `151 TH Prkcd Grin2c Glut`
  - non-target nuclei: 23,679
  - `n_cells_expressing`: 0
  - `pct_cells_expressing`: 0.0
  - `mean_raw_umi`: 0.0
  - `mean_cp10k`: 0.0
  - `mean_log1p_cp10k`: 0.0
- Functional-stock adjudication in the same bundle says that an effective edit should substantially deplete active SRY by harvest wherever `Sry` is being expressed: SRY is a short-lived nuclear transcription factor, and a postnatal rodent neural knockdown showed an effect within ten days. This supports realizability in principle, but does not override the exact zero focal thalamic expression.
- The selected same-experiment corpus release had no `Sry` Findings, Claims, or explicit reference edges, so it did not provide a same-corpus `Sry` analogue.
- The declared count table
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
  contains 1,674 training perturbations; 1,205 have `n_degs = 0` in the focal population. Its median is 0, 75th percentile is 1, 90th percentile is 2, and 95th percentile is 18.
- Sex/SRY-adjacent or SOX-family perturbations present in the training table are quiet in the same focal endpoint: `Ar = 0`, `Sox9 = 0`, `Sox4 = 0`, `Sox10 = 0`, `Sox11 = 0`, `Sox17 = 0`, `Sox18 = 0`, `Sox2 = 2`, and `Sox5 = 2`.
- A slice of the declared expression Parquet
  `[local file: training_de_all_cell_groups.parquet]`
  for `151 TH Prkcd Grin2c Glut` confirmed that `Ar`, `Sox4`, `Sox9`, `Sox10`, `Sox11`, `Sox17`, and `Sox18` had no BH-significant rows; the only BH-significant rows among `Sox2` and `Sox5` were:
  - `Sox2`: `Tnnt1` and `Stam`
  - `Sox5`: `Dgkh` and `Tnnt1`
- Whole-profile Parquet neighborhoods for `Ar`, `Sox2`, `Sox5`, and `Sox9` against all 1,674 eligible training profiles were also concentrated in the zero/tiny-count regime. The lossless neighborhood artifact is
  `codex_runtime/pipeline/sry_biological_peer_neighbors.json`. The five nearest whole-profile neighbors were all zero for `Ar`, were `0, 0, 1, 0, 0` for `Sox2`, were `0, 0, 0, 4, 0` for `Sox5`, and were `0, 1, 6, 2, 0` for `Sox9`.

## Reasoning

The exact target-reach measurement is the dominant factor. `Sry` is a transcription factor whose loss can matter in postnatal neural cells that actually express it, but the focal population had zero detected `Sry` molecules across the non-target nuclei used to define reach. With no measurable basal `Sry` in this thalamic glutamatergic population, an acute P16 edit has little reason to perturb a local transcriptional program by P37-P44.

The quantitative training evidence points the same way. This focal class has a heavily zero-inflated endpoint distribution, and the biologically closest available training perturbations are themselves silent or nearly silent. The raw Parquet rows showed no hidden broad response for the selected androgen/SOX peers, and their nearest signed profiles were drawn mostly from other zero-count perturbations.

I therefore forecast the mode and biology-supported lower tail rather than a generic nonzero training mean.

## Point prediction

`Sry` in `151 TH Prkcd Grin2c Glut`: **0** DEGs.
