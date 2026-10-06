# Direct forecast for `Relb` in `151 TH Prkcd Grin2c Glut`

## Endpoint

The requested endpoint is `n_degs`, the count of measured genes in the focal thalamic glutamatergic population with BH-adjusted Wilcoxon `pvals_adj < 0.05`.

The one-row holdout manifest names `Relb`.

## Evidence used

- Canonical `Relb` biology bundle, `view=biology` only:
  - `Relb` encodes a DNA-binding noncanonical NF-kappaB transcription-factor subunit whose main active operation is partner-containing RelB-p52 rather than a standalone enzyme.
  - The exact in-assay reach in `151 TH Prkcd Grin2c Glut` is very small: 460/23,679 non-target nuclei expressed `Relb`, `pct_cells_expressing = 1.94`, `mean_raw_umi = 0.0209`, and `mean_cp10k = 0.0130`.
  - The functional-stock card calls harvest-time loss `partially_depleted_or_leading_edge`: a P16 edit stops new RelB supply, but it does not directly destroy pre-existing RelB-p100, RelB-p52, or RelB-p50 pools, and partner binding stabilizes some of that material through an unknown neuronal lifetime.
  - The strongest postnatal-CNS phenotype evidence is not a healthy thalamic-neuron readout; it comes from broader CNS-lineage or mature-oligodendrocyte loss in an inflammatory EAE context.

- Declared training count table:
  - The table has 1,674 training targets; 1,205 have `n_degs = 0`, 1,481 have `n_degs <= 1`, and the median count is `0`. Large DEG burdens are rare and heavy-tailed.
  - The available training perturbations closest to the RelB/NF-kappaB axis were all null in this exact endpoint:

    | training target | `n_degs` |
    |---|---:|
    | `Chuk` | 0 |
    | `Nfkb1` | 0 |
    | `Rel` | 0 |
    | `Tnfrsf1a` | 0 |
    | `Traf3` | 0 |

- Declared Parquet, matched to `group_name == "151 TH Prkcd Grin2c Glut"`:
  - A symmetric profile comparison over `Chuk`, `Nfkb1`, `Rel`, `Tnfrsf1a`, and `Traf3` found an available profile for every node and `significant_feature_count = 0` for all five at `pvals_adj < 0.05`.
  - Each profile covered 17,259 measured features in the focal group. Pairwise correlations among the five were weak/moderate whole-profile similarities, with Pearson values about `0.64-0.69` and no positive or negative significant-program overlap because no member had significant features.

- Same-experiment corpus checks, used as interpretation of the same screen rather than replication:
  - July Finding/null records for `Chuk`, `Nfkb1`, `Rel`, `Tnfrsf1a`, and `Traf3` summarize the corresponding pan-neuronal or all-recovered-group NF-kappaB/TNF null surfaces at FDR < 0.10.
  - Those records support that the local zeros are part of a broader unchallenged neuronal NF-kappaB quiet state, not a single anomalous thalamic row.

## Synthesis

`Relb` has a real transcription-factor mechanism, so I did not treat it as a safe-target-like control. The factors that set the point estimate were all downward for this aggregate DEG endpoint:

- Exact expression in the focal aggregate is restricted to about two percent of non-target nuclei, so a cell-autonomous RelB program would be strongly diluted unless it were large in a sizable hidden subpopulation.
- Functional loss by P37-P44 should have started, but the biology card supports partial rather than near-complete depletion because stabilized partner-bound RelB pools are not directly destroyed by editing.
- The observed Rel/NF-kappaB/TNF-side training perturbations available in the count table and Parquet were uniformly at `0` DEGs in this endpoint and were also interpreted as flat across the recovered neuronal atlas.

The main countercase is that the unmeasured preferred partner `Nfkb2` could make `Relb` less like `Nfkb1`, `Rel`, `Chuk`, `Traf3`, or `Tnfrsf1a`, and a tiny Relb-positive thalamic subtype could have a small response hidden inside the class aggregate. That uncertainty raises the possibility of `1` or a few DEGs, but it did not outweigh the exact low reach, partial stock depletion, and complete local null among the measured NF-kappaB comparators.

I therefore predict the integer DEG burden at the floor:

`predicted_n_degs(Relb) = 0`
