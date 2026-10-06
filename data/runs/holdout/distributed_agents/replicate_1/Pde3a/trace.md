# Trace

## Question and endpoint

The held-out target for this run is `Pde3a`. I interpreted the requested value as the
integer number of measured genes in `151 TH Prkcd Grin2c Glut` with
Benjamini-Hochberg-adjusted Wilcoxon `pvals_adj < 0.05` after sparse P16-to-P37/44
AAV CRISPR loss of `Pde3a`.

Two points determined the route:

- `Pde3a` is completely held out: it is absent from the training DE parquet as a
  `gene_target` and absent from the training count CSV.
- This is a one-target scalar count prediction, not a ranking. I therefore did
  not use the rank-only `dataset.perturbseq_features`,
  `synthesis.ordering_validate`, or `corpus.predictive_graph_review`
  capabilities.

## Sources

Primary internal data:

- Declared DE table:
  `training differential-expression dataset`.
- Training endpoint table:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Requested-target manifest:
  `single-target request for Pde3a`.

Same-experiment interpretive layer:

- PerturbAI July same-experiment corpus,
  `perturbai-july-260713-sourceguard-1773-v1`, queried through the declared
  bounded `corpus.calibration` and `corpus.findings` capabilities. I used this
  only for packaged interpretation of visible held-in comparators; counts and
  focal FDR calls below come from the parquet and endpoint CSV.

External literature:

- Kelly et al. 2013, `10.1016/j.cellsig.2013.10.007`, mapped PDE isoform
  expression across adult rodent brain and showed unique, conserved regional
  patterns for individual PDE genes.
- Enterria-Morales et al. 2020, `10.1093/braincomms/fcaa105`,
  identified `Pde3a` as enriched in mouse striatal parvalbumin interneurons in
  a screen for molecular targets linked to endogenous striatal `Gdnf`.
- Bompierre et al. 2024, `10.1111/bph.17400`, showed that PDE1A, PDE3A and
  PDE4 are major controllers of cAMP in mouse striatal cholinergic
  interneurons.

The same-experiment `Pde10a` report in the July corpus also cited striatal
PDE10A localization and acute inhibitor work, including Xie et al. 2006 and
Strick et al. 2010, to interpret why its small in-atlas response was
striatal/GABAergic rather than thalamic.

## Dataset calculations

I first read the training count CSV for all visible genes whose names put them
near `Pde3a` in cyclic-nucleotide signaling. The represented phosphodiesterase
targets in the focal endpoint were:

| visible target | focal `n_degs` |
|---|---:|
| `Pde10a` | 0 |
| `Pde1c` | 0 |
| `Pde4b` | 0 |
| `Pde4d` | 0 |

I then sliced the DE parquet to
`group_name == "151 TH Prkcd Grin2c Glut"` for PDE/cAMP/PKA neighbors and
counted both FDR-supported rows and nominal rows. The closest focal surfaces
were all downstream-null at FDR 0.05:

| visible target | `n_pert_matched` | FDR < 0.05 genes | raw p < 0.05 genes | minimum adjusted p-value |
|---|---:|---:|---:|---:|
| `Pde10a` | 191 | 0 | 385 | 0.304 |
| `Pde1c` | 155 | 0 | 361 | 0.180 |
| `Pde4b` | 211 | 0 | 317 | 0.922 |
| `Pde4d` | 192 | 0 | 328 | 1.000 |
| `Adcy1` | 88 | 0 | 346 | 0.139 |
| `Adcy3` | 223 | 0 | 355 | 0.112 |
| `Adcy5` | 154 | 0 | 319 | 0.912 |
| `Gnas` | 306 | 0 | 374 | 1.000 |
| `Gnal` | 148 | 0 | 307 | 1.000 |
| `Rapgef2` | 113 | 0 | 329 | 1.000 |
| `Rapgef4` | 177 | 0 | 314 | 1.000 |

`Prkaca`, `Prkar1a`, `Gnao1`, and `Prkcg` had one focal FDR < 0.05 row each,
but in each case that one row was the perturbed transcript itself. The endpoint
count includes self rows, so those are `n_degs = 1` in the training CSV, but
they did not provide downstream cyclic-nucleotide expression analogs for a
held-out PDE.

For expression-pattern evidence, I compared the focal Wilcoxon score vectors
among this visible cAMP/PDE set. Spearman correlations of scores were all near
zero. Examples most relevant to `Pde3a` were:

- `Pde10a` versus `Pde1c`: 0.008
- `Pde10a` versus `Pde4b`: -0.027
- `Pde10a` versus `Pde4d`: -0.009
- `Pde10a` versus `Adcy5`: 0.012
- `Pde1c` versus `Pde4b`: -0.005
- `Pde1c` versus `Pde4d`: 0.007

Those correlations argue against a hidden common thalamic PDE/cAMP signature in
which individual analogs missed FDR solely because of sampling. The raw nominal
tails in the PDE knockouts also did not form a near-threshold response:
`Pde4b` and `Pde4d` had best focal FDR values of 0.922 and 1.0, and the best
`Pde10a` focal row was `Smpd4` with FDR 0.304.

I also read bounded same-experiment Findings for the visible analogs. They
reported that `Pde1c` and `Pde4d` were pan-measured central-neuron downstream
nulls, `Pde4b` had only two robust off-focal hits in `155 MB Glut` and
`191 MB P MY GABA`, and `Pde10a` had a small on-mechanism `Scg2`/`Crem`
signature in `059 CNU-LGE LSX GABA` but 0 downstream genes in
`151 TH Prkcd Grin2c Glut`. The same inventory also reported that the measured
adenylyl cyclases `Adcy1`, `Adcy3`, and `Adcy5` were downstream-null in their
recovered neuronal groups.

## Target-specific prediction

### `Pde3a`

`Pde3a` encodes a cGMP-inhibited cAMP phosphodiesterase. Complete PDE3A
manipulation can control cAMP in defined striatal interneurons: it is enriched
in striatal parvalbumin interneurons in the Enterria-Morales et al. mouse
PV-interneuron comparison, and Bompierre et al. directly found that PDE3A helps
set cAMP dynamics in mouse striatal cholinergic interneurons. That external
knowledge made `Pde10a`, `Pde1c`, `Pde4b`, `Pde4d`, adenylyl cyclases, G
proteins, PKA, and Epac/RapGEF perturbations the correct visible neighborhood
to interrogate.

The experimental causal model is:

`Pde3a` CRISPR loss in P16 postmitotic neurons -> lower PDE3A-dependent local
cAMP hydrolysis where the isoform is present and nonredundant -> changed
cyclic-nucleotide/PKA/Epac signaling -> possible CREB or activity-regulated RNA
changes in the recovered cell group -> BH-counted focal DEGs at P37-P44.

The weak link in that chain is the exposure/context step for
`151 TH Prkcd Grin2c Glut`. The strongest `Pde3a` neuronal priors point to
striatal interneurons, whereas the focal group is thalamic glutamatergic. The
best striatal PDE comparator in the training atlas, `Pde10a`, behaved in the
expected direction: it had its interpretable response in a striatal-like
`059 CNU-LGE LSX GABA` bin, but in the focal thalamic bin it had 191 matched
perturbed nuclei, zero FDR < 0.05 rows, and no close nominal miss
(`min q = 0.304`). The four visible PDE knockouts were all exactly zero in the
focal endpoint, and the represented cAMP-production nodes were also exactly
zero. Direct PKA perturbations did not reveal a downstream focal response:
`Prkaca` and `Prkar1a` only passed FDR for their own transcripts.

`Creb1` and `Crebbp` are useful counterexamples rather than positive analogs.
They showed that the `151` thalamic group can produce a small FDR-supported
cyclic-nucleotide-adjacent nuclear transcriptional response, with 10 and 8
FDR < 0.05 rows respectively, but the program sat at the CREB/CBP nuclear arm
and did not correlate with the visible PDE score vectors. A PDE3A local cAMP
buffer in a striatal interneuron is therefore too indirect to transfer the
`Creb1`/`Crebbp` count to the held-out focal thalamic perturbation.

I predict `Pde3a` will have no BH-significant measured genes in
`151 TH Prkcd Grin2c Glut`:

- zero/nonzero call: zero;
- point count: 0;
- primary driver: within-dataset zeros for all represented focal PDEs and
  cAMP-production genes, plus external `Pde3a` biology that localizes the best
  neuronal expectation away from the focal thalamic glutamatergic context.

## Limits

This is still an extrapolation because no held-in target is a one-to-one
`Pde3a` paralog; `Pde3b`, `Pde2a`, `Pde1a`, `Pde1b`, and several other PDEs were
not visible training targets in the focal count table. PDE3A protein, cAMP,
cGMP, DNA editing, spiking, and acetylcholine release were not measured, so a
zero RNA prediction does not mean that `Pde3a` editing would be functionally
silent. The assay is also survivor-conditioned and averages over a broad
thalamic glutamatergic label; a rare PDE3A-expressing subcluster or a
non-transcriptional electrophysiological phenotype could be missed. The final
integer should therefore be read as a prediction for the task's exact
BH-counted `151 TH Prkcd Grin2c Glut` endpoint, not as a judgment of PDE3A
biology in all neurons.
