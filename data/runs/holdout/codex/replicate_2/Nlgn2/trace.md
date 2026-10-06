# Nlgn2 `n_degs` forecast

Target and endpoint: `Nlgn2` in `151 TH Prkcd Grin2c Glut`, forecasting the number of measured genes with Wilcoxon BH-adjusted `p < 0.05`.

## Evidence used

- The declared holdout manifest and biology bundle both resolve the sole target to `Nlgn2`.
- Exact focal-population reach is high: in the non-target nuclei for `151 TH Prkcd Grin2c Glut`, `Nlgn2` is detected in 22,782 of 23,679 nuclei, or 96.2%, with mean 3.006 cp10k.
- The Nlgn2 functional-stock card calls the operative lesion likely substantially depleted by the P37-P44 harvest. The edit should stop resupply of a dynamic inhibitory-postsynaptic adhesion protein; NLGN2 turns over on a days-long scale in neuronal culture and adult conditional deletion clears detectable protein by about 2-3 weeks.
- The same card argues that NLGN2 loss can matter in thalamic neurons, but with important dampers for this endpoint: the direct thalamic loss-of-function physiology was developmental and region-restricted, the adult postmitotic evidence was cortical, major inhibitory-synapse remodeling can lag behind protein clearance, and the assayed `151` class aggregates thalamic glutamatergic populations.
- The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` table is strongly concentrated at the floor: among 1,674 training perturbations, 1,205 have 0 DEGs, 276 have 1, 31 have 2, 56 have 3-9, 47 have 10-49, and only 59 have at least 50.
- A typed mouse gene-analog nomination against that same training universe placed the closest available `Nlgn2` comparators in the neuroligin/neurexin/synaptic-adhesion neighborhood rather than among broad high-count chromatin or homeostasis hits. The direct or narrow candidates had very small observed counts in `151`: `Nlgn3` 1, `Dlg4` 1, `Nrxn2` 0, `Nrxn1` 1, `Nrxn3` 0, `Shank3` 2, `Lrrtm4` 0, `Lrrtm1` 1, `Lrrtm3` 0, `Gphn` 0, `Grm1` 1, `Dlgap4` 2, and `Arhgef9` 1. Their median was 1 and their log1p center was 0.63 DEGs.
- Exact Parquet rows for those direct/narrow candidates showed only 10 significant rows total. Most of the one-gene calls were either the perturbed transcript itself (`Arhgef9`, `Dlg4`, `Dlgap4`, `Grm1`, `Nlgn3`, `Nrxn1`, `Shank3`) or isolated non-recurring genes (`Vgf` for `Dlgap4`, `R3hdm2` for `Lrrtm1`, `Uba5` for `Shank3`), while `Gphn`, `Nrxn2`, `Nrxn3`, `Lrrtm3`, and `Lrrtm4` had none.
- A matched profile comparison over the top nominated synaptic candidates found no missing training profiles; 16 of 31 had no significant features, 14 had 1-9, and only the broad fallback `Grin1` had at least 50. Across 465 pairwise comparisons in that analog cohort, significant-program overlap was 0 in both directions wherever defined.

## Synthesis

The biology bundle makes an effective acute `Nlgn2` perturbation plausible in the assayed window, so I did not put the target at an assay-failure zero. The target is also well expressed in the focal population, so a single self-transcript or very local postsynaptic response is plausible.

The endpoint-specific training evidence argues strongly against a broad thalamic transcriptional state. The most relevant neuroligin/neurexin, Lrrtm, GABA-postsynaptic, and gephyrin-side comparators are all at 0-2 DEGs in the same cell class, and their significant rows do not form a shared downstream program. `Grin1` at 89 is an informative upper boundary for a much more central glutamatergic receptor subunit rather than a scale match for an inhibitory adhesion molecule.

I therefore placed `Nlgn2` at the low but nonzero analog center and rounded to one DEG.

Final prediction: `1`
