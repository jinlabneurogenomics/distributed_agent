# Evidence and forecast

## Target and endpoint

- Target: `Ednrb`, the single row of the declared holdout manifest.
- Endpoint: `n_degs` in `151 TH Prkcd Grin2c Glut`, counted as measured genes with BH-adjusted Wilcoxon `p < 0.05`.
- Declared endpoint inputs used:
  - `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`
  - `training_de_all_cell_groups.parquet`
  - `biology_bundles/Ednrb.json`

## Biology card

The canonical `Ednrb` bundle supports successful molecular realization but weak aggregate reach in the focal population.

- The functional-stock card calls the edited product a renewable EDNRB membrane GPCR. A disruptive edit stops new receptor synthesis, ligand-occupied receptor internalizes and is routed to lysosomes rather than recycled, and the 21 to 28 day window from P16 editing to P37-P44 harvest should be long enough for substantial receptor depletion in successfully edited expressing cells. The card explicitly keeps this partial because basal EDNRB turnover in thalamic neurons and local ligand demand were not measured.
- The observability card gives only a moderate postnatal-neural prior: germline Ednrb loss can cause postnatal spiral-ganglion neuron degeneration, but that is a sensory-ganglion context, not P16 somatic loss in thalamic NeuN+ neurons.
- The exact in-assay reach is very small: in non-target `151 TH Prkcd Grin2c Glut` nuclei, `Ednrb` had `mean_raw_umi = 0.0216`, `pseudobulk_cpm = 1.355`, and was detected in `453 / 23679` cells, or `1.913%`.

## Training measurements

The declared `151 TH Prkcd Grin2c Glut` count table has 1,674 held-in biological perturbations and does not contain `Ednrb`.

- The count distribution was heavily zero-inflated:

| range | held-in perturbations |
| --- | ---: |
| `n_degs = 0` | 1205 |
| `n_degs = 1` | 276 |
| `n_degs = 2..5` | 65 |
| `n_degs >= 10` | 106 |

The median was 0, the 75th percentile was 1, and `1481 / 1674 = 88.5%` of training targets had at most one DEG. Against that baseline, a rare receptor with expression in only about 2% of recovered thalamic nuclei needs unusually coherent signaling or a strong self-transcript effect to rise above zero in the aggregate contrast.

The closest directly represented endothelin-family perturbation was `Ednra`, which had `n_degs = 0` in the requested `151 TH Prkcd Grin2c Glut` count table. The same-experiment July corpus report for `Ednra` classified the Ednra response as buffered across postmitotic neuronal groups and described a lack of canonical endothelin-pathway or data-driven convergence. I treated this report as an interpretation of the same Parquet measurements, not as replication.

I also queried the expression Parquet directly in the focal cell group for 54 held-in GPCR, adhesion-GPCR, and GPCR-adjacent receptor/second-messenger perturbations present in the training table. That query covered 931,986 measured-gene rows. Forty-nine of the 54 had no BH<0.05 genes. The remaining five had exactly one significant gene each, and in every case the single significant feature was the target transcript itself:

| target | BH<0.05 genes in `151 TH Prkcd Grin2c Glut` | significant feature |
| --- | ---: | --- |
| `Adgrl1` | 1 | `Adgrl1` |
| `Adgrl2` | 1 | `Adgrl2` |
| `Adgrl3` | 1 | `Adgrl3` |
| `Gpr158` | 1 | `Gpr158` |
| `Gprasp2` | 1 | `Gprasp2` |

Thus this local receptor-like cohort supplied no clear downstream transcriptional examples in the exact target population.

## Synthesis

Ednrb has a plausible loss of receptor stock by harvest in cells that express it, so I did not treat the perturbation as intrinsically unrealized. The limiting factor is focal-population reach: the receptor transcript is detected in only `1.913%` of non-target nuclei, the relevant ligand-demand state in the thalamic class is unknown, and the readout averages over recovered `151 TH Prkcd Grin2c Glut` nuclei. The held-in quantitative surface is also dominated by exact zeros, and the most relevant held-in receptor evidence, especially `Ednra` and the GPCR-adjacent Parquet slice, does not show downstream DEGs in this class.

I therefore forecast no significant measured genes after BH correction.

```tsv
target_name	predicted_n_degs
Ednrb	0
```
