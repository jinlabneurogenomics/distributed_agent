# Q3 literature assessment methods

## Eligibility

The target manifest contained 500 assigned perturbations. I filtered the full Wilcoxon parquet to rows whose `gene_target` was in that manifest, then defined eligible perturbation by cell-type pairs as pairs with at least one row satisfying `pvals_adj < 0.10` after excluding the perturbed transcript itself with `lower(names) != lower(gene_target)`. This yielded 1602 eligible pairs, all of which are emitted in `q3_cell_type_specificity.jsonl`.

## Phenotype characterization

The parquet contains Scanpy Wilcoxon rankings for each recovered `(gene_target, group_name)` block. I scanned all row groups for FDR-significant non-target genes and retained `names`, `logfoldchanges`, `pvals`, `pvals_adj`, and matched perturbed/control cell counts. For each pair I used the lowest-FDR downstream rows as compact evidence and, for literature-supported programs, forced the relevant module genes into the evidence row: `Dbp`/`Nr1d1`/`Nr1d2` for `Bmal1`, Wnt feedback genes for `Apc`, sterol-biosynthesis genes for `Tsc2`, proteotoxic or unfolded-protein-response genes for `Pomp`/`Psmb4`, and ER-stress genes for `Atp2a2`.

## Literature search

I searched PubMed with pair-specific target and response terms before assigning literature-backed flags. Queries combined the perturbed target or a standard alias with the observed module genes and mechanism terms, including `Bmal1 Dbp circadian`, `APC AXIN2 RNA interference beta-catenin transcription`, `mTORC1 SREBP cholesterol biosynthesis`, `POMP proteasome maturation unfolded protein response`, `proteasome inhibition ATF4 CHOP unfolded protein response`, and `thapsigargin ATF4 CHOP unfolded protein response`. Sparse pairs whose strongest significant genes did not match one of those coherent modules were searched as target-to-gene relationships; a pair was left as `No Literature` only when no target-specific direct or partial bridge to its leading downstream genes was identified.

## Flagging rules

`Agree` was reserved for a documented target-specific relationship that predicted the observed direction: BMAL1/CLOCK activation of circadian output genes, APC repression of beta-catenin feedback transcription, TSC2 repression of mTORC1/SREBP sterol transcription, and POMP loss causing proteasome insufficiency and CHOP/UPR stress. `Inferred` was used when the bridge was specific but incomplete: PSMB4 was inferred through pharmacologic proteasome inhibition, and ATP2A2 was inferred through pan-SERCA thapsigargin-induced ER stress. I used `cell_type`, `stage`, `modality`, and `indirect` context tags to record species, cell-model, developmental, perturbation, or mechanistic-chain differences without downgrading a relationship that still predicted the measured direction.

## Multi-module reduction

For broad responses I assigned the pair-level flag from the dominant interpretable module rather than isolated marker genes. For example, `Tsc2` pairs with `Cyp51`, `Msmo1`, `Insig1`, `Fdft1`, or related sterol genes were judged on the mTORC1/SREBP program even when a few neuronal identity genes were also significant; `Psmb4` and `Pomp` pairs were judged on proteotoxic or UPR genes only when those genes were present among the FDR-supported response.

## Difficult pairs and coverage

Most eligible pairs were low-information responses: 1026 of 1602 pairs had five or fewer significant downstream genes. These were difficult because an isolated shift in genes such as `Snhg11`, `Rsrp1`, `Leng8`, or single neuronal markers usually did not have a documented target-to-effect bridge even for well-studied chromatin or RNA-processing targets. The outputs therefore use `No Literature` for the long tail rather than treating broad target annotations, disease associations, or complex membership as pair-level evidence.

Eligible pairs: 1602

Emitted pairs: 1602

Incompletely reviewed pairs: 0

Flag counts: {'Agree': 19, 'Inferred': 16, 'No Literature': 1567}
