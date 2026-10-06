# Tubb2a n_degs forecast

Endpoint: number of measured genes in `151 TH Prkcd Grin2c Glut` with BH-adjusted Wilcoxon `pvals_adj < 0.05`.

Prediction: `Tubb2a -> 1`.

## Evidence used

### Declared target biology bundle

- Target and context: `Tubb2a`, postnatal P16 CRISPR loss of function assayed after 21-28 days in P37-P44 mouse thalamic NeuN-positive neurons.
- Exact expression reach in the focal 151 class is high: `Tubb2a` was detected in 22,847 of 23,679 non-target nuclei, or 96.486%, with mean raw UMI 5.93 and mean log1p CP10K 1.416. This makes the perturbation reachable in this population and makes target-row detection plausible, while not proving editing efficiency or downstream effect size.
- TUBB2A is a beta-tubulin structural subunit that supplies alpha/beta heterodimers and microtubule lattice. A disruptive edit stops new isotype supply but does not instantly remove pre-existing soluble dimers or assembled lattice.
- The functional-stock card judged stock at harvest as likely substantially depleted but only from partial evidence: pooled brain tubulin kinetics imply both rapidly renewed material and a slower approximately two-week lattice-associated pool, with a possible residual stable tail.
- The strongest causal loss evidence is germline/developmental mouse cortex, not P16 thalamic neurons. Homozygous deletion is compatible with postnatal survival and has subtle cortical abnormalities.
- `Tubb2b` is almost identical to `Tubb2a`; this supports likely buffering by other beta-tubulin isotypes, but compensation was not directly proven in the 151-class P16 assay.

### Training count table

The declared 151-class count table contains 1,674 training perturbations. It is highly sparse even in this high-yield cell class:

| subset | n_degs |
| --- | ---: |
| median training target | 0 |
| 75th percentile | 1 |
| zeros | 1,205 / 1,674 |
| exactly one DEG | 276 / 1,674 |

Closest measured cytoskeleton and tubulin-family counts in the same table were low for direct tubulin genes:

| training perturbation | relation to Tubb2a | n_degs in 151 |
| --- | --- | ---: |
| `Tubb4b` | beta-tubulin structural subunit | 1 |
| `Tubb5` | beta-tubulin structural subunit | 1 |
| `Tuba4a` | alpha-tubulin structural subunit | 2 |
| `Tuba1a` | alpha-tubulin structural subunit, visible tubulin-feedback exception | 7 |
| `Tbcd` | tubulin folding machinery | 12 |
| `Dctn1` | dynein/dynactin transport adaptor | 75 |
| `Map1b`, `Mapt`, `Stmn2`, `Kif1a`, `Kif5a`, `Kif5c` | microtubule-associated or motor genes | 1 each |
| `Map6`, `Camsap1`, `Spast`, `Kif2a` | microtubule-associated or motor genes | 0 each |

### Matched profile analysis of declared Parquet

I compared a 17-node tubulin/cytoskeleton cohort directly from `training_de_all_cell_groups.parquet`, filtered to `group_name == "151 TH Prkcd Grin2c Glut"`, using Wilcoxon `scores` as the signed profile value and `pvals_adj < 0.05` as the significant-feature definition.

The raw profile counts reproduced the count table:

| perturbation | significant genes | positive | negative |
| --- | ---: | ---: | ---: |
| `Tuba1a` | 7 | 6 | 1 |
| `Tuba4a` | 2 | 1 | 1 |
| `Tubb4b` | 1 | 0 | 1 |
| `Tubb5` | 1 | 0 | 1 |
| `Tbcd` | 12 | 9 | 3 |

For `Tubb4b` and `Tubb5`, the single significant negative feature was the perturbed transcript itself. `Tuba1a` instead down-regulated its own row and up-regulated a narrow tubulin-isotype module in which `Tubb2a` was the second strongest positive feature. `Tbcd` had a different 12-gene state led by up-regulation of `Tuba1a`/`Tuba1b` and non-tubulin genes. Whole-profile and signed-tail overlaps across the 17 cytoskeleton nodes were small; the cohort-level median signed-tail overlap coefficient was 0 in both directions.

### Same-experiment corpus interpretation of training perturbations

The corpus is not an independent measurement, but it gives useful interpretation of the same training profiles. Its Tuba1a/Tubb5 Findings state that:

- `Tuba1a` loss uniquely elicited a compensatory alpha/beta-tubulin paralog mRNA program in matched Pvalb and 151 thalamic neurons.
- The beta-tubulins `Tubb5` and `Tubb4b`, and `Tuba4a`, did not phenocopy that `Tuba1a` multi-tubulin up-regulation state.
- Significant `Tubb5` self-transcript depletion was often uncoupled from a stable downstream nuclear RNA program.
- Represented MAP, motor, dynactin, and related microtubule perturbations generally did not form a shared postnatal cytoskeletal-stress module.

## Synthesis

High exact `Tubb2a` expression argues against a context-absence zero. The endpoint also counts the self transcript, and the two closest observed beta-tubulin perturbations in the same 151 population each produced exactly one DEG, their own target row, without a broader paralog-feedback or stress program. That local beta-tubulin pattern is more transferable than the `Tuba1a` exception: `Tuba1a` is an alpha-tubulin whose observed program included `Tubb2a` as a compensatory output, whereas loss of measured beta-tubulins was buffered on the downstream snRNA axis.

The postnatal Tubb2a lesion should have real reach by harvest, because most renewable tubulin stock should have turned over across 21-28 days, but the biology bundle and the training set both point to buffering by paralogous beta-tubulin supply and to weak downstream coupling rather than a `Dctn1`- or `Tbcd`-scale cytoskeletal response. I therefore place `Tubb2a` in the one-gene beta-tubulin regime rather than at zero or in the 7-12 gene alpha/folding response range.

No target perturbation signature, target count, relationship-review artifact, branch-calibration artifact, scalar prior, or calibrated probability was used.
