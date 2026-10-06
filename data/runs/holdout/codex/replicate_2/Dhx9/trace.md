# Dhx9 DEG-count forecast

## Endpoint

- **Target:** `Dhx9`
- **Cell group:** `151 TH Prkcd Grin2c Glut`
- **Endpoint:** `n_degs`, the number of measured genes with Wilcoxon `pvals_adj < 0.05`
- **Visible outcome table:** `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`, 1,674 training targets

## Dhx9 biology used

The declared biology bundle makes a nonzero transcriptional response plausible but not guaranteed:

- Dhx9 is broadly reachable in the exact focal population: `20305 / 23679` non-target 151-class nuclei expressed the transcript, with `pct_cells_expressing = 85.751`, `mean_raw_umi = 2.454`, and `mean_log1p_cp10k = 0.822`.
- Dhx9 encodes a renewable ATP-dependent nuclear DNA/RNA helicase. The functional-stock card calls pre-edit protein carryover unlikely to last through the 21-28 day P16-to-P37/P44 experimental interval, with `functional_stock_by_harvest = likely_substantially_depleted`.
- Mouse neural evidence is developmental rather than an exact P16 thalamic loss-of-function timing match. Dhx9 family membership named related helicases, especially Dhx30 and Ddx3x, but the bundle found no direct postmitotic thalamic compensation test. I therefore treated paralogy as uncertainty, not as proof of buffering.

## Training measurements that anchored the scale

The focal count table is extremely sparse: among the 1,674 visible training perturbations, the median is `0`, the 90th percentile is `2`, the 95th percentile is `18`, the 97.5th percentile is `103`, and the 99th percentile is `454`.

I used the exact 151-class counts for observed perturbations closest to Dhx9's operation:

| target | n_degs | interpretation |
| --- | ---: | --- |
| `Ddx3x` | 8 | related DDX/DHX helicase, weak observed response |
| `Ddx39b` | 0 | RNA helicase/spliceosome and export-associated, quiet |
| `Setx` | 0 | RNA/DNA helicase and R-loop axis, quiet |
| `Xrn1` | 20 | RNA turnover boundary, low |
| `Hnrnpa2b1` | 11 | RNP boundary, low |
| `Hnrnph2` | 4 | RNP boundary, low |
| `Hnrnpc` | 122 | RNP perturbation, moderate |
| `Matr3` | 149 | nuclear RNP perturbation, moderate |
| `Tardbp` | 210 | RBP/RNP perturbation, moderate-high |
| `Snrnp70` | 213 | spliceosomal RNP perturbation, moderate-high |
| `Prpf6` | 454 | spliceosome component, high |
| `Cdc40` | 624 | splicing factor, high |
| `Hnrnpu` | 733 | nuclear RNP scaffold, high |
| `U2af2` | 828 | core splicing factor, high |
| `Rnpc3` | 868 | minor spliceosome component, high |

I then compared those 15 observed targets in the 151 rows of `training_de_all_cell_groups.parquet`. Every supplied profile was present. The Parquet-derived profile tables reproduced the low direct-helicase counts (`Ddx3x = 8`, `Ddx39b = 0`, `Setx = 0`, `Xrn1 = 20`) and the high spliceosome/RNP counts, but the profile cohort was not a tight same-scale Dhx9 module: Ddx3x's nearest whole-profile peers within the cohort spanned from `0` to `733` DEGs, and the 105-pair cohort had weak top-tail overlap on average, especially for the positive tail.

Across the same cohort and all neuronal classes in the declared Parquet, the two dominant contexts were the known high-yield populations: `151 TH Prkcd Grin2c Glut` had `4244` significant rows and `155 MB Glut` had `3707`, followed by `967` in the next class. I therefore took the 151 count table itself as the proper endpoint scale rather than borrowing a lower-yield class.

## Synthesis

Dhx9 has enough 151-class reach and expected within-window target loss that I did not project it to the screen-wide median of zero. At the same time, the exact DDX/DHX and R-loop neighbors in training were mostly 0-20 DEG perturbations, so the 400-900 DEG spliceosome hits looked like upper boundaries from more obligate or structural RNA-processing lesions rather than equal-scale analogs.

I placed Dhx9 in the upper tail of the sparse training distribution but below the first clear RNP/spliceosome response plateau: above the `20`-DEG low-helicase boundary, below the `122-213` moderate RNP band, and below the 97.5th percentile of the whole training table. The resulting point forecast is:

`predicted_n_degs = 64`
