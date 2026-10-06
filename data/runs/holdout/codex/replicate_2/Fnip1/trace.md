# Fnip1 direct DEG-count forecast

Target and endpoint:

- Target: `Fnip1`
- Cell group: `151 TH Prkcd Grin2c Glut`
- Endpoint: number of measured genes with BH-adjusted Wilcoxon `p < 0.05`

Allowed target biology and reach:

- The one-row manifest and the canonical biology bundle both resolve to `Fnip1`.
- The exact in-assay non-target expression measurement shows that `Fnip1` is reachable in the focal population: 17,909 of 23,679 non-target nuclei expressed it, `pct_cells_expressing = 75.6324`, `mean_raw_umi = 1.6156`, and `pseudobulk_cpm = 101.2533`.
- The functional-stock card is indeterminate for the P16-to-P37/P44 window. A disruptive edit is expected to stop new FNIP1 synthesis, and FNIP1 is a dynamic component of FLCN/AMPK and Hsp90-associated complexes, but no postmitotic thalamic-neuron measurement establishes FNIP1 protein or complex depletion kinetics over 21-28 days.
- The source card named `Flcn` and `Fnip2` as the closest biology. `Fnip2` has experimentally supported overlap with `Fnip1` in some non-neural tissues, but no compensation test exists in juvenile thalamic neurons. Neither `Flcn` nor `Fnip2` is present in the declared focal training count table.

Training-count context:

- The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` has 1,674 training perturbations and excludes `Fnip1`.
- The focal endpoint is sparse: 1,205 of 1,674 training targets have 0 DEGs; the median is 0, the 75th percentile is 1, and the 95th percentile is 18. The mean is 14.054 only because of a long high-response tail.
- Literal AMPK/mTOR/FLCN-adjacent training comparators in the same count table are mostly near zero at BH < 0.05:

| target | n_degs in `151 TH Prkcd Grin2c Glut` |
|---|---:|
| `Mtor` | 2 |
| `Prkaa2` | 0 |
| `Prkag2` | 0 |
| `Rptor` | 0 |
| `Akt3` | 0 |
| `Pik3cb` | 0 |
| `Pik3r1` | 0 |
| `Pik3r2` | 0 |
| `Fkbp1a` | 1 |
| `Depdc5` | 13 |
| `Srebf2` | 7 |
| `Tsc2` | 86 |

Focal Parquet checks:

- Direct Parquet aggregation in the focal class reproduced the count-table values for the candidate comparators above.
- `Tsc2` is the clearest pathway-adjacent responder, with 86 BH<0.05 genes in the focal class, including sterol and feedback markers such as `Cyp51`, `Pik3r3`, `Slc2a6`, `Fads6`, `Dusp1`, `Slc16a1`, and `Nsdhl`.
- The `Tsc2` contrast did not make the closest Fnip/FLCN module a strong focal signature: in the focal class, `Fnip1` itself was up only subthreshold after `Tsc2` perturbation (`logfoldchanges = 0.23597`, `pvals_adj = 0.53892`), `Fnip2` was also subthreshold (`pvals_adj = 0.66161`), and `Flcn` was essentially unchanged (`pvals_adj = 1.0`).
- `Mtor` had only two BH<0.05 focal genes, `Rims3` and `Tmed8`; `Rptor`, `Prkaa2`, and `Prkag2` were zero in the focal count table.

Packaged same-experiment corpus:

- The selected corpus release contains no packaged `Fnip1` target report or `Fnip1` claim, so the prediction did not use a same-experiment `Fnip1` signature.
- Reports for the nearest represented pathway nodes support the same interpretation as the count table: `Rptor` and `Prkaa2` were globally flat across recovered neuronal groups, `Prkag2` had only an isolated one-gene response outside the focal class, and `Mtor` produced a very small focal response. `Tsc2` is a detectable mTORC1/sterol/lysosomal disinhibition case, but the corpus explicitly treats core or upstream PI3K/AMPK/mTOR perturbations as buffered or non-phenocopying rather than interchangeable with the `Tsc2` state.

Synthesis:

`Fnip1` is well expressed, so a zero forecast is not based on target absence. The determinant evidence is that its direct complex partner/paralog are unavailable as training perturbations, the broader represented AMPK/mTOR core-loss comparators are mostly 0-2 DEGs in the exact focal endpoint, and the one stronger branch, `Tsc2`, is a negative-regulator loss that activates a sterol/lysosomal program rather than a close proxy for `Fnip1` loss. Because the biology bundle leaves FNIP1 stock depletion and same-context `Fnip2` buffering unresolved, I treat the detectable-expression prior as insufficient to lift the prediction out of the dominant sparse/null regime.

Point forecast: `0`
