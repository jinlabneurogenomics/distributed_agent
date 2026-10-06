# Zbtb24 direct `n_degs` forecast

Endpoint: number of measured genes in `151 TH Prkcd Grin2c Glut` with BH-adjusted Wilcoxon `pvals_adj < 0.05`.

## Evidence used

- Target: the one-row holdout manifest names `Zbtb24`.
- Focal expression/reach from the declared biology bundle:
  - `Zbtb24` is available as a measured feature in `151 TH Prkcd Grin2c Glut`.
  - Non-target focal cells expressing `Zbtb24`: 13,491 / 23,679 = 56.97%.
  - Mean focal expression: 0.911 raw UMI and 0.580 CP10K.
  - This makes lack of local expression a poor explanation for a null forecast, but it does not measure editing efficiency.
- Biology bundle:
  - ZBTB24 is a sequence-specific transcription factor that directly activates `Cdca7` in mouse ESCs and participates in the CDCA7-HELLS chromatin/DNA-methylation axis.
  - The best stock adjudication is `partially_depleted_or_leading_edge`: the edit should stop new ZBTB24 production by P37-P44, while pre-existing protein and downstream methylated/chromatin states can persist.
  - Available severe phenotypes are early embryonic or hematopoietic rather than postnatal thalamic neuronal; no postnatal neural loss phenotype or tested neuronal compensator was identified.
- Same-class training count table:
  - 1,674 training perturbations are present and `Zbtb24` is absent.
  - 1,205 / 1,674 training perturbations have `n_degs = 0` in this class.
  - Median = 0, 75th percentile = 1, 90th percentile = 2, 95th percentile = 18.
  - The table has a long positive tail, but only 106 / 1,674 reach at least 10 DEGs and only 43 / 1,674 reach at least 100.
- Curated analog nomination against the actual 1,674-gene training universe:
  - No exact-complex/paralog, bidirectional same-corpus comparator, narrow-module, or direct-interaction/dependency training analog was found for `Zbtb24`.
  - All 826 nominees were `broad_functional_fallback` genes, mostly through large transcription-factor or nuclear annotations.
  - The top 10 broad fallbacks by typed biological/community priority were all `n_degs = 0`; the top 20 had median 0 and 16 / 20 zeros; the top 100 had median 0 and 74 / 100 zeros.
- Declared Parquet check in `151 TH Prkcd Grin2c Glut`:
  - For the top broad fallbacks plus available `Zbtb*` genes, the direct Parquet counts exactly matched the training count table.
  - Large responses in this loose set were isolated: `Sin3a` = 1,433, `Zbtb7a` = 841, `Ctnnb1` = 383, `Ctcf` = 270.
  - Available `Zbtb*` rows were mostly quiet: `Zbtb10` = 0, `Zbtb16` = 0, `Zbtb20` = 0, `Zbtb21` = 0, `Zbtb38` = 1, `Zbtb18` = 5; `Zbtb7a` = 841 was the single outlier.
- Same-experiment corpus context for that outlier:
  - `Zbtb7a` loss has a broad, graded neuronal response with endomembrane/lysosome, synaptic, peptidergic, and UFMylation/proteostasis-neighbor structure.
  - Its high signature was not reproduced by several canonical partners or nearby chromatin regulators, so it was treated as an upper response boundary rather than a magnitude donor for `Zbtb24`.

## Synthesis

`Zbtb24` is expressed in the focal thalamic population and the disruptive edit is biologically plausible, so the forecast should not be zero solely because the target is absent or because the locus cannot be reached. The magnitude evidence, however, points strongly downward. The 21-28 day window may catch only leading-edge loss of the operative chromatin program; methylated DNA/chromatin installed before P16 can buffer the immediate transcriptional consequence in postmitotic neurons; and the declared card provides no neural phenotype tying ZBTB24 loss to an acute thalamic RNA state.

There was no exact measured donor for the CDCA7/HELLS axis: `Cdca7`, `Hells`, and `Dnmt3b` were absent from the focal training count table. The available biological analogs are broad transcription-factor or nuclear-function fallbacks rather than close pathway matches, and their same-class outcome distribution remained zero-centered even after biological prioritization. I therefore did not transfer the rare high-tail responses from `Sin3a`, `Zbtb7a`, `Ctcf`, or `Ctnnb1`; those show that the assay can detect some postnatal chromatin/TF perturbations, not that `Zbtb24` should land in that tail.

Point forecast: the modal quiet response, `0` DEGs.
