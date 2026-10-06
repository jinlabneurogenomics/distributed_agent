# DEG-count prediction trace

## Question and endpoint

The held-out perturbation manifest for this run contains one target:

| target_name |
|---|
| Dcx |

I interpreted the task as a point prediction of `n_degs` for an acute AAV
CRISPR-Cas9 loss-of-function perturbation of `Dcx` in the `151 TH Prkcd Grin2c
Glut` neuronal cell group. `n_degs` is the count of measured genes, including
the perturbed target transcript itself when applicable, with BH-adjusted
Wilcoxon `pvals_adj < 0.05` in the perturbed nuclei versus matched
non-targeting controls. The withheld `Dcx` contrast and its DEG count are absent
from both supplied inputs, so the endpoint is directly observed for training
perturbations only and absent for the requested target.

Two ambiguities were resolved as follows.

- Isolated self-transcript FDR hits in training were counted as part of the
  assay endpoint, because the supplied training CSV counted them, but I treated
  them as weak evidence for a downstream `Dcx` response. The dataset portrait
  notes that target-mRNA loss is QC context only: weak target RNA loss does not
  imply failed editing, and strong target RNA loss does not make a knockout
  biologically stronger.
- I treated evidence from embryonic or germline `Dcx` mouse phenotypes as
  mechanistic prior information, not as a direct same-endpoint proxy, because
  this experiment edits postmitotic neurons at P16 and samples recovered nuclei
  3-4 weeks later.

## Sources

- Declared training endpoint:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared differential-expression Parquet:
  `training differential-expression dataset`.
- Requested-target manifest:
  `single-target request for Dcx`.
- Run-local Distributed Agents metadata: `task_bindings.json`, `coverage.json`,
  `measurement_registry.json`, and the PerturbAI atlas dataset portrait.
- PubMed, queried 2026-09-02, for external `Dcx`/doublecortin mouse and human
  mechanism. I did not use same-experiment Findings or Claim summaries for
  `Dcx`; the target is held out from the supplied experiment, and the Parquet is
  the authoritative source for all exact training DE statistics used here.

Key external citations:

- Lambert de Rouvroit and Goffinet 2001, doi:10.1016/s0925-4773(01)00396-3,
  reviewed neuronal migration and placed doublecortin with LIS1 in the
  microtubule-dependent nucleokinesis branch rather than in the Reelin terminal
  patterning branch.
- Kappeler et al. 2007, doi:10.1002/cne.21170, showed hippocampal and corpus
  callosal abnormalities in `Dcx` knockout mice.
- Deuel et al. 2006, doi:10.1016/j.neuron.2005.10.038, and Koizumi et al.
  2006, doi:10.1016/j.neuron.2005.10.040, showed partially redundant
  `Dcx`/`Dclk1` functions in mouse neuronal migration and axon outgrowth.
- Tanaka et al. 2006, doi:10.1093/cercor/bhk005, showed cooperation between
  `Dcx` and `Dclk1` in murine hippocampal development.
- Kerjan et al. 2009, doi:10.1073/pnas.0812687106, showed dosage-dependent
  hippocampal lamination and seizure phenotypes when `Dcx` and `Dclk2` were
  both lost.
- Khalaf-Nazzal et al. 2017, doi:10.1093/hmg/ddw370, and Stouffer et al. 2022,
  doi:10.1016/j.nbd.2022.105702, observed persistent CA3/hippocampal molecular,
  mitochondrial, Golgi, and excitability phenotypes in constitutive `Dcx`
  knockout mice.

## Quantitative calibration from the declared inputs

The focal training CSV contains 1,674 non-held-out perturbations. Its
`151 TH Prkcd Grin2c Glut` response-breadth distribution is sparse:
1,205/1,674 targets have `n_degs = 0`, the median is 0, 276 targets have exactly
one DEG, and the right tail is large but rare, with a 95th percentile of
18 DEGs and a maximum of 2,677.

I used `pyarrow.dataset` filters on `group_name == "151 TH Prkcd Grin2c Glut"`
and on selected `gene_target` values to read only focal rows for mechanistically
near training perturbations. For each selected target I counted FDR-significant
genes and separated the target transcript from downstream DEGs:

| training perturbation | focal n_degs | relevant focal expression-pattern evidence |
|---|---:|---|
| `Map1b` | 1 | only the `Map1b` self transcript was significant |
| `Mapt` | 1 | only the `Mapt` self transcript was significant |
| `Tuba1a` | 7 | self-transcript loss plus six induced tubulin paralogs: `Tubb3`, `Tubb2a`, `Tuba4a`, `Tubb4a`, `Tubb4b`, `Tubb5` |
| `Tuba4a` | 2 | self-transcript loss plus weak `Mast1` induction |
| `Tubb4b` | 1 | only the `Tubb4b` self transcript was significant |
| `Tubb5` | 1 | only the `Tubb5` self transcript was significant |
| `Stmn2` | 1 | only the `Stmn2` self transcript was significant |
| `Kif1a` | 1 | only the `Kif1a` self transcript was significant |
| `Kif1b` | 0 | no FDR-significant focal genes |
| `Kif2a` | 0 | no FDR-significant focal genes |
| `Kif3b` | 0 | no FDR-significant focal genes |
| `Kif5a` | 1 | only the `Kif5a` self transcript was significant |
| `Kif5c` | 1 | only the `Kif5c` self transcript was significant |
| `Dab1` | 0 | no FDR-significant focal genes |
| `Reln` | 0 | no FDR-significant focal genes |
| `Lrp8` | 0 | no FDR-significant focal genes |
| `Vldlr` | 0 | no FDR-significant focal genes |
| `Cdc42` | 1 | only the `Cdc42` self transcript was significant |
| `Actg1` | 1 | only the `Actg1` self transcript was significant |
| `Arx` | 0 | no FDR-significant focal genes |
| `Flnb` | 0 | no FDR-significant focal genes |
| `Ywhae` | 0 | no FDR-significant focal genes |
| `Dctn1` | 75 | broader sterol/lipid response including `Dctn1`, `Insig1`, `Msmo1`, `Hmgcs1`, `Cyp51`, `Hmgcr`, and `Fdft1` |

`Map1b`, `Mapt`, tubulin genes, `Stmn2`, and kinesins are the most direct
within-training cytoskeletal comparators: they either bind microtubules or
alter microtubule-dependent transport. Their focal signatures argue that
partial cytoskeletal perturbations in this cell group usually do not create a
large survivor-state transcriptomic footprint. `Tuba1a` is the main
counterexample, but it is a structural tubulin gene and produced a compact
tubulin-paralog compensation pattern rather than a broad stress response.
`Dctn1` is a more distant dynein/dynactin counterexample with 75 DEGs; I did
not transfer that larger count to `Dcx` because DCTN1 is a core retrograde
transport complex subunit, whereas DCX is a developmentally enriched MAP with
partial redundancy through doublecortin-like kinases.

`Reln`, `Dab1`, `Lrp8`, and `Vldlr` were used as migration/lamination pathway
counterexamples. They connect to neuronal positioning biologically, but their
intervention stage is the extracellular Reelin stop/patterning signal, not the
DCX microtubule-stabilizing nucleokinesis module. All four had zero focal
DEGs, making broad "neuronal migration gene" membership insufficient for a
positive prediction.

As another check, I read the row for measured gene `Dcx` across every visible
training perturbation in the focal class. Only 2/1,674 perturbations made `Dcx`
itself FDR-significant, `Qrich1` and `Rora`; none of the selected MAP, tubulin,
kinesin, Reelin, or small-GTPase analogs significantly regulated `Dcx`
(`pvals_adj = 1` for `Dcx` under `Map1b`, `Mapt`, `Tuba1a`, `Tuba4a`, `Tubb4b`,
`Tubb5`, `Kif1a`, `Kif1b`, `Kif2a`, `Kif3b`, `Kif5a`, `Kif5c`, `Dab1`,
`Reln`, and `Stmn2`). That does not measure `Dcx` knockout, but it argues
against a hidden within-dataset `Dcx`/doublecortin module lighting up in this
focal class.

## Dcx prediction

`Dcx` encodes doublecortin, a neuronal microtubule-associated protein important
for embryonic migration, hippocampal lamination, and axon growth. The strongest
mouse literature phenotypes come from constitutive `Dcx` loss or double mutants
with `Dclk1` or `Dclk2`, consistent with partial redundancy in the mouse
doublecortin family. This makes `Dcx` biologically real but predicts a small
acute perturb-seq footprint here: the intervention occurs after most thalamic
neuronal migration is complete, the sampled nuclei are postmitotic survivors,
and a single partial `Dcx` perturbation should not abolish the redundant MAP
module.

The decisive within-dataset evidence is that close cytoskeletal comparators
cluster at 0-1 DEGs and mostly show only their own knocked-down transcript,
while the broader tubulin-compensation counterexample `Tuba1a` reaches only
7 DEGs. I therefore predicted no coordinated downstream response and also did
not add a guaranteed one-DEG self-transcript effect, because `Dcx` expression
in this P37-44 thalamic glutamatergic class appears weak and is not repeatedly
detected as a regulated transcript across relevant training KOs.

Point prediction: `Dcx -> 0`.

## Limits

This prediction extrapolates from related cytoskeletal and migration genes
because no `Dclk1`, `Dclk2`, or `Pafah1b1/Lis1` training perturbation is present
in the focal count table. The best positive external evidence for `Dcx`
function comes from developmental or germline settings, so it may miss a
cell-autonomous postnatal role in thalamic neurons. Conversely, the Parquet
contains only recovered single-nucleus DE statistics; it cannot show earlier
selection, subcellular transport defects, dendritic defects, or altered
excitability unless those changes produce a sampled nuclear RNA signature that
passes FDR. The zero prediction should therefore be read as "no gene is expected
to pass this assay's FDR < 0.05 DEG-count endpoint", not as absence of DCX
biology.
