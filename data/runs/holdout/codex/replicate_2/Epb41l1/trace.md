# Direct `n_degs` forecast

Target: `Epb41l1`

Focal population: `151 TH Prkcd Grin2c Glut`

Endpoint: measured genes with Wilcoxon BH-adjusted `pvals_adj < 0.05`.

## Held-out target biology

- The manifest contains one target, `Epb41l1`.
- `Epb41l1` is absent from the declared `151 TH Prkcd Grin2c Glut` training count table and from the declared training Parquet, so the point below was not read from the target profile.
- The exact biology bundle reports measurable but partial focal-population reach: 9,910 of 23,679 non-target nuclei express `Epb41l1` in this class, `41.8514%`, with mean log1p(CP10K) `0.2757`.
- 4.1N/Epb41l1 is a neuronal FERM-domain membrane-cytoskeleton and postsynaptic receptor scaffold. A P16 loss-of-function edit should progressively stop new 4.1N supply, and the closest target-specific protein-turnover estimate is a `7.46` day neuronal-culture half-life, so renewable stock should be mostly depleted over the P37-P44 harvest window.
- The evidence for an acute thalamic transcriptional response is still indirect. Germline complete loss has strong postnatal neuroendocrine phenotypes outside this thalamic assay, while a juvenile hippocampal Epb41l2-null / Epb41l1-hypomorphic experiment reported largely preserved selected CA1 glutamatergic physiology despite severe 4.1N/4.1G reduction. Several protein 4.1 family members exist, but compensation in postnatal thalamic neurons is untested.

Interpretation: the perturbation is likely biologically realized, but its expected acute survivor-cell transcriptome is a local scaffold/receptor-organization effect, not the kind of broad regulatory or proteostatic collapse that dominates high `n_degs` values in this class.

## Training scale in the focal class

The declared `151 TH Prkcd Grin2c Glut` count table has 1,674 observed training perturbations.

- `n_degs = 0` for 1,205 / 1,674 targets.
- Median `n_degs = 0`; 75th percentile `= 1`; 90th percentile `= 2`; 95th percentile `= 18`; 99th percentile `= 430`.
- The mean `n_degs = 14.05` is driven by a small tail of large responses: for example `Uba5 = 2677`, `Tpr = 1768`, `Sin3a = 1433`, `Rnpc3 = 868`, `Psmb4 = 742`.

Hand-selected observed scaffold, membrane-cytoskeleton, adhesion, and receptor perturbations were mostly at the floor:

| target | focal `n_degs` |
|---|---:|
| `Add1` | 0 |
| `Add2` | 0 |
| `Add3` | 0 |
| `Ank2` | 0 |
| `Baiap2` | 0 |
| `Gria1` | 0 |
| `Gria2` | 0 |
| `Dlg4` | 1 |
| `Nrxn1` | 1 |
| `Sptan1` | 1 |
| `Shank3` | 2 |
| `Grin2a` | 1 |
| `Grin2b` | 2 |

The one- and two-DEG cases in that neighborhood were largely self-transcript-only contrasts in the focal Parquet. `Grin1`, with `89` DEGs, and `Ctnnb1`, with `383` DEGs, were useful upper-bound contrasts but are broader receptor-core or Wnt/adhesion perturbations rather than close 4.1N analogs.

## Profile check

I compared `Add1`, `Add2`, `Add3`, `Ank2`, `Baiap2`, `Dlg4`, `Gria1`, `Gria2`, `Nrxn1`, `Shank3`, `Sptan1`, `Grin1`, `Grin2a`, and `Grin2b` symmetrically in `151 TH Prkcd Grin2c Glut` using `logfoldchanges` with `pvals_adj < 0.05` as the significance column.

- 7 of the 14 selected profiles had no significant features; 6 had only 1-9 significant features; `Grin1` was the only profile above that range.
- Among the five quietest scaffold anchors, no significant feature was shared with the receptor/synapse peers at FDR 0.05, including the higher-response `Grin1` profile.
- Whole-profile correlations placed quiet scaffold nodes near both quiet and receptor nodes, but this reflected weak genome-wide tails rather than a shared significant DEG module.

The profile evidence therefore did not support lifting `Epb41l1` out of the zero/one DEG floor set.

## Point synthesis

`Epb41l1` should be expressed and sufficiently renewable for the edit to remove a substantial fraction of functional 4.1N by harvest, but only in about 42% of focal non-target nuclei and with unresolved paralog or client buffering. The nearest measured perturbations to a membrane-cytoskeleton/postsynaptic scaffold were predominantly exact zeros, and the sparse one-DEG analog outcomes were mostly self-transcript calls that should not be assumed for `Epb41l1`.

Point prediction:

```tsv
target_name	predicted_n_degs
Epb41l1	0
```
