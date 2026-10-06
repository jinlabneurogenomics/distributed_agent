# Mc4r direct count forecast

## Declared target

- Manifest target: `Mc4r`.
- Endpoint: `n_degs` in `151 TH Prkcd Grin2c Glut`, counting measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`.
- Declared exact reach for the target in this focal population was extremely low: 80 of 23,679 non-target nuclei expressed `Mc4r` (`0.337852%`), with 97 total target UMIs, mean raw UMI `0.004096`, and pseudobulk CPM `0.256739`.

## Biological prior

The Mc4r bundle supported a real loss-of-function operation in cells that actually use the receptor: MC4R is a melanocortin GPCR, editing should stop new receptor production, the pre-edit receptor pool is dynamically trafficked, and the 21-28 day edit-to-harvest interval is long enough for substantial loss of functional stock to be plausible. The evidence was still partial because endogenous MC4R turnover was not measured in juvenile thalamic neurons.

That realization prior did not outweigh the focal expression reach. The focal class aggregates thalamic glutamatergic nuclei, but `Mc4r` RNA was detected in only about one cell in 296. Even a strong cell-autonomous effect in the rare expressing subpopulation would be diluted in the class-wide matched Wilcoxon contrast, and the declared biology bundle only established low/nucleus-selective thalamic expression rather than a broad requirement across `151 TH Prkcd Grin2c Glut`.

## Training evidence used

The focal training count table contained 1,674 perturbations:

- 1,205 had `n_degs = 0`.
- The median was `0`; the 75th percentile was `1`.
- The tail was driven by qualitatively different ubiquitous RNA-processing, proteasome, transport, and chromatin targets such as `Uba5`, `Tpr`, `Sin3a`, `Rnpc3`, and `Zbtb7a`, so I did not use those as biological comparators for a sparse neuropeptide GPCR.

I used curated training-available analog nomination for `Mc4r` only as a typed comparator pool, then read the selected genes in the count table and Parquet. The closest receptor or ligand comparators were silent in the focal endpoint:

- Native or projected MC4R complex/neuropeptide comparators all had `0` DEGs: `Mchr1`, `Crhr1`, `Htr2c`, `Adrb3`, `Adrb2`, `Npy1r`, `Npy2r`, `Oxtr`, `Ntsr1`, `Npy5r`, `Htr1b`, `Gprc5b`, and `Cxcr4`.
- The direct STRING interaction comparator `Agrp` also had `0`.
- The two training-available melanocortin-receptor activity comparators, `Mc1r` and `Mc2r`, both had `0`.
- Downstream or adjacent Gs/cAMP pathway comparators `Gnas`, `Adcy1`, `Adcy3`, and `Adcy5` also had `0`.

To check this at the expression-profile level rather than relying only on the derived CSV, I queried `training_de_all_cell_groups.parquet` in the matched focal context for the 20 selected receptor/ligand/Gs-cAMP comparators above. Each had 17,259 measured-gene rows in `151 TH Prkcd Grin2c Glut`, and none had any row with `pvals_adj < 0.05`.

## Synthesis

The target is biologically capable of signaling, but it is nearly absent in the exact assayed focal population. The training distribution already has a zero-inflated baseline, and the closest receptor, melanocortin-family, neuropeptide, and cAMP comparators are uniformly `0` in the same endpoint. I therefore predicted the modal/null integer rather than adding a small nonzero count.

Predicted `n_degs`: `0`.
