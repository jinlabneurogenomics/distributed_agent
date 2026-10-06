# Atf2 prediction trace

## Endpoint and target

- Endpoint: `n_degs`, the number of measured genes in `151 TH Prkcd Grin2c Glut` with BH-adjusted Wilcoxon `pvals_adj < 0.05`.
- Target from the one-row holdout manifest: `Atf2`.
- Direct target outcome and target expression signature were not used; the quantitative training surfaces were the declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` count table and `training_de_all_cell_groups.parquet` expression parquet.

## Biology used

The canonical `Atf2` biology bundle supports target engagement but not a large postnatal thalamic response:

- Exact focal expression is available: `Atf2` is detected in 20,531 of 23,679 non-target nuclei in `151 TH Prkcd Grin2c Glut` (`86.7055%`, mean 2.365 raw UMI; pseudobulk 148.2 cpm). This says the target is expressed in the assayed population, not that perturbing it must move many downstream transcripts.
- ATF2 is a dynamic CRE/AP-1 bZIP transcription factor, not a long-lived structural stock; hours-scale turnover in source systems makes pre-edit ATF2 unlikely to persist for the 21-28 days between P16 editing and P37-P44 harvest.
- The strongest direct loss phenotype in the bundle is developmental and regional: neuron-specific mouse `Atf2` loss affects embryonic cranial motor neurons. The bundle leaves postnatal thalamic demand, response latency, and compensation by related AP-1/ATF factors unresolved.

## Training measurements used

I used the count table first to set the focal-cell response scale.

- Training targets in the focal count table: 1,674.
- Zero-count training targets: 1,205 / 1,674 = 71.98%.
- Quantiles of `n_degs`: median 0, 75th percentile 1, 90th percentile 2, 95th percentile 18, 97.5th percentile 100, 99th percentile 430.

I then selected training perturbations by molecular analogy to ATF2's AP-1/CRE bZIP transcription-factor role, restricted to available targets in the declared table:

| training target | `n_degs` in `151 TH Prkcd Grin2c Glut` | reason for use |
|---|---:|---|
| `Jund` | 0 | Jun-family AP-1 component, closer to ATF2's AP-1 dimer context than generic transcription factors |
| `Fosl2` | 0 | Fos-family AP-1 component |
| `Creb1` | 10 | CRE-binding bZIP transcription factor with a small observed local response |
| `Atf6` | 0 | ATF-family bZIP factor, but ER-stress rather than AP-1/CRE signaling |
| `Maf` | 0 | bZIP transcription factor |
| `Mafg` | 1 | small Maf bZIP transcription factor |
| `Nfe2l1` | 0 | CNC-bZIP transcription factor |
| `Nfe2l2` | 0 | CNC-bZIP transcription factor |

From the Parquet in the exact focal group, these eight selected training targets contributed 138,072 measured-gene rows, 17,259 per target. Only 11 rows were significant at `pvals_adj < 0.05`: 10 for `Creb1`, 1 for `Mafg`, and none for `Jund`, `Fosl2`, `Atf6`, `Maf`, `Nfe2l1`, or `Nfe2l2`.

The profile comparison over the same eight nodes confirmed that the small `Creb1` signal was not a reusable family-wide module: there were no pairwise overlaps in significant downregulated genes, and the only non-null overlap among significant upregulated programs was 0. Across all 28 cohort pairs, the mean positive top-tail overlap coefficient was 0.080 and the mean negative top-tail overlap coefficient was 0.130, so I treated the selected genes as a set of weak local analogs rather than one coherent expression program.

## Synthesis

The prediction is pinned close to zero for three reasons:

- The base rate in this exact neuronal class is sparse: 72% of training perturbations are zero and 90% have no more than 2 DEGs.
- The closest available AP-1/bZIP perturbations do not show a shared high-burden thalamic program; the median of the selected analog counts is 0 and the range is 0-10.
- ATF2 should be depleted by harvest, but the biology bundle does not establish that juvenile thalamic neurons require ATF2 basally enough to generate a large survivor-conditioned nuclear RNA signature. Its known stress/AP-1 activity could be silent under this postnatal, unstimulated assay condition, and the closest direct loss phenotype is embryonic motor-neuron degeneration rather than a matched P16 thalamic transcriptional effect.

I therefore forecast a focal `Atf2` response at the modal AP-1/bZIP training outcome rather than at the small `Creb1` outlier.

Predicted `n_degs`: **0**
