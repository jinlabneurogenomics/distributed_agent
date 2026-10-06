## Target and endpoint

- Target: `Ophn1`, the single gene in the declared holdout manifest.
- Endpoint: `n_degs` in `151 TH Prkcd Grin2c Glut`, i.e. the count of measured genes with Wilcoxon BH-adjusted `p < 0.05` in the focal thalamic glutamatergic class.
- The declared training count table has 1,674 rows and does not contain `Ophn1`.
- The declared target biology bundle exposes no Ophn1 outcome: the served biology view reports `labeled_neighbors_exposed=false` and `target_outcome_exposed=false`.

## Evidence used

### Ophn1 biology and focal reach

The Ophn1 biology bundle places OPHN1 in localized Rho-family signaling and synaptic trafficking rather than in a core nuclear, ribosomal, proteasomal, or spliceosomal process:

- OPHN1 is a Rho-family GAP with activity toward RhoA/Rac1/Cdc42 and with F-actin, synapse-stabilization, and AMPAR-trafficking functions.
- The P16-to-P37/P44 interval is likely long enough for edited expressing neurons to lose a large fraction of functional OPHN1 stock: neuronal RNAi evidence showed OPHN1 protein loss and synaptic/spine effects within 2-8 days, whereas the screen harvests 21-28 days after perturbation.
- The exact focal-population expression measurement is positive but partial: `Ophn1` was detected in 11,715 of 23,679 non-target `151 TH Prkcd Grin2c Glut` nuclei, or 49.47%, with mean raw UMI 0.745 and mean CP10k 0.477.

I interpreted this as target engagement plausibly being biologically real in a subset of recovered thalamic cells, but not as evidence for a broad steady-state nuclear RNA state.

### Same-experiment corpus context

The packaged corpus had no Ophn1 Finding, Claim, or explicit comparator record, so there was no direct Ophn1 same-experiment report to reuse.

The closest represented Rho/Rac/Cdc42-axis reports instead bounded the expected scale downward:

- `Cdc42` had a high-confidence negative Finding: even with significant Cdc42 self-transcript reduction in `151 TH Prkcd Grin2c Glut`, there was no robust downstream transcriptional response in any recovered neuronal class.
- `Cdc42` also had a pathway-uncoupling Finding: 43 actin, Rho-effector, and synaptic transcripts had zero FDR<0.10 calls across 903 Cdc42 gene-by-cell-class tests.
- `Rac1` was annotated as transcriptionally buffered: 21 of 22 measured groups had no FDR<0.10 downstream gene, and the sole responder had only one gene.
- The Rac1 and Cdc42 reports both found that represented Rac/Cdc42/PAK/WRC/GEF/GAP relatives were flat or singleton responders rather than a shared nuclear mRNA module.

### Declared count table and focal Parquet rows

The declared count table is heavily concentrated at the null floor in this focal cell class:

- 1,205/1,674 training targets have `n_degs = 0`.
- 1,481/1,674 have `n_degs <= 1`.
- The median is 0 and the 75th percentile is 1.
- The large tail is dominated by unrelated housekeeping / RNA-processing / proteostasis perturbations, not by localized synaptic Rho-family signaling.

I selected the represented training perturbations closest to OPHN1 by operation or downstream pathway: RhoGAP/RhoGEF genes, Rac/Cdc42 and PAK/WAVE/LIMK pathway genes, AMPAR / PSD scaffolds, and endocytic or dynamin nodes connected to OPHN1 synaptic trafficking. Their focal-class counts were:

```tsv
target_name	n_degs
Arhgap18	0
Arhgap32	0
Arhgef9	1
Baiap2	0
Cdc42	1
Cfl2	0
Cyfip1	0
Cyfip2	1
Dlg4	1
Dnm1	1
Dock3	0
Ephb2	0
Fgd4	0
Fyn	0
Gria1	0
Gria2	0
Gria3	0
Kalrn	0
Limk1	0
Ocrl	0
Pak1	1
Pak2	0
Pak3	0
Rac1	0
Shank2	0
Shank3	2
Tiam1	0
```

The mean of this 27-node operational neighborhood is 0.30 DEGs and the median is 0. Directly querying the focal rows in `training_de_all_cell_groups.parquet` confirmed that each node had 17,259 measured genes in the focal contrast; 20/27 of the above nodes had no BH<0.05 feature, and the singletons for `Cdc42`, `Dlg4`, `Dnm1`, `Pak1`, `Arhgef9`, and `Cyfip2` were their own transcripts rather than a downstream module.

## Synthesis

The strongest upward evidence is that OPHN1 should be an operative protein loss by the screen harvest and that its transcript is measurably present in roughly half of focal non-target cells, so a self-transcript hit or a tiny downstream footprint is plausible.

The stronger downward evidence is endpoint-specific. Loss of closely related Rho/Rac/Cdc42, PAK/LIMK, PSD, AMPAR, and endocytic perturbations in the same experiment almost always landed at zero or only a self-transcript singleton in this thalamic class. Cdc42 is especially informative because its own transcript was significantly reduced in the focal class but the downstream actin/spine program still remained transcriptionally silent. OPHN1 is one step upstream as a localized GAP/scaffold, and partial focal expression further dilutes the expected Wilcoxon signal.

I therefore expect no robust BH<0.05 downstream program for `Ophn1` in `151 TH Prkcd Grin2c Glut`; uncertainty is mostly whether the Ophn1 self-transcript itself happens to cross FDR. Because observed target-mRNA loss is an unreliable and often absent consequence of these CRISPR perturbations, and because the local analog cohort has a median of zero, I set the point forecast to the focal null floor.

## Prediction

`Ophn1`: 0
