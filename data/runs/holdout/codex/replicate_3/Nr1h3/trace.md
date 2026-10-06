## Evidence

Target: `Nr1h3`

Endpoint: `n_degs` in `151 TH Prkcd Grin2c Glut`, counted as measured genes with Wilcoxon BH-adjusted `p < 0.05`.

The declared exact reach bundle places `Nr1h3` at very low baseline abundance in this focal population: 843 of 23,679 non-target nuclei expressed it, for 3.56% expressing cells, mean raw UMI 0.038, mean CP10k 0.0236, and pseudobulk 2.39 CPM. This does not prove an ineffective CRISPR perturbation, but it does make a broad directly cell-autonomous transcriptional response in thalamic neurons a weak prior.

The same bundle says a P16 disruptive edit should plausibly deplete functional LXR-alpha/RXR receptor stock by P37-P44 because LXR-alpha is a renewable dynamic transcription factor rather than a durable installed structure. The biology pointing in the other direction is that the direct single-gene `Nr1h3` loss phenotype is hepatic/systemic under cholesterol challenge, matched postnatal thalamic neuronal demand is unknown, and the `Nr1h2` paralog has relevant neural biology without direct evidence that it creates a short-window `Nr1h3` single-loss state in these neurons.

I treated the declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` as the direct endpoint distribution and the 151-filtered rows of `training_de_all_cell_groups.parquet` as the exact same-experiment measurements behind chosen analogs. `Nr1h3` itself is absent from the 1,674-row training count table. The distribution is strongly concentrated at zero: 1,205 of 1,674 targets have `n_degs = 0`, the median is 0, the 75th percentile is 1, and the 90th percentile is 2.

Closest measured same-axis comparators in this focal class were quiet:

| comparator set | training targets | 151 `n_degs` |
|---|---|---|
| LXR/RXR nuclear-receptor axis | `Nr1h2`, `Rxra`, `Rxrb`, `Rxrg` | 0, 0, 0, 0 |
| lipid/cholesterol transcriptional or target genes | `Abca1`, `Abca7`, `Hmgcr`, `Srebf1`, `Srebf2` | 0, 0, 0, 0, 7 |
| PPAR nuclear receptors that share the RXR/lipid-regulatory theme | `Ppara`, `Ppard`, `Pparg` | 0, 0, 0 |
| another retinoid-family nuclear receptor | `Rarb` | 0 |

The Parquet rows for those same 151 contrasts reproduced the count-table values and showed that this was not because controls were missing: matched perturbed nuclei were 200 for `Nr1h2`, 247/249/229 for `Rxra`/`Rxrb`/`Rxrg`, 227/213/109/202/209 for `Abca1`/`Abca7`/`Hmgcr`/`Srebf1`/`Srebf2`, and 158/315/109 for `Ppara`/`Ppard`/`Pparg`, each compared with 23,679 matched controls.

I downweighted broader nuclear-receptor outliers such as `Rora` at 278 and `Nr1d1` at 116 because their 151 signatures look like direct neuronal transcription-factor programs rather than close LXR-alpha operation. The near-zero outcomes for the LXR paralog, RXR partners, lipid/cholesterol genes, and PPAR family were more informative for this target than the outliers.

## Synthesis

`Nr1h3` is likely edited into a real LXR-alpha loss-of-function state by harvest, but only a small fraction of assayed 151 thalamic neurons detectably express the transcript and the biology bundle does not establish a P16-P44 thalamic neuronal requirement for the LXR-alpha single knockout. The training distribution already favors zero, and the closest measured lipid/nuclear-receptor comparators are almost uniformly zero in this same focal population, with only `Srebf2` showing a small 7-gene response.

I therefore predict that the held-out `Nr1h3` perturbation will land at the zero-count mode rather than at a small nonzero lipid-response count.
