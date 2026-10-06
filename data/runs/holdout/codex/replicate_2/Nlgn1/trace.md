# Nlgn1 focal DEG-count forecast

## Endpoint and target

- **Target:** `Nlgn1`, from the declared one-row holdout manifest.
- **Endpoint:** `n_degs` in `151 TH Prkcd Grin2c Glut`, defined as the number of measured genes with BH-adjusted Wilcoxon `p < 0.05`.
- **Prediction:** `1`.

## Evidence used

### Biology-only target bundle

The declared `Nlgn1` bundle establishes that this is a reachable acute postnatal loss-of-function perturbation in the focal assay context, not a target that is absent from thalamic nuclei.

- The exact in-assay non-target expression measurement for `151 TH Prkcd Grin2c Glut` reports `Nlgn1` in 10,867 of 23,679 non-target nuclei, with 45.893% of nuclei expressing the feature, mean raw UMI 0.714, mean log1p CP10K 0.297, and pseudobulk CPM 44.73.
- The functional-stock card judges NLGN1 likely substantially depleted by the P37-P44 harvest: disruptive editing stops new full-length surface NLGN1 supply; the postsynaptic pool exchanges on an hour scale or can be proteolytically removed; and mature CA1 deletion at P21 produced loss of an NLGN1-dependent function after 2-3 weeks, within the Perturb-seq elapsed window.
- The same card qualifies the transfer: the closest loss evidence is hippocampal CA1 electrophysiology rather than thalamic nuclear RNA, so it supports target realization more than a broad transcriptomic endpoint.

### Training counts in the same focal class

The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` table is sparse:

- 1,205 / 1,674 training perturbations have `n_degs = 0`.
- The median is 0; the 75th percentile is 1; only 106 / 1,674 have at least 10 DEGs.
- The biologically nearest represented synaptic-adhesion/scaffold candidates are almost all null or singletons in this class:
  - `Nlgn3`: 1
  - `Nrxn1`: 1
  - `Nrxn2`: 0
  - `Nrxn3`: 0
  - `Lrrtm1`: 1
  - `Lrrtm3`: 0
  - `Lrrtm4`: 0
  - `Dlg4`: 1
  - `Shank2`: 0
  - `Shank3`: 2
  - `Grid2`: 0

The direct Parquet query of `training_de_all_cell_groups.parquet` in the exact focal group showed that several one-DEG anchors were self-transcript-only events rather than downstream programs: `Nlgn3`, `Nrxn1`, `Dlg4`, `Adgrl3`, `Cpe`, `Grin2a`, `Grm1`, and `Grik5` each had a single significant row matching the perturbed target itself. `Lrrtm1` instead had one downstream row, `R3hdm2`, at adjusted `p = 0.0269`; `Shank3` and `Dlgap4` had two rows. I did not use these as hidden `Nlgn1` observations; they are all training perturbations.

### Typed analogs and same-experiment corpus interpretation

The annotation-based analog nomination placed `Nlgn3`, `Dlg4`, `Nrxn1`, `Nrxn2`, `Nrxn3`, `Lrrtm1`, `Lrrtm3`, `Lrrtm4`, `Shank2`, and `Shank3` in the leading synaptic adhesion / neurexin-neuroligin / PSD inspection set through Reactome, STRING-physical, projected complex, and narrower synaptic annotations. That nominated a biologically sensible transfer set but did not provide an endpoint rank.

The same-experiment corpus for those training anchors agreed with the measured counts:

- `Nlgn3` produced no downstream FDR<0.10 genes across all recovered neuronal groups, and its literature-obvious neighbors were also flat or sparse.
- `Lrrtm1` produced an almost entirely buffered response, one downstream DEG across 371,796 downstream tests in 22 measured neuronal groups; its only focal DEG was `R3hdm2`.
- `Nrxn1` produced a one-gene phenotype outside this thalamic class and a self-down / no-downstream pattern in several neuronal groups.
- Higher-order corpus Claims summarized represented synaptic adhesion and postsynaptic scaffold perturbations as largely buffered or off-axis in the postnatal neuronal nuclear transcriptome, lacking a broad shared downstream module.

The report/corpus layer and the Parquet are two views of the same experiment, so I used the reports to interpret which analog signatures were self-only, flat, or downstream-singleton rather than as independent confirmation.

### Profile check in the focal Parquet rows

I compared a 40-gene, annotation-nominated synaptic cohort in the exact `151 TH Prkcd Grin2c Glut` Parquet rows using signed Wilcoxon scores. The comparison had 25 / 40 genes with no significant features, 13 / 40 with 1-9 significant features, and only 2 / 40 with at least 50. Across all 780 pairwise comparisons in the cohort, the median positive top-tail overlap was 0.01, the median negative top-tail overlap was 0.01, and the significant-program overlap median was zero in both directions.

This supports the specific transfer: `Nlgn1` is close to a local synaptic adhesion/scaffold subnetwork whose loss is often functionally real but largely invisible to a steady-state somatic snRNA response. Large focal counts such as `Tpr = 1768` and `Grin1 = 89` came from nuclear-transport or receptor perturbations with different measured programs, not from the neuroligin/neurexin/LRRTM adhesion core.

## Synthesis

`Nlgn1` should be edited in cells that express it and the existing NLGN1 surface pool should turn over within the experimental window, so a complete null forecast is too low. But the closest represented adhesion genes and postsynaptic scaffolds repeatedly produced zero or one focal significant rows, with the one rows often explained by target-mRNA depletion itself rather than a downstream state. Because `Nlgn1` is expressed strongly enough in the focal non-target population to make a self row plausible, while its mature-neuron phenotype is expected to be local synaptic physiology or protein organization rather than a large nuclear RNA module, I predict a singleton focal DEG count.
