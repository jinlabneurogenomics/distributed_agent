# DEG-count prediction trace

## Question and endpoint

The requested prediction is the integer number of genes expected to pass
Benjamini-Hochberg FDR 0.05 after each held-out perturbation in the
`151 TH Prkcd Grin2c Glut` class.  The held-out manifest contains one target:

| target_name |
|---|
| Adora2a |

I treated the output as an assay-calibrated focal-cell DEG-count endpoint, not
as a general estimate of A2A receptor importance, editing efficiency, viability,
or electrophysiologic effect size.  The held-out perturbation itself has no row
in either the focal training-count CSV or the all-cell-group differential
expression Parquet, so the prediction has to be transferred from visible
training targets and external gene-function priors.

## Sources used

- Declared input endpoint table:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared input differential-expression table:
  `training differential-expression dataset`.
- Run-local requested-target manifest:
  `single-target request for Adora2a`.
- Internal same-experiment semantic corpus:
  `perturbai-july-260713-sourceguard-1773-v1`, specifically packaged Findings
  records for `Drd2`, `Gnal`, `Adcy5`, and `Pde10a`.  These records are
  interpretations of the same experiment, not independent replication.
- External gene-function evidence from PubMed and Allen Mouse Brain Atlas:
  Lein et al. 2006, DOI `10.1038/nature05453`, PMID `17151600`; Nishi et al.
  2008, DOI `10.1523/JNEUROSCI.2518-08.2008`, PMID `18923023`;
  Bertran-Gonzalez et al. 2009, DOI `10.1038/npp.2008.228`, PMID `19158668`;
  Farrell et al. 2012, DOI `10.1038/npp.2012.251`, PMID `23303063`; Zhang et
  al. 2016, DOI `10.1016/j.celrep.2016.06.090`, PMID `27452460`.

The task is a scalar count prediction, not a ranked-output task with active
rank supervision.  The run-local manifest therefore marked
`dataset.perturbseq_features`, `corpus.predictive_graph_review`, and
`synthesis.ordering_validate` unavailable, and I did not use them.

## Quantitative calibration

The focal endpoint table contains 1,674 visible training perturbations.  Its
`n_degs` distribution is sparse and strongly right-tailed:

| statistic | n_degs |
|---|---:|
| zero-count targets | 1205 |
| median | 0 |
| 75th percentile | 1 |
| 90th percentile | 2 |
| 95th percentile | 18 |
| 99th percentile | 436 |
| maximum | 2677 |

Thus the empirical default in `151 TH Prkcd Grin2c Glut` is no FDR 0.05 hit,
with broad signatures confined to a small set of unrelated high-impact nuclear,
proteostasis, or transcriptional regulators.

I then pulled exact rows from the all-cell-group Parquet for the focal class and
training perturbations on the dopamine/adenosine/cAMP axis.  The scan was
filtered by `group_name == "151 TH Prkcd Grin2c Glut"` and by a small
`gene_target` list; for each target I recomputed `sum(pvals_adj < 0.05)`, kept
the number of nominal `pvals < 0.05` genes, and checked the minimum adjusted
p-value.  The relevant focal-cell results were:

| training perturbation | relationship to Adora2a | focal n_degs | expression-pattern evidence |
|---|---|---:|---|
| `Drd2` | Gi/o antagonist of A2A/Golf/cAMP signaling in striatopallidal neurons | 0 | no FDR 0.05 genes; minimum adjusted p-value 1.0 |
| `Gnal` | G alpha olf subunit coupling A2A and D1 receptors to adenylyl cyclase | 0 | no FDR 0.05 genes; minimum adjusted p-value 1.0 |
| `Gnas` | stimulatory G alpha family member upstream of cAMP | 0 | no FDR 0.05 genes; minimum adjusted p-value 1.0 |
| `Adcy5` | striatum-enriched adenylyl cyclase downstream of A2A/Golf | 0 | no FDR 0.05 genes; minimum adjusted p-value 0.91 |
| `Adcy1` | neuronal membrane adenylyl cyclase | 0 | no FDR 0.05 genes; minimum adjusted p-value 0.14 |
| `Adcy3` | neuronal membrane adenylyl cyclase | 0 | no FDR 0.05 genes; minimum adjusted p-value 0.11 |
| `Pde10a` | striatal cyclic-nucleotide phosphodiesterase, opposite enzymatic arm from AC activity | 0 | no FDR 0.05 genes; minimum adjusted p-value 0.30 |
| `Pde4b` | cAMP phosphodiesterase | 0 | no FDR 0.05 genes; minimum adjusted p-value 0.92 |
| `Pde4d` | cAMP phosphodiesterase | 0 | no FDR 0.05 genes; minimum adjusted p-value 1.0 |
| `Prkaca` | PKA catalytic subunit | 1 | the single FDR 0.05 hit was `Prkaca` itself; no downstream FDR hit |
| `Prkar1a` | PKA regulatory subunit | 1 | the single FDR 0.05 hit was `Prkar1a` itself; no downstream FDR hit |
| `Gpr158`, `Gprasp2` | generic GPCR / GPCR-associated counterexamples | 1 each | each one-gene call was its own target transcript, not an A2A-like downstream state |

No adenosine receptor paralog was represented as a training perturbation:
`Adora1`, `Adora2b`, and `Adora3` were absent alongside the held-out
`Adora2a`.

## Target-specific reasoning

### Adora2a

`Adora2a` encodes the adenosine A2A receptor.  A2A is best established in
striatal indirect-pathway, striatopallidal medium spiny neurons, where it is a
G alpha s/G alpha olf-coupled receptor that increases cAMP/PKA signaling and
opposes dopamine D2 receptor signaling.  The BAC strategy used by Farrell et
al. exploited `Adora2a` regulatory sequence to drive a Gs DREADD selectively in
striatopallidal MSNs, and CNO activation of that receptor induced DARPP-32
phosphorylation, matching endogenous striatal Gs signaling.  Bertran-Gonzalez
et al. showed that D2 blockade promotes histone H3 phosphorylation through
tonic A2A/G alpha olf/PKA/DARPP-32 signaling in striatopallidal neurons.
Nishi et al. separated PDE10A and PDE4 control of striatal cAMP/PKA signaling.
Zhang et al. placed `Adora2a`, `P2ry1`, `Gpr6`, and `Grik3` in a
Sp9-dependent striatopallidal differentiation program.  The Allen Mouse Brain
Atlas provides the corresponding anatomical prior: `Adora2a` is a basal
ganglia/striatal marker rather than a thalamic glutamatergic marker.

Those priors make `Drd2`, `Gnal`, `Gnas`, `Adcy5`, `Adcy1`, `Adcy3`,
`Pde10a`, `Pde4b`, `Pde4d`, `Prkaca`, and `Prkar1a` the most relevant visible
training perturbations.  They also make the direction of transfer limited:
`Adora2a` loss should decrease ligand-driven A2A/Golf/cAMP signaling, whereas
`Pde10a` loss can raise cyclic-nucleotide signaling by reducing degradation,
and `Drd2` loss removes an inhibitory Gi/o input.  The appropriate shared stage
is therefore not a common transcriptional complex but the same second-messenger
network upstream or downstream of cAMP/PKA.

In the focal thalamic glutamatergic group, all receptor, G protein,
adenylyl-cyclase, and phosphodiesterase comparators on this axis had zero
downstream FDR 0.05 genes.  Even the closer striatal components `Drd2`, `Gnal`,
and `Adcy5` were flat in `151 TH Prkcd Grin2c Glut`.  The internal
same-experiment corpus reinforced this as a real pathway-specific pattern:
`Adcy5` produced zero downstream FDR 0.10 genes across 22 recovered neuronal
groups; `Drd2` failed to induce a durable Fos/Egr/Arc/Crem or
Penk/Ppp1r1b-like cAMP/indirect-pathway panel; `Gnal` showed only isolated
signals outside the focal class; and `Pde10a` had a small cAMP-linked
`Scg2`/`Crem` response in the striatal-associated `059 CNU-LGE LSX GABA`
group while remaining non-significant in the focal thalamic group.

I therefore predict no detectable focal response for `Adora2a`, with the
zero/nonzero decision driven primarily by the focal training counts for
biochemical neighbors and secondarily by the anatomical prior that the A2A
receptor is a striatopallidal cAMP regulator rather than a core thalamic
glutamatergic gene.

Predicted `n_degs`: **0**

## Limits and extrapolation

The held-out endpoint for `Adora2a` is absent from the declared inputs by
design, and no adenosine receptor paralog was visible as a direct training
perturbation.  The inference therefore uses pathway transfer from dopamine,
G-protein, adenylyl-cyclase, phosphodiesterase, and PKA perturbations rather
than an exact receptor-family phenocopy.  A2A receptor biology is heavily
ligand-, region-, and cell-type-dependent; the Perturb-seq assay measured only
basal nuclear RNA 3-4 weeks after sparse P16 CRISPR loss, not cAMP levels,
phospho-PKA substrates, evoked activity, or adult striatal behavior.  A small
single-gene self-target response cannot be excluded, as `Prkaca`, `Prkar1a`,
`Gpr158`, and `Gprasp2` show, but the held-out target itself was not measured as
a perturbation and the closest cAMP source-arm perturbations were fully FDR
flat in the requested thalamic class.
