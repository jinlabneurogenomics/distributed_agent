# Cox6b1 DEG-count prediction

## Target and endpoint

- Target: `Cox6b1`
- Focal population: `151 TH Prkcd Grin2c Glut`
- Endpoint: count of measured genes with BH-adjusted Wilcoxon `p < 0.05`
- Prediction: `0`

## Evidence used

### Declared target biology

The one-row holdout manifest names `Cox6b1`, and `Cox6b1` is absent from the
declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` table.

The canonical Cox6b1 bundle is endpoint-blind and reports:

- Cox6b1 is an incorporated nuclear-encoded mitochondrial complex-IV subunit.
- Editing is expected to stop new Cox6b1 supply, while already assembled
  pre-edit complex IV initially persists.
- Primary-neuron turnover evidence places COX6B1 in a shorter-lived
  mitochondrial class, so 21-28 days after P16 editing should allow substantial
  but not necessarily complete depletion; respiratory supercomplex incorporation
  leaves a plausible persistent tail.
- The closest mouse phenotype evidence is germline/developmental rather than an
  acute P16-to-P37/P44 thalamic-neuron deletion, so severity is not directly
  transferable to this survivor-conditioned snRNA endpoint.
- Exact in-assay non-target expression is measurable but modest in the focal
  class: 9,769 of 23,679 non-target nuclei express Cox6b1
  (`41.26%`), with mean raw UMI `0.591`, mean log1p-CP10K `0.245`,
  and pseudobulk `37.03` CPM.

### Training count table

The declared thalamic training table contains 1,674 non-held-out targets. Its
burden is extremely sparse in this context: 1,205/1,674 rows are zero, the
median is `0`, the 75th percentile is `1`, and the mean is inflated by a small
high-burden tail.

I used same-complex or complex-IV assembly targets as the closest quantitative
training analogs:

| training target | n_degs |
| --- | ---: |
| Coa8 | 0 |
| Cox11 | 0 |
| Cox4i1 | 0 |
| Cox5a | 1 |
| Cox6a1 | 0 |
| Cox7b | 0 |
| Cox8a | 0 |

Those seven complex-IV analogs have mean `0.143`, median `0`, and maximum `1`.
The broader respiratory-chain set visible in the declared count table is also
bounded to singleton responses: 40 `Cox`/`Nduf`/`Uqcr`/`Sdha`/`Cyc1`/related
mitochondrial perturbations had mean `0.425`, median `0`, and maximum `1`.

### Matched Parquet inspection

I then inspected the declared
`training_de_all_cell_groups.parquet` rows for the same focal group and the
seven complex-IV analogs. Across all seven analogs, the only FDR 0.05 row was
the `Cox5a` self-transcript:

| training target | FDR 0.05 rows in `151 TH Prkcd Grin2c Glut` |
| --- | --- |
| Coa8 | none |
| Cox11 | none |
| Cox4i1 | none |
| Cox5a | Cox5a, logFC -1.2308, padj 5.39e-21 |
| Cox6a1 | none; Cox6a1 self was near-threshold at padj 0.0726 |
| Cox7b | none |
| Cox8a | none |

Extending the same check to 40 visible respiratory-chain and mitochondrial
targets found 17 FDR 0.05 rows total; 15 were self-transcripts. Thus a count of
`1` in this gene class usually reflected detectable loss of the assayed target
RNA, not a broader downstream survivor-state program.

The profile comparison of the seven direct complex-IV analogs used 17,259
shared measured features per node. Six nodes had no significant feature and
only Cox5a had a `1_to_9_significant_features` activity status. Pairwise
significant-program intersections were zero, and the caller-declared
complex-IV cohort showed no recurrent significant positive or negative program
overlap.

## Synthesis

Cox6b1 loss is biologically credible by harvest because new supply should be
blocked and the protein is not expected to be indefinitely stable. The
training measurements nevertheless show that acute sparse perturbation of
complex-IV subunits in this thalamic class usually does not produce a
measurable downstream DEG program among recovered nuclei. The count table and
Parquet rows put the best same-complex scale at `0` or a self-transcript-only
`1`.

For Cox6b1 specifically, exact focal expression is present but modest, and the
dataset portrait warns that measured self-transcript knockdown is not a reliable
measure of functional editing or response magnitude. If Cox6b1 itself crosses
FDR, the realized count could be `1`, but the closest same-complex profiles give
stronger support to no FDR 0.05 rows than to a singleton. I therefore choose the
integer point forecast:

`predicted_n_degs = 0`
