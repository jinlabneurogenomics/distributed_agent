# Pde3a n_degs forecast

Target and endpoint:

- Manifest target: `Pde3a`
- Cell group: `151 TH Prkcd Grin2c Glut`
- Endpoint: number of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`
- Point forecast: `0`

Evidence used:

- The declared biology bundle identifies PDE3A as the cGMP-inhibited PDE3A
  enzyme, a cyclic-nucleotide phosphodiesterase that hydrolyzes cAMP and cGMP.
  The exact in-assay non-target expression reach in `151 TH Prkcd Grin2c Glut`
  is very small: 671 of 23,679 non-target nuclei expressed `Pde3a`
  (`2.83%`), with mean raw UMI `0.0384` and pseudobulk CPM `2.41`.
- The functional-stock card is not a zero block, because a disruptive P16 edit
  should stop new PDE3A synthesis and PDE3A is a degradable enzyme. The card
  also leaves the P37-P44 operative stock indeterminate: the only direct
  target-specific turnover observation is injury-induced cardiac degradation,
  not basal turnover in juvenile thalamic neurons.
- The loss-prior card did not provide a matched postnatal neural phenotype.
  Germline `Pde3a` loss has a female-infertility phenotype, adult forebrain
  PDE3A-positive neurons have been reported outside this exact thalamic assay,
  and `Pde3b` is a related PDE3 family gene, but there is no tested thalamic
  compensation or short-window thalamic loss phenotype.
- The supplied training count table for this same cell group contains 1,674
  targets with a median of `0` DEGs, a 75th percentile of `1`, a 90th
  percentile of `2`, and a mean of `14.05` because a small number of targets
  have very large signatures.
- Typed analog nomination put the operation-matched training comparators in a
  cyclic-nucleotide phosphodiesterase tranche: `Pde10a`, `Pde4d`, `Pde4b`, and
  `Pde1c`, connected to `Pde3a` through shared GO molecular functions such as
  cyclic-nucleotide phosphodiesterase activity, 3',5'-cyclic-AMP
  phosphodiesterase activity, and 3',5'-cyclic-GMP phosphodiesterase activity.
- Direct Parquet checks in `151 TH Prkcd Grin2c Glut` gave `n_degs = 0` and
  `n_fdr10 = 0` for all four PDE comparators:

  | comparator | n_pert_matched | n_ctrl_matched | n_degs |
  | --- | ---: | ---: | ---: |
  | `Pde10a` | 191 | 23679 | 0 |
  | `Pde4d` | 192 | 23679 | 0 |
  | `Pde4b` | 211 | 23679 | 0 |
  | `Pde1c` | 155 | 23679 | 0 |

- Broader cyclic-nucleotide comparators also stayed quiet in the same table:
  `Adcy1`, `Adcy3`, and `Adcy5` each had `0` DEGs; `Prkaca` and `Prkar1a`
  each had `1`; the downstream transcriptional effector `Creb1` had `10`.
  I treated those as looser context, not as equal-scale PDE3A loss analogs.
- A profile-neighborhood scan using the four PDE anchors found that each PDE
  anchor had zero significant positive and zero significant negative genes in
  the exact group. The leading Pearson and cosine neighbors of these anchors
  were themselves almost entirely zero-count or single-digit-count profiles,
  so the observed PDE-family profiles did not uncover a recurring
  high-response module hidden behind the zero count table entries.

Synthesis:

The same-operation measured losses are all null at both 5% and 10% FDR in the
requested thalamic group, and the exact `Pde3a` reach is much lower than the
population being tested. That low expression reach makes a focal PDE3A effect
easy to dilute below BH significance even if editing depletes enzyme in the
few `Pde3a`-positive neurons. The broader cAMP/cGMP signaling comparators do
not argue for a large alternate response; adenylate-cyclase losses are also
null, PKA subunits are one-gene calls, and `Creb1` is a downstream
transcription-factor perturbation rather than a phosphodiesterase loss.

Because the P37-P44 protein realization is uncertain rather than explicitly
blocked, I did not force the forecast through an absolute zero biological
block. I placed the point at the modal and same-family value: `0` measured
DEGs.
