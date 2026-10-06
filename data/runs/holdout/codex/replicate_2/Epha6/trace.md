# Direct Epha6 n_degs forecast

Endpoint: number of measured genes in `151 TH Prkcd Grin2c Glut` with BH-adjusted Wilcoxon `p < 0.05`.

## Declared target

- The one-row holdout manifest names `Epha6`.
- The focal cell class is the exact atlas class `151 TH Prkcd Grin2c Glut`, i.e. thalamic glutamatergic neurons.
- I used the `biology` view of the declared Epha6 characterization bundle only; it exposed no target outcome and no labeled-neighbor outcomes.

## Biology that moves the forecast

- EphA6 is a single-pass EphA-family receptor tyrosine kinase for contact-dependent ephrin-A forward signaling at the plasma membrane.
- A successful P16 disruptive edit should stop new intact EphA6 receptor supply while leaving pre-edit receptor molecules to decay. The bundle judged the operative stock `likely_substantially_depleted` by the P37-P44 harvest, but with only partial kinetic evidence because no Epha6-specific half-life or neuronal persistence measurement was found.
- Exact in-assay reach is high rather than absent: in non-target nuclei from this class, `Epha6` was detected in 18,939 of 23,679 cells, `79.98%`, with mean `2.096` CP10K.
- Whole-life Epha6 loss has adult neural phenotypes, and Epha5 is the closest named neural paralog in the card. Those data support biological relevance but are adult/germline and cortex/behavior-skewed, so they do not establish a broad acute thalamic transcriptional response 21-28 days after a sparse P16 edit.

## Training evidence

The focal count table is very zero-inflated: 1,205 of 1,674 training targets are `0`; the median is `0`, the 75th percentile is `1`, and only 469 targets are nonzero.

Closest Eph-receptor rows in the same focal count table were:

| target | n_degs |
| --- | ---: |
| Epha2 | 0 |
| Epha3 | 0 |
| Epha4 | 1 |
| Epha5 | 0 |
| Epha10 | 0 |
| Ephb1 | 0 |
| Ephb2 | 0 |
| Ephb4 | 0 |

Other surface/guidance comparators with receptor or cue biology were also nearly all null in the declared table: `Slit2`, `Dcc`, `Ryk`, `Nrp1`, `Nrp2`, `Plxna1`, `Plxna4`, `Robo2`, and `Sema4d` were `0`, while `Plxna2`, `Robo1`, and `Sema5a` were `1`.

I then checked the declared Parquet in the exact focal class for these Eph/guidance rows. Each of the one-DEG receptor/guidance cases above was only the self-target transcript:

| target | significant feature | logFC | BH p_adj |
| --- | --- | ---: | ---: |
| Epha4 | Epha4 | -1.027 | 7.88e-32 |
| Plxna2 | Plxna2 | -0.596 | 0.0240 |
| Robo1 | Robo1 | -0.538 | 2.72e-06 |
| Sema5a | Sema5a | -0.915 | 3.94e-09 |

Thus the observed matched analogs do not show a multi-gene downstream program in this thalamic class; their nonzero counts are self-transcript events. A profile comparison over the seven available Eph receptors likewise found available profiles for all seven, with six `no_significant_features` rows and `Epha4` as the only `1_to_9_significant_features` row. The cohort had weak family-like negative-tail similarity, but no shared FDR-significant positive or negative program, so I treated the profile texture as insufficient to move the endpoint above a very small count.

## Point forecast

The upward bearings are real focal expression and likely within-window receptor depletion. The downward bearings are the lack of matched acute thalamic downstream responses for Epha5 and the other visible Eph receptors, the fact that nearby guidance/receptor nonzero cases are only self-knockdown, and the absence of direct evidence that Epha6 loss should induce a harvested-nucleus expression program by P37-P44.

Self-transcript knockdown could make the integer count `1`, but six of seven measured Eph receptors, including `Epha5`, had zero significant genes. The expected count is therefore below one; I round it to the nearest non-negative integer:

`predicted_n_degs = 0`
