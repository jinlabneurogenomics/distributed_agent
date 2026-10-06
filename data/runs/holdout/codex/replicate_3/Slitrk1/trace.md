# Slitrk1 n_degs forecast

Target and endpoint: `Slitrk1`, predicted as the number of genes in
`151 TH Prkcd Grin2c Glut` with BH-adjusted Wilcoxon `p < 0.05`.

## Evidence used

- The one-row holdout manifest names `Slitrk1`; it is absent from
  `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- The held-in focal-class count table has 1,674 targets. Its distribution is
  strongly zero-inflated: median `n_degs = 0`, p75 `= 1`, p90 `= 2`, p95
  `= 18`, and p99 `= 430`.
- The canonical `Slitrk1` biology bundle supports target reach and realization:
  in the matched non-target nuclei for `151 TH Prkcd Grin2c Glut`, Slitrk1 is
  detected in 20,550 of 23,679 nuclei, `86.7858%`, with mean CP10K `1.9254`.
  Its functional-stock card adjudicates the postsynaptic SLITRK1 pool as
  likely substantially depleted over the P16 to P37-P44 interval, based on
  adult postmitotic Slitrk1 deletion reducing puncta and changing excitatory
  synaptic properties within two to three weeks.
- The same bundle places SLITRK1 as a postsynaptic excitatory adhesion protein
  acting through presynaptic LAR-family receptor phosphatases, especially
  `Ptprd` and `Ptprs`; `Ptprs` was not present in the focal training count
  table, while `Ptprd` was.
- I used the held-in count table and the focal-class Parquet rows for synaptic
  adhesion, synaptic scaffold, guidance/adhesion, and glutamate-receptor
  comparators:

  ```text
  Ptprd 0, Ptprf 0, Nrxn1 1, Nrxn2 0, Nrxn3 0,
  Nlgn3 1, Lrrtm1 1, Lrrtm3 0, Lrrtm4 0,
  Cadm2 1, Cntnap1 1, Cntnap2 1,
  Dlg4 1, Shank2 0, Shank3 2,
  Grin1 89, Grin2a 1, Grin2b 2,
  Epha4 1, Robo1 1
  ```

  The median of these 20 local perturbations is 1. Excluding the mechanistically
  sharper `Grin1` outlier, the mean is 0.68 and all remaining counts are 0-2.
- A symmetric Parquet profile comparison over those 20 perturbations found no
  tight shared positive or significant program in `151 TH Prkcd Grin2c Glut`.
  Seven nodes had no significant features, twelve had 1-9 significant features,
  and only `Grin1` had at least 50.
- The same-experiment Finding ledger summarized the corresponding full surfaces
  as transcriptionally buffered or almost flat for the closest classes:
  `Ptprd` and `Ptprf` were broad FDR-null responders; `Nlgn3` was a downstream
  null in all recovered groups; `Nrxn1` was limited to one Pvalb downstream
  gene; `Lrrtm1` had a single downstream DEG across all measured tests; `Robo1`
  was FDR-null despite on-target RNA depletion in several classes; and `Shank3`
  was a two-singleton surface including one downstream hit in this focal class.
  The ledger separately treated `Grin1`/`Grin2a`/`Grin2b` as NMDAR-subunit
  responses that diverged from PSD and adhesion comparators.

## Synthesis

The exact focal-class expression and functional-stock card argue against
calling `Slitrk1` biologically unreachable: edited expressing thalamic neurons
should lose renewable SLITRK1 during the assay window. The quantitative
training evidence, however, puts acute loss of synaptic adhesion/scaffold
surface molecules very close to a transcriptional null in this endpoint.
Direct LAR-family and neurexin/neuroligin/LRRTM/CADM/CNTNAP comparators are
0-1 DEG perturbations in the focal count table, and the Parquet profile
comparison did not expose a coherent active synaptic module that would justify
borrowing the larger `Grin1` response.

I therefore placed `Slitrk1` at the low but nonzero synaptic-adhesion center:
mostly buffered at the downstream snRNA level, with the high baseline reach and
expected protein depletion allowing one FDR-significant measured gene rather
than a hard zero.

Predicted `n_degs`: `1`.
