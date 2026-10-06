# Xpo1 direct DEG-count forecast

## Target and endpoint

- Target: `Xpo1`
- Cell class: `151 TH Prkcd Grin2c Glut`
- Endpoint: measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05` in the focal class.
- Declared target expression reach: `Xpo1` was broadly detected in the focal non-target population, with 20,869 / 23,679 nuclei expressing it, 88.13% expressing cells, mean raw UMI 2.59, and mean log1p CP10K 0.871. This makes the transcript reachable but was used only as reach evidence, not as an editing-efficiency estimate.

## Biology bundle

The canonical biology bundle supports target engagement by harvest in successfully edited cells:

- XPO1 is a soluble Ran-regulated nuclear-export receptor for leucine-rich NES protein cargoes and RNA-containing complexes.
- The perturbation stops new intact XPO1 synthesis but does not instantly remove existing receptor.
- Adult mouse thalamus has an Xpo1 protein lifetime of 7.444 days; a 21-28 day post-edit interval spans about 2.8-3.8 lifetimes, leaving roughly 14%-7% of the starting pool under a no-resupply exponential approximation.

This argued against treating `Xpo1` like a long-lived installed structure whose molecular loss would be unlikely within the assay window. The two main downward caveats were endpoint-specific:

- Other exporters, especially XPO7, can buffer some cargoes but do not duplicate the full XPO1 client set.
- The readout is survivor-conditioned; cells with the strongest nuclear-export defect could be depleted or fail recovery, making the surviving snRNA signature smaller than the functional lesion.

## Training scale

The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` table contains 1,674 measured training perturbations and is dominated by small counts:

- 1,205 / 1,674 have `n_degs = 0`.
- The median is 0, the 75th percentile is 1, the 90th percentile is 2, and the 95th percentile is 18.
- The upper tail is very large but rare: 430 at the 99th percentile and a maximum of 2,677.

So the quantitative default in this focal class is zero or one DEG unless there is positive evidence for a broad RNA-processing, proteostasis, or nuclear-logistics state.

## Comparator evidence actually used

I used the curated mouse gene-analog nomination over the exact training universe to avoid symbol-only comparator choice. The useful nominees were heterogeneous:

- `Xpo7`, the closest training-available export receptor by annotation, had `n_degs = 0`.
- `Ranbp2`, the strongest direct physical XPO1 contact in the available pool, had `n_degs = 0`.
- `Setbp1`, the sole exact-complex nomination through a Setbp1-Xpo1 complex, had `n_degs = 0`.
- Other export or nucleocytoplasmic nominees were mostly quiet: `Ddx39b = 0`, `Adar = 0`, `Kpna3 = 0`, `Fmr1 = 0`, `Hnrnpa2b1 = 11`.
- Broader nuclear-logistics comparators could be much larger: `Thoc1 = 303`, `Tnpo3 = 618`, and `Tpr = 1768`.

Same-experiment corpus Findings, used as interpretation of these observed training profiles rather than independent replication, marked `Kpna3` as a near-null nuclear-transport perturbation and `Tnpo3`/`Tpr` as large but mechanistically narrower states: `Tnpo3` aligned with an SR-splicing/RNA-processing module, while `Tpr` aligned with a nuclear-basket/mRNA-export module and recurrently altered NXF1-adjacent export genes. Those high-count states are therefore upper-context comparators, not direct scale donors for CRM1 loss.

I then compared a 14-gene export/transport cohort directly in the declared `training_de_all_cell_groups.parquet` for `151 TH Prkcd Grin2c Glut`. The closest mechanistic nodes were flat:

- `Xpo7` and `Ranbp2` each had 17,259 available focal features and 0 significant features.
- `Xpo7` had no significant-feature intersections with broader responders such as `Prpf6`, `Cdc40`, `Psmb4`, or `Psmc1`; its nearest eligible outside neighbors were not export factors.
- `Ranbp2` was similarly quiet and had no significant intersections with the broad responders.
- In the same profile comparison, the high-count anchors remained clearly active: `Tnpo3` had 618 significant features, `Tpr` had 1,768, and `Thoc1` had 303.

## Synthesis

I placed `Xpo1` above the focal-class zero/one default because the target is broadly expressed in the assayed nuclei and XPO1 protein should substantially turn over during the 21-28 day window. I placed it far below the `Thoc1`/`Tnpo3`/`Tpr` broad-response branch because:

- the closest export receptor and physical-contact comparators were exactly zero in the requested cell class;
- the large training signatures were spliceosome, proteasome, or mRNA-export/nuclear-basket states rather than generic nuclear export;
- XPO7/other exporter buffering and survivor-conditioned sampling both attenuate the observed nuclear-RNA footprint.

My point forecast is therefore a very small, nonzero focal signature: **4 DEGs**.
