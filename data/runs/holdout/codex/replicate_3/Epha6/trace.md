# Trace

## Target and endpoint

- Target manifest: `Epha6`.
- Focal population: `151 TH Prkcd Grin2c Glut`.
- Endpoint: `n_degs`, the number of measured genes in this population with BH-adjusted Wilcoxon `p < 0.05`.

## Evidence used

- The declared canonical `Epha6` biology bundle reports strong focal expression in the exact non-target thalamic population: `mean_log1p_cp10k = 0.9457917937607313`, `mean_cp10k = 2.0962519499467884`, `n_cells_expressing = 18939 / 23679`, and `pct_cells_expressing = 79.98226276447485`. This made an assayed self-transcript effect possible rather than ruling the target out for lack of expression.
- The same bundle adjudicates EphA6 as a dynamic ephrin-A cell-surface receptor whose successful disruptive edit should stop new receptor supply; because a related Eph receptor has activation-dependent lysosomal clearance and the edit-to-harvest interval is 21-28 days, the bundle calls the functional stock "likely substantially depleted". It also records an important gap: no EphA6-specific protein half-life, surface-residence, post-edit persistence, or acute P16-to-P37/P44 thalamic response timing was found.
- The held-in training count table for the same population is highly zero-inflated. Among 1,674 training perturbations, 1,205 had `n_degs = 0`, the median was 0, the 75th percentile was 1, the 90th percentile was 2, and only 42 perturbations exceeded 100 DE genes.
- The represented Eph receptor perturbations in that count table were nearly all silent in `151 TH Prkcd Grin2c Glut`: `Epha10 = 0`, `Epha2 = 0`, `Epha3 = 0`, `Epha4 = 1`, `Epha5 = 0`, `Ephb1 = 0`, `Ephb2 = 0`, and `Ephb4 = 0`.
- A filtered scan of the declared training DE Parquet in the same population showed that the only significant `Epha4` row was the target transcript itself (`Epha4`, logFC -1.0266, adjusted p = 7.88e-32). The other represented Eph receptors above had no measured gene with adjusted `p < 0.05`; proximal represented signaling nodes were likewise quiet or self-only (`Fyn = 0`, `Ptpn11 = 0`, `Rac1 = 0`, `Mapk1 = 0`, `Cdc42 = 1` as self, `Pak1 = 1` as self, `Pak3 = 0`).
- Same-experiment Findings for the held-in Eph receptors support the quantitative pattern rather than an isolated table artifact. `Epha5:F003` reports high-confidence non-convergence among represented Eph-family comparators, and the corpus Claim `claim:2d52a03dd54eace8a29f` states with high confidence that single represented Eph receptors in postnatal neurons do not produce a common Eph-family nuclear transcriptomic program, instead showing flat or receptor-specific sparse effects.

## Synthesis

EphA6 is expressed and its surface receptor stock should be perturbable by the 21-28 day assay window, so I did not treat the target as a missing-function null. The endpoint, however, is a survivor-conditioned nuclear RNA DEG count, not spine morphology, phosphorylation, axon guidance, or electrophysiology. The biology bundle's affirmative phenotypes are adult germline cortical/behavioral phenotypes and expression reach; they do not provide an acute thalamic transcriptional timing anchor.

The most task-matched quantitative evidence was therefore the same-population behavior of held-in Eph receptors and proximal pathway nodes. Seven of eight represented Eph-family receptors had zero BH-significant genes in `151 TH Prkcd Grin2c Glut`; the eighth had only its own transcript significant. Packaged Findings independently summarize these perturbations as flat or singleton-only and non-convergent at the acute snRNA endpoint. That combination makes a broad downstream EphA6 RNA signature unlikely and leaves only a possible self-transcript hit. Because most assayed Eph receptors did not even show a significant self row in this population, the highest-probability integer is zero.

Predicted `n_degs`: **0**.
