# Question

I predicted the FDR 0.05 DEG-count endpoint for the single requested held-out perturbation, `Mitf`, in `151 TH Prkcd Grin2c Glut` cells.

The requested value is a scalar count, `n_degs`: the number of measured genes whose BH-adjusted Wilcoxon p-value is below 0.05 in the focal thalamic glutamatergic class. `Mitf` was completely absent as a `gene_target` from both supplied training inputs, so no `Mitf` expression signature or observed `Mitf` focal count was available. I treated the supplied Perturb-seq DE Parquet as direct evidence for visible non-held-out perturbation signatures, the focal training-count CSV as direct evidence for visible non-held-out `n_degs`, and the July same-experiment corpus as a packaged interpretation of the same experiment, not as independent replication.

# Sources Used

- Training DEG-count labels: `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Training DE signatures: `training differential-expression dataset`.
- Requested-target manifest: `single-target request for Mitf`.
- Run-local metadata: `task_bindings.json`, `coverage.json`, `dataset_context.md`/`.json`, `measurement_registry.json`, and `capabilities.json` in `codex_runtime/pipeline`.
- Internal same-experiment corpus: `perturbai-july-260713-sourceguard-1773-v1` Findings, Evidence, References, and BioKG graph.
- External literature from PubMed for MiT/TFE lysosome biology and MITF lineage biology:
  - Palmieri et al. 2011, Human Molecular Genetics, doi:10.1093/hmg/ddr306, PMID:21752829.
  - Roczniak-Ferguson et al. 2012, Science Signaling, doi:10.1126/scisignal.2002790, PMID:22692423.
  - Hershey and Fisher 2004, Bone, doi:10.1016/j.bone.2003.08.014, PMID:15050900.
  - Settembre and Perera 2023, Nature Reviews Molecular Cell Biology, doi:10.1038/s41580-023-00676-x, PMID:38001393.

# Computation Over The Supplied Data

I first read the held-out manifest and found exactly one requested target:

```tsv
target_name
Mitf
```

I then summarized the focal-cell training labels. Among 1,674 non-held-out perturbations, 1,205 had `n_degs = 0` and 1,481 had `n_degs <= 1`; the median was 0 and the mean was 14.05, because a small number of perturbations such as `Uba5`, `Tpr`, `Sin3a`, `Rnpc3`, and `Zbtb7a` produced hundreds to thousands of DEGs. This makes the expected background for a lineage-restricted or redundant target zero unless a same-pathway comparator shows a broad response in the relevant neuronal state.

For candidate analogs, I queried the training-count CSV directly and then pulled focal-class Parquet rows only for mechanistically selected targets using PyArrow dataset filters:

```python
f = (
    (ds.field("group_name") == "151 TH Prkcd Grin2c Glut")
    & ds.field("gene_target").isin(targets)
)
table = dataset.to_table(
    columns=["names", "scores", "logfoldchanges", "pvals_adj",
             "gene_target", "n_pert_matched", "n_ctrl_matched"],
    filter=f,
)
```

The count and signature checks were:

| training perturbation | focal n_degs | focal signature evidence | interpretation for Mitf |
| --- | ---: | --- | --- |
| `Mc1r` | 0 | 257 perturbed nuclei and 23,679 controls in `151`; no focal gene had `pvals_adj < 0.05`; the same-experiment Mc1r report recorded zero FDR 0.10 downstream hits in all 23 neuronal classes and no detectable `Mitf`/`Tyr`/`Tyrp1`/`Dct`/`Pmel`/`Slc45a2`/`Oca2`/`Mlph`/`Pax3`/`Sox10` melanogenesis program. | Best within-dataset melanocytic comparator. MC1R is upstream of cAMP/CREB/MITF in melanocytes, and its flat neuronal response argues that the canonical pigment branch is not operating detectably in NeuN+ thalamic neurons. |
| `Pax3`, `Pax6`, `Sox10`, `Sox9`, `Otx2`, `Cspg4` | all 0 | Each had 0 focal DEGs; top absolute-score genes for `Pax3`, `Pax6`, `Sox10`, `Otx2`, and `Cspg4` all remained far from FDR 0.05. | Lineage/developmental neighbors of melanocyte or neural-crest biology are represented but transcriptionally silent in this focal postmitotic neuronal context. They are not exact MiT/TFE paralogs, so they mainly bound the lineage-state alternative. |
| `Myc` | 0 | 210 perturbed nuclei and 23,679 controls; no focal FDR 0.05 genes. | MYC can compete with MiT/TFE factors at lysosome promoters in tumor systems, but its own acute neuronal perturbation was flat, so this does not support a large CLEAR-like response for `Mitf`. |
| `Usf1` | 1 | 200 perturbed nuclei and 23,679 controls; only `Gaa` passed FDR 0.05. | USF-family E-box/CLEAR-motif biology is adjacent but not a direct MITF paralog; the single-gene result supports a negligible focal response. |
| `Atg5`, `Atg16l1`, `Becn1`, `Lamp2`, `Atp6v1a` | all 0 | No focal gene passed FDR 0.05 for these core autophagy/lysosome perturbations. | Loss of individual autophagy/lysosome genes usually failed to elicit a broad survivor-state transcriptional response in this class. |
| `Sqstm1`, `Map1lc3a`, `Atp6v0a1`, `Ctsb` | all 1 | The one significant focal gene was the knocked-down transcript itself for `Sqstm1`, `Map1lc3a`, `Atp6v0a1`, and `Ctsb`. | Even when a lysosomal or autophagy component crossed FDR, the effect was generally self-only rather than a multi-gene thalamic state analogous to strong MITF loss. |
| `Rb1cc1` | 4 | Four focal DEGs: `Calr`, `Hspa5`, `Rb1cc1`, and `Pdia6`. | This gives a small ER/proteostasis stress response after perturbing the FIP200 autophagy-initiation scaffold, but remains very narrow. |
| `Mtor` and `Rptor` | 2 and 0 | `Mtor` produced two focal DEGs, `Rims3` and `Tmed8`; `Rptor` produced none. | MiT/TFE nuclear localization is controlled by mTORC1, but knocking down core mTORC1 components did not create a detectable broad focal transcriptome. |
| `Tsc2` | 86 | 177 perturbed nuclei and 23,679 controls; significant genes included `Cyp51`, `Pik3r3`, `Nefm`, `Slc2a6`, `Hmgcr`, `Lamp2`, `Dpp7`, `Rragd`, and others. The July Tsc2 report summarized a caudal mTORC1 sterol/lysosomal/PI3K response and noted that `Mtor`/`Rptor` loss did not reproduce a robust reciprocal signature. | This is a counterexample, not a direct positive analog. `Tsc2` loss activates Rheb/mTORC1 and engages metabolic feedback, whereas `Mitf` loss would reduce one MiT/TFE transcription factor and is expected to be buffered by TFEB/TFE3 in many cells. |
| `Vps35`, `Vps54`, `Rab7` | 17, 31, 501 | These endosomal trafficking perturbations produced progressively larger signatures; `Rab7` induced lysosomal genes such as `Atp6v1b2`, `Dpp7`, `Scpep1`, `Atp6v0b`, and `Slc20a1`. | These show that the focal neurons can mount a lysosome/endomembrane stress response, but they perturb vesicle trafficking and late endosome/lysosome identity rather than selectively removing a lineage-restricted MiT-family factor. |

I also queried focal Parquet rows where the measured gene was `Mitf`, `Tfeb`, `Tfe3`, or `Tfec` across all visible perturbations. `Mitf` itself never crossed FDR 0.05, `Tfe3` and `Tfeb` each crossed once, and `Tfec` showed only uninformative all-FDR-1.0 pseudocount-scale rows. This is not a direct baseline-expression matrix, but it did not reveal a recurrent endogenous MiT/TFE axis in the visible thalamic signatures.

# Target-Specific Prediction

## Mitf: predicted `n_degs = 0`

**Causal transfer model.** The intervention is acute, sparse AAV-CRISPR loss of `Mitf` in postnatal NeuN+ nuclei; its direct molecular consequence would be reduced MITF function in cells where MITF protein is present; downstream effects would propagate through MITF dimers to pigmentation, lysosome, autophagy, and survival/stress genes; nuclei are then observed only if exposed cells survive, are captured, and retain the `151 TH Prkcd Grin2c Glut` class; the measured endpoint is BH-significant nuclear RNA changes in those recovered thalamic glutamatergic neurons.

The strongest biological reason to predict a null is that MITF's best-established high-leverage roles are tissue-restricted. MITF is a bHLH-LZ MiT-family transcription factor required in melanocytes, retinal pigment epithelium, mast cells, natural killer cells, and osteoclasts, with MITF/TFE3 regulation of osteoclast target genes reviewed by Hershey and Fisher 2004. Those lineages are not enriched in this NeuN+ postnatal neuronal screen. The same-experiment `Mc1r` result is the closest visible check on the melanocyte branch: in melanocytes, MC1R signals through cAMP/PKA/CREB/MITF, but `Mc1r` loss was flat in the focal class and the July corpus explicitly found the expected MITF-linked pigment program absent across all neuronal groups. `Pax3`, `Pax6`, `Sox10`, `Sox9`, `Otx2`, and `Cspg4` were also zero-DEG in the focal class, supporting the inference that neural-crest/pigment lineage regulators are not operating as broad transcriptional controllers in these thalamic neurons.

There is a second plausible route through lysosome/autophagy biology. Palmieri et al. 2011 mapped a TFEB CLEAR network for lysosomal clearance, Roczniak-Ferguson et al. 2012 showed that TFEB and its close relatives TFE3 and MITF are controlled by lysosomal mTORC1-dependent localization, and Settembre and Perera 2023 review MiT/TFE feedback from mTORC1 to lysosome biogenesis. If `Mitf` were the limiting MiT/TFE family member in `151` neurons, its loss could reduce CLEAR genes. The training data do not support that as the default in this experiment: `Atg5`, `Atg16l1`, `Becn1`, `Lamp2`, and `Atp6v1a` were zero, `Sqstm1`/`Map1lc3a`/`Atp6v0a1`/`Ctsb` were self-only, `Usf1` had one DEG, and `Mtor` had two. `Rb1cc1`, `Vps35`, `Vps54`, and especially `Rab7` show that endomembrane stress can be visible, but those interventions directly disrupt trafficking or autophagy scaffolding and should not be transferred to a single, redundant transcription-factor-family member.

`Tsc2` is the main nonzero counterexample because it induced 86 focal DEGs with sterol, PI3K, lysosomal, and feedback genes. I did not use it to predict a nonzero `Mitf` count because the sign and pathway stage differ: TSC2 is an upstream inhibitor of Rheb/mTORC1, and its loss activates a broad metabolic mTORC1 program rather than phenocopying loss of one MiT/TFE activator. The same-experiment Tsc2 report made the same stage distinction by noting that `Mtor` and `Rptor` losses were not robust reciprocal Tsc2-like signatures.

The point prediction is therefore the modal and biologically matched value, 0. A prediction of 1 would mainly be justified by a self-transcript knockdown, but the experiment's measured self-target fold change is explicitly not a reliable editing-efficiency readout, and `Mitf` is not recurrently FDR-significant as a measured transcript in visible focal signatures. I therefore predict no gene, including `Mitf` itself, will pass BH FDR 0.05.

# Limits

The held-out `Mitf` endpoint is absent from the supplied inputs, and the focal DE Parquet is a differential-expression summary rather than a raw expression matrix, so I could not directly test baseline `Mitf` expression in the exact recovered neurons. `Tfeb`, `Tfe3`, and `Tfec` were also not represented as training perturbations, leaving no exact same-family knockout analog. The external MiT/TFE literature mainly comes from melanocytes, osteoclasts, fibroblasts, transformed cells, or generalized lysosome studies rather than P16 mosaic thalamic glutamatergic neurons. Finally, all Parquet and July-corpus evidence are different views of the same Perturb-seq experiment; agreement between them calibrates and interprets the run but is not independent replication.
