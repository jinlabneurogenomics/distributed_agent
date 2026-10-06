# Pi4ka n_degs prediction trace

## Target and endpoint

- The one-row holdout manifest names `Pi4ka`.
- The endpoint is `n_degs` in `151 TH Prkcd Grin2c Glut`: the number of measured genes whose matched Wilcoxon result has `pvals_adj < 0.05`.
- The numeric training table and all-cell-class expression Parquet were treated as the experimental measurements. The Pi4ka biology bundle was used as prior biology and target reach, not as an observed Pi4ka endpoint.

## Evidence that set the scale

- The declared count table for `151 TH Prkcd Grin2c Glut` is highly zero-inflated: 1,205 of 1,674 training targets have `n_degs = 0`, the median is 0, the 75th percentile is 1, the 90th percentile is 2, and only 42 targets exceed 100 DEGs.
- `Pi4ka` is readily expressed in the focal non-target population in the biology bundle: 22,732 of 23,679 nuclei express the feature, `mean_raw_umi = 4.61`, `mean_log1p_cp10k = 1.26`, and `pct_cells_expressing = 96.0`. Its transcript should therefore be observable in this cell class, while its focal perturbation contrast remains withheld.
- The same bundle adjudicates the functional stock as likely substantially depleted by the 21-28 day harvest in successfully edited cells: PI4KA supplies plasma-membrane PI4P, the PI4P product turns over within minutes after acute catalytic blockade, and adult conditional mouse loss can reduce PI4KA protein and produce tissue pathology within days. The main uncertainty is that no thalamic postmitotic-neuron edit-to-stock timing study was available.
- The closest represented phosphoinositide and adjacent training perturbations in this class were mostly silent:
  - `Pi4kb`, the only represented PI 4-kinase isoenzyme, had `n_degs = 1`; the Parquet slice showed only `Tmem50b` at FDR 0.05 and `Rnf145` at FDR 0.10.
  - `Pik3cb`, `Pik3r1`, `Pik3r2`, `Ocrl`, `Inpp5k`, `Ppip5k2`, `Pitpnm3`, `Itpr1`, `Plcb1`, `Prkca`, `Sphk1`, `Stard7`, `Cert1`, `Ddhd1`, and `Ddhd2` were all `n_degs = 0`.
  - `Synj1`, `Pld3`, `Prkcg`, `Sptlc2`, `Ywhag`, and `Ywhaz` were all one-gene responses; in the Parquet those one-gene calls were their self-target transcripts, not a resolved downstream program.
  - `Pitpna` was the strongest broad phosphoinositide-related comparator at 21 DEGs, and vesicular-trafficking targets `Vps35` and `Vps54` reached 17 and 31 DEGs, showing that modest membrane-trafficking states can be recovered in the assay but that they are not the typical scale for PI-lipid enzymes.
- The same-experiment corpus for `Pi4kb` independently summarized that represented phosphoinositide and PI4KB-adjacent targets did not converge on the tiny `Pi4kb` signature; this supported treating adjacent lipid-signaling targets as sparse boundary references rather than as a coherent high-burden module.

## Synthesis

`Pi4ka` is a real and well-expressed focal-population target, and its enzymatic product should turn over during the P16-to-P37/P44 window if edited cells survive. That argued against an inaccessible-target zero based only on expression. The quantitative training measurements, however, put direct and nearby lipid-signaling operations at zero or one DEG in `151 TH Prkcd Grin2c Glut`, with `Pitpna` as a limited exception and no recurrent stress or PI-response transcriptome shared by `Pi4kb`.

The point estimate is therefore above a hard null but still at the sparse singleton scale:

`predicted_n_degs = 1`
