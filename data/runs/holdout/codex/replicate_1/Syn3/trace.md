target_name: Syn3
cell_group: 151 TH Prkcd Grin2c Glut
predicted_n_degs: 1

Evidence used

- The declared manifest target is `Syn3`.
- The requested endpoint is the count of measured genes with `pvals_adj < 0.05`
  in `151 TH Prkcd Grin2c Glut`, including the self transcript if it passes
  the same threshold.
- The `Syn3` biology bundle shows exact focal-population target reach:
  `Syn3` was measurable in non-target nuclei from this class, with
  9,542/23,679 nuclei expressing, 40.297% expressing, mean raw UMI 0.577, and
  mean log1p CP10K 0.248. The same bundle adjudicates the operative Syn3 stock
  as likely substantially depleted by the P37-P44 harvest because Syn3 is a
  dynamic synaptic-vesicle-associated synapsin-family protein and Syn1/Syn2
  family turnover proxies are roughly 4-5 days, fitting several half-lives into
  the 21-28 day edit interval.
- The focal-class training count table is extremely sparse: 1,205/1,674
  perturbations have `n_degs = 0`, 1,481/1,674 have `n_degs <= 1`, and the mean
  of 14.05 is dominated by a small tail of broad responders.
- The closest represented presynaptic and synapsin-family comparators in this
  exact cell class were all null or self-only:

| target | n_degs | focal significant genes |
|---|---:|---|
| Syn1 | 1 | Syn1 |
| Syn2 | 0 | none |
| Synj1 | 1 | Synj1 |
| Syp | 1 | Syp |
| Sv2a | 1 | Sv2a |
| Vamp1 | 1 | Vamp1 |
| Dnm1 | 1 | Dnm1 |
| Cplx1 | 1 | Cplx1 |
| Stx1b | 0 | none |
| Unc13a | 0 | none |
| Unc13b | 0 | none |
| Unc13c | 0 | none |
| Cplx2 | 0 | none |
| Rab3gap1 | 0 | none |
| Rab3gap2 | 0 | none |

- Same-experiment corpus Findings for `Syn1`, `Syn2`, `Syp`, and `Sv2a`
  describe these vesicle-reserve/release perturbations as buffered or
  transcriptionally uncoupled from broad steady-state neuronal mRNA programs;
  the broad presynaptic exception is `Stxbp1`, but in this exact focal class
  `Stxbp1` also has only one FDR-significant gene in the training count table.
- Direct focal-class Wilcoxon-score comparisons among `Syn1`, `Syn2`, `Syp`,
  `Sv2a`, `Dnm1`, `Vamp1`, and `Cplx1` gave near-zero pairwise score
  correlations, all from -0.015 to 0.045, so the close self-only comparators do
  not hide a coherent multi-gene module that should be transferred to `Syn3`.

Synthesis

`Syn3` is reachable and should be functionally perturbed in edited cells, so I
did not treat it as an absent-target zero. However, its mechanism is the same
presynaptic vesicle-reserve biology that repeatedly produces no non-self
FDR-level RNA response in this P16 sparse postmitotic assay. The exact focal
class therefore supports a self-only forecast: no downstream significant genes,
with one DEG contributed by the `Syn3` transcript itself if the guide pool makes
a detectable nuclear mRNA drop.
