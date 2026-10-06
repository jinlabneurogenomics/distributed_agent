# Foxc1 direct n_degs forecast

## Target and endpoint

- Target manifest: `Foxc1`.
- Requested cell class: `151 TH Prkcd Grin2c Glut`.
- Endpoint: number of measured genes with BH-adjusted Wilcoxon `p < 0.05`.
- Declared same-class training count table:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Declared DE parquet:
  `[local file: training_de_all_cell_groups.parquet]`.
- Canonical biology-only bundle:
  `[local file: Foxc1.json]`.

I used the biology-only `Foxc1` characterization and the training count/profile
measurements. I did not use target outcome rows or scalar-prior,
calibrated-probability, relationship-review, branch-calibration, or
terminal-prediction artifacts.

## Evidence used

### Biology and focal reach

The Foxc1 characterization card says FOXC1 is a renewable nuclear forkhead
transcription factor and that, in an edited Foxc1-expressing cell, pre-edit
protein should be substantially depleted by the 21-28 day harvest window.
So lack of protein turnover is not the limiting factor.

The same bundle also points the other way for this specific endpoint:

- Exact in-assay non-target reach in `151 TH Prkcd Grin2c Glut` was extremely
  low: 154 of 23,679 nuclei expressed Foxc1, `pct_cells_expressing` =
  0.650365%, `mean_log1p_cp10k` = 0.003112, and `pseudobulk_cpm` = 0.455249.
- The source evidence localizes developmental brain Foxc1 largely to meninges,
  pericytes, and vascular cells rather than neural tissue, while the PerturbAI
  assay enriches NeuN-positive neuronal nuclei.
- The developmental cortical and hydrocephalus phenotypes were secondary to
  embryonic/early-postnatal meningeal loss, so they did not establish a strong
  post-P16 requirement in recovered thalamic neurons.
- Foxc2 is the closest paralog named in the biology bundle, but the bundle did
  not establish compensation or a Foxc1/Foxc2 requirement in this postmitotic
  thalamic neuronal context.

My interpretation was that successful Foxc1 editing in a rare Foxc1-positive
thalamic neuron could remove nuclear FOXC1, but very few assayed cells appear
to carry Foxc1-dependent function at baseline. The biology therefore supplies
strong downward pressure on a class-wide BH-significant signature.

### Same-class training counts

The declared `151 TH Prkcd Grin2c Glut` count table contained 1,674 non-Foxc1
training targets. Its distribution was sparse:

- 1,205 / 1,674 targets had `n_degs = 0`.
- 1,481 / 1,674 had `n_degs <= 1`.
- Median = 0; 75th percentile = 1; 90th percentile = 2; 95th percentile = 18.

The relevant forkhead-family training perturbations were all exact endpoint
nulls in the count table:

| target | n_degs |
|---|---:|
| Foxa2 | 0 |
| Foxc2 | 0 |
| Foxe3 | 0 |
| Foxi1 | 0 |
| Foxj3 | 0 |
| Foxk2 | 0 |
| Foxl1 | 0 |
| Foxl2 | 0 |
| Foxn1 | 0 |
| Foxp2 | 0 |
| Foxp3 | 0 |

This mattered more than generic transcription-factor identity. The same count
table does contain a few high-burden transcriptional regulators, so I did not
treat "TF" as a reason for a large count. Instead, the training evidence nearest
to the Foxc1 operation and family was uniformly quiet in the exact held-out cell
class.

### Training profile check

I compared those eleven forkhead targets in the declared parquet after filtering
to `group_name == "151 TH Prkcd Grin2c Glut"`, using `gene_target` as the node,
`names` as the measured feature, `logfoldchanges` as the signed profile value,
and `pvals_adj < 0.05` as the significance threshold.

The run-local profile comparison over:

`Foxa2, Foxc2, Foxe3, Foxi1, Foxj3, Foxk2, Foxl1, Foxl2, Foxn1, Foxp2, Foxp3`

reported `response_activity_status_counts = {"no_significant_features": 11}`.
Inspection of `Foxc2`, `Foxp2`, and `Foxa2` each showed `significant_feature_count
= 0`. Thus the forkhead zeros in the count table were not hiding a recurrent
BH-significant directional module.

## Synthesis

Foxc1 has a feasible acute molecular operation, but the requested endpoint is a
population-level thalamic neuronal DE count. Its exact target reach is far below
1% of non-target nuclei in that focal population, the best prior phenotypes come
from non-neuronal developmental compartments, and every measured forkhead-family
training perturbation in the same cell class had zero DEGs. Against a background
where the median training target already has no significant gene and the 75th
percentile has only one, these lines of evidence made a nonzero forecast less
plausible than a true zero.

Predicted `n_degs`: **0**.
