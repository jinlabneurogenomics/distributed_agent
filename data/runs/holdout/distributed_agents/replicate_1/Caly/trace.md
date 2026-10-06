# DEG-count prediction for held-out `Caly`

## Question and interpretation

I interpreted the task as a scalar prediction for the held-out perturbation
`Caly`: predict `n_degs`, the number of measured genes passing
Benjamini-Hochberg adjusted Wilcoxon `pvals_adj < 0.05` in the
`151 TH Prkcd Grin2c Glut` focal class after acute postnatal CRISPR-Cas9
loss of function.  The requested CSV contains one target, `Caly`, and that
target is absent from both the focal training-count CSV and the
training-only differential-expression parquet.

The endpoint is directly observed for the non-held-out training genes in the
focal count CSV.  For `Caly` itself the requested endpoint is absent by
construction, so I treated focal training counts as direct calibration for
training perturbations and used focal rows in the parquet only to inspect
which genes drove counts in candidate analog perturbations.

## Sources

* Run-local task files: `task.md`, `codex_runtime/pipeline/task_bindings.json`,
  `codex_runtime/pipeline/coverage.json`,
  `codex_runtime/pipeline/capabilities.json`, and
  `codex_runtime/pipeline/measurement_registry.json`.
* Training endpoint:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
* Training differential expression:
  `training differential-expression dataset`.
* Requested targets:
  `single-target request for Caly`.
* Literature searched through PubMed.  I did not use same-experiment
  held-out `Caly` reports or any evaluation labels.

## Quantitative calibration from the training endpoint

The focal training file has 1,674 non-held-out biological perturbations.
The endpoint distribution is sparse:

| statistic | value |
|---|---:|
| zero-DEG perturbations | 1,205 / 1,674 = 72.0% |
| perturbations with 0 or 1 DEG | 1,481 / 1,674 = 88.5% |
| median | 0 |
| 75th percentile | 1 |
| 90th percentile | 2 |
| 95th percentile | 18 |
| maximum | 2,677 |

Thus the prior for a neuronal trafficking or receptor perturbation with no
high-effect training analog is zero or one DEG, not a broad hundreds-of-DEGs
state.  I then checked the focal endpoint values of genes in Caly-relevant
biology.  The closest available analogs were:

| training perturbation | focal `n_degs` | focal expression-pattern evidence |
|---|---:|---|
| `Cltc` | 3 | Three FDR-significant genes, all at q = 0.0424: `Rbms1`, `Ero1b`, `Gabra4`; only 32 matched perturbed nuclei. |
| `Dnm1` | 1 | The only FDR-significant gene is the target transcript, `Dnm1`, q = 4.09e-25; the next genes have q = 0.575. |
| `Synj1` | 1 | The only FDR-significant gene is the target transcript, `Synj1`, q = 3.11e-7; the next genes have q = 1.0. |
| `Bin1` | 1 | The only FDR-significant gene is the target transcript, `Bin1`, q = 2.89e-6; the next genes have q = 1.0. |
| `Nrg1` | 0 | Top focal adjusted p values are all 1.0. |
| `Erbb4` | 0 | Top focal adjusted p values are all 1.0. |
| `Adam10` | 0 | Top focal adjusted p values are all 1.0. |
| `App` | 1 | The only FDR-significant gene is the target transcript, `App`, q = 8.41e-58; the next gene has q = 0.171. |
| `Drd2` / `Drd4` / `Drd5` | 0 / 0 / 0 | The closest assayed dopamine receptor perturbations have no focal DEGs. |
| `Shank3`, `Dlg4`, `Stxbp1`, `Syp`, `Cplx1` | 2, 1, 1, 1, 1 | Postsynaptic-density or synaptic-vesicle perturbations are present but mostly yield a target-transcript-only or two-gene response. |

Many obvious endocytic components were not in the non-held-out training
endpoint table, including `Clta`, `Cltb`, `Ap2a1`, `Ap2a2`, `Ap2b1`,
`Ap2m1`, `Ap2s1`, `Itsn1`, `Itsn2`, `Eps15`, `Epn1`, `Epn2`, `Picalm`,
`Amph`, and `Sh3gl2`.  `Nsg1`/`Nsg2`/`Nsg3` family members were also absent,
so there was no same-family DEG-count anchor.

## Biological transfer model for `Caly`

The best supported cellular role for calcyon is as a neuron-enriched
vesicular/endocytic protein:

* Xiao et al. 2006 found that calcyon associates with clathrin light chain,
  localizes to pre- and postsynaptic vesicular compartments, can stimulate
  clathrin assembly, and that calcyon-null cortical neurons had impaired
  transferrin uptake with preserved recycling, supporting a role in
  clathrin-mediated endocytosis in brain. DOI: 10.1074/jbc.M600265200;
  PMID: 16595675.
* Kruusmagi et al. 2007 showed neuronal expression and movement of
  calcyon-positive vesicles through the endocytic recycling pathway.
  DOI: 10.1097/WNR.0b013e3282f03f51; PMID: 17885599.
* Yin et al. 2014 connected calcyon-dependent clathrin-mediated endocytosis
  to pro-NRG1 cleavage, NRG1 ectodomain shedding, ErbB4 activation, and
  GABA transmission. DOI: 10.1038/mp.2014.131; PMID: 25349163.
* Ha et al. 2012 supported an indirect dopamine D1 receptor trafficking role
  through PSD-95, with calcyon phosphorylation increasing PSD-95 association
  and D1 receptor internalization. DOI: 10.1074/jbc.M112.370601;
  PMID: 22843680.

The intervention-to-endpoint chain for the acute screen is therefore:

`Caly` CRISPR loss of function -> reduced calcyon function on neuronal
vesicular/endocytic membranes -> weaker clathrin-mediated uptake and altered
trafficking of a subset of surface or juxtamembrane proteins such as NRG1 or
D1-containing complexes -> changed signaling or synaptic state only in
neurons where those cargoes and receptors are active -> survivor-conditioned
snRNA-seq differential expression in recovered `151 TH Prkcd Grin2c Glut`
nuclei.

That chain is plausible but not an obligate core-complex dependency.  Caly is
an accessory transmembrane trafficking factor, whereas the directly assayed
training genes closest to the limiting endocytic machinery, `Cltc`, `Dnm1`,
`Synj1`, and `Bin1`, produced only zero-to-three focal DEGs.  The NRG1-ErbB4
cleavage/signaling arm was even quieter in this focal class: `Nrg1`, `Erbb4`,
and `Adam10` each had zero focal DEGs, and `App`, a broader substrate/cargo
context for endocytic proteolysis, showed only self-target loss.  Dopamine
receptor perturbations that might mark the D1/D5 signaling neighborhood were
also null.  Together these training perturbations argue that loss of an
auxiliary calcyon-dependent trafficking input is unlikely to create a broad
FDR-significant transcriptional program after 3-4 weeks in this thalamic
glutamatergic class.

## Prediction

I predict `Caly` will have no genes passing FDR 0.05 in the held-out focal
readout.

* The zero/nonzero boundary is driven primarily by the training counts:
  the nearest available endocytosis, receptor-trafficking, and synaptic
  perturbations were 0 or 1 DEG except for the very low-cell-count `Cltc`
  result with three borderline downstream calls.
* External biology was used to select those comparators and to reject more
  distant high-DEG processes such as proteasome disruption, RNA processing,
  or general transcriptional regulation.  It did not supply a reason to
  transfer any high-burden response to `Caly`.
* I assigned 0 rather than 1 because `Caly` is an accessory trafficking gene
  and the training genes whose only significant row was their own transcript
  do not establish a downstream expression program.  Weak or absent target RNA
  knockdown is not proof of failed editing in this assay, so the estimate is
  still a prediction of response breadth, not a prediction that the guides
  fail.

## Limits

There is no direct `Caly`, `Nsg1`, `Nsg2`, `Nsg3`, AP-2 subunit, or epsin/
intersectin/PICALM training perturbation in the supplied endpoint table, so
the prediction extrapolates from one-step clathrin, dynamin, and
clathrin-linked cargo-processing analogs rather than from a same-family
knockout.  Caly may be cell-type- or cargo-selective; the external literature
largely uses cultured cortical neurons, heterologous cells, or injury and
schizophrenia contexts rather than juvenile thalamic glutamatergic nuclei
after sparse AAV-CRISPR.  The focal counts are assay- and power-dependent:
`Cltc` had only 32 matched perturbed nuclei, while other analogs had 69-276,
so a few true low-amplitude downstream effects could move across the FDR
threshold in either direction.  Finally, the parquet and the internal corpus
are same-experiment representations; I used the parquet for exact training
rows and treated PubMed literature as mechanistic prior knowledge, not as an
independent validation of any held-out `n_degs`.
