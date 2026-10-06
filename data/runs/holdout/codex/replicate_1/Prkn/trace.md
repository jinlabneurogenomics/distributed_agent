# Prkn direct n_degs forecast

Target: `Prkn`

Cell group: `151 TH Prkcd Grin2c Glut`

Endpoint: number of measured genes in the focal thalamic class with BH-adjusted
Wilcoxon `p < 0.05`.

## Evidence Used

- The declared biology bundle and the runtime `characterization_bundle` biology
  view exposed only endpoint-blind biology for `Prkn`. In the exact focal
  population reach record, `Prkn` was measured in `151 TH Prkcd Grin2c Glut`,
  with 16,623 of 23,679 non-target nuclei expressing the transcript
  (70.201%), mean CP10K 0.899, and the perturbation contrast available.
- The same biology bundle places Parkin as a PINK1/phospho-ubiquitin-activated
  RBR E3 ubiquitin ligase. A P16 edit is expected to stop new Parkin production
  in edited cells, but the operative Parkin stock at the P37-P44 harvest is
  indeterminate: endogenous Parkin was only shown to persist over a six-hour
  neuronal translation-block chase, not over 21-28 days, and the nearest mouse
  neural knockout evidence is mixed across hippocampal and midbrain contexts.
- The focal training count table is sparse: 1,205 of 1,674 visible training
  perturbations have `n_degs = 0`, 276 have `n_degs = 1`, the median is 0, the
  90th percentile is 2, and the 95th percentile is 18.
- A Parquet query over the focal class showed that self-transcript calls account
  for much of the one-count mass: 319 of 1,674 training targets have their own
  transcript significant at `pvals_adj < 0.05`, and 237 of the 276 one-DEG rows
  are self-only. I used this only as literal count accounting for the requested
  endpoint, not as evidence for functional knockout strength.
- The most relevant basal Parkinson/mitochondrial-quality-control and stress
  comparators were low in the exact focal count table:

  | target | focal `n_degs` | focal FDR<0.05 interpretation |
  | --- | ---: | --- |
  | `Park7` | 1 | self transcript only |
  | `Atp13a2` | 1 | self transcript only |
  | `Sqstm1` | 1 | self transcript only |
  | `Tomm40` | 1 | self transcript only |
  | `Uchl1` | 1 | self transcript only |
  | `Sncb` | 1 | self transcript only |
  | `Nfe2l2` | 0 | no focal call |
  | `Snca` | 0 | no focal call |
  | `Atp13a3` | 0 | no focal call |
  | `Afg3l2` | 0 | no focal call |
  | `Clpp` | 0 | no focal call |
  | `Lonp1` | 0 | no focal call |
  | `Mff` | 0 | no focal call |
  | `Yme1l1` | 0 | no focal call |

- Same-experiment corpus records for visible training perturbations agree with
  the Parquet interpretation, but are not independent replication. They
  describe `Park7` as downstream-null across recovered neuronal groups, `Tomm40`
  as pan-neuronal downstream-null despite focal target-transcript loss, and
  `Atp13a2` as buffered with expected lysosomal/autophagy/UPR programs absent.
  `Sqstm1` produced only a very sparse three-cell-type surface.
- Larger stress responses are possible in this class, but the examples are
  mechanistically farther from basal Parkin loss: `Opa1` had 37 focal DEGs,
  `Vps35` had 17, `Hspa5` had 5, and `Rab7` had 501. These are inner-membrane
  fusion, retromer/endosomal sorting, ER chaperone, and late-endosomal
  trafficking perturbations that directly enter organelle-stress states. Parkin
  is a stress-recruited mitophagy E3, and the `Prkn` bundle did not establish
  comparable basal mitochondrial-damage demand in juvenile thalamic neurons.

## Synthesis

The local evidence supports a near-null downstream transcriptional response for
`Prkn` in the unchallenged juvenile thalamic population. Its closest basal
Parkinson and autophagy pathway comparators are either zero or one-count
self-only perturbations, and the corpus explicitly treats several of those
profiles as buffered rather than as hidden broad stress states.

The difference between forecasting 0 and 1 is therefore mostly whether the
measured `Prkn` transcript itself crosses FDR. The target transcript is present
in most focal non-target nuclei, and one-count self-only profiles are common
among the relevant visible analogs. I therefore expect no downstream DEGs plus
one self-transcript call.

Predicted `n_degs`: 1
