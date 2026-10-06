# DEG-count prediction trace

## Question and endpoint

The requested held-out perturbation is `Chrna5`; the target CSV contains this
single row and no other targets. I interpreted the endpoint exactly as
`n_degs` in `151 TH Prkcd Grin2c Glut`: the number of measured genes in the
held-out perturbation with Scanpy Wilcoxon Benjamini-Hochberg adjusted
`pvals_adj < 0.05`. A value can include the perturbed transcript itself when
that transcript is measured and FDR-significant. That convention explains
`Ache` and `Chrnb2` in the training count table: both have 1 DEG in the focal
table, and in the declared parquet the only FDR < 0.05 focal row is their own
transcript.

`Chrna5` was held out entirely as a `gene_target`, so no `Chrna5` perturbation
DE rows were used. The prediction is a transfer from non-held-out targets and
from the biological role of alpha5 nicotinic acetylcholine receptor subunits.

## Sources

- Declared training endpoint:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared differential-expression parquet:
  `training differential-expression dataset`.
- Requested-target manifest:
  `single-target request for Chrna5`.
- Dataset portrait and measurement registry in `codex_runtime/pipeline`, used
  for assay design, focal cell semantics, and measurement limits.
- Internal corpus: `perturbai-july-260713-sourceguard-1773-v1`, queried through
  the declared `corpus.calibration`, `corpus.findings`, and
  `corpus.report_evidence` operations for packaged same-experiment comparator
  summaries.
- External mechanism references: NCBI Gene and UniProtKB for receptor-subunit
  identities; Picciotto and Kenny 2021, DOI `10.1101/cshperspect.a039610`;
  Scholze and Huck 2020, DOI `10.3389/fnsyn.2020.607959`; Morton et al. 2018,
  DOI `10.1523/JNEUROSCI.0023-18.2018`; McClure-Begley et al. 2009, PMID
  `19139153`; Venkatesan et al. 2023, DOI `10.1016/j.isci.2023.105992`.

The requested endpoint is directly observed for the training perturbations in
the focal count CSV. It is absent, by construction, for `Chrna5`.

## Computation over the declared inputs

I first loaded the focal count CSV and looked up cholinergic receptor and
acetylcholine-related perturbations:

| training target | `n_degs` in `151 TH Prkcd Grin2c Glut` |
| --- | ---: |
| `Chrna1` | 0 |
| `Chrna2` | 0 |
| `Chrna3` | 0 |
| `Chrna4` | 2 |
| `Chrna6` | 0 |
| `Chrna7` | 0 |
| `Chrnb1` | 0 |
| `Chrnb2` | 1 |
| `Chrnb3` | 0 |
| `Chrm2` | 0 |
| `Chrm3` | 0 |
| `Ache` | 1 |

The full training table has 1,674 perturbations. Its median count is 0, 75th
percentile is 1, 90th percentile is 2, 95th percentile is 18, and 469 of 1,674
targets are nonzero. Thus a 0 to 2 count is common, while broad signatures are
rare and concentrated in non-receptor regulators such as `Uba5`, `Tpr`,
`Sin3a`, spliceosome and proteasome components.

I then filtered the parquet to the focal cell group for the same comparator
set and inspected nominal rows with `pvals < 0.001`. The FDR-supported focal
events were:

| training target | matched perturbed nuclei | FDR < 0.05 focal rows |
| --- | ---: | --- |
| `Chrna4` | 293 | `Chrna4` logFC -0.336607, FDR 0.003726; `Cyp46a1` logFC -0.195417, FDR 0.003726 |
| `Chrnb2` | 222 | `Chrnb2` logFC -0.516730, FDR 7.37e-7 |
| `Ache` | 117 | `Ache` logFC -0.673707, FDR 0.004149 |
| `Chrna1` | 192 | none; best nominal `Mtif2`, FDR 0.779 |
| `Chrna2` | 231 | none; all nominal rows FDR 1 |
| `Chrna3` | 148 | none; best nominal `Aifm3`, `Inpp5f`, `Adam22`, and `Virma`, all FDR 0.499 |
| `Chrna6` | 133 | none; all nominal rows FDR 1 |
| `Chrna7` | 212 | none; all nominal rows FDR 1 |
| `Chrnb1` | 139 | none; all nominal rows FDR 1 |
| `Chrnb3` | 120 | none; all nominal rows FDR 1 |
| `Chrm2` | 155 | none; all nominal rows FDR 1 |
| `Chrm3` | 120 | none; all nominal rows FDR 1 |

These focal rows show that the nonzero close analogs are self-transcript or
single-downstream-gene events, not coordinated activity or stress signatures.

## Same-experiment receptor evidence

The July same-experiment corpus supports the same interpretation across the
full cell-group surface:

- `Chrna4` is the nearest functional training analog because alpha4 beta2
  receptors are the major high-affinity brain nAChR class and can include
  accessory alpha5. In `151 TH Prkcd Grin2c Glut`, `Chrna4` produced only its
  own transcript plus `Cyp46a1` at FDR < 0.05. The packaged report further
  states that its only FDR < 0.10 downstream event across all 23 cell groups was
  `Cyp46a1` in this focal group, that `Chrnb2` did not phenocopy the `Cyp46a1`
  edge, and that `Chrna5` and `Chrnb4` were absent as perturbation targets.
- `Chrnb2` is the obligatory beta partner for most alpha4-containing brain
  receptors and therefore a stringent alpha5 comparator. It had `n_degs = 1`
  in the focal count table, but the corpus resolves that as a self-transcript
  event: across 22 measured groups it had 0 non-`Chrnb2` genes at FDR < 0.10.
  Alpha2/alpha4 showed only isolated one-gene FDR < 0.10 hits in the
  `Chrnb2`-matched groups, while `Chrna3`, `Chrna6`, `Chrna7`, and `Chrnb3`
  were flat.
- `Chrna7`, a different nicotinic alpha subunit with homomeric calcium
  signaling biology, had `n_degs = 0` in the focal table and no robust
  downstream response in any recovered neuronal cell group. Its paired
  receptor-family score-vector correlations with `Chrna1`, `Chrna2`, `Chrna3`,
  `Chrna4`, `Chrna6`, `Chrnb1`, `Chrnb2`, `Chrnb3`, `Chrm2`, `Chrm3`, and
  `Ache` were all near zero in the packaged same-experiment analysis.
- The broader cholinergic controls agree: `Ache` depletion was detected in the
  focal group but produced no non-self focal DEG and no persistent
  immediate-early/activity module; `Chrm2` and `Chrm3` were transcriptionally
  silent across recovered neuronal groups.

Mechanistically, an alpha5 knockout changes nAChR composition or gating only in
cells that express alpha5-containing receptors. It is not an obligate catalytic
or transcription-factor subunit whose partial loss should force a broad
resident-neuron RNA program. Picciotto and Kenny summarize alpha4 beta2 star
receptors as the predominant brain nAChR class and the `CHRNA5-CHRNA3-CHRNB4`
cluster as a nicotine-dependence locus; Scholze and Huck summarize alpha5 as
an accessory subunit that modulates alpha4 beta2 star and alpha3 beta4 star
receptor function. McClure-Begley et al. provide a direct mouse-brain
alpha4/alpha5/beta2 electrophysiologic comparator through acetylcholine-evoked
GABA release. Morton et al. localize the strongest rodent `Chrna5` expression
and alpha5-null physiological effects to the interpeduncular nucleus, and
Venkatesan et al. show a specialized adult `Chrna5`-expressing subplate
population. Those priors make alpha5 biologically real, but they point to
specific receptor physiology, nicotine exposure, IPN or cortical subplate
contexts, not to a constitutive thalamic glutamatergic DEG program after sparse
postnatal coding loss.

## Target-specific prediction

### `Chrna5`

Relevant positive analogs are weak. The strongest one is `Chrna4`, because
alpha5 can assemble into alpha4 beta2 receptors. However, `Chrna4` itself gave
only two focal DEGs, one self row plus the recurrent `Cyp46a1` sentinel, and
the same report found no cholinergic-subunit compensation or Fos/Arc/Egr1/Npas4
activity program. The other alpha4 beta2 component, `Chrnb2`, gave only a
self-transcript focal hit and no non-self gene at FDR < 0.10 anywhere in the
measured cell groups. The `Chrnb2` result is especially important: if loss of
the main beta subunit is almost transcriptionally silent, loss of the accessory
alpha5 subunit should not exceed it in a broad thalamic snRNA-seq DEG count
unless the focal class were selectively alpha5 dependent.

The negative counterexamples are also close. Training perturbations of
`Chrna1`, `Chrna2`, `Chrna3`, `Chrna6`, `Chrna7`, `Chrnb1`, `Chrnb3`, `Chrm2`,
and `Chrm3` were all zero in the focal group, and `Ache` reached one only
through the `Ache` transcript itself. The internal corpus summarizes the
represented cholinergic receptor neighborhood as sparse across the full surface
rather than a hidden shared receptor signature. Nothing in the external alpha5
literature supplies a candidate-specific reason to expect focal thalamic
`Chrna5` loss to create a broader or more reproducible mRNA state than
`Chrna4` or `Chrnb2`; the best-established effects are electrophysiological,
nicotine-exposure, or IPN/subplate-specific.

I therefore predict zero DEGs. The main ambiguity is whether the held-out
`Chrna5` target transcript itself would be sufficiently expressed and knocked
down in `151 TH Prkcd Grin2c Glut` to count as a one-gene self hit. Because
most alpha-subunit perturbations in this focal group did not even yield a
self-transcript FDR hit, and because `Chrnb2`/`Chrna4` already bound the
maximum plausible alpha5-like count at one to two isolated rows, the best point
estimate is 0 rather than 1.

## Limits

This prediction is an extrapolation from receptor partners and pathway
neighbors; there is no direct `Chrna5` perturbation signature in either input.
The Parquet and the internal July corpus are two representations of the same
experiment, not independent replication. The corpus helped identify
full-surface nulls and exact receptor comparators but did not add a second
measurement. External studies establish receptor composition and circuit
functions under germline, engineered, or nicotine-stimulated conditions; those
readouts do not measure the P16-to-P37/44 sparse CRISPR basal snRNA-seq DEG
endpoint. A rare Chrna5-positive thalamic subset or a transient activity
response could be diluted or missed, and the point estimate should be read as
a prediction of zero FDR-significant measured genes in this assay, not as
absence of alpha5 nAChR physiology.
