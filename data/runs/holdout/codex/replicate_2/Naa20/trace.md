# Direct forecast for Naa20 in 151 TH Prkcd Grin2c Glut

Endpoint: `n_degs`, the count of measured genes with BH-adjusted Wilcoxon
`pvals_adj < 0.05` in the focal `151 TH Prkcd Grin2c Glut` contrast.

Prediction: `2`

## Evidence used

- The declared holdout manifest contains the single target `Naa20`.
- The Naa20 biology bundle reports exact focal-population reach: the Naa20
  transcript is available in this cell class, with mean log1p CP10K 0.920,
  mean raw UMI 2.815, pseudobulk 176.44 CPM, and detection in
  21,132 of 23,679 non-target nuclei, or 89.24%.
- The same bundle supports functional realization by harvest but not a matched
  postnatal mouse thalamus phenotype. Naa20 is the catalytic NatB subunit,
  depends on Naa25 for productive NatB assembly, and most NatB action is
  cotranslational. A P16 disruptive edit should stop new Naa20 supply while
  initially leaving pre-existing NatB and pre-existing N-terminally acetylated
  substrate molecules intact; the card adjudicates the enzyme/substrate stock
  as `likely_substantially_depleted` by P37-P44 because Naa20 and Naa25 turn
  over on a days scale and most measured adult-thalamus proteins are projected
  to renew substantially over 21-28 days.
- The same card leaves acute target-context timing unresolved: direct mouse
  Naa20 loss evidence is non-neural, the human neuronal CRISPRi evidence was
  established before or during differentiation, and no direct loss experiment
  initiated in postnatal mouse thalamic neurons was located in the bounded
  source-card search.
- The focal training count table is extremely sparse: of 1,674 observed
  training perturbations, 1,205 have `n_degs = 0`, 276 have `n_degs = 1`, and
  only 106 reach at least 10 DEGs.
- The closest measured N-terminal-acetyltransferase target in the training
  count table, `Naa10`, has `n_degs = 0` in this focal class. The same-experiment
  Naa10 report also summarizes it as a pan-neuronal FDR-level transcriptional
  null with no Nat-family, integrated-stress, apoptosis, proteasome, or
  ubiquitin rebound program; this is a lower bracket for acute NAT catalytic
  loss, not an exact NatB analogue.
- Weak but nonzero translation or growth-control perturbations in the focal
  count table sit near the same scale: `Rptor = 0`, `Eif4g1 = 1`,
  `Eif4a2 = 2`, `Mtor = 2`, and `Eef2 = 9`. Direct Parquet checks in
  `151 TH Prkcd Grin2c Glut` confirmed those BH<0.05 counts and showed that
  `Naa10` had no near-threshold adjusted p-values, whereas `Mtor` was supported
  by only two FDR<0.05 rows.
- Strong proteostasis and ribosome-quality-control perturbations define a much
  higher stress bracket in the same class: `Psmb4 = 742`, `Psmc1 = 430`,
  `Uba5 = 2677`, and `Ufc1 = 572`. Packaged Psmb4/Psmc1 Findings identify
  these as core proteasome-damage responses with proteasome bounce-back,
  heat-shock/ISR, autophagy-lysosome, redox, and p53/apoptotic arms, which is a
  more direct proteostasis failure than blocking one NatB-mediated
  cotranslational modification class.

## Synthesis

Naa20 is not a pure null prior: it is well expressed in the focal thalamic
population, the NatB catalytic stock should be materially depleted over the
21-28 day experimental window, and redundancy is incomplete because other NATs
are not equivalent NatB catalytic replacements. Those facts argue for a
nonzero prediction rather than simply inheriting the heavy zero mass of the
training table.

I nevertheless kept the estimate low. The measured in-assay Nat catalytic
comparator, Naa10, was fully FDR-flat, and the Naa20 bundle does not contain a
matched acute mouse postnatal-neuron phenotype showing that NatB loss crosses
into a broad nuclear-RNA stress state. The observed mTOR/translation brackets
show that broadly expressed protein-synthesis machinery can produce just
1-9 focal DEGs in this thalamic population, while the hundreds-to-thousands
DEG proteasome and UFMylation rows look like an upper stress regime that Naa20
has no direct evidence for.

I therefore placed Naa20 at the weak-response end of the active translation
bracket, just above the Naa10/Rptor nulls and near Mtor/Eif4a2, and used `2` as
the integer forecast. This uses the declared biology bundle, the declared
training count table, observed training rows from the declared Parquet, and
same-experiment packaged reports for comparator interpretation; it does not use
the held-out Naa20 expression signature or held-out Naa20 DEG count.
