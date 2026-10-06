# DEG-count prediction for held-out target Med12

## Question and endpoint

The requested held-out perturbation set contains one target, `Med12`, and the
requested endpoint is the integer number of measured genes with
`pvals_adj < 0.05` after that knockout in `151 TH Prkcd Grin2c Glut` cells.
I treated `151 TH Prkcd Grin2c Glut` as the focal thalamic glutamatergic class
named in the dataset, not as a tyrosine-hydroxylase label. `Med12` was absent
from both the supplied focal training-count CSV and the summarized training
feature table, so the prediction is a transfer from non-held-out targets rather
than a reused observation.

## Sources used

- Direct endpoint table:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
  This is the direct observed `pvals_adj < 0.05` count for visible training
  perturbations in the focal cell group.
- Direct differential-expression Parquet:
  `training differential-expression dataset`.
  I queried exact focal-cell rows for visible Mediator perturbations to inspect
  which genes crossed the FDR boundary and their directions.
- Declared `dataset.perturbseq_features` summary:
  `perturbseq_feature_workbench.py summarize` wrote
  `evidence/features.parquet`; it aggregated all non-held-out Parquet rows into
  target-level features including total all-cell `n_fdr_005`, `n_fdr_010`, and
  log-fold-change/Wilcoxon-score summaries.
- Same-experiment semantic corpus:
  `perturbai-july-260713-sourceguard-1773-v1`, queried with
  `corpus.findings` for `Cdk8`, `Med13`, `Med13l`, `Med15`, and `Med23`.
  These Findings are curated interpretations of the same Perturb-seq
  experiment, not independent replication.
- External literature from PubMed for Mediator biology:
  Fant and Taatjes 2018, DOI `10.1080/21541264.2018.1556915`, reviewed the
  CDK8/CDK19 Mediator kinase module and the roles of MED12, MED13, CCNC and
  CDK8/CDK19 in signal-responsive transcription. Chao et al. 2024, DOI
  `10.1016/j.molcel.2024.09.001`, showed structurally that MED12 and MED13
  help anchor the CDK8 kinase module to core Mediator and that MED13 can
  occlude RNA Pol II/MED26 binding. Kim et al. 2006, DOI
  `10.1074/jbc.M602696200`, identified MED12 as the Mediator interface used by
  beta-catenin for Wnt target-gene activation. Rocha et al. 2010, DOI
  `10.1242/dev.053660`, showed that mouse Med12 hypomorphs impair early
  development and Wnt/planar-cell-polarity signaling. Nizon et al. 2019, DOI
  `10.1038/s41436-019-0557-3`, and Caro-Llopis et al. 2016, DOI
  `10.1038/pr.2016.162`, support the neurodevelopmental dosage sensitivity of
  MED12/MED13L kinase-module genes in humans.

## Quantitative calibration

The endpoint distribution among 1,674 visible focal-cell training perturbations
is highly zero-inflated: the median `n_degs` is 0, only 469 targets are
nonzero, the 95th percentile is 18, and rare outliers such as `Uba5`, `Tpr`,
`Sin3a`, `Rnpc3`, `Zbtb7a`, `U2af2`, and `Psmb4` range from hundreds to 2,677
DEGs. The feature workbench confirmed that the all-cell FDR burden is the
training feature most aligned with focal `n_degs`, but it cannot score Med12
directly because Med12 has no expression signature in the held-out inputs.

The visible Mediator-family anchors had the following focal endpoint counts and
all-cell burdens:

| perturbation | focal `n_degs` | all-cell FDR<0.05 rows | focal FDR<0.10 rows | matched perturbed nuclei in 151 |
| --- | ---: | ---: | ---: | ---: |
| `Cdk8` | 0 | 0 | 0 | 192 |
| `Med13l` | 1 | 2 | 1 | 200 |
| `Med13` | 11 | 12 | 14 | 154 |
| `Med23` | 13 | 14 | 20 | 160 |
| `Med15` | 19 | 19 | 26 | 158 |

This makes a zero for Med12 unlikely, because three different visible Mediator
subunits converged on the focal cell class, but it also rules against a
large chromatin-regulator-like prediction. Even the productive Mediator
perturbations stayed in a narrow low-double-digit range, and their all-cell
burdens were essentially exhausted by the focal class.

The exact focal DE rows showed a shared, mostly down-regulated thalamic neuronal
module:

- `Med13`, `n_degs=11`: `Prkcd`, `Grin2b`, `Plekhg1`, `Atp2a2`, `Lrrtm1`,
  `Pcp4`, `Grm1`, `Ildr2`, `Ramp3`, and `Kcnc2` were down at FDR<0.05, while
  `Scnm1` was up. `Adgrb1`, `Atp2b1`, and `Zmat4` were just above the endpoint
  cutoff at FDR 0.077-0.079.
- `Med15`, `n_degs=19`: `Atp2b1`, `Lrrc7`, `Ptpn3`, `Plekhg1`, `Ntng1`, `Nin`,
  `Atp2a2`, `Lef1`, `Grm1`, `Adgrb1`, `Gabra4`, `Kcnc2`, `Hook1`, `Pcp4`,
  `Prkcd`, `Sh3d19`, `Ildr2`, `Nell1`, and `Trim9` were down at FDR<0.05.
- `Med23`, `n_degs=13`: `Prkcd`, `Grm1`, `Pcp4`, `Lef1`, `Atp6ap2`,
  `Plekhg1`, `Atp2b1`, `Amotl1`, `Grin2b`, `Ptpn3`, `Atp2a2`, `Nrxn1`, and
  `Lrrtm1` were down at FDR<0.05.
- `Med13l`, `n_degs=1`: only `Grm1` was significant in the focal group.
- `Cdk8`, `n_degs=0`: no focal genes crossed FDR<0.10 despite having the
  largest recovered focal perturbed-cell count among these analogs.

The same-experiment corpus independently summarized this same pattern as
selective convergence of `Med13`, `Med15`, and `Med23` on a 151-cell
Prkcd/Grm1/Pcp4/Plekhg1/Atp2a2/Atp2b1 down-module, with `Med13l` nearly flat
and `Cdk8` nonconvergent.

## Med12 transfer rationale

The causal transfer chain I used was:

`Med12` CRISPR loss-of-function -> impaired MED12 scaffold and signal-input
functions in the Mediator kinase module -> altered CKM/core-Mediator
regulation at a restricted set of thalamic neuronal transcriptional programs ->
survival-conditioned P37-P44 snRNA-seq DE among recovered `151 TH Prkcd Grin2c
Glut` nuclei -> FDR-thresholded DEG count.

`Med13` is the closest visible same-module scaffold perturbation. MED12 and
MED13 cooperate structurally in the CKM, so a MED12 perturbation should affect
some of the same Mediator-dependent loci rather than phenocopying an unrelated
target. The direction expected from the visible productive Mediator analogs is
same-outcome: reduced expression of thalamic synaptic, receptor,
calcium-handling, and subtype-identity transcripts. That argues for a nonzero
Med12 prediction anchored near `Med13=11`.

`Med15` and `Med23` are positive but imperfect analogs. They are Mediator
subunits outside the MED12/MED13 kinase-module scaffold, yet in this exact
cell group their FDR genes overlapped the `Med13` module in the same direction,
and their counts, 19 and 13, set the upper half of the relevant local range.
I therefore used them to move Med12 above the one-gene and zero counterexamples
but not far above 20.

`Med13l` and `Cdk8` are counterexamples. `Med13l` is a MED13 paralog and a
neurodevelopmental disease gene, but postnatal sparse CRISPR in this assay
produced only `Grm1` in the focal endpoint. `Cdk8` is in the same CKM and is
required for many stimulated kinase-module functions, but its visible
postnatal neuronal profile was completely FDR-flat. These two targets show
that membership in the CKM, human neurodevelopmental relevance, or beta-catenin
pathway proximity is not sufficient for a broad 151-cell DEG response.

The external Wnt literature raises, but does not dominate, the Med12 estimate.
MED12 can directly support beta-catenin-dependent Wnt transcription, and Med12
hypomorphic mice have strong embryonic developmental phenotypes. In the visible
postnatal Perturb-seq data, however, `Cdk8` did not recover the Ctnnb1/Tcf7l2
thalamic Wnt program and `Med13` recovered only a small subset without a broad
canonical Wnt-feedback signature. I therefore treated embryonic Wnt and
congenital phenotypes as priors for a real transcriptional role, not as a
reason to predict hundreds of DEGs.

Putting these together, I predicted a low double-digit focal response:
`Med12 = 14` DEGs. This is close to the median of the productive Mediator
analogs (`Med13`, `Med23`, `Med15`) and above the `Med13l`/`Cdk8` null branch.

## Limits

No declared input directly observes Med12 in this run; the Med12 expression
signature and true DEG count were absent from the training Parquet, training
count CSV, and summarized feature table. The internal corpus was used only for
visible training perturbations, and because it is another representation of the
same Perturb-seq experiment it is not replication. The visible Mediator set is
small and incomplete: `Ccnc`, `Cdk19`, `Med12`, and `Med12l` were not available
as visible analogs, so the prediction extrapolates from `Med13`, `Med13l`,
`Cdk8`, `Med15`, and `Med23`. Finally, the predicted count is an
assay-thresholded, power-dependent DEG burden in recovered nuclei; it should
not be read as the strength of Med12 editing, as a viability estimate, or as a
complete measure of MED12 biology in embryonic or glial contexts.
