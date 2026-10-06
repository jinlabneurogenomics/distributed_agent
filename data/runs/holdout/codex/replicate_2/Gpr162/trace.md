# Gpr162 direct DEG-count forecast

## Inputs used

- Task target and focal class: `Gpr162` in `151 TH Prkcd Grin2c Glut`.
- Biology bundle: `[local file: Gpr162.json]`, SHA-256 `adb1c7127f53d814ada9e741c0d004ccd4c27786f2e9d34dfd6bdd0017e0fa9d`.
- Training count table: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Training DE parquet: `[local file: training_de_all_cell_groups.parquet]`.

## Evidence

The focal training endpoint is highly zero-inflated. Among 1,674 visible training perturbations in `151 TH Prkcd Grin2c Glut`, 1,205 had `n_degs = 0`; the median was 0, the 75th percentile was 1, the 90th percentile was 2, and only 43 perturbations had at least 100 significant genes.

GPR-family and nearby receptor-signaling training perturbations were quiet in the focal class:

| set | focal observations |
| --- | --- |
| `Gpr*` targets | `Gpr156 = 0`, `Gpr158 = 1`, `Gpr161 = 0`, `Gpr179 = 0`, `Gpr45 = 0`, `Gprasp2 = 1`, `Gprc5b = 0` |
| neuropeptide / class-A GPCRs queried | `Npy1r`, `Npy2r`, `Npy5r`, `Ntsr1`, `Oprd1`, `Oprk1`, `Oprl1`, `Oprm1`, `Sstr5`, and `Tacr3` were all 0; `Cnr1` was 1 |
| immediate G-protein/RGS entries present | `Gnao1 = 1`, while `Gnal`, `Gnas`, `Gnb5`, and `Rgs6` were 0 |

The DE parquet showed that the `Gpr*` singleton calls were not broad downstream receptor-state signatures. In `151 TH Prkcd Grin2c Glut`, the only FDR-significant rows for `Gpr158` and `Gprasp2` were their own target transcripts. Across all measured classes in the training parquet, the seven visible `Gpr*` perturbations never produced more than one significant gene in a class.

The endpoint-blind GPR162 bundle makes target reach the strongest positive factor: in the exact non-target focal population, Gpr162 was detected in 23,598 of 23,679 cells, 99.6579%, with mean raw UMI 10.04, mean log1p CP10K 1.94, and pseudobulk CPM 629.47. Thus the target transcript is well measured in this class, unlike many receptor genes whose null calls could simply reflect little baseline expression.

The biological prior does not support a large downstream thalamic program. GPR162 is a seven-transmembrane receptor with CART/GNA13-dependent signaling demonstrated outside brain; by the 21-28 day harvest the editable receptor stock is judged likely to be substantially depleted, but the evidence is sparse. The closest perturbational neural evidence is an adult rat intracerebroventricular antisense feeding phenotype after seven days, not a mouse thalamic genetic-loss response. The curated card also leaves GPR153-related redundancy unresolved.

## Forecast

I forecast no multi-gene response and allow one measured DEG for a likely target-transcript call. The high exact Gpr162 expression makes a self row plausible, while the matched training receptor stratum argues strongly against a tens-to-hundreds DEG footprint.

Point prediction: `1`.
