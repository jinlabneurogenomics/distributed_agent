# Direct forecast for Lyst in 151 TH Prkcd Grin2c Glut

## Endpoint

- Target: `Lyst`, from the one-row holdout manifest.
- Endpoint: `n_degs`, the number of measured genes in `151 TH Prkcd Grin2c Glut` with BH-adjusted Wilcoxon `pvals_adj < 0.05`.
- Declared training table: 1,674 other perturbations for this class; `Lyst` is absent.

## Evidence used

### Training-count baseline

The declared 151-count table is strongly concentrated at zero:

- 1,205 / 1,674 training perturbations have `n_degs = 0`.
- The median is 0; the 75th percentile is 1; the 90th percentile is 2.
- Only a small right tail produces the class-wide mean of 14.1, with large outliers such as `Uba5`, `Tpr`, `Sin3a`, `Psmb4`, `Rab7`, and proteostasis/RNA-processing genes.

This makes 0 the prior mode and makes a multi-dozen or multi-hundred forecast require a close biological analogue or a clear stress-state argument.

### Held-out Lyst biology

The declared biology-only `Lyst` bundle supports reach but weakens short-window transfer:

- `Lyst` is measured in the focal non-target nuclei and is not absent from the class: 13,941 / 23,679 cells express it, mean raw UMI is 0.993, and mean CP10K is 0.629.
- LYST acts in lysosomal and autolysosomal fission/scission, a repeated organelle-remodeling process, so newly synthesized protein could matter after editing.
- Functional stock by harvest is adjudicated as indeterminate: an edit should stop new LYST supply, but pre-edit LYST is not directly destroyed; no target-specific neuronal half-life is known.
- Mouse neural loss phenotypes are late and mostly non-thalamic: germline or null models show progressive cerebellar/peripheral neural disease on a months scale, not a demonstrated P16-to-P37/P44 thalamic nuclear-RNA response.

Together, these make a material response possible but do not by themselves justify overriding the 151 zero mode.

### Training analogues

I nominated training-available analogues with the declared mouse annotation store and the selected same-experiment corpus release. This found no exact complex/paralog, reciprocal corpus comparator, narrow-module, or direct-interaction/dependency nominees for `Lyst`; all 1,097 eligible nominees were only `broad_functional_fallback` GO-style relationships.

The broad endolysosomal and organelle-trafficking fallbacks in the 151 parquet slice were mostly silent:

| target | role in reasoning | 151 `n_degs` |
|---|---:|---:|
| `Ap3b1` | top broad melanosome/lysosome fallback | 0 |
| `Dtnbp1` | melanosome fallback | 0 |
| `Gnptab` | lysosomal-enzyme trafficking fallback | 0 |
| `Becn1` | autophagy/lysosome fallback | 0 |
| `Nbea` | BEACH-domain family member noted in the `Lyst` card, but only a broad cytosol/nucleoplasm nominee | 0 |
| `Atg5` | autophagy fallback | 0 |
| `Atg16l1` | autophagy fallback | 0 |
| `Lamp2` | lysosome fallback | 0 |
| `Vps41` | HOPS/endolysosomal fallback | 0 |
| `Ppt1` | lysosomal fallback; self transcript only | 1 |
| `Sqstm1` | autophagy fallback; self transcript only | 1 |
| `Tmem106b` | lysosome-organization fallback; self transcript only | 1 |
| `Atp6ap2` | V-ATPase/lysosome fallback | 2 |
| `Vcp` | endosome-to-lysosome GO fallback | 2 |
| `Mtor` | lysosome/autophagy signaling fallback | 2 |
| `Vps35` | retromer/lysosome fallback | 17 |
| `Rab7` | proximal late-endosome stress positive control, not a direct LYST analogue | 501 |

`Rab7` was the main upward counterexample, but the same-experiment corpus places it as a direct late-endosomal/lysosomal compensation responder with V-ATPase, hydrolase, Lamp2, and sterol/lipid induction. The `Ap3b1` corpus contrast explicitly states that `Ap3b1` stayed flat while `Rab7`, `Becn1`, `Vps41`, and `Atp6v1a` had nonzero FDR<0.10 surfaces, showing both that the assay can see Rab7/HOPS/autophagy stress and that AP-3/lysosome-adjacent biology does not automatically phenocopy it.

### Self-transcript uncertainty

In the exact 151 parquet rows, 319 training perturbations had a significant self-target transcript row; many one-DEG outcomes are self-only. A one-count `Lyst` outcome is therefore plausible. However, the dataset portrait warns that measured target-mRNA reduction is not a reliable edit-efficiency or functional-effect measure, and the held-out bundle contains no calibrated self-knockdown probability or `Lyst` signature. Baseline expression reach alone was not enough to move the point estimate from the zero downstream-response mode to 1.

## Prediction

I predict `Lyst` will be transcriptionally quiet in the assayed thalamic glutamatergic class at BH FDR < 0.05.

Point prediction: `0`
