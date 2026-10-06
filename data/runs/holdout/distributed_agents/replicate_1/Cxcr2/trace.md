# Reasoning trace

## Question and endpoint

I interpreted the task as a scalar held-out prediction for one mouse perturbation, `Cxcr2`, in the `151 TH Prkcd Grin2c Glut` neuronal class. The requested endpoint is exactly the number of measured genes with Benjamini-Hochberg adjusted Wilcoxon p-value below 0.05 in that focal class after sparse postnatal AAV-CRISPR loss of the target. `Cxcr2` itself was held out: it was not present in the focal training-count CSV and was not present as a supplied `gene_target` in the Parquet input.

Important ambiguity resolved: the DEG count is a screen-specific response-breadth readout among recovered, NeuN-positive, class-assigned nuclei. It is not a count of all biological effects of `Cxcr2`, not a viability endpoint, and not a readout of immune-cell or oligodendrocyte responses that would have been excluded or heavily under-sampled by the NeuN-positive neuron design.

## Sources

- Declared focal training counts: `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared DE surface: `training differential-expression dataset`.
- Requested target manifest: `single-target request for Cxcr2`.
- Run-local dataset portrait, task bindings, coverage summary, capability manifest, and measurement registry in `codex_runtime/pipeline/`.
- Same-experiment July Findings ledger, version `perturbai-july-260713-sourceguard-1773-v1`, used only for training perturbations such as `Ccr2`, `Cx3cr1`, and `Cxcr4`; these records package interpretation of the same Perturb-seq experiment and are not independent replication.
- External literature from PubMed for CXCR2 biology: Padovani-Claudio et al. 2006, DOI `10.1002/glia.20383`; Eash et al. 2010, DOI `10.1172/JCI41649`; Liu et al. 2010, DOI `10.1038/nn.2491`; Liu et al. 2010, DOI `10.1523/JNEUROSCI.1238-10.2010`; Liu et al. 2015, DOI `10.1212/NXI.0000000000000174`.

## Quantitative calibration from the supplied training counts

The focal training table had 1,674 unique non-held-out perturbations. It was sparse and highly right-skewed:

- 1,205 of 1,674 perturbations had `n_degs = 0`.
- 1,481 of 1,674 had `n_degs <= 1`.
- The median was 0, the 75th percentile was 1, the 90th percentile was 2, the 95th percentile was 18, and the maximum was 2,677.

Thus zero is the empirical majority outcome in this focal cell group, and assigning a nonzero count needs target-specific evidence for a transcriptional response in recovered thalamic glutamatergic neurons.

For focal-cell training analogs, I selected represented perturbations that are mechanistically close to a chemokine receptor or to a chemokine-induced inflammatory cascade and then queried their focal DE rows directly:

```sql
SELECT gene_target,
       COUNT(*) FILTER (WHERE pvals_adj < 0.05) AS fdr05,
       MIN(pvals_adj) AS min_fdr,
       SUM(pvals_adj < 0.1) AS fdr10,
       MAX(n_pert_matched) AS n_pert,
       MAX(n_ctrl_matched) AS n_ctrl
FROM read_parquet(...)
WHERE group_name = '151 TH Prkcd Grin2c Glut'
  AND gene_target IN (...)
GROUP BY gene_target;
```

The focal analog results were:

| training perturbation | why it is relevant to `Cxcr2` | focal `n_degs` | focal expression-pattern evidence |
| --- | --- | ---: | --- |
| `Ccr2` | chemokine GPCR, inflammatory leukocyte receptor; not the same ligand class but the closest visible CC-chemokine receptor comparator | 0 | 170 perturbed versus 23,679 control nuclei; no measured gene with adjusted p < 0.05 or < 0.10; minimum adjusted p = 1.0 in the focal group |
| `Cxcr4` | CXC chemokine GPCR with strong CXCL12-dependent CNS developmental biology | 0 | 191 perturbed versus 23,679 controls; the only focal near-hit was `Pum1`, logFC 0.446, adjusted p = 0.067, so the count is zero at the requested 0.05 threshold |
| `Cx3cr1` | fractalkine GPCR for a CNS neuroimmune ligand-receptor axis, mostly on microglia | 0 | 258 perturbed versus 23,679 controls; no focal gene with adjusted p < 0.10; minimum adjusted p = 1.0 |
| `Il1rap`, `Il6ra`, `Il6st` | cytokine receptors or co-receptors that would be plausible inflammatory response conduits | 0, 0, 0 | no focal gene with adjusted p < 0.10; minimum adjusted p = 1.0 for each |
| `Tlr2`, `Tlr3`, `Tlr4` | innate-immune receptor comparators | 0, 0, 0 | no focal gene with adjusted p < 0.10; minimum adjusted p = 1.0 for each |
| `Nfkb1`, `Rel`, `Stat3` | transcriptional mediators downstream of inflammatory receptors | 0, 0, 0 | `Nfkb1` and `Stat3` had minimum adjusted p = 1.0; `Rel` had a single weak `Ptcd3` row at adjusted p = 0.140 |

The focal table also contained only three chemokine-receptor targets, all zero: `Ccr2`, `Cx3cr1`, and `Cxcr4`. Direct ligand or paired-receptor tests that would have been especially close to `Cxcr2`, such as `Cxcl1`, `Cxcl2`, and `Ackr1`, were not present as training perturbations, so the comparison is through receptor-class and inflammatory-pathway analogs rather than an exact receptor-ligand module.

## Same-experiment corpus evidence from visible analogs

The July same-experiment Findings ledger strengthened the interpretation that the chemokine-receptor zeros were true neuronal nulls rather than focal-cell near misses.

- `Ccr2:F001` reported a pan-neuronal downstream null: across 22 recovered neuronal groups there were 0 downstream genes at FDR < 0.10, with minimum downstream FDR 0.227 after excluding the `Ccr2` self row. `Ccr2:F003` compared represented chemokine-receptor relatives and found no phenocopy by `Cx3cr1` or `Cxcr4`.
- `Cx3cr1:F001` reported 0 downstream FDR < 0.10 genes across all 23 recovered neuronal groups. `Cx3cr1:F003` emphasized that other visible neuroimmune GPCR and cytokine-associated perturbations, including `Ccr2` and `Il10ra`, were also mostly flat in NeuN-positive neurons.
- `Cxcr4:F003` placed `Cxcr4` near a global transcriptional null, with absolute full-vector Pearson correlations below 0.027 to its strongest signed-score neighbors. `Cxcr4:F004` showed that `Ccr2`, `Rac1`, and `Tiam1` did not recover a generic chemokine/Rac-arm program; in the focal group the `Pum1` singleton did not pass the 0.05 endpoint used in this task.

These internal corpus records are same-experiment interpretation, so I used them as structured summaries of the visible training perturbations, not as external validation.

## External biology and causal transfer to `Cxcr2`

`Cxcr2` encodes a chemokine GPCR for ELR-positive CXC chemokines such as CXCL1 and CXCL2. The strongest mouse phenotypes in the literature are not cell-autonomous transcriptional programs in postmitotic glutamatergic neurons:

- Eash et al. 2010 showed that CXCR2 and CXCR4 antagonistically regulate neutrophil release from bone marrow through ELR-positive chemokines in endothelial and osteoblast niches.
- Liu et al. 2010, DOI `10.1038/nn.2491`, found that CXCR2-positive neutrophils were important for cuprizone-induced demyelination.
- Padovani-Claudio et al. 2006 and Liu et al. 2010, DOI `10.1523/JNEUROSCI.1238-10.2010`, placed CNS CXCR2 function in the oligodendrocyte lineage and myelin repair. Liu et al. 2015 used inducible oligodendrocyte-lineage `Cxcr2` deletion and also observed enhanced repair after demyelination.

The causal chain for the requested experiment is therefore weak at the first two transfer steps:

1. **Intervention:** AAV-CRISPR loss of `Cxcr2` is delivered sparsely after P16 in NeuN-positive neuronal populations.
2. **Direct molecular consequence:** productive CXCR2 signaling normally needs receptor expression and local CXCL1/CXCL2-like ligands. The best-established receptor-positive compartments are neutrophils and oligodendrocyte-lineage cells, not basal postmitotic thalamic glutamatergic neurons.
3. **Propagation:** visible chemokine GPCRs and immune receptors in the same neuronal screen were silent; there is no evidence that `Cxcr2` loss would route into a recurrent NF-kappaB, JAK/STAT, Rac, or RNA-state module in `151 TH Prkcd Grin2c Glut`.
4. **Exposure and selection:** the assay used healthy juvenile-to-young-adult brain without cuprizone, EAE, bacterial abscess, or other ligand-rich inflammatory challenge. NeuN enrichment would also discard the neutrophils, microglia, and most oligodendrocyte-lineage cells that carry the main CXCR2 biology.
5. **Measured endpoint:** the Wilcoxon DEG count is taken only among surviving recovered nuclei in this neuronal class. A non-neuronal chemotaxis or remyelination phenotype would not be counted unless it secondarily produced a neuron-autonomous nuclear expression state, which the training analogs argue is unlikely.

This transfer model predicts the same direction as the chemokine/inflammatory analogs: no genes pass BH FDR 0.05.

## Target-specific prediction

### `Cxcr2`: predicted `n_degs = 0`

I predicted a zero rather than a one- or few-gene response because every directly represented focal chemokine-receptor comparator had `n_degs = 0` and the broader represented immune signaling comparators were also zeros. `Cxcr4` is the mildest counterexample because it had one focal `Pum1` row at adjusted p = 0.067, but that is still below the requested threshold and was not reproduced by `Ccr2`, `Cx3cr1`, `Rac1`, or `Tiam1`. External CXCR2 papers show that `Cxcr2` is biologically potent in neutrophils and oligodendrocyte-lineage cells during mobilization, inflammation, demyelination, and remyelination, but those links break at cell type and challenge state before reaching a basal NeuN-positive thalamic-glutamatergic DEG endpoint.

This prediction is driven primarily by the within-dataset zeros for `Ccr2`, `Cx3cr1`, `Cxcr4`, cytokine receptors, and inflammatory transcriptional mediators. External knowledge is used to avoid over-transferring non-neuronal CXCR2 phenotypes into this neuronal screen.

## Limits

- No exact in-dataset `Cxcr2` perturbation, `Cxcl1` perturbation, or `Cxcl2` perturbation was available in the training data, so the prediction extrapolates from receptor-class and inflammatory-pathway comparators.
- CXCR2 has documented CNS roles in oligodendrocyte-lineage cells and inflammatory demyelination models; those are not measured by this NeuN-enriched basal neuronal screen.
- AAV editing was not directly measured for held-out `Cxcr2`. Per the dataset calibration, weak or absent target RNA effects are not enough to infer failed editing.
- The focal count endpoint has sampling and multiple-testing thresholds. A subthreshold single-gene change like the `Cxcr4`/`Pum1` row would still be reported as zero here even if it reflected a tiny biological effect.
