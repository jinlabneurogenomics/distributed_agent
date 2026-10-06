# Direct Tsc1 DEG-count forecast

Target and endpoint:

- target: `Tsc1`
- cell class: `151 TH Prkcd Grin2c Glut`
- endpoint: `n_degs`, the count of measured genes with BH-adjusted Wilcoxon `p < 0.05`

Allowed target prior:

- The one-row holdout manifest names `Tsc1`.
- The declared biology bundle `biology_bundles/Tsc1.json`, also served by `characterization_bundle(target="Tsc1", view="biology")`, is outcome-blind for this task and reports that `Tsc1` is expressed in the exact focal population: 16,583 of 23,679 matched non-target nuclei express it, 70.03% expressing, mean raw UMI 1.324, mean log1p CP10k 0.523, pseudobulk CPM 82.99.
- The same bundle adjudicates TSC1 as a dynamic TSC1-TSC2-TBC1D7 complex component whose functional stock should be substantially depleted inside the P16 edit to P37-P44 harvest window. Its direct mouse-neuron timing evidence places TSC1 protein decline and mTORC1 derepression within days, while sparse postnatal neuronal deletion has functional consequences by 10-14 days. This supports a real mTORC1-disinhibition transcriptional state in edited, recovered thalamic neurons, with survivor conditioning left as a possible attenuator rather than a reason to call the endpoint zero.

Training-count evidence in the focal class:

- The focal training table `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` has 1,674 training perturbations and does not contain `Tsc1`.
- It is highly zero-inflated: 1,205/1,674 targets have 0 DEGs; median 0; mean 14.05; 90th percentile 2; 95th percentile 18; 99th percentile 430; only 59 targets have at least 50 DEGs.
- The closest measured target is the catalytic TSC-complex partner `Tsc2`, with 86 DEGs in this same cell class.
- Other available mTOR-axis rows are smaller or directionally less transferable: `Depdc5` has 13 DEGs as an upstream GATOR1 negative regulator of mTORC1, `Mtor` has 2 despite perturbing the kinase itself, and `Rptor`, `Akt3`, `Strada`, and `Atg5` are at 0.

Parquet/profile evidence:

- Direct filtered Parquet counts in `training_de_all_cell_groups.parquet` reproduce the focal class scale: `Tsc2` has 86 significant features among 17,259 rows with 177 matched perturbed nuclei; `Depdc5` has 13 with 121 matched perturbed nuclei; `Mtor` has 2 with 188 matched perturbed nuclei; `Rptor` and `Atg5` have 0 despite 235 and 114 matched perturbed nuclei.
- Across the training Parquet, `Tsc2` is the only selected TSC/mTOR-axis comparator with recurrent responses outside the focal class, including 202 DEGs in `155 MB Glut` and 53 in `066 CNU-HYa HY GABA`. `Mtor` and `Depdc5` are essentially focal-only among this selected pathway set.
- A symmetric focal profile comparison over `Tsc2`, `Depdc5`, `Mtor`, `Rptor`, and `Atg5` classified the same activity ladder: `Tsc2` in the `at_least_50_significant_features` band; `Depdc5` in `10_to_49_significant_features`; `Mtor` in `1_to_9_significant_features`; `Rptor` and `Atg5` with no significant features.

Synthesis:

`Tsc2` is the quantitative anchor because it is the same protein complex and the same expected endpoint direction: loss of TSC-complex Rheb-GAP restraint and consequent mTORC1 activation. `Depdc5` is a lower, more indirect activation comparator, while `Mtor`/`Rptor` loss remove mTORC1 activity rather than phenocopying TSC loss and were quiet in this focal class.

The target biology moves the point away from the zero-heavy training prior: `Tsc1` is detectably expressed in most focal non-target nuclei, has no close replacement in the biology bundle, and has a direct postmitotic-neuron timing clock compatible with the 21-28 day harvest. I therefore place `Tsc1` close to the measured `Tsc2` count. I round slightly above the `Tsc2` count to allow for high exact target reach and complete structural dependence of the complex, but not into the several-hundred-DEG tail because survivor-conditioned sampling and sparse editing can dampen a severe TSC loss state.

Predicted `n_degs`: 90
