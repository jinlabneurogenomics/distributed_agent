# Kmt5b DEG-count forecast

## Declared target and endpoint

- **Target:** `Kmt5b`, from the one-row holdout manifest.
- **Population:** `151 TH Prkcd Grin2c Glut`.
- **Endpoint:** `n_degs`, measured genes with Wilcoxon BH-adjusted `p < 0.05`.
- **Point prediction:** **18**.

## Evidence used

The target biology bundle shows that `Kmt5b` is present in the focal assay context rather than absent or unreachable. In matched non-target `151 TH Prkcd Grin2c Glut` nuclei, `Kmt5b` RNA was detected in 15,633 of 23,679 nuclei, 66.02%, with mean raw UMI 1.201 and pseudobulk CPM 75.29. Its card adjudicates the operative enzyme plus renewable H4K20me2-marked chromatin stock as **likely substantially depleted** by the P37-P44 harvest: juvenile mouse PFC Kmt5b shRNA reduces KMT5B protein and H4K20me2 within 14-20 days, whereas the declared Perturb-seq interval is 21-28 days.

That made a complete null less plausible than the screen-wide median of 0, but not enough to put `Kmt5b` in the very large chromatin-regulator tail. The same card also gives reasons to shrink the forecast: the installed H4K20 mark initially persists on pre-edit nucleosomes, canonical histones can be long lived, `Kmt5c` and `Nsd2` may retain overlapping H4K20 chemistry, and the direct timing evidence is PFC shRNA rather than sparse thalamic CRISPR.

From the declared 151-class training count table:

| perturbation | relevant interpretation | `n_degs` |
|---|---:|---:|
| `Nsd2` | proposed alternative H4K20 dimethylating enzyme | 0 |
| `Kmt2c` | lysine methyltransferase, low focal response | 0 |
| `Setd2` | lysine methyltransferase, low focal response | 1 |
| `Ash1l` | lysine methyltransferase, low focal response | 1 |
| `Ehmt1` | lysine methyltransferase, low focal response | 4 |
| `Setd5` | chromatin/NDD regulator with small response | 9 |
| `Setdb1` | histone lysine methyltransferase | 22 |
| `Nsd1` | NSD-family histone lysine methyltransferase | 23 |
| `Kmt2a` | histone lysine methyltransferase | 24 |
| `Chd8` | ASD chromatin regulator, moderate upper comparator | 61 |

This deliberately brackets `Kmt5b` with H4K20-adjacent or histone-methylation perturbations first, then uses `Chd8` as a moderate NDD/chromatin upper comparator. The selected set has median 6.5, mean 14.5, and a one-from-each-tail trimmed mean 10.5. Larger remodeler/cofactor perturbations in the same population were much higher, for example `Chd4` 100, `Smarcc2` 185, `Brd4` 311, `Setd1a` 368, and `Sin3a` 1433, but their transcriptional and remodeling roles are broader than KMT5B's H4K20 methyltransferase operation.

I used the expression Parquet to confirm that these analogs were directly measured in the same matched class and to inspect their signed profiles. Each queried analog had all 17,259 measured features in `151 TH Prkcd Grin2c Glut` with matched control size 23,679 and perturbation matched counts from 55 to 207. The profile comparison showed `Nsd2` and `Kmt2c` as no-significant-feature perturbations, `Setd2`/`Ash1l`/`Ehmt1`/`Setd5` as 1-9 DEG perturbations, `Kmt2a`/`Nsd1`/`Setdb1` as 22-24 DEG perturbations, and `Chd8` as a 61 DEG perturbation. The broader high-burden regulators formed the expected upper tail but were not used as a numeric center.

## Synthesis

The prediction is above the near-zero H4K20-adjacent `Nsd2` result because the held-out target is itself well expressed in the focal thalamic population and external juvenile-neuron evidence supports measurable KMT5B/H4K20me2 loss within the harvest window. It is below `Setd1a`, `Brd4`, `Smarcc2`, `Chd4`, and `Sin3a` because KMT5B has partial persistence of the installed chromatin mark and plausible residual family activity rather than immediate loss of a central transcriptional cofactor or remodeler.

I placed the point estimate in the small, nonzero methyltransferase band defined by `Setdb1`, `Nsd1`, and `Kmt2a`, with a slight shrinkage toward the lower direct analogs. That yields **18 DEGs**.
