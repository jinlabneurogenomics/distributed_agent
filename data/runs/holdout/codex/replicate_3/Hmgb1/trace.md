# Hmgb1 DEG-count forecast

## Target and endpoint

- Manifest target: `Hmgb1`.
- Endpoint: `n_degs` in `151 TH Prkcd Grin2c Glut`, counted as measured genes with BH-adjusted Wilcoxon `p < 0.05`.
- Same-experiment direct Hmgb1 evidence: no same-experiment corpus Findings or Claims were available for Hmgb1, and the target perturbation profile was absent from the declared training Parquet/count inputs.

## Hmgb1 biology used

The exact focal expression bundle made target reach plausible: in non-target `151 TH Prkcd Grin2c Glut` nuclei, `Hmgb1` was detected in 13,307 / 23,679 cells, with 56.197% expressing cells, mean raw UMI 0.9907, mean CP10K 0.6315, and pseudobulk CPM 62.09.

HMGB1 is a dynamic nuclear chromatin/DNA chaperone with additional cytoplasmic and extracellular pools. A CRISPR loss-of-function edit should stop resupply, but the P16-to-P37/P44 assay samples only 21-28 days after editing. The functional-stock card therefore called the harvest state `partially_depleted_or_leading_edge`: material stock decline is likely, while near-complete loss at the assay time is not established. Direct neural evidence also supported possible postnatal observability but in non-matched contexts: young-adult inducible global loss had sustained brain depletion measured at 6-7 weeks, and newborn astroglial loss affected postnatal gliovascular maturation.

Net effect of the biology: Hmgb1 has real thalamic expression and should not be treated like an unexpressed null target, but the endpoint should be discounted versus fast-turnover or acutely disabling chromatin regulators because pre-existing HMGB1 protein can persist through the 3-4 week Perturb-seq window.

## Training-count scale

The `151 TH Prkcd Grin2c Glut` training table was extremely sparse overall:

| count bin | training targets |
|---|---:|
| 0 | 1205 |
| 1 | 276 |
| 2-5 | 65 |
| 6-20 | 50 |
| 21-100 | 36 |
| 101-500 | 27 |
| >500 | 15 |

So the screen-wide median is 0, the 75th percentile is 1, and the 95th percentile is 18. A low nonzero point already places the perturbation above most training targets.

For chromatin, DNA-binding, and architectural regulators available in the training count table, the same focal-population counts were heterogeneous:

| training perturbation | n_degs |
|---|---:|
| Dnmt3a, Ep300, Kat6a, Kat6b, Ncoa1, Ncoa3, Nsd2, Smarca4 | 0 |
| Ehmt1 | 4 |
| Crebbp | 8 |
| Smarce1 | 11 |
| Mecp2 | 16 |
| Setdb1 | 22 |
| Nsd1 | 23 |
| Chd2 | 34 |
| Chd8 | 61 |
| Bptf | 65 |
| Chd4 | 100 |
| Smarcc2 | 185 |
| Ctcf | 270 |
| Setd1a | 368 |
| Yy1 | 720 |
| Hnrnpu | 733 |
| Sin3a | 1433 |

The profile diagnostic over these 26 selected chromatin/architectural targets found no tight shared response that could be averaged for Hmgb1: positive-tail overlap across pairs had median 0.075 and negative-tail overlap had median 0.145 among top-200 signed features. Packaged same-experiment Claims likewise warned that broad chromatin labels did not create interchangeable neuronal signatures: CHD paralogs were not simple phenocopies, NuRD/MBD-adjacent perturbations remained target-selective, and Ctcf's large Pcdh-centered response was not reproduced by represented cohesin machinery.

## Forecast

The final point is `4` DEGs.

I set the forecast above the screen-wide zero/one mode because Hmgb1 is detectably expressed in over half of focal thalamic cells and loss of a dynamic chromatin DNA chaperone is biologically reachable. I kept it in the 2-5 bin because the target is not a sequence-specific transcription factor or an obligate chromatin-remodeling subunit, the declared stock card indicates only partial functional depletion by harvest, Hmgb2 redundancy is unresolved, and many measured chromatin cofactors with clear nuclear functions were zero or single-digit responders. The small Ehmt1-like scale, rather than the Chd4/Ctcf/Setd1a/Sin3a outlier scale, best matched that mixed evidence.
