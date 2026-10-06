# Task

The manifest for this run contains one held-out target, `Arnt2`.  I interpreted the
task as a point prediction of how many measured genes would satisfy
`pvals_adj < 0.05` in `151 TH Prkcd Grin2c Glut` after acute AAV-CRISPR
loss-of-function of `Arnt2`.  The target itself was completely held out, so its
own DEG count and Wilcoxon score vector were not in either training input.

The only ambiguity I had to resolve was how much weight to put on severe
germline/developmental `Arnt2` phenotypes.  I downweighted those for the endpoint
because this experiment perturbs sparse postmitotic juvenile neurons from P16 to
P37-44 and measures basal nuclear RNA, not embryonic hypothalamic specification,
hypoxia, ligand stimulation, or activity-driven immediate-early induction.

# Sources Used

- `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`: exact observed
  `n_degs` values for the focal cell group.
- `training_de_all_cell_groups.parquet`: focal-cell Wilcoxon score profiles and
  matched perturbed/control cell counts for represented comparator perturbations.
- Distributed Agents same-experiment corpus release
  `perturbai-july-260713-sourceguard-1773-v1`, especially the `Arnt`, `Ahr`,
  `Ahrr`, `Hif1a`, `Npas3`, and `Bmal1` reports and their synthesized claims.
- PubMed literature searches, used to place `Arnt2` in bHLH-PAS biology:
  - Michaud et al. 2000, PMID 10640708, DOI `10.1016/s0925-4773(99)00328-7`.
  - Hosoya et al. 2001, PMID 11318878, DOI `10.1046/j.1365-2443.2001.00421.x`.
  - Keith et al. 2001, PMID 11381139, DOI `10.1073/pnas.121494298`.
  - Liu et al. 2003, PMID 12947113, DOI `10.1074/jbc.M304489200`.
  - Bersten et al. 2014, PMID 24465693, DOI `10.1371/journal.pone.0085768`.
  - Turer et al. 2018, PMID 30563851, DOI `10.1242/dmm.035451`.
  - Sun et al. 2022, PMID 36343253, DOI `10.1073/pnas.2208804119`.

# Dataset Calibration

The focal training count table has 1674 non-held-out perturbations.  The endpoint
is extremely zero-inflated: 1205 of 1674 perturbations have `n_degs = 0`, the
median is 0, the 75th percentile is 1, and the 95th percentile is 18.  I
therefore treated zero as the natural prior for a perturbation unless the
specific within-screen analogs or gene biology pointed to a detectable program.

For Arnt-related bHLH-PAS/xenobiotic/circadian comparators, I read the focal
rows from the parquet and counted genes with `pvals_adj < 0.05`.  Each of these
profiles had 17,259 measured genes and 23,679 matched controls in `151 TH Prkcd
Grin2c Glut`.

| training perturbation | focal n_degs | matched perturbed nuclei | relevance to Arnt2 |
|---|---:|---:|---|
| `Arnt` | 0 | 209 | closest represented paralog / ARNT-family class II bHLH-PAS dimerization partner |
| `Ahr` | 0 | 93 | ARNT-dependent xenobiotic receptor branch |
| `Ahrr` | 0 | 159 | AHR feedback repressor |
| `Hif1a` | 0 | 175 | HIF alpha partner for ARNT/ARNT2-like oxygen response |
| `Npas3` | 0 | 198 | neural bHLH-PAS factor; useful same-fold comparator |
| `Bmal2` | 0 | 182 | BMAL paralog in the bHLH-PAS family |
| `Bmal1` | 103 | 152 | CLOCK/BMAL circadian positive control, not an ARNT2 partner |
| `Clock` | 3 | 162 | circadian bHLH-PAS positive control |
| `Rora` | 278 | 139 | RORE/circadian nuclear-receptor counterexample |
| `Rorb` | 0 | 162 | RORE family counterexample |
| `Rorc` | 0 | 195 | RORE family counterexample |

I also compared the `Arnt` focal Wilcoxon-score vector against the represented
PAS/circadian comparators with the Distributed Agents runtime `profile_neighbors` tool
using `scores` as signed features and `pvals_adj < 0.05` as significant
features.  `Arnt` itself had zero FDR-significant features.  The pairwise
whole-profile similarities were background scale: `Arnt` vs `Ahr` Pearson
0.007, vs `Hif1a` 0.023, vs `Ahrr` 0.002, vs `Npas3` -0.002, vs `Bmal1`
-0.004, and vs `Clock` -0.0005.  The top-100 signed-tail overlaps were only
0 to 2 genes for the mechanistically closest ARNT/AHR/HIF/Npas comparators.
This supports the Distributed Agents corpus finding `Arnt:F004`: in the complete
perturbation universe, the Arnt score vector had no coherent positive or
negative neighbors and only approximately 0.02 to 0.03 absolute correlations to
its nearest profiles.

# Target Reasoning

## Arnt2

`Arnt2` is a neural bHLH-PAS class II transcription factor.  Its strongest
curated developmental biology is the SIM1-ARNT2 axis: ARNT2 dimerizes with SIM1
in vitro and is co-expressed with SIM1 in the developing PVN/SON; constitutive
mouse `Arnt2` knockout causes perinatal death and loss of hypothalamic
neurosecretory neurons in the same developmental lineages affected by `Sim1`
loss; inducible SIM1/ARNT2 can drive candidate hypothalamic target genes; and a
viable hypomorphic `Arnt2` allele impairs SIM1-dependent transcription and
causes hyperphagic obesity.  ARNT2 can also form functional NPAS4/ARNT2
heterodimers relevant to activity-dependent inhibitory-synapse transcription.

Those mechanisms argue that `Arnt2` is a real neuronal regulator, but they do
not automatically predict a broad basal P16 CRISPR signature.  The decisive
SIM1 phenotypes are embryonic neuroendocrine specification phenotypes, whereas
the assayed nuclei are sparse postmitotic juvenile neurons sampled 3-4 weeks
after viral editing.  The NPAS4 mechanism is stimulus/activity-gated, and this
screen was not a depolarization paradigm.  The training set also lacked direct
`Sim1`, `Sim2`, and `Npas4` perturbations in the focal count table, so I could
not transfer from the two most specific ARNT2 partner axes.

The represented within-dataset analogs all point lower than the germline
literature would suggest.  In the focal cell group, the closest represented
ARNT-family perturbation, `Arnt`, had `n_degs = 0`.  The same-experiment
Distributed Agents corpus found that `Arnt` was a pan-neuronal transcriptional null
across all 22 recovered cell groups and that its canonical AHR and HIF target
programs were absent.  Its direct pathway comparators were also exactly flat in
151 cells: `Ahr = 0`, `Ahrr = 0`, and `Hif1a = 0`.  `Npas3 = 0` and `Bmal2 = 0`
add that multiple non-circadian bHLH-PAS perturbations landed in the same flat
class.  The nonzero `Bmal1` and `Clock` profiles are important counterexamples:
they show that this snRNA-seq/Wilcoxon pipeline could detect PAS-family
transcription-factor output, but their circadian CLOCK/BMAL1 program was
uncoupled from `Arnt`, `Ahr`, `Hif1a`, and `Npas3` in the corpus and in the
near-zero score correlations.

Taken together, the prediction is within-data driven: the most relevant
represented analog is exactly zero and no represented ARNT/AHR/HIF-related
branch produced FDR genes under basal juvenile neuronal conditions.  External
knowledge keeps `Arnt2` from being treated as an inert gene, but it mainly
places the strong biology in missing contexts: embryonic hypothalamic
development, ligand/hypoxic activation, and NPAS4-coupled activity responses.
I therefore predict no measured gene will pass FDR 0.05 for acute `Arnt2` loss
in `151 TH Prkcd Grin2c Glut`.

Predicted `n_degs`: **0**.

# Limits

- `Arnt2` was held out and absent from the DEG parquet, so no target-specific
  expression signature was available.
- The strongest biological partners, `Sim1`, `Sim2`, and `Npas4`, were not
  available as direct training perturbations in the focal count table; the
  decision has to extrapolate from `Arnt`, `Ahr`, `Ahrr`, `Hif1a`, and `Npas3`.
- `Arnt2` is more neuronally specialized than `Arnt`, so `Arnt = 0` is an
  imperfect paralog comparison.
- The endpoint is assay- and power-dependent.  It can miss protein-level,
  electrophysiologic, chromatin, or stimulus-evoked changes that do not appear
  as steady-state nuclear RNA changes at this sampling time.
- Germline `Arnt2` null and hypomorphic phenotypes are developmental or chronic;
  translating them to sparse juvenile CRISPR loss is the largest biological
  extrapolation.
