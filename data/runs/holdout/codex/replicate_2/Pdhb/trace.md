# Direct `Pdhb` DEG-count forecast

## Prediction

`151 TH Prkcd Grin2c Glut`, target `Pdhb`: **1 DEG** at BH-adjusted Wilcoxon `p < 0.05`.

## Evidence used

- The declared holdout manifest and biology bundle both identify the sole target as `Pdhb`; `Pdhb` is absent from the focal-population training count table.
- The canonical biology bundle says PDHB is the obligate beta subunit of the mitochondrial PDH E1 heterotetramer with PDHA1. A disruptive edit should block new beta-subunit supply, but pre-existing assembled E1 is not directly disabled, and the bundle adjudicates functional stock at P37-P44 as `partially_depleted_or_leading_edge` because no matched postmitotic thalamic neuronal PDH E1 half-life was found.
- Exact in-assay reach is high in the focal population: non-targeting `151 TH Prkcd Grin2c Glut` nuclei have `Pdhb` expression in 21,831 of 23,679 nuclei, `92.20%`, with mean log1p CP10K `1.041` and mean raw UMI `3.462`. This supports measurability of the self transcript but does not measure editing efficiency or downstream response.
- The selected same-experiment corpus release has no `Pdhb` Finding, Claim, or explicit comparator reference, so there was no packaged `Pdhb` signature interpretation to transfer directly.
- The exact `p < 0.05` focal-population training table is zero-inflated: `1205/1674` training targets have `0` DEGs, `469/1674` are nonzero, and only `106/1674` have at least 10 DEGs.
- Immediate mitochondrial pyruvate/PDC comparators in the same `151 TH Prkcd Grin2c Glut` endpoint were at the floor:

  | target | n_degs |
  |---|---:|
  | `Pdha1` | 1 |
  | `Dlat` | 1 |
  | `Dld` | 0 |
  | `Mpc1` | 0 |
  | `Aco2` | 0 |
  | `Ogdh` | 0 |
  | `Idh3a` | 1 |
  | `Mdh2` | 1 |
  | `Suclg1` | 0 |

- In the declared expression Parquet for the same class, the only `pvals_adj < 0.05` rows among the positive singleton analogues were their own perturbed transcripts: `Pdha1` for `Pdha1`, `Dlat` for `Dlat`, `Idh3a` for `Idh3a`, `Mdh2` for `Mdh2`, `Sucla2` for `Sucla2`, and `Uqcrc2` for `Uqcrc2`. `Dld`, `Mpc1`, `Aco2`, `Ogdh`, and `Suclg1` had no significant feature at this threshold.
- A symmetric profile comparison of `Pdha1`, `Dlat`, `Dld`, `Mpc1`, `Aco2`, `Ogdh`, `Idh3a`, `Mdh2`, `Suclg1`, `Sucla2`, and `Uqcrc2` found no shared significant positive or negative feature intersections among the inspected direct PDH/TCA pairs in the focal class, consistent with singleton or null profiles rather than a coherent mitochondrial carbon-flow nuclear program.
- Packaged same-experiment Findings, used only as semantic interpretation of the same Parquet/count evidence, agree with this boundary: `Pdha1:F003` reports that thalamic `Pdha1` had significant self-transcript loss without downstream FDR<0.10 genes; `Pdha1:F004`, `Dld:F003`, `Mpc1:F002`, and `Dlat:F004` describe represented PDC, mitochondrial pyruvate-entry, and TCA comparators as mostly buffered or sparse, and explicitly note that these neighboring perturbations did not form a generic PDH/TCA transcriptional module.

## Reasoning

`Pdhb` has an exact direct partner in `Pdha1`; loss of either E1 subunit should threaten the same proximal pyruvate-to-acetyl-CoA step. The in-assay expression reach for `Pdhb` is high enough that its own transcript is measurable in this population, and lack of a PDHB beta paralog leaves the perturbation biologically credible.

The quantitative training evidence nevertheless argues strongly against a broad downstream footprint. The closest measured `p < 0.05` analogues are either null or self-only in the target thalamic class, and the report-level evidence generalizes that point across the pyruvate-entry/PDC/TCA neighborhood: acute sparse perturbation of postmitotic neurons does not reliably turn mitochondrial carbon-flow loss into a nuclear snRNA-seq DE program by 21-28 days. Because the endpoint counts every significant measured gene, including the target transcript, the best forecast is a singleton rather than a strict zero: one significant `Pdhb` self-transcript row and no BH-significant downstream genes.
