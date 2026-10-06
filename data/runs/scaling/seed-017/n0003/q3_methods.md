# Q3 Literature Assessment Methods

## Eligibility

The screen was filtered to the exact target manifest `Psmb4`, `Tpr`, and `Ppp2r1a`. Eligibility was computed on the target-filtered parquet with this downstream-only predicate:

```python
pvals_adj < 0.10 and names.str.lower() != gene_target.str.lower()
```

A cell group was emitted only if at least one non-target gene for the manifest target passed that FDR threshold. Groups represented only by target-transcript rows were treated as ineligible, and groups absent for a target were treated as not measured/recovered rather than as biological zeroes. This yielded 52 eligible perturbation-by-cell-type pairs, and `q3_cell_type_specificity.jsonl` emits exactly 52 rows.

## Phenotype Characterization

For each eligible pair I inspected the full set of FDR-supported downstream genes, the sign of each log-fold change, the minimum adjusted p-value, and `n_pert_matched`/`n_ctrl_matched`. Pairs with hundreds to thousands of DEGs were reduced to representative central genes by combining the lowest-FDR genes with target-recurring modules: `Psmb4` was dominated by proteasome/stress compensation plus broad neuronal and synaptic down-regulation, `Tpr` by repeated nuclear-transport/RNA-processing changes, and `Ppp2r1a` by mixed `Amy1`, RNA-processing, tubulin/synaptic, immediate-early, and lipid/cholesterol components. Sparse one- to ten-gene responses were interpreted by the individual significant genes rather than by target-wide modules.

The perturbed target transcript itself was never used for eligibility and was not the sole evidence for any pair. Target mRNA behavior was also not used to call failed editing, inactivity, or a null result.

## Literature Search

Searches were target and module specific. PubMed queries combined official target symbols with representative measured genes or modules, for example `PSMB4 proteasome activity ATF3`, `Tpr nuclear pore mRNA export Ranbp6 Rnpc3`, `Ppp2r1a Stmn4 Rsrp1 Pabpn1 Kifc2`, `PPP2R1A Insig1 Sqle Dhcr24`, `PSMB4 UCHL1 Sort1 Syt7`, and `Tpr Pigm Camkk2 Arhgap5`. I used the exact sparse-pair genes for rows that otherwise risked inheriting broad target biology.

For each broad `Psmb4`, `Tpr`, or `Ppp2r1a` module I reviewed two to four PubMed-indexed papers with target-to-mechanism evidence. For sparse pairs assigned `No Literature`, exact target/gene searches either returned no records or returned only background ubiquitin-proteasome, PP2A, or nuclear-pore literature without a specific bridge to the observed transcript.

## Flagging Rules

`Agree` was reserved for a direct PSMB4-to-proteasome-dysfunction relationship that predicted the observed increase in ATF3, DDIT3/Bax/SQSTM1, ubiquitin, or proteasome recovery genes. Some `Psmb4` pairs also showed strong synaptic transcript decreases; those were disclosed as less gene-specific and were not the sole basis for an `Agree` call.

`Inferred` was used when the literature supplied a concrete but incomplete chain. TPR papers directly connect the target to tRNA export, NXF1-pathway RNA surveillance, HSF1/HSP70 export, and CRM1 trafficking, but they do not predict the signs of `Ranbp6`, `Pigm`, `Rnpc3`, or `Snhg11` expression. Ppp2r1a papers directly connect the target to excitatory synaptic/endocannabinoid physiology, PP2A literature connects phosphatase loss to c-Jun activation, and PPP2R1A work connects disrupted PP2A assembly to SREBP1-dependent lipid expression, but none is a decisive match for the recurrent `Amy1`, `Stmn4`, `Rsrp1`, `Pabpn1`, and `Kifc2` transcript modules.

`No Literature` was used only after a pair-specific search for the measured significant genes found no target-to-effect bridge. Generic facts that PSMB4 is a proteasome subunit, TPR is a nucleoporin, or PPP2R1A is a PP2A scaffold were not treated as sufficient.

## Multi-Module Rows

A single pair-level flag was assigned from the central FDR-supported response. When a broad pair contained both a literature-supported module and a materially different module, the summary names both: for example, `Psmb4` broad rows are called on the stress/proteasome arm and disclose that the synaptic decreases are less direct. Conversely, `Psmb4` rows with only isolated `Syt7`, `Pkm`/`Uchl1`/`Sort1`, or calcium-channel responses were not upgraded using target-wide proteasome knowledge.

## Difficult Or Low-Confidence Pairs

Low-confidence `Inferred` calls were concentrated in `Ppp2r1a` rows where `Jun` or `Insig1` was only one part of a larger RNA-processing response, and in `Tpr` rows where the biology of nuclear export was plausible but the exact measured genes lacked a published direction. Sparse rows for `Ppp2r1a` (`012`, `017`, `059`, `308`), `Psmb4` (`007`, `022`, `046`, `059`), and `Tpr` (`008`, `022`, `054`, `110`, `308`) were searched explicitly and assigned `No Literature`, not inferred from an omitted search.

Total eligible pairs: 52. Emitted pair rows: 52. Incompletely reviewed pairs: 0.
