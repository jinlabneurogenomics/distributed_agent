# DEG-count prediction for `151 TH Prkcd Grin2c Glut`

## Question and endpoint

The held-out manifest contains one requested perturbation:

| target_name |
|---|
| Arnt2 |

I interpreted the requested value as the integer number of measured genes with
`pvals_adj < 0.05` in `151 TH Prkcd Grin2c Glut` after acute mosaic AAV-CRISPR
loss of the named target. The count is the assay-specific Wilcoxon/BH DEG burden
among recovered nuclei, not a direct viability, editing-efficiency, or target
importance endpoint. `Arnt2` is absent as both a `gene_target` in
`training_de_all_cell_groups.parquet` and a `target_name` in
`151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`; all expression-signature
comparisons below therefore use non-held-out perturbations only.

## Sources used

* Declared training endpoint:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
  This supplied the observed `n_degs` values for the non-held-out perturbations
  in the focal cell group.
* Declared differential-expression Parquet:
  `training differential-expression dataset`.
  I queried it only for non-held-out ARNT/AHR/HIF/NPAS/circadian PAS-family
  targets to measure FDR-0.05 and FDR-0.10 DEG burdens and the minimum adjusted
  p-value in the focal class and across other assayed neuronal classes.
* Run-local Distributed Agents manifests:
  `task_bindings.json`, `coverage.json`, `measurement_registry.json`, and
  `capabilities.json`. The scalar endpoint has no ranked supervision, so the
  Perturb-seq ranking workbench, graph predictive-review operation, and
  ordering validator were not task-available. I did not read the same-experiment
  Finding, Claim, graph, or report corpus for `Arnt2`, because those corpus
  surfaces are alternate representations of the original experiment and could
  expose information held out of the declared DEG-count inputs.
* External literature from PubMed:
  Michaud et al. 2000, DOI `10.1016/s0925-4773(99)00328-7`, PMID `10640708`;
  Hosoya et al. 2001, DOI `10.1046/j.1365-2443.2001.00421.x`, PMID `11318878`;
  Liu et al. 2003, DOI `10.1074/jbc.M304489200`, PMID `12947113`;
  Bersten et al. 2014, DOI `10.1371/journal.pone.0085768`, PMID `24465693`;
  Turer et al. 2018, DOI `10.1242/dmm.035451`, PMID `30563851`; and
  Rossi et al. 2021, DOI `10.1038/s41598-021-86041-4`, PMID `33758288`.

## Computational calibration

The focal training distribution is heavily zero-inflated. Among 1,674
non-held-out training perturbations, 469 have any DEG at FDR 0.05; the mean is
14.05, the median is 0, the 75th percentile is 1, and the 95th percentile is 18.
This makes an exactly zero prediction the calibrated baseline unless a target
has a close in-dataset analog with a nonzero response or a mechanism that should
produce a broad survivor-state transcriptome in this thalamic class.

For ARNT2, the relevant non-held-out in-dataset perturbations were the ARNT/AHR,
HIF, NPAS, and PAS-circadian genes present in the training CSV. I queried the
Parquet for these `gene_target` values:

```sql
select gene_target, group_name,
       count(*) as n_rows,
       sum(pvals_adj < 0.05) as n_fdr05,
       sum(pvals_adj < 0.10) as n_fdr10,
       min(pvals_adj) as min_padj,
       avg(n_pert_matched) as pert,
       avg(n_ctrl_matched) as ctrl
from read_parquet(...)
where gene_target in (...)
group by gene_target, group_name;
```

In the focal class, all of the most direct ARNT2-complex and HIF/AHR-branch
analogs were empirical nulls:

| training target | `n_degs` | focal FDR < 0.10 | minimum focal `pvals_adj` | matched perturbed nuclei | interpretation for Arnt2 |
|---|---:|---:|---:|---:|---|
| `Arnt` | 0 | 0 | 1.000 | 209 | closest paralog/ARNT-class partner; no measured focal response |
| `Ahr` | 0 | 0 | 0.221 | 93 | tests the AHR-ARNT signaling branch; no FDR signal |
| `Ahrr` | 0 | 0 | 1.000 | 159 | AHR-pathway repressor; no focal response |
| `Hif1a` | 0 | 0 | 0.306 | 175 | oxygen-responsive bHLH-PAS alpha factor; no focal response |
| `Npas3` | 0 | 0 | 1.000 | 198 | neuronal PAS transcription factor able to use ARNT2 partners; no focal response |

The broader PAS/circadian controls were weak except for `Bmal1`: `Bmal2` had 0
focal DEGs, `Clock` had 3, `Cry1` had 1, `Cry2` had 3, and `Bmal1` had 103. I
treated `Bmal1` as a counterexample showing that a PAS-family transcription
factor can be visible in this assay, not as the best quantitative proxy for
`Arnt2`, because BMAL1 is the core circadian partner of CLOCK/NPAS2 while ARNT2
is the neuronal partner for SIM1 and NPAS4 and can substitute in HIF/AHR-type
heterodimers.

The all-cell check pointed the same way for the closest branch: `Arnt`,
`Ahr`, `Ahrr`, `Hif1a`, `Bmal2`, and `Npas3` had zero FDR-0.05 DEGs in every
assayed neuronal class in the training Parquet. `Bmal1` and `Clock` were
visible in `151 TH Prkcd Grin2c Glut`, but they represent the circadian module
more than the ARNT2-SIM1/NPAS4 module.

## Target-specific reasoning

### `Arnt2`

ARNT2 is a neuronal bHLH-PAS dimerization partner. Embryonic work shows a strong
SIM1-ARNT2 requirement for paraventricular and supraoptic hypothalamic
neuroendocrine differentiation: Michaud et al. showed that SIM1 and ARNT2
co-express, dimerize in vitro, and are required for the same PVN/SON endocrine
lineages, and Hosoya et al. showed that germline `Arnt2` mutants die soon after
birth with loss of several PVN/SON secretory neuron classes. Liu et al. further
identified SIM1/ARNT2 transcriptional targets in a neuronal induction system,
and Turer et al. found that a viable hypomorphic `Arnt2` allele impairs
SIM1-dependent transcription and produces a hypothalamic feeding phenotype.
ARNT2 also partners with NPAS4 in neuronal activity-dependent transcription:
Bersten et al. showed that human ARNT2/NPAS4 variants can disrupt NPAS4 reporter
and BDNF activation, and Rossi et al. connected truncating NPAS3/NPAS4 variants
to loss of heterodimerization with ARNT2.

That biology makes `Arnt2` a real neuronal regulator, but it does not transfer
cleanly to a broad 3-4 week acute CRISPR DEG burden in postnatal
`151 TH Prkcd Grin2c Glut` neurons. The strongest SIM1/ARNT2 evidence concerns
embryonic generation of PVN/SON hypothalamic secretory neurons; the focal atlas
class is a thalamic glutamatergic class, and the assay perturbs postmitotic
neurons long after those developmental windows. NPAS4-dependent ARNT2 biology
is activity-regulated and target-gene-specific, but `Npas4` itself was not in
the visible training set, and the assayed neighboring PAS factors `Npas3`,
`Arnt`, `Ahr`, and `Hif1a` were complete focal nulls, with no genes even at FDR
0.10.

Therefore the causal transfer chain is weak at the propagation/context stage:
the intervention should impair ARNT2 protein, but the best-established
downstream programs are SIM1 developmental hypothalamic programs or
activity-induced NPAS4 programs rather than a constitutive limiting program in
the focal thalamic population. The exact ARNT/AHR/HIF/NPAS training
perturbations place the expected response at the zero/nonzero boundary, and
their lack of subthreshold FDR-0.10 structure argues against assigning a small
positive count. I predict `0` DEGs.

## Limits and uncertainty

The prediction is extrapolative because no held-out `Arnt2`, `Sim1`, or `Npas4`
signature is present in the declared training data. `Arnt` is the nearest
assayed ARNT-class paralog, but it is not fully equivalent to the
neuron-enriched ARNT2-SIM1 or ARNT2-NPAS4 complexes. Conversely, the
SIM1/ARNT2 mouse evidence is decisive for embryonic hypothalamic PVN/SON
development but imperfect for acute mosaic loss in recovered juvenile thalamic
neurons. A small nonzero count of a few genes would be plausible if ARNT2
controls an activity-dependent NPAS4 program in this cell group, but the
in-dataset HIF/AHR/ARNT/NPAS and circadian-PAS calibration did not justify
moving off the modal value of zero.
