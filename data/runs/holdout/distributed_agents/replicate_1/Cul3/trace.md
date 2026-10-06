# Task interpretation

I interpreted the task as a scalar holdout prediction: estimate `n_degs` for the
held-out `Cul3` perturbation in `151 TH Prkcd Grin2c Glut` cells, where
`n_degs` means the number of measured genes in that cell group with
Benjamini-Hochberg-adjusted Wilcoxon `pvals_adj < 0.05`. The `Cul3` row was not
present in either the training DEG-count CSV or the all-cell differential
expression parquet, so the endpoint for `Cul3` is absent from the declared
inputs rather than directly observed.

The requested-target CSV contained exactly one row:

| target_name |
|---|
| Cul3 |

# Sources used

- Declared row-level Perturb-seq differential-expression table:
  `training differential-expression dataset`.
- Declared focal-cell training counts:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared requested-target manifest:
  `single-target request for Cul3`.
- Run-local Distributed Agents task bindings, measurement registry, coverage summary,
  and capability manifest under `codex_runtime/pipeline`.
- Same-experiment internal corpus:
  `perturbai-july-260713-sourceguard-1773-v1`. I used the corpus calibration
  summary and bounded Finding records for represented analogs/counterexamples
  (`Klhl7`, `Kctd1`, `Uba5`, `Ufc1`, `Psmb4`). The same-experiment graph had no
  `Cul3` comparator rows, and its topology was not used as evidence or as a
  score.
- External mechanism literature from PubMed, used only as a biological prior for
  whether a training perturbation is an appropriate analog:
  - Chen and Chen 2016, Frontiers in Oncology, DOI
    `10.3389/fonc.2016.00113`, PMID `27200299`: CUL3-RING ligases use BTB
    proteins such as KEAP1 and KLHL20 as substrate adaptors.
  - Dubiel et al. 2017, Trends in Biochemical Sciences, DOI
    `10.1016/j.tibs.2017.11.010`, PMID `29249570`: CUL3-based CRLs are a major
    cullin-RING family and are especially linked to differentiation programs.
  - Jerabkova and Sumara 2018, Seminars in Cell & Developmental Biology, DOI
    `10.1016/j.semcdb.2018.12.007`, PMID `30586619`: CUL3-BTB ligases can
    make proteolytic and non-proteolytic ubiquitin signals rather than simply
    acting as a generic proteasome-loss perturbation.
  - Dong et al. 2019, Neuron, DOI `10.1016/j.neuron.2019.10.035`, PMID
    `31780330`: neuronal CUL3 deficiency affects excitatory/inhibitory balance
    and cap-dependent translation in mouse.
  - Rapanelli et al. 2019, Molecular Psychiatry, DOI
    `10.1038/s41380-019-0498-x`, PMID `31455858`: forebrain or regional Cul3
    deletion changes cortico-striatal physiology and protein abundance in mice.
  - Morandell et al. 2021, Nature Communications, DOI
    `10.1038/s41467-021-23123-x`, PMID `34031387`: Cul3 is important during a
    developmental migration window, and later induction of Cul3
    haploinsufficiency did not reproduce the autism-relevant behavioral
    phenotypes.
  - Xia et al. 2023, PLOS ONE, DOI `10.1371/journal.pone.0283299`, PMID
    `37428799`: global Cul3 heterozygosity produced only modest adult
    hippocampal synaptic, morphology, behavioral, and proteomic changes.

# Quantitative calibration from the training set

The training endpoint itself was highly zero-inflated in the focal class:

| quantity | value |
|---|---:|
| training targets | 1,674 |
| targets with `n_degs = 0` | 1,205 |
| median `n_degs` | 0 |
| 75th percentile | 1 |
| 90th percentile | 2 |
| 95th percentile | 18 |
| maximum | 2,677 |

To verify the supplied count table and get analog signatures, I scanned only the
parquet row groups overlapping `151 TH Prkcd Grin2c Glut`, filtered to the
focal cell group, grouped by `gene_target`, and counted rows with
`pvals_adj < 0.05`. This exactly reproduced all 1,674 counts in the focal
training CSV.

# Cul3 analogs and counterexamples

`Cul3` is the cullin scaffold for many CRL3 complexes. The closest unavailable
perturbations would have been the cullin core itself or the shared CRL
machinery (`Cul1`, `Cul2`, `Cul4a`, `Cul4b`, `Cul5`, `Rbx1`, `Cand1`, `Nedd8`,
`Keap1`), but none of those was represented in the focal training-count CSV.
I therefore used the available BTB/Kelch, KCTD, F-box, and other ubiquitin
ligase perturbations as imperfect local analogs:

| training target | focal `n_degs` | focal signature evidence | relationship to Cul3 |
|---|---:|---|---|
| `Klhl7` | 0 | no FDR-significant focal genes; the internal corpus reported no reproducible downstream `Klhl7` response at FDR 0.10 in any recovered neuronal class | BTB/Kelch CUL3 adaptor, substrate-specific and not a scaffold phenocopy |
| `Klhl20` | 0 | no focal DEGs | distinct CUL3-KLHL adaptor; useful as a CUL3-family adaptor counterexample |
| `Kctd1` | 2 | only `Resp18` up and `Cluap1` down passed FDR 0.05 in the focal class; the corpus described the KCTD1 response as sparse and not a core Wnt or Hedgehog phenocopy | BTB/KCTD family member; weak analogy because it is not a known broad neuronal CRL3 core subunit |
| `Kctd8` | 0 | no focal DEGs | KCTD family counterexample |
| `Kctd16` | 0 | no focal DEGs | KCTD family counterexample |
| `Btbd9` | 0 | no focal DEGs | BTB-domain family counterexample |
| `Kbtbd7` | 0 | no focal DEGs | BTB/Kelch-domain family counterexample |
| `Fbxo11` | 1 | only `Ppib` down passed FDR 0.05 | cullin adaptor-like E3 biology, but SCF/CUL1 rather than CRL3 |
| `Fbxo38` | 0 | no focal DEGs | F-box adaptor counterexample |
| `Fbxw7` | 1 | only `Trp53inp2` up passed FDR 0.05 | SCF/CUL1 adaptor; very weak positive boundary |
| `Ube3a` | 0 | no focal DEGs despite known neuronal disease relevance | E3 ligase counterexample showing that famous neuronal ubiquitin biology need not give a focal transcriptional footprint |
| `Ube2e2` | 0 | no focal DEGs | E2 ubiquitin-conjugating counterexample |
| `Rlim` | 0 | no focal DEGs | RING E3 counterexample |

The high-count proteostasis controls were important counterexamples in the
opposite direction but were not close enough to transfer quantitatively. `Uba5`
had 2,677 focal DEGs and `Ufc1` had 572 because they hit the core UFMylation
cascade; the same-experiment corpus tied their focal signatures to translation,
ER/ribosome quality control, OXPHOS, and ubiquitin-like/autophagy compensation.
`Psmb4` had 742 focal DEGs and `Psmc1` had 430 after direct proteasome subunit
loss. Those perturbations remove limiting machinery for protein quality control.
CUL3 instead changes substrate-specific ubiquitination through many adaptors and
can produce proteomic or localization effects without immediate transcriptome
collapse, so I did not map `Cul3` onto the `Uba5`/`Ufc1` or `Psmb4`/`Psmc1`
counts.

# Target-specific prediction

The causal chain I assumed was:

`Cul3` CRISPR loss -> reduced CRL3 scaffold function across BTB/Kelch/KCTD
adaptors -> altered stability or localization of direct protein substrates,
including developmental, cytoskeletal, NRF2/KEAP1, translation, and synaptic
effectors -> possible homeostatic transcriptional response in surviving,
postnatal thalamic glutamatergic nuclei -> Wilcoxon DEGs at FDR 0.05.

External mouse work makes `Cul3` a real neurodevelopmental and synaptic gene,
not a safe-target-like gene: Dong et al. and Rapanelli et al. found altered
neural excitability or cortico-striatal function after Cul3 deficiency, and
Morandell et al. showed a developmental migration mechanism. The postnatal
Perturb-seq setting weakens that transfer. The assay perturbed sparse
postmitotic neurons at P16 and measured recovered nuclei only 3 to 4 weeks
later, after the embryonic migration window emphasized by Morandell et al.;
Xia et al. also found that Cul3 heterozygosity can give modest adult
hippocampal effects rather than a large cellular collapse. Those reports are
proteomic, morphologic, electrophysiologic, or behavioral rather than the exact
BH-Wilcoxon snRNA-seq count used here.

Within the declared experiment, every represented substrate-adaptor branch that
looked closer to CUL3 than global proteasome or UFMylation loss was quiet or at
most a one- to two-gene boundary signal in `151 TH Prkcd Grin2c Glut`. Because
none of those analogs mounted a broad integrated-stress, oxidative-stress, Wnt,
or Hedgehog RNA program, and because the focal training distribution puts 90%
of perturbations at two DEGs or fewer, I predicted that acute mosaic `Cul3`
loss would remain below the FDR 0.05 count threshold rather than crossing into
a reproducible nonzero response.

Point prediction for `Cul3`: `0` DEGs.

# Limits

- There is no direct `Cul3` signature in the supplied parquet, no `Cul3`
  training count, and no same-experiment `Cul3` report in the July internal
  corpus, so this is an extrapolation from imperfect analogs.
- The available BTB/Kelch and KCTD genes are substrate-specific adaptors or
  family members. A cullin scaffold perturbation could affect more substrates
  than any one represented adaptor.
- The strongest proteostasis perturbations in the training set are real but
  probably overestimate `Cul3`, because direct UFMylation or proteasome loss is
  a more obligate protein-quality-control hit than partial CRL3 impairment.
- The external `Cul3` literature is mostly germline, conditional, or
  region-specific mouse work with proteomic or physiological endpoints. It
  supports biological importance, but it is not an exact proxy for the
  post-P16 sparse CRISPR snRNA-seq `n_degs` endpoint in thalamic glutamatergic
  survivor nuclei.
