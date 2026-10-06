# Direct DEG-count prediction trace

## Target and endpoint

- Holdout target: `Zkscan3`
- Focal population: `151 TH Prkcd Grin2c Glut`
- Endpoint: `n_degs`, the count of measured genes with BH-adjusted Wilcoxon `p < 0.05`
- Prediction: `0`

## Evidence used

The declared biology bundle for `Zkscan3` identifies it as a nuclear KRAB/SCAN C2H2 zinc-finger transcription regulator. Exact non-target expression in the requested thalamic class was high enough to make perturbation reach plausible: 16,790 of 23,679 non-target nuclei expressed the gene, or 70.9%, with mean log1p CP10K 0.539 and mean raw UMI 1.37.

The same bundle did not provide a matched postnatal thalamic loss phenotype or an acute P16-to-P37/P44 clearance clock. Its stock card called functional ZKSCAN3 realization by harvest indeterminate: new protein supply should stop after a disruptive edit, but existing nuclear protein and chromatin occupancy are not directly removed, and endogenous ZKSCAN3 turnover was not located. The mouse perturbation evidence was systemic or non-neural: grossly normal germline-null mice with an erythroid phenotype under stress, not a demonstrated thalamic neuronal dependency. The `Zkscan4` paralog was only a proposed buffer, without a same-context double-loss or compensation test.

The declared focal-class count table contained 1,674 training perturbations and was very zero-heavy: 1,205 had `n_degs = 0`, the median was 0, the 75th percentile was 1, the 90th percentile was 2, and the 95th percentile was 18. Thus the quantitative base rate for an expressed but weakly grounded target is no detectable downstream DE rather than a broad response.

The closest literal training perturbations from the same SCAN/zinc-finger naming neighborhood were quiet:

| training target | focal `n_degs` | best focal adjusted p in Parquet |
|---|---:|---:|
| `Zkscan1` | 0 | 1.0 |
| `Zscan26` | 0 | 1.0 |

The non-neural genes linked by the curated `Zkscan3` source card also had no focal response when directly perturbed:

| training target | focal `n_degs` | best focal adjusted p in Parquet |
|---|---:|---:|
| `Gata1` | 0 | 0.989 |
| `Klf1` | 0 | 1.0 |
| `Tiam1` | 0 | 0.312 |

A wider literal `Zkscan`/`Zscan`/`Zfp`/`Zbtb`/`Zfpm` scan found 40 training rows, 32 of which had zero DEGs and a median of 0. There were real positive zinc-finger/BTB boundaries, especially `Zbtb7a` at 841 and `Zfp423` at 150, so the class can produce strong transcription-factor footprints. I treated those as mismatched high-response boundaries rather than as the center for `Zkscan3`: they did not share the specific KRAB/SCAN identity or the weak postnatal thalamic functional prior.

## Synthesis

`Zkscan3` is expressed broadly enough that a null result cannot be dismissed as simple target absence. Still, the task-matched perturbational prior is weak: no matched neuronal phenotype, uncertain protein-stock depletion by the 21-28 day harvest window, possible but unproven buffering, two quiet same-neighborhood SCAN/zinc-finger training perturbations, and zero response from the curated erythroid-circuit genes. Because the count table's default state in `151 TH Prkcd Grin2c Glut` is 0 and the closest measured analogs stayed exactly at 0 with no near-threshold Parquet support, the point forecast is `0` DEGs.

No held-out `Zkscan3` expression signature or target outcome was used.
