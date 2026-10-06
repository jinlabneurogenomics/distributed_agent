target: Kansl1
cell class: 151 TH Prkcd Grin2c Glut
endpoint: n_degs, measured genes with BH-adjusted Wilcoxon p < 0.05

Prediction: 6

Evidence used

- The prediction-safe biology bundle identifies KANSL1 as a noncatalytic nuclear
  subunit of the KAT8/NSL histone-acetyltransferase complex and as an upstream
  regulator of STX17-linked autophagosome-lysosome fusion.
- Exact in-assay reach is present rather than merely inferred: in matched
  non-target nuclei from 151 TH Prkcd Grin2c Glut, Kansl1 RNA was detected in
  19,567 of 23,679 nuclei, or 82.63%, with mean log1p(CP10k) 0.7399 and
  pseudobulk CPM 131.57. This supports perturbation reach in the focal
  population, but was not treated as editing efficiency.
- The functional-stock card favors substantial depletion by the P37-P44 harvest:
  editing at P16 should stop new KANSL1 supply, and inducible Kansl1 deficiency
  in primary mouse neurons produced KANSL1-linked STX17/mitophagy effects on a
  timescale shorter than the 21-28 day Perturb-seq window. The card also leaves
  the numeric KANSL1 protein half-life, thalamic complex kinetics, and possible
  Kansl1l buffering unresolved.
- The declared 151 TH Prkcd Grin2c Glut training count table is sparse: 1,674
  perturbations have median 0, 75th percentile 1, 90th percentile 2, 95th
  percentile 18, mean 14.05, and only 106 perturbations reach at least 10 DEGs.
- Direct same-complex training rows are mostly absent. The only represented
  MOF/KAT8/NSL-adjacent counts I found were Ogt = 4 and Msl2 = 0 in the focal
  class. Same-experiment Findings mark Msl2 as downstream-flat and contrast it
  with a broad Ogt response outside this cell class, separating an acute Msl2
  null from the Ogt/NSL-associated axis.
- Nearby chromatin/HAT comparators in the focal count table also sit near the
  low single-digit range when the target is not one of the screen's broad
  chromatin outliers: Crebbp = 8, Ep300 = 0, Kat6a = 0, Kat6b = 0, with Brd4,
  Yy1, Sin3a, Setd1a, and Phf12 treated as possible but too-broad upper
  context.
- The STX17/autophagy bearing argues for a possible stress response, not for
  direct transfer of severe lysosomal or UFMylation scales. In the focal count
  table, core autophagy and mTOR-adjacent perturbations were small or absent
  for Atg5, Becn1, Lamp2, Rb1cc1, and Mtor, whereas proximal stress genes such
  as Rab7, Ufc1, and Uba5 had 501, 572, and 2,677 DEGs. Same-experiment
  Findings describe Rab7 and Uba5 as broad endolysosomal/proteostasis stress
  states, so I used them only as an upper bound on what a severe secondary
  organelle state can look like.

Reasoning

Kansl1 is expressed in most focal nuclei and its biology is realized within the
assay window, so I did not collapse the forecast to the endpoint median of zero.
At the same time, the closest measured NSL/KAT8-adjacent targets and several
HAT/autophagy comparators are zero to low single-digit responders in exactly
this cell class, and the stronger Rab7/Uba5 stress programs are more direct and
severe than KANSL1 loss of a transcriptional input into STX17 machinery. I
therefore placed Kansl1 just above the Ogt/Crebbp low-response anchors but
below the 95th percentile of the training endpoint.
