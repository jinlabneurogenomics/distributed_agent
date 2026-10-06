# Cul3 direct `n_degs` forecast

## Target and endpoint

- Target: `Cul3`
- Cell class: `151 TH Prkcd Grin2c Glut`
- Endpoint: count of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`
- Forecast: `64`

I used the declared biology-only Cul3 bundle, the visible `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` counts, and profile comparisons computed from the declared `training_de_all_cell_groups.parquet` in the matching thalamic class. I did not use a Cul3 expression signature, Cul3 DEG count, calibrated response probability, labeled-neighbor outcome, or endpoint-selection artifact.

## Cul3 biology used for the forecast

The canonical target bundle places Cul3 loss in the ubiquitin-proteasome system but not at the same proximal severity as knocking down a core proteasome particle or UFMylation enzyme. CUL3 is the cullin scaffold of BTB-CUL3-RBX1 E3 ligase complexes; loss should impair repeated adaptor-specific substrate ubiquitination and can plausibly affect postmitotic neurons over weeks. The exact in-assay reach is favorable: in non-target nuclei from `151 TH Prkcd Grin2c Glut`, `Cul3` was detected in 21,435 of 23,679 cells, or 90.523%, with mean raw UMI 2.9748.

The bundle also weakens a high-count forecast. Its functional-stock card concludes `functional_stock_by_harvest = partially_depleted_or_leading_edge`: a P16 edit stops production of new intact CUL3, but pre-existing CUL3 complexes are not directly destroyed, and no transferable neuronal half-life establishes near-complete protein clearance by P37-P44. I therefore treated Cul3 as a broad, direct CRL3 scaffold perturbation with partial realization, not as an acute collapse of all proteasomal degradation.

## Visible quantitative references

The visible training count table for this same cell class contained 1,674 perturbations. It was sparse: 1,205 had zero DEGs, 469 had any DEGs, 106 had at least 10, 69 had at least 25, 59 had at least 50, and 43 had at least 100; the median was 0 and the mean was 14.05.

Ubiquitin/proteostasis-related visible perturbations spanned three regimes:

| visible target | `n_degs` | interpretation |
|---|---:|---|
| `Uba5` | 2677 | UFMylation E1; extreme ER/mitochondrial/proteostasis state |
| `Ufc1` | 572 | UFMylation E2; same pathway, still very large |
| `Psmb4` | 742 | 20S proteasome core; strong proteasome stress |
| `Psmc1` | 430 | 19S proteasome ATPase; strong proteasome stress |
| `Nrf1` | 138 | proteasome-stress transcriptional regulator |
| `Huwe1` | 158 | broad E3 ligase perturbation |
| `Tsc2` | 86 | broad stress/metabolic comparator |
| `Mib1` | 27 | E3 ligase, moderate-low |
| `Usp48` | 10 | ubiquitin protease, weak |
| `Kctd1` | 2 | BTB/KCTD adaptor-like gene, near-null |
| `Klhl7` | 0 | CUL3 BTB adaptor, null |
| `Fbxw7` | 1 | cullin-adaptor pathway gene, near-null |
| `Ube3a` | 0 | E3 ligase, null |
| `Sqstm1` | 1 | autophagy cargo-receptor gene, near-null |
| `Vcp` | 2 | proteostasis ATPase, near-null |

The packaged same-experiment Findings for the high references matched those counts: `Psmb4` and `Psmc1` were annotated as core proteasome insults with broad but cell-type-gated proteasome bounce-back, autophagy/endolysosomal, heat-shock/integrated-stress, redox, and p53-like damage arms. `Uba5` was even larger but carried a UFMylation-specific state with uniformly upward OXPHOS/import and ER-quality-control compensation. Those are upper-scale references for severe proteostasis failure, not direct estimates for a partial CRL3 scaffold loss.

The matched-profile comparison over 15 visible references in the Parquet kept the same separation. `Uba5` and `Ufc1` were the tightest large ubiquitin-like pair and shared 304 positive and 191 negative significant same-direction genes. `Psmb4` and `Psmc1` were also coherent relative to the hand-picked cohort, sharing 88 positive and 127 negative significant genes with a 0.29 positive top-tail overlap. Cross-pair overlap between UFMylation and core proteasome was partial rather than centroid-like: for `Uba5` against `Psmb4` and `Psmc1`, the positive significant overlap coefficients were 0.319 and 0.290 and the direction-conflict counts were 59 and 49. Thus I used these visible signatures as response-scale boundaries, not as one pooled module.

## Point synthesis

The strongest downward bearings were the partial CUL3 stock loss by harvest and the near-null counts for specific BTB/CUL3-adaptor perturbations. The strongest upward bearings were high Cul3 baseline reach in the assayed nuclei, scaffold-level rather than single-adaptor biology, weak evidence for true cullin-family compensation, and the clear ability of this thalamic population to produce hundreds to thousands of DEGs when proteostasis is directly disrupted.

I therefore placed Cul3 above the isolated adaptor/E3 near-null range and above `Mib1`/`Usp48`, but below the `Nrf1`/`Huwe1`/`Tsc2` high-moderate group because CUL3 loss is upstream and incompletely realized at 21-28 days. A forecast of 64 DEGs puts it just into the visible table's high-response tail without projecting the core-proteasome or UFMylation footprints onto Cul3.
