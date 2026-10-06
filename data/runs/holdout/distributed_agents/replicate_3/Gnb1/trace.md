# DEG-count prediction trace

## Question and resolved ambiguity

The manifest `093_Gnb1.csv` requests one held-out perturbation, `Gnb1`.
I interpreted the endpoint as the total number of measured genes with
Benjamini-Hochberg adjusted Wilcoxon `pvals_adj < 0.05` in `151 TH Prkcd
Grin2c Glut` for that perturbation.

One important ambiguity is whether the count includes the target transcript
itself. The training table is consistent with inclusion: in the focal raw DE
rows, `Gnao1`, `Gabbr1`, `Gabbr2`, `Gpr158`, `Grm7`, and `Prkaca` each have
exactly one FDR < 0.05 row and that row is the knocked-out gene itself. I
therefore predicted total counted rows, not downstream-only rows.

## Sources used

- `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`:
  the task-matched training endpoint for 1,674 non-held-out perturbations.
- `[local file: training_de_all_cell_groups.parquet]`:
  raw per-gene DE statistics. I queried the exact focal group for mechanistic
  analogs and counted which rows were FDR-significant.
- Distributed Agents same-experiment corpus
  `perturbai-july-260713-sourceguard-1773-v1`: I used `target_context` for
  `Gnb5`, `Gnao1`, `Gnas`, `Gnal`, and `Gabbr1`, plus
  `expand_candidate_set` and `candidate_set_topology` over their explicitly
  referenced GPCR/G-protein/cAMP neighbors. `target_context("Gnb1")` returned
  no entries, as expected for this held-out target.
- Distributed Agents runtime profile comparison over focal log fold changes for
  `Gnb5`, `Gnao1`, `Gnas`, `Gnal`, `Adcy1`, `Adcy3`, `Adcy5`, `Gabbr1`,
  `Gabbr2`, `Gpr158`, `Gpr179`, `Grm7`, `Rgs6`, `Kcnj6`, `Pde10a`, and
  `Prkaca`.
- PubMed literature for external mechanism:
  Petrovski et al. 2016, DOI `10.1016/j.ajhg.2016.03.011`, PMID `27108799`;
  Lohmann et al. 2017, DOI `10.1093/hmg/ddx018`, PMID `28087732`;
  Reddy et al. 2021, DOI `10.1016/j.isci.2021.103018`, PMID `34522861`;
  Colombo et al. 2023, DOI `10.3389/fncel.2023.1175895`, PMID `37275776`;
  Muntean et al. 2021, DOI `10.1016/j.celrep.2021.108718`,
  PMID `33535037`; Panicker et al. 2010,
  DOI `10.1111/j.1471-4159.2010.06616.x`, PMID `20100282`.

## Computations over the supplied DE data

The focal endpoint is sparse: among the 1,674 training targets, 1,205 had
`n_degs = 0`, 363 had 1-9, 63 had 10-99, and 43 had at least 100.

To verify task-matched G-protein analogs, I selected focal rows for a curated
set of represented proximal GPCR/G-protein/cAMP genes and counted rows with
`pvals_adj < 0.05`:

```python
f = (
    (pc.field("group_name") == "151 TH Prkcd Grin2c Glut")
    & pc.field("gene_target").isin(nodes)
    & (pc.field("pvals_adj") < 0.05)
)
```

The significant focal rows for the 16-node GPCR/G-protein comparison set were
all self decreases:

| target | focal `n_degs` | focal FDR < 0.05 rows in the candidate query |
| --- | ---: | --- |
| `Gnb5` | 0 | none |
| `Gnao1` | 1 | `Gnao1` logFC -0.591 |
| `Gnas` | 0 | none |
| `Gnal` | 0 | none |
| `Adcy1` | 0 | none |
| `Adcy3` | 0 | none |
| `Adcy5` | 0 | none |
| `Gabbr1` | 1 | `Gabbr1` logFC -0.602 |
| `Gabbr2` | 1 | `Gabbr2` logFC -0.926 |
| `Gpr158` | 1 | `Gpr158` logFC -0.991 |
| `Gpr179` | 0 | none |
| `Grm7` | 1 | `Grm7` logFC -0.364 |
| `Rgs6` | 0 | none |
| `Kcnj6` | 0 | none |
| `Pde10a` | 0 | none |
| `Prkaca` | 1 | `Prkaca` logFC -0.940 |

The Distributed Agents profile comparison on the same focal logFC vectors found 10 of
16 represented signaling nodes with no FDR < 0.05 feature and 6 with only 1-9
features; among the core comparisons I inspected, the significant-feature
intersections were zero because these singletons were different self-target
rows.

Separately, I scanned the focal parquet for rows with `names == gene_target`.
There were 1,642 self rows among the 1,674 focal training targets, and only 319
were FDR-significant. Thus a counted self transcript is common but not
guaranteed; it has to be predicted target by target.

## Target-specific reasoning

### `Gnb1`

`GNB1` encodes the conventional G protein beta-1 subunit of heterotrimeric
G proteins. Human de novo `GNB1` variants cause neurodevelopmental disability,
hypotonia, seizures, and movement phenotypes, and functional assays show that
pathogenic variants can disrupt G-protein heterotrimer assembly or alter
Gbetagamma effector signaling (Petrovski 2016; Lohmann 2017). More recent
mechanistic work ties encephalopathy alleles particularly to GIRK-channel
regulation and Gnb1 mutant mouse seizure phenotypes (Reddy 2021; Colombo
2023). These facts make `Gnb1` biologically real in neurons, but they point
mostly to membrane and circuit physiology rather than to a direct
transcription-factor-like nuclear program.

The most direct represented beta-subunit comparator was `Gnb5`, which is an
imperfect analog: Gbeta5 is the most divergent beta subunit and forms a
specialized complex with R7-family RGS proteins rather than behaving like a
generic Gbeta1 replacement (Panicker 2010). Still, its same-experiment result
is informative as a negative boundary. In the focal 151 group `Gnb5` had
`n_degs = 0`, and the Distributed Agents corpus reports no robust downstream Gnb5
transcriptional response in any measured neuronal group; `Rgs6`, `Gpr158`,
`Gpr179`, `Gnao1`, and `Kcnj6` were likewise flat or near-flat in Gnb5/R7
context. This supports a low downstream count for a beta/gamma signaling node
under basal 3-4 week snRNA-seq.

`Gnao1` is another useful proximal comparator because Galpha-o is abundant in
neurons and modulates striatal GPCR/cAMP signaling (Muntean 2021). In the
focal endpoint it had `n_degs = 1`, solely its own mRNA row, and the corpus
summarizes `Gnao1` as transcriptionally buffered in 21 of 22 measured groups,
with only a one-gene `Puf60` response outside the focal thalamic group. The
represented source-arm cAMP nodes were similarly quiet in 151 cells:
`Gnas = 0`, `Gnal = 0`, `Adcy1 = 0`, `Adcy3 = 0`, `Adcy5 = 0`,
`Pde10a = 0`, and `Pde4b = 0`. Corpus expansion from `Gnb5`, `Gnao1`, `Gnas`,
`Gnal`, and `Gabbr1` recovered exactly these expected cAMP/GIRK/GABA_B
neighbors; their observed counts keep the whole module in the 0-1 focal band
rather than nominating a hidden multi-gene state.

The focal GABA_B receptor perturbations are a counterexample to the idea that
knocking out every Gbetagamma-coupled receptor or channel node gives the same
RNA output. `Gabbr1` and `Gabbr2` each had `n_degs = 1` in the focal group,
but those were self-transcript decreases, not a shared downstream signature.
The Distributed Agents `Gabbr1:F003` and `Gabbr2:F002` findings explicitly contrast
the obligate GABA_B partner, `Gnao1`, `Kcnj6`, calcium-channel, `Adcy1`, and
`Adcy5` perturbations and report no common directional transcriptome. That is
mechanistically close to Gbetagamma/GIRK signaling, and it again argues against
a broad secondary `Gnb1` signature.

Putting those together, the within-dataset evidence is strong for
downstream transcriptional buffering of basal GPCR/G-protein perturbations in
this readout. I therefore predict no non-self Gnb1-regulated genes will pass
FDR < 0.05 in `151 TH Prkcd Grin2c Glut`. I nevertheless choose a nonzero
total count of 1 because `Gnb1` itself should be a well-expressed, directly
edited conventional G-protein transcript in thalamic glutamatergic neurons,
whereas several comparably proximal and expressed focal analogs had exactly
one self row. This is more likely than a strict zero for a core G-protein beta
subunit, but far below a medium or strong response.

Candidate dispositions:

| perturbation | observed focal `n_degs` | use for `Gnb1` |
| --- | ---: | --- |
| `Gnb5` | 0 | kept as the represented beta/RGS boundary, but imperfect because Gbeta5 is R7-specialized |
| `Gnao1` | 1 | kept as a proximal neuronal Galpha comparator; its focal singleton is self-only |
| `Gnas` | 0 | kept as a classical G-protein/cAMP counterexample |
| `Gnal` | 0 | kept as striatal/olfactory Galphaolf cAMP counterexample |
| `Adcy1`, `Adcy3`, `Adcy5` | 0, 0, 0 | kept as cAMP source-arm counterexamples |
| `Gabbr1`, `Gabbr2` | 1, 1 | kept as Gbetagamma/GIRK-coupled receptor counterexamples; focal singletons are self-only |
| `Rgs6`, `Kcnj6`, `Gpr158`, `Gpr179`, `Grm7` | 0, 0, 1, 0, 1 | kept as Gbeta5/R7, GIRK, and GPCR-adjacent boundaries |
| `Pde10a`, `Pde4b`, `Prkaca` | 0, 0, 1 | kept as downstream cAMP/PKA boundaries; none supports a multi-gene 151 response |
| `Crebbp`, `Psmc1` | 1, 430 | rejected as quantitative analogs; corpus recovers them as mechanistic contrasts rather than G-protein phenocopies |

## Limits

- `Gnb1` was held out completely, so no Gnb1 expression signature or count was
  available from the supplied inputs. The exact on-target FDR call is an
  extrapolation from target identity and from analog self rows.
- The best conventional beta-subunit paralog, `Gnb2`, was not present in the
  focal training table; the assayed `Gnb5` is R7-RGS specialized and therefore
  a boundary, not a one-to-one paralog.
- Many missing close components, including `Gnai1/2/3`, `Gng` partners,
  `Rgs7`, `Rgs9`, and `Rgs11`, prevent a complete same-complex transfer.
- Germline and missense `GNB1` disease mechanisms include development,
  dominant/gain-of-function effects, GIRK gating, sodium-channel effects, and
  thalamocortical circuit physiology. These are not the same as sparse P16
  CRISPR loss-of-function in recovered P37-44 nuclei.
- The profile comparison shows no FDR-supported shared GPCR/G-protein module,
  but the whole-profile correlations among flat signatures are not themselves
  positive biological evidence; they were used only after checking FDR-level
  rows and same-experiment corpus interpretations.

## Prediction

| target | predicted `n_degs` |
| --- | ---: |
| `Gnb1` | 1 |
