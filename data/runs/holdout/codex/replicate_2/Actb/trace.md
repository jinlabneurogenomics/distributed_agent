# Direct Actb n_degs prediction

## Target and endpoint

- Target: `Actb`
- Cell class: `151 TH Prkcd Grin2c Glut`
- Endpoint: number of measured genes in this class with BH-adjusted Wilcoxon `p < 0.05`
- Prediction: `0`

The one-row holdout manifest and the canonical biology bundle both identify `Actb` as the held-out perturbation. The exact focal-population reach record reports that an `Actb` perturbation contrast is available in `151 TH Prkcd Grin2c Glut`, but `Actb` itself has `feature_available = false` with `feature_status = not_in_expression_matrix`; therefore any visible count has to come from downstream or compensatory measured genes rather than from an `Actb` self-transcript hit.

## Biology used

The prediction-safe biology bundle supports target engagement in principle but also argues for a buffered RNA phenotype in the recovered postnatal nuclei:

- a disruptive `Actb` edit should stop new beta-actin synthesis;
- beta-actin is a dynamic monomer/filament cytoskeletal pool and direct conditional-loss experiments show beta-actin protein can drop substantially within days, so successful edits should have cleared much of the pre-edit beta-actin by the P37-P44 harvest;
- other actin isoforms, especially `Actg1` and `Acta2`, rise after neural `Actb` loss and preserve much of total actin, so loss of the beta isoform is partly compensated;
- the strongest CNS phenotype evidence comes from developmental Nestin-Cre loss, not a P16-to-P37/P44 postmitotic thalamic edit, so it raises plausibility of an effect without implying a broad acute thalamic survivor-state transcriptome;
- survivor conditioning could attenuate observed single-nucleus differential expression if the most affected edited neurons were depleted before recovery.

## Training-scale evidence

The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` table is strongly zero-inflated:

- 1,674 training perturbations;
- 1,205 with `n_degs = 0`;
- median `0`;
- 75th percentile `1`;
- 90th percentile `2`;
- 95th percentile `18`.

The local training perturbations most directly tied to actin or nearby cytoskeletal structure had minimal burdens:

| perturbation | n_degs |
|---|---:|
| `Actg1` | 1 |
| `Actn4` | 0 |
| `Tpm3` | 0 |
| `Add1` | 0 |
| `Add2` | 0 |
| `Add3` | 0 |
| `Tubb4b` | 1 |
| `Tubb5` | 1 |
| `Tuba4a` | 2 |
| `Tuba1a` | 7 |
| `Dnm1` | 1 |
| `Map1b` | 1 |
| `Mapt` | 1 |

In the focal-cell Parquet slice, the single significant `Actg1` feature was the self transcript:

| perturbation | significant measured gene | logFC | p_adj |
|---|---|---:|---:|
| `Actg1` | `Actg1` | -0.824 | 9.85e-16 |

The measured cytoskeletal compensators were not induced after the `Actg1` edit in this cell class: `Acta2` stayed nonsignificant after pseudocount-driven dropout-like values, and `Tuba1a`, `Tuba4a`, `Tubb3`, and `Tubb5` all had adjusted p-values of `1.0`. The tubulin perturbations mostly showed self-loss plus limited tubulin-family compensation rather than a large generic cytoskeletal stress program.

I also projected `Actg1`, `Actn4`, `Tpm3`, `Tuba1a`, `Tuba4a`, and `Tubb5` into the complete 1,674-node training universe using the declared Parquet log-fold-change profiles for `151 TH Prkcd Grin2c Glut`. These anchors had 0, 1, 2, or 7 significant features and their nearest-neighbor overlaps were weak and nonspecific: top-50 signed-feature overlaps for `Actg1` were at most 0.22 on the negative side and 0.14 on the positive side, with nearest profile neighbors almost all at `n_degs <= 1`. That supported treating the direct `Actg1` measurement and the hand-picked cytoskeletal counts as low-count scale anchors rather than as evidence for a hidden high-DEG actin state.

## Synthesis

`Actb` is likely functionally perturbed over the experimental interval, so I did not forecast a null because of absent biology. The decisive downward adjustments were endpoint-specific:

- the closest measured analogue, `Actg1`, produced only a self-transcript hit in this cell class;
- the `Actb` self transcript cannot contribute to `n_degs` because it is absent from the expression matrix;
- partial isoactin buffering makes a large survivor RNA state less likely than the developmental neural phenotype might imply;
- most broader cytoskeletal perturbations in the declared training table were measured as 0-2 DEGs.

I therefore placed `Actb` below `Actg1`'s observed count of 1 and used `0` as the point prediction for the measured downstream DEG count.
