# Ahi1 direct `n_degs` forecast

Target perturbation: `Ahi1`

Forecasted endpoint: number of genes in `151 TH Prkcd Grin2c Glut` with BH-adjusted Wilcoxon `p < 0.05`.

## Evidence used

- The one-row manifest and biology bundle both name `Ahi1`.
- `Ahi1` is well detected in the focal non-target population: 21,822 of 23,679 non-target nuclei express the measured feature, with 92.16% expressing, mean CP10K 2.19, and pseudobulk CPM 212.61. This supports reach in the assayed class, but does not quantify editing efficiency.
- The Ahi1 biology bundle supports real postnatal neuronal function in ciliary transition-zone trafficking and in endocytic signaling through HAP1/TrkB. Its functional-stock adjudication is weaker for the P16-to-P37/P44 atlas window: new Ahi1 synthesis should stop after editing, but pre-existing cytoplasmic and transition-zone pools may persist, so harvest was judged a partially depleted or leading-edge state rather than confident complete functional clearance.
- Thalamic `n_degs` in the declared training count table is sparse: 1,205/1,674 measured training perturbations have 0 DEGs, 1,481/1,674 have at most 1 DEG, and the 90th percentile is 2 DEGs.
- Ahi1's most specific measured analogs in the mouse annotation nomination were transcriptionally quiet in the same count table:
  - `Hap1`, the human-ortholog-projected AHI1-HAP1 complex partner, has 0 DEGs.
  - `Cep290` and `B9d1`, the two measured direct-interaction/MKS-complex candidates, both have 0 DEGs.
- The broader measured ciliary neighborhood was also mostly null in `151 TH Prkcd Grin2c Glut`:
  - the two measured `MKS complex` nominees were both 0;
  - 7/10 `non-motile cilium assembly` nominees were 0, including `Cep290`, `Rpgrip1l`, `Ift88`, `Dync2h1`, and `Tbc1d32`;
  - 29/34 `cilium assembly` nominees were 0.
- A matched profile comparison over 14 high-priority measured Ahi1 nominees from the declared Parquet found no missing profiles and 12/14 with no FDR-significant genes; only `Ntrk2` and `Ttc8` fell in the 1-9 DEG bin. The direct ciliary and HAP1 comparators in that profile check all had `n_degs = 0`.

## Synthesis

The focal population expresses `Ahi1`, and the prior literature makes a realized perturbation biologically plausible. The major downward constraints are more specific to this endpoint: the P16 acute edit may not fully clear installed ciliary transition-zone function by harvest, the source biology is strongest in retina, hypothalamus, hippocampus, and cortex rather than juvenile thalamus, and measured perturbations of the closest available ciliary/MKS/HAP1 comparators are almost all exact nulls in the same thalamic class. Because the declared training distribution already puts most perturbations at 0 or 1 DEG and the closest task-matched analogs concentrate at 0, I forecast the modal near-null outcome.

Predicted `n_degs`: 0
