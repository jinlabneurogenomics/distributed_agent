# Q3 methods

## Eligibility

The target sidecar contained 893 perturbations. I filtered the parquet to those `gene_target` values and to the 23 allowed `group_name` values, then used the exact downstream-DEG predicate:

```sql
pvals_adj < 0.10 AND lower(names) <> lower(gene_target)
```

Grouping rows passing that predicate by `(gene_target, group_name)` yielded 2324 eligible perturbation x cell-type pairs; exactly 2324 pair rows were emitted. Pairs with no downstream row satisfying that predicate, including cases where the only significant row was the perturbed target transcript, were not emitted.

## Phenotype characterization

For every eligible pair I counted all downstream FDR<0.10 genes, the number of positive and negative log-fold changes, and the matched perturbed and control nucleus counts. Evidence rows retain the top 12 downstream genes ordered by adjusted p value plus the five largest absolute-effect genes when those added information, so singleton pairs are represented by their measured singleton and broad pairs retain their leading mixed modules.

The pair summaries report the leading FDR-supported genes and a compact module label inferred from recurring marker sets for actin/filamin remodeling, proteostasis and unfolded-protein stress, ribosome/translation, mitochondrial respiration, Wnt/beta-catenin, and synaptic responses. If no marker set matched, the module was named from the leading one to three genes rather than forced into a generic pathway.

## Literature assessment

PubMed searches combined the perturbed target symbol or common protein name with the central observed genes and module terms. Sparse pairs were queried as target plus the leading one to five FDR genes; broad pairs were queried as target plus the leading genes and the recurring module terms visible in the FDR set, such as `FLNB`/actin, proteasome/unfolded-protein response, `mTORC1`/SREBP, and RNA-splicing terms. I inspected the returned titles and abstracts for 1-10 PubMed records for each cited target-module family and used only records with resolvable NCBI URLs as supporting references; broad background papers were not cited unless they connected the assigned target, its direct protein complex, or a complete downstream mechanism to the measured module.

The main adjacent decision was `Inferred` versus `No Literature`. I used `Inferred` where literature linked the target to the assayed transcript or a proximal module but the decisive expression direction was missing, indirect, pharmacologic, complex-level, or established in another tissue. I left pairs as `No Literature` when the search did not find a target-specific bridge to the named response, even if the target has extensive unrelated disease or pathway literature.

Directionally interpretable transfer across species, stage, cell type, or modality was allowed without automatic downgrading. The `indirect` context records mechanistic gaps such as proteasome-subunit loss inferred through pharmacologic proteasome inhibition, TSC/PTEN/DEPDC5 inferred through mTORC1 signaling, or ADARB1 inferred through FLNB RNA editing rather than FLNB abundance.

## Multi-module handling

When a pair had multiple downstream modules, the pair-level flag followed the most central recurring FDR-supported module rather than a late incidental hit. Broad proteasome and RNA-splicing perturbations often showed mixed synaptic, proteostasis, RNA-processing, and stress genes; those were reduced to the module with the strongest target-specific bridge and the summary still names the observed lead genes.

## Difficult pairs

Most singleton and two-hit pairs were difficult because their leading genes had no PubMed record tying that exact target loss to that exact transcript in any cell type; these low-confidence absences were kept as `No Literature` with the searched target-to-response relationship stated in each summary. ADARB1-FLNB pairs were assigned `Inferred` rather than `Agree` because ADARB1 directly edits FLNB but published mouse data did not show altered FLNB abundance after ADAR2 loss. Proteasome and mTOR pairs were also `Inferred` because the evidence transfers from pharmacologic or pathway-level perturbations to individual acute CRISPR targets.

## Totals

- Eligible pairs: 2324
- Emitted pair rows: 2324
- Incompletely reviewed pairs: 0
- Flags: {"Inferred": 115, "No Literature": 2209}
