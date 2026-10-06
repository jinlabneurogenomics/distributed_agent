# Direct Dlx5 `n_degs` forecast

## Target and endpoint

- Target: `Dlx5`, from the declared one-row holdout manifest.
- Focal population: `151 TH Prkcd Grin2c Glut`.
- Endpoint: the count of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`.
- Prediction: `0`.

## Evidence used

### Canonical Dlx5 biology bundle

Source: `[local file: Dlx5.json]`, also read through `characterization_bundle(target="Dlx5", view="biology")`.

- DLX5 is a soluble nuclear sequence-specific homeobox transcription activator. A disruptive edit should block new functional DLX5 production, and the functional-stock adjudication calls the protein `likely_substantially_depleted` by the P37-P44 harvest in edited cells that are actually producing DLX5.
- The timing evidence is indirect: no DLX5-specific protein half-life or acute P16 neuronal loss experiment was located.
- The available neural biology places adult Dlx5 expression mainly in GABAergic interneuron classes rather than broadly across neurons. Dlx6 is a paired paralog with overlapping interneuron-development functions, but Dlx5 single loss still has developmental interneuron phenotypes in another context, so redundancy is not a complete biological null.
- Exact non-target expression in the requested `151 TH Prkcd Grin2c Glut` class is extremely sparse:
  - `207 / 23679` nuclei expressed Dlx5: `0.8741923223%`.
  - mean raw UMI: `0.0109379619`.
  - mean log1p CP10k: `0.0042010609`.
  - pseudobulk CPM: `0.6855208601`.

I treated the stock card as saying Dlx5 knockout would be realized in the rare cells with active Dlx5, and the exact expression measurement as saying that only a very small slice of the assayed thalamic glutamatergic aggregate is poised for a direct Dlx5-dependent response.

### Training count table

Source: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.

The training endpoint in this cell class is sparse and zero-inflated:

- training targets: `1674`
- targets with `n_degs = 0`: `1205` (`71.9833%`)
- targets with `n_degs <= 1`: `1481` (`88.4707%`)
- targets with `n_degs <= 5`: `1546` (`92.3536%`)
- median `n_degs`: `0`
- mean `n_degs`: `14.05`, dominated by a long high-count tail.

The closest simple training analogs for the off-lineage/GABAergic interpretation of Dlx5 were all null in the same count table:

| target | `n_degs` in `151 TH Prkcd Grin2c Glut` |
| --- | ---: |
| `Dlx6` | 0 |
| `Arx` | 0 |
| `Dlx3` | 0 |
| `Gad2` | 0 |
| `Slc32a1` | 0 |
| `Slc6a1` | 0 |

### Direct Parquet checks

Source: `[local file: training_de_all_cell_groups.parquet]`.

I recomputed significance counts directly for the same focal population and the GABAergic/DLX-neighborhood controls above; each had zero `pvals_adj < 0.05` genes in `151 TH Prkcd Grin2c Glut`. The matched perturbed nucleus counts were not unusually absent for the key comparators:

| target | focal `n_pert_matched` | focal `n_degs` from Parquet |
| --- | ---: | ---: |
| `Arx` | 269 | 0 |
| `Dlx6` | 294 | 0 |
| `Gad2` | 178 | 0 |
| `Slc32a1` | 268 | 0 |
| `Slc6a1` | 220 | 0 |

Across all assayed cell groups in the declared Parquet, `Dlx6` had no significant genes at all; `Arx`, `Gad2`, `Slc32a1`, and `Slc6a1` each had only 4-6 significant gene x group results total and none in the focal population.

The smallest raw p-values for these analogs in the focal population still did not approach focal-population BH significance. The best example was `Arx` on `Zfp827`, with raw `p = 2.0063e-05` but adjusted `p = 0.3463`; other inspected top nominal rows had `pvals_adj = 1`.

### Run-local profile comparison

Artifact:

- `workbench/dlx5_low_reach_profile_compare.json`
- `workbench/dlx5_low_reach_profile_inspect.json`

The symmetric profile comparison over `Arx`, `Dlx3`, `Dlx6`, `Gad2`, `Slc32a1`, and `Slc6a1` in `151 TH Prkcd Grin2c Glut` wrote 15 pairwise comparisons and classified all six nodes as `no_significant_features`. The bounded inspection table returned `significant_feature_count = 0` for the closer five-node subset `Arx`, `Dlx6`, `Gad2`, `Slc32a1`, and `Slc6a1`.

## Synthesis

The strongest upward piece of evidence is molecular: DLX5 is a regulative nuclear transcription factor whose edited allele should stop new functional protein supply, and a 21-28 day interval is long enough that a free protein pool should usually decline. That makes a response plausible in cells that are using Dlx5.

The downward evidence is more endpoint-matched. The requested endpoint is an aggregate thalamic glutamatergic differential-expression count, and Dlx5 is almost absent in the exact non-target focal population: only 0.874% of cells have any detected target transcript. The Dlx5 bundle also places adult Dlx5 primarily in GABAergic neurons, while the requested class is glutamatergic. Training perturbations that either hit the paired Dlx gene (`Dlx6`), a GABAergic specification factor (`Arx`), or GABAergic markers/transporters (`Gad2`, `Slc32a1`, `Slc6a1`) were all silent in the same thalamic glutamatergic population, even with hundreds of matched perturbed nuclei for several of them.

Given that the median training target is already zero and the target-specific reach is lower than the plausible footprint needed to move thousands of aggregated recovered glutamatergic nuclei, I forecast that Dlx5 will behave as a focal-population null rather than produce even a small BH-significant tail.

Point prediction: `0`.
