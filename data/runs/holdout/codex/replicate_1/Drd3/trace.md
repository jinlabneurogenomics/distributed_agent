# Direct forecast trace

## Target and endpoint

- Target: `Drd3`
- Focal population: `151 TH Prkcd Grin2c Glut`
- Endpoint: `n_degs`, the number of measured genes in this focal population with BH-adjusted Wilcoxon `p < 0.05`.

## Biology used

The declared prediction-safe Drd3 bundle identifies DRD3 as a Gi/Go-coupled seven-transmembrane dopamine receptor at the plasma membrane/dopaminergic synapse. Its exact same-assay expression reach in `151 TH Prkcd Grin2c Glut` is low: `961 / 23679` non-target nuclei express Drd3, `pct_cells_expressing = 4.058448414206681`, `mean_raw_umi = 0.07960640229739431`, and `mean_cp10k = 0.04791854418871145`.

The prior biology is therefore compatible with a real D3 perturbation in a small thalamic subpopulation, but not with a broad perturbation of most aggregated thalamic glutamatergic nuclei. The stock card also leaves within-window receptor depletion unresolved: gene disruption stops new receptor production, but existing membrane/intracellular receptor initially persists, and no basal neuronal DRD3 half-life or direct P16-to-P37/P44 clearance series is available.

## Training measurements used

The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` table contains `1674` observed training targets. Its count distribution is sharply concentrated at zero:

- `1205 / 1674` training targets have `n_degs = 0`.
- The median is `0`.
- The 75th percentile is `1`.
- The upper tail is mechanistically dominated by ubiquitous RNA processing, proteostasis, and chromatin targets such as `Uba5`, `Tpr`, `Sin3a`, `Rnpc3`, and `Psmb4`, not by sparse neuromodulatory receptors.

The closest directly observed dopamine-receptor rows in the focal count table are all null:

- `Drd2 = 0`
- `Drd4 = 0`
- `Drd5 = 0`

Represented dopamine/cAMP-axis rows are also focal-null or near-null:

- `Adcy1 = 0`, `Adcy3 = 0`, `Adcy5 = 0`
- `Gnal = 0`, `Gnas = 0`, `Gnao1 = 1`
- `Pde1c = 0`, `Pde4b = 0`, `Pde4d = 0`, `Pde10a = 0`
- `Prkaca = 1`, `Camk2b = 1`, `Creb1 = 10`

## Parquet/profile checks

I scanned the declared training Parquet in the exact focal context using `Drd2`, `Drd4`, and `Drd5` as observed anchors and the 1,674-row training table as the eligible universe. All three receptor anchors had available focal profiles with `17259` measured features and zero FDR-significant features at `pvals_adj < 0.05`, matching the focal count table.

Their nearest whole-profile neighbors were weakly informative null-space neighbors rather than a dopamine receptor module: top-50 positive/negative tail overlaps were tiny and there was no shared significant program for any of the three anchors. The 219-node receptor-neighborhood union was mostly quiet (`158 / 219` at zero), and the few high-count members were unrelated RNA-processing or regulatory outliers such as `Cdc40`, `Dctn1`, `Chd8`, and `Stag2`. I therefore used the family/pathway rows themselves as the quantitative comparators rather than averaging the incidental profile-neighbor union.

## Same-experiment corpus checks

Packaged Findings for the observed dopamine receptors agree with the raw focal observations and help bound their interpretation:

- `Drd2` produced only a restricted one-gene cortical response and did not converge with represented dopamine-family receptors or proximal cAMP effector nodes.
- `Drd4` was FDR-clean across all recovered neuronal groups at FDR<0.10 and did not converge with `Drd2`, `Drd5`, G-protein, adenylyl-cyclase, or phosphodiesterase perturbations.
- `Drd5` was also transcriptionally silent across recovered neuronal groups at FDR<0.10; its report notes that canonical immediate-early/cAMP/CREB mRNAs were assay-visible elsewhere but did not appear after Drd5 loss.

Those reports are same-experiment interpretations, not independent replication, but they argue that this basal juvenile mosaic snRNA assay does not generally convert dopamine-receptor loss into a durable broad mRNA module.

## Forecast

Drd3 has some positive biological observability evidence: it is present in postnatal mouse thalamus and D3-null adult mice show neural phenotypes. The endpoint-specific downward bearings are stronger for this aggregate count: exact focal expression is only about 4%, the receptor is a neuromodulatory GPCR rather than an obligate housekeeping/chromatin/proteostasis factor, within-window installed receptor depletion is uncertain, the closest D2-family dopamine-receptor perturbations were focal-null, and the represented dopamine/cAMP pathway was mostly focal-null or singleton-scale.

I therefore predict the modal focal count:

```tsv
target_name	predicted_n_degs
Drd3	0
```
