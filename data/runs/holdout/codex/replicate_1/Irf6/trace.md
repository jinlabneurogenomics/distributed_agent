# Irf6 direct DEG-count forecast

## Requested target and endpoint

- Target: `Irf6`
- Cell class: `151 TH Prkcd Grin2c Glut`
- Endpoint: `n_degs`, the count of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05` in the held-out perturbation.

## Evidence used

- The declared canonical `Irf6` biology bundle reports exact focal-population reach of only 13 `Irf6`-expressing matched non-target nuclei among 23,679 in `151 TH Prkcd Grin2c Glut`:
  - `pct_cells_expressing = 0.0549009671`
  - `mean_raw_umi = 0.0005490097`
  - `total_target_umi = 13`
  - `pseudobulk_cpm = 0.0344084`
- The same bundle makes functional realization plausible rather than impossible: IRF6 is a renewable intracellular IRF-family DNA-binding transcription factor, not an installed extracellular or structural product, and the adjudicated stock conclusion is `likely_substantially_depleted` by the P37-P44 harvest after a P16 edit.
- The bundle does not supply evidence for a broad acute postnatal thalamic-neuron requirement. Its strongest mouse phenotypes are developmental or lifelong; the adult neural and injured cortical-culture observations are not a matched acute thalamic loss experiment.
- The exact class-specific training count table is zero-inflated: among 1,674 observed perturbations in `151 TH Prkcd Grin2c Glut`, 1,205 had `n_degs = 0`, the median was 0, and the 75th percentile was 1.
- The most direct family comparators present in that count table were silent in this class: `Irf1`, `Irf2`, `Irf3`, `Irf5`, `Irf8`, and `Irf9` each had `n_degs = 0`.
- A nearby inflammatory/transcription-factor sanity set also did not show a broad class response: `Ifih1`, `Nfkb1`, `Stat2`, `Stat3`, `Stat4`, `Stat5b`, and `Trp63` all had `n_degs = 0`; `Stat1` had only one significant feature, its self-target transcript.
- The training parquet confirmed that those low-count comparator rows had matched perturbed-cell depths on the order of 114-268 nuclei against 23,679 controls in this class. At the declared `Irf6` non-target expression frequency, that depth would contain only about 0.06-0.15 `Irf6`-expressing nuclei in expectation, before accounting for sparse editing and nuclear capture.

## Synthesis

`Irf6` loss should be biologically real in an edited cell that was using IRF6, but the exact in-assay reach says such cells are essentially absent from the focal non-target population. That makes a survivor-conditioned bulk contrast across the recovered thalamic perturbation group very unlikely to accumulate a coordinated rank shift across measured genes. The class-wide training distribution already has a zero median, and the closest assayed IRF-family perturbations are all zero-DEG examples rather than small-but-detectable positive responses. I therefore predict that the held-out `Irf6` perturbation will have no BH-significant measured genes in `151 TH Prkcd Grin2c Glut`.

Predicted `n_degs`: 0
