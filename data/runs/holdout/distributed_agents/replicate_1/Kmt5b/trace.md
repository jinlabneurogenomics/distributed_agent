# DEG-count prediction trace

## Question and endpoint

The requested endpoint is a scalar count for each held-out perturbation:
`n_degs`, the number of measured genes with `pvals_adj < 0.05` in the
`151 TH Prkcd Grin2c Glut` focal cell group after acute sparse P16-to-P37/44
mouse neuronal CRISPR loss of function. The held-out target in this run was
`Kmt5b`; its DEG count and its DE signature were absent from both supplied
tables, so the prediction is an extrapolation from non-held-out perturbations.

I treated the supplied
`151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` as the direct observation of
the endpoint for training perturbations. I used
`training_de_all_cell_groups.parquet` for focal-cell expression-pattern context
and for checking whether analog perturbations were broad or narrow in the same
DE surface. I treated the packaged July same-experiment Findings corpus
(`perturbai-july-260713-sourceguard-1773-v1`) as interpreted context from the
same experiment, not as independent replication. I used PubMed/NCBI E-utilities
on 2026-09-03 for external KMT5B literature.

No rank supervision was supplied and no ranking output was requested. The
rank-calibration workbench and predictive graph-review capabilities were
therefore not authorized for this scalar prediction task, and no graph topology
or comparator multiplicity was used as an ordering or scoring signal.

## Quantitative calibration

The focal training table contained 1,674 perturbations. It was strongly
zero-inflated: 1,205/1,674 had 0 DEGs at FDR 0.05, 276 had exactly 1 DEG, the
median was 0, the 90th percentile was 2, the 95th percentile was 18, and the
maximum was 2,677. Thus a held-out target needs fairly close evidence before it
should be assigned a high count.

For candidate analogs, I first used gene function to choose chromatin and
histone-lysine-methylation perturbations present in the training set, then
queried the parquet only for the focal group and those training targets. The
operation was a direct count of rows satisfying
`group_name == '151 TH Prkcd Grin2c Glut'` and `pvals_adj < 0.05`, with the
lowest adjusted p-value genes retained to check whether the signatures looked
like a shared local module or target-specific responses.

| Training analog | FDR 0.05 DEGs in 151 TH | Expression-pattern evidence and interpretation |
| --- | ---: | --- |
| `Ash1l` | 1 | Only the self transcript reached FDR 0.05. The July corpus reports no adjusted downstream DEG in any recovered neuronal group and notes that H3K36/Polycomb-antagonist relatives were weak or null rather than uniformly broad. This is a close negative counterexample for a pathogenic histone methyltransferase in the same acute postmitotic assay. |
| `Nsd1` | 23 | A small positive H3K36-related signature led by `Ddo`, `Pygm`, `Capn3`, and `Ptgds`. Appropriate as a low-positive chromatin writer analog, but it writes a different histone mark from H4K20. |
| `Nsd2` | 0 | No focal FDR 0.05 gene despite representation in the same class. This argues that NSD/H3K36 family membership alone does not imply a detectable thalamic DEG burden. |
| `Setd2` | 1 | Only `Septin5` reached FDR 0.05. Like `Ash1l` and `Nsd2`, this shows buffering of some H3K36-axis perturbations. |
| `Kmt2a` | 24 | A low-positive H3K4 writer signature, with `Nr2f1`, `Pcdh7`, `Lhx9`, and the `Kmt2a` self transcript among the top focal rows. Useful for scale, not for exact pathway transfer. |
| `Kmt2c` | 0 | Null H3K4-related counterexample. |
| `Setd1a` | 368 | Broad outlier among histone methyltransferases, led by many mitochondrial/processing genes such as `Itfg1`, `Foxred1`, `Nprl3`, `Sfi1`, and `Tafazzin`. I treated it as a counterexample showing that the assay can detect chromatin effects, not as a close KMT5B proxy. |
| `Setdb1` | 22 | Low-positive H3K9 writer response led by `Tasor`, `Ccdc84`, `Pmvk`, `Abhd12b`, and `Atf7ip`. Mechanistically distinct but a useful low-count chromatin-repression analog. |
| `Ehmt1` | 4 | Very narrow H3K9 methyltransferase response led by `Abhd12b`. |
| `Kdm5b` | 0 | H3K4 demethylase null. |
| `Kdm5c` | 18 | Low-positive H3K4 demethylase response led by `Ptgds`, `Capn3`, `Man2a2`, `Zfp532`, and `Col9a3`. |
| `Adnp` | 25 | An NDD chromatin regulator with a narrow focal surface led by `Xylt2`, `Cpne7`, and `Srrm4`; the corpus reports selective thalamic/midbrain rather than pan-neuronal behavior. |
| `Arid1b` | 1 | Core NDD BAF subunit but essentially flat in the focal group. The corpus specifically reports that other mSWI/SNF relatives did not phenocopy `Arid1b`, another warning against generic chromatin transfer. |
| `Chd2` | 34 | Moderate NDD remodeler response led by `Snhg11`, `Plekhg1`, and `Ptpn3`. |
| `Chd8` | 61 | Moderate NDD remodeler response led by `Pnisr`, `Tmem50a`, and `Chd8`, broader than most methyltransferase analogs. |

The nearest enzymatic comparison for KMT5B would have been KMT5A or KMT5C,
because KMT5A deposits H4K20me1 and SUV4-20H/KMT5B-KMT5C enzymes convert it to
H4K20me2/3. Those genes were not present in the focal training table. I
therefore did not assign a large count from an obligate same-complex neighbor;
the estimate comes from weaker mark-level and chromatin-disease analogs.

## Kmt5b reasoning

KMT5B/SUV420H1 is a nucleosomal H4K20 methyltransferase. Structural and
biochemical work shows that SUV420H1 recognizes nucleosomes, including
H2A.Z-containing nucleosomes, to methylate H4K20 and participate in chromatin
compaction, DNA replication, and repair (Lin 2023, DOI
10.1038/s41421-023-00620-5; Huang 2023, DOI
10.1016/j.molcel.2023.07.001; Abini-Agbomson 2023, DOI
10.1016/j.molcel.2023.07.020). Depletion of SUV4-20H enzymes blocks conversion
of H4K20me1 toward H4K20me2/3 in other systems and can drive large
lineage-specific transcriptional changes, for example in Xenopus multiciliated
cell differentiation (Angerilli 2023, DOI 10.26508/lsa.202302023).

External neurodevelopmental evidence supports `Kmt5b` as a genuine neuronal
chromatin gene but does not match the held-out assay directly. Loss-of-function
KMT5B variants cause an overgrowth/intellectual-disability syndrome and are
enriched among neurodevelopmental-disorder genes (Stessman 2017, DOI
10.1038/ng.3792; Faundes 2017, DOI 10.1016/j.ajhg.2017.11.013). Patient-cell
and mouse-brain work found that KMT5B haploinsufficiency perturbs pathways
related to nervous-system development and axon guidance (Sheppard 2023, DOI
10.1126/sciadv.ade1463). Human cortical organoids showed that SUV420H1/KMT5B,
`ARID1B`, and `CHD8` haploinsufficiency all alter neuronal developmental
timing, but through largely distinct molecular pathways (Paulsen 2022, DOI
10.1038/s41586-021-04358-6).

The causal transfer chain is therefore:

`Kmt5b` CRISPR loss -> reduced SUV420H1 H4K20me2/3 writing and chromatin
effects -> altered repression/replication-repair/developmental programs -> only
postmitotic, recovered, P37/P44 thalamic glutamatergic neurons are sampled ->
DEGs counted by single-nucleus Wilcoxon FDR.

The first two links are well supported, but the training experiment starts
after most cell-fate specification, uses sparse mosaic acute CRISPR, and samples
surviving NeuN-positive neurons rather than proliferating progenitors. That
breaks a direct same-outcome transfer from developmental organoids,
whole-brain germline or haploinsufficient mouse measurements, Xenopus
ciliogenesis, and cancer-cell DNA-replication phenotypes. Within this assay,
close chromatin writers with different histone marks mostly produced either no
response or low-positive counts; even disease genes such as `Ash1l`, `Arid1b`,
`Kmt2c`, and `Nsd2` were buffered, while `Kmt2a`, `Nsd1`, `Setdb1`, `Adnp`, and
`Kdm5c` clustered between 18 and 25 DEGs.

I therefore predicted a real but very small focal signature for `Kmt5b`, below
the low-positive writer analogs and far below `Setd1a`/`Chd8`: **8 DEGs**.
This is primarily driven by the training counts of mechanistically related
histone-modification genes, with external KMT5B literature used to shift the
call away from a pure zero.

## Limits

`Kmt5b` has no exact H4K20 paralog or obligate partner in the supplied focal
training endpoint table, so the prediction depends on imperfect chromatin
analogs. The external studies establish KMT5B function in neurodevelopment and
chromatin regulation but usually measure germline, developmental, organoid,
non-neuronal, or proliferating-cell consequences rather than the same acute
postmitotic thalamic-neuron endpoint. The supplied assay is also
survivor-conditioned: a quiet DEG signature could reflect buffering, low power,
or selection before nuclei were recovered. For these reasons the zero/nonzero
decision is uncertain and the integer count should be read as a point estimate
near the lower edge of the detectable positive range, not as a mechanistic
stoichiometric expectation.
