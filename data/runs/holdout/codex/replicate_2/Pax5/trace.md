# Pax5 DEG-count forecast

## Endpoint and declared target

- The one-row holdout manifest declares `Pax5` as the target.
- The requested endpoint is `n_degs` in `151 TH Prkcd Grin2c Glut`: the number of measured genes with BH-adjusted Wilcoxon `p < 0.05`.
- The declared focal count table has 1,674 training perturbations and does not contain `Pax5`.

## Biology bundle evidence

The target-specific biology bundle argues that Pax5 is a free nuclear sequence-specific transcription factor whose operative protein stock should largely turn over within the 21-28 day P16-to-P37/P44 experimental window in cells that truly express Pax5. Its 9.7 hour protein half-life was measured in a mouse pro-B-cell line, so timing transfer to postmitotic thalamic neurons is partial rather than direct.

The stronger constraint is focal-population reach. In the exact `151 TH Prkcd Grin2c Glut` non-target population, the Pax5 feature is present but nearly absent:

- `n_non_target_cells = 23679`
- `n_cells_expressing = 29`
- `pct_cells_expressing = 0.1224713881498374`
- `total_target_umi = 33`
- `mean_raw_umi = 0.0013936399341188395`
- `pseudobulk_cpm = 0.08734435669051036`

The source-card and residual cards are consistent with that narrow reach: adult mouse brain evidence supports restricted Pax5 signal enriched outside broad thalamic neurons, while the closest mouse neural loss evidence is developmental cerebellar and midbrain evidence rather than postnatal thalamic loss. Pax2 can compensate Pax5 dosage during embryonic midbrain/cerebellar development, but there is no postnatal thalamic compensation test.

## Training measurements used

I treated the declared count CSV and Parquet as two same-experiment representations: the CSV supplied the already counted focal endpoint, and the Parquet supplied exact focal rows and recovered-cell counts.

The `151 TH Prkcd Grin2c Glut` training count distribution is highly zero-inflated:

- 1,205 of 1,674 training targets have `n_degs = 0`.
- The median is 0.
- 1,481 of 1,674 have `n_degs <= 1`.
- The 95th percentile is 18.
- The long right tail is driven by a small number of broad/high-impact perturbations such as `Uba5`, `Tpr`, `Sin3a`, spliceosome/proteasome genes, and global regulators.

The focal Parquet slice contains 28,891,566 rows across the same 1,674 training perturbations. Matched recovered perturbed nuclei per target in this class have:

- minimum 23
- first quartile 140
- median 177
- third quartile 211
- maximum 419
- matched controls 23,679

Combining the median perturbed-cell count with the exact Pax5 non-target expression reach gives `177 * 29 / 23679 = 0.217` Pax5-expressing recovered cells expected per median perturbation under a matching random draw from this class. Even at the training maximum of 419 matched perturbed cells, the expectation is only `419 * 29 / 23679 = 0.513` Pax5-expressing recovered cells. Sparse mosaic editing would further dilute the functional Pax5-loss subset. Thus, even if Pax5 loss has a strong single-cell effect in the rare Pax5-positive nuclei, the class-aggregated Wilcoxon contrast is expected to have essentially no detectable population-average footprint.

Developmental or lineage-skewed transcription-factor perturbations with closer qualitative biology were also quiet in the same focal count table. `Pax2`, `Pax3`, `Pax4`, `Pax6`, `Pax7`, `Pax8`, `Ebf1`, `Ebf2`, `Ebf3`, `En1`, `En2`, `Pou2f1`, `Pou2f2`, `Foxa2`, `Foxp2`, `Ikzf3`, `Lhx3`, and `Lhx4` all had `n_degs = 0`; none had even one gene with BH-adjusted `p < 0.05`.

## Forecast

Pax5 is plausibly functionally depleted by harvest in cells that express it, so the null is not due to durable pre-edit protein. The forecast is nevertheless dominated by exact focal reach: only 29 of 23,679 non-target nuclei expressed Pax5 at all, and the expected number of Pax5-positive recovered perturbed nuclei is far below one for a typical training target in this cell class. The training distribution and related restricted/developmental TF perturbations both show that zero DEGs is the ordinary outcome for such mismatched targets in `151 TH Prkcd Grin2c Glut`.

Predicted `n_degs`: 0.
