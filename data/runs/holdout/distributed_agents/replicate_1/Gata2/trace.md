# DEG-count prediction trace

## Question

The requested target set contains exactly one held-out perturbation:
`Gata2`. I interpreted the endpoint as the number of measured genes passing
Benjamini-Hochberg-adjusted Wilcoxon `pvals_adj < 0.05` in the focal
`151 TH Prkcd Grin2c Glut` recovered-neuron contrast. Because `Gata2` was
held out, neither its focal DEG count nor any of its DE signatures are present
in the supplied inputs; the task is therefore a prediction by transfer from
non-held-out perturbations rather than a lookup.

## Sources

- Direct quantitative source: the supplied focal training counts,
  `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Direct expression source: the declared full differential-expression Parquet,
  `training_de_all_cell_groups.parquet`.
- Run-local metadata: `task_bindings.json`, `coverage.json`,
  `measurement_registry.json`, and the `perturbai-atlas-v5` dataset portrait.
- Same-experiment semantic source: the July
  `perturbai-july-260713-sourceguard-1773-v1` Finding/Evidence/Reference
  corpus and graph. This is a packaged interpretation of the same Perturb-seq
  experiment, not independent replication.
- External literature, queried through NCBI PubMed E-utilities: Virolainen et
  al. 2012, DOI `10.1242/dev.075192`; Achim et al. 2012, DOI
  `10.1242/dev.076380`; Lahti et al. 2015, DOI `10.1242/dev.129957`; Ling et
  al. 2004, DOI `10.1084/jem.20031556`; Tevosian et al. 1999, DOI
  `10.1073/pnas.96.3.950`; Lu et al. 1999, DOI `10.1128/MCB.19.6.4495`.

## Quantitative checks

The requested manifest has one unique row, `Gata2`, and it has no overlap with
the 1,674-row training-count CSV.

I first compared represented GATA-family and GATA-associated perturbations in
the focal training counts:

| training perturbation | focal `n_degs` |
|---|---:|
| `Gata1` | 0 |
| `Gata3` | 0 |
| `Gata4` | 0 |
| `Gata6` | 0 |
| `Zfpm2` | 0 |
| `Ets1` | 0 |
| `Klf1` | 0 |
| `Meis1` | 0 |
| `Meis2` | 0 |
| `Runx2` | 0 |
| `Runx3` | 0 |

I then read the raw Parquet for
`group_name == "151 TH Prkcd Grin2c Glut"` and the core GATA analogs to verify
that this was not a count-table artifact. The relevant predicate was:

```python
(pc.field("group_name") == "151 TH Prkcd Grin2c Glut") & pc.field("gene_target").isin(targets)
```

Each represented target had 17,259 measured-gene rows in the focal cell group.
`Gata1`, `Gata3`, `Gata4`, `Gata6`, and `Zfpm2` all had zero genes at
`pvals_adj < 0.05`. Matched perturbed nuclei were in the same range for these
comparators: `Gata1` 223, `Gata3` 220, `Gata4` 250, `Gata6` 330, and `Zfpm2`
180 nuclei versus 23,679 matched controls. `Gata3` was the closest to a focal
signal, but its two smallest adjusted p-values, `Cttn` and `Hagh`, were only
`0.159`. A broader all-cell scan of these five target genes found only a single
FDR<0.05 gene total, caused by `Gata6` in `059 CNU-LGE LSX GABA`, and no
significant hit for `Gata1`, `Gata3`, `Gata4`, or `Zfpm2` in any measured cell
group.

The same-experiment July corpus was also consistent with this null GATA
surface: `Gata1:F001` summarized `Gata1` as a complete neuronal DE null across
all 23 measured cell groups, and `Gata1:E008` noted that represented
GATA-family and hematopoietic-circuit perturbations were flat or limited to
isolated one-gene hits in this neuronal dataset. This was used only as compact
interpretation of the same data, not as independent evidence.

## Target-specific reasoning

### `Gata2`

`Gata2` encodes a zinc-finger GATA transcription factor. The strongest external
functions for `Gata2` are outside the assayed postnatal neuronal compartment:
for example, Ling et al. 2004 showed a gene-dose requirement in definitive
hematopoietic stem-cell generation and expansion. Those blood and endothelial
programs are not expected to be active in the NeuN-enriched whole-brain
neuronal nuclei used here.

The neural literature gives a more relevant but still developmental role:
Virolainen et al. 2012 showed that `Gata2` acts in postmitotic GABAergic
precursors of embryonic diencephalon, promoting GABAergic identity and
repressing glutamatergic differentiation in pretectum and specifying a rostral
thalamic GABAergic subtype. Achim et al. 2012 and Lahti et al. 2015 likewise
place `Gata2` with `Gata3` and `Tal1` in embryonic GABAergic precursor fate
choice in ventral rhombomere 1. That causal stage is not the requested
intervention stage: the Perturb-seq edit is delivered postnatally at P16,
3-4 weeks before a snRNA-seq readout in surviving glutamatergic thalamic
neurons.

The most appropriate within-dataset analog is `Gata3`, because external neural
work places `Gata3` beside `Gata2` in the embryonic GATA/TAL1 GABAergic program
and in inhibitory-vs-excitatory fate specification. `Gata3` knockout produced
`n_degs = 0` in the focal class; the smallest focal adjusted p-value was 0.159.
That is a direct negative analog for postnatal neurons: if the represented
neural GATA partner did not elicit a detectable focal footprint, an acute
`Gata2` perturbation of the same broad family is unlikely to cause a broad
`151 TH Prkcd Grin2c Glut` signature.

`Gata1`, `Gata4`, and `Gata6` are weaker biological analogs because their best
known lineage programs are erythroid/megakaryocytic or cardiac/endodermal, not
thalamic neuronal. Their focal DEG counts were nevertheless useful as
counterexamples to a simple "GATA-factor knockout must be broad" expectation:
all three had `n_degs = 0`. `Zfpm2`/FOG2 physically interacts with GATA factors
and is brain enriched in the mouse according to Tevosian et al. 1999 and Lu et
al. 1999, so its `n_degs = 0` in the focal class further argues that this
neuronal assay did not contain a responsive mature GATA/FOG transcriptional
circuit.

The zero/nonzero call is therefore driven primarily by the within-dataset null
GATA-family response, with external developmental biology used to choose
`Gata3` as the closest comparator and to downgrade embryonic GABAergic fate
evidence for a postnatal glutamatergic endpoint. I predict no genes will pass
the stringent focal FDR threshold for `Gata2`, so the point estimate is
`0`.

## Limits

This is a single-gene extrapolation. `Gata2` itself was absent as a
`gene_target`, and `Tal1` and `Zfpm1` were also absent from the training
perturbation set, so the exact embryonic `Gata2`-`Tal1`-`Gata3` module could
not be fully tested. The GATA homologs are lineage-biased transcription
factors rather than obligate subunits of one complex, so their null responses
are analogs and counterexamples, not guaranteed same-outcome causal transfers.
The external neural studies mostly concern embryonic fate specification in
GABAergic precursors, whereas this assay perturbed P16 postmitotic neurons and
measured recovered nuclei. A quiet signature is consequently best interpreted
as "unlikely to produce a detectable broad recovered-cell transcriptional
response in this endpoint", not as proof that `Gata2` has no developmental or
non-neuronal function.
