# Q3 cell-type-specific literature assessment

## Eligibility

I loaded `[local file: n0030.targets.json]` and treated its 30 `gene_targets` entries as the complete output scope. I queried `[local file: wilcoxon_de_results_group_name_final_data_no_multi_guide_cells.parquet]` for those targets and the 23 allowed `group_name` labels, then defined an eligible pair as one with at least one row satisfying `pvals_adj < 0.10 AND lower(names) <> lower(gene_target)`. This yielded 213 eligible pairs, and `q3_cell_type_specificity.jsonl` emits exactly 213 rows.

## Phenotype characterization

For each eligible pair, I used all downstream rows with adjusted Wilcoxon `p < 0.10` after target-transcript exclusion, counted up- and down-regulated genes, and ranked genes by `pvals_adj` with absolute `logfoldchanges` as the tie breaker. Evidence rows report the leading FDR-supported genes, the number of significant downstream genes, the up/down split, perturbed and matched-control nucleus counts, and the target-transcript row when it was present. The target transcript was used only as an engagement caveat inside the evidence statistics and never as the qualifying downstream hit.

Central modules were selected from the most significant genes plus recurrence across cell types for the same perturbation. The clear recurrent modules were Psmc1/Psmc5 proteasome-stress responses, Hspa9 mitochondrial or amino-acid stress responses, the single Vps41 lysosomal Mcoln1 response, and many target-specific RNA-processing or chromatin-factor signatures for which the measured genes did not collapse onto a documented named pathway downstream of the target.

## Literature searches and flag rules

PubMed was searched with target symbols, common aliases when needed, the top significant genes, and recurrent module genes. Examples included `Psmc1` or `Psmc5` with proteasome stress genes such as `Bax`, `Ddit3`, and `Sqstm1`; `HSPA9`/mortalin with `SHMT2`, `CHAC1`, and mitochondrial stress; `VPS41` with HOPS, lysosome, TFEB, and `MCOLN1`; splicing targets `RNPC3`, `CDC40`, `U2AF2`, and `SRRM2` with their leading DEGs; and chromatin or transcriptional targets including `ANKRD11`, `CHD4`, `KMT2B`, `SETD1A`, `KANSL1`, `TRRAP`, `PROX1`, `SMARCE1`, `NR1D1`, and `TCF7L2` with their pair-defining DEGs. For sparse one-gene pairs, the searched relationship was the exact target-to-gene pair.

`Agree` was used only when a target-specific perturbation or a complete explicit chain predicted the observed direction of the central response. The accepted chains were Psmc1 or Psmc5 loss causing 19S/proteasome impairment and proteasome impairment in neuronal cells causing a stress/apoptotic program. `Inferred` was used for specific but incomplete bridges: Hspa9 loss to mitochondrial stress without a direct CHAC1/SHMT2/DDIT3 neuronal transcript expectation, and Vps41 loss to HOPS/TFEB lysosomal regulation without a direct Mcoln1 direction. `No Literature` was used after target-plus-observed-gene searches found no direct relationship or specific partial bridge, even when the target had broad literature on transcription, splicing, chromatin regulation, membrane traffic, calcium transport, or neurodevelopment.

Species, cell-type, stage, and modality differences were recorded in `lit_context` but were not, by themselves, used to downgrade directionally interpretable chains. `indirect` marks pairs where the cited prior combined a target-specific perturbation with a downstream mechanism measured in another system.

## Multi-module reduction

Pairs with many DEGs were assigned using the dominant FDR-supported module, not an incidental late-ranked gene. For Psmc1 and Psmc5 this meant the proteasome, ubiquitin, chaperone, integrated-stress, or apoptotic genes within the broad response. For splicing and chromatin regulators, recurrent DEGs such as `Rsrp1`, `Srrm2`, `Amy1`, `Mapk8`, `Dmtf1`, `Snhg11`, `Peg3`, `Ttc4`, or `Fbxw5` were inspected together, but no cited target-specific relationship connected the perturbation to that observed module.

## Difficult or low-confidence pairs

Sparse pairs with only one to three DEGs were the lowest-confidence calls because a single FDR-supported gene such as `Svop`, `Lnpep`, `Idh1`, `Dpp7`, or `Rnf26` rarely maps to an experimentally documented target-to-response mechanism. They were nevertheless reviewed with exact target-plus-gene searches and were left as `No Literature` when no bridge was found.

The Hspa9 and Vps41 `Inferred` calls are also intentionally cautious: the literature documents mitochondrial or lysosomal stress after target loss, but not the exact acute brain-cell transcriptional response or its direction. No pair was marked `Disagree`; no reviewed literature gave a target-specific expectation opposite to a sufficiently powered measured central response.

## Counts

- Total eligible pairs: 213
- Emitted pair rows: 213
- Agree: 17
- Inferred: 9
- Disagree: 0
- No Literature: 187
- Incompletely reviewed pairs: 0
