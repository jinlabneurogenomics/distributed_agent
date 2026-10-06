# Cacng8 prediction trace

## Question and endpoint

I interpreted the task as a point prediction for the held-out perturbation `Cacng8`, exactly as listed in `027_Cacng8.csv`, in the focal `151 TH Prkcd Grin2c Glut` thalamic glutamatergic class. The quantity to predict is the integer number of measured genes with Benjamini-Hochberg-adjusted Wilcoxon `pvals_adj < 0.05`; this definition includes the target transcript itself if it passes the same cutoff.

I verified that `Cacng8` is present in neither the focal training count table nor the `gene_target` column of `training_de_all_cell_groups.parquet`, so no Cacng8 endpoint or Cacng8 signature rows were used.

## Sources

- `training_de_all_cell_groups.parquet`: focal-cell log2 fold changes and adjusted p values for non-held-out perturbations.
- `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`: observed focal-cell `n_degs` for 1,674 non-held-out perturbations.
- `027_Cacng8.csv`: the requested target list.
- Distributed Agents same-experiment PerturbAI corpus release `perturbai-july-260713-sourceguard-1773-v1`: target findings, the AMPAR/TARP buffered-response claim `claim:a9367c3aeaad95bfae9c`, and related Cacng2, Cacng3, Gria, Frrs1l, and Dlg4 findings. This is a structured interpretation layer over the same screen, not independent replication.
- Distributed Agents runtime profile tools: signed `logfoldchanges` comparison for an AMPAR/NMDAR/PSD candidate cohort in the focal cell group.
- PubMed literature:
  - Tomita et al. 2003, PMID 12771129, DOI 10.1083/jcb.200212116: defined the classical TARP family including stargazin/gamma-2, gamma-3, gamma-4, and gamma-8 as AMPAR regulators.
  - Rouach et al. 2005, PMID 16222232, DOI 10.1038/nn1551: showed TARP gamma-8 controls hippocampal AMPAR number, distribution, and synaptic plasticity.
  - Tomita et al. 2007, PMID 18000041, DOI 10.1073/pnas.0708970104: showed gamma-8 deletion changes hippocampal kainate/AMPAR physiology and reduces hippocampal neurotoxicity.
  - Herguedas et al. 2022, PMID 35136046, DOI 10.1038/s41467-022-28404-7: structural work explaining how TARP gamma-8 modulates GluA1/2 AMPAR gating and conductance.
  - Yamasaki et al. 2023, PMID 36655318, DOI 10.1177/0271678X231152025: rat PET with a TARP gamma-8 ligand found highest binding in hippocampus and lower binding in thalamus.

## Computational steps

1. I read the manifest and focal count table, confirming that the only requested held-out target was `Cacng8`.
2. I summarized the training `n_degs` distribution. It is highly zero-inflated: 1,205/1,674 perturbations have 0 focal DEGs, the median is 0, the 75th percentile is 1, the 90th percentile is 2, and the 95th percentile is 18. This calibration means that a quiet synaptic perturbation should stay at 0 or 1 unless there is target-specific evidence for a broad response.
3. I queried the focal-cell Parquet rows for mechanistic candidates:

```python
filter = (
    (field("group_name") == "151 TH Prkcd Grin2c Glut")
    & field("gene_target").isin(candidate_targets)
)
```

Then I counted `pvals_adj < 0.05` and inspected the significant rows per candidate. The relevant observed counts in the focal group were:

| training perturbation | focal n_degs | expression-pattern evidence |
| --- | ---: | --- |
| `Cacng2` | 0 | no FDR < 0.05 rows; even the top focal rows had `pvals_adj = 1.0` |
| `Cacng3` | 0 | no FDR < 0.05 rows; top focal rows had `pvals_adj = 1.0` |
| `Gria1` | 0 | no focal FDR < 0.05 rows; best adjusted p value was 0.246 |
| `Gria2` | 0 | no focal FDR < 0.05 rows |
| `Gria3` | 0 | no focal FDR < 0.05 rows; `Gria3` self row had adjusted p = 0.971 |
| `Frrs1l` | 1 | the one call was `Frrs1l` itself; no downstream focal genes |
| `Dlg4` | 1 | the one call was `Dlg4` itself; no downstream focal genes |
| `Grik5` | 1 | the one call was `Grik5` itself |
| `Grin2a` | 1 | the one call was `Grin2a` itself |
| `Grin2b` | 2 | `Grin2b` itself plus `Pianp` |
| `Grin2d` | 0 | no focal FDR < 0.05 rows |
| `Grin1` | 89 | broad positive counterexample; `Grin1` self plus synaptic/activity-state genes such as `Scg2`, `Stmn4`, and `Kctd16` |
| `Camk2a` | 0 | no focal FDR < 0.05 rows |
| `Camk2b` | 1 | the one call was `Camk2b` itself |
| `Dlgap4` | 2 | `Dlgap4` itself plus `Vgf` |
| `Shank2` | 0 | no focal FDR < 0.05 rows |
| `Shank3` | 2 | `Shank3` itself plus `Uba5` |
| `Syngap1` | 0 | no focal FDR < 0.05 rows |
| `Tanc2` | 0 | no focal FDR < 0.05 rows |

4. I used Distributed Agents runtime profile comparison over focal `logfoldchanges`, with `pvals_adj < 0.05` supplied as the significant-feature mask, for 18 AMPAR/NMDAR/PSD candidates. In that review, `Cacng2` and `Cacng3` were assigned the primary-analog role; `Frrs1l`, `Gria1`, `Gria2`, `Gria3`, and `Dlg4` were AMPAR-module support nodes; NMDAR and downstream PSD genes were retained as boundaries. The response activity split was 10/18 with no significant focal features, 7/18 with 1 to 9 features, and only `Grin1` with at least 50.

## Target-specific reasoning

### Cacng8

`Cacng8` encodes TARP gamma-8, a four-pass AMPAR auxiliary subunit. The biology makes `Cacng2` and `Cacng3` the closest measured transfers: Tomita et al. placed gamma-2/stargazin, gamma-3, gamma-4, and gamma-8 in the classical TARP family, all acting on AMPAR surface expression; Rouach et al. then showed that gamma-8 is especially important for hippocampal AMPAR number and extrasynaptic localization. Herguedas et al. gives the direct structural mechanism for gamma-8 in GluA1/2 gating, so the analog class is AMPAR trafficking/gating rather than generic voltage-gated calcium-channel gamma subunits.

The two available TARP paralogs were completely quiet in the target cell group:

- `Cacng2`: 0 DEGs. The same-experiment corpus finding `Cacng2:F004` reported that represented AMPAR/TARP/PSD-95 relatives were flat or almost flat, with the caveat that `Cacng8`, `Cacng4/5/7`, `Cnih2/3`, and `Gria4` were not measured perturbations.
- `Cacng3`: 0 DEGs. Corpus finding `Cacng3:F003` reported no robust Cacng3-like genome-wide signature and no hidden AMPAR-neighbor module.

The receptor-core and scaffold checks point the same way. `Gria1`, `Gria2`, and `Gria3` each had 0 focal DEGs; `Frrs1l` and `Dlg4` had self-only focal calls; `Syngap1`, `Tanc2`, and `Camk2a` had 0. The Distributed Agents corpus high-confidence claim `claim:a9367c3aeaad95bfae9c` summarizes these same-experiment observations as: represented AMPAR-core and AMPAR-trafficking/scaffold perturbations are transcriptionally buffered in basal juvenile neurons rather than forming an interchangeable AMPAR-loss nuclear RNA program.

I treated `Grin1` as a counterexample rather than a positive analog. `Grin1` had 89 focal DEGs, showing that this cell group can report ionotropic glutamate-receptor perturbation as a nuclear RNA state. However, `Grin1` is the obligatory NMDAR pore subunit, while Cacng8 is an AMPAR auxiliary trafficking/gating subunit; the AMPAR subunit and TARP perturbations in the same input are much closer and are near-null.

The remaining question was whether to predict a single self-transcript DEG. I decided against it. `Frrs1l`, `Dlg4`, `Grin2a`, `Camk2b`, `Grik5`, `Cacnb4`, and `Cacna2d1` demonstrate that self-only calls are possible, but both directly assayed TARPs lacked focal self calls. External expression evidence also made a focal thalamic self call less compelling for Cacng8 than a hippocampal one: Yamasaki et al. observed lower TARP gamma-8 PET binding in rat thalamus than hippocampus. The acute P16 mosaic CRISPR design further argues against importing the broad electrophysiological or behavioral consequences of germline gamma-8 knockout as a guaranteed steady-state RNA response.

Therefore I predict no FDR-controlled focal rows for `Cacng8`: `predicted_n_degs = 0`.

## Limits and extrapolation

- This is an extrapolation from `Cacng2`, `Cacng3`, AMPAR-core genes, and PSD scaffolds; the training set did not include `Cacng8`, `Cacng4`, `Cacng7`, `Cnih2`, `Cnih3`, `Shisa6`, `Shisa7`, `Shisa9`, `Grip1/2`, or `Pick1` as direct perturbations.
- snRNA-seq cannot see AMPAR localization, surface abundance, gating kinetics, or synaptic currents, so a prediction of 0 DEGs is compatible with a real electrophysiological Cacng8 phenotype.
- Literature on gamma-8 is strongest in hippocampal and forebrain circuits and often uses germline nulls or pharmacology. The requested context is sparse, postnatal, mosaic CRISPR in thalamic recovered nuclei.
- The endpoint includes self-transcript loss. Average mRNA reduction in this screen is modest and not a direct editing-efficiency measure; I used the TARP-paralog self rows as calibration, but the hidden Cacng8 self row could in principle cross FDR even without any downstream response.
