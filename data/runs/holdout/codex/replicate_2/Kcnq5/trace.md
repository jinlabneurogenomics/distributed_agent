# Kcnq5 direct DEG-count forecast

## Target and endpoint

- Target: `Kcnq5`
- Cell class: `151 TH Prkcd Grin2c Glut`
- Endpoint: count of measured rows with `pvals_adj < 0.05` in the focal class.
- Target-outcome handling: `Kcnq5` was absent from the declared 1,674-row training count table and had no same-experiment corpus report for its own perturbation. I did not use a held-out `Kcnq5` expression signature or any `Kcnq5` DEG count.

## Biology bundle evidence

The canonical Kcnq5 biology bundle places KCNQ5 as a pore-forming Kv7.5 voltage-gated potassium-channel subunit that can assemble with KCNQ3 and with KCNQ2/3-containing native channel combinations. The edit should matter at the stock level: KCNQ5 was adjudicated as a dynamic membrane-channel component whose functional stock is likely substantially depleted by the 21-28 day P16-to-P37/P44 window, with partial evidence because the direct CRISPR-to-protein timing evidence was in cultured hippocampal neurons rather than juvenile thalamus.

Exact focal-population reach was low but nonzero: in non-targeting `151 TH Prkcd Grin2c Glut` nuclei, `Kcnq5` was detected in 4,350 / 23,679 nuclei, `18.3707%`, with `mean_cp10k = 0.2133`, `pseudobulk_cpm = 21.25`, and an available focal perturbation contrast. That made a complete silent prediction too low, but the low reach, weak adult thalamic KCNQ5 abundance, and unresolved acute thalamic phenotype argued against a broad downstream program.

## Training counts and declared Parquet evidence

The focal training count table is zero-heavy: 1,205 / 1,674 training targets have `n_degs = 0`, the median is 0, and the 75th percentile is 1. A tiny integer therefore needs more weight than the high mean, which is pulled by a few broad responders.

Typed Kcnq5 analog nomination over the declared training universe recovered:

- `Kcnq3`, rank 1, as an exact-complex/paralog analog through an ortholog-projected KCNQ3-KCNQ5 complex plus physical and functional annotations; focal `n_degs = 1`.
- `Kcnq2`, rank 2, as a direct-interaction/function analog; focal `n_degs = 1`.
- Broader voltage-gated potassium-channel candidates were sparse in the same count table: `Kcna1 = 0`, `Kcna2 = 0`, `Kcnc1 = 0`, `Kcnc2 = 1`, `Kcnh1 = 0`, `Kcnj6 = 0`, and `Kcnb1 = 0`.
- More distant excitability/channel fallbacks were also mostly tiny in this focal group: `Scn1a = 1`, `Scn2a = 1`, `Grin2a = 1`, `Grin2b = 2`, with `Grin1 = 89` as a broader NMDAR exception rather than a Kv7-scale analog.

Direct slices from `training_de_all_cell_groups.parquet` showed that the closest Kv7 analogs were at the self-transcript edge of significance in `151 TH Prkcd Grin2c Glut`:

- `Kcnq2` had exactly one `pvals_adj < 0.05` row, the target transcript itself; its nearest focal downstream candidate, `Agap2`, was just above the requested cutoff at `pvals_adj = 0.050867`.
- `Kcnq3` had exactly one `pvals_adj < 0.05` row, also the target transcript itself.
- `Kcnq1` had zero significant rows in this focal class.

A profile-neighborhood query on `Kcnq1`, `Kcnq2`, `Kcnq3`, `Hcn2`, `Scn1a`, and `Gabrg2` within the same focal Parquet context gave the same qualitative picture: `Kcnq1` had `0` significant features, the other channel anchors had `1` each, and their best whole-profile neighbors were weak (`r = 0.077` for `Kcnq3`, `r = 0.148` for `Kcnq2`, `r = 0.125` for `Scn1a`). That supported treating the single significant self row as the common scale for electrically active channel perturbations in this class rather than borrowing a broad stress or receptor program.

## Same-experiment corpus context

The corpus around represented Kv7 genes was used as interpreted same-experiment context, not as independent validation. It reported that `Kcnq1`, `Kcnq2`, and `Kcnq3` produce sparse, paralog-specific neuronal outputs rather than a shared KCNQ RNA program; it explicitly notes that `Kcnq5` was not represented as a perturbation target. `Kcnq3` in particular was summarized as having no robust immediate-early, ISR/UPR, heat-shock, or voltage-gated-channel compensation program despite electrical Kv7 biology. This matches the declared Parquet: focal Kv7 perturbations did not generate a persistent multi-gene resting nuclear signature.

## Synthesis

`Kcnq5` is expressed in enough focal thalamic nuclei, and its stock is expected to be depleted quickly enough, that a pure null is not the best point. But every task-matched analog closer than a broad ion-channel fallback points to a one-row or zero-row focal signature, and the most relevant observed Kv7 partners reached one FDR<0.05 row in this cell class without a counted downstream module. I therefore forecast the Kcnq5 focal response as the same self-row-sized footprint, with no durable downstream program crossing the hard 0.05 threshold.

Point forecast: `1`
