# Sdhb n_degs forecast

Target: `Sdhb` in `151 TH Prkcd Grin2c Glut`.

Prediction: `1` measured gene with BH-adjusted Wilcoxon `p < 0.05`.

## Evidence used

- The one-row holdout manifest is `[local file: Sdhb.csv]`, and the target is exactly `Sdhb`.
- The outcome-blind `Sdhb` biology bundle reports exact focal-class expression reach: the transcript is available in `151 TH Prkcd Grin2c Glut`, with mean raw UMI 1.409, mean log1p CP10K 0.535, and 16,626 of 23,679 non-target nuclei expressing it. I treated this as evidence that the self transcript is observable, not as an editing-efficiency estimate.
- The same bundle places SDHB as the obligate iron-sulfur electron-transfer subunit of mitochondrial complex II and adjudicates the 21-28 day P16-to-P37/P44 window as long enough for substantial turnover of pre-edit thalamic SDHB protein. That supports a real complex-II lesion being reachable, with residual uncertainty from bulk thalamus protein half-life, unknown reserve complex-II activity, and survivor-conditioned snRNA-seq.
- The focal training count table `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]` is very sparse: among 1,674 training targets, 1,205 have `n_degs=0`, 276 have `n_degs=1`, the median is 0, the 75th percentile is 1, and counts above 20 are in the upper tail.
- The closest represented complex-II perturbation is `Sdha`, whose `151 TH Prkcd Grin2c Glut` training count is `1`.
- Direct focal Parquet rows from `[local file: training_de_all_cell_groups.parquet]` show that `Sdha`'s only BH<0.05 focal feature is `Sdha` itself (`pvals_adj=2.11e-12`); its next focal candidate, `Edem2`, has `pvals_adj=0.0646` and therefore does not enter this endpoint.
- In the same Parquet slice, represented TCA and OXPHOS targets were mostly null or self-only in the focal group. A 50-target mitochondrial/TCA cohort drawn from the training table had 27 zero-count targets, 21 one-count targets, and only two 10-49-count exceptions (`Opa1`, `Mdh1`).
- `Opa1` and `Mdh1` were not used as scale analogs for `Sdhb`: `Opa1` is a mitochondrial dynamics perturbation with a detectable ISR-like state, and `Mdh1` is a cytosolic malate-dehydrogenase perturbation. The SDH and respiratory-chain subunits were the more local evidence.
- Packaged same-experiment `Sdha` Findings, interpreted as annotations of the same Perturb-seq experiment rather than independent replication, call `Sdha` broadly buffered: no HIF/pseudohypoxia, mitochondrial ISR/UPRmt, NRF2/redox, or broad ER/ISR program was recovered, and the available TCA/OXPHOS targets did not phenocopy a common module.
- A full signed-profile neighbor scan for `Sdha` in the exact focal class produced no mitochondrial nearest-neighbor cluster, and a 50-node mitochondrial cohort diagnostic showed median top-tail overlap of only 0.025 in both directions. I therefore used the cohort as local count-scale evidence, not as a transferable multi-gene program.

## Synthesis

`Sdhb` should be expressed well enough in the assayed focal nuclei for its own transcript to be counted if editing makes the row significant. Biology argues that the edit can reach SDHB function by harvest, but the closest measured complex-II loss, `Sdha`, and the broader respiratory-chain/TCA training cohort both argue against a large downstream transcriptional state in acute postmitotic thalamic neurons. Most local metabolic subunits gave either zero significant rows or only their self transcript; the rare larger mitochondrial signatures came from less direct state perturbations.

I therefore forecast the same endpoint scale as `Sdha`: one BH<0.05 row, most likely the target transcript itself, with no confident additional downstream genes.
