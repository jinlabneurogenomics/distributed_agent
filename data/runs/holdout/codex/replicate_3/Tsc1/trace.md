# Direct Tsc1 n_degs forecast

## Target and endpoint

- Target: `Tsc1`, the only row of the declared holdout manifest `Tsc1.csv`.
- Endpoint: number of `151 TH Prkcd Grin2c Glut` measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`.
- Direct endpoint sources used:
  - `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`, which contains 1,674 observed training targets and excludes `Tsc1`.
  - `training_de_all_cell_groups.parquet`, filtered only to training targets and the focal `151 TH Prkcd Grin2c Glut` population for signed Wilcoxon profiles.
- Target-prior source used: `biology_bundles/Tsc1.json`.

No `Tsc1` differential-expression profile or `Tsc1` DEG count was used.

## Biology prior

The declared `Tsc1` bundle supports that the perturbation should be active by harvest rather than latent:

- `Tsc1` encodes a structural/regulatory component of the TSC1-TSC2-TBC1D7 complex that restrains Rheb/mTORC1.
- The functional-stock adjudication calls operative TSC1 `likely_substantially_depleted` by the P37-P44 harvest because adult neuronal TSC1 protein and mTORC1 restraint decline within days and postnatal sparse neuronal deletion changes function within 10-14 days.
- Exact focal-population expression is available and broad enough for reach: `Tsc1` is detected in 16,583 of 23,679 non-target nuclei in `151 TH Prkcd Grin2c Glut` with 70.03% expressing cells and pseudobulk CPM 82.99.

This makes a zero-DEG forecast biologically unattractive, but the prior does not by itself fix endpoint scale because the readout is survivor-conditioned and depends on guide editing, focal thalamic coupling, and recovered edited nuclei.

## Training measurements

The count-table distribution is very sparse:

- median `n_degs`: 0
- mean `n_degs`: 14.05
- zero-DEG fraction: 1,205 / 1,674 = 71.98%
- only 106 / 1,674 targets have at least 10 DEGs, 43 have at least 100 DEGs, and 3 have at least 1,000 DEGs

The direct complex partner is visible and already in the upper tail:

| training target | focal n_degs | positive DEGs | negative DEGs | interpretation |
| --- | ---: | ---: | ---: | --- |
| `Tsc2` | 86 | 58 | 28 | TSC-complex partner; best local quantitative anchor |
| `Depdc5` | 13 | 10 | 3 | profile-proximal weaker mTORC1-pathway response |
| `Mtor` | 2 | 1 | 1 | opposite/downstream mTOR kinase loss; weak in this endpoint |
| `Rptor` | 0 | 0 | 0 | mTORC1 component, but quiet here |
| `Pik3r1` | 0 | 0 | 0 | PI3K pathway input, quiet here |
| `Akt3` | 0 | 0 | 0 | AKT paralog, quiet here |

The `Tsc2` thalamic signature is a recurrent state rather than a count-table singleton. A profile-neighbor projection using signed Wilcoxon `scores` over all 1,674 training targets placed `Rab7` and `Depdc5` as the two nearest whole-profile neighbors of `Tsc2`, and `Depdc5` shared 8 of its 13 focal significant genes with `Tsc2` (`Amy1`, `Ldlr`, `Msmo1`, `Pik3r1`, `Pik3r3`, `Rnpc3`, `Snhg11`, `Tubb3`). Across all assayed classes, the `Tsc2` perturbation had 202 DEGs in `155 MB Glut`, 86 in the focal thalamic class, 53 in `066 CNU-HYa HY GABA`, 38 in `191 MB P MY GABA`, and 37 in `308 CB GABA`, so its effect is not an isolated single-population numerical accident.

## Synthesis

I weighted `Tsc2` most because it is the only measured direct TSC-complex loss anchor. `Tsc1` should stop renewal of the same inhibitory complex and the bundle argues that this occurs inside the assay window in expressing postmitotic neurons. I did not average upward toward `Rab7` or the high-count splicing/proteasome neighbors, because those are shared stress/lysosomal transcriptional states rather than TSC-complex loss operations and their counts range into broad, nonspecific footprints. I did shrink modestly below `Tsc2` because the only other observed mTORC1-activating anchor, `Depdc5`, is much smaller, and because target expression/functional-stock reach does not guarantee identical guide editing or equal recovered-cell state size.

On that basis, my point forecast is slightly below the `Tsc2` direct-anchor count:

`predicted_n_degs = 75`
