# Q3 literature-direction assessment

## Eligibility

The manifest contained 500 assigned perturbations. I filtered the full parquet to those exact targets and to the 23 allowed `group_name` values, then used the downstream DEG query below:

```sql
SELECT gene_target, group_name
FROM wilcoxon_de
WHERE gene_target IN manifest.gene_targets
  AND group_name IN allowed_cell_types
  AND pvals_adj < 0.10
  AND lower(names) <> lower(gene_target)
GROUP BY gene_target, group_name
HAVING count(*) > 0;
```

This yielded 1590 eligible perturbation x cell-type pairs supported by 62165 downstream significant gene rows after exclusion of the perturbed transcript itself. The emitted table also contains 1590 rows, so no eligible pair was intentionally collapsed or dropped.

## Phenotype Characterization

For each eligible pair, I sorted downstream genes by adjusted Wilcoxon p-value with absolute log fold change as the secondary key and used the leading FDR-supported genes as the local response signature. The evidence rows report the number of significant downstream genes, up/down counts, perturbed and control nucleus counts, and up to eight leading genes with log fold changes, raw p-values, adjusted p-values, and Wilcoxon scores.

When the leading genes formed a recognizable module, the module rather than a singleton drove the literature comparison: canonical Wnt output for `Apc`; ER or integrated-stress genes for `Atp2a2`, `Elp1`, `Elp2`, and `Gfpt1`; cholesterol/lipid genes downstream of mTORC1 for `Tsc2` and `Depdc5`; Bax/Sqstm1/Ubc/Hsp90ab1 proteotoxic stress for `Psmc1` and `Psmc5`; and repeated `Flnb` loss for `Adarb1`. Pairs with only one or a few isolated downstream genes were assessed on those exact target-to-gene relationships.

## Literature Searches

PubMed was the primary source. Pair-specific queries combined the perturbed target with the leading significant genes or with the central module terms, for example `Adarb1 Flnb RNA editing`, `Apc Axin2 Nkd1 beta-catenin`, `Atp2a2 SERCA2 CHOP DDIT3`, `Tsc2 mTORC1 SREBP cholesterol`, `Depdc5 GATOR1 mTORC1`, and `proteasome Bax neuronal apoptosis`; exact target symbols were expanded to common aliases such as ADAR2, APC, SERCA2, and Elongator when needed. The first PubMed page, up to five titles and abstracts, was reviewed for target-plus-signature queries that returned hits; pairs with no exact target-to-signature hits therefore contributed zero relevant papers and stayed in `No Literature` unless a broader target-to-module query supplied a specific bridge.

For non-`No Literature` calls I inspected PubMed abstracts for the cited papers and required either a direct target-to-response relation or a specific chain that covered the observed module. `Agree` calls used literature that predicts the observed direction; `Inferred` calls used a biologically specific bridge whose direction or target specificity remained incomplete. `No Literature` calls were reserved for pair-specific searches that did not find a documented bridge from the perturbed target to the observed leading genes or module.

## Context Transfer

Species, cell type, developmental stage, and perturbation modality differences were recorded in `lit_context` and were not by themselves treated as downgrades. I used `indirect` only when the cited relationship transferred through a complex-level or pathway-level intermediate, such as `Depdc5 -> mTORC1 -> sterol genes`, `Gfpt1 -> O-GlcNAc -> eIF2alpha/CHOP`, or 26S proteasome inhibition standing in for an individual 19S ATPase perturbation.

Target mRNA knockdown was never used as a sole criterion for a null call. Eligibility and the pair summaries are based on downstream genes after excluding rows where `names` matched `gene_target` case-insensitively.

## Multi-Module and Low-Confidence Pairs

For multi-module pairs, I assigned the pair-level flag using the module with the strongest FDR support and the clearest target-specific literature bridge. If a large response also contained synaptic, apoptotic, or housekeeping changes not covered by the cited bridge, the flag was kept at `Inferred` unless the core observed module itself was directionally documented.

The lowest-confidence groups were sparse pairs with a single FDR-supported gene and large pleiotropic responses in `151 TH Prkcd Grin2c Glut`, `155 MB Glut`, or `191 MB P MY GABA` whose leading genes had no specific target-to-effect literature despite broad literature on the perturbed gene. The repeated `Adarb1`/`Flnb` and `Depdc5`/cholesterol calls are marked `Inferred` because the literature supports RNA-editing or mTORC1 intermediates but not the exact screened mRNA change.

## Totals

- Eligible pairs: 1590
- Emitted pair rows: 1590
- Evidence rows: 1590
- Reference rows: 9
- Flag counts: Agree=16, Inferred=40, Disagree=0, No Literature=1534
- Incompletely reviewed pairs: 0
