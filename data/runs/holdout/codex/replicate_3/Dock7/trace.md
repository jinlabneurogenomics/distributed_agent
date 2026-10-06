# Dock7 DEG-count forecast

## Target and endpoint

- Target: `Dock7`
- Population: `151 TH Prkcd Grin2c Glut`
- Endpoint: number of measured genes with BH-adjusted Wilcoxon `p < 0.05`
- Prediction: `0`

## Evidence used

### Canonical biology-only Dock7 bundle

- `Dock7` is expressed in the focal non-target nuclei: `93.6568%` of `151 TH Prkcd Grin2c Glut` non-target cells expressed it, with mean raw UMI `3.5935`, mean CP10k `2.2779`, and mean log1p CP10k `1.0901`.
- Functional stock depletion by P37-P44 is plausible. Dock7 is a dynamic DHR2-domain Rac-family/Cdc42 GEF and scaffold, the source card cites target-specific mouse-cell protein half-life of about 16-17 hours in a non-neural context, and acute P3 Dock7 RNAi creates a rescued postnatal neuroblast-migration defect within seven days.
- The same biology bundle also weakens endpoint transfer into this assay: the directly observed in vivo postnatal phenotype is in migratory V-SVZ neuroblasts, the Tacc3 and ErbB4 interactions are embryonic progenitor or cortical interneuron contexts, severe germline truncation mice are grossly normal across the bounded neurological panel, and mature thalamic functional demand is unestablished.

### Exact training count table

The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` contains 1,674 non-held-out perturbations. It is highly zero-inflated for this exact endpoint:

- `1,205 / 1,674` have `n_degs = 0`
- `1,481 / 1,674` have `n_degs <= 1`
- `80 / 1,674` have `n_degs >= 20`
- `43 / 1,674` have `n_degs >= 100`

For the directly represented local Dock7 signaling neighborhood in the same count table:

| target | `n_degs` |
|---|---:|
| `Rac1` | 0 |
| `Cdc42` | 1 |
| `Dock3` | 0 |
| `Erbb3` | 0 |
| `Erbb4` | 0 |
| `Tiam1` | 0 |
| `Kalrn` | 0 |
| `Arhgap32` | 0 |
| `Limk1` | 0 |
| `Mapk1` | 0 |
| `Mapk9` | 0 |
| `Pak1` | 1 |
| `Pak2` | 0 |
| `Pak3` | 0 |

That gives 12 exact zeros and two singleton profiles across 14 nearby GEF/GTPase/kinase/receptor targets.

### Training Parquet profile review

I compared the 14 represented Dock7-neighborhood training perturbations in the declared Parquet, restricted to `group_name == "151 TH Prkcd Grin2c Glut"`, using signed Wilcoxon `scores` and `pvals_adj < 0.05`.

- The profile comparison reported 12 nodes with no significant features and 2 nodes with `1_to_9_significant_features`.
- The two nonzero nodes were single self-transcript calls:
  - `Cdc42`: one significant feature, the `Cdc42` transcript itself, `pvals_adj = 8.622e-05`.
  - `Pak1`: one significant feature, the `Pak1` transcript itself, `pvals_adj = 5.019e-08`.
- The selected whole-profile similarities were near zero. For example, `Rac1` had no significant features and cosine values from `-0.0149` to `0.0244` against the nine non-focal peers in the inspected local cohort; `Cdc42` had no significant-feature intersection with any inspected peer.

Thus, among the observed perturbations closest to Dock7's Rac/Cdc42 and non-GEF signaling roles, the focal thalamic class shows no recurring downstream RNA state; the only nonzero counts come from detectable loss of the perturbed target transcript itself.

### Same-experiment corpus context for training comparators

The selected corpus is an interpretation layer over the same perturbation experiment rather than independent replication, so I used it only to interpret the measured training rows:

- `Cdc42:F003` states that neither unbiased signature neighbors nor represented Rho/Rac/Cdc42-axis relatives formed a shared Cdc42-like transcriptomic module, and explicitly lists `Rac1`, `Pak1`, `Pak2`, `Pak3`, `Limk1`, `Tiam1`, `Kalrn`, `Dock3`, `Arhgap32`, and `Arhgef9` as flat or single-gene responders.
- `Dock3:F001` and `Dock3:F002` describe Dock3 as producing no robust downstream snRNA-seq response and not converging with canonical Rac/WAVE/GSK3b nodes in the matched cell groups.
- `Erbb4:F001` and `Erbb4:F002` describe Erbb4 as buffered at the nuclear RNA level after receptor transcript reduction and not phenocopied by directly represented Erbb-family/neuregulin targets.

## Synthesis

The Dock7 perturbation should be functionally realized: its mRNA is present in this thalamic population and its operative protein pools should turn over within the P16-to-P37/P44 window. The biological evidence, however, points mainly to local cytoskeletal, polarity, migration, and receptor-signaling functions whose proximal readouts are GTP loading, morphology, phosphorylation, or cell movement. Those are exactly the classes of Rac/Cdc42/PAK/DOCK/ErbB perturbations that are almost completely buffered in the training thalamic snRNA endpoint.

I therefore treated the focal training neighborhood as the closest quantitative scale evidence. Its downstream median is zero, and the two one-count examples are self-transcript-only events rather than an expressed pathway state. `Dock7`'s high expression leaves a small chance that the target transcript itself would be counted, but the atlas-wide design notes make self mRNA reduction an unreliable readout of CRISPR activity, and zero remained the modal and biologically best-supported count.

Point forecast: **`n_degs = 0`**.
