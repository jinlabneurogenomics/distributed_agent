# Notch3 direct n_degs forecast

Target: `Notch3`

Focal population: `151 TH Prkcd Grin2c Glut`

Predicted `n_degs`: `0`

## Evidence used

- The one-row holdout manifest names `Notch3`; `Notch3` is absent from the
  declared 1,674-row `151 TH Prkcd_Grin2c_Glut` training count table, so the
  target count itself was not used.
- The biology bundle's exact in-assay reach for `Notch3` in
  `151 TH Prkcd Grin2c Glut` is extremely low: 61 of 23,679 non-target nuclei
  expressed the transcript, with 72 total UMIs, 0.2576% expressing cells, and
  0.1906 pseudobulk CPM.
- The same bundle adjudicates successfully edited Notch3-expressing cells as
  likely to lose substantial functional Notch3 stock by harvest, but its
  matched expression and phenotype evidence points to mouse CNS vascular mural
  cells rather than the NeuN-positive thalamic neuronal population sampled here.
- The focal-class training distribution is zero-heavy: among 1,674 available
  training perturbations, 1,205 have `n_degs = 0`, the median is 0, the 75th
  percentile is 1, and the mean is pulled to 14.05 by a small set of large
  responders.
- Notch and vascular/pericyte comparators in the same count table support a
  null forecast for this context. `Notch1`, `Notch2`, `Notch4`, `Dll1`,
  `Adam10`, `Psen1`, `Abcc9`, `Acvrl1`, `Axl`, `Pdgfrb`, and `Cspg4` all have
  `n_degs = 0` in `151 TH Prkcd Grin2c Glut`.
- Direct Parquet checks for `Notch1`, `Notch2`, `Notch4`, `Dll1`, `Adam10`,
  `Abcc9`, `Acvrl1`, `Axl`, `Pdgfrb`, and `Cspg4` confirmed 17,259 measured
  genes apiece in the focal class with zero genes even at FDR < 0.10. Their
  matched perturbed-cell counts ranged from 69 for `Adam10` to 324 for
  `Notch4`, so the zeros were not simply missing rows.
- `Mib1` was the one represented Notch-proximal exception checked in the focal
  class, with 27 FDR<0.05 genes led by cholesterol/SREBP genes such as
  `Insig1`, `Dhcr24`, `Fdft1`, and `Ldlr`. Packaged same-experiment Findings
  interpret this as a sterol/cholesterol response that is uncoupled from
  canonical Dll1/Notch receptor/Adam10/presenilin transcriptional signaling,
  so I treated it as a boundary on Notch analog transfer rather than as a
  positive analog for `Notch3`.

## Synthesis

The edit should be molecularly realized in the tiny minority of edited cells
that actually express `Notch3`, but the assayed thalamic NeuN-positive class
has essentially no baseline `Notch3` RNA and the curated loss phenotypes come
from vascular mural cells outside the recovered neuronal compartment. In the
training table, the same class is dominated by true zeros, and the closest
available Notch receptor, ligand, processing, and mural-cell context targets
are all flat. A one-gene idiosyncratic event is possible, but the posterior
mass is concentrated at no BH-significant genes.

Final point estimate: `0`
