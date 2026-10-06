# Tacr1 n_degs direct prediction

## Endpoint and target

- Requested endpoint: `n_degs`, the number of measured genes in `151 TH Prkcd Grin2c Glut` with BH-adjusted Wilcoxon `p < 0.05`.
- Held-out target from the declared manifest and biology bundle: `Tacr1`.
- The prediction uses the declared Tacr1 biology bundle, the exact Tacr1 expression reach for the focal population, the focal-group training DEG count table, and focal-group rows from the declared training Parquet. I treated the Parquet and the count table as two views of the same experiment.

## Evidence used

- Functional plausibility is present but context-limited. The bundle identifies `Tacr1` as the NK1 substance-P GPCR. Its operative receptor pool is dynamic, adult neuronal CRISPR against `Tacr1` can remove substance-P-evoked firing in another postmitotic neuronal population, and the stock adjudication calls signaling-competent receptor loss by the P37-P44 harvest likely in successfully edited expressing cells.
- The exact in-assay focal reach is very small. In matched non-target `151 TH Prkcd Grin2c Glut` nuclei, `Tacr1` has mean raw UMI 0.033, pseudobulk 2.07 CPM, and is detected in 628 of 23,679 nuclei, or 2.65%.
- Focal training contrasts are sampled with far fewer perturbed than control nuclei. Reading one row per target from the declared Parquet gave 1,674 training targets with constant `n_ctrl_matched = 23679`; their `n_pert_matched` median was 177, with IQR 140-211. At the observed 2.65% expression reach, a median Tacr1-guide contrast would contain only about 4.7 Tacr1-expressing assayed nuclei before considering mosaic editing or survivor conditioning.
- The direct focal count table is zero-heavy: 1,205 of 1,674 training targets had `n_degs = 0`; the median was 0, the 75th percentile was 1, and the 90th percentile was 2, with a small essential/splicing/proteostasis tail producing most large counts.
- Receptor perturbations visible in the same focal count table mostly behaved like null aggregate perturbations. In an a priori set of 35 neuromodulatory, peptide-family, sensory, or metabotropic receptor/channel genes available in training - adrenergic, angiotensin, vasopressin, muscarinic, dopamine, metabotropic glutamate, serotonin, `Tacr3`, TRP, and `Tshr` targets - 33 had zero focal DEGs. Only `Grm1` and `Grm7` had one DEG each, and the related tachykinin receptor `Tacr3` had zero.

## Prediction

The biology says a successful edit should remove new NK1 receptor supply, so I did not treat `Tacr1` as an impossible perturbation. The limiting evidence is reach: this target is detected in only a few percent of focal nuclei, and the assayed perturbed pool is small enough that the signal would be concentrated in only a handful of receptor-positive cells. The receptor-comparator subset in the training table also stays at zero or one DEG in this exact group.

I therefore forecast that the held-out aggregate Tacr1 signature lands on the modal no-DEG outcome:

`predicted_n_degs = 0`
