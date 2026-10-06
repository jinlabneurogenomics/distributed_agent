# Grik2 forecast for 151 TH Prkcd Grin2c Glut

## Endpoint

The requested endpoint is `n_degs`: the count of measured genes in `151 TH Prkcd Grin2c Glut` with BH-adjusted Wilcoxon `pvals_adj < 0.05`. The held-out target is `Grik2`; its target expression signature and target count were not used.

## Evidence used

- The declared `Grik2` biology bundle identifies GluK2 as a kainate-family ionotropic glutamate receptor subunit that contributes to tetrameric surface receptor complexes. Its exact focal-population reach is high: in the matched non-target nuclei for `151 TH Prkcd Grin2c Glut`, Grik2 is detected in 23,374 of 23,679 nuclei, with 98.71% of cells expressing and mean log1p(CP10K) 1.62.
- The same bundle adjudicates the functional-stock prior as `likely_substantially_depleted` by the P37-P44 harvest: a P16 disruptive edit should stop new GluK2 supply, while existing receptors turn over through dynamic surface, recycling, and lysosomal routes. The evidence is partial, because measured GluK2 trafficking was stimulated hippocampal trafficking rather than a basal thalamic edit-to-clearance curve, and the mouse loss phenotypes were germline hippocampal or adult behavioral observations rather than acute thalamic knockouts.
- The declared 151-TH training count table is strongly zero-inflated. Among 1,674 non-held-out perturbations, 1,205 have `n_degs = 0`, the median is 0, the 75th percentile is 1, and the 90th percentile is 2; only 42 perturbations have more than 100 DEGs, mostly broad transcription, splicing, ubiquitin, proteasome, or transport machinery rather than receptor subunits.
- The closest represented kainate receptor subunits are quiet in this focal class: `Grik1 = 0`, `Grik3 = 0`, `Grik4 = 0`, and `Grik5 = 1` in the declared `pvals_adj < 0.05` count table. A direct Parquet query for the focal class showed that all four have zero non-self significant genes; the lone `Grik5` hit is its target transcript.
- Broader ionotropic receptor comparators also support a near-null forecast. In the same count table, `Gria1 = 0`, `Gria2 = 0`, `Gria3 = 0`, `Grid1 = 1`, `Grid2 = 0`, `Grin2a = 1`, `Grin2b = 2`, `Grin2d = 0`, and `Grin3a = 0` in `151 TH Prkcd Grin2c Glut`. The clear high receptor boundary is `Grin1 = 89`, but direct Parquet rows show 88 downstream DEGs for `Grin1`, making it a special obligate NMDAR-core response rather than the scale expected for individual kainate, AMPA, delta, or modulatory NMDAR subunits.
- Same-experiment corpus interpretation was used as a semantic layer over those training observations, not as independent replication. The packaged high-confidence kainate Claim states that represented `Grik1`, `Grik3`, `Grik4`, and `Grik5` perturbations do not form a shared basal neuronal transcriptomic response module, while explicitly noting that `Grik2` and NETO auxiliary subunits were not tested. A separate `Grin1` Claim notes that represented NMDA subunit losses are subunit- and context-specific rather than a generic NMDAR loss-of-function transcriptional signature.

## Reasoning

Grik2 has much better focal reach than a target absent from these thalamic neurons, and functional receptor stock should not simply persist through the whole 21-28 day window. Those two points move the prediction above a hard null.

The magnitude evidence is still dominated by receptor-class buffering. All four measured kainate paralogs have no downstream DEG in the focal class, and the broader receptor set is nearly all 0-2 DEGs. `Grin1` shows that a synaptic receptor perturbation can be visible in this assay, but it is an obligate core NMDAR subunit with a distinctive 151-TH adaptive/stress and synaptic-remodeling program; the other Grin subunits do not phenocopy it in this cell class. I therefore treated `Grin1` as an upper biological boundary, not as a local scale donor for `Grik2`.

The count I expect for `Grik2` is consequently a near-null singleton: the high target reach and likely protein turnover leave room for one detected feature, but the family and pathway evidence argue against a multi-gene response. I predict:

`predicted_n_degs = 1`
