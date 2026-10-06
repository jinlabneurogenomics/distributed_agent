# Held-out perturbation evaluation

This directory contains the measurements and annotations used to evaluate saved
DEG-count predictions for 272 held-out perturbations in
`151 TH Prkcd Grin2c Glut` cells. DEG counts use `pvals_adj < 0.05`.

- [Training counts](151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv): observed
  counts for 1,674 non-held-out targets.
- [Held-out counts](151_TH_Prkcd_Grin2c_Glut_deg_counts_holdouts.csv) and
  [measurements](measurements.csv): evaluation outcomes for the 272 targets.
- [Holdout registry](holdout_perturbations.csv): selection metadata, including
  one additional safe-targeting control outside the 272-target evaluation set.
- [Prediction prompt template](deg_count_prediction.md): the task definition
  used to generate the saved predictions.
- The remaining tables contain reviewed case annotations and biological
  comparisons used in the manuscript figures.

Saved answers and reasoning are bundled in
[`distributed_agents`](../../runs/holdout/distributed_agents/) and
[`codex`](../../runs/holdout/codex/), each with `replicate_1` through `replicate_3`.
Each replicate contains one directory per target. Distributed Agents replicate 1
combines the initial 10-target run with the remaining 262 targets; replicates 2
and 3 are the toolbox runs.

Run `python -m manuscript_figures.prepare` from an editable installation to
rebuild the evaluation tables, then execute
[`fig3.ipynb`](../../../notebook/fig3.ipynb) and
[`figS9.ipynb`](../../../notebook/figS9.ipynb). Reproducing these analyses uses the
bundled answers and measurements and requires no model calls or external files.
