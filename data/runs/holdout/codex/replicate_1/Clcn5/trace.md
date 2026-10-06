# Direct forecast for Clcn5

Target: `Clcn5`

Focal population: `151 TH Prkcd Grin2c Glut`

Endpoint: `n_degs`, the number of measured genes with BH-adjusted Wilcoxon `p < 0.05` in the focal population.

Predicted `n_degs`: **0**

## Evidence used

### Clcn5 biology-only bundle

Source: declared biology bundle `Clcn5.json`.

- Exact focal-population reach is low but nonzero: `Clcn5` RNA is detected in 6,645 of 23,679 non-target nuclei, 28.0628% of the focal population, with mean CP10K 0.225918, mean raw UMI 0.362811, and pseudobulk CPM 22.7386.
- ClC-5 is an endosomal 2Cl-/H+ exchanger that supports endosomal ionic state and trafficking.
- Mouse loss-of-function evidence is strong for kidney proximal-tubule endocytosis, but the direct tested phenotype is non-neural and does not establish an acute postnatal thalamic-neuron requirement.
- The bundle adjudicates the pre-edit operative pool as a renewable endosomal membrane-protein pool. A P16 edit should stop new ClC-5 supply while old protein turns over, so functional stock is likely substantially depleted by the P37-P44 harvest, but ClC-5-specific neuronal turnover was not measured.
- `Clcn3` and `Clcn4` are the close same-family genes named in the bundle. Kidney genetics argues they did not replace the ClC-5 renal endocytic role, but the bundle explicitly leaves thalamic redundancy unresolved.

Interpretation: the perturbation is probably realized in edited, expressing cells, but focal reach is sparse and the direct functional evidence for a survivor-conditioned thalamic transcriptional state is weak. That makes a near-zero count more plausible than a broad endolysosomal stress response.

### Focal training DEG counts

Source: declared training table `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.

The training distribution in this same focal population is heavily concentrated at zero:

| statistic | value |
| --- | ---: |
| training targets | 1,674 |
| targets with `n_degs = 0` | 1,205 |
| targets with `n_degs = 1` | 276 |
| targets with `n_degs <= 1` | 1,481 |
| median | 0 |
| 75th percentile | 1 |
| 90th percentile | 2 |
| 95th percentile | 18 |
| mean | 14.0538 |

The long right tail is driven by broad regulators, while the mode, median, and closest local comparators are quiet.

### Selected same-population training profiles

Source: declared Parquet `training_de_all_cell_groups.parquet`, restricted to `group_name = '151 TH Prkcd Grin2c Glut'`.

| training perturbation | focal `n_degs` | Parquet check |
| --- | ---: | --- |
| `Clcn3` | 0 | self row `logfoldchanges = -0.546803`, `pvals_adj = 0.619708`; no BH-significant genes |
| `Clcn4` | 1 | the only BH-significant row is `Clcn4` itself, `logfoldchanges = -0.802075`, `pvals_adj = 6.72e-11` |
| `Atp6v0a1` | 1 | the only BH-significant row is `Atp6v0a1` itself, `logfoldchanges = -0.639531`, `pvals_adj = 4.52e-12` |
| `Atp6v1a` | 0 | self row `logfoldchanges = -0.236252`, `pvals_adj = 1`; no BH-significant genes |
| `Vps35` | 17 | a larger retromer/endosomal-traffic perturbation, used as a loose upper local scale rather than as a close donor |
| `Rab7` | 501 | central endolysosomal trafficking perturbation, used only as a broad-response boundary |

`Clcn3` and `Clcn4` were the most direct measured family-level comparators available in the training table. Both were essentially downstream-silent in this focal population; the single `Clcn4` DEG was the target transcript itself. Looser vesicle-acidification or trafficking perturbations showed that this cell class can mount a transcriptional response when core endolysosomal machinery is hit, but the response size rose with much broader machinery disruptions and therefore should not be transferred to a low-expressed ClC-5 exchanger.

## Synthesis

The endpoint includes the perturbed transcript, so a one-gene count is possible if `Clcn5` itself reaches FDR significance. I still put the integer point at 0 because:

- exact Clcn5 focal expression is sparse, with only 28.1% non-target nuclei expressing any detected transcript;
- the close ClC paralog perturbations landed at 0 and 1, and `Clcn4`'s one hit was only self RNA;
- other narrow endosomal acidification genes in the sampled set also landed at 0 or a self-only 1;
- the bundle has no direct postnatal neuronal phenotype or timing evidence that would push Clcn5 toward a multi-gene state; and
- the empirical focal count distribution has zero as its modal and median outcome.

Balancing a realized but low-reach lesion against mostly silent nearest training perturbations, the best blind point forecast is:

```tsv
target_name	predicted_n_degs
Clcn5	0
```
