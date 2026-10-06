# Foxj1 forecast trace

## Target and endpoint

- Target from the declared one-row holdout manifest: `Foxj1`.
- Cell class: `151 TH Prkcd Grin2c Glut`.
- Endpoint: `n_degs`, the number of measured genes with BH-adjusted Wilcoxon `p < 0.05` in this class.
- The declared target is absent from the `151 TH Prkcd Grin2c Glut` training count table, as expected for the holdout.

## Evidence that set the scale

The biology bundle supports real Foxj1 loss of function within the experimental window but in the wrong principal cell type for this readout. Foxj1 is a motile-ciliogenesis transcription factor required to maintain mature multiciliated ependymal identity, Foxj1 protein turns over rapidly, and P14 inducible loss in mature ependyma produced a phenotype by P28. That argues against long-lived functional stock shielding truly Foxj1-dependent cells at P37-P44.

The same bundle reports exact focal expression in the assayed thalamic neuronal population:

- `n_non_target_cells = 23679`
- `n_cells_expressing = 718`
- `pct_cells_expressing = 3.0322226445373537`
- `mean_cp10k = 0.02090257146304476`
- `mean_raw_umi = 0.032940580260990754`
- `total_target_umi = 780`

That very small reach was the dominant reason to keep the expected `151` response at the floor despite the strong ependymal Foxj1 prior.

The declared training count table for `151 TH Prkcd Grin2c Glut` is itself highly zero-inflated:

- 1,674 training perturbations
- 1,205 with `n_degs = 0`
- median `n_degs = 0`
- 75th percentile `n_degs = 1`
- mean `n_degs = 14.054`, reflecting a small set of very large responses

## Training perturbations interpreted

I used biologically close measured genes, rather than table rank, to check how much the thalamic count table moved for out-of-context FOX/ciliary perturbations.

Available FOX-family perturbations in the training count table were all null in `151`:

| target | n_degs |
|---|---:|
| Foxa2 | 0 |
| Foxc2 | 0 |
| Foxe3 | 0 |
| Foxi1 | 0 |
| Foxj3 | 0 |
| Foxk2 | 0 |
| Foxl1 | 0 |
| Foxl2 | 0 |
| Foxn1 | 0 |
| Foxp2 | 0 |
| Foxp3 | 0 |

Cilia and centriole-related training perturbations were also essentially at the floor:

| target | n_degs |
|---|---:|
| Adcy3 | 0 |
| Alms1 | 0 |
| Arl3 | 1 |
| B9d1 | 0 |
| Bbs5 | 0 |
| Cep290 | 0 |
| Ift43 | 0 |
| Ift81 | 0 |
| Ift88 | 0 |
| Rpgrip1l | 0 |
| Trp73 | 0 |
| Ttc21b | 0 |
| Ttc8 | 1 |
| Ttll5 | 0 |

I then projected 27 FOX/ciliary/regulatory training perturbations from the declared parquet in the matched `151 TH Prkcd Grin2c Glut` context. The measured profile comparison found all 27 profiles present; 25 had no adjusted-significant measured genes and only 2 fell into the `1_to_9_significant_features` activity bin. The cohort diagnostic over all 351 pairs showed no recurrent significant program: significant-program overlap was absent except for one zero-overlap entry, and the mean positive top-tail overlap coefficient was only 0.073.

## Synthesis

Foxj1 would be an effective 3-4 week perturbation in Foxj1-expressing multiciliated cells, but the requested endpoint samples recovered thalamic NeuN-positive neuronal nuclei where native Foxj1 RNA is detected in only a small minority of cells at extremely low abundance. In the same high-yield cell class, the measured FOX-family and ciliary training perturbations most related to Foxj1 were almost uniformly `0`, with no coherent subthreshold state in their expression profiles to justify inflating the estimate above the floor.

My point forecast is therefore the modal and biology-supported floor outcome:

`predicted_n_degs = 0`
