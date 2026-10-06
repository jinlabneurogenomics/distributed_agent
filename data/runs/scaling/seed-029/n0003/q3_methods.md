# Q3 methods

## Eligibility

I loaded the manifest targets `Srsf1`, `Uba5`, and `Sin3a` from `[local file: n0003.targets.json]` and filtered `[local file: wilcoxon_de_results_group_name_final_data_no_multi_guide_cells.parquet]` to those targets and the 23 allowed `group_name` values. For each measured `(gene_target, group_name)` pair, the eligibility query was:

```python
pair_rows = df[(df.gene_target == target) & (df.group_name == group)]
downstream = pair_rows[
    pair_rows.names.str.casefold().ne(pair_rows.gene_target.str.casefold())
    & (pair_rows.pvals_adj < 0.10)
]
eligible = len(downstream) > 0
```

This yielded 45 eligible downstream pairs: 23/23 measured `Srsf1` groups, 8/23 measured `Uba5` groups, and 14/21 measured `Sin3a` groups. All 45 eligible pairs are emitted exactly once in `q3_cell_type_specificity.jsonl`; no measured but downstream-ineligible pair was emitted.

## Phenotype Characterization

I first ranked FDR-significant downstream rows by adjusted P value within each eligible pair, recorded perturbed and control nucleus counts, up/down DEG counts, and the target-transcript row as an engagement caveat when present. I then counted recurrence of FDR-significant downstream genes across the eligible pairs of each target.

The recurrent `Srsf1` response was a spliceosome/RNA-processing state: `Arglu1`, `Far1`, `Psip1`, `Dazap1`, `Rbm28`, `Hnrnpm`, and `Drosha` were repeatedly increased, while `Fam193b`, `Srsf2`, and `Hnrnpdl` were repeatedly decreased. The only `Srsf1` exception was `017 CA3 CA2-FC DG Glut`, which had four isolated downstream genes (`Phf14`, `Auts2`, `Psma4`, `Itm2c`) and did not share the central RNA-processing module.

The recurrent high-confidence `Uba5` response in caudal groups combined ER/proteostasis and mitochondrial genes: `Atp6v0c`, `Syt11`, `Rtn3`, and `Srebf2` decreased, `Ndufa2` and `Atp5j2` increased, and `Ddit3` or `Sqstm1` was FDR-significant in the larger caudal responses. `054 CNU-MGE GABA` and `066 CNU-HYa HY GABA` were weaker mitochondrial/vacuolar-ATPase versions of that pattern, while `110 CNU-HYa HY MM Glut` had only a single downstream `Drosha` hit.

The recurrent `Sin3a` response was dominated by `Odf2` up-regulation together with repeated `Snhg11`, `Srrm2`, and `Tmem191` decreases and sterol/ER-associated genes including `Cyp46a1` and `Os9`. `012 MEA LA CA1 DG Glut` had only four significant genes and was searched around those pair-specific hits rather than the recurrent module.

## Literature Searches

Searches used PubMed title/abstract and broad PubMed queries. I searched each target both against its recurrent module and against pair-specific leading genes when the response was weak or atypical.

For `Srsf1`, searches included broad `SRSF1 alternative splicing`, `SRSF1 autoregulation`, and `SRSF1 knockdown RNA-seq` queries, exact searches for `SRSF1` with `Arglu1`, `Fam193b`, `Dazap1`, `Rbm28`, `Hnrnpm`, `Hnrnpdl`, `Ptbp2`, `Drosha`, and exact searches for the CA3 genes `AUTS2`, `PHF14`, `PSMA4`, and `ITM2C`. I reviewed SRSF1 autoregulatory-splicing and acute Srsf1-deficiency transcriptome papers and rejected unrelated co-occurrences where the observed gene was discussed independently of SRSF1.

For `Uba5`, searches included `UBA5 UFM1`, `UBA5 ER stress`, `UFMylation endoplasmic reticulum stress neurons`, `UBA5 mitochondria`, `UFMylation mitochondrial oxidative phosphorylation`, exact title/abstract searches for `UBA5` with `DDIT3`, `SQSTM1`, `ATP6V0C`, `SYT11`, `NDUFA2`, and `Drosha`, plus UFMylation pathway papers. I reviewed UBA5 patient-derived cortical organoid work, UFM1-deficient neuron data, zebrafish UBA5 mitochondrial data, and an ER-phagy CRISPRi paper to decide whether ER or mitochondrial responses were bridged specifically enough for `Inferred`.

For `Sin3a`, searches included `Sin3a neuron`, `SIN3A cortical neuron`, `SIN3A histone deacetylase neuron`, exact title/abstract searches for `Sin3a` with `Odf2`, `Cyp46a1`, `Snhg11`, `Srrm2`, `Tmem191`, `Os9`, `Limk1`, `Tspan17`, `Dpy19l1`, `Cdk9`, `Wsb1`, `Ing1`, `Phf1`, `Epha10`, and `Coro6`. I reviewed Sin3a cortical-development, postnatal hippocampal-deletion, hippocampal siRNA, REST/Sin3A, and BAHCC1/SIN3A-HDAC1 papers; these documented SIN3A biology but did not connect SIN3A to the central Odf2/Snhg11/Srrm2/Tmem191/Cyp46a1 response.

## Flag Rules

I assigned `Inferred` when the literature was target-specific and biologically close to the module but failed to predict the measured gene directions. This covered the recurrent `Srsf1` RNA-processing module and most `Uba5` mitochondrial/ER-stress responses. Context tags record species, cell type, stage, modality, and indirect pathway transfer; these tags were not used as independent downgrades.

I assigned `No Literature` only after a pair-specific search found no target-to-response bridge for the central observed genes. I did not use flat or increased target mRNA as a reason to call a row a null: for example, `Uba5` target mRNA had padj >= 0.115 in all eligible groups, and several `Sin3a` target rows increased, but those observations were retained only as engagement caveats in `q3_evidence.jsonl`.

No pair was assigned `Agree` or `Disagree`: no reviewed relationship supplied a decisive target-loss prediction matching or opposing the specific central modules. Isolated exact-gene precedents, such as the published `Homer1` increase after postnatal hippocampal `Sin3a` deletion, were not used to override a much larger unrelated central module.

## Difficult Rows

The lowest-confidence rows were `Srsf1` in `017 CA3 CA2-FC DG Glut`, `Uba5` in `054 CNU-MGE GABA`, `Uba5` in `066 CNU-HYa HY GABA`, `Uba5` in `110 CNU-HYa HY MM Glut`, and the weak `Sin3a` rows with fewer than 25 downstream genes. Exact searches for their leading genes did not reveal a direct bridge; the two weak mitochondrial `Uba5` rows were left as `Inferred` because UBA5-deficiency and UFMylation literature specifically link the target pathway to mitochondrial/ER homeostasis, whereas the `Drosha` singleton was assigned `No Literature`.

Eligible pairs: 45. Emitted pair rows: 45. Incompletely reviewed pairs: 0.
