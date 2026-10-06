# Caly DEG-count prediction

Target: `Caly`

Focal population: `151 TH Prkcd Grin2c Glut`

Predicted `n_degs`: `1`

## Evidence used

- The canonical `Caly` biology bundle states that calcyon is a neuronal single-pass vesicular membrane protein that binds clathrin light chain and participates in clathrin/AP-linked cargo internalization and sorting. Germline loss perturbs hippocampal AMPA-receptor internalization/LTD and NRG1-ErbB4-linked signaling, so the target is not biologically inert, but those data are outside the P16 thalamic edit context and do not establish an induced-loss latency.
- Functional stock by harvest is indeterminate. A genome edit should stop new calcyon synthesis, but the bundle found no Caly-specific protein half-life, vesicular residence time, or acute deletion time course proving how much pre-edit calcyon is removed during the 21-28 day Perturb-seq window.
- Exact focal expression is favorable for detecting the transcript: in matched non-target `151 TH Prkcd Grin2c Glut` nuclei, `Caly` was detected in 20,881 of 23,679 cells, or 88.18%, with mean raw UMI 2.81 and pseudobulk CPM 176.11.
- The direct count table for this class contains 1,674 training perturbations. Its empirical mass is near zero: 1,205 targets had `n_degs = 0`, 276 had `n_degs = 1`, 31 had `n_degs = 2`, 59 had 3-10, and 103 had more than 10.
- I used the raw 151-class Parquet only for observed training genes chosen from the Caly mechanism. The closest measured clathrin/endocytic and receptor-pathway comparators were small:
  - `Cltc`: 3 DEGs
  - `Dnm1`: 1 DEG, the self transcript
  - `Synj1`: 1 DEG, the self transcript
  - `Ap3b1`: 0 DEGs
  - `Nrg1`: 0 DEGs
  - `Erbb4`: 0 DEGs
  - `Gria1`: 0 DEGs
  - `Gria2`: 0 DEGs
  - `Dlg4`: 1 DEG, the self transcript
  - `Bin1`: 1 DEG, the self transcript
  - `Syp`: 1 DEG, the self transcript
- This 11-target close comparator set has median 1 DEG and mean 0.73 DEGs. Adding larger boundary perturbations that act in late endosome/retromer, receptor signaling, or growth pathways left the median at 1 but made the mean unrepresentative: `Vps35` had 17 DEGs, `Rab7` had 501, `Grin1` had 89, and `Tsc2` had 86.
- Across all training perturbations in this class, one-DEG cases usually reflected self-transcript loss rather than a downstream program: 237 of 276 `n_degs = 1` targets had the perturbed gene itself as an FDR-significant row.

## Synthesis

The training distribution and the Caly-matched biology both argue against a large signature. Caly is a cargo-selective accessory membrane component, not a broad transcriptional, proteostasis, splicing, or core lysosomal factor like the high-burden training outliers. The AP/clathrin and synaptic receptor comparators were mostly transcriptionally quiet in the recovered thalamic nuclei, and the best boundary cases with broader signatures were mechanistically farther from Caly's limited clathrin-adaptor role.

I therefore placed the downstream component of the expected response at approximately zero. Because `Caly` itself is broadly detected in the focal cells, a one-gene count from the self transcript is more likely than a strict zero, while the functional-stock uncertainty and the quiet pathway comparators keep the prediction at a self-only-sized value.
