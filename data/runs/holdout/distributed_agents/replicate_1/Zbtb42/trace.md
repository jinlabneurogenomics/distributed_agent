# DEG-count prediction for `151 TH Prkcd Grin2c Glut`

## Question and endpoint

I interpreted the task as a one-target prediction:

- held-out target: `Zbtb42`
- cell group: `151 TH Prkcd Grin2c Glut`, a thalamic glutamatergic class
- endpoint: `n_degs`, the number of measured genes with Wilcoxon
  Benjamini-Hochberg-adjusted `pvals_adj < 0.05` in perturbed recovered nuclei
  versus matched controls

The requested target was absent from both supplied training inputs, so its
endpoint and its expression signature were not directly observed.  The training
DEG counts are a direct observation of the same endpoint for non-held-out
targets.  The differential-expression Parquet is direct evidence for expression
signatures of training perturbations in the same experiment and focal cell
group.  External gene-function literature is a prior used to decide which
training perturbations are plausible analogs or counterexamples.

## Sources used

### Declared Perturb-seq inputs

- `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`
  gave the observed `n_degs` values for 1,674 non-held-out targets.
- `training differential-expression dataset`
  gave per-gene log-fold changes, signed Wilcoxon scores, adjusted p-values,
  and matched perturbed/control nucleus counts.  I filtered it to
  `group_name = '151 TH Prkcd Grin2c Glut'` and to selected training analogs.
- `single-target request for Zbtb42`
  supplied the requested target list.  It contained exactly `Zbtb42`.

I used the run-local capability and measurement manifests only to establish
that this is a scalar count prediction, not a ranked output.  The
`dataset.perturbseq_features`, `corpus.predictive_graph_review`, and
`synthesis.ordering_validate` capabilities were explicitly unavailable for this
task type, so I did not invoke them.  I did not use the same-experiment
Finding/Claim graph or internal report corpus for endpoint evidence.

### External literature

PubMed was queried through NCBI PubMed E-utilities.  The two target-specific
papers that changed the biological prior were:

- Devaney, Mate, Devaney and Hoffman, 2010, "Characterization of the ZBTB42
  gene in humans and mice", PMID 21193930, DOI 10.1007/s00439-010-0940-2.
  This characterized ZBTB42 as a conserved two-exon zinc-finger/BTB nuclear
  protein, with mouse tissue distribution strongest in skeletal muscle and
  ovary and with enrichment in nuclei underlying neuromuscular junctions.
- Patel, Smith, Faqeih, Mohamed, Gupta and Alkuraya, 2014, "ZBTB42 mutation
  defines a novel lethal congenital contracture syndrome (LCCS6)",
  PMID 25055871, DOI 10.1093/hmg/ddu384.  This linked recessive human
  ZBTB42 mutation and zebrafish zbtb42 knockdown to abnormal skeletal-muscle
  development and myofibrillar disorganization.

Those data support a muscle/neuromuscular developmental function but do not
establish an obligate postnatal thalamic-neuron complex, pathway, or regulator
whose perturbation was represented by a strong training response.

## Quantitative checks over the training data

The focal training endpoint is highly zero-inflated.  Among the 1,674 training
perturbations, 1,205 had `n_degs = 0`; the median was 0, the 75th percentile was
1, the 90th percentile was 2, the 95th percentile was 18, and the maximum was
2,677.  Thus an unvalidated held-out target should not be assigned a nonzero
count unless either a within-dataset analog or target-specific biology argues
for a response broad enough to pass FDR 0.05 in this sparse AAV-CRISPR assay.

Because `Zbtb42` is a C2H2 zinc-finger/BTB protein, I inspected the ZBTB-family
training perturbations first, then nearby zinc-finger transcriptional regulators
as looser counterexamples.  The targeted Parquet query read only
`151 TH Prkcd Grin2c Glut` rows for those candidate analogs:

```python
filter = (
    (pc.field("group_name") == "151 TH Prkcd Grin2c Glut")
    & pc.field("gene_target").isin(zbtb_and_zfp_targets)
)
```

All inspected focal signatures had 17,259 measured rows and 23,679 matched
control nuclei.  The relevant observed training counts were:

| training target | matched perturbed nuclei | observed focal `n_degs` | expression-pattern evidence in `151 TH Prkcd Grin2c Glut` |
| --- | ---: | ---: | --- |
| `Zbtb10` | 187 | 0 | no FDR-significant measured gene; the most nominal rows were weak, with `pvals_adj = 1.0` |
| `Zbtb16` | 180 | 0 | no FDR-significant measured gene; the most nominal rows were weak, with `pvals_adj = 1.0` |
| `Zbtb20` | 185 | 0 | no FDR-significant measured gene; the best adjusted p-value was 0.71 |
| `Zbtb21` | 137 | 0 | no FDR-significant measured gene; the most nominal rows were weak, with `pvals_adj = 1.0` |
| `Zbtb38` | 199 | 1 | exactly one significant gene, `Msra`, adjusted p = 0.0045 |
| `Zbtb18` | 208 | 5 | a small positive signature: `Endou`, `Pxdn`, `Clstn2`, `Man2a2`, and `Zbtb18` itself were significant |
| `Zbtb7a` | 282 | 841 | a broad transcriptional response, starting with strong up-regulation of `Pnma3`, `Col9a3`, `Gpc1`, `Usp11`, and `Sema4a` |

The zero-DEG ZBTB training genes are the closest empirical analogs for a
poorly characterized ZBTB factor without a known thalamic-neuron role.  The
`Zbtb18` and `Zbtb38` responses show that the assay could detect a small
response from a ZBTB perturbation at similar matched perturbed-nucleus counts
when one existed.  `Zbtb7a` is a biologically useful counterexample rather than
a count template: in this dataset it produced an 841-DEG state, but it is a
well-studied, broadly active transcriptional repressor with a footprint very
unlike the quiescent ZBTB-family members.  There is no target-specific evidence
that acute `Zbtb42` loss should transfer the `Zbtb7a` state.

Looser C2H2 and chromatin-associated zinc-finger transcription factors were
also mixed but mostly small in this focal class.  `Zeb2` was 0; `Zfp148` was 8;
`Zeb1` was 15; `Zfp236` was 19; `Zmym2` was 22; `Zmynd8` was 74; and `Zfp423`
was 150.  These genes are less direct analogs than the ZBTB-family genes and
mainly show that zinc-finger or transcription-factor annotation alone does not
predict a large focal response.

## Target-specific decision

### `Zbtb42`

`Zbtb42` itself was completely held out, so the prediction rests on transfer.
The causal chain needed here is:

`Zbtb42` AAV-CRISPR loss in postmitotic thalamic glutamatergic nuclei ->
loss of a ZBTB42 molecular function in those nuclei -> altered transcriptional
or splicing regulation in a relevant neuronal pathway -> a survivor-state
expression shift large enough to yield BH-FDR-significant genes after
3-4 weeks -> observed focal `n_degs`.

The known biology supports the first two steps in skeletal muscle and
neuromuscular-junction biology but not in the focal neuronal context.  ZBTB42 is
nuclear and can be developmentally important, because human biallelic mutation
and zebrafish knockdown disrupt skeletal-muscle development, but the published
phenotype is contracture/myofibrillar rather than a thalamic glutamatergic
neuron transcriptional program.  In the training data, the ZBTB-family members
most analogous by domain membership had observed counts of 0, 0, 0, 0, 1, and
5, with no shared broad expression module.  Those are better comparators for
`Zbtb42` than the large `Zbtb7a` outlier or the broader `Zfp423`/`Zmynd8`
chromatin-associated responses, because they match the lack of a known
obligate pathway in these recovered postnatal neurons.

I therefore predicted a null measured footprint:

- predicted `n_degs`: **0**
- zero/nonzero call: **zero**
- evidence balance: primarily within-dataset zero/near-zero ZBTB-family
  training signatures, reinforced by external ZBTB42 literature pointing away
  from a strong postnatal thalamic-neuron program

## Limits

This is an extrapolation, not a directly observed `Zbtb42` count.  The published
ZBTB42 literature is sparse and focuses on muscle, ovary, neuromuscular
junctions, and early vertebrate development, so it cannot exclude a subtle
neuronal role.  The ZBTB-family comparisons are domain-level analogs rather
than paralogs in a shared obligate complex.  Acute mosaic AAV-CRISPR in
surviving P37-P44 nuclei can miss effects that would appear in embryonic or
muscle models, and a true one-gene response is difficult to distinguish from a
zero before seeing the held-out data.  Those uncertainties affect confidence,
but they do not overcome the strong local prior that an unvalidated ZBTB-family
perturbation in this focal cell group should have zero or only a near-zero
number of FDR-significant genes.
