# Q3 Literature Specificity Methods

## Eligibility

The target scope was read from `[local file: n0100.targets.json]` and kept fixed at all 100 manifest perturbations. I queried `[local file: wilcoxon_de_results_group_name_final_data_no_multi_guide_cells.parquet]` for manifest targets and marked a perturbation x cell-group pair eligible only when at least one downstream row satisfied `pvals_adj < 0.10` after excluding the perturbed transcript with `lower(names) != lower(gene_target)`. This yielded 528 eligible pairs; 116 measured pairs with only a significant target-transcript row were excluded.

## Phenotype Characterization

For each eligible pair I counted all downstream FDR-significant genes, split them by positive and negative `logfoldchanges`, recorded the minimum adjusted P value and the largest absolute log fold change, and retained the matched perturbed/control nucleus counts. The evidence rows report the highest-ranked downstream genes by adjusted P value, with high-amplitude FDR genes retained as secondary context when they differed from the top Wilcoxon ranks. I treated the target transcript, when present, only as an engagement caveat in the evidence statistics; no target transcript was used to make a pair eligible.

## Literature Search

Searches were built from the perturbed gene plus the leading FDR genes or the coherent module those genes represented, for example `Adarb1 Flnb filamin B RNA editing`, `Clock Dbp Nr1d2 Tef`, `Srebf2 Dhcr24 Cyp51 Hmgcr Ldlr`, and `Depdc5 GATOR1 mTORC1 Ldlr`. PubMed was the primary source, using title/abstract hits with canonical PubMed URLs; support papers were required to document a target-to-effect or target-to-mechanism bridge rather than only general disease association, family membership, or broad transcriptional disruption.

## Flagging Rules

`Agree` was reserved for modules with a directionally interpretable prior. Clock pairs were called `Agree` because CLOCK/BMAL1 is an activator of clock-output transcripts and the screen showed reduced `Dbp`, `Nr1d2`, `Tef`, or `Per3`; Srebf2 pairs were called `Agree` because SREBP2 activates sterol-biosynthetic and cholesterol-uptake genes and the screen showed reduced `Dhcr24`, `Cyp51`, `Hmgcs1`, `Hmgcr`, `Insig1`, or `Ldlr`.

`Inferred` was used when the literature reached the right biology but not a decisive direction for the snRNA-seq response. ADARB1 was connected to `Flnb`/`Flna` by RNA editing rather than filamin mRNA abundance, ACTB was connected to ACTG1 compensation and filamin-related actin mechanics without a direct neuronal `Flna` induction prior, DEPDC5 was connected to GATOR1/mTORC1 with only an indirect route to the `Pik3r`/`Ldlr` response, and two Tsc2 pairs had an indirect mTORC1-to-lipid-transcript bridge.

`No Literature` was assigned when the pair-level target plus leading-gene/module search did not find a biologically specific bridge. Many of these pairs involved chromatin regulators, nuclear transport, proteasome biogenesis, or spliceosome factors with abundant general literature but no paper connecting the assigned target to the exact leading genes in the recovered cell group.

## Multi-Module Pairs

For dense responses, the pair flag follows the central FDR-supported module visible among the lowest adjusted P values rather than isolated high-logFC tail genes. When the lowest-ranked genes and the largest-effect genes differed, both were retained in `statistics.top_genes`; no high-effect incidental gene was used to override a more coherent leading module.

## Difficult Pairs

The hardest calls were broad regulators such as `Psmb4`, `Ppp2r1a`, `Tpr`, `Prpf6`, `Yy1`, `Zbtb7a`, and `Wac`, where the screen recovered hundreds to thousands of downstream genes in some thalamic or midbrain groups but the top genes did not form a documented target-specific module. Those pairs were still reviewed at the pair level and emitted; none were left incomplete or relabeled as `No Literature` because of an omitted search.

## Totals

Total eligible pairs: 528. Emitted pair rows: 528. Emitted evidence rows: 528. Emitted cited references: 8. Flag counts: {"Agree": 13, "Inferred": 33, "No Literature": 482}. Incompletely reviewed pairs: 0.
