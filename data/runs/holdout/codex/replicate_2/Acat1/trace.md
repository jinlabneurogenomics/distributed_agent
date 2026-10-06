# Acat1 direct n_degs forecast

## Target and requested endpoint

- Target: `Acat1`, the single row of `manifests/Acat1.csv`.
- Endpoint: number of measured genes in `151 TH Prkcd Grin2c Glut` with Wilcoxon BH-adjusted `pvals_adj < 0.05`.
- The declared training endpoint was `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`; `Acat1` was absent from it.

## Biology used

The canonical Acat1 biology bundle identifies ACAT1 as mitochondrial acetyl-CoA acetyltransferase used in ketone-body and isoleucine metabolism, not the ER cholesterol-esterifying enzyme SOAT1. Exact focal-population reach is high: in non-target `151 TH Prkcd Grin2c Glut`, `Acat1` was detected in 21,744 of 23,679 nuclei, or 91.83%, with mean raw UMI 3.36 and mean log1p CP10K 1.03.

The functional-stock card favored real loss by harvest: a disruptive P16 edit stops new ACAT1 supply, and the available target-specific turnover measurement, although from rat hepatocytes rather than neurons, was a 38 h apparent half-life, far shorter than the 21-28 day screen window. I therefore treated failed target reach or persistent pre-edit stock as unlikely to be the main reason for a low response.

The uncertain axis was endpoint coupling. Human ACAT1 deficiency can cause episodic ketoacidosis and neurological injury, but the bundle found no matched mouse postnatal neuronal loss experiment and no evidence that normally fed thalamic neurons would enter a beta-ketothiolase stress state within this sparse survivor-conditioned assay.

## Training perturbations checked

Curated annotation sets gave no measured exact ketone-body comparator: in the screen target universe, Reactome `R-MMU-74182`/`R-MMU-77108`/`R-MMU-77111` and GO `GO:0046952` contained only `Acat1`.

The nearest represented branch was mitochondrial organic-acid and branched-chain amino-acid catabolism. Every member present in the focal DEG-count training table was a zero at FDR 0.05:

| Prior set | Training members in `151 TH Prkcd Grin2c Glut` | Counts |
| --- | --- | --- |
| GO `GO:0006550`, L-isoleucine catabolic process | `Bckdk` | 0 |
| KEGG `mmu00280`, valine/leucine/isoleucine degradation | `Abat`, `Auh`, `Bckdhb`, `Ivd`, `Pcca` | all 0 |
| Reactome `R-MMU-77289`, mitochondrial fatty-acid beta-oxidation | `Mecr`, `Mmaa`, `Pcca` | all 0 |

Direct parquet aggregation over `151 TH Prkcd Grin2c Glut` confirmed that the selected catabolic comparators `Abat`, `Auh`, `Bckdhb`, `Bckdk`, `Ivd`, `Mecr`, `Mmaa`, and `Pcca` each had 0 genes at `pvals_adj < 0.05` and 0 genes even at `pvals_adj < 0.10`; their minimum focal adjusted p-values ranged from 0.275 for `Ivd` to 1.0 for several targets, so these were not near misses. Across all cell groups in the declared training parquet, `Bckdhb`, `Bckdk`, `Ivd`, `Mmaa`, and `Pcca` also had no significant genes at FDR 0.05, while `Abat`, `Auh`, and `Mecr` had only one significant gene each outside the focal group.

Same-experiment Findings were concordant with that direct count pattern but were used only as interpretation of the same dataset. Packaged records described `Bckdhb`, `Bckdk`, `Ivd`, `Mmaa`, and `Pcca` as pan-neuronal or pan-measured FDR<0.10 nulls and specifically noted absence of expected secondary ISR, mitochondrial-stress, redox, autophagy, or organic-acidemia stress programs for the represented BCAA/organic-acid perturbations.

I also checked a broader mitochondrial/OXPHOS prior set. In Hallmark oxidative phosphorylation, 28 of 53 training members were zero, 51 of 53 had at most 2 focal DEGs, and the median was 0. The main nonzero outliers, `Mdh1` and `Opa1`, had 29 and 37 DEGs at FDR 0.05 in the focal count table, but they represent a cytosolic malate-aspartate shuttle arm and mitochondrial cristae/dynamics stress respectively rather than the same local ketone-body/isoleucine thiolase chemistry.

The full 1,674-target focal training distribution was itself heavily sparse: median 0, 1,205 zeros, 1,512 targets at 0-2 DEGs, and a 90th percentile of 2 DEGs.

## Synthesis

The high Acat1 expression and the functional-stock card argue that a real mitochondrial ACAT1 lesion could be present in many recovered thalamic neurons. The decisive quantitative evidence, however, was that the closest measured basal mitochondrial catabolic perturbations were complete focal zeros, and the curated corpus interpreted several of those zeros as broad absence of the nuclear stress programs expected from severe organismal organic-acid disease. Acat1 has no exact measured same-enzyme-family mitochondrial comparator, but it is much closer to the buffered BCAA/organic-acid enzyme losses than to `Opa1`, `Atp2a2`, or `Gfpt1`, whose broader organelle or ER-stress lesions produced resolved ISR-like signatures.

I therefore forecast that Acat1 loss will be FDR-flat in `151 TH Prkcd Grin2c Glut`.

Point prediction: 0
