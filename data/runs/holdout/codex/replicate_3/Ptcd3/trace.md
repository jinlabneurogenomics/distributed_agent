# Ptcd3 DEG-count prediction

Target: `Ptcd3`

Focal population: `151 TH Prkcd Grin2c Glut`

Predicted `n_degs`: `0`

## Declared target context

- The one-row holdout manifest declares `Ptcd3` as the target.
- The declared target bundle is outcome-blind for `Ptcd3`: it reports exact focal-population target expression but not the held-out `Ptcd3` differential-expression signature or DEG count.
- Exact focal expression in matched non-target nuclei is strong enough that the transcript is in reach: `Ptcd3` is detected in 20,854 / 23,679 nuclei, 88.07%, with mean raw UMI 2.707 and pseudobulk 169.68 CPM in `151 TH Prkcd Grin2c Glut`.
- The biological card places PTCD3/mS39 in the mitochondrial small ribosomal subunit. PTCD3 depletion can impair mitochondrial translation and respiration, but the card found no neuronal PTCD3 half-life, mS39 exchange, assembled-mitoribosome residence time, or post-edit timing anchor that determines how much operative small-subunit stock is gone 21-28 days after P16 editing.

## Training measurements used

- The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` table contains 1,674 focal-population training targets. Its distribution is very sparse: 1,205 / 1,674 are zero, the median is 0, the 75th percentile is 1, and the mean is 14.05 because a small tail has hundreds to thousands of hits.
- Curated closed-universe annotation put `Ptcd3` in Reactome mitochondrial translation with only one other perturbed target in that set, `Gfm2`; `Gfm2` has `n_degs = 0` in the focal count table.
- The broader GO mitochondrial-translation set adds `Lars2` and `Rars2`; both have `n_degs = 0` in the focal count table.
- Direct Parquet queries of `training_de_all_cell_groups.parquet`, filtered to `151 TH Prkcd Grin2c Glut`, confirmed that `Gfm2`, `Lars2`, and `Rars2` each had 17,259 measured-gene rows and zero genes at both FDR < 0.05 and FDR < 0.10.
- A structural mitoribosome comparator, `Dap3`, had one focal FDR < 0.05 row, but the row was `Dap3` itself; the same-experiment `Dap3:F001` and `Dap3:F002` Findings interpret its downstream surface as flat and as lacking the Opa1-like mitochondrial ISR module.
- Core OXPHOS training comparators were also focal-null or self/singleton-like: observed complex I, III, and IV subunits in the count table all had `n_degs` of either 0 or 1.

## Same-experiment corpus boundaries

The selected July 260713 same-experiment corpus is another representation of the mounted experiment, not an independent replicate. I used it only to interpret why the relevant measured training targets should or should not be transferred.

- `Gfm2:F001-F003` reports no robust downstream DE after postnatal `Gfm2` perturbation and places `Gfm2` with weak core OXPHOS/mitochondrial-translation perturbations rather than the strong `Opa1` stressor.
- `Lars2:F002` and `Lars2:F004` report absence of the expected mitochondrial translation/OXPHOS/ATF4 program and note that `Fars2`, `Gfm2`, and `Rars2` were also flat or nearly flat.
- `Rars2:F002-F003` reports absence of the expected mitochondrial translation, OXPHOS, ATF4/ISR, or UPRmt transcriptional programs and lack of convergence with `Fars2`, `Lars2`, and `Gfm2`.
- A shared Claim over `Aimp1`, `Fars2`, `Gfm2`, `Lars2`, and `Rars2` summarizes the represented mitochondrial aaRS and mitochondrial-protein-synthesis perturbations as transcriptionally buffered or nonconvergent in this postnatal neuronal assay.
- `Opa1:F002-F004` shows that this snRNA readout can detect a mitochondrial ATF4/ISR-like state with mitochondrial-RNA decreases when a perturbation crosses that state. Because `Opa1` is an inner-membrane fusion/cristae perturbation with 37 focal FDR < 0.05 genes, it is a positive benchmark for detectability, not a same-complex quantitative analog for `Ptcd3`.

## Synthesis

The nearest measured biochemical neighbors of `Ptcd3` are mitochondrial translation or mitoribosome perturbations whose focal thalamic transcriptomes are zero or self-only, and the broader respiratory-chain subunits almost never exceed a singleton count. The `Ptcd3` bundle gives no reason to expect faster loss of operative mitoribosomes than those buffered comparators: editing stops new PTCD3 supply, but pre-existing mS39-containing mitoribosomes and downstream respiratory complexes can persist for an unmeasured fraction of the 21-28 day window.

`Ptcd3` expression is clearly detectable in the focal population, so a self-transcript hit is possible. I did not add one for self knockdown because the closest same-axis training targets `Gfm2`, `Lars2`, `Rars2`, `Fars2`, and `Lrpprc` had zero focal hits including self, and the dataset portrait cautions that measured self-target loss is not a reliable proxy for functional disruption. I therefore chose the modal and same-pathway-supported integer:

`predicted_n_degs = 0`
