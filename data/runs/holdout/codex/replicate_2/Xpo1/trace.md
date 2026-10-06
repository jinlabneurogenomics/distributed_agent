# Xpo1 n_degs prediction for 151 TH Prkcd Grin2c Glut

## Declared target

- Holdout manifest target: `Xpo1`.
- Requested endpoint: count of measured genes in `151 TH Prkcd Grin2c Glut` with BH-adjusted Wilcoxon `p < 0.05`.
- Direct declared measurements used:
  - `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`, 1,674 training targets with endpoint counts.
  - `training_de_all_cell_groups.parquet`, filtered to `group_name == "151 TH Prkcd Grin2c Glut"` for training profile comparison only.
  - `biology_bundles/Xpo1.json` / `characterization_bundle(view="biology")` for the target biology card.

## Target biology

The Xpo1 bundle supports a reachable post-edit lesion in this assay. `Xpo1` RNA is directly detected in the focal non-target nuclei, with expression in 20,869 of 23,679 cells, 88.13% of the class, mean raw UMI 2.59, and mean log1p CP10k 0.871. The functional-stock card calls XPO1 a renewed soluble Ran-dependent nuclear export receptor rather than a permanent preinstalled structure. Its adult mouse thalamus protein T50 is 7.444 days, so the 21-28 day P16-to-P37/P44 interval is long enough to remove most pre-edit protein in cells with a disruptive edit.

That makes a broad response plausible. The operation is also cargo-specific rather than a structural failure of the whole nuclear pore: XPO1 exports leucine-rich-NES protein cargoes and RNA-containing cargo complexes, and the card notes only narrow cargo-specific buffering by XPO7 rather than global redundancy. The main downward uncertainties are survivor conditioning, incomplete sparse editing, juvenile thalamus versus the adult bulk turnover prior, and the possibility that only a subset of XPO1 cargoes drives a measured nuclear-RNA state over the screen window.

## Training measurements

The class-specific count table is mostly sparse:

- 1,674 training targets.
- Median `n_degs` = 0.
- 75th percentile = 1.
- 95th percentile = 18.
- 99th percentile = 430.
- 15 targets have at least 500 DEGs.

The closest manually selected training perturbations on nuclear transport / RNA-trafficking biology were:

| target | `n_degs` |
|---|---:|
| `Tpr` | 1768 |
| `Tnpo3` | 618 |
| `Xrn1` | 20 |
| `Vcp` | 2 |
| `Xpo7` | 0 |
| `Ranbp2` | 0 |
| `Kpna3` | 0 |

`Tpr` and `Tnpo3` are the informative upper-scale donors: both are assayed in the same cell class and both are among the high-count tail of the training distribution. `Tpr` is a nuclear-pore basket perturbation with a more structural route to broad RNA-processing/export disruption, so I treated its 1,768 DEGs as an upper scale reference rather than a direct equal-scale analog. `Tnpo3` is a transport receptor for splicing factors and is closer to an import/export receptor mechanism; its 618 DEGs make the lower end of the high-response band credible for a nuclear-transport receptor perturbation. `Xpo7` being exactly 0 DEGs was treated as a boundary that cargo-distinct export receptors can be buffered, not as strong evidence that Xpo1 itself should be null.

## Profile check

I generated a same-class profile comparison from the declared training Parquet for `Tpr`, `Tnpo3`, `Xpo7`, `Xrn1`, `Vcp`, `Ranbp2`, and `Kpna3` in `workbench/transport_profile_compare.json`. It reproduced the count-table burden for the selected nodes:

- `Tpr`: 1,768 significant features, 1,315 positive and 453 negative.
- `Tnpo3`: 618 significant features, 305 positive and 313 negative.
- `Xpo7`: 0 significant features.

The `Tpr`-`Tnpo3` whole-profile cosine was 0.574 and Pearson correlation was 0.514 across 17,259 shared measured features, with stronger shared negative-tail structure than positive-tail structure. A full training-universe neighbor projection for `Tpr` and `Tnpo3` found 177 bounded nearest-neighbor targets, but that union was mostly low-count: median 0 and mean 24.3 DEGs, with only a few broad RNA-processing/proteostasis targets such as `U2af2`, `Psmb4`, `Elp1`, `Ufc1`, and `Prpf6` in the high-count tail. I therefore used the all-universe profile result as a guard against overinterpreting generic whole-profile similarity, not as a reason to pull `Xpo1` up to the `Tpr` count.

## Synthesis

`Xpo1` should be far above the zero background because the focal cells express it broadly, the perturbation window should deplete the renewable XPO1 stock, and two direct training genes in adjacent nuclear transport / RNA-processing biology show broad responses in exactly this thalamic class. I placed it below `Tpr` because XPO1 is a soluble cargo receptor rather than an NPC scaffold and because `Xpo7` demonstrates that exporter loss can be silent when cargo coverage or buffering differs. I placed it above `Tnpo3` because XPO1 handles a broad set of protein and RNA-containing export cargoes, has high measured focal reach, and has limited evidence for blanket redundancy.

The resulting direct point forecast is:

```tsv
target_name	predicted_n_degs
Xpo1	900
```
