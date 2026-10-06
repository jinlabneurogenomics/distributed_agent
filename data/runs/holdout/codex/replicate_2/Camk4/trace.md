# Camk4 forecast for `151 TH Prkcd Grin2c Glut`

## Target biology used

- The one-row holdout target is `Camk4`.
- The canonical biology bundle reports that Camk4 is expressed in the exact focal non-target population: 20,002 of 23,679 nuclei express it, with 84.47% expressing cells and 2.465 mean raw UMIs in `151 TH Prkcd Grin2c Glut`.
- The bundle also supports functional reach by harvest: CAMK4 is a renewable monomeric Ca2+/calmodulin-dependent kinase, edits should stop new functional kinase supply, and the 21-28 day assay window spans many reported CAMK4 turnover times.
- The same bundle leaves endpoint coupling only partial: the mouse loss evidence is germline or from other neural contexts, and related CaM kinases plus parallel routes to CREB/activity-regulated transcription create plausible buffering in unstimulated postnatal thalamic nuclei.

## Training measurements used

The declared training table for the same class has 1,674 observed perturbations.

- 1,205 / 1,674 have `n_degs = 0`.
- Median `n_degs` is 0; the 90th percentile is 2; the 95th percentile is 18.
- The large right tail is dominated by core RNA/protein-homeostasis and chromatin regulators: the top training counts include `Uba5` 2677, `Tpr` 1768, `Sin3a` 1433, `Rnpc3` 868, `Zbtb7a` 841, and `U2af2` 828.

Calcium-, CREB-, synaptic-, and transcriptional-output comparators were much quieter in this same training table:

| Comparator set | Training `n_degs` in the focal class |
| --- | --- |
| CAMK2 family | `Camk2a` 0, `Camk2b` 1, `Camk2g` 0 |
| CAMK4 downstream transcription factors | `Creb1` 10, `Mef2c` 1, `Mef2d` 0, `Jund` 0, with `Rora` the high outlier at 278 |
| CaM/calcineurin/PKA/PKC/MAPK signaling | `Calm1` 14, `Calm2` 0, `Calm3` 1, `Ppp3ca` 4, `Ppp3cc` 0, `Prkaca` 1, `Prkca` 0, `Prkcg` 1, `Mapk1` 0 |
| NMDA and voltage-channel neighborhood | `Grin1` 89, `Grin2a` 1, `Grin2b` 2, `Cacna1a` 0, `Cacna1d` 0 |

I also compared 24 of those measured profiles directly in the declared Parquet, restricted to `151 TH Prkcd Grin2c Glut`, and wrote the run-local artifacts:

- `workbench/camk4_calcium_profile_compare.json`
- `workbench/camk4_calcium_profile_cohort.json`
- `workbench/camk4_anchor_profile_neighbors.json`

Within the 24-node cohort, 12 profiles had no FDR-significant genes, 8 had 1-9, 2 had 10-49, and only `Rora`/`Grin1` were at least 50. Cohort-level significant-program overlap was weak despite shared broad pathway placement, so I treated `Rora` and `Grin1` as high-side biological boundaries rather than scale-matched donors for a Camk4 kinase knockout.

## Forecast

High exact expression and likely CAMK4 stock depletion move the forecast above the screen median of zero. The strongest downward evidence is that direct calcium/CaM signaling perturbations and the proximal CREB/MEF2/JUN transcriptional outputs are mostly null or single-digit in the exact focal population, while the two higher activity-related examples are either a receptor core subunit (`Grin1`) or a direct nuclear receptor transcription factor (`Rora`) whose state is not a close operation match to losing the upstream CAMK4 kinase.

I therefore expect a detectable but small survivor-conditioned response in this focal class, closer to `Ppp3ca`/low `Creb1` than to `Rora` or `Grin1`.

Point prediction: `4` DEGs.
