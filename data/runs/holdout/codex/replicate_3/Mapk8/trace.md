# Evidence and forecast for `151 TH Prkcd Grin2c Glut`

## Target

- Held-out manifest target: `Mapk8`.
- Endpoint to predict: `n_degs`, the number of measured genes with BH-adjusted Wilcoxon `p < 0.05` in `151 TH Prkcd Grin2c Glut`.

## Evidence used

1. **Biology-only Mapk8 bundle**
   - The declared canonical bundle reports that Mapk8 is measured in the focal non-target thalamic population and is broadly detectable: mean log1p CP10K 0.676 and 18,740 / 23,679 nuclei expressing, or 79.1%.
   - The functional-stock card calls MAPK8/JNK1 a soluble, renewable kinase whose supply should stop after disruptive editing; over the P16 to P37-P44 interval, functional stock is therefore likely substantially depleted, but the card flags only partial evidence because no target-specific neuronal half-life or residual-activity threshold was available.
   - The source evidence supports a mouse neural role and family redundancy: constitutive Mapk8/Jnk1 loss has adult hippocampal spine and spatial-learning phenotypes despite Mapk9/Mapk10 paralogs, but those data are hippocampal, constitutive, and long-window rather than an acute juvenile thalamic snRNA-seq endpoint.

2. **Matched 151-class training count table**
   - The exact training table contains 1,674 measured perturbations for this endpoint.
   - The endpoint is strongly zero-inflated: 1,205 / 1,674 targets have `n_degs = 0`; 1,481 / 1,674 have `n_degs <= 1`.
   - Represented MAPK/JNK-adjacent perturbations in the same endpoint were quiet:
     - `Mapk9`: 0
     - `Mapk1`: 0
     - `Map2k2`: 0
     - `Map2k6`: 0
     - `Map3k7`: 0
     - `Pak2`: 0
     - `Pak3`: 0
     - `Rac1`: 0
     - `Jund`: 0
     - `Cdc42`: 1
     - `Pak1`: 1
     - `Mef2c`: 1
     - `Shoc2`: 1
     - `Braf`: 4
     - `Map2k1`: 4
     - `Mef2a`: 4

3. **Observed-profile checks in the matched thalamic class**
   - I projected the represented MAPK/JNK-related nodes `Mapk9`, `Mapk1`, `Map2k1`, `Map2k2`, `Map2k6`, `Map3k7`, `Mef2a`, and `Mef2c` in `151 TH Prkcd Grin2c Glut`.
   - Five of the eight had no significant profile features at `pvals_adj < 0.05`; `Map2k1` and `Mef2a` had four and `Mef2c` had one.
   - The profile-neighborhood union was broad rather than a tight family module, so these weak MAPK/JNK reference profiles did not provide a coherent high-DEG analogue.

4. **Packaged same-experiment corpus interpretations**
   - The Mapk9 report describes single JNK2 loss as FDR-silent across every recovered neuronal class at the experiment's reporting threshold, with canonical AP-1/immediate-early, apoptosis, and FoxO/autophagy transcript proxies absent.
   - The Mapk1 report similarly interprets ERK2 loss as transcriptomically buffered, with represented Braf/Map2k1 showing only a small thalamic branch and most broader Ras/MAPK neighbors flat.
   - The Map3k7 report places the TAK1-to-NF-kappaB/JNK/p38 axis among represented basal neuronal modules that were transcriptionally silent.

## Synthesis

Mapk8 is a real, expressed, likely realized perturbation rather than an invisible target, so the forecast should not be a technical null by fiat. The relevant biological operation is a single JNK-family kinase loss in unstimulated postnatal neurons, however, and the closest measured endpoint evidence points downward: `Mapk9`, upstream `Map3k7`, p38-side `Map2k6`, ERK2 `Mapk1`, MEK2 `Map2k2`, and Rho/JNK-adjacent cytoskeletal inputs were all exactly zero in the same thalamic count table. The only local Ras/MAPK positives, `Braf` and `Map2k1`, were four-gene 151-class responses and belong to a narrow ERK-linked thalamic branch rather than to a broad stress-JNK module.

Those data make a very small Mapk8 response plausible, but the modal outcome for both the local training distribution and the represented JNK/MAPK comparators is zero. I therefore choose the zero-count mode as the integer point forecast.

`predicted_n_degs = 0`
