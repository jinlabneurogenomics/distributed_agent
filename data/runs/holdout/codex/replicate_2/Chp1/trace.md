# Chp1 direct DEG-count forecast

## Target and endpoint

- Target: `Chp1`, from the declared one-row holdout manifest.
- Cell class: `151 TH Prkcd Grin2c Glut`.
- Endpoint: `n_degs`, the count of measured genes with Wilcoxon `pvals_adj < 0.05` in this focal class.
- Prediction: `1`.

## Evidence used

The canonical `Chp1` biology bundle gives a biologically real but not uniformly penetrant perturbation prior. `Chp1` is expressed in the focal non-target nuclei but not in all of them: 15,491 of 23,679 nuclei express it, or 65.4208%, with mean expression of 0.7476 CP10K and 1.2108 raw UMI. Its functional-stock card adjudicates the P16-to-P37/P44 lesion as `partially_depleted_or_leading_edge`: ongoing CHP1 supply should matter because the NHE1 carrier proxy turns over on an approximately daily scale, but CHP3 compensation is age- and cell-type-dependent and wild-type CHP1 lifetime in postmitotic thalamic neurons is unresolved. This supports possible self-transcript detection or a small local effect, while arguing against assuming a broad uniform response.

Gene-analog nomination against the 1,674 training perturbations found no close local substitute for `Chp1`: the target was absent from the training universe and from the selected same-experiment ledger graph, and all 1,586 nominees were `broad_functional_fallback` rather than exact paralogs, exact complexes, direct interactions, or narrow modules. The leading mechanistic community was Na+/H+ exchange/pH regulation, not an observed same-complex CHP1/NHE1 training group.

The focal-class training count table is heavily zero-inflated: among 1,674 visible perturbations, 1,205 have 0 DEGs, the median is 0, the 75th percentile is 1 DEG, and the 90th percentile is 2 DEGs. The nearest pH/Na+ fallbacks were at this null edge:

| comparator | relationship to `Chp1` used here | `n_degs` in `151 TH Prkcd Grin2c Glut` |
| --- | --- | ---: |
| `Slc9a9` | broad Na+/H+ exchanger / pH annotation | 0 |
| `Slc9a7` | broad Na+/H+ exchanger / pH annotation | 1 |
| `Gnas` | acid-pH response fallback | 0 |
| `Atp1a1` | intracellular sodium-homeostasis fallback | 1 |
| `Prnp` | broad calcineurin-NFAT / targeting fallback | 1 |
| `Mtor` | broad phosphatase / trafficking fallback | 2 |
| `Gsk3b` | broad phosphatase / trafficking fallback | 6 |
| `Grin2a` | broad calcium-binding / sodium-transport fallback | 1 |

The exact significant rows for the two one-count local fallbacks showed that `Slc9a7` and `Atp1a1` each contributed only their own target transcript at FDR < 0.05, not a downstream program. A 12-node profile comparison over the nearest broad fallbacks preserved this split: the source-like pH/Na+ nodes were null or self-only, while larger responses such as `Atp1a3` and `Grin1` came from broader, direct perturbations of Na+/K+ pumping or NMDA-receptor signaling that should not be used as equal-scale analogs for losing a renewable NHE cofactor.

## Synthesis

I therefore treated `Chp1` as more likely to be detected, if at all, through its own moderately expressed transcript than through a recurrent downstream state. The realized-loss prior is not zero, because CHP1-supported exchanger complexes should turn over during the 21-28 day window, but the exact focal expression reaches only about two thirds of nuclei and the nearest assayed pH/NHE fallbacks are 0-1 DEG. I placed the point at a self-transcript-sized response: `1` measured gene.
