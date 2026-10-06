# Nr2f2 prediction trace

## Question and resolved ambiguities

The requested target file contains one held-out perturbation, `Nr2f2`. I interpreted the task as a point prediction for the number of genes that would pass `pvals_adj < 0.05` in the focal `151 TH Prkcd Grin2c Glut` differential-expression table if the held-out `Nr2f2` perturbation had been included.

I treated the endpoint as a statistical DEG burden in this assay, not as a direct measure of editing, viability, or gene importance. Zero therefore means "I predict no measured gene passes the Scanpy/Wilcoxon BH cutoff in this focal group", not "NR2F2 is biologically inert".

## Sources used

- Input endpoint counts: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Input DE signatures: `[local file: training_de_all_cell_groups.parquet]`.
- Requested target manifest: `[local file: 157_Nr2f2.csv]`.
- PerturbAI dataset portrait in `codex_runtime/pipeline/dataset_context.md`.
- Distributed Agents selected internal semantic corpus: `perturbai-july-260713-sourceguard-1773-v1`.
- Distributed Agents run-local profile-neighbor tool, over the focal-cell `scores` signatures, to check whether observed NR-family anchors had coherent matched neighbors.
- Distributed Agents gene-analog nomination and gene-annotation stores over the PerturbAI closed gene universe. These contributed curated functional-class/pathway memberships, CORUM 5.0 mouse records and one-to-one human-to-mouse CORUM projections through MGI `HOM_MouseHumanSequence.rpt` downloaded 2026-09-13. I used only membership/provenance, not a similarity score.
- PubMed literature for external mechanism checks:
  - Hu et al. 2017, *Development*, "Coup-TF1 and Coup-TF2 control subtype and laminar identity of MGE-derived neocortical interneurons", DOI `10.1242/dev.150664`, PMID `28694260`.
  - Kim et al. 2009, *Developmental Biology*, "Chicken Ovalbumin Upstream Promoter-Transcription Factor II (COUP-TFII) regulates growth and patterning of the postnatal mouse cerebellum", DOI `10.1016/j.ydbio.2008.11.001`, PMID `19041640`.

## Computations over the training data

I first loaded the focal training count CSV and verified the response scale in `151 TH Prkcd Grin2c Glut`: there were 1,674 training perturbations, 469 with a nonzero count, median `n_degs` = 0, 75th percentile = 1, 90th percentile = 2, and 95th percentile = 18. Thus a zero or 1-2 DEG prediction is not an unusual low-confidence tail case; it is the assay's dominant behavior in this cell group.

I then queried the Parquet only for rows with `group_name == "151 TH Prkcd Grin2c Glut"` and biologically nominated comparator `gene_target` values. This gave the exact focal signatures for the NR2F/NR2/RAR/RXR/ROR/Nr1d/circadian and MEF2 comparators without touching the held-out `Nr2f2` target, which is absent from the inputs.

The closest observed comparators had the following focal DEG burdens:

| comparator | relationship to `Nr2f2` | observed `n_degs` in 151 |
| --- | --- | ---: |
| `Nr2f1` | COUP-TF/NR2F paralog; shared nuclear-receptor annotations | 2 |
| `Nr2f6` | COUP-TF/NR2F family member; shared nuclear-receptor annotations | 0 |
| `Mef2a` | human ortholog is in the projected CORUM 5.0 MEF2-NR2F2 complex with NR2F2 | 4 |
| `Mef2c` | MEF2 paralog and corpus comparator for the MEF2 axis | 1 |
| `Nr2c1` | NR2-family nuclear receptor | 0 |
| `Nr2c2` | NR2-family nuclear receptor | 3 |
| `Nr2e1` | NR2-family nuclear receptor | 0 |
| `Nr2e3` | NR2-family nuclear receptor | 0 |
| `Rarb`, `Rarg` | RAR nuclear receptors | 0, 0 |
| `Rxra`, `Rxrb`, `Rxrg` | RXR nuclear receptors | 0, 0, 0 |

`Nr2f1`, the best biological training analog, changed only `Sorl1` up and `Sema7a` down at FDR 0.05 in 151. `Nr2f6` had zero corrected DEGs in the same group. In the Distributed Agents corpus, the reciprocal `Nr2f1`/`Nr2f6` comparison reports no phenocopy: matched score-space correlation `r = 0.003` and no shared FDR < 0.10 genes. The focal score-neighbor run was consistent with that sparse/null interpretation: `Nr2f1` and `Nr2f6` had strongest whole-signature Pearson similarities of only 0.115 and 0.086, respectively, over the 1,674 eligible training targets.

I also inspected counterexamples among more distant nuclear receptors and clock-linked transcription factors:

| comparator | observed `n_degs` in 151 | interpretation |
| --- | ---: | --- |
| `Rora` | 278 | A broad, down-dominant thalamic RORalpha program; Distributed Agents reports it as Rora-selective and not phenocopied by `Rorb` or `Rorc`. |
| `Rorb`, `Rorc` | 0, 0 | ROR paralogs were flat despite the `Rora` response. |
| `Nr1d1`, `Bmal1` | 116, 103 | Circadian-accessory/bHLH programs can be detected in 151, but these are mechanistically tied to the ROR/REV-ERB/BMAL1 module rather than to COUP-TFII. |
| `Clock`, `Cry1`, `Cry2`, `Nr1d2` | 3, 1, 3, 1 | Other clock nodes were far smaller than `Bmal1`/`Nr1d1`; module membership alone did not force a broad count. |
| `Esrra`, `Esrrb`, `Esrrg` | 57, 0, 0 | ESRR receptors also diverged. |
| `Ar`, `Esr1`, `Esr2`, `Pgr`, `Thra`, `Thrb`, `Vdr`, `Pparg`, `Ppara`, `Ppard`, `Ppargc1a`, `Nr4a1`, `Nr4a3` | all 0 except `Thra` = 3 | Most represented ligand/nuclear receptors were flat to near-flat in 151. |

This mattered because the `Rora`, `Nr1d1`, and `Bmal1` responses show that the focal cell group and the CRISPR/snRNA-seq pipeline can recover strong transcription-factor and nuclear-receptor signatures when that regulator is an acute postnatal requirement. They do not justify transferring hundreds of DEGs to `Nr2f2`, because even closer ROR, ESRR, and NR2-family relatives frequently failed to phenocopy each other in the same data.

## Target-specific reasoning for `Nr2f2`

`Nr2f2` encodes COUP-TFII, an orphan nuclear receptor transcription factor. The analog-nomination store recovered broad NR, RAR/RXR and transcription-factor annotations, and one exact-complex prior: human NR2F2 and MEF2A share CORUM 5.0 complex 6097, projected to mouse by one-to-one MGI orthology. The exact-complex comparator `Mef2a` was weak in the focal group with 4 DEGs, and `Mef2c` had 1. This argues against a MEF2/NR2F2 interaction prior implying a large corrected signature in postnatal 151 thalamic neurons.

The most directly informative training perturbation is `Nr2f1`, because COUP-TFI/NR2F1 is the closest screened COUP-TF relative. It was not silent but was tiny: two focal DEGs and only sparse responses elsewhere in the Distributed Agents report. `Nr2f6` was even flatter, with 0 focal DEGs and no FDR < 0.10 genes in any recovered neuronal group in the corpus. These are imperfect analogs, because COUP-TF paralogs are developmentally non-interchangeable, but they are more relevant than the high-count `Rora` or `Zfp423` examples.

The external literature pushed in the same low-response direction for this experimental window. Hu et al. showed roles for COUP-TF1 and COUP-TF2 in MGE-derived neocortical interneuron subtype and laminar identity, and Kim et al. showed a postnatal COUP-TFII requirement in cerebellar growth/patterning. Those are real neuronal roles, but neither is the requested 151 thalamic glutamatergic context: the Perturb-seq experiment started at P16, FACS-enriched NeuN+ nuclei, and the focal group is thalamic glutamatergic rather than MGE/CGE GABAergic interneuron or cerebellar circuitry.

I therefore predicted no robust focal effect. A one- or two-gene singleton would not be surprising given `Nr2f1 = 2` and `Mef2a = 4`, but the prior probability mass in this assay is at exactly zero, `Nr2f6` and most NR2/RAR/RXR analogs are zero, and no `Nr2f2`-specific evidence pointed to the exceptional `Rora`/`Bmal1`/`Nr1d1` scale.

## Final point prediction

| target_name | predicted_n_degs |
| --- | ---: |
| `Nr2f2` | 0 |

## Limits

- `Nr2f2` itself was absent from the July Distributed Agents target ledger and from the training Parquet, so this is extrapolation from paralogs and pathway/complex neighbors rather than interpolation from an `Nr2f2` expression profile.
- Nuclear receptors were deliberately used as typed biological comparators, not averaged into a family mean. The family is heterogeneous in this assay: `Rora` and `Esrra` were active, many steroid/RAR/RXR/NR2 perturbations were flat, and `Nr2f1`/`Nr2f6` did not converge.
- The CORUM MEF2-NR2F2 complex is a human record projected to mouse by one-to-one orthology. It supports looking at `Mef2a`, but it does not prove that the same complex is abundant in postnatal mouse 151 thalamic neurons.
- The outside literature establishes strong NR2F biology in other developmental stages and neuronal lineages. Those papers do not directly assay sparse post-P16 CRISPR loss in thalamic Prkcd/Grin2c glutamatergic neurons, so they were used to discount unsupported analogs rather than to set a numeric DEG burden.
- The prediction is a point estimate for an FDR-thresholded, power-dependent count. A weak true downstream effect could still produce zero corrected DEGs with the available perturbed-cell count and snRNA-seq depth.
