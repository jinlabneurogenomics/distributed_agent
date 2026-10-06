# Q3 Cell-Type Specificity Methods

## Eligibility

I loaded `[local file: n0893.targets.json]` and used all 893 manifest entries as the only primary target scope. The exact downstream eligibility predicate was:

```text
gene_target in manifest gene_targets
and group_name in the 23 allowed cell groups
and pvals_adj < 0.10
and lower(names) != lower(gene_target)
```

The parquet screen contained 136,665 FDR<0.10 rows for those targets before target-transcript exclusion and 135,055 downstream rows after exclusion. Grouping the downstream rows by `(gene_target, group_name)` yielded 2324 eligible pairs; 2324 rows were emitted in `q3_cell_type_specificity.jsonl`, and no cell group without a downstream FDR<0.10 row was emitted.

## Phenotype Characterization

For each eligible pair I sorted significant downstream genes by absolute Wilcoxon score, preserving the signed `logfoldchanges`, adjusted p-values, and matched perturbed/control nucleus counts. The evidence record for each pair reports the number of downstream FDR<0.10 genes, the up/down split, the matched cell counts, and either the top absolute-score genes or the literature-matched marker genes followed by the top residual genes.

Response modules were selected from recurrent FDR-supported genes rather than from a single incidental marker. The curated modules that were recognized before flagging were canonical Wnt targets for `Apc`, ER/unfolded-protein-response genes for `Atp2a2`, `Gfpt1`, `Elp1`, and `Elp2`, THAP11 mitochondrial/Parkin targets, sterol and lysosomal genes for `Tsc1` and `Tsc2`, `Atp6v0a1` recurrence after `Atp6v0c` perturbation, and a lysosomal/TFEB-like response after `Rab7` perturbation. Remaining singleton or idiosyncratic multi-gene responses were kept as their observed lead genes and were not forced into a pathway label.

## Literature Search

I queried PubMed through the filtered literature gateway. For repeated target-module patterns I searched the target with the mechanism and marker genes once, then reused the same inspected papers across cell types only when the pair contained the relevant FDR genes. Examples of successful query patterns were `APC Axin2 Nkd1 Wnt`, `SERCA2 CHOP endoplasmic reticulum stress`, `GFPT1 unfolded protein response`, `THAP11 mitochondrial gene expression`, `THAP11 PARKIN`, `TSC1/TSC2 mTORC1 neuron`, `mTORC1 SREBP cholesterol biosynthesis genes`, `mTORC1 lysosome biogenesis TFEB TSC1`, `Atp6v0c lysosome autophagy neurons v-ATPase`, and `RAB7 TFEB lysosomal gene expression`. Pair-specific No Literature calls used the manifest target plus the top FDR genes or the apparent response class as search terms; broad target reviews, disease associations, and shared pathway membership were not counted as support unless they supplied a bridge to the measured genes or module.

## Flagging Rules

`Agree` was reserved for a target-specific relationship or complete mechanistic chain with a signed prediction matching the screen: Apc loss to increased beta-catenin targets, Atp2a2/Gfpt1/Elp1 loss to increased unfolded-protein-response transcripts, Thap11 loss to increased Prkn or decreased mitochondrial genes, and Tsc1/Tsc2 loss to increased mTORC1-linked sterol or TFEB/lysosomal genes. `Inferred` was used for biologically specific but incomplete transfers, namely Elp2 by transfer from the ELP1/Elongator UPR literature, Atp6v0c by V-ATPase/TFEB pathway evidence that does not predict Atp6v0a1 direction in neurons, Rab7 by an indirect RAB7A-effector-to-TFEB bridge, and Thap11 pairs whose evidence was mitochondrial but lacked either Prkn or Ndufa3.

Context labels record transportability gaps without changing the flag when the signed chain was complete. I used `cell_type` and `stage` for papers in developing retina, medulloblastoma, skeletal muscle, cardiomyocytes, developing cortical neurons, Drosophila discs, or kidney/tumor systems; `species` when the strongest citation was human or fly rather than mouse; `modality` for germline, conditional, cell-line, or disease-genetic studies instead of acute AAV CRISPR; and `indirect` for complex-level or effector-level bridges.

## Multi-Module and Difficult Pairs

Pairs containing several response modules were reduced to one pair-level flag by prioritizing the module with a target-specific signed relationship among the highest-ranked FDR genes. For example, Tsc1/Tsc2 pairs with both sterol and lysosomal transcripts were evaluated as the shared mTORC1/TFEB response, while unrelated neuronal genes in the same pair were disclosed only in the evidence top-gene list. Where a cell group for the same target had only an unrelated singleton or no matched module genes, it was independently assigned No Literature.

The lowest-confidence calls are the `Inferred` rows for Elp2, Atp6v0c, Rab7, and mitochondrial-only Thap11 responses because their support is complex-level, effector-level, or cross-species and does not document the exact signed transcript set in postmitotic mouse neurons. No pair was left incompletely reviewed; difficult pairs that lacked a specific target-to-response bridge after pair-specific PubMed/PMC searches were assigned No Literature rather than being promoted by general target biology.

## Totals

- Eligible pairs: 2324
- Emitted pair rows: 2324
- Evidence rows: 2324
- Reference rows cited: 11
- Flags: Agree=47, Disagree=0, Inferred=20, No Literature=2257
- Incompletely reviewed pairs: 0
