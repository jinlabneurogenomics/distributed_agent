# Q3 Literature Classification Methods

## Eligibility

The sidecar manifest assigned one perturbation, `Psmc1`. I filtered the parquet to `gene_target == "Psmc1"` and to the 23 allowed `group_name` values, then evaluated eligibility after removing the perturbed transcript with a case-insensitive target comparison:

```sql
gene_target IN manifest
AND group_name IN allowed_cell_groups
AND pvals_adj < 0.10
AND lower(names) <> lower(gene_target)
```

A `(gene_target, group_name)` pair was emitted when at least one row passed that downstream-DEG predicate. `Psmc1` was measured in 21 allowed groups; 16 groups had at least one significant non-target gene and are present in `q3_cell_type_specificity.jsonl`. Five measured groups had zero downstream hits after the target exclusion (`007 L2-3 IT CTX Glut`, `009 L2-3 IT PIR AON ENT Glut`, `017 CA3 CA2-FC DG Glut`, `022 L5 ET CTX Glut`, `053 Sst Gaba`), and two allowed groups had no `Psmc1` rows.

## Phenotype Summaries

For each eligible pair, I read the actual significant downstream rows and selected evidence genes from the top FDR-ranked changes plus genes that represented coherent modules recurring across eligible groups:

- proteasome and ubiquitin-system induction, for example `Psmc3`, `Psmc4`, `Psmc6`, `Psmd1`, `Psmd3`, `Psmd9`, `Psme4`, `Ubc`, `Uchl1`, and `Usp5`
- heat-shock and proteotoxic-stress induction, for example `Hspa1a`, `Hspa1b`, `Hsp90aa1`, `Hsp90ab1`, `Hsph1`, `Dnajb1`, `Dnajb4`, and `Dnajb9`
- ER-stress, apoptotic, and p53-associated induction, for example `Ddit3`, `Bax`, `Mdm2`, `Ccng1`, and `Aen`
- neuronal or synaptic transcript decreases, for example `Dnm1`, `Syp`, `Vamp1`, `Sv2a`, `Slc17a6`, `Slc17a7`, `Camk2a`, `Camk2b`, `Atp1a3`, `Atp1b1`, `Scn1a`, and `Gria2`

Pairs with several modules were assigned on the most target-specific, FDR-supported module. Thus, pairs with proteasome-subunit and HSP/UPR/apoptotic induction were called on that induced stress module, with synaptic decreases recorded as accompanying effects. Sparse pairs were not forced into that model unless proteasome-subunit or stress markers were themselves significant.

## Literature Search And Flag Rules

The primary searches used PubMed with queries for exact `Psmc1`/`Rpt2` neuronal deletion, `Psmc1` conditional knockout in mouse brain, Nrf1 proteasome bounce-back, and HSP/UPR/apoptotic responses to proteasome inhibition. Those searches identified a target-specific neuronal Psmc1 conditional-knockout paper, a mechanistic Nrf1 bounce-back paper, and proteasome-inhibition papers documenting HSP70/UPR and `DDIT3`/`BAX` induction.

For sparse or discordant modules, I ran pair-specific PubMed queries combining `Psmc1` or `Rpt2` with the observed central genes:

- `Ahi1`, `Pafah1b2`, and `Nbdy` for `005 L4-5 IT CTX Glut`
- `Hgs`, `Ubc`, `Uchl1`, `BC005537`, and `Syt7` for `027 NP-CT-L6b-OB Glut`
- `Rnpc3` for `059 CNU-LGE LSX GABA`

Shared ubiquitin-proteasome pathway membership without a specific Psmc1-to-response mechanism was not considered sufficient for `Agree` or `Inferred`. Species, cell-type, and perturbation differences were recorded in `lit_context` but did not downgrade a directional, mechanistically connected expectation. `indirect` was reserved for the CTX-CGE GABA call, where the literature documents the Psmc1-to-neuronal-injury relationship but does not resolve how that injury maps onto the exact mixed CTX-CGE transcript module.

No pair was assigned `Disagree`: none had a target-specific directional expectation that conflicted with an adequately measured dataset result. Pairs assigned `No Literature` were searched to the pair level and left uncited because the searches found either no Psmc1/Rpt2 hit or only broad UPS/pathway context that did not connect the target to the observed genes.

## Difficult Pairs And Review Completeness

The difficult low-information pairs were `005 L4-5 IT CTX Glut`, `027 NP-CT-L6b-OB Glut`, and `059 CNU-LGE LSX GABA`; all lacked the canonical proteasome-subunit/HSP/UPR module and were assigned `No Literature` only after the exact observed genes were searched with `Psmc1`/`Rpt2`. `046 CTX-CGE GABA` had 131 significant genes but little FDR-supported canonical HSP or proteasome-subunit induction, so it was kept at `Inferred` on the Psmc1 neuronal-injury prior rather than upgraded to `Agree`.

Weak or increased `Psmc1` mRNA was treated only as an engagement caveat. The target transcript itself was never used to make a pair eligible and was not used as sole evidence for agreement or null behavior.

Total eligible pairs: 16. Total emitted pair rows: 16. Incompletely reviewed pairs: 0.
