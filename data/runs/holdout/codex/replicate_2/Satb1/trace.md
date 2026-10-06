# Satb1 direct DEG-count forecast

## Target and endpoint

- Target: `Satb1`
- Focal population: `151 TH Prkcd Grin2c Glut`
- Endpoint: `n_degs`, the number of measured genes with BH-adjusted Wilcoxon `p < 0.05`
- Prediction: `6`

## Outcome-blind target biology

The declared Satb1 biology bundle supports a realized loss in target-positive cells but not a broad pan-thalamic aggregate effect:

- Exact in-assay non-target expression in `151 TH Prkcd Grin2c Glut` was present but restricted: 10,806 of 23,679 nuclei expressed `Satb1`, or 45.635%, with mean raw UMI 0.716 and mean CP10k 0.456.
- The functional-stock adjudication concluded that P16 CRISPR should likely substantially deplete active SATB1 by the P37-P44 harvest in successfully edited SATB1-positive neurons.
- The closest loss-of-function timing prior was adult postmitotic dopaminergic-neuron knockdown, where molecular and cell-state changes appeared by 14 days and cell loss by 21-28 days; that matches the postmitotic time window better than developmental knockout but is not thalamic.
- Thalamic SATB1 expression and acute thalamic loss were incompletely resolved: adult mouse IHC detected SATB1 in relatively small thalamic neuronal populations, and the bounded search found no direct thalamic Satb1 loss experiment.
- Survivor conditioning could attenuate a DEG count if the most strongly affected Satb1-positive neurons were depleted before snRNA-seq.

I therefore treated `Satb1` as plausibly observable, but with a subset-diluted focal aggregate and weaker scale transfer than ubiquitous chromatin-machinery perturbations.

## Training measurements used

The declared 151-TH training count table contained 1,674 targets. Its same-endpoint empirical distribution was strongly zero-inflated:

- 1,205 / 1,674 targets had `n_degs = 0` in this class.
- Median = 0, 75th percentile = 1, 90th percentile = 2, 95th percentile = 18.
- The mean, 14.1, was pulled upward by a small broad-response tail; only 43 training targets had more than 100 DEGs.

I then checked biologically interpretable training perturbations in the declared Parquet in the matched `151 TH Prkcd Grin2c Glut` rows:

| training perturbation | reason for comparison | focal `n_degs` |
|---|---|---:|
| `Satb2` | closest SATB paralog and developmental chromatin/TF axis | 0 |
| `Bcl11a`, `Bcl11b`, `Foxp2`, `Tbr1`, `Nfia`, `Nfib`, `Nfix`, `Neurod2` | postmitotic neuronal/developmental TF boundary set | 0 each |
| `Sox5` | sparse thalamic developmental TF response | 2 |
| `Mecp2` | postmitotic methyl-CpG chromatin regulator with thalamic/midbrain basal effects | 16 |
| `Chd4` | NuRD remodeler; broad chromatin machinery boundary | 100 |
| `Ctcf` | architectural chromatin factor; broad Pcdh-dominated boundary | 270 |

Packaged same-experiment corpus context for `Satb2` reported a pan-surface null after P16 perturbation and absence of the canonical juvenile/embryonic projection-identity inversion, which made the exact SATB paralog a strong lower boundary. The `Sox5` corpus and raw Parquet rows gave only two positive FDR-significant genes, `Dgkh` and `Tnnt1`, in this exact thalamic class. In contrast, `Ctcf` and `Chd4` were real high-count thalamic responders, but their reports mapped them to broader CTCF-dominant protocadherin control and CHD4/NuRD programs rather than to an equal-scale SATB1 subset lesion.

The bounded profile comparison of these training genes also kept the high chromatin responses from dominating the forecast: `Satb2` had 0 significant features, `Sox5` had 2, `Mecp2` had 16, `Chd4` had 100, and `Ctcf` had 270; the nearest full-profile relationships among the SATB2/SOX/Mecp2/chromatin set were all weak, with no shared significant program between the sparse `Satb2`/`Sox5` nodes and the broad chromatin anchors.

## Synthesis

I forecast a small nonzero response.

The point is above the exact-paralog/null developmental-TF surface because `Satb1` has exact 151-TH expression in nearly half of control nuclei, dynamic rather than permanently installed chromatin occupancy, and direct postmitotic-neuron evidence that loss can be realized within the assay window. The point is below `Mecp2` and far below `Chd4`/`Ctcf` because SATB1-positive thalamic cells are a subset, direct thalamic loss is not established, and the large chromatin anchors perturb broader machinery or architectural programs that should act across more of the assayed aggregate.

A log-scale interpolation between the most relevant lower and upper local anchors, sparse `Sox5` at 2 and thalamic chromatin regulator `Mecp2` at 16, gives a center near six DEGs, while the broader `Chd4`/`Ctcf` observations function as upper boundaries rather than point donors.
