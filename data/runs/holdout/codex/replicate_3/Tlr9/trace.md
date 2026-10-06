# Direct forecast for `Tlr9`

Endpoint: number of measured genes in `151 TH Prkcd Grin2c Glut` with BH-adjusted Wilcoxon `p < 0.05`.

## Evidence used

### Canonical `Tlr9` biology and reach

- The declared one-row holdout manifest names `Tlr9`.
- The canonical biology bundle describes TLR9 as an endolysosomal CpG DNA receptor that traffics from ER to endolysosomes and signals through its cleaved, MyD88-recruiting pool. The functional-stock card favors substantial depletion by the P37-P44 harvest after a disruptive P16 edit, but only with partial, out-of-region timing evidence.
- TLR9 has postnatal neuronal evidence in adult hippocampal CA1 neurons and germline neural behavioral evidence, so I did not treat it as biologically inert in all neurons.
- The exact focal-population expression reach is the dominant context evidence for this endpoint: in non-target nuclei from `151 TH Prkcd Grin2c Glut`, `Tlr9` had only 35 UMIs across 23,679 nuclei, 35 expressing nuclei, `0.147810296%` of nuclei expressing, mean raw UMI `0.001478103`, mean CP10K `0.001019532`, and pseudobulk CPM `0.092637954`. The bundle explicitly states that this exact in-assay expression supersedes broader qualitative target-presence estimates.

### Declared training counts

- The declared class-matched count table has 1,674 held-in perturbations. Its distribution is zero-heavy: 1,205/1,674 targets have `n_degs = 0`, the median is 0, the 75th percentile is 1, the 90th percentile is 2, the 95th percentile is 18, and the mean is pulled up to 14.05 by a small set of very large essential or regulatory footprints.
- The biologically nearest measured Toll-like receptors in this training set are all silent in the target class:

| target | n_degs |
| --- | ---: |
| `Tlr2` | 0 |
| `Tlr3` | 0 |
| `Tlr4` | 0 |
| `Tlr5` | 0 |
| `Tlr7` | 0 |
| `Tlr8` | 0 |

- Immediate or downstream innate-signaling comparators that were available in the same count table were also silent:

| target | n_degs |
| --- | ---: |
| `Chuk` | 0 |
| `Irf1` | 0 |
| `Irf2` | 0 |
| `Irf3` | 0 |
| `Irf5` | 0 |
| `Irf8` | 0 |
| `Irf9` | 0 |
| `Nfkb1` | 0 |
| `Traf3` | 0 |

### Expression Parquet spot check

I checked the declared `training_de_all_cell_groups.parquet` in the exact `151 TH Prkcd Grin2c Glut` context for the same TLR-family and innate-signaling comparators. Each comparator had 17,259 measured feature rows in this class and zero rows with `pvals_adj < 0.05`; even the best adjusted p-value among the checked set was nonsignificant. This confirmed that the zero counts above were not hiding a near-threshold common TLR program in the full measured-gene table.

## Synthesis

`Tlr9` has a plausible acute loss-of-function operation over the 21-28 day experimental window, and TLR9 can matter in postnatal neurons outside this thalamic population. For this exact endpoint, the more decisive facts are that the assayed `151 TH Prkcd Grin2c Glut` population almost never expresses `Tlr9`, and every held-in Toll-like receptor plus the available NF-kB/IRF signaling comparators produced zero BH-significant genes in the same focal class. The focal reach is too small to expect a detectable survivor-conditioned bulk transcriptional state from sparse mosaic CRISPR in these thalamic neurons.

Prediction: `0` DEGs.
