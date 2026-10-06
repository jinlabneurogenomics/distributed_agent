# Stt3b n_degs forecast

Prediction for `151 TH Prkcd Grin2c Glut`: `Stt3b -> 0`.

## Target biology

The target is expressed in the exact focal class: the declared biology bundle reports
Stt3b in 20,103 of 23,679 non-target nuclei, 84.898% of the class, with mean
1.637 CP10K.  That makes the perturbation reachable in the assayed thalamic
neurons, but it is not a calibrated response probability and I did not use any
Stt3b differential-expression endpoint.

The functional-stock card judged P16 editing of `Stt3b` as likely to
substantially deplete operative STT3B by the P37-P44 harvest.  The same card
kept two important dampers: existing glycans remain on pre-edit carrier
proteins until those carriers turn over, and STT3A supplies partially
overlapping OST activity.  The observability card also marked the postnatal
neuronal loss phenotype as unknown because direct mouse loss data are systemic
embryonic lethality rather than acute postmitotic thalamic loss.

Biologically, STT3B is the OST-B catalytic subunit for selected
post-translocational N-glycosylation sites.  That made me weight core
N-glycan/ER glycoprotein handling perturbations more than generic proteasome,
splicing, nuclear-transport, or ubiquitin outliers.

## Training measurements used

The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` contains 1,674
held-in perturbations and excludes `Stt3b`.  Its BH<0.05 count distribution in
this class is extremely zero-inflated: 1,205 / 1,674 targets are 0, 1,481 are
0 or 1, and 1,512 are 0 to 2; the long tail is driven by broad responses such
as `Uba5` 2,677, `Tpr` 1,768, `Psmb4` 742, and `Psmc1` 430.

Typed analog nomination over the same training universe reported that `Stt3b`
was absent from training and from the same-experiment corpus graph.  Only two
available candidates were in the narrow N-glycan KEGG module:

| perturbation | typed relation to Stt3b | BH<0.05 n_degs |
| --- | --- | ---: |
| `Dpm1` | N-Glycan biosynthesis module | 0 |
| `Deaf1` | N-Glycan biosynthesis module annotation | 3 |

The same scan of the expression parquet in `151 TH Prkcd Grin2c Glut` gave
near-null counts for the ERQC/glycoprotein nominees I considered most relevant:
`Edem3` 0, `Atf6` 0, `Fktn` 0, `Tmem165` 0, `Manba` 0, `Ext2` 0, `Atg5` 0,
`Large1` 1, `Vcp` 2, `Hspa5` 5, and `Gsk3b` 6.

The same-experiment Findings around these held-in perturbations put the larger
ER-stress examples at a mechanistic remove from STT3B.  `Dpm1` had no genes at
BH<0.05 and only two genes below BH<0.10 in the focal class; its report
explicitly contrasted that weak Dol-P-Man response with a strong `Gfpt1` UPR
program.  `Hspa5` linked to a detectable ER-stress manifold with `Gfpt1`,
`Dhdds`, and `Atp2a2`, whose BH<0.05 counts were 311, 116, and 187, but those
are broader hexosamine/dolichol/ER-calcium perturbations rather than selective
STT3B OST-B loss.  `Edem3` and `Atf6` reinforced that basal loss of an
ERAD/UPR-adjacent gene need not engage the HSPA5-like UPR state.

## Synthesis

The focal neurons express `Stt3b`, and a completely realized lesion should
affect newly synthesized STT3B-selective glycoproteins.  However, the closest
measured thalamic glycosylation and ER-quality-control analogs were flat or
nearly flat at the task's BH<0.05 threshold, with the broader high-count UPR
perturbations arising from upstream supply or proteostasis mechanisms.  Given
STT3B's substrate selectivity, partial STT3A overlap, and carrier-protein
buffering, I predicted a thresholded null rather than a small nonzero count:
`predicted_n_degs = 0`.
