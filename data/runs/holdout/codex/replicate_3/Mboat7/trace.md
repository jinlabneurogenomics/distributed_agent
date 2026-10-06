# Mboat7 DEG-count forecast

## Target and endpoint

- **Target:** `Mboat7`
- **Cell class:** `151 TH Prkcd Grin2c Glut`
- **Endpoint:** `n_degs`, the count of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`
- **Prediction:** **1 DEG**

## Biology used

The canonical `Mboat7` biology bundle supports target engagement but not a
large, rapidly amplified RNA state:

- Exact focal-population reach is high: `Mboat7` is expressed in
  17,659 / 23,679 non-target nuclei in `151 TH Prkcd Grin2c Glut`
  (`74.58%`; pseudobulk CPM `105.48`).
- MBOAT7/LPIAT1 catalyzes arachidonoyl-CoA transfer to lysophosphatidylinositol
  in the phosphatidylinositol Lands cycle.
- The functional-stock card calls the 21-28 day P16-to-harvest window
  **likely substantially depleted** because newly synthesized enzyme should stop
  and the arachidonoyl-PI pool is actively remodeled.
- Two parts weaken a large-response extrapolation: residual enzyme and
  pre-edited PI can persist until protein and lipid-carrier turnover, and the
  direct mouse neural phenotype is germline/developmental cortex-hippocampus
  rather than a matched postnatal thalamic-neuron loss time course.
- The bounded paralog search in the bundle found no close postmitotic-neuron
  compensating enzyme, so I did not force the estimate to zero on redundancy
  grounds.

## Training endpoint scale

The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` table contains
1,674 visible training targets. The endpoint is very sparse:

- 1,205 / 1,674 training perturbations have `n_degs = 0`.
- The median is 0, the 75th percentile is 1, the 90th percentile is 2, and the
  95th percentile is 18.
- The largest counts are a small long tail, led by broad essential regulators
  such as `Uba5 = 2677`, `Tpr = 1768`, `Sin3a = 1433`, and spliceosome,
  proteasome, chromatin, or core transcriptional regulators.

That distribution makes a high count require a strong operation-matched reason,
not just general cellular importance.

## Training analogs

I nominated training-available `Mboat7` comparators from the curated
mouse-annotation store and the selected PerturbAI corpus release. No exact
complex/paralog, bidirectional corpus comparator, narrow module, or direct
interaction/dependency candidate was present; all 787 candidates were
`broad_functional_fallback` matches.

The most operation-relevant broad matches were quiet in the count table:

- `Dgke`, the only direct `phosphatidylinositol biosynthetic process`
  training candidate in the nomination output: `1`
- direct `phosphatidylinositol metabolic process` candidates:
  `Ddhd1 = 0`, `Pik3r1 = 0`, `Plcb1 = 0`, `Synj1 = 1`
- Reactome `Phospholipid metabolism` direct candidates around the PI kinase /
  phosphatase subnetwork:
  `Agk = 0`, `Ddhd1 = 0`, `Ddhd2 = 0`, `Inpp5k = 0`, `Ocrl = 0`,
  `Pi4kb = 1`, `Pik3cb = 0`, `Pik3r1 = 0`, `Pik3r2 = 0`, `Selenoi = 5`,
  `Stard7 = 25`
- `Acsl4`, a lipid/ER candidate relevant to arachidonoyl-CoA handling: `1`

The broader lipid and ER fallback sets contain occasional high outliers, but
those are dominated by generic ER stress, transcriptional, or developmental
links rather than the PI acyl-chain remodeling operation closest to `Mboat7`.

## Expression-profile check

I compared a bounded PI/lipid cohort in the exact thalamic class using the
declared Parquet with `logfoldchanges` as the signed profile value and
`pvals_adj < 0.05` as significance:

`Dgke, Ddhd1, Pik3r1, Inpp5k, Acsl4, Pi4kb, Plcb1, Ocrl, Synj1, Ddhd2, Agk,
Pik3cb, Pik3r2, Srebf2, Hspa5, Ctnnb1`

All 16 profiles were present. Nine had no significant genes; six had only
1-9 significant genes; `Ctnnb1` was the sole large outlier with 383 and was
also isolated from the PI component in the explicit Finding-reference topology.
Across the 120 selected pairs, the shared positive significant program had no
overlap, and the negative significant-program overlap was present for only
15 pairs with median overlap coefficient 0. The profile check therefore
supports the count-table impression: there is a weakly connected PI/lipid
neighborhood, but it is not a coherent high-response transcriptomic module in
`151 TH Prkcd Grin2c Glut`.

## Synthesis

`Mboat7` is expressed in most assayed thalamic nuclei, its lipid product should
be at least partly renewed during the 21-28 day CRISPR window, and there is no
specific compensating paralog; those are enough to forecast a real chance of a
nonzero sparse DE footprint. The closest measured phosphatidylinositol and
glycerophospholipid perturbations, however, almost all fall at `0` or `1` DEG,
and no same-operation high-count donor was found. I therefore placed `Mboat7`
just above the screen's zero mass rather than in the long responsive tail:

`predicted_n_degs = 1`
