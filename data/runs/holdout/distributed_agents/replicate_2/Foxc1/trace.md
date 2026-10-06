# Foxc1 held-out DEG-count prediction

## Question and target

The requested held-out target was `Foxc1` from `078_Foxc1.csv`.
I interpreted the endpoint as:

- cell group: `151 TH Prkcd Grin2c Glut`;
- contrast: acute sparse CRISPR loss of the target gene versus matched non-targeting/safe-targeting controls;
- scalar to predict: the number of measured genes in this cell group with Benjamini-Hochberg adjusted Wilcoxon `pvals_adj < 0.05`;
- prediction type: a nonnegative integer point prediction, with `0` meaning no measured gene is expected to pass FDR 0.05.

`TH` was treated as the atlas abbreviation for thalamus, not tyrosine hydroxylase. `Foxc1` itself is completely held out from the supplied parquet and the focal-cell training count CSV, so no `Foxc1` differential-expression row or `Foxc1` count was used.

## Sources used

- Declared training endpoint CSV:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- Declared DE parquet:
  `[local file: training_de_all_cell_groups.parquet]`
- Distributed Agents PerturbAI atlas dataset context, local run version `perturbai-atlas-v5`.
- Distributed Agents July 260713 `sourceguard-1773` same-experiment corpus, used for curated finding summaries around visible training perturbations, especially `Foxc2`, `Foxa2`, `Foxp2`, `Notch1`, `Fgfr2`, `Smad1`, `Pitx2`, and `Ctnnb1`.
- Distributed Agents gene-annotation and analog-nomination resources over the closed PerturbAI gene universe, including GO Biological Process, GO Molecular Function, MSigDB WikiPathways, MSigDB Hallmark, functional-class annotations, and STRING/CORUM relationships where available.
- NCBI PubMed literature for external FOXC1 biology.

External mechanistic references:

- Aldinger et al. 2009, `DOI:10.1038/ng.422`, `PMID:19668217`: FOXC1 dosage is linked to human 6p25.3 Dandy-Walker/cerebellar vermis malformations; mouse `Foxc1` mutants implicate mesenchyme-neuroepithelium signaling in mid-hindbrain development.
- Hecht et al. 2010, `DOI:10.1002/ana.22103`, `PMID:20976766`: primary meningeal defects in `Foxc1` mutants cause neocortical dysplasia, overmigration, and basement-membrane remodeling defects.
- Zarbalis et al. 2012, `DOI:10.1186/1749-8104-7-2`, `PMID:22248045`: meningeal defects in `Foxc1` hypomorphs disrupt embryonic tangential interneuron migration, with `Cxcl12` identified as a direct meningeal Foxc1 target.
- Haldipur et al. 2014, `DOI:10.7554/eLife.03962`, `PMID:25513817`: `Foxc1` is expressed in posterior fossa mesenchyme; `Foxc1`-dependent mesenchymal `SDF1a/Cxcl12` signaling non-autonomously drives embryonic cerebellar radial-glial proliferation and Purkinje-cell migration.
- Mishra et al. 2016, `DOI:10.1016/j.ydbio.2016.09.019`, `PMID:27671872`: `Foxc1` in neural-crest-derived meninges and brain pericytes, not endothelial cells, is needed for cerebrovascular development through meninges-derived retinoic-acid effects on WNT and VEGF-A pathways.
- Haldipur et al. 2017, `DOI:10.7554/eLife.20898`, `PMID:28092268`: hypomorphic mouse `Foxc1` mutants phenocopy core aspects of human FOXC1-dependent Dandy-Walker cerebellar malformation through developmental granule/Purkinje migration and later foliation consequences.

## Computation over the supplied training data

1. Read the held-out manifest and confirmed that the only requested target was `Foxc1`.

2. Read the focal-cell training count table with pandas. It contains 1,674 non-held-out perturbations. Counts are highly zero-inflated in this endpoint:

   - 1,205 / 1,674 targets have `n_degs = 0`;
   - 469 / 1,674 have `n_degs > 0`;
   - median `n_degs = 0`;
   - 90th percentile `n_degs = 2`;
   - 95th percentile `n_degs = 18`.

   This established that a zero prediction is common, so a nonzero estimate needs a target-specific reason.

3. Queried all obvious in-training forkhead and neural developmental TF names from the count CSV. The focal-cell counts were:

   | training perturbations | focal `n_degs` |
   |---|---:|
   | `Foxa2`, `Foxc2`, `Foxe3`, `Foxi1`, `Foxj3`, `Foxk2`, `Foxl1`, `Foxl2`, `Foxn1`, `Foxp2`, `Foxp3` | all `0` |
   | `Pax6`, `Tbr1`, `Otx2`, `Neurod1`, `Neurod2` | all `0` |
   | `Sox2`, `Sox5` | `2`, `2` |
   | `Sox4`, `Sox9`, `Sox10`, `Sox11`, `Sox17`, `Sox18` | all `0` |

   I used this as a first calibration of postnatal neuronal developmental-TF responsiveness, not as a symbol-stem rule.

4. Ran the Distributed Agents gene-analog nomination skill for `Foxc1` against the focal count table's training universe. `Foxc1` resolved through curated annotations but was absent from the same-experiment finding ledger and BioKG. The strongest training-available nominee was `Foxc2`; it shared narrow MSigDB WikiPathways modules with `Foxc1`, especially `WP_BMP_SIGNALING_PATHWAY_IN_EYELID_DEVELOPMENT`, `WP_GDNFRET_SIGNALING_AXIS`, and `WP_HEART_DEVELOPMENT`, plus broad GO developmental annotations. There was no exact-complex or exact-paralog nominee in the curated store.

5. Looked up the top 80 typed `Foxc1` nominees in the exact focal training endpoint. The narrow and pathway-proximal candidates around BMP/Notch/FGF/TGF-beta/vascular development were almost entirely null:

   | comparator | why it was considered | focal `n_degs` |
   |---|---|---:|
   | `Foxc2` | closest curated narrow-module forkhead-C analog | `0` |
   | `Notch1` | shared eyelid/BMP and mesenchymal-development logic | `0` |
   | `Fgfr2` | shared eyelid/BMP and developmental signaling | `0` |
   | `Smad1` | BMP-SMAD effector | `0` |
   | `Smad3` | TGF-beta SMAD | `0` |
   | `Smad4` | common SMAD | `0` |
   | `Tgfbr1`, `Tgfbr2`, `Tgfbr3` | TGF-beta receptors | `0`, `0`, `0` |
   | `Bmpr1a`, `Bmpr1b`, `Bmpr2` | BMP receptors | `0`, `0`, `0` |
   | `Sox17`, `Sox9`, `Gata4`, `Kdr`, `Flt4`, `Gata3`, `Acvrl1`, `Eng`, `Ret` | vascular/mesenchymal/GDNF-RET nominees | all `0` |
   | `Smad2` | TGF-beta SMAD | `1` |
   | `Crebbp` | transcriptional coactivator attached to the broad GO graph | `8` |
   | `Ctnnb1`, `Tcf7l2` | Wnt effector counterexamples | `383`, `106` |

   `Ctnnb1` and `Tcf7l2` were the only strong responses in this typed region. The same-experiment corpus reports that `Ctnnb1` and `Tcf7l2` converge on a 151 TH thalamic Wnt/excitability/adhesion state; `Foxc1` is upstream of meningeal retinoic-acid and SDF1a/Cxcl12 programs during embryonic patterning rather than an acute beta-catenin/TCF effector in P16 postmitotic thalamic neurons, so I treated this Wnt branch as a mechanistic counterexample.

6. Ran Distributed Agents runtime measured-profile comparisons in the exact focal group:

   - a 22-node developmental-TF cohort containing 11 `Fox*` perturbations and neural-patterning TFs; 20/22 profiles had no significant features and the only active nodes had 2 DEGs;
   - a 70-node cohort from the top `Foxc1` annotation nominees plus `Tcf7l2`; 62/70 had no significant features, 6/70 had 1-9 significant features, and only `Ctnnb1` and `Tcf7l2` had at least 50.

   The profile inspection used `logfoldchanges` by `names` in `151 TH Prkcd Grin2c Glut`, with `pvals_adj` only to annotate the same pairwise profiles. `Foxc2`, `Smad1`, and `Notch1` had `0` significant features; `Ctnnb1` had 100 positive plus 283 negative features; and `Tcf7l2` had 39 positive plus 67 negative features. `Ctnnb1` shared 35 negative and 5 positive significant genes with `Tcf7l2`, but it shared no significant genes with `Foxc2`, `Smad1`, `Notch1`, or the other null BMP/TGF-beta candidates. This supported separating Wnt-effectors from the much quieter `Foxc1`-like branch.

## Target-specific reasoning

### `Foxc1`

The strongest in-dataset analog for a held-out `Foxc1` prediction was `Foxc2`, not because `Foxc2` had a matching measured profile to `Foxc1`--`Foxc1` has no measured profile here--but because the curated annotation layer placed `Foxc2` in the same narrow MSigDB/WikiPathways developmental modules as `Foxc1`. `Foxc2` had `n_degs = 0` in the focal thalamic glutamatergic group. The July 260713 Distributed Agents same-experiment corpus also summarized `Foxc2` as pan-null across the recovered NeuN-positive neuronal groups and noted failure to engage arterial VEGF-Dll4/Notch-Hey2, CXCR4, lymphatic NFATc1/ITGA9, or RhoA/ROCK programs in this neuronal assay.

Other forkhead-family and forkhead-adjacent controls reinforced the same calibration. `Foxa2`, `Foxl1`, `Foxp2`, and `Foxp3` have same-experiment corpus findings describing pan-neuronal or broad neuronal nulls, and all measured `Fox*` perturbations in the focal training count table were `0`. `Foxp2`, which is much more overtly neuronal than `Foxc1`, was also flat in this exact focal group. This made the direct forkhead developmental-TF branch a zero-scale donor.

The next mechanistic tier consisted of BMP/TGF-beta/Notch/FGF and mesenchymal or vascular developmental genes nominated through GO and MSigDB terms shared with `Foxc1`: `Smad1`, `Smad3`, `Smad4`, `Tgfbr1`, `Bmpr1a`, `Bmpr2`, `Notch1`, `Fgfr2`, `Kdr`, `Flt4`, `Sox17`, `Gata4`, `Gata3`, `Pitx2`, and related receptors/cofactors. Nearly all of these had `n_degs = 0`; `Smad2` had a singleton count of `1`; `Mef2c` had `1`; `Crebbp`, a general coactivator rather than a specific FOXC1 branch effector, had `8`. The same-experiment corpus reports likewise described `Smad1` as absent for canonical BMP-SMAD output, `Notch1` as lacking the canonical NICD1/RBPJ/MAML program, `Fgfr2` as lacking the canonical FGF/ERK feedback program, and `Pitx2` as a pan-null juvenile neuronal surface.

The major high-count counterexamples were `Ctnnb1` and `Tcf7l2`. They are real developmental/Wnt genes, and both were large in 151 TH (`383` and `106`). I did not transfer their magnitude to `Foxc1` because their Distributed Agents findings show a direct thalamic Wnt feedback, synaptic/excitability, adhesion, and beta-catenin/TCF state after loss of Wnt effectors. External Foxc1 literature instead places the best-established CNS role in embryonic head mesenchyme/meninges and pericytes, acting non-cell-autonomously through Cxcl12/SDF1a, retinoic acid, WNT, and VEGF-A to shape rhombic-lip, cerebellar, cortical, interneuron-migration, and vascular development. Those source tissues and time windows are outside the P16-to-P37/44 sparse NeuN-positive postmitotic-neuron assay, and the focal class is a thalamic glutamatergic class rather than embryonic meninges, hindbrain mesenchyme, or recovered vascular/pericyte cells.

Therefore the zero/nonzero decision is driven primarily by within-dataset evidence from `Foxc2` and the null BMP/TGF-beta/Notch/Fox branch, with external knowledge explaining why the large developmental effects of FOXC1 disease biology should not be projected into this acute postnatal neuronal readout. My point prediction is:

| target | predicted `n_degs` |
|---|---:|
| `Foxc1` | `0` |

## Limits and extrapolation

- There is no measured `Foxc1` profile or same-experiment `Foxc1` corpus report; the prediction is a transfer from available training perturbations plus external developmental biology.
- `Foxc2` is the best curated narrow-module neighbor, but it is not an exact complex member or an exact-paralog edge in the local annotation store. Its null profile is strong calibration for the pathway context, not a direct measurement of `Foxc1`.
- The Wnt effector branch is a real non-null counterexample in the focal thalamic group. I down-weighted it because `Ctnnb1` and `Tcf7l2` are direct neuronal Wnt/beta-catenin effectors with an observed same-experiment thalamic module, whereas FOXC1's documented brain actions are mainly embryonic and non-neuronal or non-cell-autonomous.
- Acute CRISPR knockout in sparse P16 neurons can reveal retained postnatal TF functions, so the developmental timing argument is not absolute. The prediction is that any residual `Foxc1` function in recovered 151 TH neurons will fall below FDR 0.05 in this assay, not that FOXC1 is unimportant in brain development.
- Training counts are assay- and power-conditioned. A prediction of zero DEGs should not be read as a claim of failed editing, lack of target mutation, lack of all biological effect, or lack of FOXC1 relevance in meninges, vasculature, eye, heart, or embryonic cerebellar development.
