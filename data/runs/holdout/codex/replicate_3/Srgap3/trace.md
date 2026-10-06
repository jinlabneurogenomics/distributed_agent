# Srgap3 `n_degs` forecast

## Target and focal population

- Manifest target: `Srgap3`.
- Cell class: `151 TH Prkcd Grin2c Glut`.
- Endpoint: count of measured genes with BH-adjusted Wilcoxon `p < 0.05` in the perturbation-vs-matched-control contrast for this cell class.

## Biology used

The declared biology bundle maps the packet label `Srgap3` to the identifier-matched mouse `Srgap2` locus, encoding an F-BAR/RhoGAP/SH3 postsynaptic membrane-remodeling protein. The exact focal-population expression measurement in non-target nuclei was present but sparse: 7,313 of 23,679 nuclei expressed the feature, with 30.8839% expressing, mean raw UMI 0.4431, mean CP10K 0.2708, mean log1p CP10K 0.1847, and pseudobulk CPM 27.7729.

Functional realization by the P37-P44 harvest is biologically plausible: the curated card judged functional stock `likely_substantially_depleted`, based mainly on the fact that acute Srgap2 knockdown in postmitotic mouse cortical neurons changed spine morphology within 9-10 days, while the atlas edit-to-harvest interval is 21-28 days. The remaining uncertainty is context transfer rather than knockout realization: the direct loss phenotypes are cortical or cultured postmitotic neurons, not the aggregate thalamic `151 TH Prkcd Grin2c Glut` population, and no same-context compensation test for `Srgap1`/current-symbol `Srgap3` was available.

## Training-table scale

The declared `151 TH Prkcd Grin2c Glut` count table contains 1,674 training targets. Its `n_degs` distribution is zero-inflated and long-tailed:

| quantity | value |
|---|---:|
| targets with `n_degs = 0` | 1,205 / 1,674 |
| median | 0 |
| 75th percentile | 1 |
| 90th percentile | 2 |
| 95th percentile | 18 |
| maximum | 2,677 |

A direct scan of the same focal population in `training_de_all_cell_groups.parquet` gave the same mean count, 14.0538, and showed that 1,442 / 1,674 targets had zero significant non-self genes after excluding any significant row whose `names` equaled `gene_target`. Thus a one-DEG value for many neuronal genes is only target-transcript loss and does not imply a downstream thalamic state.

## Closest measured perturbations

I interpreted Srgap3 as a postsynaptic/cytoskeletal Rho-family regulator and therefore weighted RhoGAP/RhoGEF, Rac/Cdc42/Pak, Slit/Robo guidance, and excitatory synapse scaffold genes most heavily.

| comparator set in the training table | `n_degs` pattern in `151 TH Prkcd Grin2c Glut` |
|---|---|
| Rho/cytoskeletal and Slit-Robo genes: `Arhgap32`, `Arhgef9`, `Baiap2`, `Cdc42`, `Dock3`, `Fyn`, `Kalrn`, `Pak1`, `Pak2`, `Pak3`, `Rac1`, `Robo1`, `Robo2`, `Slit2`, `Actn4` | 11/15 were 0; `Arhgef9`, `Cdc42`, `Pak1`, and `Robo1` were 1, each from the perturbed transcript itself with 0 non-self DEGs |
| Postsynaptic scaffold and NMDAR subunit genes: `Dlg4`, `Shank2`, `Shank3`, `Syngap1`, `Grin2a` | `Shank2` and `Syngap1` were 0; `Dlg4` and `Grin2a` were self-only 1; `Shank3` was 2 with only 1 non-self DEG |
| Calcium/MAPK/NMDAR exceptions used as an upper-bound check: `Ppp3ca`, `Ppp3r1`, `Map2k1`, `Grin1` | 4, 9, 4, and 89 DEGs respectively |

The upper-bound genes are less transferable to Srgap3 because `Grin1` is an obligatory ionotropic receptor subunit and the calcineurin/MAPK genes have direct activity-dependent signaling roles. The more transferable cytoskeletal and guidance comparators were almost entirely transcriptionally quiet in this class.

## Synthesis

The target is probably engaged and expressed in enough recovered thalamic neurons for a local synaptic effect to exist, but its expression reach is partial and the closest observed loss-of-function perturbations rarely produced any significant non-self genes in the requested aggregate class. The forecast therefore stays at the bottom of the training distribution. I assign no extra DEG for self-transcript detection because Srgap3/SRGAP2 is lowly and sparsely expressed in this population and the atlas-wide self-transcript readout is not a reliable editing-strength proxy.

Point prediction: `0`.
