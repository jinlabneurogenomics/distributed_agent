# Camk4 direct prediction trace

## Endpoint

- **Target:** `Camk4`
- **Cell class:** `151 TH Prkcd Grin2c Glut`
- **Endpoint:** `n_degs`, the number of measured genes in the class with Wilcoxon `pvals_adj < 0.05`
- **Point prediction:** 9

## Evidence used

1. **Declared target identity and inputs**

   `codex_runtime/pipeline/task_bindings_receipt.json` declares a one-row holdout manifest whose exact target is `Camk4`. The declared training endpoint table is `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`; it has 1,674 observed training targets and no `Camk4` row. The declared Parquet `[local file: training_de_all_cell_groups.parquet]` is the matching training DE surface.

2. **Biology-only Camk4 bundle**

   The declared `Camk4.json` bundle reports exact focal expression in the matched non-target nuclei: `Camk4` is detected in 20,002 of 23,679 `151 TH Prkcd Grin2c Glut` cells, or 84.47%, with mean raw UMI 2.46 and pseudobulk CPM 154.48. This makes the perturbation reachable in the focal population, but per the bundle this expression measurement is not a target-knockdown efficiency readout.

   The same bundle adjudicates CAMK4 functional stock as `likely_substantially_depleted` by the P37-P44 harvest after P16 editing: CAMK4 is a renewed monomeric Ca2+/calmodulin-dependent kinase, the edit-to-harvest window is 21-28 days, and the selected turnover anchor is a 2.37-day CAMK4 lifetime in postmitotic cultured neurons. That supports a realized kinase perturbation while leaving uncertainty from mouse thalamic turnover, mosaic editing, survivor conditioning, and parallel CREB-regulating pathways.

3. **Absence of same-experiment Camk4 report context**

   `corpus.target_context(Camk4)` returned zero same-experiment Findings, Claims, and explicit report references in the selected release. I therefore did not use packaged report relations to nominate analogues for Camk4.

4. **Training counts for Camk4-pathway perturbations**

   The full 1,674-target training count table is sparse in this class: 1,205 targets have `n_degs = 0`; the median is 0, the 75th percentile is 1, the 90th percentile is 2, and the 95th percentile is 18. Counts for observed perturbations around the CaM/CAMK-CREB axis were low:

   - CaM family and CAMK relatives: `Calm1 = 14`, `Calm2 = 0`, `Calm3 = 1`, `Camk2a = 0`, `Camk2b = 1`, `Camk2g = 0`
   - downstream or parallel transcriptional regulators: `Creb1 = 10`, `Crebbp = 8`, `Mef2a = 4`, `Mef2c = 1`, `Mef2d = 0`, `Jund = 0`, `Rora = 278`
   - adjacent signaling controls: `Ppp3ca = 4`, `Ppp3cc = 0`, `Ppp3r1 = 9`, `Prkaca = 1`, `Mapk1 = 0`, `Mapk9 = 0`

   I treated `Rora = 278` as an upper-scale boundary, not as the local center: RORA is named as a CAMK4-regulated transcription factor in the biology card, but perturbing a developmental nuclear receptor is not the same operation as removing the upstream signal-dependent kinase.

5. **Training expression signatures**

   I compared those 19 observed CaM/CAMK/CREB/MEF/calcineurin/PKA/MAPK/Rora training perturbations in the declared Parquet, restricted to `group_name = "151 TH Prkcd Grin2c Glut"`, using `logfoldchanges` as the signed profile and `pvals_adj < 0.05` as the significant-gene flag. The resulting cohort had 19 profiles and 171 complete pairwise comparisons. Positive significant programs had median pairwise overlap 0 and mean overlap coefficient 0.00397; negative significant programs also had median overlap 0 and mean overlap coefficient 0.0333. Thus the few 1-14 DEG responses in the most proximal observed analogues did not hide a large coherent state, and the Rora-scale response was not supported as a shared CAMK-pathway module.

## Synthesis

`Camk4` is a better-than-null target because it is expressed in most focal thalamic nuclei and its renewable kinase stock should be depleted by harvest if editing succeeds. I therefore moved above the screen-wide median and above the many silent related kinases. At the same time, the expected perturbation is a loss of a signal-dependent transcriptional kinase in unstimulated recovered neurons, not deletion of a core spliceosome, proteasome, or chromatin regulator; the bundle also leaves thalamic postnatal coupling and pathway redundancy unresolved. The task-matched counts for the nearest observed perturbations put that scale in the high single digits to low teens (`Creb1 = 10`, `Crebbp = 8`, `Ppp3r1 = 9`, `Calm1 = 14`), with weak shared-profile support and a strong reason not to anchor on `Rora = 278`.

I therefore predicted a small but nonzero focal response: **9 DEGs**.
