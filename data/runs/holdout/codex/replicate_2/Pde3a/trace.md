# Pde3a DEG-count forecast

## Target and endpoint

- Target: `Pde3a`
- Focal population: `151 TH Prkcd Grin2c Glut`
- Endpoint: number of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`
- The target perturbation was absent from the training count table and from `training_de_all_cell_groups.parquet`; I used only the biology-only `Pde3a` bundle plus training perturbations.

## Biology prior

The exact in-assay reach for `Pde3a` in `151 TH Prkcd Grin2c Glut` is very low:

- 671 / 23,679 non-target nuclei expressed `Pde3a`
- `pct_cells_expressing = 2.8337`
- `mean_cp10k = 0.0231`
- `mean_raw_umi = 0.0384`
- `pseudobulk_cpm = 2.4059`

The biology bundle supports a weakly observable, not high-penetrance, perturbation in this assay. `Pde3a` encodes the PDE3A cyclic-nucleotide phosphodiesterase, so a disruptive edit should stop synthesis of new catalytic enzyme. The operative pre-edit PDE3A protein could still persist until degraded, however, and the available rapid-turnover fact is from stressed cardiomyocytes rather than basal juvenile thalamic neurons. The source card did not contain a postnatal thalamic-neuron loss phenotype or a compensation test for the related PDE3 paralog `Pde3b`.

That leaves room for a focal cAMP/cGMP effect, but the exact focal-population expression argues that only a small minority of the assayed class should have direct target reach.

## Training comparators

The 151 TH training count table contains 1,674 perturbations. Its count distribution is sparse:

- 1,205 / 1,674 perturbations have `n_degs = 0`
- median = 0
- 75th percentile = 1
- 90th percentile = 2
- mean = 14.05, inflated by a small long tail of high-count chromatin, proteostasis, and RNA-processing perturbations

Typed annotation-based nomination recovered four training-available phosphodiesterase comparators as the closest direct enzyme class for `Pde3a`:

| comparator | relationship evidence | 151 TH `n_degs` |
|---|---|---:|
| `Pde10a` | cyclic-nucleotide and 3',5'-cyclic-AMP phosphodiesterase activity | 0 |
| `Pde4d` | cyclic-nucleotide and 3',5'-cyclic-AMP phosphodiesterase activity | 0 |
| `Pde4b` | 3',5'-cyclic-AMP and 3',5'-cyclic-nucleotide phosphodiesterase activity | 0 |
| `Pde1c` | 3',5'-cyclic-AMP and 3',5'-cyclic-nucleotide phosphodiesterase activity | 0 |

I recomputed those rows directly from the declared Parquet in the exact focal cell class. Each had 17,259 measured genes, and the smallest adjusted p-values were still nonsignificant:

| comparator | matched perturbed nuclei | matched controls | recomputed `n_degs` | min `pvals_adj` |
|---|---:|---:|---:|---:|
| `Pde10a` | 191 | 23,679 | 0 | 0.304 |
| `Pde4d` | 192 | 23,679 | 0 | 1.000 |
| `Pde4b` | 211 | 23,679 | 0 | 0.922 |
| `Pde1c` | 155 | 23,679 | 0 | 0.180 |

The broader cAMP/cGMP-adjacent pathway was also quiet in the focal count table:

| comparator | role | 151 TH `n_degs` |
|---|---|---:|
| `Gnas` | Gs signaling into adenylyl cyclase | 0 |
| `Adcy1` | adenylyl cyclase | 0 |
| `Adcy3` | adenylyl cyclase | 0 |
| `Adcy5` | adenylyl cyclase | 0 |
| `Plcb1` | phosphodiesterase superfamily / receptor calcium signaling | 0 |
| `Prkar1a` | PKA regulatory subunit | 1 |
| `Prkaca` | PKA catalytic subunit | 1 |
| `Creb1` | downstream cAMP-response transcription factor, broad transcriptional node | 10 |

`Calm1` was the only training-available nominated comparator with an exact complex-level relationship, via a projected human CORUM `CALM1-PDE1A-PDE3A` complex, and it had 14 DEGs. I treated it as weaker quantitative evidence for `Pde3a` than the PDE-family enzyme perturbations because it is a broad calcium sensor rather than a PDE3-family cyclic-nucleotide-degrading enzyme.

## Synthesis

The best task-matched evidence points to a null or near-null footprint:

- `Pde3a` has very sparse exact focal expression.
- The only closely source-like measured PDE perturbations all have 0 DEGs in the same cell class.
- Neighboring adenylyl-cyclase and PKA perturbations are also 0-1 DEGs, with only broader downstream transcriptional/calcium hubs reaching 10-14.
- The biology bundle does not establish full PDE3A protein depletion in the P16-to-P37/P44 window.

An idiosyncratic single-gene or very low single-digit response remains plausible, but the strongest point prediction is at the modal local value and the direct PDE comparator value.

Predicted `n_degs`: 0
