# Kmt2b direct DEG-count forecast

## Target and endpoint

- Target: `Kmt2b`, the single row in the declared holdout manifest.
- Endpoint: `n_degs` in `151 TH Prkcd Grin2c Glut`, counted as measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`.
- The prediction uses the one-row Kmt2b biology bundle, the training count table for this cell class, and measured training profiles from `training_de_all_cell_groups.parquet`; the Kmt2b perturbation profile and Kmt2b endpoint were not used.

## Biology of Kmt2b in the assay window

- The exact focal-population reach is strong: `Kmt2b` was detected in 19,448 of 23,679 non-target nuclei in `151 TH Prkcd Grin2c Glut` (82.13%), with mean raw UMI 1.995 and pseudobulk CPM 125.03. This supports expression reach in the assayed thalamic glutamatergic nuclei, but only as reach; the dataset portrait warns that target-transcript abundance or self-knockdown should not be converted into editing efficiency.
- The biology bundle assigns KMT2B to promoter H3K4me2/H3K4me3 support in neuronal genes. Postnatal forebrain excitatory-neuron Kmt2b loss caused functional hippocampal phenotypes in mouse, and the Kmt2b phenotype occurred despite Kmt2a/Kmt2c family expression, so complete paralog buffering is unlikely.
- The same bundle also makes the acute P16-to-P37/P44 timing a major downward modifier. A disruptive edit stops new KMT2B production but does not immediately erase existing KMT2B protein or pre-existing H3K4-methylated histones; more than 30% H3.3 turnover over four weeks gives a real renewal front, but no direct KMT2B half-life makes complete stock depletion by 21-28 days unsupported. I therefore treated Kmt2b as reachable and plausibly nonzero, not as an immediate broad chromatin collapse.

## Training measurements that set the count scale

- The supplied focal count table has 1,674 training perturbations. It is zero-heavy: 1,205 have `n_degs = 0`, 469 are nonzero, 106 have at least 10 DEGs, 43 have at least 100 DEGs, the median is 0, the 75th percentile is 1, the 95th percentile is 18, and the 99th percentile is about 430.
- The closest measured H3K4/Trithorax-side entries are sparse or heterogeneous:

| perturbation | focal `n_degs` | matched perturbed nuclei |
| --- | ---: | ---: |
| `Kmt2c` | 0 | 55 |
| `Ash1l` | 1 | 130 |
| `Ogt` | 4 | 71 |
| `Kmt2a` | 24 | 161 |
| `Setd1a` | 368 | 154 |

- `Kmt2a` is the most relevant measured paralog-scale anchor: it had 24 focal DEGs at BH < 0.05, split evenly between 12 up- and 12 down-regulated significant genes in the profile inspection. The same-experiment corpus describes this as a sparse, glutamatergic-biased Kmt2a response with its clearest positive biology in `151 TH Prkcd Grin2c Glut`.
- `Kmt2c` and `Ash1l` are boundary evidence that chromatin-writer or Trithorax-family membership alone does not guarantee a detectable P16 postmitotic signature.
- `Setd1a` is response-capable in the exact same cell class, but it is not a clean magnitude donor for Kmt2b: its 368-DEG focal signature was dominated by down-regulated organelle-maintenance programs, and direct profile inspection of the H3K4-side cohort found only one same-direction BH < 0.05 intersection between `Kmt2a` and `Setd1a`. The corpus likewise places Setd1a away from other represented KMT2-family writers and toward RNA-biogenesis / organelle-maintenance states.

## Synthesis

I placed `Kmt2b` above the all-target median/zero mass because it is expressed in most focal nuclei and has direct postnatal neuronal loss-of-function evidence. I did not transfer the broad `Setd1a` count, because the KMT2A/KMT2C/SETD1A comparisons show target-specific H3K4-family footprints rather than a shared family-wide module. The best scale anchor is the sparse `Kmt2a` thalamic program at 24 DEGs, with a downward adjustment for KMT2B's unresolved protein/mark persistence across only 21-28 days.

Predicted `n_degs`: 18.
