# Q3 literature-direction methods

## Eligibility and emitted scope

The manifest contained 100 assigned perturbations. I filtered the screen to `gene_target in manifest` and to the 23 allowed `group_name` values, then called eligible target x cell-type pairs with this downstream-only criterion:

```python
(pvals_adj < 0.10) & (names.str.lower() != gene_target.str.lower())
```

Rows for `names == gene_target`, compared case-insensitively, were excluded before counting significant genes, so a pair with only the target transcript significant would not be eligible. This produced 518 eligible pairs, and `q3_cell_type_specificity.jsonl` emits 518 rows.

## Phenotype characterization

For each eligible pair I sorted all downstream FDR-significant rows by adjusted p value and then by absolute log fold change. The corresponding evidence row records the perturbed and control nucleus counts, the total number of downstream significant genes for that pair, and up to the first 12 measured genes with log fold changes and adjusted p values. Pair summaries name the top three genes as the concise description of the central response.

Large signatures were reduced to their dominant coherent module when one was apparent across genes and cell types. Examples were the SREBP sterol module in `Srebf2` and `Marchf6`, ER-stress chaperones in `Manf`, the integrated-stress module in `Hspa9`, `Flnb` in `Adarb1`, E2F/DNA-replication genes in `Rb1`, canonical Wnt targets in `Apc`, and gamma-actin compensation in the subset of `Actb` pairs containing `Actg1`. If a pair had a materially different leading module from the cited target-specific relationship, I did not project the flag onto it; for example, `Manf` plus `Mtor` and `Actb` plus `Flna`-only pairs were left as `No Literature`.

## Literature search and flagging

I built PubMed queries from the perturbed target, its aliases when obvious, and the leading measured genes or module terms. The focused module searches reviewed the following target-to-response result sets:

- `ACTB` with `ACTG1`, beta-actin, gamma-actin, knockout, and compensation.
- `ADARB1`/ADAR2 with `Flnb`/filamin B and RNA editing.
- `APC` with `Axin2`, `Nkd1`, beta-catenin, and Wnt target genes.
- `HSPA9`/mortalin with neuronal mitochondria, and mitochondrial stress with ATF4/CHOP/CHAC1.
- `MANF` with HSPA5/BiP, DDIT3/CHOP, and ER stress.
- `MARCHF6`/MARCH6 with SREBP, HMGCR, SQLE, and cholesterol.
- `RB1` with E2F and DNA-replication genes.
- `SREBF2`/SREBP-2 with sterol genes, HMGCR, LDLR, and SQLE promoters.

Those searches contributed the 10 cited PubMed references. For the remaining rows I searched the target with the central genes named in the evidence table and did not find a direct relationship or a biologically specific partial bridge strong enough to cite; broad disease, chromatin, spliceosome, proteasome, vesicle-trafficking, or ion-channel literature was not counted when it did not reach the measured response genes.

## Context transfer and adjacent decisions

I used `Agree` when the literature gave a target-specific expectation for the measured direction even if the species, cell type, developmental stage, or perturbation modality differed from this acute mouse neuronal CRISPR screen. Those differences were recorded in `lit_context`. I used `Inferred` when the literature reached the right target and a plausible specific mechanism but missed a decisive step: `Adarb1` reaches `Flnb` editing but not the observed `Flnb` down-regulation, and `Hspa9` reaches neuronal mitochondrial damage plus a separate mitochondrial ISR-to-ATF4/CHAC1 bridge but not this exact Hspa9 response. `No Literature` was used when target plus central measured genes did not yield a specific bridge; generic target function or shared family membership was insufficient.

## Difficult and low-confidence pairs

The largest low-confidence group is the broad chromatin and RNA-processing set, including `Setd1a`, `Kansl1`, `Trrap`, `U2af2`, `Rnpc3`, `Cdc40`, `Hnrnpu`, and `Srrm2`. These perturbations often affected hundreds of genes, but the top genes were idiosyncratic rather than a literature-documented target-specific module, so they were intentionally assigned `No Literature` unless a direct bridge was found. Single-gene pairs near FDR 0.10 were also kept if eligible but were searched and flagged conservatively.

No pair was left incompletely reviewed. Totals: 518 eligible pairs, 518 emitted pair rows, 0 incompletely reviewed pairs. Flag counts were {"Agree": 34, "Inferred": 23, "No Literature": 461}.
