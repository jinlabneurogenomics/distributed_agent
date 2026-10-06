# Klrk1 held-out DEG-count prediction

## Question and endpoint

I predicted the held-out `n_degs` for `Klrk1` in `151 TH Prkcd Grin2c Glut` cells, where `n_degs` is the number of measured genes with Wilcoxon Benjamini-Hochberg adjusted `pvals_adj < 0.05` in the focal cell group after acute mosaic CRISPR-Cas9 loss of function.

`Klrk1` itself was absent from both supplied training inputs, so its focal DEG count is not directly observed in the declared inputs. The endpoint is a validated direct endpoint for non-held-out training perturbations in `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`, and the held-out task requires transfer from those training counts and the companion differential-expression parquet rather than recovery of a hidden `Klrk1` signature.

## Sources

- Declared training DEG counts: `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`, 1,674 non-held-out targets.
- Declared differential-expression parquet: `training_de_all_cell_groups.parquet`; I queried exact focal-cell rows for biologically related training perturbations and recomputed `SUM(pvals_adj < 0.05)` as a guard against CSV/parquet mismatch.
- Run-local dataset portrait, task bindings, coverage, and capability manifest in `codex_runtime/pipeline/`.
- Internal same-experiment corpus `perturbai-july-260713-sourceguard-1773-v1`: used only as packaged same-experiment interpretation for visible analogs; BioKG had no `Klrk1` `TargetGene` node, consistent with the target being held out.
- External PubMed literature on NKG2D/KLRK1 biology: Watzl 2003, DOI `10.1016/S1286-4579(02)00057-6`; Lanier 2015, DOI `10.1158/2326-6066.CIR-15-0098`; Zompi et al. 2003, DOI `10.1038/ni930`; Graham et al. 2006, DOI `10.4049/jimmunol.177.4.2349`; Walsh et al. 2007, DOI `10.1128/JVI.02033-07`; Backstrom et al. 2003, DOI `10.1002/immu.200390012`.

## Quantitative calibration from training data

The focal training endpoint is sparse and zero inflated:

| targets | mean `n_degs` | median | 75th pct. | 95th pct. | max | nonzero |
|---:|---:|---:|---:|---:|---:|---:|
| 1674 | 14.05 | 0 | 1 | 18 | 2677 | 469 |

There were no non-held-out perturbations from the `Klrk1`/NK C-type lectin receptor family itself: no `Klr*`, `Ncr*`, `Raet*`, `H60*`, `Ulbp*`, `Mica`, or `Micb` targets were present in the focal training count table. I therefore used immune-lineage and immune-receptor targets as the nearest within-dataset counterfactuals, requiring each analog to be a real training perturbation with a recomputable focal signature.

For these analogs I filtered the parquet to `group_name = '151 TH Prkcd Grin2c Glut'` and counted adjusted p-values below 0.05. The relevant query was:

```sql
SELECT gene_target,
       SUM(pvals_adj < 0.05)::INT AS n_degs_recomputed,
       MIN(pvals_adj) AS min_padj,
       MAX(ABS(scores)) AS max_abs_score,
       ANY_VALUE(n_pert_matched) AS n_pert,
       ANY_VALUE(n_ctrl_matched) AS n_ctrl
FROM read_parquet('training_de_all_cell_groups.parquet')
WHERE group_name = '151 TH Prkcd Grin2c Glut'
  AND gene_target IN (...)
GROUP BY gene_target;
```

Closest training perturbations, all focal-cell nulls:

| analog perturbation | reason for comparison to `Klrk1` | focal `n_degs` | best focal adjusted p-value |
|---|---|---:|---:|
| `Cd3d` | immune receptor complex component; same logic of lymphocyte-restricted surface signaling | 0 | 1.000 |
| `Cd3e` | CD3/TCR component | 0 | 0.752 |
| `Cd3g` | CD3/TCR component | 0 | 1.000 |
| `Cd247` | immunoreceptor ITAM signaling chain in T/NK-lineage receptors | 0 | 1.000 |
| `Cd4` | lymphocyte coreceptor | 0 | 0.221 |
| `Ptprc` | CD45, proximal leukocyte/TCR signaling phosphatase | 0 | 0.551 |
| `Cd79a`, `Cd79b` | B-cell antigen-receptor signaling chains | 0, 0 | 1.000, 1.000 |
| `Cd14`, `Tlr2`, `Tlr3`, `Tlr4`, `Tlr5`, `Tlr7`, `Tlr8` | innate immune receptors rather than neuronal transcriptional regulators | all 0 | all 1.000 |
| `Il2ra`, `Il2rb`, `Il2rg`, `Il12rb1`, `Il23r` | cytokine receptor chains used by immune cells | all 0 | 0.435 to 1.000 |
| `Fcgr4`, `Itgb2`, `Clec16a` | Fc/integrin/C-type-lectin-adjacent immune genes | all 0 | 0.059 to 1.000 |
| `P2ry12`, `Cx3cr1`, `Csf1r`, `Mertk`, `Spi1`, `Irf8` | microglial/myeloid-enriched genes included in the screen | all 0 | 0.121 to 1.000 |

The same-experiment July corpus independently summarized the Cd3d perturbation as transcriptionally silent across all measured NeuN+ neuronal groups and contrasted it with Cd3e, Cd3g, Cd247, Cd4, and Ptprc, which also failed to form a shared neuronal module. That corpus is a packaged interpretation of the same Perturb-seq experiment, not independent replication, but it agrees with the raw focal-cell counts for the closest visible immune signaling genes.

## Target-specific causal transfer

`Klrk1` encodes NKG2D, an activating C-type lectin-like receptor on NK cells, CD8-positive T cells, gamma-delta T cells, invariant NKT cells, and some activated CD4-positive T cells. Its biological role is to recognize stress-induced ligands and route immune effector signaling through DAP10 and, in mouse, DAP12-associated isoforms. That places its canonical intervention chain as:

`Klrk1` loss -> impaired NKG2D surface receptor signaling -> impaired cytotoxic lymphocyte activation/costimulation against stressed ligand-positive targets -> altered immune killing or cytokine output.

That chain does not map onto the requested assay stage. The Perturb-seq intervention was delivered to postmitotic NeuN-positive brain nuclei and read out among recovered thalamic glutamatergic neurons; NK cells, T cells, and microglia were absent or under-sampled. CNS studies that implicate NKG2D do so through infiltrating immune cells reacting to infected or injured neural targets: Walsh et al. found NKG2D on infiltrating CD8 T cells in viral encephalitis, while Backstrom et al. showed RAE-1/NKG2D-dependent NK killing of ligand-positive dorsal root ganglion neurons. Those studies support NKG2D as a receptor on immune effectors or NK cells, with neurons more naturally acting as ligand-bearing targets under stress, not as `Klrk1`-dependent receptor-bearing effectors.

The within-dataset analogs therefore predict the same endpoint direction: perturbing a lymphocyte or innate-immune receptor in sparse juvenile neurons should not produce a broad cell-autonomous transcriptional signature. None of the available leukocyte receptor analogs had any focal FDR<0.05 gene, and several extremely immune-restricted counterexamples with stronger proximal signaling relationships than `Klrk1` to neuronal biology, such as `Cd3d`, `Cd247`, `Ptprc`, `Cd79a`, `Cd79b`, `Cd14`, and `Fcgr4`, were exactly zero.

## Prediction and limits

I predict `Klrk1 -> 0` DEGs in `151 TH Prkcd Grin2c Glut` cells.

This prediction is driven mainly by within-dataset nulls for immune-lineage receptor/signaling perturbations, then by external NKG2D biology. It is still an extrapolation because the training set contained no direct `Klrk1`, `Klr` paralog, `Ncr1`, or Rae1/H60/Mult1 perturbation. A subtle neuron-intrinsic function in a rare stressed or injured substate would be missed in this pooled recovered-nucleus assay, and the delivered CRISPR guides could perturb any cell exposed by AAV-PHP.eB rather than just focal neurons; however, the endpoint only counts transcriptional DE among recovered focal thalamic glutamatergic nuclei. Under that endpoint, the best-supported point estimate is the zero-DEG boundary rather than a small positive count.
