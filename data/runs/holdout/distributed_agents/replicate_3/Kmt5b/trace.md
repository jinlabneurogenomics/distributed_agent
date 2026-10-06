# Kmt5b DEG-count prediction trace

## Question and resolved ambiguities

The requested endpoint is the number of genes with `pvals_adj < 0.05` after each held-out CRISPR perturbation in the focal cell group, `151 TH Prkcd Grin2c Glut`. The endpoint is therefore an assay-specific breadth count from the Wilcoxon differential-expression table, not a measure of gene essentiality or developmental phenotype size.

The manifest for this run contains one held-out target:

```text
Kmt5b
```

`Kmt5b` is absent from both the training DEG-count table and the DE parquet as a perturbation target, so all within-dataset evidence below comes from other targets assayed in the same cell group.

## Sources used

- Input training count CSV: `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Input training DE parquet: `training_de_all_cell_groups.parquet`, restricted to `group_name == "151 TH Prkcd Grin2c Glut"` for profile comparisons.
- Distributed Agents corpus, release `perturbai-july-260713-sourceguard-1773-v1`, for same-experiment claims about `Nsd1`, `Setdb1`, `Ehmt1`, and `Dnmt3a`.
- Distributed Agents runtime profile comparison over a hand-declared 33-target chromatin cohort, using `logfoldchanges` as the signed feature value and `pvals_adj < 0.05` as the significance definition.
- Local Distributed Agents gene-annotation tables:
  - GO/KEGG/Reactome membership placed `Kmt5b` in histone H4K20 methyltransferase activity, PKMT histone-lysine methylation, and chromatin organization annotations.
  - STRING v12.0 had one mouse `Kmt5b` direct physical-interaction edge, to `Dnmt3a`, but it was text-mining-only (`score = 0.744`) and was treated as weak.
  - CORUM 5.0 plus MGI one-to-one homology, downloaded 2026-09-13, supplied no exact same-complex training target for `Kmt5b`.
- External biological literature:
  - Benetti et al. 2007, DOI `10.1083/jcb.200703081`, PubMed `17846168`: Suv4-20h enzymes are responsible for telomeric H4K20me3 and influence telomere recombination.
  - Jorgensen, Schotta, and Sorensen 2013, DOI `10.1093/nar/gkt012`, PubMed `23345616`: SET8/KMT5A monomethylates H4K20, while SUV4-20H1/KMT5B and SUV4-20H2/KMT5C mediate higher H4K20 methylation involved in genome integrity, DNA repair, replication, and chromatin compaction.
  - Stessman et al. 2017, DOI `10.1038/ng.3792`, PubMed `28191889`: damaging KMT5B variants were identified among neurodevelopmental-disorder risk genes.
  - Wickramasekara et al. 2021, DOI `10.1002/aur.2516`, PubMed `33871180`: heterozygous Kmt5b gene-trap mice have neurodevelopmental and behavioral phenotypes.
  - Chen et al. 2022, DOI `10.1016/j.jgg.2022.03.004`, PubMed `35331928`: KMT5B loss of function is linked to neurodevelopmental disorder; Kmt5b knockdown in mouse cortical neurons altered dendritic complexity/spine density, and in utero knockdown affected progenitor proliferation and migration.

## Computation over the supplied data

I first summarized the focal training endpoint. There are 1,674 non-held-out targets. The distribution is zero-heavy: median `0`, 75th percentile `1`, 90th percentile `2`, 95th percentile `18`, 99th percentile about `436`, and maximum `2677`. Only 469 of 1,674 targets are nonzero; only 106 have at least 10 DEGs.

To ground `Kmt5b` in measured analogs, I extracted all `151 TH Prkcd Grin2c Glut` parquet rows for 33 chromatin-regulator comparators chosen from H3K/H4K writers, chromatin repressors, and counterexamples named by the Distributed Agents corpus. The extract had 569,547 `(target, measured gene)` rows and was passed to `profile_compare` with:

```text
entity_column = gene_target
feature_column = names
value_column = logfoldchanges
significance_column = pvals_adj
significance_threshold = 0.05
```

The most relevant observed focal DEG counts were:

```tsv
target	n_degs
Setd1a	368
Brd4	311
Smarcc2	185
Chd4	100
Zmynd8	74
Chd8	61
Arid2	56
Chd2	34
Kmt2a	24
Nsd1	23
Setdb1	22
Arid1a	22
Kdm5c	18
Mecp2	16
Setd5	9
Crebbp	8
Brd1	4
Ehmt1	4
Setd2	1
Ash1l	1
Dnmt3a	0
Ep300	0
Hdac5	0
Hdac8	0
Kat6a	0
Kat6b	0
Kdm5b	0
Kmt2c	0
Mbd5	0
Nsd2	0
Smarca4	0
Smchd1	0
Zmynd11	0
```

The profile inspection supported using the small chromatin-repressor counts rather than the broad remodelers as the main calibration set:

- `Nsd1` had 23 significant genes, `20` up and `3` down. The Distributed Agents corpus reports that `Nsd1` converges with `Zmynd8` and `Kdm5c` on a same-direction thalamic de-repression module, including `Myo5c`; the runtime comparison recovered 8 shared same-direction significant up-regulated genes between `Nsd1` and `Zmynd8`.
- `Setdb1` had 22 significant genes, `17` up and `5` down. The corpus calls its response sparse and cell-type-restricted, with protocadherin and `Atf7ip`/`Tasor` output rather than a generic interferon or broad stress state. It also explicitly contrasts `Setdb1` with flat `Dnmt3a` and `Smchd1` and with only weak `Ehmt1` overlap.
- `Ehmt1` had only 4 significant genes in the focal table, all up. The corpus describes this as a very sparse TH chromatin-repressor-linked module that shares a few genes with `Chd4`, `Setdb1`, and `Sin3a` rather than a broad Kleefstra-like or synaptic program.
- `Dnmt3a`, the only local STRING edge for `Kmt5b`, had 0 focal DEGs; the corpus interprets `Dnmt3a` as a buffered acute P16 perturbation of a cumulative DNA-methylation writer and notes that the identical assay readily detects other chromatin regulators.

I did not use whole-profile correlations among the weak chromatin targets as quantitative weights, because vectors with thousands of tiny nonsignificant log-fold changes and sparse, high-amplitude `pvals_adj = 1` genes can rank flat nodes together. The decision came from the actual focal FDR counts, shared FDR-positive genes, and biological relevance of each target.

## Target-specific reasoning

### Kmt5b

`Kmt5b` encodes SUV4-20H1, an H4K20 methyltransferase. GO and Reactome put mouse `Kmt5b` in H4K20 histone methyltransferase activity and chromatin organization. The most exact enzymatic relatives, `Kmt5a`/SET8 and `Kmt5c`/SUV4-20H2, were not profiled as perturbation targets in the training count table, so there is no direct same-mark paralog count to transfer.

The strongest broad chromatin responders in the same focal cell type are poor one-hop analogs. `Setd1a` at 368, `Brd4` at 311, `Smarcc2` at 185, and `Chd4` at 100 are immediate transcriptional coactivator/corepressor or remodeler nodes with large same-assay surfaces. KMT5B is instead a writer of the stable H4K20me2/H4K20me3 heterochromatin mark. Published SUV4-20H work ties the mark to telomeres, DNA damage/replication, and genome integrity, processes that are partly outside the coding-gene nuclear-RNA readout and further displaced in postmitotic P16-to-P37/44 neurons.

The closest measured positive analogs are the smaller repressive methylation outputs. `Setdb1` gives a 22-gene focal response, but that response is an H3K9/HUSH and clustered-protocadherin program with induced `Atf7ip` and `Tasor`; the Distributed Agents corpus explicitly warns that it is not reproduced by `Dnmt3a`, `Smchd1`, or a generic set of adjacent chromatin repressors. `Ehmt1` is therefore the more conservative count analog: it is also an NDD-linked repressive histone methyltransferase in the same broad H3K9/heterochromatin neighborhood, but its acute postnatal response is just 4 focal DEGs.

The counterexamples push the prediction downward. `Dnmt3a` had 0 DEGs despite its developmental disease biology and the weak STRING text-mining edge to `Kmt5b`; `Nsd2`, `Kmt2c`, `Kdm5b`, `Mbd5`, `Smarca4`, `Smchd1`, `Ep300`, `Kat6a`, and `Kat6b` were also flat in the focal count table. The Distributed Agents same-experiment claims emphasize that chromatin genes that look adjacent by mark, domain, or disease label are often buffered or noninterchangeable in this acute neuronal assay.

External KMT5B evidence kept the estimate above zero. KMT5B loss-of-function variants cause neurodevelopmental disorder; cultured or embryonic mouse knockdown affects dendrites, spines, progenitor proliferation, and migration; and Kmt5b haploinsufficient mice have behavioral/developmental phenotypes. Those phenotypes argue that neuronal and neurodevelopmental systems are sensitive to KMT5B dosage, even if much of that sensitivity is prenatal and may not produce a broad acute P16 postmitotic RNA signature.

Balancing those points, I predict a real but very sparse response: closer to `Ehmt1`/`Brd1` at 4 than to `Setd5`/`Crebbp` at 8-9, and far below `Setdb1`/`Nsd1` near the low 20s. The final point prediction is:

```text
Kmt5b -> 4 DEGs
```

## Limits and extrapolations

- The key missing datum is an exact H4K20 perturbation: `Kmt5a` and `Kmt5c` were not in the focal training target table, and `Kmt5b` itself was held out completely.
- The local database did not expose an exact KMT5B protein complex containing a represented perturbation target; the lone `Dnmt3a` STRING link was text-mining-only and weak for count transfer.
- H4K20me3 effects on telomeric/subtelomeric chromatin, transposons, DNA damage, or chromatin compaction may be invisible to a coding-gene 10x Flex nuclear RNA DEG count.
- KMT5B protein and histone-mark turnover over 3-4 weeks after sparse P16 AAV CRISPR could be slower than mRNA editing. A flat DEG count would not prove failed editing.
- The external KMT5B literature is richer for constitutional or embryonic loss than for acute loss in juvenile postmitotic thalamic neurons, so the nonzero call is extrapolated from general chromatin and NDD biology plus `Ehmt1`/`Setdb1` within-dataset behavior.
