# Lrpap1 DEG-count forecast

Target and endpoint: `Lrpap1` in `151 TH Prkcd Grin2c Glut`; predict the number of measured genes with BH-adjusted Wilcoxon `p < 0.05`.

## Target biology

The declared one-row holdout manifest contains `Lrpap1`. In the canonical biology bundle for this same target, `Lrpap1` is measurably present in the focal cell class: 17,528 of 23,679 matched non-target nuclei express the feature, or 74.0%, with mean raw UMI 1.64 and pseudobulk 102.76 CPM. This makes the perturbation reachable in the thalamic class but does not quantify editing efficiency.

The functional-stock card calls the P16 to P37-P44 perturbation likely substantially depleted by harvest. The core reason is that LRPAP1/RAP acts as a continuing ER chaperone for newly synthesized LDL-receptor-family clients, so loss of new RAP synthesis should first spare pre-edit mature receptor and then progressively reduce renewed mature client stock over the 21-28 day window. That evidence is partial: the receptor-turnover timing uses heterologous LRP1 data, and the direct mouse-neural evidence is RAP-null hippocampal/developmental evidence rather than an induced postnatal thalamic time course.

The same biology bundle supports reach more than a large focal snRNA-seq response. RAP-null mouse neural evidence reported impaired LRP maturation/localization, but gross brain architecture and cultured hippocampal-neuron morphology/survival were normal; phenotype latency after acute postnatal loss is unreported; no close Lrpap1 paralog was found, but other ER quality-control routes could still buffer individual clients.

## Training measurements

The declared focal count table has 1,674 training perturbations. It is highly sparse in `151 TH Prkcd Grin2c Glut`: 1,205 targets have `n_degs = 0`, the median is 0, the 75th percentile is 1, the 90th percentile is 2, and only 43 targets reach at least 100 DEGs.

Direct receptor/client analogs in the same focal count table are nearly all null:

| group | training genes | focal `n_degs` |
| --- | --- | --- |
| LDL-receptor-family clients or sorters | `Lrp1`, `Lrp2`, `Lrp4`, `Lrp5`, `Lrp6`, `Lrp8`, `Vldlr`, `Sorl1`, `Sort1` | median 0; sum 4 across 9 genes; only `Lrp6` was nonzero, at 4 |
| APP/LRP axis | `App`, `Adam10`, `Apbb2`, `Appl1` | median 0; sum 1 across 4 genes |
| ER/secretory comparators in the visible training universe | `Hspa5`, `Atf6`, `Sec63` | 5, 0, and 11 |

The full declared Parquet reproduces that focal-class quietness over 17,259 measured features for the adjacent genes: `Lrp1`, `Lrp2`, `Lrp4`, `Lrp5`, `Lrp8`, `Vldlr`, `Sorl1`, and `Sort1` each have zero BH-significant genes in the focal class; `Lrp6` has 4 and `App` has only 1. Broader trafficking perturbations such as `Rab7`, `Vps35`, and `Vps54` can be detected in this class, but they perturb core endolysosomal machinery rather than the narrower RAP-dependent receptor-maturation step, so I used them only as a positive boundary on assay sensitivity.

## Synthesis

The Lrpap1 edit should be biologically realized by harvest, yet the endpoint most relevant to the requested count is the local training behavior of LRP-family receptors, APP-axis genes, and selective secretory/trafficking perturbations. Those measured perturbations land at zero or low single-digit DEG counts in the same thalamic class, while the Lrpap1 biology bundle lacks evidence for an acute postnatal thalamic stress, survival, or broad UPR program. Simultaneous partial loss of multiple client receptors leaves uncertainty above an exact null, but the strongest local analogs support a point forecast at the focal-class mode and receptor-family median.

Predicted `n_degs`: 0
