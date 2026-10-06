# Direct Tfap2a n_degs forecast

## Target and endpoint

- Target: `Tfap2a`.
- Focal cell class: `151 TH Prkcd Grin2c Glut`.
- Endpoint: number of measured genes in that class with Wilcoxon BH-adjusted `pvals_adj < 0.05`.
- Prediction: `0`.

## Evidence used

### Declared target biology bundle

`Tfap2a` encodes AP-2alpha, a soluble nuclear sequence-specific transcription factor. The P16 edit should stop new functional TFAP2A synthesis, and the 21-28 day interval to P37-P44 harvest is likely long enough for most pre-edit dynamic TFAP2A stock to decline. That argues against a durable-stock failure mode.

The counterweight is focal reach. In the exact non-target focal population, `Tfap2a` was nearly absent:

| quantity | value |
| --- | ---: |
| expressing nuclei | 81 / 23,679 |
| pct expressing | 0.342075% |
| mean CP10K | 0.00266767 |
| mean log1p CP10K | 0.00178779 |
| mean raw UMI | 0.00502555 |
| pseudobulk CPM | 0.314969 |

The external biology in the bundle was also not a clean positive postnatal-thalamus prior. Severe mouse phenotypes came from germline or embryonic neural-crest loss, the neural AP-2 redundancy evidence came from developing retina, and no acute postnatal thalamic requirement or TFAP2A-specific neuronal clearance curve was available. Retinal single `Tfap2a` loss being mild while combined `Tfap2a`/`Tfap2b` loss was disruptive made AP-2 paralog buffering plausible but unresolved for this population.

Interpretation: functional stock should probably be cleared by harvest, but the target RNA is so rare in the assayed thalamic class that a class-aggregated survivor snRNA-seq Wilcoxon contrast is more likely to be null than to produce a broad significant signature.

### Training count table for this class

The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` contains 1,674 observed training perturbations. Its distribution is dominated by null or near-null values:

| statistic | value |
| --- | ---: |
| zero-DEG perturbations | 1,205 / 1,674 |
| median | 0 |
| 75th percentile | 1 |
| 90th percentile | 2 |
| 95th percentile | 18 |
| mean | 14.054 |
| max | 2,677 |

So the unconditional focal-class prior is already zero-inflated; the high mean is produced by a small long tail of broad essential or chromatin/RNA-processing regulators such as `Uba5`, `Tpr`, `Sin3a`, `Rnpc3`, `Zbtb7a`, and spliceosome/proteasome factors.

### Comparator focal signatures from the declared expression Parquet

I checked the declared Parquet for a manually selected panel of observed developmental or sequence-specific TF perturbations in exactly `151 TH Prkcd Grin2c Glut`. The closest operation/context analogues were quiet:

| comparator | focal n_degs |
| --- | ---: |
| `Arx` | 0 |
| `Atoh1` | 0 |
| `Foxp2` | 0 |
| `Pax6` | 0 |
| `Pou2f1` | 0 |
| `Tfap4` | 0 |
| `Zbtb38` | 1 |
| `Sox2` | 2 |
| `Sox5` | 2 |
| `Zic1` | 2 |
| `Zbtb18` | 5 |
| `Zfp148` | 8 |

The same Parquet scan also confirmed that TFs can sit in the response tail when their biology is broad in this class, for example `Zbtb7a` with 841 DEGs and `Zfp423` with 150. I treated those as positive scale references, not close transfers, because `Tfap2a` has a much narrower exact focal expression footprint and its direct evidence is developmental or retinal rather than an established mature thalamic maintenance program.

## Synthesis

Three signals drove the point estimate:

1. `Tfap2a` has a plausible post-edit molecular loss by harvest because AP-2alpha is a dynamic nuclear TF rather than an inherited stable structure.
2. The exact focal reach is extremely low: only 0.34% of control nuclei in the class expressed detectable `Tfap2a`.
3. Training perturbations with developmental TF-like biology usually gave 0-2 DEGs in this class despite comparable recovered-cell counts, whereas the large DEG tail came from broader regulatory machinery.

The remaining upward uncertainty is that low nuclear RNA does not rule out a functional TFAP2A protein pool and the edit could affect a rare but transcriptionally distinctive cell subset. The nearest quantitative evidence still favors a measured class-aggregate null, so I forecast `n_degs = 0`.
