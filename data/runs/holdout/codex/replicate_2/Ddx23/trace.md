# Ddx23 n_degs forecast

Target: `Ddx23`

Predicted `151 TH Prkcd Grin2c Glut` DEG count at BH-adjusted Wilcoxon `p < 0.05`: `560`

## Evidence used

- The declared holdout manifest contains one target, `Ddx23`.
- The canonical Ddx23 biology bundle places DDX23 at a recurrent nuclear RNA-processing operation: it is a DDX23/PRP28-subfamily ATP-dependent helicase associated with U5/U4-U6-U5 tri-snRNP function and spliceosomal B-complex formation, with an additional R-loop-control annotation.
- The same bundle supports realization by harvest rather than long-lived pre-edit stock: successful editing should stop new intact DDX23 supply, and the measured mouse mpkCCD Ddx23 half-lives of 39.06-61.43 h imply substantial depletion across the P16 to P37-P44 interval even though the kinetic source is non-neuronal.
- Focal expression reach is not limiting: in non-target `151 TH Prkcd Grin2c Glut` nuclei, Ddx23 was detected in 18,481 / 23,679 nuclei, or 78.05%, with mean CP10K 1.0965.
- The Ddx23 same-experiment corpus target context had no released Ddx23 Findings or Claims, so the forecast rests on its biology bundle plus measured training perturbations.
- The 1,674-target focal count table is very sparse overall: median `n_degs` is 0, 75% of targets have at most 1 DEG, 95% have at most 18, and the 99th percentile is 430.
- Spliceosome and RNA-processing training perturbations are a narrow high-response island in that sparse background. In `151 TH Prkcd Grin2c Glut`, the core or near-core analogs had these FDR<0.05 counts:
  - `Rnpc3`: 868
  - `U2af2`: 828
  - `Cdc40`: 624
  - `Prpf6`: 454
  - `Snrnp70`: 213
- The analogous module was selective rather than a property of every snRNP, DEAD-box, or PRP19-adjacent gene:
  - `Snrpb`: 0
  - `Ddx39b`: 0
  - `Ctnnbl1`: 1
  - `Snrpn`: 1
  - `Ddx3x`: 8
  - `Ascc3`: 18
- Broader same-state or downstream RNA/proteostasis neighbors were also high but less proximal to DDX23:
  - `Tpr`: 1768
  - `Psmb4`: 742
  - `Hnrnpu`: 733
  - `Tnpo3`: 618
  - `Psmc1`: 430
  - `Thoc1`: 303
- In the focal expression profile, `Cdc40`, `Rnpc3`, `U2af2`, `Prpf6`, and `Snrnp70` formed a coherent direct spliceosome cohort: the ten pairwise cosines were 0.630-0.698, and their significant down-regulated programs had a median pairwise overlap coefficient of 0.398. Their positive arms were weaker, with median significant overlap coefficient 0.125, so I treated the common state as dominated by shared loss of neuronal/synaptic and RNA-processing-maintenance transcripts rather than by exact identity of every up-regulated marker.
- Report-derived topology put `Cdc40`, `Prpf6`, `Rnpc3`, `Snrnp70`, `Thoc1`, `Tnpo3`, and `U2af2` in one fully connected explicit-Finding-reference set, while the same corpus kept `Snrpb`, `Snrpn`, and `Ctnnbl1` as boundary cases that do not phenocopy the strong branch despite superficial spliceosome membership.

## Synthesis

Ddx23 is closer to the strong major-spliceosome branch than to the flat Sm-ring/peripheral cases. Its U5/tri-snRNP role makes `Prpf6` the closest represented operation, `Cdc40` and `U2af2` relevant same-process comparators at different spliceosome stages, and `Rnpc3` a high-response minor-spliceosome state analog rather than a same-complex proxy. I therefore did not regress all the way to the zero-inflated table median.

At the same time, the exact Ddx23 perturbation power, guide functionality, and survivor-conditioned response magnitude are unobserved. The adjacent training perturbations span roughly 200-900 DEGs in the focal group, with `Prpf6` at 454 and `Cdc40` at 624 bracketing the closest major-spliceosome expectation. I set the point forecast just above that bracket's midpoint and below the `U2af2`/`Rnpc3` high end, yielding a several-hundred-DEG prediction rather than a `Tpr`-scale outlier.
