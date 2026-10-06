# Direct Timp2 n_degs forecast

## Target and endpoint

- Target manifest: `Timp2`.
- Endpoint: `n_degs` in `151 TH Prkcd Grin2c Glut`, the count of measured genes with Wilcoxon BH-adjusted `pvals_adj < 0.05`.
- Declared training sources used:
  - `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
  - `[local file: training_de_all_cell_groups.parquet]`
  - `[local file: Timp2.json]`

## Biology of the held-out perturbation

The biology bundle identifies TIMP2 as a secreted, extracellular metalloproteinase regulator that binds metalloproteinase catalytic zinc and can participate with MT1-MMP/MMP14 in pro-MMP2 activation complexes. The requested P16 CRISPR lesion should stop new neuronal TIMP2 supply, but it should not directly disable already secreted or already MMP-bound TIMP2. Its functional-stock card therefore called harvest-time TIMP2 loss `likely_substantially_depleted`, with partial evidence completeness rather than complete clearance.

The exact focal expression measurement makes target reach plausible in the assayed class: `Timp2` was detected in 18,431 of 23,679 non-target `151 TH Prkcd Grin2c Glut` nuclei, or 77.84%, with mean raw UMI 3.17 and mean CP10k 2.01. That is strong evidence that the target transcript itself can be measured in this class, but it does not establish editing efficiency or the size of a downstream program.

The residual biological uncertainty is important. Postnatal or adult neural loss phenotypes are reported for other mouse neural contexts, especially cerebellar, neuromuscular, and hippocampal settings, but no card evidence matched acute P16 loss in thalamic glutamatergic neurons over the 21-28 day experimental interval.

## Visible training measurements

The declared `151` count table is highly sparse:

- 1,205 / 1,674 visible training targets had `n_degs = 0`.
- 276 / 1,674 had `n_degs = 1`.
- 1,542 / 1,674 had `n_degs <= 4`.
- The median was 0, the 75th percentile was 1, and the mean was inflated to 14.05 by a small high-response tail.

`Timp2` has no other visible perturbed member in its MMP14-TIMP2 or MMP2-MMP14-TIMP2 CORUM complexes. The nearest curated pathway set that did have visible members was `WP_MATRIX_METALLOPROTEINASES`, and its visible non-target members were sparse in `151`:

| Perturbation | 151 `n_degs` | FDR-significant measured genes from the Parquet |
| --- | ---: | --- |
| `Bsg` | 1 | `Bsg` |
| `Tcf20` | 0 | none |
| `Timp3` | 1 | `Timp3` |

The broader visible extracellular-matrix / protease-regulation cohort was also quiet. Among 28 visible members selected from Timp2's curated ECM and proteolysis-regulation annotations, 21 had `n_degs = 0`, six had `n_degs = 1`, one had `n_degs = 2`, and the total was only eight DEGs. Parquet inspection showed that the one-count members were self-transcript-only hits: `Bsg`, `Cst3`, `Ctsb`, `Ide`, `Plxna2`, and `Timp3` each passed FDR only at their own transcript; `Serpine2` passed at `Serpine2` and `Clip2`; the rest were null in `151`.

The selected same-experiment corpus supports the same interpretation as the Parquet, not as independent replication but as the curated semantic layer over those measurements. `Timp3:F001` and `Timp3:F004` describe a one-transcript TIMP3 effect in CTX-CGE GABA interneurons and broad buffering elsewhere, including no downstream response in the thalamic group despite a significant thalamic Timp3 self-drop. `Bsg:F001` similarly reports a pan-neuronal transcriptional null downstream of Bsg self-mRNA depletion, and `Bsg:F002`/`Bsg:F003` show that represented extracellular, MMP, PMCA, lactate/pH, and stress-program neighbors did not turn Bsg loss into a 151 thalamic DEG program.

## Forecast

The mechanistically closest visible data argue against a broad downstream response in recovered thalamic nuclei. TIMP2 is secreted and extracellular, the exact thalamic neuron setting is only partially supported by prior biology, and visible TIMP/MMP/ECM perturbations were almost all null or self-only in the same class. That puts the downstream expectation near zero.

I nevertheless assign one DEG rather than zero because `Timp2` is expressed in most non-target nuclei in the exact focal class, the endpoint includes the self-transcript, and the closest visible secreted/extracellular perturbations with a measurable effect in `151` most often contributed only their own depleted transcript. The point forecast is therefore a self-dominated sparse response with no expected additional FDR-level downstream gene.

Predicted `n_degs`: **1**
