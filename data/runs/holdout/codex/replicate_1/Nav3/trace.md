# Nav3 151 TH Prkcd Grin2c Glut DEG-count forecast

## Endpoint and declared target

- Holdout manifest target: `Nav3`.
- Endpoint: `n_degs` in `151 TH Prkcd Grin2c Glut`, counting measured-gene rows with BH-adjusted Wilcoxon `pvals_adj < 0.05`.
- Target perturbation DE rows and the target DEG count were not used; the forecast uses the declared `Nav3` biology bundle, the same-cell-class training count table, and training rows from the all-cell expression Parquet.

## Nav3 biology prior

- The exact focal-population expression card shows `Nav3` is readily present in the assayed thalamic population: `22647 / 23679` matched non-target nuclei expressed the feature (`95.6417%`), with mean `2.7793` CP10K and `4.3937` raw UMI per nucleus.
- The canonical biology bundle supports a microtubule/cytoskeletal operation: NAV3 binds microtubules and promotes persistence of polymerized microtubules.
- Loss evidence is not matched to this P16-to-P37/P44 mouse neuronal assay. The available loss evidence is human developmental genetics plus embryonic zebrafish knockdown, adult mouse thalamic expression establishes reach but not postnatal demand, and no target-specific NAV3 turnover or postnatal loss clock was found.
- The functional-stock card therefore leaves `functional_stock_by_harvest` indeterminate: a disruptive edit should stop new full-length NAV3 supply, but does not instantly remove existing cytoskeletal-associated protein or already organized microtubules.

## Training scale

- The declared 151-class training table contains 1,674 targets. It is highly sparse: 1,205 targets have `n_degs = 0`, the median is `0`, the 75th percentile is `1`, the 90th percentile is `2`, and the 95th percentile is `18`.
- `Nav1`, `Nav2`, and `Nav3` are absent from the training count table, so there is no measured neuron-navigator paralog donor.
- A manually inspected set of 33 cytoskeletal, microtubule, actin-signaling, and microtubule-trafficking training targets had a median `n_degs` of `1` and an interquartile range of `0-1`. Examples at exactly one DEG include `Actg1`, `Atl1`, `Cdc42`, `Dnm1`, `Kif1a`, `Kif5a`, `Kif5c`, `Map1b`, `Mapre2`, `Mapt`, `Pak1`, `Stmn2`, `Tubb4b`, and `Tubb5`.
- Direct inspection of the training Parquet showed that those one-DEG cytoskeletal examples were usually self-transcript-only calls in this cell class: `Actg1`, `Atl1`, `Cdc42`, `Dnm1`, `Kif1a`, `Kif5a`, `Kif5c`, `Map1b`, `Mapre2`, `Mapt`, `Pak1`, `Stmn2`, `Tubb4b`, and `Tubb5` each had only the perturbed target itself significant at FDR 0.05.
- Axon-guidance ligands and receptors in the same training table were even quieter: `Epha2`, `Epha3`, `Epha5`, `Epha10`, `Ephb1`, `Ephb2`, `Ephb4`, `Robo2`, `Robo4`, `Sema4d`, `Sema6a`, and `Slit2` were all zero; only `Epha4`, `Robo1`, and `Sema5a` reached `1`.
- The major cytoskeletal exception was `Dctn1` at 75 DEGs. Raw 151-class rows and same-experiment Findings both indicated this was a sterol/cholesterol-response profile rather than a generic response to perturbing axon or microtubule regulators, so I treated it as an upper-side boundary rather than a direct point donor.

## Synthesis

`Nav3` is expressed broadly enough in the target population that a measured self-transcript effect could plausibly contribute one significant row. However, the biology bundle provides no evidence for rapid postnatal depletion of an essential functional stock, the closest developmental/axon-growth evidence is timing-mismatched, and measured training perturbations in microtubule, actin, motor, and axon-guidance machinery are predominantly silent or self-only in `151 TH Prkcd Grin2c Glut`.

I therefore forecast a self-only-scale response rather than a broad downstream module.

Predicted `n_degs`: `1`
