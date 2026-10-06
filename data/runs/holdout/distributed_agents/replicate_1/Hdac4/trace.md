# DEG-count prediction trace

## Question and endpoint

The requested prediction is the integer number of genes expected to pass
Benjamini-Hochberg FDR 0.05 in the `151 TH Prkcd Grin2c Glut` focal class after
acute P16 AAV-CRISPR loss of each held-out perturbation. The requested manifest
contains one target, `Hdac4`, and I preserved that order in `answer.txt`.

I treated the count as an assay-specific focal-cell DEG burden among recovered
snRNA-seq nuclei, not as a viability, developmental-essentiality, or editing
efficiency endpoint. I therefore calibrated against the supplied
`151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` counts and against focal-cell
rows in `training_de_all_cell_groups.parquet`; external biology was used only
to choose meaningful assayed analogs and counterexamples for the held-out gene.
`Hdac4` was confirmed to be a held-out perturbation and has no focal signature
or training count in the supplied inputs.

## Sources used

- Declared DE Parquet:
  `training differential-expression dataset`.
  I queried focal-cell rows for HDAC4-related assayed genes and counted rows
  with `pvals_adj < 0.05` and `< 0.10`; the focal-cell counts matched the
  supplied training CSV.
- Declared focal training counts:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
  This file contains 1,674 unique non-held-out perturbations; 1,205 have 0
  focal DEGs, the median count is 0, and the mean is 14.1 because a few broad
  perturbations such as `Uba5`, `Tpr`, and `Sin3a` are very large.
- Requested-target manifest:
  `single-target request for Hdac4`.
  It contains exactly `Hdac4`.
- PerturbAI July same-experiment semantic corpus,
  `perturbai-july-260713-sourceguard-1773-v1`. I used its bounded Findings and
  Evidence for `Hdac5`, `Mef2a`, `Mef2c`, `Crebbp`, and `Ep300` to avoid
  hand-interpreting sparse signatures as broad pathway phenocopies. This corpus
  is a packaged interpretation of the same experiment, not independent
  replication.
- External literature retrieved through PubMed, including class-IIa HDAC/MEF2
  mechanism papers and neuronal HDAC4/MEF2 papers: Grozinger and Schreiber 2000
  doi:10.1073/pnas.140199597; Wang et al. 2000
  doi:10.1128/MCB.20.18.6904-6912.2000; Wang and Yang 2001
  doi:10.1128/MCB.21.17.5992-6005.2001; McKinsey et al. 2000
  doi:10.1073/pnas.260501497; Hudson et al. 2015
  doi:10.1074/jbc.M115.661058; Li and Yang 2016
  doi:10.1007/978-1-4939-3667-0_4; Flavell et al. 2006 PMID:16484497;
  Flavell et al. 2008 PMID:19109909; Akhtar et al. 2012
  doi:10.1371/journal.pone.0034863; Majidi et al. 2019 PMID:31722213; and
  Kim et al. 2022 doi:10.1038/s41586-022-05450-1.

## Computational calibration

For `Hdac4` I first enumerated focal training counts for the assayed
class-IIa/MEF2/CaMK/calcineurin/KAT3 branch rather than using all chromatin
regulators as a single pool. In `151 TH Prkcd Grin2c Glut` the relevant
assayed perturbations were:

| target | focal FDR 0.05 DEG count | matched perturbed nuclei | role in prediction |
| --- | ---: | ---: | --- |
| `Hdac5` | 0 | 289 | closest represented class-IIa HDAC paralog and the strongest analog |
| `Hdac8` | 0 | 111 | HDAC family member but class I/IIb-adjacent, not a mechanistic class-IIa analog |
| `Mef2a` | 4 | 138 | downstream HDAC4/5-regulated transcription factor; loss is the opposite sign of HDAC4 derepression |
| `Mef2c` | 1 | 223 | MEF2 paralog and best focal `Mef2a` signature neighbor, still nearly null |
| `Mef2d` | 0 | 262 | MEF2 paralog, buffered in this assay |
| `Camk2a` | 0 | 122 | upstream activity/CaMK arm |
| `Camk2b` | 1 | 218 | upstream activity/CaMK arm; only the self transcript passed |
| `Camk2g` | 0 | 119 | upstream activity/CaMK arm |
| `Ppp3ca` | 4 | 240 | calcineurin arm converging on MEF2/HDAC regulation |
| `Ppp3r1` | 9 | 93 | calcineurin arm; small thalamic response |
| `Ppp3cc` | 0 | 104 | calcineurin arm |
| `Prkaca` | 1 | 192 | PKA branch upstream of class-IIa trafficking |
| `Crebbp` | 8 | 61 | MEF2/CREB coactivator comparator, small and target-specific |
| `Ep300` | 0 | 155 | CBP paralog comparator, completely buffered |
| `Creb1` | 10 | 126 | CREB-pathway transcription factor, small |
| `Runx2` | 0 | 219 | non-neuronal HDAC4/MEF2/Runx2 comparator, a counterexample |
| `Runx3` | 0 | 221 | Runx-family counterexample |
| `Ctbp1` | 5 | 202 | corepressor/coregulator counterexample |

I also inspected the focal rows with the smallest adjusted p values. `Hdac5`
had no row below FDR 0.05 or 0.10; its best focal row was `Hdac5` itself
(`logfoldchanges = -0.327`, adjusted p = 0.273), followed by `Xbp1`,
`Selenok`, `Ptpn3`, and `Cacna2d1`, all with adjusted p = 0.646. `Mef2a`
was small but real, with four FDR 0.05 genes (`Gpr4`, `Prkcg`, `Ogt`, `Sez6`),
and `Mef2c` had only its self transcript at FDR 0.05. The canonical
activity/MEF2 genes checked as possible hidden evidence, including `Npas4`,
`Bdnf`, `Arc`, and `Fos`, all had adjusted p = 1.0 in the focal `Hdac5`,
`Mef2a`, `Mef2c`, `Mef2d`, `Crebbp`, and `Ep300` rows.

Across all measured cell groups, the same-experiment corpus reports that
`Hdac5` produced only one downstream FDR 0.10 gene in the complete DE surface:
`Chd5` up-regulation in `012 MEA LA CA1 DG Glut`. `151 TH Prkcd Grin2c Glut`
was the best-powered `Hdac5` group with 289 perturbed cells and still had 0
FDR 0.10 genes, so the focal null is not caused by obviously poor recovery.
The corpus also reports that an all-cell-group signature-neighbor search for
`Hdac5` had maximum absolute Pearson r = 0.0347 and included safe targets among
the extremes; I therefore did not transfer from its nominal nearest neighbors.

## Target-specific reasoning

### Hdac4

`Hdac4` encodes a class-IIa histone deacetylase. HDAC4 and HDAC5 both shuttle
between cytoplasm and nucleus through phosphorylation-dependent 14-3-3 binding;
in the nucleus, class-IIa HDACs act mainly as signal-responsive corepressors
through MEF2 and SMRT/NCOR/HDAC3 rather than as strong catalytic deacetylases.
That makes `Hdac5` the most appropriate assayed same-direction analog for
`Hdac4` loss. In the focal cells, `Hdac5` loss had 0 observed DEGs out of
17,259 measured genes at FDR 0.05. Even at FDR 0.10 it remained completely
flat in the focal class, and the packaged Hdac5 report found no coherent
whole-profile neighbor.

The main causal chain I considered was:

`Hdac4` CRISPR loss -> less class-IIa HDAC4 repression at nuclear MEF2/other
targets -> possible derepression of activity/synaptic or neuronal-state genes
in recovered thalamic excitatory nuclei -> FDR-level DEG count.

The transfer from `Hdac5` is imperfect because class-IIa HDAC paralogs can have
distinct nuclear localization and tissue functions, and `Hdac4` has a
documented sleep-regulatory SIK3 link in excitatory neurons. That evidence
raises the prior that HDAC4 is functional in neurons: Kim et al. 2022 showed
that Hdac4 haploinsufficiency and an HDAC4 S245A SIK3-phosphorylation mutant
affect mouse sleep through an LKB1-SIK3-HDAC4 cascade. The same paper,
however, localizes sleep quantity/depth effects to cortical and hypothalamic
excitatory populations and to sleep-deprivation/SIK3 gain-of-function
transcriptional states, not to unstimulated P16-to-P37 thalamic
`151 TH Prkcd Grin2c Glut` CRISPR.

The downstream MEF2 arm also argues for a zero or tiny focal count rather than
a large one. Loss of `Mef2a`, `Mef2c`, and `Mef2d` gave 4, 1, and 0 FDR 0.05
genes in the same focal class, respectively. Because HDAC4 loss should
derepress part of the MEF2 program whereas MEF2 loss removes activator
function, the signs are not directly transferable; still, if basal MEF2-linked
transcription were a broad limiting program in this cell type, one of the
three represented MEF2 losses or the `Camk2`/`Ppp3` upstream perturbations
would be expected to leave a larger footprint. They did not. The focal
`Hdac5` rows likewise did not move `Npas4`, `Bdnf`, `Arc`, `Fos`, `Scn4b`, or
`Tacr1`, preventing transfer from the canonical activity-dependent HDAC5/MEF2
literature and supporting a stimulus-gated rather than basal signature.

Finally, broad chromatin counterexamples were rejected. `Sin3a`, `Brd4`, and
`Ctnnb1` are large focal responders with 1433, 311, and 383 FDR 0.05 genes, but
they perturb different limiting functions. The KAT3 comparators illustrate the
risk of family-level transfer: `Crebbp` produced only 8 focal DEGs and `Ep300`
produced 0 despite being paralogous coactivators, and the same-experiment
corpus reports that they did not phenocopy each other. I therefore used
`Hdac5 = 0` as the strongest quantitative anchor and treated the MEF2/CaMK/CBP
small counts as a weak upper boundary, not as grounds to predict a broad
chromatin response.

Prediction: `Hdac4` is expected to be non-broad and most likely below the FDR
0.05 detection threshold in `151 TH Prkcd Grin2c Glut`, so I assign
`predicted_n_degs = 0`.

## Limits and uncertainty

The requested endpoint is absent for `Hdac4`; this is a prediction from
training analogs, not a direct observation. The closest assayed paralog was
`Hdac5`; `Hdac7`, `Hdac9`, `Hdac3`, `Ncor1`, and `Ncor2` were not available as
training perturbations, so the core class-IIa repression complex is only
partially sampled. The assay was sparse mosaic CRISPR in unstimulated
postmitotic neurons and cannot rule out an HDAC4 effect after sleep pressure,
calcium stimulation, injury, or stress, nor can its recovered-nucleus DE rows
measure earlier selection. `Hdac4` may also act in cortex or hypothalamus more
than in the requested thalamic focal group. Those points make a very small
nonzero result plausible, but the focal within-dataset evidence is concentrated
at zero and single-digit counts, so zero is the best point prediction.
