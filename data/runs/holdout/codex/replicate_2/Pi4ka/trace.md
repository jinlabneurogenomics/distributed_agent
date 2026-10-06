# Pi4ka n_degs forecast

## Endpoint

The requested endpoint is `n_degs`: the number of measured genes in `151 TH Prkcd Grin2c Glut` with BH-adjusted Wilcoxon `pvals_adj < 0.05`.

Prediction:

```tsv
target_name	predicted_n_degs
Pi4ka	1
```

## Evidence used

- Declared biology bundle for `Pi4ka`
  - Pi4ka is expressed across the focal population: 22,732/23,679 non-target nuclei in `151 TH Prkcd Grin2c Glut` expressed the feature, with 96.0% expressing cells, mean raw UMI 4.61, mean CP10K 2.86, and pseudobulk CPM 289.1.
  - The perturbation should be biologically reachable by harvest: editing at P16 stops new PI4KA supply, adult mouse deletion can deplete PI4KA protein in permissive tissues over days, and once PI4KA catalytic supply is lost the plasma-membrane PI4P product has minute-scale turnover.
  - The reach evidence is incomplete for the exact assayed state. Existing adult systemic and Schwann-cell data do not directly measure edit-to-PI4KA-stock loss in postmitotic thalamic neurons, and Schwann-cell preservation of some lipid pools means buffering can be pool-specific.

- Declared count table, `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`
  - The focal response scale is sparse in the training perturbations: 469/1,674 are nonzero at `pvals_adj < 0.05`, the median is 0, the 75th percentile is 1, 106/1,674 have at least 10 DEGs, and 43/1,674 have at least 100 DEGs.
  - Direct phosphoinositide or endosomal-phosphoinositide comparators in the table sit at the near-null floor:
    - `Pi4kb`: 1
    - `Dgke`: 1
    - `Synj1`: 1
    - `Inpp5k`: 0
    - `Ocrl`: 0
  - Less direct membrane-traffic or stress comparators can respond, but they are not specific PI4KA plasma-membrane PI4P analogues:
    - `Cltc`: 3
    - `Vps35`: 17
    - `Vps54`: 31
    - `Tsc2`: 86
    - `Atp2a2`: 187
    - `Rab7`: 501

- Raw signed profiles from `training_de_all_cell_groups.parquet`
  - I compared `Pi4kb`, `Dgke`, `Synj1`, `Inpp5k`, and `Ocrl` in the focal class against the broader membrane-stress comparators above.
  - Each close PI-cycle profile had 17,259 measured features and 0 or 1 significant feature at `pvals_adj < 0.05`.
  - The close PI-cycle cohort did not form a recurrent significant program: there was no positive significant-feature overlap among the five close nodes, and the only negative significant overlap coefficient among the pair set was 0.
  - The close nodes had no significant same-direction intersections with `Rab7`, `Tsc2`, `Atp2a2`, `Vps35`, `Vps54`, or `Cltc`; the focal response of those broader stress genes therefore looks like a looser upper reference, not a program to transfer directly onto Pi4ka.

- Same-experiment corpus Findings, used only for measured training comparators
  - The corpus described `Pi4kb`, `Ocrl`, `Inpp5k`, `Dgke`, and `Synj1` as buffered or near-null in this screen, with Pi4kb showing only tiny FDR signal and no robust phenocopy among represented phosphoinositide comparators.
  - `Rab7`, `Atp2a2`, and `Vps35` demonstrate that this cell class can report lysosomal, ER-stress, and retromer perturbations, but their Findings place those responses in endolysosomal or proteostasis states rather than a close PI4KA-loss state.
  - These corpus records and the Parquet summarize the same perturbation experiment; I used them as interpretation of the training rows, not as independent replication.

I did not query a Pi4ka same-experiment report, Pi4ka rows from the DE Parquet, or any target outcome/count artifact.

## Synthesis

Pi4ka has two upward bearings relative to the all-target prior: it is expressed in almost all recovered focal neurons, and its continuously renewed PI4P product should fall once existing PI4KA enzyme stock turns over. Those facts make a pure "gene absent or unedited" null less compelling.

The quantitative training evidence pulls harder downward. The closest measured PI-cycle and phosphoinositide comparators are all at 0 or 1 DEG in exactly the requested `151 TH Prkcd Grin2c Glut` count table, and their raw profiles do not share a significant gene program that would justify projecting a larger coherent PI response. The stronger `Rab7` and `Atp2a2` signatures are clear evidence that the assay can detect stress when it enters a lysosomal or ER-UPR state, but PI4KA is a plasma-membrane PI4P supply perturbation with documented pool-specific buffering, so I treated those larger signatures as ceilings rather than analogues.

The resulting point estimate is therefore just above zero: one FDR-significant feature, consistent with either the target transcript or a single small compensatory transcript passing threshold, and below the modest Vps/lysosome scales.
