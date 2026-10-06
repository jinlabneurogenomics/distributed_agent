# DEG-count prediction trace

## Question and endpoint

The requested endpoint is `n_degs` for the held-out `Ppargc1b` perturbation in
`151 TH Prkcd Grin2c Glut`, the thalamic glutamatergic class whose dataset label
uses `TH` for thalamus rather than tyrosine hydroxylase.  I interpreted
`n_degs` exactly as the count of measured genes with `pvals_adj < 0.05` in the
Wilcoxon differential-expression table for perturbed nuclei versus matched
non-targeting controls.

`Ppargc1b` itself was completely held out: it is absent from both the training
count CSV and the Parquet `gene_target` column.  The endpoint for the held-out
gene is directly observed for training perturbations only; for `Ppargc1b` it is
absent from the declared inputs and must be predicted from visible
Perturb-seq analogs plus external biology.

## Sources used

* Declared training endpoint:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
* Declared differential-expression Parquet:
  `training differential-expression dataset`.
* Requested-target manifest:
  `single-target request for Ppargc1b`,
  which contained only `Ppargc1b`.
* Run-local dataset portrait, task bindings, coverage, capability manifest, and
  measurement registry under `codex_runtime/pipeline`.
* Same-experiment internal corpus:
  `perturbai-july-260713-sourceguard-1773-v1`, queried through
  `corpus.calibration`, `corpus.findings`, and pathway records.  These records
  are interpretations of the same Perturb-seq experiment, not independent
  replication.
* External PubMed literature, used as mechanistic priors:
  Scarpulla 2008, Physiol Rev, DOI 10.1152/physrev.00025.2007;
  Scarpulla 2010, BBA, DOI 10.1016/j.bbamcr.2010.09.019, PMID 20933024;
  Wareski et al. 2009, J Biol Chem, DOI 10.1074/jbc.M109.018911, PMID 19542216;
  Shao et al. 2010, Mitochondrion, DOI 10.1016/j.mito.2010.05.012,
  PMID 20561910; Camacho et al. 2012, Exp Neurol,
  DOI 10.1016/j.expneurol.2012.06.031, PMID 22771762.

## Quantitative calibration from the training data

The focal training count table has 1,674 non-held-out perturbations.  Its
distribution is strongly zero-inflated:

* 1,205/1,674 perturbations have `n_degs = 0`.
* 469/1,674 are nonzero.
* The quartiles are 0, 0, and 1 DEG; the 90th percentile is only 2 DEGs.
* The 95th percentile is 18 DEGs, the 99th percentile is about 436, and the
  maximum is 2,677.

I then queried the Parquet for mechanistically plausible analogs in
`151 TH Prkcd Grin2c Glut`:

```
sum(pvals_adj < 0.05) by gene_target
where group_name = '151 TH Prkcd Grin2c Glut'
```

The relevant focal-cell counts and matched perturbed nuclei were:

| perturbation | `n_degs` in training | matched perturbed nuclei | interpretation for `Ppargc1b` |
| --- | ---: | ---: | --- |
| `Ppargc1a` | 0 | 135 | Closest measured PGC-1 paralog; strongest counterexample |
| `Ppara` | 0 | 158 | Canonical PGC/PPAR neighborhood but flat |
| `Ppard` | 0 | 315 | PPAR neighborhood; high recovered-cell count yet flat |
| `Pparg` | 0 | 109 | PPAR neighborhood but flat |
| `Esrrb` | 0 | 209 | ERR paralog and negative ESRRA-axis control |
| `Esrrg` | 0 | 183 | ERR paralog and negative ESRRA-axis control |
| `Nfe2l1` | 0 | 157 | Alias/paralog counterexample for respiratory/proteasome NRF biology |
| `Nfe2l2` | 0 | 207 | Related oxidative-stress transcription factor, flat |
| `Esrra` | 57 | 275 | Positive mitochondrial transcription-factor analog |
| `Nrf1` | 138 | 222 | Positive respiratory transcription-factor analog |
| `Opa1` | 37 | 195 | Mitochondrial stress analog, but an inner-membrane structural hit |
| `Creb1` | 10 | 126 | Upstream transcriptional regulator of some PGC programs |
| `Mef2a` | 4 | 138 | Weak activity-dependent mitochondrial/plasticity analog |
| `Mef2c` | 1 | 223 | Weak MEF2 analog |
| `Ndufs2` | 1 | 197 | Core OXPHOS complex I member, nearly flat |
| `Cox5a` | 1 | 219 | Core OXPHOS complex IV member, nearly flat |

The count comparison separates two classes of evidence.  Acute loss of the
DNA-binding factors `Esrra` and `Nrf1` is detectable in this cell group, so the
assay can report a mitochondrial-transcriptional perturbation.  In contrast,
the visible PGC/PPAR/ERR relatives closest to `Ppargc1b` are all exactly zero,
including `Ppargc1a`, and many single ETC-subunit perturbations are zero or
one-gene responses rather than broad mitochondrial stress states.

I also compared focal-cell Wilcoxon score vectors for the same targets.  The
largest rank correlation from `Ppargc1a` to a positive analog was with `Esrra`,
but it was only Spearman rho = 0.107.  `Ppargc1a` versus `Nrf1` was rho =
-0.021, and `Ppara`, `Ppard`, and `Pparg` were all near zero relative to `Esrra`,
`Nrf1`, and `Opa1`.  The top subthreshold `Ppargc1a` rows included plausible
`Esrra`-program genes such as `Bcan`, `Atp1b1`, `Idh3a`, and `Got1`, but the
best adjusted p-value was still 0.189 for `Bcan` and the next strongest rows
were already `pvals_adj >= 0.797`.  That is consistent with a faint
same-direction tendency and not with a near-miss broad signature.

## Same-experiment corpus evidence

The July Perturb-seq corpus reinforced the direct count queries:

* `Ppargc1a:F001` summarized `Ppargc1a` as having no FDR<0.10 downstream
  transcriptomic signature in any recovered neuronal group after P16 acute
  CRISPR loss of function.
* `Ppargc1a:F002` described `Ppargc1a` as flat while `Nrf1` and `Esrra` were
  responsive in overlapping high-yield groups, arguing that the non-DNA-binding
  PGC-1alpha coactivator was not the rate-limiting basal input into the
  NRF1/ERRalpha mitochondrial axis in these juvenile neurons.
* `Esrra:F002` showed that `Esrra` recovered the expected down-regulation of a
  partial ERRalpha/PGC-1 oxidative-metabolism arm in `151 TH Prkcd Grin2c Glut`,
  including genes such as `Mdh1`, `Got1`, `Mpc1`, `Dlat`, `Idh3a`, `Ndufs2`,
  `Cyc1`, and `Uqcrc1`.
* `Esrra:F005` and `Esrrg:F003` reported that the obvious ESRR/PGC/PPAR
  relatives did not phenocopy `Esrra`: `Esrrb`, `Esrrg`, `Ppargc1a`, `Ppara`,
  `Ppard`, and `Pparg` were flat in the matched `151` responder group.
* `Nrf1:F003` and `Nrf1:F007` showed that `Nrf1`, although a detectable
  mitochondrial regulator in `151`, had a different response from the
  PGC-1/ERR relatives and did not create a concerted broad
  `Tfam`/`Tfb1m`/`Tfb2m`/COX program.
* `Opa1:F002` interpreted `Opa1` as inducing an ATF4/integrated-stress-response
  amino-acid program.  That is endpoint-relevant as mitochondrial perturbation
  evidence but biologically farther from the transcriptional coactivator
  `Ppargc1b`.

I did not use graph topology, comparator multiplicity, or corpus frequency to
score `Ppargc1b`.  Corpus records were used only to interpret the measured
training analogs.

## Causal transfer to `Ppargc1b`

`Ppargc1b` encodes PGC-1beta, a transcriptional coactivator rather than a
DNA-binding transcription factor or a mitochondrial structural component.
Published work places PGC-1alpha, PGC-1beta, and PRC/PPRC1 upstream of NRF1,
NRF2/GABP, ERRalpha, and other transcription factors that drive respiratory
chain, mitochondrial biogenesis, and oxidative-metabolism genes
(Scarpulla 2008; Scarpulla 2010).  In primary neurons, PGC-1alpha and
PGC-1beta can independently and additively control mitochondrial density, and
PGC-1beta overexpression can protect against mutant alpha-synuclein- or
huntingtin-associated mitochondrial loss (Wareski et al. 2009).  In myotubes,
PGC-1beta regulation of mitochondrial biogenesis and oxidative phosphorylation
requires NRF1 and ERRalpha promoter inputs (Shao et al. 2010).  Constitutive
whole-body `Ppargc1b` loss has also been linked to altered brain mitochondrial,
mTOR, and ER-stress responses under nutritional stress (Camacho et al. 2012).

Those priors make a same-direction effect on `Esrra`/`Nrf1`-like oxidative
targets plausible:

`Ppargc1b` perturbation -> less PGC-1beta coactivation -> weaker activity of
some ERRalpha/NRF1/GABP targets -> altered mitochondrial and energy-demand
programs -> a possible small survivor-state transcriptomic response in `151`.

However, three candidate-specific points make the transfer weak in this assay:

1. The direct molecular consequence of losing a coactivator is conditional on
   which DNA-bound partners are present and whether PGC-1beta is limiting.
   `Esrra` and `Nrf1` remove DNA-binding factors themselves; `Ppargc1b` does
   not.
2. The best visible paralog, `Ppargc1a`, is an exact zero in the focal training
   endpoint and has no robust downstream signature across measured neuronal
   groups, despite published neuronal PGC-1alpha biology.  This argues that
   acute partial disruption of a PGC coactivator is strongly buffered or
   state-dependent in the P16-to-P37/44 basal snRNA-seq design.
3. The negative `Ppara`/`Ppard`/`Pparg`/`Esrrb`/`Esrrg` controls show that
   sharing the same metabolic nuclear-receptor neighborhood was not enough to
   create FDR-significant DE in recovered `151` neurons.

I therefore expect `Ppargc1b` to have, at most, a faint partial version of the
`Esrra` oxidative-metabolism tendency rather than the 57-DEG `Esrra` signature
or the 138-DEG `Nrf1` state.  Given that the median and 75th percentile of the
training endpoint are 0 and 1, and the closest PGC/PPAR/ERR comparators are
zero, I predict no gene will pass FDR 0.05.

## Prediction

| target | predicted `n_degs` |
| --- | ---: |
| `Ppargc1b` | 0 |

## Limits

The prediction extrapolates because `Ppargc1b` itself has no training signature.
The external literature contains clear PGC-1beta mitochondrial biology, but much
of it is from primary cultured neurons, muscle, hypothalamus, or constitutive
knockout and stress paradigms rather than sparse CRISPR loss of function in
postnatal thalamic glutamatergic nuclei.  The Parquet supplies only
survivor-conditioned differential expression; it does not measure indel
fractions, PGC-1beta protein, mitochondrial mass, respiration, absolute RNA, or
cells lost before harvest.  A subthreshold or physiological mitochondrial
effect could therefore be missed by the DEG-count endpoint.  Finally, a zero
point prediction is a threshold prediction for BH FDR 0.05, not a claim that
PGC-1beta is biologically inert in these neurons.
