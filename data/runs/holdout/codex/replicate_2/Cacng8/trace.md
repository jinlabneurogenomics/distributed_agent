# Direct n_degs forecast for Cacng8

## Declared target and endpoint

- Target: `Cacng8`
- Cell group: `151 TH Prkcd Grin2c Glut`
- Endpoint: `n_degs`, the count of measured genes with BH-adjusted Wilcoxon `p < 0.05` in this thalamic glutamatergic class.

## Evidence used

### Cacng8 biology bundle

The canonical held-out bundle supports real biology but only moderate visibility for this endpoint:

- `Cacng8` encodes TARP gamma-8, an AMPA-receptor auxiliary membrane component that regulates receptor abundance, extrasynaptic surface localization, synaptic transmission, and plasticity.
- The functional stock card adjudicates gamma-8 as a dynamic complex component whose operative stock is `likely_substantially_depleted` by P37-P44 after a P16 disruptive edit, but the evidence is partial because no Cacng8-specific turnover measurement in thalamic neurons was found.
- Prior mouse loss phenotypes are hippocampal/prefrontal or behavioral germline observations, not a direct postnatal thalamic CRISPR measurement.
- Exact focal-population reach is modest rather than absent: in non-target nuclei from `151 TH Prkcd Grin2c Glut`, `Cacng8` is detected in 10,129/23,679 nuclei, with 42.776% expressing, mean CP10K 0.526, mean raw UMI 0.858, and pseudobulk CPM 53.794.

### Training-count distribution

The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` table is strongly zero-inflated:

- 1,674 observed training targets.
- 1,205/1,674 have `n_degs = 0`.
- Median `n_degs = 0`, 75th percentile = 1, 90th percentile = 2, 95th percentile = 18.
- Only 43/1,674 targets have 100 or more DEGs.

### Same-class measured AMPAR/TARP comparators

The closest functional perturbations present in the 151-class training table are at the endpoint floor:

| target | `n_degs` in 151 TH Prkcd Grin2c Glut |
| --- | ---: |
| `Cacng2` | 0 |
| `Cacng3` | 0 |
| `Gria1` | 0 |
| `Gria2` | 0 |
| `Gria3` | 0 |
| `Dlg4` | 1 |
| `Dlgap4` | 2 |
| `Camk2a` | 0 |
| `Camk2b` | 1 |

The same-class Parquet rows confirmed that each of these selected observed nodes had 17,259 measured features in this class. The exact significant-feature counts were 0 for `Cacng2`, 0 for `Cacng3`, 0 for `Gria1`, 0 for `Gria2`, 0 for `Gria3`, 1 for `Dlg4`, 2 for `Dlgap4`, 0 for `Camk2a`, and 1 for `Camk2b`; `Dlg4` and `Camk2b` only crossed FDR through their own target transcripts. In the same scan, the matched recovered perturbed-nucleus counts were within the typical range for these low-count calls: 143 for `Cacng2`, 149 for `Cacng3`, 174 for `Gria1`, 157 for `Gria2`, 132 for `Gria3`, 273 for `Dlg4`, and 262 for `Dlgap4`, all against the same 23,679 matched controls.

### Positive local contrasts

The flat AMPAR/TARP pattern is not a universal failure of thalamic receptor perturbations:

| target | 151-class `n_degs` | interpretation |
| --- | ---: | --- |
| `Grin1` | 89 | strong positive NMDAR contrast; 49 down and 40 up in the Parquet inspection |
| `Grin2a` | 1 | self-transcript only |
| `Grin2b` | 2 | self-transcript plus one downstream gene |
| `Cacna1g` | 12 | T-type calcium-channel perturbation with 11 downstream genes plus self |

These positives bound the forecast upward but are weaker magnitude donors for `Cacng8`: loss of an obligatory NMDAR pore subunit is more directly coupled to calcium-dependent nuclear signaling than loss of a TARP auxiliary AMPAR-trafficking subunit, and `Cacna1g` is a thalamic excitability channel rather than an AMPAR auxiliary component.

### Same-experiment corpus context

The selected same-experiment corpus had no Cacng8 Findings or Claims, so it did not provide target-outcome information. It did provide consistent interpretation for the observed relatives: packaged Findings describe `Cacng2` as having no robust downstream transcriptional response and no AMPAR/TARP/BDNF/immediate-early mRNA rebound, `Cacng3` as a pan-null transcriptional perturbation without AMPAR, TARP-paralog, PSD-scaffold, or activity-regulated feedback induction, `Dlg4` as globally flat at the downstream snRNA level, and `Gria1` as broadly buffered in the nuclear transcriptome.

## Synthesis

I treated Cacng8 as biologically real and probably functionally depleted by harvest rather than as an unreachable edit. Its exact expression in the focal class also makes a response possible. The point forecast is still at the zero mode because the direct local analogues are not NMDAR-like transcriptional triggers in this assay: `Cacng2` and `Cacng3` are the closest TARP relatives and both have zero 151-class DEGs, the represented AMPAR pore genes `Gria1`/`Gria2`/`Gria3` are also zero, and the PSD scaffold `Dlg4` contributes only one self hit. Cacng8 could in principle be stronger than Cacng2/Cacng3 because hippocampal gamma-8 loss has clear AMPAR phenotypes and the thalamic population expresses the transcript in 42.8% of control nuclei, but the biological effect is expected to be receptor trafficking and synaptic physiology, not a broad autonomous nuclear RNA program, and expression in less than half of the aggregated thalamic population should further dilute a cell-state signature.

Predicted `n_degs`: 0
