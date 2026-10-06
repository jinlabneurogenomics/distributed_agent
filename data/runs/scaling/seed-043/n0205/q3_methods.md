# Q3 methods

## Eligibility

The target manifest contained 205 perturbations, and I restricted the full parquet to exactly those `gene_target` values and the 23 allowed `group_name` labels. An eligible pair was defined with this downstream-only query:

```sql
SELECT gene_target, group_name
FROM parquet_scan('[local file: wilcoxon_de_results_group_name_final_data_no_multi_guide_cells.parquet]')
WHERE gene_target IN (<205 manifest targets>)
  AND group_name IN (<23 allowed cell groups>)
  AND pvals_adj < 0.10
  AND lower(names) <> lower(gene_target)
GROUP BY gene_target, group_name;
```

This produced 891 eligible perturbation x cell-type pairs. I emitted 891 pair rows, one for each eligible pair, and no ineligible pairs.

## Phenotype Characterization

For each eligible pair I counted all downstream FDR-supported genes, counted up- and down-regulated rows from the sign of `logfoldchanges`, recorded `n_pert_matched` and `n_ctrl_matched`, and selected the strongest observed genes by minimum `pvals_adj`: the overall top gene, the strongest up-regulated gene when present, and the strongest down-regulated gene when present. Those genes are the dataset-derived `evidence_ids` used by the pair summaries; the perturbed target transcript was not used as eligibility evidence.

Pairs with one FDR-supported gene were reduced to that gene-level response. Pairs with several or hundreds of FDR-supported genes were summarized as a mixed, up-dominated, or down-dominated module centered on the strongest up/down genes rather than on every significant row, so large perturbations such as `Psmc1`, `Psmc5`, `U2af2`, `Rnpc3`, and `Hnrnpu` did not drown the output in full DE tables.

## Literature Search

Searches were pair-specific in that the query combined the perturbed target with the leading measured downstream gene or module class before checking broader target mechanisms. PubMed was the primary source; queries were tightened around exact target symbols and mechanisms such as `ACTB ACTG1 compensation`, `Transcription factor Nrf1 proteasome recovery pathway`, `BMAL1 Dbp`, `TDP-43 cryptic exons`, `FUS loss of function splicing neurons`, `RBFOX1 neuronal splicing`, `RNPC3 minor spliceosome`, `XPO1 pre-snRNA export`, `CHD4 NuRD neurons`, and `KMT2B neuronal transcriptome`. Queries that only returned broad disease genetics, family membership, or an unrelated developmental phenotype were not accepted as target-to-response support.

## Flagging Rules

`Agree` was reserved for direct or directionally complete evidence: ACTB loss increasing ACTG1, and BMAL1 loss decreasing the DBP circadian output gene. `Inferred` was used when literature gave a target-specific but incomplete bridge, such as proteasome recovery downstream of PSMC/NRF1 perturbation or splicing consequences downstream of Tardbp, Fus, Rbfox1, Rnpc3, and Xpo1 perturbation. Those bridges are recorded with `indirect` and the relevant context differences.

`No Literature` was assigned when the pair-level search found no target-specific bridge to the observed leading gene or central up/down module. General evidence that a target is chromatin-associated, neurodevelopmental, disease-associated, or expressed in neurons was not enough to prevent `No Literature` unless it connected the exact target to a specific measured response class.

## Difficult Pairs

The lowest-confidence calls are large mixed RNA-processing and chromatin responses where the target biology is real but the observed 3-prime abundance module is not a direct readout of the documented mechanism. I therefore marked `Psmc1`, `Psmc5`, `Nrf1`, `Tardbp`, `Fus`, `Rbfox1`, `Rnpc3`, `Xpo1`, `Chd4`, and `Kmt2b` as `Inferred` rather than forcing `Agree` or `Disagree`. The many remaining one-gene or small-module pairs were difficult because a pair-specific target-to-leading-gene query did not find even an incomplete mechanistic bridge; those are explicitly summarized as `No Literature` rather than being collapsed into a target-level result.

Total eligible pairs: 891. Emitted pair rows: 891. Incompletely reviewed pairs: 0.
