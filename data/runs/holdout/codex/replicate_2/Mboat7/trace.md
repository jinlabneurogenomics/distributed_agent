# Trace

Target: `Mboat7` in `151 TH Prkcd Grin2c Glut`.

The requested endpoint is the direct BH-adjusted Wilcoxon DEG count in this one
thalamic glutamatergic class.

Evidence used:

- The declared holdout manifest contains only `Mboat7`; `Mboat7` is absent from
  the 1,674-row training count table.
- The biology bundle gives exact in-assay focal reach for the target:
  `Mboat7` RNA is present in 17,659 of 23,679 matched non-target nuclei
  in `151 TH Prkcd Grin2c Glut` (74.58%; mean raw UMI 1.68; mean CP10k 1.07).
  Thus the assayed cells express the gene often enough that a target-transcript
  hit is plausible.
- The same bundle adjudicates the functional stock as likely substantially
  depleted by the P37-P44 harvest because MBOAT7 supplies arachidonoyl
  phosphatidylinositol in an active deacylation/reacylation cycle. Confidence is
  limited: the positive phenotype evidence is developmental cortex/hippocampus
  from germline loss, and no matched postnatal thalamic neuron clock for MBOAT7
  protein or arachidonoyl-PI carrier turnover was available.
- The target count distribution in the `151 TH Prkcd Grin2c Glut` training table
  is sharply concentrated at no or one significant gene: 1,205/1,674 targets are
  0, the median is 0, the 75th percentile is 1, and only 103/1,674 exceed 10.
- I treated the lipid/phosphoinositide training perturbations as the most
  interpretable analogs. Their focal counts were uniformly near-null:

  | perturbation | focal `n_degs` | BH<0.05 rows in the focal Parquet |
  | --- | ---: | --- |
  | `Acsl4` | 1 | `Acsl4` only |
  | `Dgke` | 1 | `Dgke` only |
  | `Synj1` | 1 | `Synj1` only |
  | `Inpp5k` | 0 | none |
  | `Ocrl` | 0 | none |
  | `Pik3cb` | 0 | none |
  | `Pik3r1` | 0 | none |
  | `Pik3r2` | 0 | none |

- The same-experiment corpus supports interpreting these as buffered lipid
  pathway examples rather than as missed large modules. `Dgke` had no
  non-`Dgke` genes at FDR<0.10 in any of 23 measured cell groups and PI-cycle,
  DAG, and PKC comparators failed to produce a common neuronal RNA program.
  `Synj1` was also pan-surface flat, with `Ocrl` and `Inpp5k` failing to uncover
  a compensatory phosphoinositide module. `Acsl4` had only a restricted
  non-thalamic `Srebf2` response rather than a broad ferroptosis/lipid-stress
  signature.

Reasoning:

MBOAT7 is expressed in the focal cells and the P16 edit should eventually reduce
its enzymatically supplied PI acyl state, so I did not treat the perturbation as
unengaged or unreachable. The closest observed lipid and phosphoinositide
perturbations, however, show that even biologically real disruption of these
membrane-lipid cycles usually leaves no steady-state thalamic RNA program in
this assay. The exact focal Parquet rows were especially constraining: among
`Acsl4`, `Dgke`, and `Synj1`, the lone significant row was the edited transcript
itself, while `Inpp5k`, `Ocrl`, and PI3K components were complete zeros.

I therefore placed `Mboat7` in the self-only/isolated-hit regime rather than in a
multi-gene stress or homeostatic-response regime. Its broad focal expression and
likely stock depletion make a single BH-significant gene slightly more likely
than a complete zero, but the training analogs give little support for tens or
hundreds of downstream DEGs.

Predicted `n_degs`: 1
