# Gpr162 n_degs forecast

Prediction target: `Gpr162` in `151 TH Prkcd Grin2c Glut`.

## Endpoint and allowed measurement

`n_degs` is the count of measured genes with BH-adjusted Wilcoxon
`pvals_adj < 0.05` in the declared `151 TH Prkcd Grin2c Glut` training count
table and matched all-cell-class DE parquet. The target was absent from the
training count table and the selected same-experiment corpus had no `Gpr162`
Finding, Claim, or explicit reference records, so the point below is a
biology-to-training extrapolation rather than a lookup of a hidden `Gpr162`
profile.

## Target biology prior

The declared `Gpr162` bundle makes the perturbation biologically reachable in
the requested cell class:

- Exact non-target expression in `151 TH Prkcd Grin2c Glut` was very broad:
  23,598 of 23,679 assayed non-target nuclei expressed `Gpr162`
  (`99.6579%`), with mean raw UMI `10.0436` and pseudobulk CPM `629.467`.
- The functional-stock card judged the P16-to-P37/P44 perturbation likely to
  substantially deplete GPR162 receptor stock by harvest, but with sparse
  target-specific kinetic evidence.
- The source facts support a class-A seven-transmembrane receptor operation
  outside brain, adult mouse neuronal expression, an adult-rat 7-day antisense
  neural phenotype, and unresolved buffering by the paralog `Gpr153`. They do
  not establish a tonic thalamic transcriptional program after juvenile mouse
  `Gpr162` loss.

I treated the high exact expression as evidence that a self-transcript count is
plausible, not as evidence for a large downstream state.

## Training counts and receptor comparators

The declared `151 TH Prkcd Grin2c Glut` count table was sparse: 1,205/1,674
training perturbations had `n_degs = 0`; 1,481/1,674 had `n_degs <= 1`;
1,512/1,674 had `n_degs <= 2`; and only 43/1,674 had `n_degs >= 100`. The
large tail was dominated by general RNA/proteostasis/chromatin regulators such
as `Uba5`, `Tpr`, `Sin3a`, `Rnpc3`, `Zbtb7a`, and `U2af2`, which are not close
to the GPR162 biology.

I therefore compared the observed `151` profiles of a 50-target GPCR or
receptor-like cohort from the training table:

`Adra1a`, `Adra2a`, `Adra2b`, `Adrb2`, `Adrb3`, `Ccr2`, `Chrm2`, `Chrm3`,
`Cnr1`, `Cxcr4`, `Drd2`, `Drd4`, `Drd5`, `Fzd2`, `Fzd4`, `Fzd6`, `Fzd9`,
`Gabbr1`, `Gabbr2`, `Gpr156`, `Gpr158`, `Gpr161`, `Gpr179`, `Gpr45`,
`Gprc5b`, `Grm1`, `Grm5`, `Grm6`, `Grm7`, `Grm8`, `Htr1a`, `Htr1b`, `Htr1f`,
`Htr2a`, `Htr2b`, `Htr2c`, `Htr3a`, `Htr3b`, `Htr4`, `Htr6`, `Htr7`, `Npy1r`,
`Npy2r`, `Npy5r`, `Oprd1`, `Oprk1`, `Oprl1`, `Oprm1`, `Smo`, `Sstr5`.

The run-local profile comparison
`evidence/receptor_profile_compare.json` matched all 50 nodes in the 151-class
parquet rows. Forty-four had no `pvals_adj < 0.05` feature and the remaining
six were all singletons in the count table: `Cnr1`, `Gabbr1`, `Gabbr2`,
`Gpr158`, `Grm1`, and `Grm7` each had `n_degs = 1`. The cohort diagnostic
`evidence/receptor_profile_cohort.json` found weak within-cohort similarity:
across 1,225 receptor pairs the median signed top-tail overlap coefficient was
0.025 in both the positive and negative tails, and significant-feature overlap
was absent or zero-valued. The focused inspection
`evidence/key_receptor_profile_inspect.json` showed that the singleton hits for
`Gpr158`, `Gabbr1`, and `Gabbr2` were the self-transcript itself, while the
`Cnr1` singleton was `Srcap`.

Packaged same-experiment corpus findings pointed the same way. `Gabbr2:F001`
reported no non-`Gabbr2` genes at FDR < 0.10 across 22 tested neuronal cell
groups. `Cnr1:F001` reported an otherwise buffered snRNA-seq surface with a
single `Srcap` hit in the same 151 class. The moderate-confidence Claim
`claim:944ca6185dd70e5a895c` summarized GPR158/GPR179, mGluR, Gbeta5/R7,
inhibitory-GPCR/GIRK, and cAMP-adjacent perturbations as flat, sparse, or
receptor-specific rather than a common neuronal phenocopy. The
high-confidence Hedgehog Claim `claim:cdb20b21467eeac1c3c5` likewise placed
`Gpr161` and `Smo` in a postnatal neuronal context where acute GPCR/ciliary
single-node perturbations failed to recover a coordinated canonical
transcriptional circuit.

## Forecast

I predict a self-transcript-sized event and no broader downstream program.
The exact `Gpr162` reach is much stronger than for an unexpressed receptor and
makes a BH-significant self row credible. But GPR162 is still a membrane GPCR
with uncertain tonic signaling in these juvenile thalamic neurons, the mouse
loss phenotype is untested, `Gpr153` redundancy is unresolved, and the closest
measured receptor perturbations in this class were overwhelmingly 0 or 1 DEGs.

Point prediction: `1`.
