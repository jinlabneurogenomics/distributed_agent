# Trpv4 n_degs prediction

Target: `Trpv4`

Cell group: `151 TH Prkcd Grin2c Glut`

Predicted `n_degs`: `0`

## Evidence used

The canonical biology bundle supports functional realization in an edited, TRPV4-dependent cell but not broad reach in the assayed thalamic neuronal aggregate.

- `Trpv4` encodes a calcium-permeable TRP-family membrane cation channel. A disruptive edit should stop new channel synthesis, and the functional-stock card adjudicates the operative channel pool as `likely_substantially_depleted` by the P37-P44 harvest after P16 editing.
- The kinetic evidence is partial: surface TRPV4 can cycle on a minute timescale and engineered TRPV4 protein persistence was measured in hours, not weeks, but there is no synchronized wild-type TRPV4 clearance assay in postmitotic thalamic neurons.
- The loss-of-function phenotype evidence is outside the target population: germline `Trpv4` loss affects adult mouse CNS-linked osmoregulation, while the closest cellular-distribution evidence is a restricted minority of hippocampal astrocytes rather than thalamic NeuN-positive neurons.
- The exact focal expression measurement is the decisive reach constraint: among 23,679 matched non-target nuclei in `151 TH Prkcd Grin2c Glut`, only 167 had a `Trpv4` UMI, with 177 total UMIs, 0.705% expressing nuclei, mean raw UMI 0.00747, mean CP10K 0.00444, and pseudobulk CPM 0.468. This makes the aggregate thalamic-neuron contrast much more likely to average over mostly non-expressing cells than to expose a class-wide state.

The declared count table shows that this population is already sparse and that closely related local training perturbations are quiet.

- Of 1,674 training perturbations in `151 TH Prkcd Grin2c Glut`, 1,205 have `n_degs = 0`, 1,481 have `n_degs <= 1`, the median is 0, the 75th percentile is 1, and the 90th percentile is 2.
- The training TRP-channel rows nearest to the target were all null in the count table: `Trpv1`, `Trpa1`, `Trpm3`, and `Trpm7` each had `n_degs = 0`.
- Other calcium-, sodium-, potassium-, and ionotropic-glutamate-channel perturbations were mostly null or self-only in the same table: `Cacna1a`, `Cacna1d`, `Cacna1e`, `Grin2d`, and `Grin3a` were 0; `Scn1a`, `Scn2a`, and `Scn8a` were each 1; the clearer active exception among this manually inspected channel set was `Cacna1g` with 12 DEGs.
- Direct reads from `training_de_all_cell_groups.parquet` in the exact cell group confirmed no BH-significant genes for the four quiet TRP-channel perturbations above. For the one-DEG sodium-channel controls, the sole significant rows were their self-target transcripts, so those do not provide evidence for a downstream multi-gene survivor state.

## Synthesis

I used the exact reach measurement as a stronger endpoint-specific constraint than the general TRPV4 loss-of-function phenotype. The channel should be lost after a successful edit, but in the assayed thalamic NeuN-positive aggregate it is detected in fewer than 1% of control nuclei. That makes both the self-target row and any downstream cell-autonomous program weakly powered after BH correction. The declared training distribution is heavily zero-inflated, and the available local TRP/cation-channel comparators sit at the zero or self-only end of that distribution.

The remaining uncertainty is a rare-subpopulation effect: a tiny `Trpv4`-expressing subset could in principle enter a strong state that survives aggregation. I did not see enough matched biology or profile evidence to move the point estimate off the modal null count, so my direct forecast is:

`Trpv4	0`
