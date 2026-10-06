# Direct n_degs forecast for Gabra4

Target: `Gabra4` in `151 TH Prkcd Grin2c Glut`.

Prediction: `2` genes at BH-adjusted Wilcoxon `p < 0.05`.

## Evidence used

### Declared Gabra4 biology bundle

- The one-row holdout manifest names `Gabra4`.
- The canonical bundle for `Gabra4` was served in biology-only mode with `target_outcome_exposed=false` and `labeled_neighbors_exposed=false`.
- Exact focal expression is strong in the non-targeting thalamic population: `Gabra4` is detected in 23,570 of 23,679 nuclei, `pct_cells_expressing=99.5396765`, with `mean_raw_umi=13.7366`, `mean_log1p_cp10k=2.1815`, and `pseudobulk_cpm=860.919`.
- Functional-stock adjudication concludes that P16 editing should `likely_substantially_depleted` alpha-4-containing receptor stock by the P37-P44 harvest. The positive evidence is direct alpha-4 tonic-current dependence in mouse thalamic relay neurons plus broad thalamic expression; the limiting uncertainty is that the rapid turnover clock is a delta-partner surface-trafficking proxy from rat hippocampal preparations rather than an alpha-4-specific postnatal thalamic clearance measurement.

I treated this as support that productive edits should be functionally reachable and broadly sampled in the assayed population, but not as evidence for a large RNA program: germline Gabra4 physiology establishes tonic-current loss, not a P16-to-P37/44 nuclear DEG count.

### Same-experiment GABA_A receptor corpus

The same-experiment corpus has no `Gabra4` report, claim, or explicit comparator edge, so there was no internal Gabra4 outcome to use. Its represented GABA_A receptor evidence was still informative:

- `claim:5b4c69534eb3f2fea19b` states that `Gabrb2` loss selectively induced an activity-associated response in `151 TH Prkcd Grin2c Glut`, whereas represented `Gabra3`, `Gabra2`, `Gabrd`, `Gabrr2`, and `Slc12a2` did not reproduce that multi-gene response.
- `Gabrb2:F001` and `Gabrb2:F002` anchor the upper same-family scale: a small thalamic response with activity-associated genes including `Nr4a1`, `Vgf`, `Fos`, `Npas4`, and `Homer2`.
- `Gabrd:F001` reports the closest alpha4/delta-side perturbation as a one-downstream-gene response in this class: `Gabrd` self-reduction plus `Cttnbp2` up-regulation.
- `Gabrd:F003` explicitly contrasts the weaker `Gabrd` surface with `Gabrb2` and `Gabrg2`, noting that `Gabrd` did not induce the thalamic activity-gene program.
- `Gabra3:F001` to `Gabra3:F003` and `Slc12a2:F001` to `Slc12a2:F003` define the lower boundary: several ion-channel or chloride-axis perturbations can be physiologically meaningful yet transcriptionally flat in this postnatal snRNA readout.

This made `Gabrb2` a scale ceiling rather than the main donor. Alpha-4/delta tonic receptors sit closer to `Gabrd` than to beta-2-containing phasic GABA(A) receptor loss, and the represented alpha subunits argue against a generic alpha-subunit activity signature.

### Training count table in the exact cell class

The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` contains 1,674 training targets and excludes `Gabra4`.

Overall scale:

- 1,205 / 1,674 targets have `n_degs=0`.
- 276 / 1,674 have `n_degs=1`.
- The median is 0 and the 90th percentile is 2.
- The mean is inflated to 14.05 by a small heavy tail of RNA-processing/proteostasis regulators.

Exact GABA-system training counts:

| target | n_degs |
|---|---:|
| Gabra1 | 1 |
| Gabra2 | 0 |
| Gabra3 | 0 |
| Gabra5 | 0 |
| Gabrb1 | 0 |
| Gabrb2 | 4 |
| Gabrb3 | 0 |
| Gabrd | 2 |
| Gabrg2 | 1 |
| Gabrg3 | 0 |
| Gabrr2 | 0 |
| Slc12a2 | 0 |

The family mean is only 0.67 DEGs, and even the expressed, self-reduced receptor subunits are in the 1-4 range. That placed the Gabra4 expectation in the bottom of the global distribution despite its clear target expression and known thalamic physiology.

### Direct Parquet/profile evidence

I sliced the declared training Parquet in `151 TH Prkcd Grin2c Glut` and compared the represented GABA_A cohort. The run-local profile comparison retained all 12 requested profiles and found 8 with no significant features and 4 with 1-9 significant features.

The exact FDR < 0.05 hits among same-family nodes were:

| target | FDR < 0.05 genes |
|---|---|
| Gabrb2 | `Gabrb2`, `Nr4a1`, `Vgf`, `Nalf1` |
| Gabrd | `Gabrd`, `Cttnbp2` |
| Gabra1 | `Gabra1` |
| Gabrg2 | `Gabrg2` |
| Gabra2, Gabra3, Gabra5, Gabrb1, Gabrb3, Gabrg3, Gabrr2, Slc12a2 | none |

The same slice showed `Gabrb2` was the only represented receptor perturbation with the coherent `Nr4a1`/`Vgf`/`Fos`/`Npas4`/`Homer2` activity pattern near FDR thresholds. `Gabrd`, `Gabra1`, `Gabrg2`, and the null subunits did not share those significant downstream genes.

## Synthesis

I predict `Gabra4` will have a self-transcript DEG because the target is highly expressed in essentially all recovered non-targeting cells from this population and because the other clearly detected GABA(A) receptor subunits with sufficient power often show a self row below 0.05.

For downstream genes, I assigned only a weak expectation. The biology bundle says alpha-4-containing receptor stock should decline and the mouse thalamic tonic-current phenotype is real, but the postnatal snRNA endpoint repeatedly converts GABA receptor or chloride perturbations into either no FDR genes or a very small number of genes. The nearest represented subunit, `Gabrd`, contributed one downstream hit, whereas `Gabrb2` is a beta-2-specific upper comparator and not a good direct scale donor for alpha-4/delta tonic receptors.

Putting one likely self-transcript call together with one expected small downstream call gives a point forecast of:

`predicted_n_degs = 2`

Target outcome values for `Gabra4` were not present in the declared inputs and were not used.
