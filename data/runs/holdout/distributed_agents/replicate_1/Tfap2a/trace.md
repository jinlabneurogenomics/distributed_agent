# DEG-count prediction trace

## Question and endpoint

The requested prediction is the integer `n_degs` that would have been observed
for held-out `Tfap2a` in `151 TH Prkcd Grin2c Glut` cells, where `n_degs`
means the number of measured genes in that focal thalamic glutamatergic class
with a Benjamini-Hochberg-adjusted Wilcoxon p-value below 0.05 in perturbed
versus matched control nuclei.

`Tfap2a` was completely held out: I confirmed it has zero rows as a
`gene_target` in the declared differential-expression Parquet and is absent
from the focal-cell training endpoint CSV. I interpreted this as a pure
outcome-prediction task, not as a request for a ranked candidate list.

## Sources used

- Declared DE table:
  `training differential-expression dataset`.
  This is the direct same-experiment measurement surface for per-gene log fold
  changes and FDR-adjusted p-values among non-held-out perturbations.
- Declared training endpoint table:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
  This is the direct same-experiment source for observed `n_degs` in the focal
  cell group for 1,674 non-held-out targets.
- Declared requested-target table:
  `single-target request for Tfap2a`.
  It contains the single held-out target `Tfap2a`.
- Run-local task metadata: `task_bindings.json`, `coverage.json`,
  `capabilities.json`, and `measurement_registry.json`.
- Internal same-experiment corpus:
  `perturbai-july-260713-sourceguard-1773-v1`. I used `corpus.calibration` to
  confirm July atomic-Finding semantics, and a bounded `story-count` query on
  the nearest in-dataset developmental TF analogs. That query returned no
  atomic Findings for `Lmx1b`, `Foxa2`, `Pitx3`, `En1`, `Otx2`, `Rarb`,
  `Pax6`, `Sox2`, `Sox5`, `Phox2a`, or `Phox2b`, so no same-experiment report
  prose or packaged Finding changed the decision.
- External literature from PubMed:
  Brewer et al. 2004, DOI 10.1016/j.ydbio.2003.10.039, PMID 14975722;
  Li and Cornell 2006, DOI 10.1016/j.ydbio.2006.12.042, PMID 17258188;
  Schmidt et al. 2011, DOI 10.1016/j.ydbio.2011.04.011, PMID 21539825;
  Seberg et al. 2017, DOI 10.1371/journal.pgen.1006636, PMID 28249010;
  Nguyen et al. 2024, DOI 10.1242/dev.202095, PMID 38063857.

## Quantitative calibration from the focal endpoint

The focal training endpoint is highly sparse:

- 1,674 visible biological perturbations in the training CSV.
- 1,205/1,674 have `n_degs = 0`.
- Median `n_degs = 0`; 75th percentile = 1; 90th percentile = 2;
  95th percentile = 18.
- The large responses are a small tail of broad molecular-machinery and
  chromatin/splicing perturbations; for example `Uba5` = 2677, `Tpr` = 1768,
  `Sin3a` = 1433, `Rnpc3` = 868, and `Zbtb7a` = 841.

This made zero the baseline for a perturbation without focal postnatal
expression evidence or a close nonzero analog.

The closest biological neighborhood represented in training was made of
neural-crest, sympathetic/noradrenergic, craniofacial, melanocyte, and embryonic
neural-patterning regulators rather than AP-2 paralogs themselves:

| training perturbation | focal `n_degs` | focal signature details |
| --- | ---: | --- |
| `Alx1` | 0 | no focal FDR-significant genes; only 1 significant gene across all assayed cell groups |
| `Alx3` | 0 | no focal FDR-significant genes; only 1 significant gene across all assayed cell groups |
| `Alx4` | 0 | no significant genes in any assayed cell group |
| `Dlx3` | 0 | no significant genes in any assayed cell group |
| `Dlx6` | 0 | no significant genes in any assayed cell group |
| `Ebf1` | 0 | no significant genes in any assayed cell group |
| `Ebf2` | 0 | no focal FDR-significant genes; only 1 significant gene across all assayed cell groups |
| `Ebf3` | 0 | no significant genes in any assayed cell group |
| `En1` | 0 | no significant genes in any assayed cell group |
| `Foxa2` | 0 | no significant genes in any assayed cell group |
| `Gata3` | 0 | no significant genes in any assayed cell group |
| `Kit` | 0 | no focal FDR-significant genes; only 1 significant gene across all assayed cell groups |
| `Lmx1b` | 0 | no significant genes in any assayed cell group |
| `Msx2` | 0 | no focal FDR-significant genes; only 1 significant gene across all assayed cell groups |
| `Otx2` | 0 | no significant genes in any assayed cell group |
| `Pax6` | 0 | no significant genes in any assayed cell group |
| `Phox2a` | 0 | no significant genes in any assayed cell group |
| `Phox2b` | 0 | no significant genes in any assayed cell group |
| `Pitx3` | 0 | no significant genes in any assayed cell group |
| `Rarb` | 0 | no significant genes in any assayed cell group |
| `Robo1` | 1 | one focal DEG and one DEG in `052 Pvalb Gaba` |
| `Robo2` | 0 | no focal DEG; three one-gene signatures in other classes |
| `Sox10` | 0 | no significant genes in any assayed cell group |
| `Sox2` | 2 | only `Tnnt1` and `Stam` in the focal class |
| `Sox5` | 2 | only `Dgkh` and `Tnnt1` in the focal class |
| `Sox9` | 0 | no significant genes in any assayed cell group |
| `Tfap4` | 0 | no significant genes in any assayed cell group |

I also queried focal rows in which the measured genes were AP-2/neural-crest
markers. Among all 1,674 visible perturbations in the focal class, the minimum
adjusted p-value was 1.0 for measured `Tfap2a`, `Tfap2b`, `Tfap2c`, `Tfap2d`,
and `Tfap2e`; `Alx1`, `Alx3`, and `Alx4` likewise had minimum adjusted
p-values of 1.0. `Ascl1` had one weak significant increase under `Tpr`
perturbation, but that was in a very broad `Tpr` response and was not an
AP-2-like signature.

These Parquet summaries were computed by filtering the declared table to
`group_name == "151 TH Prkcd Grin2c Glut"` and to a narrow set of mechanistic
analogs or AP-2/neural-crest marker `names`, then counting
`pvals_adj < 0.05` by `gene_target`. For the all-cell-group check I used the
same threshold grouped by `gene_target` and `group_name`.

## Target-specific biological reasoning

### `Tfap2a`

`Tfap2a` encodes AP-2alpha, a sequence-specific transcription factor with
well-established roles in embryonic neural crest, surface ectoderm,
craniofacial development, and other neural-crest-derived lineages. Neural
crest-specific deletion in mouse causes neural-crest-related defects
(Brewer et al. 2004), AP-2alpha/AP-2beta are required for survival of
sympathetic progenitors and sympathetic neurons (Schmidt et al. 2011), AP-2
paralogs act redundantly in neural-crest and non-neural ectoderm derivatives
(Li and Cornell 2006), and AP-2 paralogs cooperate in melanocyte and midfacial
programs, including TFAP2 activation of `Alx1`, `Alx3`, and `Alx4` expression
in midfacial neural crest cells (Seberg et al. 2017; Nguyen et al. 2024).

The causal transfer chain for the requested experiment is weak, however:

1. The intervention is an acute, mosaic CRISPR loss of function at P16, not a
   germline or Wnt1-Cre embryonic neural-crest knockout.
2. The requested assayed population is recovered P37-P44
   `151 TH Prkcd Grin2c Glut` thalamic glutamatergic nuclei, not premigratory
   neural crest, sympathetic ganglion, melanocyte, or craniofacial mesenchyme.
3. The strongest external AP-2 phenotypes occur during lineage specification,
   survival, or migration before the postnatal perturbation window.
4. Training perturbations of nearby lineage-specification genes were almost
   uniformly silent in the same focal class: `Alx1`, `Alx3`, `Alx4`, `Lmx1b`,
   `Foxa2`, `Pitx3`, `Phox2a`, `Phox2b`, `Sox10`, `Gata3`, `Dlx3`, `Dlx6`,
   `Ebf1`, `Ebf2`, `Ebf3`, `Pax6`, `Otx2`, and `Rarb` all had focal
   `n_degs = 0`.
5. No AP-2 measured gene was detectably regulated in the focal class across
   the training perturbations, and no `Alx1/3/4` module was detectably induced
   or suppressed there.

The small nonzero counterexamples, `Sox2` = 2, `Sox5` = 2, and `Robo1` = 1,
show that a developmental regulator can occasionally produce one or two
focal DEGs in this assay. They do not provide a strong positive analog for
`Tfap2a`: their focal signatures involve isolated genes rather than an
AP-2/ALX/neural-crest or noradrenergic program, and they are not obligate
partners of AP-2alpha in postnatal thalamic glutamatergic neurons.

I therefore treated the external literature as establishing TFAP2A biology but
not as same-endpoint transfer evidence for a broad DEG response in this
experimental context. The within-dataset analogs are all at or extremely close
to zero, so the best point prediction is:

| target_name | predicted_n_degs |
| --- | ---: |
| `Tfap2a` | 0 |

## Limits and uncertainty

This is an extrapolation from functionally related developmental genes rather
than a paralog-matched training perturbation; `Tfap2b`, `Tfap2c`, `Tfap2d`, and
`Tfap2e` were not visible training targets in the focal endpoint CSV. The
within-dataset report corpus did not contain target-specific AP-2 Findings for
the available analog genes, so the decision leans on direct Parquet summaries
and external embryonic/neural-crest biology. A very small one-gene or two-gene
response would be plausible given `Robo1`, `Sox2`, and `Sox5`, but the evidence
does not justify moving the point estimate away from the dominant zero class.
