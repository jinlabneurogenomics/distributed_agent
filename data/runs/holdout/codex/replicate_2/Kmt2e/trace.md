# Direct forecast for Kmt2e

## Target biology

- The one-row holdout manifest names `Kmt2e`; the prediction is `n_degs` for `151 TH Prkcd Grin2c Glut` at BH-adjusted Wilcoxon `p < 0.05`.
- The declared `Kmt2e` biology bundle is endpoint-blind. Its exact in-assay reach shows the target transcript is readily observable in this class: 20,409/23,679 non-target nuclei express `Kmt2e` (`86.1903%`), with mean CP10k `1.4834` and pseudobulk CPM `144.714`.
- The functional-stock card favors actual loss of KMT2E by the P37-P44 harvest, but only with partial evidence: KMT2E is a dynamic chromatin-associated H3K4me3 reader/transcriptional regulator, not a durable installed catalytic mark; generic brain-proteome kinetics make 21-28 day depletion plausible, while a target-specific neuronal half-life was not found and an OGT/USP7-stabilized residual pool is unresolved.
- The prior phenotype evidence is developmental rather than acute thalamic/postmitotic, and the closest named related protein, SETD5, has no demonstrated acute thalamic-neuron compensation or phenocopy with KMT2E.

## Training measurements used

- The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` has 1,674 training targets and no `Kmt2e`. It is very sparse: 1,205/1,674 targets have `n_degs = 0`; the quartiles are 0, 0, and 1; the 95th percentile is 18; and a few generic high-visibility perturbations run far higher, up to 2,677.
- I used chromatin and H3K4-axis perturbations rather than the high-count generic outliers as the main numerical comparators. In the same count table, `Setd5 = 9`, `Kmt2a = 24`, `Arid1a = 22`, `Kdm5c = 18`, `Crebbp = 8`, `Ehmt1 = 4`, `Ash1l = 1`, `Setd2 = 1`, `Arid1b = 1`, and `Kmt2c`, `Ep300`, `Kat6a`, `Kat6b`, `Smarca4`, `Smarcc1`, and `Mbd5` are all 0. The closest corpus-supported Setd5 module neighbor `Ankrd11` has 20.
- A direct Parquet slice of 19 selected chromatin comparators in `151 TH Prkcd Grin2c Glut` gave 17,259 measured genes per perturbation and reproduced the count-table values exactly for this FDR < 0.05 endpoint.
- Same-experiment report context for `Setd5` describes its acute P16 postmitotic signature as localized and TH-dominant rather than a broad chromatin-fidelity collapse. Same-experiment report context for `Kmt2a` says H3K4-axis perturbations were not interchangeable: `Kmt2a` was sparse, `Setd1a` was broad, and `Kmt2c` was almost flat.
- In the compact profile comparison among those hand-selected chromatin comparators, `Setd5` shared no FDR-significant same-direction genes with `Kmt2a`, `Kdm5c`, `Crebbp`, `Setd1a`, `Chd8`, `Ash1l`, `Kmt2c`, or `Setd2`, and only one with `Arid1a`. I therefore treated the measured chromatin counts as a response-scale prior, not as one coherent module to average or inherit.

## Synthesis

`Kmt2e` has sufficient target reach and should lose at least some renewable KMT2E protein by harvest, so a strict zero forecast is too low. The missing acute thalamic phenotype, noncatalytic reader biology, low-confidence residual-stock issue, and flat/modest H3K4-family comparators argue strongly against the broad `Setd1a`/`Chd8` tail. I placed `Kmt2e` just below the closest positive comparator `Setd5` and near the low single-to-low double digit chromatin range.

Predicted `n_degs`: **8**
