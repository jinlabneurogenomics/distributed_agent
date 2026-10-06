# Tbk1 direct n_degs forecast

## Target and endpoint

- Target manifest: `Tbk1`.
- Cell population: `151 TH Prkcd Grin2c Glut`.
- Endpoint: count of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`.
- Point forecast: `1`.

## Evidence used

### Outcome scale in the declared training table

The declared 151 count table contains 1,674 training perturbations. Counts were
sparse: 1,205/1,674 were 0, the median was 0, the 90th percentile was 2, the
95th percentile was 18, and the maximum was 2,677. This makes a zero or
single-digit response the default scale unless the target's biology matches one
of the rare broad stress programs.

### Tbk1 biology-only bundle

The declared biology bundle shows that `Tbk1` itself is reachable in the exact
assay population: 19,805 of 23,679 non-target nuclei expressed `Tbk1`
(`83.64%`; mean raw UMI 2.50; mean CP10k 1.53).

The same bundle adjudicates TBK1 as a renewable diffusible kinase whose
functional stock is likely substantially depleted by the P37-P44 harvest after
a P16 disruptive edit. That argues against treating the perturbation as an
unexpressed or development-only null. The bundle also keeps the support partial:
matched thalamic-neuron timing was not available, direct TBK1 neuronal turnover
was not found, and IKKepsilon/`Ikbke` compensation was unresolved in neurons.

### Matched training perturbations

The closest 151 training counts available for the TLR/TNFR-to-TBK1/NF-kB/IRF
lane were flat:

| Perturbation | 151 `n_degs` |
|---|---:|
| `Traf3` | 0 |
| `Map3k7` | 0 |
| `Chuk` | 0 |
| `Nfkb1` | 0 |
| `Rel` | 0 |
| `Tlr2` | 0 |
| `Tlr3` | 0 |
| `Tlr4` | 0 |
| `Tnfrsf1a` | 0 |
| `Tnfrsf13c` | 0 |

Core and receptor-adjacent autophagy comparators were also quiet in this same
endpoint:

| Perturbation | 151 `n_degs` |
|---|---:|
| `Atg5` | 0 |
| `Atg16l1` | 0 |
| `Becn1` | 0 |
| `Sqstm1` | 1 |
| `Rb1cc1` | 4 |

ALS/endolysosomal comparators supplied upper-bound context rather than a direct
point scale. `Grn` had 1, `Vcp` had 2, `Vps35` had 17, while broader trafficking
or RNA/proteostasis perturbations could be much larger (`Vps54` 31, `Tardbp`
210, `Rab7` 501). Those larger donors were interpreted as severe boundary
states, because core RNA metabolism or late endosomal machinery loss is broader
than TBK1's kinase/adaptor role.

For the 18 direct NF-kB/IRF/autophagy/endolysosomal counts from `Traf3` through
`Vps35` listed above, the median was 0 and the log1p center was
`expm1(mean(log1p(n_degs))) = 0.47`. That local quantitative scale supports a
near-zero integer even after allowing a small upward adjustment for high
`Tbk1` expression.

### Same-experiment corpus interpretation of training genes

Same-experiment reports for the training perturbations agreed with the count
table rather than supplying independent replication:

- `Traf3` was pan-neuronally flat and did not induce the expected interferon,
  NF-kB/MAPK, oxidative-stress, or apoptosis sentinel transcripts. Its report
  also grouped represented TNFR/TLR/NF-kB relatives as mostly silent in
  unchallenged NeuN-positive neurons.
- `Sqstm1` had a sparse surface: only one FDR feature in the target 151
  population and no robust NRF2/redox, lysosomal-autophagy, proteasome, UPR, or
  ISR RNA program.

The report-derived topology over selected comparator genes separated two
relevant connected subsets: `Chuk`/`Map3k7`/`Nfkb1`/`Traf3` for basal NF-kB and
`Atg16l1`/`Atg5`/`Becn1`/`Rb1cc1`/`Sqstm1` for autophagy. Both subsets were
biologically close enough to inform scale, and both remained near zero in 151.

### Declared Parquet profile comparison

I compared the 151 expression profiles for 14 selected training perturbations
from the declared Parquet: `Traf3`, `Chuk`, `Nfkb1`, `Irf3`, `Atg5`,
`Atg16l1`, `Becn1`, `Sqstm1`, `Rb1cc1`, `Vcp`, `Grn`, `Vps35`, `Usp48`, and
`Tardbp`. All profiles were available. The selected cohort contained 7 targets
with no significant features, 4 with 1-9 features, 2 with 10-49 features, and
only `Tardbp` with at least 50 features. The five focal nodes nearest to TBK1's
operation in the profile inspection were:

| Perturbation | significant features in 151 |
|---|---:|
| `Traf3` | 0 |
| `Sqstm1` | 1 |
| `Rb1cc1` | 4 |
| `Vcp` | 2 |
| `Vps35` | 17 |

This supported using `Tardbp` and severe trafficking hits as upper bounds, not
as point analogues.

## Synthesis

The TBK1 edit is likely realized and the target is expressed in the focal
population, so a strict structural-zero forecast would be too low. But TBK1's
transcriptionally loud contexts in the biology bundle are stimulated immune or
nonmatched neural contexts, while the assay is unchallenged, juvenile,
NeuN-positive, and survivor-conditioned. The directly measured basal
NF-kB/IRF/TLR axis and the nearest measured autophagy receptor/core genes are
overwhelmingly null in the exact endpoint. A sparse one-gene event like
`Sqstm1` is therefore the most defensible integer scale: it preserves a small
penalty for `Tbk1` reach and kinase-stock realization without transferring the
much larger broad endolysosomal or RNA-binding programs.

No `Tbk1` expression signature or held-out `Tbk1` DEG count was used.
