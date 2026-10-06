# Pum1 DEG-count prediction

## Question and resolved ambiguities

The requested held-out target file contains one gene:

```tsv
target_name
Pum1
```

I interpreted the task as predicting the exact `n_degs` endpoint for `Pum1` loss in `151 TH Prkcd Grin2c Glut`: the number of assayed genes whose Wilcoxon Benjamini-Hochberg adjusted p-value is `< 0.05`, including `Pum1` itself if the target transcript were to pass that cutoff. `Pum1` was absent from both supplied training files, so no `Pum1` log-fold-change vector or observed count was used. I treated zero as "no measured gene reaches FDR 0.05 in this specific assay" rather than as failed editing or no biology.

## Sources used

- Supplied endpoint counts: `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Supplied differential-expression parquet: `training_de_all_cell_groups.parquet`, filtered to `group_name == "151 TH Prkcd Grin2c Glut"` for the expression-pattern checks below.
- Distributed Agents same-experiment corpus, release `perturbai-july-260713-sourceguard-1773-v1`.
  - There were no frozen Findings or Claims for `Pum1` or `Pum2`.
  - I used the corpus' FMRP/local-translation Claim `claim:cd1432c2212d3410afea`, miRNA/CCR4-NOT/Xrn1 Claims `claim:d51dde311fd8615c6cd1` and `claim:ad4a0296dcb7226557e1`, and the translation/mTOR calibration Claims `claim:ded7056c09e3b5815c0f` and `claim:d9c5c745caea54cd56a7` as same-assay summaries.
- Public literature from PubMed:
  - Van Etten et al. 2012, DOI `10.1074/jbc.M112.373522`.
  - Gennarino et al. 2015, DOI `10.1016/j.cell.2015.02.012`.
  - Zhang et al. 2017, DOI `10.1101/gad.298752.117`.
  - Goldstrohm et al. 2018, DOI `10.1016/j.tig.2018.09.006`.
  - Bohn et al. 2018, DOI `10.1093/nar/gkx1120`.
  - Gennarino et al. 2018, DOI `10.1016/j.cell.2018.02.006`.
  - Enwerem et al. 2021, DOI `10.1261/rna.078436.120`.
  - Botta et al. 2023, DOI `10.15252/embj.2022112721`.

## Dataset operations

1. I counted the focal training endpoints. There are `1674` non-held-out perturbations with `1205/1674 = 72.0%` at `n_degs = 0`; `276` more have only one DEG. Thus weak and singleton responses are the norm in this cell group.
2. I scanned the parquet for `151 TH Prkcd Grin2c Glut` and confirmed the focal group has one full 17,259-gene profile for each of the `1674` training targets.
3. I pulled counts for the training genes selected as biological analogs or counterexamples:

```tsv
set	training_target	n_degs
FMRP/local translation	Fmr1	0
FMRP/local translation	Cyfip1	0
FMRP/local translation	Cyfip2	1
FMRP/local translation	Fxr1	0
FMRP/local translation	Kcnt1	0
miRNA/CCR4-NOT/decay	Ago1	1
miRNA/CCR4-NOT/decay	Ago2	0
miRNA/CCR4-NOT/decay	Dicer1	0
miRNA/CCR4-NOT/decay	Tnrc6a	0
miRNA/CCR4-NOT/decay	Tnrc6b	0
miRNA/CCR4-NOT/decay	Cnot1	0
miRNA/CCR4-NOT/decay	Xrn1	20
translation or NMD	Ddx3x	8
translation or NMD	Eif4a2	2
translation or NMD	Eif4g1	1
translation or NMD	Eif4h	1
translation or NMD	Upf3b	1
mTOR/Atxn1 counterexamples	Mtor	2
mTOR/Atxn1 counterexamples	Tsc2	86
mTOR/Atxn1 counterexamples	Atxn1	187
```

4. I computed pairwise signed log-fold-change profile evidence for these 21 candidates in a run-local Distributed Agents Runtime `profile_compare`, using `pvals_adj < 0.05` only to label significant features. This did not identify a shared significant program among the `Pum1` analogs: across 210 pairwise comparisons in the cohort, the median overlap coefficient of significant features was `0` in both the up- and down-regulated directions. In the top 200 signed features, `Fmr1` shared only `10-21` up-tail genes and `3-53` down-tail genes with `Ago2`, `Cnot1`, `Dicer1`, and `Xrn1`, and none of those pairs shared a significant DEG.

## Target-specific reasoning

### Pum1

PUM1 and PUM2 are sequence-specific PUF-family RNA-binding proteins that bind PUM response elements and usually repress bound RNAs through translational repression and mRNA decay. Human PUM proteins recruit CCR4-NOT deadenylase components, including CNOT subunits, to repress targets (Van Etten et al. 2012; Enwerem et al. 2021). Their neuronal importance is real: Pumilio proteins are required for postnatal dentate-gyrus neurogenesis in mouse conditional knockouts, PUM1 dosage controls ATXN1 abundance and cerebellar disease severity, and human PUM1 haploinsufficiency causes a neurodevelopmental and seizure syndrome (Gennarino et al. 2015, 2018; Zhang et al. 2017; Goldstrohm et al. 2018; Botta et al. 2023).

That biology does not translate cleanly into a broad acute nuclear RNA signature in this assay. `Pum1` loss should weaken a cytoplasmic post-transcriptional repressor for selected target mRNAs, but many PUM1 outputs are protein-level or translational. In Zhang et al. 2017, many Pum1/Pum2 CLIP targets changed at the protein level without comparable changes in mRNA abundance. The experiment here is an snRNA-seq readout in postmitotic juvenile neurons after sparse AAV CRISPR, not a germline or neural-progenitor double knockout, so I down-weighted the developmental lethality and neurogenesis phenotypes.

The closest measured training perturbation was `Fmr1`: Pumilio proteins and FMRP can occupy an overlapping neuronal post-transcriptional network, and Zhang et al. reported RNA-dependent Pum1/Pum2 interaction with FMRP. `Fmr1` had `0` DEGs in `151 TH Prkcd Grin2c Glut`; the adjacent `Cyfip1`, `Cyfip2`, `Fxr1`, and `Kcnt1` comparators were also flat or singleton (`0, 1, 0, 0`). The Distributed Agents corpus summarizes the same screen as showing no robust acute neuronal nuclear RNA module for FMRP/CYFIP/FXR/local-translation perturbations. The `Fmr1` expression vector also lacked any significant overlap with the other post-transcriptional candidates I profiled, so I did not infer a hidden broad PUM-like response from this neighborhood.

Because PUM1 can repress by recruiting CCR4-NOT and then decay machinery, I treated `Cnot1`, `Ago1/Ago2`, `Dicer1`, `Tnrc6a/Tnrc6b`, and `Xrn1` as a second mechanistic panel. The result again argued for a near-null prediction. The direct CNOT scaffold perturbation had `0` DEGs despite only `57` matched perturbed nuclei, the miRNA/RISC and TNRC6 factors were `0` or `1`, and `Xrn1` reached only `20` DEGs while showing no significant-program intersection with `Cnot1` in the pairwise profile. Distributed Agents Claims `d51dde311fd8615c6cd1` and `ad4a0296dcb7226557e1` likewise state that represented miRNA/TNRC6, CNOT, XRN1, and related decay branches did not collapse into one generic neuronal mRNA-silencing signature in this screen.

I considered, but did not use as primary analogs, the larger responses from broad nuclear RNA-processing factors: `Rnpc3` `868`, `U2af2` `828`, `Hnrnpu` `733`, `Tardbp` `210`, and `Hnrnpc` `122` DEGs. Those genes perturb spliceosomal or nuclear RNP functions and the Distributed Agents corpus reports that measured hnRNP-family responses are not interchangeable with each other, much less with a cytoplasmic sequence-specific PUF repressor. I also treated `Atxn1` and `Tsc2` as counterexamples. PUM1 controls ATXN1 abundance over long time scales, but `Atxn1` loss in the training data is not the same direction as derepressing Atxn1 after `Pum1` loss; `Tsc2` is the broad mTOR-axis outlier while `Mtor`, `Fmr1`, and cap-initiation factors were weak in the same assay.

My final zero/nonzero call is therefore: no broad transcriptional state, and even a singleton self-transcript or direct-target hit is more likely to miss FDR than pass. A count of `1` would be plausible if the edited nuclei had a clean `Pum1` self-knockdown, but `Fmr1`, `Ago2`, `Cnot1`, `Dicer1`, `Tnrc6a`, and `Tnrc6b` show that functionally relevant RNA-regulatory perturbations often have no significant self or downstream DEG under this power model. I predicted:

```tsv
target_name	predicted_n_degs
Pum1	0
```

## Limits

The strongest limitation is that both mammalian Pumilio paralogs are absent from the observed training perturbations, and the Distributed Agents same-experiment corpus has no curated `Pum1` or `Pum2` findings. I therefore transferred from FMRP/local-translation and CNOT/miRNA/decay branches, which are mechanistically adjacent but not direct paralogs. The external literature includes strong effects from germline, heterozygous, or conditional developmental Pum1/Pum2 loss and from cultured cells; those experiments alter dosage, cell class, duration, and sometimes both Pumilio paralogs relative to this sparse postnatal CRISPR assay. Finally, `n_degs` is thresholded and sample-size dependent, so the distinction between `0` and a target-self singleton is the least stable part of the call.
