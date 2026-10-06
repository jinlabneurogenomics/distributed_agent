# Prediction trace

## Question and resolved ambiguities

The manifest for this run contains one held-out perturbation:

```tsv
target_name
Edar
```

I interpreted the requested endpoint as the exact training-count endpoint:
the number of genes with Benjamini-Hochberg adjusted Wilcoxon `pvals_adj <
0.05` in the `151 TH Prkcd Grin2c Glut` cell group after acute, sparse
AAV-CRISPR loss of the held-out target. `Edar` itself is absent as a
perturbation target from both supplied training inputs, so the prediction has
to be transferred from non-held-out perturbations and from pathway knowledge.

I treated the count as an assay-specific integer breadth endpoint, not as a
continuous pathway-importance score. In particular, weak target-mRNA depletion
in this mosaic CRISPR setting was not used as evidence that editing failed.

## Sources used

Primary run data:

- `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
  for observed focal-cell `n_degs` in the 1,674 non-held-out training
  perturbations.
- `[local file: training_de_all_cell_groups.parquet]`
  for focal-cell adjusted p-values and signed log fold changes of biologically
  relevant comparator perturbations.
- `[local file: 065_Edar.csv]`
  for the requested held-out target list.

Internal same-experiment evidence:

- Distributed Agents corpus MCP release `perturbai-july-260713-sourceguard-1773-v1`,
  especially the `Eda` findings and the TNFR/TLR/TAK1/IKK/NF-kappaB claims.
  The corpus had no direct held-out `Edar` claim, but it did have a direct
  non-held-out `Eda` report.

External biological sources:

- Koppinen et al. 2001, DOI `10.1006/excr.2001.5331`, PMID `11570810`:
  EDAR is a TNF-receptor-superfamily receptor for ectodysplasin and activates
  NF-kappaB; EDAR variants associated with the downless phenotype reduce that
  activity.
- Schmidt-Ullrich et al. 2001, DOI `10.1242/dev.128.19.3843`, PMID
  `11585809`: NF-kappaB/Rel activity downstream of EDAR is required for hair
  follicles and other epidermal appendages.
- Mikkola and Thesleff 2003, DOI `10.1016/s1359-6101(03)00020-0`, PMID
  `12787560`: review of EDA-A1/EDAR signaling as an ectodermal-organ
  developmental pathway for hair, teeth, and exocrine glands.
- Morlon et al. 2005, DOI `10.1093/hmg/ddi405`, PMID `16251197`: EDARADD
  couples EDAR to TAB2, TRAF6, TAK1, and IKK/NF-kappaB activation.
- Fujikawa et al. 2012, DOI `10.1111/bjd.12018`, PMID `22924441`, and Yagi
  et al. 2022, DOI `10.1111/1346-8138.16610`, PMID `36258277`: pathogenic
  EDAR/TRAF6/EDARADD interactions affect EDARADD-mediated NF-kappaB signaling
  in hypohidrotic ectodermal dysplasia.
- Lefebvre et al. 2012, DOI `10.1038/jid.2011.453`, PMID `22277947`: in
  embryonic skin explants, Eda/NF-kappaB induces several Wnt, FGF, TGF-beta,
  TNF, EGF, and chemokine-pathway genes.

## Computational checks over the supplied data

I first read the focal training-count CSV and used it as the endpoint
calibration table. It contains 1,674 perturbations; 469 have `n_degs > 0`.
The distribution is very zero-inflated in this cell group:

```text
min = 0
25% = 0
median = 0
75% = 1
90% = 2
95% = 18
99% = 436.48
max = 2677
```

I then used parquet row-group metadata to avoid scanning the whole 616M-row DE
file and extracted `151 TH Prkcd Grin2c Glut` rows for EDA/EDAR, TNF/TLR,
TAK1/IKK/NF-kappaB, IL-17/FGF, BMP, and Wnt comparators. For each comparator I
recomputed the number of focal measured genes with `pvals_adj < 0.05` and
checked the minimum adjusted p-value and top-ranked rows. Each extracted
training comparator below had 17,259 measured genes in the focal cell group.

## Target-specific reasoning

### Edar

External function. `Edar` encodes the Eda-A1 receptor. The established EDAR
pathway is ligand-gated EDAR recruitment of EDARADD, TRAF6, TAB2/TAK1, and IKK,
followed by NF-kappaB activation in embryonic ectodermal placodes. Loss of this
pathway causes the hypohidrotic ectodermal dysplasia spectrum, with major
effects on hair, tooth, sweat-gland, and other epithelial appendage
morphogenesis. That biology makes a direct, basal, cell-autonomous
postmitotic-neuronal RNA response possible only if the `151 TH Prkcd Grin2c
Glut` cells have ongoing EDAR/NF-kappaB tone after P16; it is not the canonical
developmental context for the pathway.

Most relevant direct analog:

| training perturbation | focal `n_degs` | focal expression-pattern evidence | relationship to held-out `Edar` |
| --- | ---: | --- | --- |
| `Eda` | 0 | no adjusted hits; minimum focal q = 1.0 | the cognate ligand upstream of EDAR |

The direct ligand was therefore a strong zero analog. The raw focal `Eda`
signature also did not show near-threshold canonical EDAR-output genes:
`Edar`, `Edaradd`, `Dkk4`, `Lrp4`, `Shh`, `Ccnd1`, and `Cxcl10` were all in the
ranked focal gene universe for `Eda` perturbation and all had adjusted q = 1.0.
The same-experiment Distributed Agents `Eda` report extended that observation beyond
this one cell group: `Eda` produced no FDR<0.10 downstream genes in any of the
23 measured neuronal groups, and its closest whole-surface signature neighbors
were noise-level profiles with cosine magnitudes below 0.045. This argues that
there is no hidden EDA/EDAR module sitting just under the 0.05 threshold.

Downstream and adjacent NF-kappaB/TNF-family comparators:

| training perturbation | focal `n_degs` | focal minimum q | why compared |
| --- | ---: | ---: | --- |
| `Map3k7` | 0 | 1.0 | TAK1, immediately downstream of TRAF/TAB complexes including the EDARADD/TRAF6 route |
| `Chuk` | 0 | 0.727 | IKK-alpha, an IKK/NF-kappaB pathway kinase |
| `Nfkb1` | 0 | 1.0 | canonical NF-kappaB transcription-factor component |
| `Rel` | 0 | 0.140 | NF-kappaB-family transcription factor |
| `Traf3` | 0 | 1.0 | represented TRAF-family immune-receptor adaptor; not the EDAR-specific `Traf6`, but a TNFR/TLR-side counterexample |
| `Tnfrsf1a` | 0 | 1.0 | represented TNF receptor with NF-kappaB and MAPK outputs |
| `Tnfrsf11a` | 0 | 1.0 | TNFR-superfamily receptor that can signal through TRAF/NF-kappaB |
| `Tnfrsf13c` | 0 | 0.816 | TNFR-superfamily receptor |
| `Tnfrsf4` | 0 | 1.0 | TNFR-superfamily receptor |
| `Tnfrsf9` | 0 | 0.391 | TNFR-superfamily receptor |

These are not equivalent to knocking out `Edar`: `Traf6` and `Edaradd` were
not available as training targets, and `Map3k7`, `Chuk`, and `Nfkb1` integrate
many receptors other than EDAR. Still, their behavior is the relevant boundary
inside this particular neuronal assay. The Distributed Agents corpus summarized the
represented TNFR/TLR/IL-1/CD40-to-TAK1/IKK/NF-kappaB/JNK/p38 perturbations as
broadly transcriptionally silent as a basal module in unchallenged postnatal
NeuN-positive neurons, with flat or sparse TNFR-superfamily and TRAF3
comparisons rather than a shared immune-like module.

Other inflammatory receptor-side comparators were also flat in the focal
endpoint:

| training perturbations | focal `n_degs` |
| --- | ---: |
| `Tlr2`, `Tlr3`, `Tlr4`, `Tlr5`, `Tlr7`, `Tlr8` | all 0 |
| `Il17ra`, `Il17rd` | both 0 |
| `Fgf1`, `Fgfr1`, `Fgfr2`, `Fgfr3` | all 0 |
| `Acvr1`, `Bmpr1a`, `Bmpr1b`, `Bmpr2` | all 0 |

The IL-17/FGF/TLR data are mostly counterexamples rather than mechanistic
analogs, but they reinforce the same condition-specific point: ligand-gated
immune/developmental receptors tied to MAPK or NF-kappaB signaling were usually
quiescent in the unchallenged juvenile neuronal nuclei.

Positive counterexamples in the same focal group:

| training perturbation | focal `n_degs` | interpretation |
| --- | ---: | --- |
| `Ctnnb1` | 383 | direct beta-catenin perturbation is detectable in `151 TH Prkcd Grin2c Glut` |
| `Lrp6` | 4 | weak but nonzero thalamic Wnt/beta-catenin-related perturbation |

These prevent an over-broad conclusion that all developmental signaling is
unobservable in this cell type. The Distributed Agents corpus specifically reports that
the focal thalamic Wnt/beta-catenin response links `Lrp6` with `Ctnnb1/Tcf7l2`
and is not reproduced by `Eda`; therefore the Wnt hits are counterexamples to
generic pathway transfer, not evidence that held-out `Edar` should inherit the
large `Ctnnb1` count.

Zero/nonzero decision. I predict no focal genes will pass FDR 0.05 after
`Edar` perturbation. The exact ligand `Eda` is a corrected-DE null in the
focal group and across the neuronal surface; the available TAK1/IKK/NF-kappaB
and TNFRSF/TLR comparators are flat; and external literature places EDAR's
strong transcriptional role in embryonic epithelial appendage formation rather
than in basal P37/P44 postmitotic thalamic neurons. The most likely count is
therefore the same endpoint as `Eda`: 0.

## Limits and extrapolation

The decisive limitation is that `Edar` itself was held out and neither
`Edaradd` nor the most receptor-proximal EDA adaptor `Traf6` was available as a
training perturbation. The direct ligand `Eda` is close but not identical:
ligand loss cannot rule out ligand-independent receptor tone, receptor
functions mediated by another ligand, or a non-cell-autonomous role that the
neuronal nuclei screen would miss. The downstream genes that were present in
training are broad signaling hubs and can be buffered, redundant, or
post-translational in ways that differ from a receptor knockout. Finally, the
prediction is for acute sparse P16 AAV CRISPR in NeuN-enriched neurons; it does
not contradict germline or embryonic epithelial EDAR phenotypes, and it does
not address glial, skin, tooth, sweat-gland, or hair-follicle compartments.

## Final point prediction

`Edar`: **0** DEGs.
