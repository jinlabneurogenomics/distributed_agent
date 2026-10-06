# Q3 methods

## Eligibility

I used the manifest at `[local file: n0100.targets.json]` as the complete perturbation scope and filtered the full Wilcoxon table to those 100 targets and the 23 allowed `group_name` values. The downstream-DEG eligibility query was:

```text
gene_target in manifest.gene_targets
and group_name in allowed_cell_groups
and pvals_adj < 0.10
and lower(names) != lower(gene_target)
```

A `(gene_target, group_name)` group was eligible when at least one row remained after that target-transcript exclusion. This yielded **529 eligible pairs**, and `q3_cell_type_specificity.jsonl` emits **529 pairs** exactly once. Rows matching `lower(names) == lower(gene_target)` were retained only to annotate target-mRNA caveats in `q3_evidence.jsonl`; they were not counted as downstream support.

## Phenotype Characterization

For each eligible pair I sorted downstream FDR-significant genes by absolute log fold change with adjusted P value as a tie breaker. The evidence row records the number of downstream FDR hits, matched perturbed and control nucleus counts, the strongest downstream genes with log fold changes and adjusted P values, and the target transcript when it was available in the rank table.

Module calls were made from the strongest repeated genes in that pair, with recurrence across cell groups used only as screen-wide context. Clear modules included MANF/ATP2A2/HSPA5 ER-stress and UPR markers, APC/LRP6 Wnt targets, a TSC1 sterol/SREBP module, ACTB actin-remodeling genes, MYT1L developmental-state genes, NF1 Ras/activity-associated genes, and UBA5 proteostasis-associated stress programs. Pairs with one or a few isolated genes were still emitted if they passed FDR, but were not assigned a positive literature flag unless a target-specific bridge to those genes or to the local module was found.

## Literature Review

Searches were constructed per pair from the perturbed gene and the observed top downstream genes or module terms, for example `MANF Hspa5 Hyou1 Pdia6 unfolded protein response`, `ATP2A2 SERCA2 endoplasmic reticulum stress Chac1 Ddit3`, `Apc Axin2 Nkd1 beta-catenin Wnt`, and `TSC1 SREBP mTORC1 cholesterol`. Searches prioritized PubMed and PubMed Central records; titles and abstracts were inspected for a relationship that connected the target to the measured response rather than merely to a general disease or pathway.

For `Agree`, I required a directionally interpretable target-to-effect relationship or a complete cited mechanism whose expected sign matched the data, while allowing differences in species, cell type, age, and perturbation modality to appear as `lit_context` annotations. `Inferred` was used when the literature gave a biologically specific bridge but not a complete sign prediction for the observed genes, as with ACTB compensation outside neurons, MYT1L developmental repression that did not nominate the measured Rreb1/Yap1 module, NF1 as a neuronal RasGAP without a documented Vgf/Egr1 module, and UBA5/UFMylation disruption of ER homeostasis without a documented H1f4/mitochondrial transcript signature. `No Literature` was used when target-plus-response searches found only unrelated target biology, only broad pathway membership, or no inspected paper connecting the manifest target to the observed genes.

## Reducing Multi-Module Pairs

Each row receives one pair-level flag based on the dominant FDR-supported module in its evidence row. When a pair had a recognized module plus scattered singleton genes, the flag follows the recognized module and the summary names the genes that drove that choice. When several unrelated genes passed FDR without a target-specific module, the pair was left as `No Literature` even if the target itself has extensive background literature.

## Difficult Pairs

The hardest calls were the high-DEG RNA-processing and chromatin-regulator perturbations, especially `Srsf1`, `Thap11`, `Thoc1`, `Tnpo3`, `Wdr26`, `Cdk13`, `Wac`, `Trrap`, and `Sin3a`. They produced reproducible transcript sets in this screen, but searches for the actual central genes, such as `Ttc41`/`Thoc6`/`Acp6` for `Thap11` and `Ogt`/`Eif4a2`/`Cpt1c` for `Zfp236`, did not identify target-specific bridges strong enough for `Inferred`.

I assigned low-confidence `Inferred` rather than `Agree` to broad but plausible mechanistic transfers where the direction of the actual module was not directly documented. No eligible pair was intentionally left unreviewed; total eligible pairs = **529**, emitted pairs = **529**, and incompletely reviewed pairs = **0**.
