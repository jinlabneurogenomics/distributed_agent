# Cacna1c direct forecast

## Endpoint

- Target: `Cacna1c`
- Cell group: `151 TH Prkcd Grin2c Glut`
- Endpoint: count of measured genes with BH-adjusted Wilcoxon `p < 0.05`
- Prediction: `1`

## Evidence used

### Declared target biology

The canonical Cacna1c biology bundle identifies the target as CaV1.2 alpha-1C, the pore-forming and voltage-sensitive subunit of an L-type calcium channel. The exact in-assay non-target expression measurement for `151 TH Prkcd Grin2c Glut` shows the target transcript is broadly present in the focal population: mean raw UMI 6.68, mean log1p CP10K 1.565, pseudobulk CPM 418.84, and 23,322 of 23,679 non-target nuclei expressing Cacna1c, or 98.49%.

The same bundle judged the post-edit functional channel stock `likely_substantially_depleted` by harvest: an edit should stop intact alpha-1C resupply, existing surface and recycling-pool channels can persist initially, but the 21-28 day edit-to-harvest interval is much longer than measured CaV1.2 surface cycling. This is only partial evidence because the kinetic anchor is target-specific but non-neural, native juvenile-thalamic turnover was not measured, and Cacna1d/CaV1.3 may buffer some L-type function.

### Same-experiment training counts

The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` table contained 1,674 visible training perturbations. Its burden distribution was highly zero-inflated in this thalamic class:

- 1,205/1,674 visible targets had zero DEGs.
- 469/1,674 had at least one DEG.
- 106/1,674 had at least 10 DEGs.
- 43/1,674 had at least 100 DEGs.
- The median was 0, the 75th percentile was 1, the 95th percentile was 18, and the maximum was 2,677.

The biology-matched voltage-gated calcium-channel perturbations were near-null:

- Pore subunits: `Cacna1a=0`, `Cacna1d=0`, `Cacna1e=0`, `Cacna1g=12`.
- Auxiliary/gamma subunits: `Cacna2d1=1`, `Cacna2d2=0`, `Cacnb2=0`, `Cacnb4=1`, `Cacng2=0`, `Cacng3=0`.

The calcium-signal and excitatory-receptor perturbations gave a small upper bearing but were not direct L-type-channel analogues:

- `Grin1=89`
- `Calm1=14`, `Calm2=0`, `Calm3=1`
- `Ppp3ca=4`, `Ppp3r1=9`

### Matched Parquet profile review

I compared the 16 named channel, NMDAR, calmodulin, and calcineurin training perturbations in the declared Parquet, filtered exactly to `group_name == "151 TH Prkcd Grin2c Glut"`, with `gene_target` as the node, `names` as the feature, `logfoldchanges` as the signed value, and `pvals_adj < 0.05` as significance. All 16 requested profiles and all 120 within-cohort pairs were available.

The exact matched profile counts reproduced the scalar table:

- `Cacna1a`, `Cacna1d`, `Cacna1e`, `Cacna2d2`, `Cacnb2`, `Cacng2`, and `Cacng3`: 0 significant features.
- `Cacna2d1`, `Cacnb4`, and `Calm3`: 1 significant feature.
- `Ppp3ca`: 4.
- `Ppp3r1`: 9.
- `Cacna1g`: 12.
- `Calm1`: 14.
- `Grin1`: 89.

The cohort diagnostic found poor transfer of a shared significant program: across the 120 channel/signaling pairs, the significant-program overlap coefficient had median 0 in both positive and negative directions. This keeps the larger `Grin1` and `Calm1` DEG burdens from being a direct estimate for Cacna1c.

### Packaged corpus context

The selected same-experiment corpus had no packaged `Cacna1c` Findings, Claims, or explicit same-experiment references, so it did not add a Cacna1c-specific measured profile. Existing packaged findings for represented CaV targets reinforced the direct count evidence: `Cacna1d` was interpreted as a near-null basal snRNA response rather than as a simple failed-targeting result, represented voltage-gated calcium-channel comparators did not phenocopy one another, and `Cacna1g` was the main thalamic calcium-channel exception with a small, Cav3.1-specific footprint.

## Synthesis

The random-training prior for this endpoint is dominated by zero and one-DEG outcomes, and the closest same-family perturbation, `Cacna1d`, is flat in this focal thalamic class despite being another neuronal L-type pore subunit. Other high-voltage CaV pore and auxiliary subunit losses are also flat or singleton-scale.

Cacna1c is not identical to those flat comparators: it is expressed in nearly every non-target nucleus in the exact assayed population, and the biology bundle supports substantial CaV1.2 stock depletion over the 21-28 day window. That argues against forcing an exact zero. Conversely, the absence of a shared CaV transcriptome and the sparse counts for `Cacna1g`, `Calm1`, and calcineurin argue against projecting an NMDAR-like or broad activity-response signature.

I therefore placed Cacna1c just above the direct L-type/CaV zero mode and below the small Cacna1g/Calm1 response scale: one measured FDR-significant gene.
