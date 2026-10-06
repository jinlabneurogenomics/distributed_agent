# Direct Zbtb24 n_degs forecast

## Target and endpoint

- Target manifest: `Zbtb24`
- Cell group: `151 TH Prkcd Grin2c Glut`
- Endpoint: count of measured genes in this focal group with BH-adjusted Wilcoxon `p < 0.05`.
- Declared target-expression signature and target count were absent from the training count table and parquet; I used the biology-only `Zbtb24` bundle, the 1,674-row focal count table, same-experiment corpus context, and focal rows from the declared training parquet for observed training targets.

## Evidence that set the scale

The focal count table is sharply zero-inflated: among 1,674 training perturbations, 1,205 had `n_degs = 0`, 276 had `n_degs = 1`, the median was 0, the 75th percentile was 1, and only 106 reached 10 or more DEGs. A large prediction therefore needs a target-specific reason to put `Zbtb24` into the rare high-footprint tail rather than the 0-1 bulk.

The declared exact reach measurement shows that `Zbtb24` was present in this thalamic population rather than absent: 13,491 of 23,679 non-target nuclei expressed it, with 56.97% expressing nuclei, mean CP10k 0.5802, and pseudobulk CPM 57.12. That supports perturbability in principle, but the bundle explicitly warns that target expression does not measure editing efficiency or endpoint strength.

The biology bundle gives `Zbtb24` a real but temporally uncertain molecular role. ZBTB24 is a sequence-specific transcriptional activator of `Cdca7` in the CDCA7-HELLS DNA-methylation pathway, and mouse loss is severe in early embryos and in postnatal hematopoietic loss. The postnatal neuronal evidence is unresolved, wild-type neuronal ZBTB24 turnover was not found, and the functional-stock adjudication was `partially_depleted_or_leading_edge` by the P16 to P37-P44 assay window because new ZBTB24 production should stop but pre-existing chromatin/DNA-methylation states may persist.

The most literal represented ZBTB-family comparators argued against assigning the broad `Zbtb7a` response to `Zbtb24` by family membership alone. In the same focal count table, `Zbtb10`, `Zbtb16`, `Zbtb20`, and `Zbtb21` had 0 DEGs, `Zbtb38` had 1, `Zbtb18` had 5, and `Zbtb7a` was the lone family outlier at 841. The corpus' ZBTB-family Finding context likewise states that ZBTB/BTB-ZF membership was not interchangeable in this juvenile postmitotic neuronal assay.

Chromatin and methylation-maintenance comparators also split by acute accessibility of the molecular state. In the focal table, `Dnmt3a`, `Mbd2`, `Smchd1`, and `Smarcad1` had 0 DEGs, while immediately acting or broader chromatin regulators such as `Mecp2`, `Setdb1`, `Kmt2a`, `Chd4`, and `Sin3a` had 16, 22, 24, 100, and 1,433 respectively. The corpus records for `Dnmt3a` interpret its flat P16 surface as buffering of an acute sparse perturbation to a cumulative DNA-methylation writer, which is closer to the persistence caveat for `Zbtb24` than the large `Sin3a` or `Zbtb7a` outliers.

## Synthesis

`Zbtb24` is not excluded by expression or by molecular plausibility, so I would not treat it as an assay-missing target. Still, the most endpoint-matched evidence points to a count in the mass of the focal prior rather than the broad-response tail: the direct neuronal requirement is unknown, the stock at harvest is expected to be partial or leading-edge, the direct CDCA7-HELLS/methylation output can be buffered by pre-edit installed chromatin, and both same-family and same-process training perturbations were mostly flat or sparse. I therefore place the point forecast at the modal/median low endpoint, `0` DEGs.
