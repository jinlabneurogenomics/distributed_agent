# Foxc1 n_degs forecast

## Prediction

`Foxc1` in `151 TH Prkcd Grin2c Glut`: **0** measured genes with BH-adjusted Wilcoxon `p < 0.05`.

## Evidence used

- The one-row holdout manifest names `Foxc1`; `Foxc1` is absent from the declared 1,674-target focal-class training count table.
- The target bundle reports extremely low exact focal-population reach for `Foxc1` in matched non-target nuclei: 154 / 23,679 nuclei expressing, 0.650365% expressing, 0.0072638 mean raw UMI, 0.0042307 mean cp10k, 0.0031123 mean log1p cp10k, and 0.455249 pseudobulk CPM in `151 TH Prkcd Grin2c Glut`.
- The biology bundle supports a realizable loss in cells that actually express the target: FOXC1 is a renewable nuclear forkhead transcription factor, and the adjudicated functional-stock card calls pre-edit FOXC1 likely substantially depleted by the P37-P44 harvest after a P16 edit.
- The same bundle argues that the expected expressing compartment is poorly matched to this assay. Mouse loss phenotypes are developmental and meningeal or vascular-adjacent, developing-brain localization placed Foxc1 in meninges/pericytes/vascular smooth muscle rather than neural tissue apart from vessel-associated cells, adult thalamic signal is only low bulk RNA with Allen ISH non-detection, and NeuN-positive sorting excludes the non-neuronal populations in which the literature most clearly places `Foxc1`.
- In the declared `151 TH Prkcd Grin2c Glut` count table, zero is the dominant training outcome: 1,205 / 1,674 perturbations have `n_degs = 0`; the median is 0, the third quartile is 1, the 90th percentile is 2, and the high mean of 14.05 is driven by a small tail of broad responders.
- Deterministic annotation placed `Foxc1` in the broad `transcription_factor` and `dna_binding` groups. Intersecting annotated TF perturbation targets with the declared training table gave 344 TFs, 284 of them zero in this focal class; the median TF count was 0, the 90th percentile was 2, and the largest TF outliers were context-general regulators such as `Zbtb7a`, `Yy1`, `Cic`, `Thap11`, and `Rora`.
- The count table and the focal rows of the expression parquet agree that the available FOX-family training perturbations were silent in this class: `Foxa2`, `Foxc2`, `Foxe3`, `Foxi1`, `Foxj3`, `Foxk2`, `Foxl1`, `Foxl2`, `Foxn1`, `Foxp2`, and `Foxp3` each had 17,259 measured genes and zero BH-significant genes in the `151 TH Prkcd Grin2c Glut` parquet slice.

## Synthesis

The stock card prevents interpreting `Foxc1` as an intrinsically impossible acute perturbation: if a recovered thalamic neuron were materially dependent on FOXC1, the 21-28 day post-edit window should be long enough to deplete the pre-edit nuclear TF pool. The limiting issue is instead target reach and context. Only ~0.65% of focal non-target nuclei contain a `Foxc1` UMI, the pseudobulk level is below 0.5 CPM, and the curated source facts put the strongest endogenous Foxc1 brain activity in meningeal/perivascular compartments outside the NeuN-positive nuclear gate. Any true FOXC1-dependent cell-autonomous program should therefore be diluted across the aggregated thalamic neuronal contrast and unlikely to generate BH-significant whole-class DE.

The training table reinforces choosing the focal-class mode rather than a small positive count. Most perturbations in this class are zero, annotated transcription factors are even more often zero, and the directly available FOX training perturbations, including the close paralog `Foxc2`, are all zero despite having the same 17,259-gene DE test surface in the parquet. The rare large TF responses come from broad neuronal or chromatin/transcriptional regulators with stronger plausibility in recovered neurons, which is not the evidence profile for `Foxc1`.

Balancing the realizable knockout against very weak neuronal reach and FOX/TF training precedent, the point forecast is:

`predicted_n_degs = 0`
