# Direct forecast for `151 TH Prkcd Grin2c Glut`

## Target and endpoint

- Target perturbation: `Sim1`.
- Focal population: `151 TH Prkcd Grin2c Glut`.
- Endpoint: `n_degs`, the number of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05` in the focal class.
- Declared target context used here: the one-row `Sim1.csv` holdout manifest, the biology-only `Sim1.json` bundle, the `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` training count table, and filtered rows from `training_de_all_cell_groups.parquet`.

## Evidence used

### Exact focal expression reach

The declared biology bundle reports that Sim1 was almost absent in matched non-target nuclei for `151 TH Prkcd Grin2c Glut`:

- `n_non_target_cells`: 23,679
- `n_cells_expressing`: 16
- `pct_cells_expressing`: 0.067570421%
- `total_target_umi`: 22
- `total_non_target_rna_umi`: 377,814,907
- `pseudobulk_cpm`: 0.058229571
- `mean_raw_umi`: 0.000929093
- `mean_log1p_cp10k`: 0.000423236

The same bundle adjudicates the perturbation as biologically realizable where Sim1 is actually active: SIM1 is a dynamic nuclear bHLH-PAS transcription factor, adult neuronal Sim1 inactivation can produce transcriptional and physiological changes within about two weeks, and functional stock should likely be substantially depleted by the P37-P44 harvest interval after a P16 edit. The context limiter is therefore not persistence of a long-lived protein pool; it is the near-absence of the transcript in the assayed thalamic focal population. The source card also noted that known adult neural Sim1 expression is concentrated in hypothalamic neuroendocrine nuclei and amygdala, with very low or undetected adult thalamic expression at regional resolution.

### Training-count base rate

The declared focal count table contains 1,674 measured training perturbations. Its distribution is strongly concentrated at zero:

- `n_degs = 0`: 1,205 / 1,674
- nonzero: 469 / 1,674
- median: 0
- 75th percentile: 1
- 90th percentile: 2
- 95th percentile: 18
- mean: 14.05, inflated by a small set of high-response outliers

That base rate already favors a zero or one-count forecast for an unexpressed or barely expressed target in this class.

### Typed Sim1 analogs available in training

I nominated training-available Sim1 analogs from the curated mouse annotation store and selected same-experiment corpus release. The strongest specific available analog was `Arnt`, a native mouse CORUM member of the `Arnt-Sim1 complex` and a STRING physical interactor. The other top bHLH/PAS-related available analogs were broader functional fallbacks rather than exact Sim1 partners.

For the focal class, the declared count table and matching Parquet rows gave:

| comparator | relationship to Sim1 | `151 TH Prkcd Grin2c Glut n_degs` |
| --- | --- | ---: |
| `Arnt` | exact Arnt-Sim1 complex; STRING physical interaction | 0 |
| `Ahr` | bHLH/PAS-family transcriptional regulator, broad fallback | 0 |
| `Hif1a` | bHLH/PAS-family transcriptional regulator, broad fallback | 0 |
| `Npas3` | bHLH/PAS-family transcriptional regulator, broad fallback | 0 |
| `Mlxip` | broader dimeric transcriptional regulator | 0 |
| `Clock` | circadian bHLH/PAS-family regulator | 3 |
| `Cry1` | clock pathway | 1 |
| `Cry2` | clock pathway | 3 |
| `Bmal1` | circadian bHLH/PAS-family regulator | 103 |

The filtered Parquet query returned one full measured-gene row set per listed comparator in the focal class. `Arnt`, `Ahr`, `Hif1a`, `Npas3`, and `Mlxip` had zero rows with `pvals_adj < 0.05`. `Clock`, `Cry1`, and `Cry2` had only one to three significant rows. `Bmal1` was the clear outlier among these comparators; its leading significant genes were circadian outputs such as `Dbp`, `Nr1d1`, `Nr1d2`, and `Cry1`, so I treated it as a clock-state perturbation rather than as a quantitative proxy for sparsely expressed Sim1.

Among the first 30 typed nominees, 25 had `n_degs = 0`; the exceptions were `Smad2` and `Fbxo11` at 1, `Crebbp` at 8, and the high-count outliers `Bmal1` at 103 and `Ctnnb1` at 383. A same-corpus topology audit of the top 20 nominees placed `Ahr`, `Arnt`, `Hif1a`, and `Bmal1` in one explicit-reference component, but only the clock gene `Bmal1` carried a large 151-class burden; the three PAS comparators closest to Sim1/ARNT biology were all zero.

## Synthesis

A functional Sim1 edit should matter in a Sim1-maintained hypothalamic neuron, but the focal thalamic population had only 16 Sim1-detecting nuclei among 23,679 matched non-target nuclei and 22 Sim1 UMIs total. With such low reach, even complete functional loss in the rare expressing nuclei is unlikely to generate a coherent BH-significant survivor-conditioned bulk shift across 17,259 measured focal rows. The focal training distribution is mostly zero, and the available exact/near bHLH-PAS comparators were also zero in this class.

I therefore forecast the held-out `Sim1` perturbation at the floor:

`predicted_n_degs = 0`
