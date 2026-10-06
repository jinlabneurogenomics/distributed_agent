# Foxg1 direct DEG-count forecast

## Target and endpoint

Target: `Foxg1`

Endpoint: `n_degs`, the number of measured genes in `151 TH Prkcd Grin2c Glut` with BH-adjusted Wilcoxon `p < 0.05`.

## Evidence used

- The declared target bundle reports very low exact focal-population reach for `Foxg1` in the 151 thalamic population: `2,151 / 23,679` non-target nuclei expressed the feature, `pct_cells_expressing = 9.084%`, `mean_raw_umi = 0.1359`, `mean_cp10k = 0.0784`, and `pseudobulk_cpm = 8.52`.
- The same bundle adjudicates FOXG1 as a soluble DNA-binding transcriptional regulator whose functional stock would likely be substantially depleted by the P37-P44 harvest if a P16 edit lands in a genuinely FOXG1-dependent expressing cell. It also records the major caveat that mouse thalamus is the wrong normal expression territory for `Foxg1`; the in-assay expression measurement is therefore the limiting factor rather than protein persistence.
- The selected same-experiment corpus had no `Foxg1` Findings, no Claim assignments, and no explicit comparator references, so there was no preinterpreted target-local report to reuse.
- The 151 training count table has 1,674 targets. It is strongly zero-inflated: 1,205 targets have `n_degs = 0`, the median is `0`, the 75th percentile is `1`, the 90th percentile is `2`, and the mean is pulled up to `14.05` only by a small high-yield tail.
- Developmental or postnatal transcription-factor perturbations that are more comparable to an off-territory `Foxg1` edit were essentially flat in the same 151 table:
  - `Foxp2`, `Otx2`, `Pax6`, `Tbr1`, `Satb2`, `Zbtb20`, `Arx`, `Smad4`, `Tcf4`, `Zic2`, `Zic3`, and `Zic4`: `0`.
  - `Sox2`, `Sox5`, and `Zic1`: `2`.
  - all 11 non-`Foxg1` `Fox*` targets in the table were `0`; all six `Pax*` targets were `0`; five of six `Smad*` targets were `0`.
- Direct Parquet inspection in the matched `151 TH Prkcd Grin2c Glut` context confirmed that the selected quiet comparators were measured over `17,259` genes per perturbation rather than being absent from the DE table. In a 17-node cohort of quiet developmental TFs plus Wnt/catenin contrasts, 13 nodes had no FDR<0.05 genes, 2 had only 1-9 significant genes, and only `Ctnnb1` and `Tcf7l2` had large 151 responses.

## Synthesis

The upward case is that `Foxg1` encodes a renewed nuclear transcription factor with postnatal neural loss phenotypes in other contexts, so a productive edit should matter where FOXG1 is actually being used. The downward case is stronger for this endpoint: `151 TH Prkcd Grin2c Glut` is a thalamic population with only a small, low-UMI `Foxg1`-positive minority, and analogous juvenile developmental TF perturbations in the 151 training table are dominated by zero or singleton/two-gene outcomes even when assayed with enough rows for DE testing.

I therefore treated the Wnt/catenin high-DEG responses as pathway-specific thalamic positives rather than scale donors for `Foxg1`, and placed `Foxg1` at the quiet end of the same measured TF distribution.

Predicted `n_degs`: `0`
