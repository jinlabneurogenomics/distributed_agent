# Fcgr2b DEG-count forecast

## Target and endpoint

- Target: `Fcgr2b`
- Focal population: `151 TH Prkcd Grin2c Glut`
- Requested endpoint: number of measured genes with BH-adjusted Wilcoxon `p < 0.05`
- Prediction: `0`

## Evidence used

1. Declared target biology bundle for `Fcgr2b`

   The structured card describes Fcgr2b as a low-affinity IgG Fc receptor with inhibitory ITIM signaling and immune-complex uptake in B-cell/myeloid contexts. A disruptive P16 edit should stop new receptor synthesis, and the functional-stock adjudication favors substantial depletion by the P37-P44 harvest because Fcgr2b is a renewable membrane receptor rather than a durable installed carrier.

   The same card also makes the main endpoint-lowering point: Fcgr2b biology is strongest in immune or microglial compartments, not in healthy NeuN-positive thalamic neurons. The exact focal expression measurement shows only 119 total `Fcgr2b` UMIs among 23,679 non-target nuclei in `151 TH Prkcd Grin2c Glut`, with 105 nuclei expressing the transcript. That is 0.443430888% of the focal non-target population, mean raw UMI 0.00502555, and mean log1p CP10K 0.00229477. This exact reach is task-matched and supersedes broader qualitative expression priors.

   Fcgr2b loss has neural evidence in adult systemic seizure assays and amyloid-beta-stressed neuronal systems, but those settings do not establish a healthy juvenile thalamic neuron-autonomous response within 21-28 days. The card also marks acute phenotype latency in this matched context as unreported.

2. Same-experiment corpus

   The selected PerturbAI corpus release has no `Fcgr2b` Findings, no Claims, and no explicit report references. I therefore did not have a same-experiment Fcgr2b semantic profile to transfer.

3. Training count table for `151 TH Prkcd Grin2c Glut`

   The declared training table contains 1,674 visible perturbations for this focal class. It is very zero-inflated:

   - 1,205 / 1,674 have `n_degs = 0`
   - 276 / 1,674 have `n_degs = 1`
   - median = 0, 75th percentile = 1, 90th percentile = 2
   - the large tail is carried by chromatin, splicing, proteostasis, and general transcriptional regulators, for example `Uba5` 2677, `Tpr` 1768, `Sin3a` 1433, `U2af2` 828, and `Psmb4` 742

   The immune/Fc-adjacent training perturbations I considered were all at the flat end of the focal count distribution:

   | training target | focal `n_degs` |
   | --- | ---: |
   | `Fcgr4` | 0 |
   | `Csf1r` | 0 |
   | `Cx3cr1` | 0 |
   | `Irf8` | 0 |
   | `Spi1` | 0 |
   | `H2-Eb1` | 0 |
   | `Cd14` | 0 |
   | `Cd36` | 0 |
   | `Cd40` | 0 |
   | `Cd80` | 0 |
   | `Tlr2` | 0 |
   | `Tlr3` | 0 |
   | `Tlr4` | 0 |
   | `Tlr5` | 0 |
   | `Tlr7` | 0 |
   | `Tlr8` | 0 |

4. Declared expression Parquet

   I checked the raw differential-expression rows for the selected immune and neuroimmune analogues in the exact focal population. The queried training nodes each had 17,259 measured focal rows. `Fcgr4`, `Csf1r`, `Cx3cr1`, `Irf8`, `Spi1`, `H2-Eb1`, `Cd14`, `Cd36`, `Cd40`, `Cd80`, and `Tlr2/3/4/5/7/8` each had zero rows with `pvals_adj < 0.05`. Their matched perturbed-nucleus counts were in the same sparse Perturb-seq regime as other real training perturbations, so the zero counts are not just missing entries in the count table.

## Synthesis

The focal-cell expression measurement is the decisive prior. Fcgr2b protein should eventually be lost after CRISPR disruption, but the receptor is nearly absent in the assayed thalamic NeuN-positive nuclei, and the neural phenotypes in the biology bundle come from systemic adult or amyloid-beta-stressed contexts rather than a matched healthy thalamic context. The best same-endpoint training comparators are immune/Fc-neighborhood or microglial-lineage targets, including the related Fc receptor `Fcgr4`; these sit at `n_degs = 0` in `151 TH Prkcd Grin2c Glut`.

I therefore forecast that `Fcgr2b` falls in the zero-DEG mass of the focal training distribution rather than in the small nonzero tail.
