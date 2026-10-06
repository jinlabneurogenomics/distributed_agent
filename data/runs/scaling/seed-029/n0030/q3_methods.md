# Q3 cell-type specificity methods

## Eligibility

I read `[local file: n0030.targets.json]` and treated its 30 `gene_targets` as the complete output scope. Differential-expression rows were loaded from `[local file: wilcoxon_de_results_group_name_final_data_no_multi_guide_cells.parquet]`, filtered to those targets and to the 23 allowed `group_name` values, and an eligible pair was defined as:

```python
(pvals_adj < 0.10) & (names.str.casefold() != gene_target.str.casefold())
```

The target-transcript exclusion was applied before counting significant rows. This produced 234 eligible perturbation x cell-type pairs, and `q3_cell_type_specificity.jsonl` emits exactly 234 rows.

## Phenotype Characterization

For each eligible pair I sorted the downstream significant genes by adjusted p value, with absolute log fold change used only as a tie-breaker. The per-pair evidence row records the number of downstream FDR-supported genes, the up/down split, the matched perturbed and control nucleus counts, and the leading downstream genes used to summarize the response. Target-transcript rows, when recovered, were retained only in `statistics.target_transcript` as an engagement caveat and were never used to make a pair eligible.

Recurring modules were identified from the FDR-supported genes rather than from target identity alone. Examples include `Manf` responses dominated by ER-UPR genes such as `Hspa5`, `Hyou1`, `Dnajb9`, and `Pdia6`; `Srsf1`, `Fus`, `Tnpo3`, `Ogt`, and `Hnrnph2` responses dominated by RNA-binding or spliceosome-associated genes such as `Rsrp1`, `Srrm2`, `Fam193b`, `Arglu1`, `Ptbp2`, and `Atxn2l`; V-ATPase/lysosome-associated responses in many `Atp6v0c`, `Atp6v1a`, `Tsc1`, and `Vps41` pairs; and small idiosyncratic one-gene responses for which no coherent module was visible.

## Literature Search

For every pair I combined the perturbed target with the leading FDR-supported genes and, where appropriate, a module term such as `unfolded protein response`, `V-ATPase`, `autophagy`, `splicing`, `mTOR`, `UFM1`, `KCC2`, `HOPS`, or `thalamus`. Searches were run against PubMed through the filtered NCBI gateway; result titles and abstracts were inspected for a target-to-effect relationship, and PMC full text was preferred when the abstract established a likely but incomplete bridge. Queries that returned only a target family, a broad disease association, or unrelated uses of the downstream gene symbol were counted as no pair-specific bridge.

Pairs sharing the same target and the same leading module reused the same literature decision after confirming that the cited target-to-module relationship covered the response genes in that cell group. Usually one to three primary papers or reviews were inspected for such grouped pairs; sparse `No Literature` pairs with only unrelated hits had no cited reference because no target-to-response support remained after title and abstract screening.

## Flag Decisions

`Agree` required a documented target-specific relationship that predicted the direction of the observed response. The only `Agree` calls here were `Manf` pairs in which `Hspa5`, `Hyou1`, `Dnajb9`, or `Pdia6` were up-regulated; MANF is an ER protein that restrains IRE1-alpha UPR signaling, so its loss predicts release of an ER-stress program. I did not call `Disagree`: no searched pair contained both a transferable, target-specific directional expectation and a sufficiently decisive opposite result.

`Inferred` was used when the literature gave a specific but incomplete bridge, such as V-ATPase subunits to lysosomal acidification/autophagy, TSC1 to neuronal mTORC1-autophagy/mitophagy control, UBA5 to UFM1-dependent ER quality control, TNPO3 to SR-protein nuclear import, FUS or SRSF1 to RNA splicing, VPS41 to neuronal HOPS-dependent autophagosome maturation, SLC12A5/KCC2 to thalamic disinhibition, or TCF7L2 to thalamic terminal differentiation. In all of these cases the cited mechanism did not directly document the measured genes or their directions under the acute mosaic Perturb-seq conditions, which prevented an `Agree` or `Disagree` verdict.

`No Literature` was used only after a pair-specific search for the target plus its observed top genes/module did not find a direct or biologically specific partial bridge. General evidence that a target is a chromatin regulator, RNA-associated protein, ciliopathy gene, neurodevelopmental gene, disease gene, or member of a broad complex was not treated as support unless it could be tied to the observed response module.

## Multi-Module And Low-Confidence Pairs

Large responses, especially for `Srsf1`, `Sin3a`, `Ogt`, `Thap11`, `Tsc1`, `Wac`, `Uba5`, and `Wdr26`, often contained several modules. I assigned the pair-level flag to the dominant or most interpretable FDR-supported module and left materially different modules uncited when no target-to-module bridge was found; for example, the `Tsc1` calls rest on lysosome/autophagy/sterol biology and do not claim literature support for every synaptic gene in the same rows.

The lowest-confidence calls are the broad `Inferred` RNA-processing assignments for `Srsf1`, `Fus`, `Ogt`, `Tnpo3`, and `Hnrnph2`, because the prior literature supports the perturbed target's RNA-processing role but not the measured steady-state expression of many specific RNA-binding genes. Sparse one-gene pairs for `Atp6v1a`, `B9d1`, `Bap1`, `Grin2a`, `Myef2`, `Nefl`, `Peg3`, `Pafah1b1`, `Rrn3`, `Tecr`, `Tnrc6a`, `Vps41`, and `Wac` were difficult because they frequently had plausible broad target biology but no target-to-observed-gene bridge; these were left as `No Literature` unless a lysosome, UPR, splicing, or mTOR bridge was specific enough to state explicitly. No eligible pair was left incompletely reviewed.

## Counts

- Eligible pairs: 234
- Emitted pair rows: 234
- Emitted evidence rows: 234
- Emitted cited references: 17
- Incompletely reviewed pairs: 0
