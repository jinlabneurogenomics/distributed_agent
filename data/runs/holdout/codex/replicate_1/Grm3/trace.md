# Grm3 forecast for `151 TH Prkcd Grin2c Glut`

## Declared target and endpoint

- Target: `Grm3`, from the one-row holdout manifest.
- Endpoint: `n_degs`, the count of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05` in `151 TH Prkcd Grin2c Glut`.
- Same-experiment measurement sources used:
  - `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
  - `[local file: training_de_all_cell_groups.parquet]`
- Target-side source used: the declared endpoint-blind `Grm3` biology bundle via `reference.perturbation_characterization`.

The count table has 1,674 training perturbations and omits `Grm3`.

## Target biology

The canonical Grm3 bundle supports a real but likely muted perturbation in this endpoint:

- mGluR3 is a membrane class-C metabotropic glutamate GPCR coupled to Gi/o signaling and inhibition of adenylate cyclase.
- Postnatal neuron-restricted `Grm3` deletion has neuronal functional consequences, so this is not an inert target.
- By the 21-28 day harvest, the functional stock call is `partially_depleted_or_leading_edge`: editing stops new receptor production, but pre-existing surface and recycling receptor pools can persist, and the direct six-week postnatal deletion anchor is later and frontal-cortical rather than juvenile thalamic.
- Exact non-target expression in the assayed 151 population is low and sparse: 2,034 of 23,679 non-target nuclei express `Grm3` RNA, 8.59% of cells; pseudobulk abundance is 7.01 CPM and mean expression is 0.069 CP10K / 0.112 raw UMI.

Together these argue for low aggregate visibility: only a small fraction of the broad thalamic class is target-positive at baseline, the readout pools all class-assigned nuclei, and receptor stock may not be fully cleared within the experimental window.

## Training-count scale

The requested 151-class endpoint is extremely sparse in the declared training counts:

- 1,205 / 1,674 training targets have `n_degs = 0`.
- 1,481 / 1,674 have `n_degs <= 1`.
- 1,512 / 1,674 have `n_degs <= 2`.
- The mean, 14.05, is dominated by a small upper tail of broad regulators, with a median of 0 and a 95th percentile of 18.

I therefore did not use the global mean as the forecast for a restricted modulatory receptor.

The close group-II paralog `Grm2` was not present in the declared training table. Biology-chosen available metabotropic/cAMP/Gi receptor-signaling comparators in the 151-class table were:

| target | `n_degs` |
| --- | ---: |
| `Adcy1` | 0 |
| `Gnas` | 0 |
| `Grm5` | 0 |
| `Grm8` | 0 |
| `Gabbr1` | 1 |
| `Gabbr2` | 1 |
| `Gnao1` | 1 |
| `Grm1` | 1 |
| `Grm7` | 1 |
| `Grin1` | 89 |

The Parquet rows for the five one-DEG metabotropic/Gi anchors showed that each single significant call was the perturbed transcript itself:

| target | significant feature |
| --- | --- |
| `Gabbr1` | `Gabbr1` |
| `Gabbr2` | `Gabbr2` |
| `Gnao1` | `Gnao1` |
| `Grm1` | `Grm1` |
| `Grm7` | `Grm7` |

So the local analogue set had no FDR-significant downstream response in this population. `Grin1` supplied an upper contrast rather than a matched analogue: a core ionotropic NMDA receptor subunit produced 89 DEGs, but its immediate synaptic role and much broader downstream program are not good scale evidence for sparse mGluR3 loss.

## Point synthesis

`Grm3` has enough postnatal neuronal biology that a tiny signal is plausible, but three factors keep the point at the null edge:

- the exact in-assay RNA reach is only 8.59% of the broad 151 population;
- mGluR3 protein/receptor stock is expected to be only partially depleted at 21-28 days; and
- observed metabotropic/Gi receptor-signaling perturbations are 0 or self-only 1, with no downstream DEG among the local anchors checked in the Parquet.

Because the endpoint includes the perturbed gene itself, the only real ambiguity is whether `Grm3` self-transcript reduction would be called significant. Given its sparse baseline detection and the atlas-wide warning that measured target-mRNA loss is neither reliable nor proportional to functional editing, I put the integer point estimate just below the self-only analogue value:

`predicted_n_degs = 0`
