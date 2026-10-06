# Direct forecast for Arsb

Target: `Arsb` in `151 TH Prkcd Grin2c Glut`.

## Declared outcome and inputs

- The requested endpoint is the count of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`.
- The held-out manifest contains a single target, `Arsb`.
- The focal population is the exact atlas class `151 TH Prkcd Grin2c Glut`, i.e. thalamic glutamatergic neurons.
- The training count table for this population has 1,674 measured training perturbations and is highly zero-inflated:
  - `n_degs = 0`: 1,205 / 1,674 targets = 72.0%.
  - median `n_degs`: 0.
  - 75th percentile: 1.
  - 90th percentile: 2.
  - 95th percentile: 18.
  - >=100 DEGs: 43 / 1,674 targets = 2.6%.

## Arsb biology used for the forecast

- The declared biology bundle maps the Perturb-seq target `Arsb` to mouse `Slurp1`/`ArsB`, a small secreted Ly6/uPAR-family extracellular protein.
- Exact expression reach in non-target `151 TH Prkcd Grin2c Glut` nuclei is present but weak: mean raw UMI 0.541, pseudobulk 33.93 cpm, and 9,021 / 23,679 nuclei expressing the feature.
- The bundle's functional-stock adjudication is indeterminate by the P37-P44 harvest: a P16 disruptive edit should stop new Slurp1 secretion from edited expressing cells, but pre-edit extracellular product is not directly neutralized and no target-specific half-life or clearance measurement was found.
- The same bundle gives no matched postmitotic thalamic neuronal loss phenotype. The best causal loss evidence is mouse but peripheral/systemic; the established null phenotypes are skin/metabolic with hind-limb clasping not localized to thalamic neurons; adult public thalamus datasets report no Slurp1 regional signal.
- The same-experiment corpus release contains no `Arsb` Findings, Claims, explicit report references, or related-target paths, so no packaged Perturb-seq report offered a direct `Arsb` comparator.

## Training perturbations used as local scale checks

I compared the target biology with training targets whose operations sit closer to extracellular signaling than to the large intracellular response tail. In the exact focal count table:

| training target | n_degs |
| --- | ---: |
| Gal | 0 |
| Reln | 0 |
| Cck | 1 |
| Fgf1 | 0 |
| Fgfr1 | 0 |
| Nrg1 | 0 |
| Nrg2 | 0 |
| Ret | 0 |
| Ngfr | 0 |
| Vldlr | 0 |
| Csf1r | 0 |
| Tgfbr1 | 0 |

A same-Parquet focused profile comparison for `Gal`, `Reln`, `Cck`, `Fgf1`, `Nrg1`, and `Ret`, restricted to `151 TH Prkcd Grin2c Glut`, found no FDR-significant genes for five of the six profiles; the sixth fell in the 1-9 significant-feature bin. That matched the count-table view that these extracellular or signaling perturbations are transcriptionally quiet in this class.

By contrast, the largest count-table outliers were intracellular RNA-processing, proteostasis, chromatin, and nuclear-transport regulators such as `Uba5` at 2,677 DEGs, `Tpr` at 1,768, `Sin3a` at 1,433, spliceosome/RNP factors, proteasome genes, `Yy1`, and `Ctcf`. `Arsb` has neither their cell-intrinsic machinery role nor their strong in-assay state rationale.

## Point synthesis

The focal class has a zero median even among measured training targets, and `Arsb` is a weakly detected secreted peripheral-product gene with uncertain local stock depletion and no thalamic neuron-specific causal prior. The exact-expression evidence prevents treating it as wholly absent, but the biology points away from a large acute survivor-conditioned nuclear RNA state. The most defensible integer point is therefore the modal/median training endpoint, with the forecast concentrated at the no-DEG state.

Predicted `n_degs`: **0**
