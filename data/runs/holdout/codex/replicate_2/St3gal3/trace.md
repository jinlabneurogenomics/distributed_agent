# Direct forecast for St3gal3

## Target and endpoint

- Target: `St3gal3`
- Cell group: `151 TH Prkcd Grin2c Glut`
- Endpoint: `n_degs`, the number of measured genes with BH-adjusted Wilcoxon `p < 0.05`
- Prediction: `1`

The target biology bundle at `[local file: St3gal3.json]` is endpoint-blind.  It reports that `St3gal3` is directly expressed in the focal non-target population (`14416 / 23679` nuclei expressing; `60.88%`, mean log1p CP10K `0.4252`, pseudobulk CPM `66.74`) and that a P16 disruptive edit should probably deplete much of the functional ST3Gal-III enzyme plus renewed ST3Gal-III-marked glycoprotein stock by the P37-P44 harvest.  That supports real target reach in this class.

The same bundle also makes the loss-to-DE projection weak rather than assured: ST3Gal-III installs alpha-2,3 sialic-acid marks on existing glycoproteins rather than directly regulating transcription, installed glycans disappear only as their carriers turn over, target-specific carrier turnover is unknown, and overlapping ST3Gal-family enzymes may buffer part of the biochemical flux.  Adult and germline mouse data establish a neural phenotype for severe or lifelong `St3gal3` reduction, but they do not provide an acute post-P16 thalamic-neuron time course.

## Training evidence used

The declared `151 TH Prkcd Grin2c Glut` training count table contains 1674 non-held-out targets.  Its response burden is extremely concentrated near zero:

- `1205 / 1674` rows have `n_degs = 0`.
- `276 / 1674` rows have `n_degs = 1`.
- The median is `0`, the 75th percentile is `1`, the 90th percentile is `2`, and the 95th percentile is `18`; the mean is inflated to `14.05` by a small high-burden tail.

Within the count table, the closest available glycan/Golgi-carbohydrate perturbations were mostly silent:

| training target | n_degs |
|---|---:|
| B3gat3 | 0 |
| Dpm1 | 0 |
| Ext1 | 0 |
| Ext2 | 0 |
| Gal | 0 |
| Hs6st2 | 0 |
| St3gal5 | 1 |

I then checked the exact same seven training profiles in the declared training parquet, filtered to `151 TH Prkcd Grin2c Glut`.  Each had 17,259 measured rows in this class.  `St3gal5`'s one significant row was the self transcript itself (`logfoldchange = -0.788`, `p_adj = 1.96e-14`, `n_pert_matched = 163`, `n_ctrl_matched = 23679`); no downstream `St3gal5` row was significant.  The other six carbohydrate-processing comparators had zero BH 0.05 genes with similar matched perturbed-cell counts, ranging from 129 to 238.

A symmetric signed-profile comparison of those seven comparator profiles did not reveal a hidden recurrent module behind the low counts.  Only one selected node had any significant feature, the positive and negative top-tail overlap coefficients across the 21 comparator pairs averaged only `0.0143` and `0.0157`, respectively, and the cohort had no FDR-significant program overlap.

## Synthesis

`St3gal3` has better exact in-class expression than a technical no-reach target, and the multiweek edit window is long enough that an enzymatic glycan mark should substantially refresh.  Those points make a complete functional non-event less likely than for an unexpressed or fully persistent target.

The task-matched measurements nevertheless argue for a very small observed transcriptional footprint.  The focal class count distribution places most perturbations at 0 or 1 DEG, the available glycan-processing comparators are all null or self-only, and their signed profiles are not coordinated.  The biology of `St3gal3` also routes through post-translational glycan remodeling with uncertain substrate turnover and possible family compensation, so there is no strong reason to move it into the broad stress/regulatory tail of the count table.

Because `n_degs` includes any significant self-transcript row, the most defensible point estimate is one significant measured gene: a possible self or singleton event, with little expected downstream FDR-significant response.
