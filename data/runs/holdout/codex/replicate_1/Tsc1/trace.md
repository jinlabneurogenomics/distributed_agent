## Forecast

target: `Tsc1`

predicted `n_degs`: `86`

## Evidence used

The declared target is `Tsc1`; the one-row manifest and the canonical biology bundle agree on that symbol. The endpoint is the number of measured genes in `151 TH Prkcd Grin2c Glut` with Wilcoxon `pvals_adj < 0.05`.

The exact target-expression card makes target absence unlikely: in the matched non-target population of `151 TH Prkcd Grin2c Glut`, `Tsc1` is detected in 16,583 of 23,679 nuclei, with 70.03% of nuclei expressing it, mean log1p CP10K 0.5228, mean raw UMI 1.324, and pseudobulk 82.99 CPM. The same bundle adjudicates the operative perturbation as loss of a renewable TSC1-TSC2-TBC1D7 Rheb-GAP complex, not a long-lived stored state: TSC1 stock is expected to be substantially depleted within the 21-28 day P16-to-P37/P44 window, with adult-neuron TSC1 protein falling within days and mTORC1 restraint failing by days 6-8 in the cited mouse forebrain model. The bundle also reports no close TSC1 paralog or same-context replacement subunit after bounded search.

The training count table is very sparse in this focal class: among 1,674 observed perturbations, 1,205 have `n_degs = 0`, 469 are nonzero, the median is 0, the 90th percentile is 2, the 95th percentile is 18, and only 63 targets exceed 20 DEGs. Thus an 80-ish response is in the upper tail but far below the broad global stress responses such as `Uba5` or `Sin3a`.

The direct complex analogue is `Tsc2`. In the declared training count table `Tsc2` has 86 focal-class DEGs, and a direct Parquet query in `151 TH Prkcd Grin2c Glut` reproduced 86 genes with `pvals_adj < 0.05`: 58 up, 28 down, 17,259 measured genes, and 177 matched perturbed nuclei. The strongest significant `Tsc2` rows include the sterol/lysosome and mTOR-feedback genes `Pik3r3`, `Cyp51`, `Ldlr`, `Msmo1`, `Ddit4`, `Rragd`, and `Lamp2`, consistent with the same-experiment Tsc2 Findings that describe a caudal neuronal mTORC1 sterol/lysosomal response rather than a random injury signature.

More distant mTOR-axis training perturbations did not justify shrinking the direct-complex estimate to the class baseline. The same count table has `Depdc5 = 13`, `Mtor = 2`, `Lztr1 = 1`, and `Rptor`, `Akt3`, `Pik3cb`, `Pik3r1`, `Pik3r2`, and `Strada` all at 0 in this focal class. A bounded same-experiment Tsc2 report similarly separated these by pathway position: `Depdc5` partially matched the thalamic Tsc2 sterol state, whereas `Mtor`, `Rptor`, `Igf1r`, `Irs1`, and `Akt3` did not give robust matched overlap. I used these as evidence that generic mTOR-pathway membership is insufficient, not as evidence against Tsc1 itself.

I did not use the larger high-DEG stress and endolysosomal neighbors (`Psmb4`, `Psmc1`, `Rab7`, `Sin3a`) as equal-scale anchors. The Tsc2 corpus record treats them as downstream-state convergence, and their direct perturbations are broader or off-axis relative to removing the TSC complex brake.

## Synthesis

`Tsc1` and `Tsc2` are the closest available operation-matched pair: disrupting either should disable the TSC complex and relieve Rheb/mTORC1 restraint in successfully edited neurons. The exact expression reach argues that Tsc1 is present in most assayed thalamic neurons, and the stock card argues that an edit has enough time to remove functional TSC1 by harvest. Those facts make a zero or 1-2 DEG forecast inappropriate despite the sparse training prior.

The main downward uncertainties are guide/editing realization, survivor conditioning, and the fact that TSC1 is the stabilizing subunit while TSC2 is the catalytic GAP-bearing subunit. None gives a quantified reason to move far away from the directly measured `Tsc2` footprint, while the weak `Mtor`/`Rptor`/PI3K rows are upstream, downstream, or opposite-sign pathway tests rather than same-complex analogues.

I therefore used `Tsc2` as the quantitative center and predicted the same focal-class scale: **86 DEGs**.
