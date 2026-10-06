# Dock7 forecast for 151 TH Prkcd Grin2c Glut

## Prediction

`Dock7` is predicted to have **1** measured gene with BH-adjusted Wilcoxon
`p < 0.05` in `151 TH Prkcd Grin2c Glut`.

## Evidence used

- The declared one-row holdout manifest contains `Dock7`, and the declared
  focal training count table contains 1,674 other targets, not `Dock7`.
- The focal training counts are extremely sparse: 1,205/1,674 targets have
  `n_degs = 0`, 276 have `n_degs = 1`, the median is 0, and the 90th percentile
  is only 2 despite a small number of very large RNA-processing/proteostasis
  outliers.
- The Dock7 biology-only bundle reports strong focal reach of the transcript:
  Dock7 was detected in 22,177/23,679 non-target nuclei from this class
  (93.66%), with mean raw UMI 3.59 and mean log1p CP10K 1.09. The same bundle
  adjudicates Dock7 operative protein as likely substantially depleted within
  the 21-28 day edit-to-harvest window, because Dock7 is a dynamic Rac/Cdc42
  GEF and scaffold rather than a permanently installed structure.
- The functional evidence for Dock7 argues for possible engagement but not for
  a large mature-thalamic downstream state. The direct mouse neural phenotypes
  are developing hippocampal polarity, embryonic cortical progenitor migration,
  chandelier-cell ErbB4 signaling, and postnatal V-SVZ neuroblast migration.
  Those contexts involve cytoskeletal migration, polarity, or interneuron
  specialization and are displaced from juvenile postmitotic thalamic
  glutamatergic neurons.
- Typed analog nomination placed the closest available Rac/GEF/WAVE candidates
  in the training universe at `Tiam1`, `Rac1`, `Cyfip1`, `Dock3`, and `Cdc42`.
  In the focal count table and exact focal Parquet slice these were:

  | target | focal `n_degs` | focal Parquet interpretation |
  | --- | ---: | --- |
  | `Tiam1` | 0 | no FDR gene; minimum q = 0.3117 |
  | `Rac1` | 0 | no FDR gene; minimum q = 1 |
  | `Cyfip1` | 0 | no FDR gene; minimum q = 1 |
  | `Dock3` | 0 | no FDR gene; minimum q = 0.5838 |
  | `Cdc42` | 1 | only the `Cdc42` self transcript was FDR-significant |
  | `Pak1` | 1 | only the `Pak1` self transcript was FDR-significant |
  | `Pak2` | 0 | no FDR gene |
  | `Pak3` | 0 | no focal FDR gene |
  | `Kalrn` | 0 | no FDR gene |

- Same-experiment Findings for these measured analogs explicitly supported this
  as a buffered axis rather than isolated sampling noise: Dock3 produced no
  robust downstream response in any recovered neuronal class; Cdc42, Rac1, and
  Pak1/2/3 did not recover a canonical Rac/Cdc42-to-PAK/LIMK actin cascade;
  Tiam1 and the Rac/EphB/PAK/WAVE neighborhood generated only singleton or null
  FDR calls across their matched surfaces; and Cyfip1 had zero downstream genes
  in all 23 measured neuronal classes.
- The Dock7 scaffolded ErbB4 branch also pointed to a null or singleton
  endpoint in this assay. Focal counts were `Erbb4 = 0`, `Nrg1 = 0`,
  `Nrg2 = 0`, and `Nrg3 = 1`, with the single Nrg3 focal call being the Nrg3
  self transcript.
- The exact focal score vectors for the closest Rac/GEF/WAVE analogs were not a
  shared weak module just below the FDR line. Pairwise Wilcoxon-score
  correlations among `Tiam1`, `Rac1`, `Cyfip1`, `Dock3`, `Cdc42`, `Pak1`,
  `Pak2`, `Pak3`, `Kalrn`, `Erbb4`, and `Nrg1` were all close to zero in the
  focal Parquet slice.
- In the full focal training matrix, 319/1,642 targets with a self row had an
  FDR-significant self transcript, and 237 training targets had exactly one
  DEG consisting only of the perturbed transcript. This pattern matters because
  many Dock7-relevant singleton analogs in the focal slice were self-only
  events, and Dock7 itself is strongly expressed in the focal non-target
  nuclei.

## Reasoning

I treated Dock7 as likely edited and expressed in the focal class, but not as a
strong driver of a recurrent recovered-nucleus transcriptional state. The
closest task-matched perturbations in the Rac/Cdc42/PAK/WAVE, Rho-GEF/GAP, and
ErbB/neuregulin neighborhoods were almost all null in `151 TH Prkcd Grin2c
Glut`, and same-experiment reports described those axes as buffered rather
than as mutually phenocopying. The large focal responses among broader
annotation nominees, such as `Ctnnb1`, `Rab7`, `Tsc2`, and `Bmal1`, came from
Wnt, endosomal, mTOR, or circadian response programs that do not follow from
Dock7's specific postnatal GEF/scaffold biology.

The remaining reason to move above zero is the target transcript itself.
Dock7's very broad focal expression gives substantial power to see even a
modest edited-transcript decrease, and a sizeable fraction of near-null
training perturbations register exactly one focal DEG through their own mRNA.
Because the biology and analog signatures argue against a downstream module but
the in-assay Dock7 transcript is highly reachable, the best point forecast is a
single DEG: a self-transcript call and no additional downstream gene.
