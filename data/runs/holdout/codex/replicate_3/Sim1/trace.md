# Direct n_degs forecast for Sim1 in 151 TH Prkcd Grin2c Glut

## Determining evidence

- Target: `Sim1`, from the one-row manifest.
- Endpoint: `n_degs`, the count of measured genes with BH-adjusted Wilcoxon `p < 0.05` in `151 TH Prkcd Grin2c Glut`.
- Target outcome used: no. The target 151-class signature and target DEG count were absent from the declared inputs.

### Canonical Sim1 biology bundle

The strongest biological prior for an expressing cell is active: SIM1 is a dynamic nuclear bHLH-PAS transcription factor acting through ARNT-class partners, adult inducible neuronal deletion causes physiological and transcriptional changes within roughly one to two weeks, and the functional-stock adjudication therefore calls Sim1 function likely substantially depleted within the 21-28 day Perturb-seq interval.

That active prior is sharply limited by focal-population reach. The exact in-assay non-target expression measurement for `151 TH Prkcd Grin2c Glut` reports:

- `n_non_target_cells = 23679`
- `n_cells_expressing = 16`
- `pct_cells_expressing = 0.06757042104818616`
- `total_target_umi = 22`
- `mean_raw_umi = 0.0009290932894125596`
- `mean_log1p_cp10k = 0.00042323565914616977`
- `pseudobulk_cpm = 0.058229571127006906`

The source card independently points the same way: adult neural Sim1 expression is concentrated in hypothalamic neuroendocrine nuclei, with amygdala also reported, and adult thalamus has very low mouse bulk RNA plus no Allen ISH regional signal. In this task the exact focal expression measurement supersedes that qualitative context-reach evidence.

### Training endpoint distribution

The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` table contains 1,674 held-in biological targets. It is highly zero-inflated:

- 1,205 / 1,674 targets have `n_degs = 0`.
- Median `n_degs = 0`.
- 75th percentile `n_degs = 1`.
- 90th percentile `n_degs = 2`.
- 95th percentile `n_degs = 18`.
- 103 / 1,674 targets have `n_degs > 10`.

So the focal class commonly yields no FDR-significant genes even for assayed biological perturbations, and the sparse, non-expressed Sim1 case should start near the modal zero rather than the heavy right tail.

### Endpoint-matched PAS/ARNT comparators

Closest held-in PAS-family or ARNT-axis comparators in the training count table were all zero in this exact endpoint:

| target | held-in `n_degs` |
| --- | ---: |
| `Ahr` | 0 |
| `Ahrr` | 0 |
| `Arnt` | 0 |
| `Hif1a` | 0 |
| `Npas3` | 0 |

I compared their `151 TH Prkcd Grin2c Glut` Parquet profiles using `logfoldchanges` and the same `pvals_adj < 0.05` significance threshold. All five profiles were present, all five had `response_activity_status = no_significant_features`, and the cohort diagnostic had zero significant-program overlap in both positive and negative directions. This is the same experiment as the count table, not an independent replicate, but it checks that the selected biologically related zeros were also profile-flat rather than a shared subthreshold response module.

## Synthesis

The upward evidence is that Sim1 loss can deplete an active transcriptional regulator within the assay window in Sim1-dependent hypothalamic neurons. The downward evidence is more endpoint-specific: the requested thalamic class contains only 16 Sim1-detectable nuclei among 23,679 matched non-target nuclei, Sim1 has only 22 total UMIs in that population, regional priors place Sim1 outside adult thalamus, the held-in focal endpoint is already mostly zero, and the closest measured bHLH-PAS / ARNT-axis comparators are all zero-count and FDR-flat in this same class.

A rare Sim1-positive subpopulation could in principle respond, but at 0.0676% of the focal population it is too diluted to plausibly move a class-aggregated Wilcoxon DEG count. I therefore place the point forecast at the modal/no-response endpoint.

Predicted `n_degs`: 0
