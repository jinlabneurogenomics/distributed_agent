# Arnt2 direct DEG-count forecast

## Target and endpoint

- Holdout target: `Arnt2`
- Cell group: `151 TH Prkcd Grin2c Glut`
- Endpoint: `n_degs`, the number of measured focal-class genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`

## Evidence used

### Canonical target biology

The declared biology bundle for `Arnt2` supports functional realization by harvest but with limited endpoint reach:

- `Arnt2` is a dynamic nuclear bHLH-PAS transcriptional partner rather than a permanent structural stock; a disruptive P16 edit is expected to stop intact resupply, and the P37-P44 harvest window is long enough that ARNT2-dependent complex capacity should be substantially depleted.
- The closest molecular evidence is from other neuronal contexts: ARNT2 can occupy neuronal regulatory elements with NCoR2 at baseline and NPAS4 after depolarization.
- The strongest mouse loss-of-function phenotype is developmental, in embryonic hypothalamic PVN/SON neurons with perinatal lethality, not an inducible P16 loss in postmitotic thalamic neurons.
- ARNT provides experimentally supported partial bHLH-PAS overlap, including retained HIF1A complex function in Arnt2-null cortical neurons, so loss of `Arnt2` need not eliminate all related transcriptional output.
- Exact in-assay non-target expression in `151 TH Prkcd Grin2c Glut` is present but modest: 7,219 of 23,679 nuclei express `Arnt2` at nonzero counts, `30.4869%` of the focal non-target nuclei, with mean raw UMI `0.49394`, mean log1p CP10K `0.20027`, and pseudobulk CPM `30.95696`.

### Training count table

The declared focal-class count table contains 1,674 measured training perturbations. Its empirical distribution is very sparse:

- `1205/1674` training targets have `n_degs = 0`.
- `1481/1674` have `n_degs <= 1`.
- The median is `0`, the 75th percentile is `1`, and the 90th percentile is `2`.
- The mean, `14.05`, is dominated by a long high-response tail: 42 targets exceed 100 DEGs and 15 exceed 500.

The closest measurable ARNT2-related or activity-dependent transcription-factor comparators in the same focal count table were all exact zeros:

| training target | relation considered | focal `n_degs` |
| --- | --- | ---: |
| `Arnt` | bHLH-PAS paralog/partial functional overlap cited in the `Arnt2` bundle | 0 |
| `Hif1a` | ARNT/ARNT2 bHLH-PAS partner axis | 0 |
| `Ahr` | ARNT-family bHLH-PAS partner axis | 0 |
| `Ahrr` | AHR-axis repressor | 0 |
| `Npas3` | NPAS/bHLH-PAS family member | 0 |
| `Nr4a1` | immediate-early/activity-linked transcription factor | 0 |
| `Nr4a3` | immediate-early/activity-linked transcription factor | 0 |
| `Egr2` | immediate-early/activity-linked transcription factor | 0 |
| `Fosl2` | AP-1/immediate-early-axis factor | 0 |
| `Jund` | AP-1/immediate-early-axis factor | 0 |

`Npas4`, the strongest activation partner named by the target bundle, and `Ncor2`, the baseline repressive partner, were not present in this training count table.

### Parquet focal rows

I directly filtered the declared expression Parquet to `group_name == "151 TH Prkcd Grin2c Glut"` for `Arnt`, `Hif1a`, `Ahr`, `Ahrr`, `Npas3`, `Nr4a1`, `Nr4a3`, `Egr2`, `Fosl2`, and `Jund`. Each perturbation had 17,259 focal-class measured-gene rows and zero rows with `pvals_adj < 0.05`, confirming that the aggregate zeros were not hiding any significant focal features.

The closest bHLH-PAS comparators were also far from a BH-significant profile:

- `Arnt`: minimum focal adjusted p-value `1.0`
- `Hif1a`: minimum focal adjusted p-value `0.3063`
- `Ahr`: minimum focal adjusted p-value `0.2206`

## Synthesis

`Arnt2` loss should be molecularly realized by the end of the experiment, so I did not treat the perturbation as failed. However, the endpoint is survivor-conditioned nuclear RNA aggregated across the focal thalamic class, not a stimulated NPAS4 program or a developmental hypothalamic assay. The exact target expression reaches only about 30% of focal non-target nuclei, the mean expression is below one raw UMI per nucleus, the most transferable phenotype evidence is developmental and anatomically different, and ARNT/other bHLH-PAS activity can buffer some target functions.

The training distribution makes zero the modal and median count in this class, and every measured local analogue I considered, including `Arnt`, `Hif1a`, and `Ahr`, is an exact verified zero in the focal rows. I therefore place `Arnt2` in the quiet focal-class transcription-factor regime rather than in the rare high-yield tail driven by broad RNA-processing, proteostasis, or essential-cell-state perturbations.

Predicted `n_degs`: `0`
