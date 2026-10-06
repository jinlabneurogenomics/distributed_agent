# Il10rb direct DEG-count forecast

## Target and endpoint

- **Target manifest:** `Il10rb`
- **Cell context:** `151 TH Prkcd Grin2c Glut`
- **Endpoint:** `n_degs`, the count of measured genes in the focal thalamic glutamatergic class with BH-adjusted Wilcoxon `p < 0.05`
- **Point forecast:** `0`

## Evidence used

### Outcome-blind Il10rb biology

The declared canonical biology bundle for `Il10rb` reported no target outcome and no labeled-neighbor outcomes. Its exact focal-population expression measurement showed that `Il10rb` is detectable but very sparse in non-target nuclei from `151 TH Prkcd Grin2c Glut`: 818/23,679 cells, 3.45% expressing, mean raw UMI 0.0395, mean CP10k 0.0258, and pseudobulk CPM 2.48.

The same bundle adjudicated IL10RB as a dynamic cell-surface accessory chain for class II cytokine receptor complexes. A disruptive edit should stop new IL10RB synthesis, and receptor complexes can traffic away from the surface, so some functional loss by the 21-28 day harvest is plausible. That depletion is uncertain rather than complete: pre-existing receptor protein can remain initially competent, ligand-triggered trafficking does not by itself prove irreversible degradation, IL10RB participates in multiple receptor pools, and the best neural loss phenotype in the bundle was from `Il10rb`-deficient transferred CD4 T cells after adult facial nerve axotomy rather than from healthy thalamic neurons.

I therefore treated `Il10rb` as a low-reach, only partially realized postmitotic neuronal perturbation. Sparse focal expression argues against a broad cell-autonomous transcriptional response, while the cytokine-receptor biology keeps a very small response possible.

### Training count table

The declared training count table for `151 TH Prkcd Grin2c Glut` contained 1,674 non-held-out perturbations. Its empirical distribution was highly zero-inflated:

| quantity | value |
| --- | ---: |
| zero-count perturbations | 1,205 / 1,674 |
| median `n_degs` | 0 |
| 75th percentile | 1 |
| 80th percentile | 1 |
| 90th percentile | 2 |
| 95th percentile | 18 |
| mean | 14.05 |

The mean is pulled upward by a small tail of very large perturbations, not by the typical target. For a lowly expressed cytokine-receptor target, the zero/marginal part of the distribution was the relevant baseline.

I then inspected biologically adjacent training perturbations named by the `Il10rb` biology bundle or by the same cytokine/interferon signaling neighborhood in the count table. The closest direct partner in the table, `Il10ra`, had `n_degs = 0`. `Atg16l1`, the IL10RB-trafficking related gene in the bundle, also had `0`; downstream or neighboring signaling perturbations were likewise quiet: `Stat3 = 0`, `Il6st = 0`, `Ifnar1 = 0`, `Ifnar2 = 0`, `Ifngr1 = 0`, `Ifngr2 = 0`, and `Nfkb1 = 0`. `Stat1` was the only member of the selected analog cohort with any FDR-significant feature, and it had only `1`.

### Focal expression-profile comparison

Using the declared all-cell-class DE Parquet restricted to `group_name == "151 TH Prkcd Grin2c Glut"`, I symmetrically compared the profiles of ten training analogs:

`Il10ra`, `Atg16l1`, `Stat1`, `Stat3`, `Ifnar1`, `Ifnar2`, `Ifngr1`, `Ifngr2`, `Il6st`, and `Nfkb1`.

All ten profiles were present. The raw focal profiles contained 17,259 measured features per inspected node. Nine analogs had zero significant features and `Stat1` had one negative significant feature. Across all 45 pairs, there was no overlap of FDR-significant programs. The positive signed-tail overlap was weak, with a mean coefficient of 0.0758 across pairs; negative tails had higher same-direction cosine, but this reflected shared weak directional structure below the FDR threshold, not a recurrent significant response.

## Synthesis

`Il10rb` has exact but rare expression in the requested thalamic population and an operation whose loss should be slower and more context-dependent than depletion of a soluble enzyme, chromatin regulator, spliceosome component, or proteasome factor. Its direct IL-10 receptor partner and a small cytokine/JAK-STAT receptor-signaling cohort were empirically zero or one-DEG perturbations in the same count table and focal Parquet context. I therefore placed `Il10rb` in the quiet cytokine-receptor stratum rather than in the heavy-tailed response class.

The main residual uncertainty is that low transcript reach does not prove failed editing or absent receptor function, and IL10RB-dependent signaling could affect a rare thalamic subpopulation. Still, a response large enough to push multiple measured genes past BH FDR 0.05 was less likely than the observed zero-count behavior of its closest measured receptor analogs. The single-integer direct forecast is:

**predicted `n_degs = 0`**
