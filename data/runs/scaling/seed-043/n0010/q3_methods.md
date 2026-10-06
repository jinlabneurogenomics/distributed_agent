# Q3 methods

## Eligibility

The target manifest was read from `[local file: n0010.targets.json]` and was used without replacement or expansion: `Psmc1, Psmc5, U2af2, Naa20, Hnrnpu, Rnpc3, Setd1a, Cdc40, Kansl1, Hspa9`. The parquet at `[local file: wilcoxon_de_results_group_name_final_data_no_multi_guide_cells.parquet]` was filtered to those ten `gene_target` values and to the 23 allowed `group_name` values.

A perturbation/cell-type pair was eligible when at least one row satisfied:

```text
gene_target in manifest AND
group_name in allowed_cell_groups AND
lower(names) != lower(gene_target) AND
pvals_adj < 0.10
```

Rows for the perturbed transcript itself were excluded before counting significant downstream genes. This produced 131 eligible pairs: Psmc1 16, Psmc5 13, U2af2 13, Naa20 17, Hnrnpu 18, Rnpc3 18, Setd1a 11, Cdc40 5, Kansl1 10, and Hspa9 10. `q3_cell_type_specificity.jsonl` emits the same 131 pairs and no ineligible target/cell-type pairs.

## Phenotype Characterization

For every eligible pair I first sorted downstream FDR<0.10 genes by adjusted p-value and by absolute log fold change, recorded `n_pert_matched` and `n_ctrl_matched`, and then inspected both the top genes within each pair and recurrence across cell types of the same perturbation. Recurrent genes were used to recognize coherent modules: proteasome/UPS and ISR genes for Psmc1 and Psmc5; ATF4/UPRmt amino-acid stress genes for Hspa9; spliceosome and SR-protein genes for U2af2, Cdc40, and parts of Hnrnpu; RNPC3-associated minor-spliceosome expression changes for Rnpc3; nuclear mitochondrial/OXPHOS genes for Setd1a; and repeated but literature-orphan modules around Snhg11/Peg3/Kifc2 for Naa20 and Ttc4/Ccdc39/Commd4/Nsmce2 for Kansl1. The evidence rows report the top FDR genes plus module genes when the top rank alone would have missed the central response.

## Literature Search

Searches used PubMed queries combining each perturbation with the observed central genes and the module name, for example `HSPA9 AND DDIT3/CHAC1/UPRmt`, `PSMC1 OR PSMC5 AND NFE2L1/ZFAND2A/UBC`, `RNPC3 AND minor spliceosome`, `U2AF2 AND exon inclusion`, `CDC40 AND intron retention`, and `SETD1A AND mitochondrial`. For candidate `No Literature` calls I ran exact co-mention searches against the observed orphan modules, including `HSPA9 SDC3`, `HSPA9 ALDH1L2 NCL KIFC2`, `NAA20 Snhg11 Peg3 Kifc2 Cyp46a1 Flnb`, `KANSL1 CCDC39 TTC4 COMMD4 NSMCE2 VTI1A STX8`, `HNRNPU DMTF1 RSRP1 ATXN2L AHI1 GPR180`, `U2AF2 KIFAP3 UBR4 RSRP1`, `CDC40 PDE4A ANAPC1 RACK1 SRSF6`, `PSMC1 Pafah1b2 Ahi1 Nbdy`, `PSMC1 RNPC3`, `PSMC5 EPM2AIP1`, `PSMC5 LRFN5 SEC23A PPP3CB FAM32A FKBP2`, and `SETD1A LETM2`. I reviewed at least two to five returned records for the mechanistic groups and at least the returned abstracts, or confirmed zero PubMed hits, for exact orphan-module searches; no pair was assigned `No Literature` because of an omitted search.

## Flag Rules

`Agree` was used when target loss predicted the measured module direction through a direct or complete mechanistic relationship. This applied to Psmc1/Psmc5 pairs with PSM, Ubc, Zfand2a/Zfand5, chaperone, or apoptotic proteasome-stress induction; Hspa9 pairs with Chac1, Ddit3, Lonp1, Herpud1, Slc7a5/Slc7a1, Shmt2, Asns, or aminoacyl-tRNA synthetase induction; and Setd1a pairs with a coordinated decrease of nuclear mitochondrial genes.

`Inferred` was used when the literature bridge was real but the measured assay could not test the decisive event or contained only a fragment of the expected module. U2af2, Rnpc3, and Cdc40 primarily fall here because published perturbations alter exon inclusion or intron retention, whereas the screen reports total gene-level counts. Sparse proteasome or mitochondrial pairs with only one expected gene were also kept as `Inferred` rather than forced to `Agree`.

`No Literature` was used for exact orphan responses after target/module co-mention searches found no target-to-effect bridge. General target biology was not counted: NatB/NAA20 effects on alpha-synuclein or generic proteostasis did not explain Snhg11/Peg3/Kifc2 down-regulation, HNRNPU neurodevelopmental and splicing papers did not explain Dmtf1/Gpr180/Ahi1 changes, and KANSL1/NSL chromatin literature did not explain the repeated Ttc4/Ccdc39/Commd4/Nsmce2 vesicle-like signature. No `Disagree` call was made because no eligible pair had a target-specific directional expectation that the gene-level result contradicted with enough engagement and module support to resolve a conflict.

## Multi-Module and Difficult Pairs

When a pair had multiple FDR-supported modules, the flag follows the dominant recurrent module rather than a single largest log-fold-change gene. The summary names the supported module and, for sparse pairs, states when additional genes were not covered by the literature relationship. Difficult pairs were the target/cell-type combinations with one or two FDR genes, and large Naa20, Hnrnpu, and Kansl1 responses whose modules were highly recurrent in the screen but not described in target-specific literature. These were reviewed with exact co-mention searches and retained as `No Literature` when no partial bridge was found.

## Review Counts

Total eligible pairs: 131. Emitted pair rows: 131. Incompletely reviewed pairs: 0. Flag counts were Agree 34, Inferred 40, No Literature 57, and Disagree 0.
