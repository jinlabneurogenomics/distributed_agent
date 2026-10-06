# Edar DEG-count forecast

## Target

- `gene_target`: `Edar`
- `group_name`: `151 TH Prkcd Grin2c Glut`
- Endpoint: number of measured genes in this group with BH-adjusted Wilcoxon `p < 0.05`

## Evidence used

1. **Declared Edar biology-only bundle.** The in-assay non-target expression reach is near the detection floor: 19 of 23,679 focal-class non-target nuclei expressed `Edar`, with 22 total Edar UMIs, mean CP10K `0.0004996465`, mean raw UMI `0.0009290933`, pseudobulk CPM `0.05822957`, and `0.0802399%` of cells expressing. The bundle also adjudicates EDAR as a renewable cell-surface TNFR-family receptor whose pre-existing receptor pool is likely substantially depleted by the 21-28 day harvest, but this only matters in the very small Edar-expressing compartment. The matched biological phenotypes are developmental ectodermal phenotypes, not postnatal thalamic-neuron phenotypes, and target-specific neuronal EDAR turnover or signaling demand was absent from the card evidence.

2. **Declared `151 TH Prkcd Grin2c Glut` training counts.** The training response distribution is extremely sparse: 1,205 of 1,674 training perturbations have `n_degs = 0`; 1,481 have `< 2`; and 1,542 have `< 5`. Thus a weakly expressed target with no known postnatal thalamic function starts on the modal zero branch, while large counts in this class are concentrated in broadly operative nuclear/RNA/proteostasis regulators rather than in low-context receptor targets.

3. **Function/pathway comparators from the count table and expression Parquet.** The assayed EDAR ligand `Eda` has `n_degs = 0` in the same focal count table. So do measured TNFR/NF-kappaB-adjacent genes `Tnfrsf1a`, `Tnfrsf11a`, `Tnfrsf13c`, `Tnfrsf4`, `Tnfrsf9`, `Nfkb1`, `Map3k7`, and `Traf3`. A direct profile comparison on the declared Parquet for `Eda`, `Tnfrsf1a`, `Nfkb1`, `Map3k7`, `Traf3`, and several low-neural receptor controls (`Tlr4`, `Kit`, `Tshr`, `Vdr`, `Igf1r`, `Notch1`, `Tgfbr1`) found each of the 12 selected perturbations had zero significant measured genes in `151 TH Prkcd Grin2c Glut`.

## Synthesis

The operative lesion is plausible in edited cells because EDAR is not a permanent pre-installed structure, but exact focal expression makes the reachable EDAR-maintaining population tiny. The biology card gives no positive reason to expect an EDAR-dependent postnatal thalamic transcriptional state, and the closest declared training measurements around EDA/TNFR/NF-kappaB signaling are flat in this same neuronal class. I therefore place the point prediction at the modal floor rather than borrowing counts from broad essential or chromatin regulators.

`predicted_n_degs = 0`
