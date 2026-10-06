# Naa15 DEG-count forecast

## Declared target and endpoint

- Target manifest: `Naa15`
- Endpoint: number of measured genes in `151 TH Prkcd Grin2c Glut` with BH-adjusted Wilcoxon `pvals_adj < 0.05`
- Point forecast: `0`

## Evidence used

### Endpoint scale from the declared training count table

I used `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`, which contains 1,674 observed training perturbations for this exact thalamic glutamatergic class.

The observed class-specific response was sparse:

- 1,205 / 1,674 training targets had `n_degs = 0`.
- 276 / 1,674 had `n_degs = 1`.
- The median was `0`; the 75th percentile was `1`; the 90th percentile was `2`.
- The high tail was very skewed: the maximum was 2,677.

Thus the count-table base rate puts an uncalibrated target near 0-1 unless the biology identifies a high-response process.

### Biology bundle for Naa15

The canonical bundle at `[local file: Naa15.json]` reports exact in-assay expression for the focal class but no endpoint outcome:

- `Naa15` was detected in 18,674 / 23,679 non-target cells in `151 TH Prkcd Grin2c Glut` (`78.86%`; pseudobulk 112.23 CPM).
- The perturbation is an acute P16 CRISPR edit read out 21-28 days later at P37-P44 in recovered postmitotic neuronal nuclei.
- NAA15 is the auxiliary NatA subunit that complexes with NAA10 and supports cotranslational N-terminal acetylation.
- Functional-stock adjudication favored `partially_depleted_or_leading_edge` by harvest: new NAA15 supply should be blocked in edited cells, but existing NAA15-containing NatA complexes and already acetylated carrier proteins can persist, neuronal carrier turnover is heterogeneous, and Naa16-supported alternative NatA complexes are plausible but untested in mouse thalamic neurons.
- The observability card supported biological reach only incompletely: postnatal NatA relevance was based on cerebellar Purkinje culture and adult thalamic expression, while a matched acute Naa15-loss phenotype in thalamic neurons was not available.

So the bundle argues against a pure expression-missing null, but it also makes full NatA collapse by the 3-4 week endpoint uncertain.

### Same-experiment corpus around the NatA catalytic comparator

`Naa10` was the only literal NatA-complex target present in the focal training count table; `Hypk` and `Naa16` were absent from that table. Its focal count was:

```text
Naa10	0
```

The selected same-experiment corpus had no Naa15 report, Claim, or explicit comparator reference, so it did not expose the held-out target outcome. It did contain a Naa10 report: postmitotic P16 `Naa10` perturbation produced zero downstream genes at FDR < 0.10 across 22 measured neuronal groups, including the focal `151 TH Prkcd Grin2c Glut` surface with 240 matched perturbed cells, 23,679 controls, Naa10 logFC -0.081, Naa10 FDR 1, zero downstream FDR < 0.10 genes, and minimum downstream FDR 1.

The Naa10 report also found no compensatory NAT-family, integrated-stress, apoptosis, proteasome, or ubiquitin rebound program at FDR < 0.10, and contrasted the Naa10 null with active protein-homeostasis / translation comparators. In the focal BH 0.05 training table, those indirect comparators had much larger responses (`Psmb4 = 742`, `Psmc1 = 430`, `Eef2 = 9`), confirming that the class can detect secondary proteostasis-like programs when they are present.

### Focal measured-profile comparison of the Naa10 neighborhood

I ran a symmetric profile comparison in the exact `151 TH Prkcd Grin2c Glut` context over Naa10, its flat full-vector neighbors named in the report, and the responsive proteostasis comparators:

- Lossless comparison: `evidence/naa10_comparator_profile_compare.json`
- Bounded inspection: `evidence/naa10_comparator_profile_inspect.json`
- Data source: declared `training_de_all_cell_groups.parquet`

`Naa10` had 17,259 measured features and `0` significant positive or negative features at BH < 0.05. Pairwise similarity between Naa10 and the report-named peers was near zero: Pearson/cosine values ranged from about `-0.024` to `+0.024`, with no significant-feature intersections because Naa10 had no significant features. A full eligible-neighbor projection over all 1,674 training perturbations also yielded only weak whole-profile neighbors, with best Pearson about `0.074`.

That profile evidence made Naa10 useful mainly as a buffered NatA-family boundary, not as a donor for a large transcriptional program.

## Synthesis

I weighted the direct NatA-family evidence downward from a definite `Naa15 = Naa10` equivalence because NAA15 is the ribosome-anchoring auxiliary subunit, NAA10 is catalytic, NAA15 has possible NAA16 bypass rather than NAA12 bypass, and NAA15 loss leaves pre-existing NatA-installed protein states that may only partially turn over by harvest. Those differences make a few DEGs plausible.

I nevertheless kept the forecast at the zero-count mode because:

- the exact focal class has a strong zero base rate in the training endpoint;
- the target bundle supports Naa15 expression but only partial functional-stock realization in the P16-to-P37/P44 window;
- the closest measured NatA perturbation, Naa10, was zero both in this focal class and across all measured neuronal classes; and
- the same assay did detect hundreds of focal DEGs for proteostasis comparators, so a large stress or proteotoxic RNA state is not the best prior for NatA loss here.

The final point is therefore:

```text
Naa15	0
```
