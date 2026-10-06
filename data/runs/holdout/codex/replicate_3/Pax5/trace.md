# Pax5 direct DEG-count forecast

## Target and endpoint

- Manifest target: `Pax5`
- Focal population: `151 TH Prkcd Grin2c Glut`
- Endpoint: `n_degs`, the count of measured genes with BH-adjusted Wilcoxon `p < 0.05` in the focal population.
- Prediction: `0`

## Declared target biology

The declared Pax5 perturbation characterization was the biology-only bundle; it exposed no Pax5 response signature and no Pax5 outcome count. Its exact focal-expression measurement is the dominant local constraint:

- `Pax5` was detected in 29 of 23,679 non-target focal nuclei, or 0.122471% of nuclei.
- Total Pax5 support in the focal non-target population was 33 raw UMIs, with mean raw UMI 0.00139364 and pseudobulk CPM 0.0873444.
- Pax5 is a renewable nuclear sequence-specific transcription factor, so a disruptive edit should deplete new functional Pax5 in truly expressing cells over the 21-28 day P16-to-P37/P44 window.
- Functional realization is nevertheless limited by context reach: the closest neural evidence is developmental midbrain/cerebellum evidence, adult mouse brain data support restricted rather than broad thalamic Pax5 expression, and Pax2 compensation has only been tested in embryonic midbrain-hindbrain patterning.

Taken together, the bundle supports effective loss of Pax5 protein where Pax5 is present, but it argues that very few assayed 151 TH Prkcd Grin2c Glut nuclei have a Pax5-dependent postnatal program to perturb.

## Training measurements used

The focal training count table contained 1,674 non-held-out targets. It was strongly zero-inflated:

- 1,205 / 1,674 training targets had `n_degs = 0`.
- The median was 0, the 75th percentile was 1, the 90th percentile was 2, the 95th percentile was 18, and the maximum was 2,677.

The closest family-level and developmental-transcription-factor training perturbations were focal nulls:

| training target | 151 TH `n_degs` |
| --- | ---: |
| `Pax2` | 0 |
| `Pax3` | 0 |
| `Pax4` | 0 |
| `Pax6` | 0 |
| `Pax7` | 0 |
| `Pax8` | 0 |
| `En1` | 0 |
| `En2` | 0 |
| `Otx2` | 0 |
| `Foxa2` | 0 |

The same-experiment Parquet was used only for training perturbations. A focal profile comparison of `Pax2`, `Pax3`, `Pax4`, `Pax6`, `Pax7`, `Pax8`, `En1`, `En2`, `Otx2`, and `Foxa2` in `151 TH Prkcd Grin2c Glut` found complete profiles for all 10 nodes and `response_activity_status = no_significant_features` for every node. A direct Parquet check across all cell groups found only one significant feature among `Pax2`, `Pax3`, `Pax4`, `Pax6`, `Pax7`, `Pax8`, `En1`, `En2`, and `Otx2`, namely a single `Pax7` DEG in `022 L5 ET CTX Glut`; thus the Pax-family null behavior was not a narrow artifact of the 151 TH class.

These are same-experiment measurements rather than independent biological replication.

## Synthesis

Pax5 has two properties that point in opposite directions: it is a transcription factor whose functional stock should turn over after editing, but it is almost absent from the focal nuclei and its strongest known neural roles are developmental and regionally restricted. For this endpoint the expression reach is the stricter term: a broad focal DEG count needs either a sizable edited, Pax5-dependent subset or a non-cell-autonomous/survivor transcriptional state large enough to be visible in the recovered 151 TH aggregate. The declared bundle does not support that scenario, and the training table shows that related Pax genes and nearby developmental TFs are measured as focal zeroes under comparable postnatal whole-brain CRISPR conditions.

Given the very low focal Pax5 transcript reach, the zero-inflated empirical background, and the zero DEG burden of the closest assayed Pax-family comparators, the biology-only point forecast is:

`Pax5	0`
