# Direct forecast for `Nr4a2`

Prediction: `0` FDR < 0.05 DEGs in `151 TH Prkcd Grin2c Glut`.

## Evidence used

- Declared one-row manifest target: `Nr4a2`.
- Declared training count table: 1,674 non-held-out perturbations for `151 TH Prkcd Grin2c Glut`; `Nr4a2` was absent. The focal-class distribution was sparse: 1,205/1,674 had `n_degs = 0`, the median was 0, the 75th percentile was 1, the 95th percentile was 18, and 106 targets had at least 10 DEGs.
- Declared expression Parquet: a filtered `gene_target == "Nr4a2"` count returned 0 rows, confirming that the held-out target's perturbation signature was not present in the raw training surface I queried.
- Target biology bundle, exact focal reach: in the non-target nuclei of `151 TH Prkcd Grin2c Glut`, `Nr4a2` was detected in 1,584/23,679 nuclei, or 6.689%, with mean `log1p_cp10k = 0.0369` and mean `cp10k = 0.0553`.
- Target biology bundle, operation and stock: NR4A2 is a free nuclear transcriptional regulator. A successful disruptive edit should stop new NR4A2 production, and the bundle adjudicates functional stock by harvest as `likely_substantially_depleted`, because adult postmitotic-neuron loss caused near-complete nuclear protein loss within one week, shorter than the P16 to P37-P44 assay interval.
- Focal-class training counts for the closest directly represented family members were null:

| comparator | biological relation | `151` `n_degs` |
|---|---:|---:|
| `Nr4a1` | NR4A paralog | 0 |
| `Nr4a3` | NR4A paralog | 0 |
| `Rxra` | nuclear-receptor heterodimer partner class | 0 |
| `Rxrb` | nuclear-receptor heterodimer partner class | 0 |
| `Rxrg` | nuclear-receptor heterodimer partner class | 0 |
| `Rarb` | retinoid nuclear receptor | 0 |
| `Pitx3` | dopaminergic identity TF comparator | 0 |
| `Lmx1b` | dopaminergic/diencephalic TF comparator | 0 |
| `En1` | dopaminergic developmental TF comparator | 0 |
| `Foxa2` | dopaminergic developmental TF comparator | 0 |

- Direct focal Parquet rows for `Nr4a1`, `Nr4a3`, `Rxra`, `Rxrb`, `Rxrg`, `Rarb`, `Esrrb`, `Esrrg`, `Pitx3`, `Lmx1b`, `En1`, `Foxa2`, and `Egr2` all had zero measured genes with `pvals_adj < 0.05`. Matched perturbed-cell counts for these zero-footprint analogs were 183-273, so the zeroes are not from a missing focal contrast.
- Same-experiment corpus context, interpreted as the same screen rather than replication, supported the raw analog signal: `Nr4a1` had no FDR-gated downstream transcriptional response in any measured neuronal cell group; `Nr4a3` had a single narrow hit in `217 P MY Pineal Glut` and was flat elsewhere; and the represented individual NR4A perturbations were summarized as largely buffered at baseline.
- Counterexamples kept the forecast from treating "nuclear receptor" as intrinsically invisible: `Rora` had 278 focal DEGs and `Nr1d1` had 116 in the declared FDR < 0.05 count table, with packaged reports describing true `151` thalamic/circadian responses. Those were less direct than the NR4A paralogs because `Rora` and `Nr1d1` are broad thalamic/circadian regulators in this cell class, not localized NR4A-family factors.

## Synthesis

The strongest upward evidence is that NR4A2 protein should be depleted during the experimental window wherever `Nr4a2` is expressed and edited, so a biological response is plausible in the small expressing subpopulation. The two dominant downward bearings are assay reach and matched training behavior. Only 6.689% of the exact non-target focal population expressed `Nr4a2`; at the 183-273 matched perturbation-cell scale of close zero-count transcription-factor comparators, that would put a potential cell-intrinsic effect into roughly a dozen to twenty baseline-expressing nuclei before any guide/editing loss, making class-aggregated Wilcoxon FDR support hard to achieve. The closest assayed NR4A family members and RXR partners were also null in the focal group and largely buffered across the same basal postnatal screen.

I therefore put most mass on a flat `151 TH Prkcd Grin2c Glut` profile, with residual uncertainty for one or a few subpopulation marker hits. The direct integer forecast is `0`.
