# DEG-count prediction trace

## Question and endpoint

I interpreted the task as a scalar prediction for one held-out perturbation,
`Tmem63a`, in `151 TH Prkcd Grin2c Glut` thalamic glutamatergic neurons.  The
point prediction is the number of measured genes with `pvals_adj < 0.05` in the
held-out `Tmem63a` contrast.  The held-out target itself is absent as a
`gene_target` in the supplied differential-expression Parquet and absent from
the training count table, so the predicted count must be inferred from
non-held-out perturbations rather than measured directly.

I counted the target transcript itself as eligible for the endpoint because the
training CSV does so: in the focal Parquet slice, `Tmem63b` has exactly one
`pvals_adj < 0.05` row and it is the `Tmem63b` self transcript, matching
`n_degs=1` in the training table.

## Sources used

- Declared inputs:
  - `training differential-expression dataset`
  - `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`
  - `single-target request for Tmem63a`
- Run-local context:
  - `codex_runtime/pipeline/dataset_context.md`
  - `codex_runtime/pipeline/measurement_registry.json`
  - `codex_runtime/pipeline/task_bindings.json`
  - `codex_runtime/pipeline/coverage.json`
  - `codex_runtime/pipeline/capabilities.json`
- Internal same-experiment interpretation: PerturbAI July sourceguard release
  `july_260713_sourceguard_1773_v1`, queried with `corpus.findings`,
  `corpus.report_evidence`, and the read-only graph only to resolve packaged
  reports and comparator identities for `Tmem63b` and `Tmem63c`.  This corpus
  is a semantic layer over the same experiment, not independent replication.
- External literature from PubMed:
  - Murthy et al. 2018, eLife, doi:10.7554/eLife.41844, PMID:30382938.
  - Zhao et al. 2016, Cell Biochemistry and Function, doi:10.1002/cbf.3185,
    PMID:27045885.
  - Zheng et al. 2023, Neuron, doi:10.1016/j.neuron.2023.07.006,
    PMID:37543036.
  - Vetro et al. 2023, American Journal of Human Genetics,
    doi:10.1016/j.ajhg.2023.06.008, PMID:37421948.
  - Yang et al. 2024, Cell Discovery, doi:10.1038/s41421-023-00628-x,
    PMID:38172113.

## Computations

The held-out manifest contains exactly one requested row, `Tmem63a`; it has no
overlap with the 1,674 training rows in the focal count CSV.

I first summarized the training counts for `151 TH Prkcd Grin2c Glut`.
The distribution is very sparse:

- 1,205 of 1,674 training perturbations have `n_degs = 0`.
- 276 have `n_degs = 1`.
- The median is 0, the 75th percentile is 1, the 90th percentile is 2, and the
  95th percentile is 18.

I then selected the represented TMEM63 paralogs and other ion-channel
comparators from the training table.

| analog class | focal training perturbations | observed focal `n_degs` |
|---|---:|---:|
| TMEM63 paralogs | `Tmem63b`, `Tmem63c` | 1, 0 |
| broader `Tmem` targets in the panel | `Tmem106b`, `Tmem126a`, `Tmem163`, `Tmem165`, `Tmem63b`, `Tmem63c` | 1, 0, 1, 0, 1, 0 |
| TRP-family/channel-like comparators | `Trpa1`, `Trpm3`, `Trpm7`, `Trpv1` | 0, 0, 0, 0 |
| potassium-channel targets | 20 `Kcn*` targets | 15/20 at 0, 5/20 at 1 |
| other cation/calcium-channel targets | `Cacna1a`, `Cacna1d`, `Cacna1e`, `Cacna1g`, `Cacna2d1`, `Cacna2d2`, `Cacnb2`, `Cacnb4`, `Cacng2`, `Cacng3` | mostly 0-1; `Cacna1g` at 12 |

The decisive Parquet query was a direct focal-cell filter:

```python
filter = (
    (ds.field("group_name") == "151 TH Prkcd Grin2c Glut")
    & ds.field("gene_target").isin(["Tmem63b", "Tmem63c"])
)
```

This returned 34,518 rows.  `Tmem63b` had one FDR<0.05 row:
`Tmem63b` itself, log2 fold change -0.701, adjusted p = 4.16e-17, with
150 matched perturbed nuclei and 23,679 controls.  Every non-self row for
`Tmem63b` was adjusted p = 1.0 in this focal cell group.  `Tmem63c` had zero
FDR<0.05 rows; its best adjusted p-value was 0.449 for `Psmc1`, and its own
transcript was not significant in the focal group: log2 fold change -0.317,
adjusted p = 0.975, with 243 matched perturbed nuclei.

I computed the Pearson correlation of focal signed Wilcoxon scores between the
two represented TMEM63 paralogs across the 17,259 genes observed for both:
`r = 0.019`.  This is effectively a null correlation and agrees with the
same-experiment July corpus summary that the full 22-cell-group
`Tmem63b`-versus-`Tmem63c` signed-score cosine was 0.0028 with no robust shared
same-direction FDR<0.10 genes.

Finally, I used `Tmem63a` as a measured gene across all 1,674 represented focal
perturbations.  It never reached FDR<0.05 as a downstream gene; its minimum
adjusted p-value was 0.735.  This does not prove that the `Tmem63a`
self-transcript would be undetectable after `Tmem63a` CRISPR, but it is a
warning that `Tmem63a` expression is not a robust focal DE feature comparable
to the highly significant `Tmem63b` self row.

## Target-specific reasoning

### Tmem63a

The most specific within-dataset analogs are `Tmem63b` and `Tmem63c`, because
Murthy et al. established OSCA/TMEM63 proteins as an evolutionarily conserved
mechanically activated channel family, Zhao et al. reported that mouse
TMEM63A/B/C can confer hyperosmolarity-activated currents in heterologous
cells, and Zheng et al. showed mammalian TMEM63A and TMEM63B are bona fide,
monomeric, high-threshold mechanosensitive ion channels.  That family-level
prior is useful for choosing analogs, but it does not create an obligate same
steady-state transcriptional response in postnatal thalamic neurons.

The training data put both direct paralogs at the assay floor in
`151 TH Prkcd Grin2c Glut`:

- `Tmem63b`: `n_degs=1`; the only focal FDR<0.05 gene was the knocked-down
  `Tmem63b` transcript itself, with no downstream FDR genes.
- `Tmem63c`: `n_degs=0`; no focal self-transcript or downstream FDR genes.

The internal July corpus reinforces the same conclusion across the whole
experiment.  `Tmem63b` was a buffered perturbation: across 22 recovered cell
groups, it produced only two singleton downstream FDR<0.10 events, `Caln1` in
`022 L5 ET CTX Glut` and borderline `Fdft1` in `066 CNU-HYa HY GABA`, while
the focal thalamic group had no downstream FDR<0.10 genes.  `Tmem63c` was
FDR-null in every one of its 22 measured cell groups.  The two represented
paralogs were nonconvergent despite being measured in the same groups.

I also checked the main counterexample direction raised by the Tmem63 reports.
`Tmem63b` had an isolated sterol marker outside the focal cell group, and
stronger sterol programs in the same experiment are carried by `Dctn1`,
`Mib1`, `Tsc2`, and `Srebf2`.  Those are not appropriate direct analogs for
`Tmem63a`: in the focal group, `Dctn1`, `Mib1`, and `Tsc2` have larger DEG
counts of 75, 27, and 86 and induce coordinated sterol genes, while `Srebf2`
has 7 DEGs and is a direct sterol transcription-factor perturbation.  TMEM63A
is an osmo/mechanosensitive channel, not a sterol biosynthesis regulator, and
neither `Tmem63b` nor `Tmem63c` carried a focal sterol response.  The sterol
examples therefore show that the focal assay can see membrane-lipid programs
when engaged, not that `Tmem63a` should be promoted into the tens of DEGs.

The external causal model also favors a null or near-null count.  The
intervention is mosaic P16 CRISPR loss of one TMEM63-family channel in neurons
that are recovered 3-4 weeks later at baseline.  The direct molecular
consequence should impair a high-threshold mechanosensitive or osmosensitive
channel.  Propagation to nuclear RNA would require either a persistent change
in tonic ion flux, a local membrane-lipid program, osmotic challenge, or
selection of sensitive neurons.  Yang et al. showed a specialized baseline
physiologic role for `Tmem63b` in subfornical-organ thirst neurons, and Vetro
et al. showed that human `TMEM63B` disease variants can act through altered
gating and inward leak currents rather than simple loss.  Those mechanisms do
not imply that single-gene `Tmem63a` loss in `151 TH Prkcd Grin2c Glut` cells
under unchallenged conditions should trigger a broad transcriptional state.

I therefore predict that `Tmem63a` behaves more like `Tmem63c` than like a
multi-gene stress perturbation, and I round the expected focal count down to
zero.  A count of one remains plausible if the hidden `Tmem63a` self transcript
is significantly reduced, but the requested point prediction is:

`Tmem63a -> 0`

## Limits and uncertainty

- `Tmem63a` itself is held out as a perturbation, so no direct `Tmem63a` CRISPR
  expression signature or focal `n_degs` is present in the declared inputs.
- The TMEM63-family comparison is the best within-dataset evidence, but only
  `Tmem63b` and `Tmem63c` were available.  Their nonconvergence means paralogy
  is informative mainly as a floor estimate, not as a precise scalar model.
- The assay is baseline nuclear RNA in recovered neurons.  It does not measure
  channel currents, osmotic or mechanical stimulus responses, DNA indels,
  organelle morphology, axonal degeneration, or unrecovered cells.
- A hidden `Tmem63a` self-transcript hit could make the true endpoint 1 even if
  downstream biology is buffered.  I did not use weak or absent self-transcript
  change as editing-efficiency evidence; I used it only to calibrate whether a
  target RNA is likely to contribute one count to the count endpoint.
