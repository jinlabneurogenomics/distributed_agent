# Col4a1 n_degs forecast

Target and endpoint:

- Target manifest: `Col4a1`
- Cell class: `151 TH Prkcd Grin2c Glut`
- Endpoint: number of measured genes with BH-adjusted Wilcoxon `p < 0.05`

Evidence used:

- The declared biology-only `Col4a1` bundle reports exact focal-population reach for the target transcript: in non-target nuclei from `151 TH Prkcd Grin2c Glut`, `Col4a1` was available, expressed in 17,735 / 23,679 cells, with mean raw UMI 2.43 and mean CP10K 1.52. This supports enough local transcript abundance for a self-target contrast to be detected, but it does not reveal the held-out perturbation log-fold change or DEG count.
- The same bundle characterizes COL4A1 as a secreted structural chain of the installed alpha1-alpha1-alpha2 type IV collagen basement-membrane network. A P16 disruptive edit should stop new edited-cell supply but should not immediately remove matrix deposited before editing; the card adjudicates functional stock at P37-P44 as only `partially_depleted_or_leading_edge`.
- The adult brain prior in the bundle places major `Col4a1` expression in vascular/perivascular compartments rather than neurons, and the postnatal turnover evidence is from cerebral vessels rather than selectively edited thalamic neurons. I treated this as limiting confidence in a strong cell-autonomous neuronal state despite the exact in-assay RNA reach.
- The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` table is zero-heavy: 1,205 / 1,674 training perturbations have `n_degs = 0`, and the median is 0. The high tail is dominated by intracellular splicing, chromatin, proteostasis, and trafficking genes rather than extracellular structural genes.
- Available extracellular-matrix, collagen, adhesion, and matrix-receptor-adjacent training perturbations were quiet in the same endpoint. In a 27-gene hand-selected check from the count table, 21 had 0 DEGs and the median was 0; the closest structural ECM rows were `Col2a1 = 0`, `Col11a1 = 0`, `Fbn1 = 0`, `Dag1 = 0`, and `Itgb1 = 0`. Single-count neighbors such as `App`, `Ncam1`, `Nrxn1`, and `Timp3` were explained in the raw focal Parquet by self-transcript detection with no broad downstream program.

Synthesis:

`Col4a1` is more reachable than the silent collagen rows because its transcript is detected in most focal nuclei, so I do not want to force the prediction to the all-zero structural-ECM median. The functional product, however, is an extracellular pre-installed network with partial persistence over the 21-28 day window and an unresolved neuronal postnatal requirement, and the matched training perturbations do not support a broad ECM or adhesion response in recovered thalamic neurons. I therefore forecast one significant feature, corresponding to a likely self-transcript hit and little to no additional downstream transcriptional response.

Predicted `n_degs`: 1

No target outcome, target expression signature, labeled-neighbor outcomes, scalar-prior, calibrated-probability, branch-calibration, relationship-review, or terminal-prediction artifact was used to choose this value.
