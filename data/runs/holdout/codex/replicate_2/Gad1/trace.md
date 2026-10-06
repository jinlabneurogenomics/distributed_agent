target_name: Gad1
predicted_n_degs: 0

## Evidence used

- The one-row holdout manifest target is `Gad1`; the requested context is `151 TH Prkcd Grin2c Glut`.
- The canonical `Gad1` biology bundle exposes no target outcome and reports that disruptive P16 editing should be able to deplete Gad1-encoded GAD67 by P37-P44 in cells that rely on it: GAD67/GABA are renewed functional pools, and the bundle adjudicates `functional_stock_by_harvest` as `likely_substantially_depleted`.
- The exact non-target expression reach in this focal class is narrow and low: 2,900 / 23,679 nuclei express `Gad1` = 12.247%, with mean raw expression 0.184 UMI per nucleus, mean CP10K 0.106, and pseudobulk CPM 11.519. This makes an edited `Gad1` state biologically reachable but strongly diluted across the assayed aggregate.
- The declared training table for the same focal class has 1,674 observed targets; 1,205 have `n_degs = 0`, 276 have `n_degs = 1`, and the median is 0. Large DEG burdens are rare and concentrated in broadly disruptive targets.
- The closest assayed GABA pathway perturbations are quiet in this class:
  - `Gad2`: 0 DEGs; Parquet minimum BH-adjusted p-value = 1.0 across 17,259 measured genes.
  - `Slc32a1`: 0 DEGs; minimum BH-adjusted p-value = 1.0.
  - `Slc6a1`: 0 DEGs; minimum BH-adjusted p-value = 1.0.
  - `Abat`: 0 DEGs; minimum BH-adjusted p-value = 0.831.
- Nearby GABA receptor/glutamate metabolism perturbations were also tiny rather than broad: `Gabra1` = 1 DEG, `Gabrg2` = 1, `Gabrb2` = 4, `Glud1` = 1, `Slc1a1` = 1, and `Slc1a2` = 1.
- The selected same-experiment corpus release had no packaged `Gad1` Findings, Claims, or explicit references, so no report-derived `Gad1` outcome was used.

## Synthesis

`Gad1` itself should be a functional knockout in the minority of 151-class cells that express it, but this Perturb-seq contrast is averaged over recovered nuclei in a glutamatergic thalamic class where observed Gad1 RNA reach is only about 12%. The in-class training perturbations of the paralogous GABA synthesis enzyme, vesicular GABA transporter, GABA reuptake transporter, and GABA catabolism all produced no BH-significant genes, and the few receptor or glutamate-handling comparators that did register were only self-target-scale responses of 1-4 genes. I therefore placed `Gad1` at the modal low-response value rather than assigning a broader transcriptional footprint.
