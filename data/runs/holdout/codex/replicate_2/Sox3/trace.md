# Direct forecast for Sox3 in `151 TH Prkcd Grin2c Glut`

## Target and endpoint

- Target manifest: `Sox3`.
- Endpoint: `n_degs`, the number of measured genes in `151 TH Prkcd Grin2c Glut` with BH-adjusted Wilcoxon `pvals_adj < 0.05`.
- Declared measured endpoint sources:
  - `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
  - `[local file: training_de_all_cell_groups.parquet]`
- The training count table contained 1,674 perturbations and no `Sox3` row, so the predicted value below is not read from a Sox3 outcome.

## Evidence that drove the prediction

### Sox3 biology and focal reach

The declared Sox3 biology bundle reports exact baseline reach in the same focal population:

- `521 / 23679` non-target nuclei expressed `Sox3`, i.e. `2.2002618353815615%`.
- Mean focal expression was `0.023903036445795854` raw UMI per nucleus, `0.014972383773357429` CP10K, or `1.4980880571766322` pseudobulk CPM.

That is the dominant downward bearing. Only a small minority of recovered thalamic glutamatergic nuclei have detectable target RNA, so even a biologically real edit has little room to produce a large population-averaged survivor transcriptome in this aggregated class.

The same endpoint-blind bundle adjudicates SOX3 as a nuclear HMG-box SOXB1 transcription factor. A disruptive edit should stop new functional SOX3 supply, but no target-specific SOX3 half-life, residence-time, conditional-deletion clearance, or acute postmitotic-neuronal clearance measurement was located. The best mouse loss evidence is developmental ventral-diencephalic / hypothalamo-pituitary biology rather than an acute P16-to-P37/P44 thalamic requirement. Engineered Sox2 expression from the Sox3 locus can substitute for Sox3 during mouse development, which leaves open buffering by related factors but does not prove natural compensation in this assay. Altogether, the card supports possible functional engagement but gives no reason to override the weak focal reach with a large expected DEG burden.

### Training count scale

The focal-class training count table is zero-inflated:

- 1,205 / 1,674 training perturbations had `n_degs = 0`.
- 1,481 / 1,674 had `n_degs <= 1`.
- 1,674 median = 0; 75th percentile = 1; 90th percentile = 2; 95th percentile = 18.

Thus a biologically unconstrained draw is already most likely to be 0 or 1; Sox3's very low thalamic reach shifts the point toward the zero side rather than toward the rare high-count tail.

### Sox-family training analogues

The available Sox-family perturbations in the same count table were:

| perturbation | n_degs |
| --- | ---: |
| Sox2 | 2 |
| Sox4 | 0 |
| Sox5 | 2 |
| Sox9 | 0 |
| Sox10 | 0 |
| Sox11 | 0 |
| Sox17 | 0 |
| Sox18 | 0 |

The corresponding focal-class Parquet rows confirmed that only `Sox2` and `Sox5` had any BH-significant genes:

| perturbation | BH-significant genes |
| --- | --- |
| Sox2 | `Tnnt1`, `Stam`, both lower after perturbation |
| Sox5 | `Dgkh`, `Tnnt1`, both higher after perturbation |

So the closest named family evidence is not a coherent positive response module: 6 of 8 Sox-family training perturbations were null, the two non-null ones were only two genes each, and their only repeated significant feature (`Tnnt1`) flipped direction.

### Sox2 measured-profile neighborhood

Because Sox2 is the direct SOXB1 family analogue available in training, I projected `Sox2` against all 1,674 declared training perturbations in the same Parquet/context. Among the 80 unique top-10 neighbors emitted across whole-profile and signed-tail views:

- 64 had `n_degs = 0`.
- 78 had `n_degs <= 2`.
- Only one high-count outlier appeared (`Elp2`, `150`), and it entered through the very small positive 0.1% tail view rather than through whole-profile similarity.
- The top whole-profile Pearson/cosine neighbors were all `0` or `1` DEG.

This kept the Sox2-local empirical expectation close to null and made the `Sox2 = 2` count look like a small upper analogue rather than a lower bound for Sox3.

## Synthesis

`Sox3` has a transcription-factor mechanism, but the assayed focal class contains very little detectable target transcript and the prior mouse phenotypes are developmental rather than an acute postnatal thalamic program. The most relevant training family is quiet in this endpoint, and the strongest direct paralogue, `Sox2`, produces only two significant features with a low-count local profile neighborhood. I therefore place Sox3 at the modal quiet outcome for this class rather than at the two-gene Sox2 value.

Predicted `n_degs`: **0**
