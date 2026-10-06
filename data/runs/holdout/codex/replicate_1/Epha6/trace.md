# Epha6 DEG-count forecast

## Target and endpoint

- Target: `Epha6`
- Population: `151 TH Prkcd Grin2c Glut`
- Endpoint: `n_degs`, the count of measured genes with Wilcoxon `pvals_adj < 0.05`
- Prediction: `0`

## Evidence used

1. The declared characterization bundle identified Epha6 as a single-pass cell-surface EphA receptor tyrosine kinase that signals through contact-dependent ephrin-A binding. Successful editing should stop new intact receptor supply, and the 21-28 day P16-to-P37/P44 interval is long enough that the functional surface-receptor stock is likely substantially depleted, but this inference is partial because EphA6-specific turnover in juvenile thalamic neurons was not measured.

2. Exact in-assay reach for `Epha6` in `151 TH Prkcd Grin2c Glut` was substantial: 18,939 of 23,679 non-target nuclei expressed the gene, 79.98% of cells, with mean log1p CP10k 0.946 and pseudobulk CPM 211.9. This made a transcriptional response observable if acute EphA6 loss drove one, but did not itself say the target endpoint would be nonzero.

3. Curated analog nomination against the 1,674-gene training universe placed the direct Eph receptor comparators first: `Epha3`, `Epha4`, `Ephb1`, `Ephb2`, `Epha5`, `Epha2`, `Ephb4`, and `Epha10`. A STRING physical edge nominated `Ephb1`; the other leading Eph-family nodes were shared ephrin-receptor or Eph/ephrin signaling annotations rather than exact paralogs.

4. The same-experiment corpus connected those eight Eph receptors as a fully linked explicit-Finding cohort and summarized their postnatal snRNA surfaces as flat, singleton-only, or receptor-specific rather than a common Eph-family nuclear RNA program. Epha5's report was especially relevant because it stated that `Epha6` was not a queryable perturbation in that family test, so I used the represented family as a boundary rather than as a direct Epha6 outcome.

5. The exact 151-class training counts for the direct receptor/proximal cohort were very low:

| cohort | genes | 151-class counts |
|---|---:|---|
| Eph receptors: `Epha10`, `Epha2`, `Epha3`, `Epha4`, `Epha5`, `Ephb1`, `Ephb2`, `Ephb4` | 8 | seven zeros and `Epha4 = 1` |
| top receptor/proximal analogs: Eph receptors plus `Ntrk1`, `Fyn`, `Kdr`, `Ptpn11` | 12 | eleven zeros and `Epha4 = 1` |

6. Expansion from recurrent corpus mentions added 20 PI3K, MAPK, Rho/PAK, NMDAR, membrane-processing, and RTK boundary nodes. Fresh profile comparison on the declared Parquet, restricted to `151 TH Prkcd Grin2c Glut`, found that the 32-node expanded cohort was still mostly inactive in the task-matched endpoint: 24 of 32 nodes had no significant features; 7 had 1-9 significant features; only the NMDAR core gene `Grin1` had >=50. The expanded count table gave 13 zeros among the 20 expanded nodes, singleton `Grin2a`, `Pak1`, and `Cdc42`, small `Grin2b = 2` and `Ntrk2 = 3`, and `Grin1 = 89`.

## Synthesis

EphA6 is expressed in the assayed thalamic neurons and should be functionally engaged by the harvest window, so I did not treat it as an unedited or unobservable target. The measured training data nevertheless put the relevant biology on a flat scale: represented EphA/EphB receptor losses had 0 or 1 DEG in the exact target population, and same-experiment Findings explicitly described a lack of shared Eph-family nuclear convergence in this acute postnatal snRNA readout.

The larger PI3K/MAPK/Rho/PAK/NMDAR expansion did not justify lifting the estimate. Most of those proximal nodes were also flat in `151 TH Prkcd Grin2c Glut`, and the one strong count, `Grin1 = 89`, is a synaptic NMDAR boundary rather than an EphA receptor analog. Given the direct Eph receptor mean of 0.125, the median of 0, and the absence of a matched thalamic acute-loss phenotype stronger than expression itself, the most defensible integer forecast is:

```tsv
target_name	predicted_n_degs
Epha6	0
```
