# Nfkb2 direct DEG-count prediction

## Target and endpoint

- Target: `Nfkb2`
- Cell group: `151 TH Prkcd Grin2c Glut`
- Endpoint: number of measured genes with BH-adjusted Wilcoxon `p < 0.05`
- Predicted `n_degs`: `0`

## Evidence that determined the prediction

1. The declared one-row holdout manifest contains only `Nfkb2`; `Nfkb2` is not present in the 1,674-row focal-class training count table.

2. The focal training distribution is zero-heavy and sharply skewed. Among 1,674 observed training perturbations in `151 TH Prkcd Grin2c Glut`, 1,205 had `n_degs = 0`, the median was 0, the 75th percentile was 1, the 90th percentile was 2, the 95th percentile was 18, only 43 perturbations reached at least 100 DEGs, and only 3 reached at least 1,000 DEGs. Thus the base rate already favors a zero or very small count unless the target biology points to a known active neuronal module.

3. `Nfkb2` has very low baseline reach in the exact focal population: 301 of 23,679 non-target nuclei expressed it, or 1.271% of nuclei, with mean raw expression of 0.01377 UMI per nucleus and pseudobulk abundance of 0.863 CPM. That is weak support for a broad thalamic, cell-autonomous transcription-factor footprint.

4. The biology-only `Nfkb2` bundle supports target engagement but not a strong matched neuronal endpoint. A disruptive edit should stop resupply of both p100 and processed p52, and the bundle adjudicates functional stock by P37-P44 as likely substantially depleted. At the same time, the best direct loss phenotype is non-neural or systemic, postnatal thalamic relevance is unknown, CNS expression is qualitative rather than matched to the focal neurons, and the related-gene evidence for `Nfkb1` compensation comes from non-neural lineages.

5. NF-kappaB/TNF/TLR pathway training perturbations were flat in the same endpoint. In the focal count table, `Chuk`, `Map3k7`, `Nfkb1`, `Rel`, `Tnfrsf1a`, and `Traf3` each had `n_degs = 0`. Direct profile analysis of the focal Parquet confirmed 17,259 measured genes for each of those six perturbations and zero features with `pvals_adj < 0.05`; their minimum adjusted p-values were 0.727 for `Chuk`, 1.0 for `Map3k7`, 1.0 for `Nfkb1`, 0.140 for `Rel`, 1.0 for `Tnfrsf1a`, and 1.0 for `Traf3`. Packaged same-experiment Findings also describe `Nfkb1`, `Rel`, `Chuk`, `Map3k7`, `Tnfrsf1a`, and `Traf3` as broadly FDR-flat across recovered neuronal groups and lacking canonical NF-kappaB inflammatory or feedback outputs; these reports summarize the same experiment rather than independent replication.

## Synthesis

`Nfkb2` is not obviously an editing-failure case, because the p100/p52 pools should lose new supply across the 21-28 day interval. The decisive issue is endpoint coupling: the perturbation is being assayed in sparse, recovered postmitotic thalamic neurons where `Nfkb2` itself is barely observed, and the closest measured NF-kappaB/TNF/TLR training perturbations are exact zeros in the focal class and broad neuronal nulls in the same experiment. I therefore expect any true downstream effect to be absent or below FDR detection in this class rather than a moderate thalamic transcriptional program.

The integer point prediction is:

```tsv
target_name	predicted_n_degs
Nfkb2	0
```
