# Syn3 n_degs forecast

Endpoint: `n_degs` is the count of measured genes in `151 TH Prkcd Grin2c Glut`
with BH-adjusted Wilcoxon `p < 0.05`.

Target: `Syn3`.

## Evidence used

- The exact focal-population reach card reports `Syn3` expression in the target
  class: 9,542 of 23,679 non-target nuclei expressed the gene
  (`40.297%`), with mean log1p CP10K `0.2484`, mean CP10K `0.3685`, and
  pseudobulk CPM `36.17`. This supports some direct target reach, but not broad
  or high expression across the whole thalamic aggregate.
- The endpoint-blind biology bundle places Syn3 in the synapsin family as a
  synaptic-vesicle/recycling-pool regulator. It also adjudicates the stock as
  `likely_substantially_depleted` by P37-P44 after a P16 disruptive edit because
  Syn1/Syn2 family protein half-life proxies are 4.40-4.95 days.
- That same bundle keeps the assay-match evidence only moderate: the direct
  Syn3 loss studies were germline or hippocampal and behavioral/physiologic,
  not postnatal conditional loss in thalamic glutamatergic neurons.
- The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` table is very
  sparse in this focal class: 1,205 of 1,674 training perturbations have
  `n_degs = 0`, the median is `0`, the 75th percentile is `1`, the 90th
  percentile is `2`, and only 106 of 1,674 reach at least 10 DEGs.
- The closest measured paralogs in the count table are at the floor in this
  exact class: `Syn1 = 1` and `Syn2 = 0`.
- The same-experiment Syn1/Syn2 Findings interpret both as broadly buffered
  perturbations: Syn1 had only two one-gene downstream FDR<0.10 events across
  recovered cell groups, Syn2 had only one one-gene downstream event, neither
  had a robust activity/stress/paralog-compensation program, and their
  high-confidence shared Claim places most represented presynaptic
  vesicle-cycle or active-zone perturbations on the flat or singleton side, with
  `Stxbp1` as the visible exception.
- An exact Parquet query of `151 TH Prkcd Grin2c Glut` for the represented
  presynaptic comparators showed the local FDR<0.05 counts were all 0 or 1:
  `Bsn 0`, `Cplx1 1`, `Cplx2 0`, `Dnm1 1`, `Nsf 0`, `Pclo 0`, `Stx1b 0`,
  `Stxbp1 1`, `Sv2a 1`, `Syn1 1`, `Syn2 0`, `Syp 1`, `Syt2 0`, `Unc13a 0`,
  `Unc13b 0`, `Unc13c 0`, and `Vamp1 1`. For the seven local singleton
  responders in this set, the sole significant gene was the perturbed target
  transcript itself.

## Forecast

I put `Syn3` with the buffered Synapsin/presynaptic neighborhood rather than
with the high-burden tail of the thalamic screen. The biology supports real
Syn3 perturbation by harvest and the expression reach is high enough that a
self-transcript call or isolated sentinel is plausible. The direct training
comparators argue against a propagated nuclear RNA program: Syn1/Syn2 are
0-to-1 DEG events in this exact class, most vesicle-release comparators are
0-to-1 events here, and even the broader `Stxbp1` presynaptic outlier has only
one local BH<0.05 feature in `151 TH Prkcd Grin2c Glut`.

Point prediction: `1`.
