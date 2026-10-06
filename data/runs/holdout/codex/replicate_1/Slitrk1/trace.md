# Slitrk1 direct n_degs forecast

## Declared target and endpoint

- Target: `Slitrk1`, from the one-row declared manifest.
- Cell class: `151 TH Prkcd Grin2c Glut`.
- Endpoint: `n_degs`, the count of measured genes in that focal class with BH-adjusted Wilcoxon `pvals_adj < 0.05`.
- Declared direct measurements used:
  - `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
  - `[local file: training_de_all_cell_groups.parquet]`
- Declared target biology used:
  - `[local file: Slitrk1.json]`
  - canonical bundle SHA-256 `a3ec8970fb830399879dd525131208cdfd2db75c18a0774760ce1e7dff411ec2`

## Target biology

The canonical `Slitrk1` biology bundle was served in the `biology` view; its serving metadata reported `target_outcome_exposed=false` and `labeled_neighbors_exposed=false`.

The focal non-target expression reach is high: `Slitrk1` is detected in 20,550 of 23,679 non-target `151 TH Prkcd Grin2c Glut` nuclei, 86.7858%, with mean raw UMI 3.1139 and mean log1p CP10K 0.9440. Thus the focal thalamic population is not a target-absence case.

The functional-stock card calls SLITRK1 a dynamic postsynaptic adhesion component whose extracellular LRR domains interact with presynaptic LAR-family receptor phosphatases. Its adjudication is that new SLITRK1 production should stop after disruptive editing and that the operative synaptic pool is `likely_substantially_depleted` by P37-P44. The best timing evidence in the bundle is adult hippocampal conditional Slitrk1 loss, where reduced SLITRK1 puncta and synaptic changes were observed two to three weeks after deletion. The same card also flags imperfect transfer to thalamus and subset-restricted thalamic expression in the anatomical literature, so this is a realized synaptic perturbation prior, not a prior for a broad RNA state.

## Training counts in the focal class

The focal-class training count table has 1,674 measured training perturbations:

- 1,205/1,674 are zero-DEG perturbations, 72.0%.
- 276/1,674 have exactly one DEG, 16.5%.
- 1,512/1,674 have two or fewer DEGs, 90.3%.
- The median is 0 and the 75th percentile is 1; the high tail is dominated by global RNA-processing, chromatin, proteasome, and homeostatic regulators rather than synaptic adhesion genes.

Given SLITRK1's operation, the count table rows I treated as closest were postsynaptic adhesion, neurexin/neuroligin/LRRTM, LAR-family receptor-phosphatase, and postsynaptic scaffold perturbations:

| group | training targets and focal `n_degs` |
| --- | --- |
| LAR-family Slitrk partners | `Ptprd 0`, `Ptprf 0`; `Ptprs` was absent from the focal training table |
| LRRTM/neurexin/neuroligin axis | `Lrrtm1 1`, `Lrrtm3 0`, `Lrrtm4 0`, `Nlgn3 1`, `Nrxn1 1`, `Nrxn2 0`, `Nrxn3 0` |
| Other synaptic adhesion or glutamatergic synapse organizers | `Adam22 1`, `Cadm2 1`, `Grid1 1`, `Grid2 0` |
| PSD scaffolds | `Dlg4 1`, `Shank2 0`, `Shank3 2` |

Across those 16 measured analogs, the exact focal counts were eight zeros, seven ones, and one two, for a mean count of 0.5625 and no comparator above 2 DEGs.

## Parquet profile check

I compared the 16 biologically selected training perturbations in the declared parquet, filtered to `151 TH Prkcd Grin2c Glut`, with `logfoldchanges` as the signed value and `pvals_adj < 0.05` as the significance definition. The comparison wrote run-local profile artifacts under `profile/` and found all 16 profiles available.

The node-level focal activity from the profile inspection matched the count table exactly:

- 8/16 analogs had `no_significant_features`.
- 8/16 had `1_to_9_significant_features`; in practice these were all 1 except `Shank3`, which had 2.

The significant rows in the selected cohort were:

| perturbed target | significant measured gene(s) at BH 0.05 |
| --- | --- |
| `Adam22` | `Adam22`, logFC -0.5502 |
| `Cadm2` | `Cadm2`, logFC -0.7574 |
| `Dlg4` | `Dlg4`, logFC -0.4444 |
| `Grid1` | `Grid1`, logFC -0.4875 |
| `Lrrtm1` | `R3hdm2`, logFC +0.2830 |
| `Nlgn3` | `Nlgn3`, logFC -0.8956 |
| `Nrxn1` | `Nrxn1`, logFC -0.5183 |
| `Shank3` | `Uba5`, logFC +0.4186; `Shank3`, logFC -0.2725 |

Thus the one-DEG analogs were mostly self-transcript calls, not broad downstream programs, and the cohort had no recurring positive or negative significant program overlap among the selected synaptic perturbations.

## Forecast

`Slitrk1` is strongly expressed in the focal nuclei and the biology bundle supports within-window depletion of functional SLITRK1, so I did not choose the global zero mode purely from baseline sparsity. However, SLITRK1 is a local postsynaptic adhesion organizer, its LAR-family receptor-phosphatase partners are quiet in the same focal endpoint, and nearby synaptic adhesion/scaffold perturbations almost never exceed the self-transcript-only regime.

I therefore placed the point at the low end of the analog distribution, with one possible significant row rather than a multi-gene trans response.

Predicted `n_degs`: 1
