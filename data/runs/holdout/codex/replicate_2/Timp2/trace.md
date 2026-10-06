# Timp2 direct `n_degs` forecast

## Declared target and endpoint

- Manifest target: `Timp2`.
- Focal population: `151 TH Prkcd Grin2c Glut`.
- Endpoint: the number of measured genes with Wilcoxon `pvals_adj < 0.05` in the focal population.
- Prediction: `1`.

## Evidence used

### Canonical Timp2 biology bundle

The exact in-assay reach entry for the declared target showed that `Timp2` is a usable local target transcript in the focal population:

- `group_name`: `151 TH Prkcd Grin2c Glut`
- `n_non_target_cells`: `23679`
- `n_cells_expressing`: `18431`
- `pct_cells_expressing`: `77.83690189619495`
- `mean_cp10k`: `2.0101145570716605`
- `pseudobulk_cpm`: `198.372268037587`

The functional-stock card makes Timp2 biologically reachable over the 21-28 day window but does not make it look like a high-amplitude cell-autonomous transcription-factor perturbation. TIMP2 is a secreted extracellular/pericellular metalloproteinase regulator. A disruptive edit should stop new TIMP2 supply; the existing extracellular protein can persist at least over hours after MT1-MMP binding, while week-scale persistence to P37-P44 is not supported. The card therefore calls functional stock at harvest `likely_substantially_depleted`, but with partial evidence and residual uncertainty from extracellular persistence, family buffering by other TIMPs, and the lack of a P16-onset thalamic timing study.

The observability card also points to a real but mismatched neural prior: Timp2 loss has postnatal/adult neural phenotypes in cerebellar, neuromuscular, and hippocampal settings, but not a demonstrated thalamic 151-class survivor RNA signature.

### Focal count table

The declared 151-class training count table has 1,674 training targets and is heavily concentrated at zero:

- `1205 / 1674` targets had `n_degs = 0`.
- `276 / 1674` targets had `n_degs = 1`.
- `469 / 1674` had any nonzero DEG count.
- `106 / 1674` reached at least 10 DEGs.
- `43 / 1674` reached at least 100 DEGs.
- median count was `0`; 75th percentile was `1`; 95th percentile was `18`.

The large focal responses were dominated by global RNA-processing, proteostasis, transcriptional, and chromatin perturbations such as `Uba5`, `Tpr`, `Sin3a`, `Rnpc3`, `Zbtb7a`, `U2af2`, `Psmb4`, `Hnrnpu`, and `Yy1`, not by extracellular matrix regulators.

### Training perturbations near Timp2 biology

The closest obvious matrix/TIMP/protease-adjacent training rows were low or zero:

- `Timp3`: `1`
- `Adam10`: `0`
- `Adamts17`: `0`
- `App`: `1`
- `Itgb1`: `0`
- `Lrp1`: `0`

`Timp1`, `Timp4`, `Mmp2`, `Mmp9`, `Mmp14`, `Mmp16`, and `Mmp17` were not visible focal training perturbations in the declared count table, so they could not supply measured count analogs.

I scanned the declared Parquet in `151 TH Prkcd Grin2c Glut` for the six low-count analogs above. The only FDR-significant rows were self-target transcripts:

- `App` perturbation: significant row `App`, log-fold change `-1.4204920530319214`, adjusted p-value `8.410042957648515e-58`.
- `Timp3` perturbation: significant row `Timp3`, log-fold change `-0.841637909412384`, adjusted p-value `1.4532540541573227e-06`.

Across the whole focal training table, `237 / 276` one-DEG perturbations were self-only, and `277 / 363` perturbations in the `1`-to-`9` DEG band had a significant self transcript. Thus a one-gene count in this assay very often means visible editing of the target transcript rather than a broad downstream program.

The profile-neighborhood check in the focal class agreed with the simple count interpretation. In a symmetric comparison of `Timp3`, `Adam10`, `Adamts17`, `App`, `Itgb1`, and `Lrp1`, four of the six anchors were in the `no_significant_features` band and only `Timp3` and `App` were in the `1_to_9_significant_features` band.

## Synthesis

`Timp2` is expressed broadly enough in the exact focal population that a lone significant self or directly local row is plausible. However, its product is secreted, extracellular, partly non-cell-autonomous, and embedded in a redundant TIMP/MMP system; the supplied loss phenotypes are outside the matched thalamic context; and the closest measured ECM/TIMP-adjacent perturbations were zero or self-only. That combination argues against a large 151-class survivor-state program and puts the point forecast at the sparse edge of the distribution.

I therefore predict one FDR-significant measured gene:

```text
Timp2 n_degs = 1
```

The held-out `Timp2` outcome was not used.
