# Gapdh DEG-count forecast

Target:

- `Gapdh` in `151 TH Prkcd Grin2c Glut`.
- Endpoint: measured genes with BH-adjusted Wilcoxon `p < 0.05`.

Evidence used:

- The one-row holdout manifest names `Gapdh`; the selected same-experiment
  Finding/Claim release has no `Gapdh` Finding or Claim records, so no packaged
  Gapdh outcome was used.
- The canonical `Gapdh` biology bundle supports biochemical realization but not
  a large task-matched transcriptional response. A productive P16 edit should
  stop new cytosolic GAPDH supply, the soluble pool is expected to turn over
  materially by the P37-P44 harvest, and `Gapdhs` is germline-restricted rather
  than a neural replacement. Counterweights are that the direct P16-to-P37/P44
  thalamic phenotype is unknown, residual catalytic reserve is unknown, and
  exact in-assay thalamic `Gapdh` expression was unavailable with
  `feature_status = excluded_as_unused_gene`.
- The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` table is
  heavily zero-inflated: 1205/1674 training perturbations have `n_degs = 0`,
  the median is 0, and 1481/1674 have at most one DEG.
- I used direct glycolysis comparators from the declared training table rather
  than broad essential RNA-processing or proteostasis genes: `Hk1 = 1`,
  `Gpi1 = 1`, `Pfkm = 1`, `Tpi1 = 1`, and `Eno1 = 0` in the exact focal
  population. Querying the declared parquet for those rows showed that the lone
  `151 TH Prkcd Grin2c Glut` significant row for `Hk1`, `Gpi1`, `Pfkm`, and
  `Tpi1` was the target transcript itself; `Eno1` had no significant row.
- The packaged reports for the same training glycolysis perturbations interpret
  the matched experiment as a buffered central-glycolysis surface: `Hk1` was a
  pan-neuronal downstream null, `Pfkm` had zero downstream FDR<0.10 genes in
  every measured neuronal group despite self-RNA depletion in several groups,
  `Gpi1` was near-origin, `Tpi1` produced only a tiny isolated downstream
  response outside this target class, and `Eno1` was a corrected null. These
  records are semantic summaries of the same Perturb-seq experiment, not
  independent replication.

Reasoning:

`Gapdh` is a renewed cytosolic glycolytic enzyme, so it is a plausible
biochemical perturbation by harvest, but the closest measured single-node
central-glycolysis losses were not large `151 TH Prkcd Grin2c Glut`
responders. In the exact focal population their apparent one-gene counts were
self-transcript calls, not downstream stress programs. Because the `Gapdh`
expression feature was unavailable, an analogous self-only hit would not add a
measured DEG for `Gapdh`. I therefore projected the buffered-glycolysis
downstream count rather than the all-gene one-count artifact and rounded to the
modal low endpoint.

Predicted `n_degs`: 0
