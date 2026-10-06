# Drd3 n_degs forecast

## Target and endpoint

- Target: `Drd3`
- Cell group: `151 TH Prkcd Grin2c Glut`
- Endpoint: number of measured genes with Wilcoxon `pvals_adj < 0.05`
- Forecast: `0`

The declared training table contains 1,674 non-`Drd3` targets for this focal
cell group; `Drd3` is absent from that count table as intended.

## Evidence used

### Focal Drd3 reach and biology

The canonical `Drd3` biology bundle reports direct in-assay focal expression,
but it is sparse in the matched non-target nuclei:

- mean CP10K: `0.04791854418871145`
- pseudobulk CPM: `4.989215526109455`
- expressing nuclei: `961 / 23679`, or `4.058448414206681%`

The same bundle characterizes DRD3 as a Gi/Go-coupled dopamine GPCR at the
plasma membrane and dopaminergic synapses. Adult germline `Drd3` mutants have
neural behavioral phenotypes, so the target is not biologically inert. For this
P16-to-P37/P44 assay, though, the evidence is only partially matched: the loss
phenotypes are lifelong/systemic, the thalamic expression is low and regionally
restricted, DRD2-related buffering is unresolved, and the amount of installed
DRD3 receptor remaining 21 to 28 days after editing is indeterminate.

### Training count distribution

The focal-group training counts are dominated by zero or near-zero outcomes:

- `1205 / 1674` training targets had `n_degs = 0`
- `1481 / 1674` had `n_degs <= 1`
- `1546 / 1674` had `n_degs <= 5`
- median `n_degs` was `0`

This creates a strong base rate for zero unless a target has evidence for a
direct, high-penetrance, cell-autonomous transcriptional program in this
thalamic aggregate.

### Same-endpoint receptor and cAMP/Gi/o comparators

The closest represented dopamine receptors were flat in the declared count
table for `151 TH Prkcd Grin2c Glut`:

| target | n_degs |
|---|---:|
| `Drd2` | 0 |
| `Drd4` | 0 |
| `Drd5` | 0 |

I also checked the declared expression Parquet for a broader mechanistic panel:

`Drd2`, `Drd4`, `Drd5`, `Adcy3`, `Adcy5`, `Gnal`, `Gnao1`, `Gnas`, `Npsr1`,
`Pde1c`, `Pde10a`, `Pde4b`, `Chrm2`, `Oprd1`, `Oprk1`, `Oprl1`, `Oprm1`

Across those 17 receptor, dopamine/cAMP, and Gi/o-linked perturbations in the
focal group, the Parquet contained only one FDR-significant row: the `Gnao1`
self transcript. All other members of the panel had zero significant rows in
the focal group, and the matched perturbation counts for this panel were in the
same few-hundred-nucleus range used across the training screen.

### Same-experiment corpus boundaries

The same-experiment corpus has no `Drd3` target report in the selected release,
so no held-out `Drd3` signature was used. I used three higher-order corpus
statements only as interpretation of the represented training perturbations:

- represented dopamine/GPCR and cAMP-pathway perturbations did not collapse
  into one shared durable basal neuronal mRNA module;
- represented dopamine receptors did not transcriptionally phenocopy
  represented G-protein, cyclase, phosphodiesterase, PKA, or CREB-axis
  perturbations; and
- represented Gi/o opioid receptor paralogs were broadly buffered at the basal
  neuronal nuclear RNA level.

These are packaged readings of the same experiment, not independent
replication, but they are useful guardrails against projecting an acute
second-messenger GPCR pathway into a broad chronic snRNA-seq response.

## Synthesis

`Drd3` could matter physiologically in a small anterior-thalamic receptor pool,
but the exact focal expression reach is only about four percent of non-target
nuclei, functional receptor depletion by harvest is uncertain, and the most
direct represented dopamine-receptor analogs are all `0` in this exact cell
group. The broader GPCR/cAMP/Gi/o panel is also essentially flat in the same
endpoint, while the count-table prior has a large atom at zero.

I therefore round the expected response down to the endpoint mode rather than
assigning a small positive count.
