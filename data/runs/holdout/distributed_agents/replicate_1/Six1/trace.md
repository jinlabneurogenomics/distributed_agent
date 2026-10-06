# DEG-count prediction trace

## Question and endpoint alignment

The requested prediction is the integer number of genes expected to pass
Benjamini-Hochberg FDR < 0.05 after acute AAV-CRISPR loss of `Six1` in the
`151 TH Prkcd Grin2c Glut` thalamic glutamatergic population.  `Six1` is
held out from both supplied inputs, so there is no direct `Six1` perturbation
signature in the parquet and no observed `Six1` `n_degs` value in the training
CSV.  I treated the training count file as the directly observed endpoint for
non-held-out perturbations and the focal-cell rows of the DE parquet as direct
expression-pattern evidence for those same training perturbations.  External
SIX1/SIX-EYA-DACH biology was used only to decide which measured perturbations
were mechanistically plausible analogs.

No ranking supervision was supplied: the requested-target file contains one
unranked target, `Six1`.  The rank-calibration, ordering-validation, and
predictive graph-review workbenches were therefore not authorized.  I did not
use graph multiplicity or embedding similarity as evidence.

## Sources used

- Declared DEG-count training CSV:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared DE parquet:
  `training differential-expression dataset`.
- Run-local PerturbAI atlas v5 dataset portrait and measurement registry.
- PerturbAI July 260713 same-experiment report/evidence corpus, via
  `corpus.report_evidence`, for packaged Six3, Six5, and Dach1 summaries.
  These records are a curated view of the same experiment, not independent
  replication.
- PubMed for external mechanism:
  Ikeda et al. 2002, DOI `10.1128/MCB.22.19.6759-6766.2002`; Li et al. 2003,
  DOI `10.1038/nature02083`; Wong et al. 2012, DOI
  `10.1016/j.heares.2012.09.009`; Meurer et al. 2021, DOI
  `10.3389/fcell.2021.707854`.

## Quantitative checks over the supplied inputs

I queried the focal cell class in the parquet for represented Six/Eya/Dach/Pax
and developmental transcription-factor perturbations and joined the identities
back to the training endpoint.  The endpoint distribution in the focal group is
strongly zero-inflated: among 1,674 training targets, 1,205 had `n_degs = 0`,
307 had only 1-2 DEGs, 56 had 3-9, 63 had 10-99, and only 43 had at least
100.  Thus a large nonzero prediction needs positive local analog evidence,
not just the fact that the held-out gene encodes a transcription factor.

The closest available SIX/retinal-determination network perturbations in the
training endpoint were all null in `151 TH Prkcd Grin2c Glut`:

| training perturbation | focal matched cells | observed `n_degs` at FDR < 0.05 | best focal evidence |
| --- | ---: | ---: | --- |
| `Six3` | 167 | 0 | every focal row had `pvals_adj = 1`; the same-experiment Six3 report classified the 151 group as a null surface with no downstream genes even at FDR < 0.10 |
| `Six5` | 215 | 0 | every focal row had `pvals_adj = 1`; the Six5 report also found no FDR < 0.10 downstream gene in any assayed neuronal group |
| `Dach1` | 173 | 0 | every focal row had `pvals_adj = 1`; the Dach1 report recorded no downstream FDR < 0.10 genes in the thalamic, hypothalamic, midbrain, pontine, pineal, or cerebellar groups |
| `Pax6` | 138 | 0 | all focal rows had `pvals_adj = 1`, supporting `Pax6` as a null retinal-determination-network counterexample |

The CSV did not contain `Eya1`, `Eya2`, `Eya3`, `Eya4`, `Six2`, `Six4`,
`Six6`, or `Dach2` as perturbation targets, so they could not be endpoint
analogs.  As measured genes in the `151` focal rows, however, `Six1`, `Six2`,
`Six3`, `Six5`, `Six6`, `Eya1-4`, and `Dach1-2` were never significant under
any of the 1,674 training perturbations.  `Six4` was the only queried
SIX-network transcript that moved at FDR < 0.05 in this cell class, and only
under two very large generic nuclear-factor responses (`Sin3a` and `Tpr`);
that is weak context for `Six1` itself rather than an argument for a SIX-specific
response.

I also looked at a broader panel of training developmental transcription
factors as local negative controls.  `Myod1`, `Tbx1`, `Pitx2`, `Pitx3`,
`Pou1f1`, `Pou2f1`, `Dlx3`, `Dlx6`, many `Hox*` genes, many `Fox*` genes, and
`Pax2/3/4/6/7/8` all had zero focal DEGs; `Sox2` and `Sox5` had only two.  This
reinforced that this postnatal neuronal CRISPR assay does not systematically
produce a broad focal thalamic signature when a developmental selector or
lineage regulator is perturbed.

## Biological transfer model for Six1

SIX proteins are homeodomain transcription factors whose classical roles lie
in the conserved Pax/Six/Eya/Dach retinal-determination and organogenesis
network.  Ikeda et al. showed that Six, Eya, and Dach proteins can cooperate
through direct Six-Eya interaction and CBP-mediated activation; Li et al.
showed in mouse organogenesis that Six1 genetically and transcriptionally
interacts with Eya factors and that Eya phosphatase activity can switch a
Six1-Dach complex from repression to activation.  Wong et al. reviewed the
requirement for the EYA1-SIX1 activation complex in mammalian inner-ear
neurosensory proliferation, survival, and differentiation, and Meurer et al.
summarized the broader SIX family as embryonic developmental and cancer
regulators.

That biology makes `Six3`, `Six5`, `Dach1`, and `Pax6` relevant training
comparisons because they perturb represented members of the same SIX/DACH/PAX
developmental transcriptional cassette.  It does not establish an obligate
same-endpoint prior in P16-to-P37/44 thalamic glutamatergic neurons.  The
canonical SIX1 effects occur in proliferative or differentiating embryonic
placodal, kidney, muscle, ear, and other organogenetic tissues with EYA/DACH
cofactor availability.  The requested intervention occurs later, in sparse
postmitotic NeuN-positive neurons, and the focal thalamic training data show
that knocking out available SIX/DACH/PAX network members did not recreate a
large survivor-state transcriptome.  Thus the causal chain

`Six1 loss -> impaired SIX1/EYA/DACH transcriptional complex -> altered
progenitor or organogenesis programs -> cell-state change in recovered neurons
-> many FDR-significant genes`

is expected to fail at the context/cofactor/program step for this cell group.
The closest measured perturbations point in the same null direction, and I did
not find a candidate-specific counterexample suggesting that `Six1`, unlike
`Six3`, `Six5`, or `Dach1`, should be a broad regulator in `151 TH Prkcd Grin2c
Glut`.

## Target-specific prediction

`Six1`: predicted `0` DEGs.  This is primarily a within-dataset prediction from
null focal DEG counts for the measured SIX/retinal-determination analogs
`Six3`, `Six5`, `Dach1`, and `Pax6`, plus the flat focal expression-pattern
surfaces for those perturbations.  External SIX1 literature explains why those
are plausible analogs, but it also downgrades transfer because the validated
SIX1 programs are embryonic and organogenetic rather than postmitotic thalamic
maintenance programs.  A tiny one- or two-gene call is possible in this assay,
as seen for `Sox2`, but there was no focal Six/Eya/Dach evidence justifying a
nonzero point estimate.

## Limits and uncertainty

The prediction extrapolates from related factors because `Six1` itself is
withheld as a perturbation.  `Eya1-4`, `Six2`, `Six4`, `Six6`, and `Dach2` were
not training perturbations, so their loss-of-function endpoint could not be
measured locally.  AAV CRISPR produces mosaic protein loss and may perturb
cells without decreasing the assayed nuclear target transcript, so I did not
treat lack of self-transcript knockdown in related targets as failed editing.
The NeuN-enriched, recovered-nucleus readout can miss earlier selection, rare
substates, or non-neuronal effects.  Finally, FDR-significant DEG counts are
power- and threshold-dependent; predicting zero means I expect no gene to cross
the assay's FDR < 0.05 threshold in the focal recovered nuclei, not that SIX1
is biologically irrelevant in every mouse cell type.
