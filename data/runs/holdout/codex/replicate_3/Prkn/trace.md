# Direct n_degs forecast for Prkn

Target and endpoint:

- Target: `Prkn`
- Focal population: `151 TH Prkcd Grin2c Glut`
- Endpoint: number of measured genes with BH-adjusted Wilcoxon `p < 0.05`
- Point prediction: `1`

Evidence used:

- The canonical `Prkn` biology bundle shows that the target transcript is measurable in the requested focal population: `Prkn` is detected in 16,623 of 23,679 non-target focal nuclei, with `pct_cells_expressing = 70.2014`, `mean_raw_umi = 1.4276`, and `pseudobulk_cpm = 89.4697`. This makes a focal assay effect possible, but the same bundle keeps the functional effect uncertain: Parkin is a cytosolic or mitochondria-recruited catalytic RBR E3 whose activity is PINK1/phospho-ubiquitin dependent, existing Parkin protein persisted across a 6 hour neuronal translation-block chase, and no fact measures Parkin protein clearance across the 21 to 28 day P16-to-harvest interval.
- The focal training count table is highly concentrated at the floor. Among 1,674 non-held-out training perturbations in `151 TH Prkcd Grin2c Glut`, 1,205 have `n_degs = 0`, the median is `0`, the 75th and 80th percentiles are `1`, and the 90th percentile is `2`.
- The closest represented basal PINK1/Parkin, mitophagy, and autophagy comparators in the count table are all flat or nearly flat at the requested FDR cutoff in the focal class: `Atg5 = 0`, `Rhot1 = 0`, `Snca = 0`, `Atp13a3 = 0`, `Park7 = 1`, `Sqstm1 = 1`, and `Vcp = 2`. Exact Parquet rows for `151 TH Prkcd Grin2c Glut` showed that the one significant row for `Park7` was `Park7` itself and the one significant row for `Sqstm1` was `Sqstm1` itself; their inspected focal profiles had no significant-feature intersection with `Atp13a2`, `Atp13a3`, `Snca`, `Vps35`, `Hspa5`, `Opa1`, or `Tsc2`.
- Packaged same-experiment Findings gave the sparse counts a biological interpretation. `Park7` was annotated as a basal juvenile-neuron null with no FDR-significant downstream response across recovered neuronal groups and no induction of NRF2, UPR/ISR, autophagy, or PINK1/Parkin-mitophagy sentinel transcripts. `Rhot1` lacked an Opa1-like mitochondrial ATF4/ISR state and had no meaningful whole-parquet neighbor. `Atg5` was restricted to a two-gene `155 MB Glut` response, not a pan-neuronal autophagy, p62, lysosome, proteasome, or UPR/ISR program. `Sqstm1` produced only isolated single-gene responses, and canonical p62-adjacent NRF2/redox, lysosomal-autophagy, UPR, and ISR transcripts were absent from its FDR surface.
- I treated `Hspa5`, `Opa1`, `Vps35`, and `Tsc2` as boundaries rather than point comparators. They can move RNA in `151 TH` (`5`, `37`, `17`, and `86` genes respectively), showing that the class has power to detect organelle and proteostasis stress, but they are direct UPR, mitochondrial inner-membrane, retromer, or mTOR/lysosome stressors rather than unchallenged Parkin loss. In the matched profile comparison, `Park7` and `Sqstm1` had near-zero or negative cosines to these broader responders, while only `Vcp` weakly approached `Hspa5` and it still had just two significant genes at `p_adj < 0.05`.

Synthesis:

The held-out perturbation is reachable at the RNA level in this thalamic population, but the expected basal effect is very small. Parkin loss stops new supply of a conditionally recruited E3 ligase rather than directly blocking a core house-keeping complex, the stock remaining by 3 to 4 weeks is unknown, and the closest represented mitophagy/Parkinson/autophagy training perturbations are either null or self-transcript-only in this focal group. The stronger mitochondrial and proteostasis responders bound the assay's sensitivity but are too mechanistically severe to transfer their tens of DE genes to `Prkn`.

I therefore placed `Prkn` at the floor of the training distribution, allowing for at most an isolated self or one-gene effect because `Prkn` is detected in most focal non-target nuclei. No `Prkn` target outcome, `Prkn` DE signature, calibrated response probability, labeled-neighbor outcome, relationship-review artifact, branch-calibration artifact, or scalar-prior artifact was used.
