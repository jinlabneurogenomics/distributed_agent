# Held-out DEG-count prediction trace

## Question and endpoint

I interpreted the task as a point prediction for the held-out `Atf2` perturbation in the single focal class `151 TH Prkcd Grin2c Glut`.  The endpoint is exactly the count of measured mouse genes whose adjusted Wilcoxon p value is below 0.05 in perturbed versus matched control recovered nuclei.  A prediction of 0 means no gene is expected to cross the FDR 0.05 cutoff in this assay; it does not mean ATF2 is biologically irrelevant.

The requested target CSV contained one row:

```tsv
target_name
Atf2
```

The requested endpoint is absent for `Atf2`: `Atf2` was held out as a `gene_target` and is not present in the training DEG-count CSV.  The training DEG counts are direct observations of the same endpoint for non-held-out perturbations.  The large DE parquet is direct evidence for each visible comparator's gene-level expression pattern.  Packaged same-experiment corpus reports were used only to interpret those visible comparator responses; they are another representation of the same Perturb-seq experiment, not independent replication.

## Sources

- Training endpoint table: `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared Perturb-seq DE parquet: `training differential-expression dataset`.
- Requested-target manifest: `single-target request for Atf2`.
- Run-local dataset portrait, bindings, coverage, capability, and measurement registries under `codex_runtime/pipeline/`.
- Internal same-experiment interpretation corpus: `perturbai-july-260713-sourceguard-1773-v1`, queried through `corpus.findings`, `corpus.report_evidence`, and a bounded BioKG lookup for visible comparators.  `Atf2` itself was not a visible `TargetGene` or `Gene` node in that graph.
- External mechanism literature was retrieved from NCBI PubMed E-utilities.  Key records used were Liu et al. 2006, DOI `10.1038/sj.emboj.7601020`, PMID `16511568`; Morton et al. 2004, DOI `10.1016/j.febslet.2004.07.031`, PMID `15304344`; Breitwieser et al. 2007, DOI `10.1101/gad.430207`, PMID `17699753`; Yuan et al. 2009, DOI `10.1128/MCB.01344-08`, PMID `19255142`; and Gozdecka and Breitwieser 2012, DOI `10.1042/BST20110630`, PMID `22260696`.

## Quantitative calibration from the declared inputs

The endpoint table has 1,674 non-held-out perturbations in this focal class.  It is strongly sparse:

```tsv
quantity	value
median_n_degs	0
mean_n_degs	14.05
training_targets_with_zero	1205
training_targets_with_positive_count	469
95th_percentile_n_degs	18
99th_percentile_n_degs	436.48
max_n_degs	2677
```

The same distribution has a few very broad outliers such as `Uba5` with 2,677 DEGs, `Tpr` with 1,768, `Sin3a` with 1,433, and spliceosome or proteasome components with hundreds of DEGs.  Those high-yield perturbations are poor analogs for `Atf2`: they perturb core proteostasis, RNA processing, or chromatin-maintenance processes and are not near the ATF2/AP-1/MAPK causal branch.

I then queried the parquet for the requested focal group and the biologically relevant visible ATF/AP-1/MAPK/CREB/small-Maf comparators.  The operation was:

1. Filter `group_name == "151 TH Prkcd Grin2c Glut"`.
2. Keep visible comparators around `Atf2`: `Atf6`, `Creb1`, `Crebbp`, `Jund`, `Fosl2`, `Maf`, `Mafa`, `Mafb`, `Mafg`, `Map2k1`, `Map2k2`, `Map2k6`, `Map3k7`, `Mapk1`, `Mapk9`, `Nfe2l1`, `Nfe2l2`, and STAT-family negative controls.
3. Count `pvals_adj < 0.05` and list the significant measured genes.

For the most relevant comparators the focal-class results were:

```tsv
training_target	n_degs_in_151TH	significant_pattern_at_FDR_0.05
Jund	0	no genes
Fosl2	0	no genes
Atf6	0	no genes
Maf	0	no genes
Mafa	0	no genes
Mafb	0	no genes
Mafg	1	Lamp2 up
Mapk1	0	no genes
Mapk9	0	no genes
Map2k6	0	no genes
Map3k7	0	no genes
Map2k1	4	Vgf, Ptpn5, Unc13a, and Etv5 down
Creb1	10	Crem up; Tmem181a, Txndc12, Chkb, Nceh1, Ppox, Rnf139, and Sez6l2 down; Vwc2l up; Creb1 itself up
Crebbp	8	sparse mixed signature headed by Stxbp2 up
Nfe2l1	0	no genes
Nfe2l2	0	no genes
```

The requested endpoint is therefore directly observed for the visible comparators, and those observations support a zero-or-very-small prior for an unstimulated ATF2 loss in this cell class.  `Creb1` and `Crebbp` are the positive counterexamples: nearby CREB/ATF/CBP transcriptional machinery can give a small response in 151 TH neurons, but the response is only 8-10 genes and is not an AP-1 or immediate-early program.  `Map2k1` is a second small counterexample with an ERK-linked `Vgf`/`Ptpn5`/`Etv5` module.  In contrast, the direct AP-1/bZIP branch represented by `Jund` and `Fosl2` was silent in 151 TH, the p38/JNK-side kinases `Mapk9`, `Map2k6`, and `Map3k7` were silent, and large-Maf/small-Maf/NRF-family bZIP losses were silent or one-gene.

## Target-specific reasoning

### Atf2

ATF2 is a basic leucine-zipper transcription factor in the CREB/AP-1 family.  It is activated by stress MAPK phosphorylation; JNK and p38 can phosphorylate ATF2 sites in mouse fibroblasts (Morton et al. 2004, DOI `10.1016/j.febslet.2004.07.031`, PMID `15304344`), and ATF2 can heterodimerize with c-Jun as an AP-1/CRE-binding factor (Liu et al. 2006, DOI `10.1038/sj.emboj.7601020`, PMID `16511568`).  ATF2 and the homolog ATF7 also share developmental functions: ATF2 phosphorylation-site mutation phenocopied loss of the DNA-binding domain, and combining ATF2 impairment with `Atf7` knockout caused embryonic liver and heart lethality through a p38-feedback defect (Breitwieser et al. 2007, DOI `10.1101/gad.430207`, PMID `17699753`; Gozdecka and Breitwieser 2012, DOI `10.1042/BST20110630`, PMID `22260696`).  In challenged neurons, c-Jun/ATF2 dimers can participate in apoptotic transcription under potassium deprivation (Yuan et al. 2009, DOI `10.1128/MCB.01344-08`, PMID `19255142`).

Those mechanisms are real, but they predict strong ATF2 output in a stress-activated, developmental, or injury/apoptosis setting, not necessarily in unstimulated P16-to-P37/44 postmitotic NeuN-positive nuclei.  The training parquet strongly favors the latter interpretation in this exact focal group:

- `Jund`, the represented Jun-family AP-1 factor, had 261 perturbed 151 TH nuclei and 0 FDR<0.05 genes.  Its same-experiment corpus report summarized the whole response as buffered: 22 of 23 measured cell groups had no downstream genes at FDR<0.10, and AP-1/bZIP relatives and MAPK neighbors did not phenocopy the residual one-gene response outside 151 TH.
- `Fosl2`, the represented Fos-family AP-1 factor, had 211 perturbed 151 TH nuclei and 0 FDR<0.05 genes.  The corpus likewise found it almost completely buffered across P16-to-P37/44 postmitotic neurons, with its only downstream event in 155 MB Glut rather than in 151 TH.
- `Mapk9`/JNK2, `Map2k6` on the p38 arm, and `Map3k7` upstream of p38/JNK all had 0 DEGs in 151 TH.  `Mapk1` also had 0, while the positive ERK-pathway lesion `Map2k1` produced only a 4-gene `Vgf`/`Ptpn5`/`Unc13a`/`Etv5` signature.  This argues against a constitutive MAPK-to-ATF2 transcriptional state being captured by the basal assay.
- `Creb1` had the broadest local CREB/ATF-like footprint but only 10 genes at FDR 0.05; its significant genes centered on `Crem` compensation and an ER/lipid/lysosome/heme/membrane module, not an ATF2/AP-1 stress program.  The packaged Creb1 analysis reported that represented PKA, CBP/p300, TrkB, CaMK, and MAPK perturbations did not phenocopy it and that basal `Bdnf`/`Fos`/`Arc`/`Npas4` immediate-early targets were absent.
- `Atf6` is a more distant ATF bZIP factor, but it was a useful counterexample for stress-conditional transcription factors: it had 177 perturbed 151 TH nuclei and no downstream genes.  The same-experiment report showed this was a basal ATF6 null despite the assay's ability to detect an ER quality-control response after `Hspa5` perturbation.
- Small and large Maf/NRF-family bZIP factors were not broad alternatives for ATF2.  `Maf`, `Mafa`, `Mafb`, `Nfe2l1`, and `Nfe2l2` were zero in 151 TH; `Mafg` had only `Lamp2` at FDR 0.05.

The causal transfer model is therefore: acute sparse CRISPR `Atf2` loss should reduce ATF2 protein function in a subset of recovered thalamic glutamatergic neurons; ATF2 loss would propagate most strongly through JNK/p38-activated AP-1/CRE transcription and through ATF-family compensation; but the experiment did not impose UV, cytokine, ER stress, potassium deprivation, axotomy, or embryonic-liver-like developmental stress, and the analogous visible kinases and dimer partners were mostly silent.  The expected 151 TH survivor-state RNA response is thus zero or a handful of genes rather than a broad DEG program.

I set the point prediction to **0 DEGs**.  The specific zero is slightly more likely than a small nonzero value because the best direct branch comparators, `Jund`, `Fosl2`, `Mapk9`, `Map2k6`, and `Map3k7`, were all zero in the focal class despite good perturbed-cell recovery.  A 1-10 DEG outcome analogous to `Mafg`, `Map2k1`, or `Creb1` would not be surprising, but the local evidence does not identify an ATF2-specific basal marker such as `Crem`, `Lamp2`, or `Vgf` that should pass FDR.

## Limits and uncertainty

- There is no `Atf2` expression signature in the declared parquet; every inference for `Atf2` is a transfer from visible pathway members plus external ATF2 biology.
- The closest paralogs `Atf7` and `Atf1`, and the strongest AP-1 partners `Jun`, `Junb`, and `Fos`, were not present as training perturbations, so the transfer relies on `Jund`, `Fosl2`, `Creb1`, `Crebbp`, and MAPK nodes.
- The parquet and same-experiment corpus are two surfaces over one experiment.  Agreement between them increases interpretability but is not biological replication.
- ATF2 is stimulus- and partner-dependent.  The prediction should not be extrapolated to UV/stress, inflammatory, injury/apoptosis, retinal, tumor, embryonic, or compound `Atf2`/`Atf7` settings.
- The endpoint is a sharp FDR count.  The difference between 0 and a few DEGs could be driven by power, recovered nucleus count, and multiple-testing thresholding, not by a qualitative biological switch.
