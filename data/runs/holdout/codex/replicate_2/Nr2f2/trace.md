# Nr2f2 DEG-count forecast

## Endpoint

- Target: `Nr2f2`
- Cell class: `151 TH Prkcd Grin2c Glut`
- Endpoint: number of measured genes in this cell class with Wilcoxon BH-adjusted `p < 0.05`
- Prediction: `2`

## Evidence used

### Declared target biology

The canonical `Nr2f2` biology bundle supports real focal reach but uncertain acute realization.

- Exact focal expression in non-target cells was available: `Nr2f2` was detected in 12,024 of 23,679 nuclei, `50.779%`, with mean CP10k `0.71397`, mean log1p(CP10k) `0.41288`, and pseudobulk CPM `74.817`.
- NR2F2 is a DNA-binding nuclear-receptor transcription factor; an effective CRISPR lesion should stop synthesis of new functional receptor and can in principle change cis-regulatory control.
- The functional-stock adjudication was unresolved: pre-existing receptor can remain active until cleared, but no mouse-neuron NR2F2 half-life or post-edit depletion clock was found, so functional loss by P37-P44 after a P16 edit is indeterminate.
- The direct mouse neural loss evidence is developmental cerebellar or hippocampal conditional deletion, not temporally matched acute loss in postmitotic juvenile thalamic neurons.

### Training endpoint scale

The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` table contains 1,674 training perturbations and excludes `Nr2f2`.

- The endpoint is highly zero-inflated: 1,205/1,674 training targets had `0` DEGs.
- The median was `0`, the 75th percentile was `1`, the 90th percentile was `2`, and the 95th percentile was `18`.
- Only 43/1,674 training targets reached at least 100 DEGs.

This makes the global mean of `14.05` a poor prior for an ordinary transcription factor or nuclear receptor because it is driven by a small tail of proteostasis, spliceosome, chromatin, and special cell-state hits.

### Nuclear-receptor comparators

I used the deterministic closed-universe annotation store to form target-side cohorts and then measured their actual 151-class DEG counts from the declared count table and training Parquet.

GO `nuclear receptor activity` contributed 49 present training targets after excluding held-out `Nr2f2`, `Nr1h3`, `Nr4a2`, and `Rara`:

- 42/49 had `0` DEGs.
- Median was `0`; the 75th percentile was `0`; the 90th percentile was `2.2`.
- The only large or moderate 151 responders were `Rora` with 278 DEGs, `Nr1d1` with 116, and `Esrra` with 57.

The curated WikiPathways nuclear-receptor set was similarly sparse:

- 33 training targets were present.
- 27/33 had `0` DEGs.
- The nonzero tail was `Rora` 278, `Esrra` 57, `Thra` 3, `Nr2c2` 3, `Nr2f1` 2, and `Nr1d2` 1.

The closest measured NR2-family comparators were tiny:

| comparator | 151-class DEGs |
|---|---:|
| `Nr2f1` | 2 |
| `Nr2f6` | 0 |
| `Nr2c2` | 3 |
| `Nr2c1` | 0 |
| `Nr2e1` | 0 |
| `Nr2e3` | 0 |

Profile review of the 49 measured GO nuclear-receptor targets in the focal Parquet gave the same activity structure: 42 nodes had no significant 151 features, four had 1-9 significant features, and only three had at least 50.

### Same-experiment corpus context for training genes

I used the July sourceguard corpus only as a semantic layer over measured training perturbations, not as independent replication.

- `Nr2f1` was interpreted as a sparse acute response: in the corpus report it crossed FDR only for `Ell` outside the focal class and for `Sorl1`/`Sema7a` in `151 TH Prkcd Grin2c Glut`.
- `Rora` was a special maintained thalamic program; `Rorb` and `Rorc` failed to phenocopy it in the same 151 responder group.
- `Nr1d1` and `Rora` formed an opposing ROR/REV-ERB-like 151 contrast rather than a generic nuclear-receptor response.
- `Esrra` was an ESRRA-specific oxidative-metabolism/structure response; ESRR paralogs and PGC/PPAR neighbors were flat in the matched 151 surface.

Those records argue against borrowing the 57-278 DEG scale of `Esrra`, `Nr1d1`, or `Rora` for `Nr2f2` just because they are all nuclear receptors.

## Synthesis

`Nr2f2` is expressed in the focal thalamic population and encodes a direct transcriptional regulator, so I did not collapse it to the global all-target median of zero. The evidence also does not support a broad 151-class state comparable to `Rora`, `Nr1d1`, or `Esrra`: those were special pathway modules in the training measurements, whereas the closest measured NR2/COUP-family analog, `Nr2f1`, gave only two strict 151 DEGs and `Nr2f6` gave none.

The unresolved NR2F2 protein persistence after P16 editing and the developmental, not acute, nature of the causal mouse literature further pull the point estimate toward a small sparse response. I therefore used the closest-family 0-3 DEG scale, with a small upward allowance for the exact 50.8% focal expression of `Nr2f2`, and chose:

`predicted_n_degs = 2`
