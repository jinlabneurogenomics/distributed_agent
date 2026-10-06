# Prediction trace

## Question and resolved ambiguities

The held-out manifest for this run contains one requested perturbation:

```text
Sry
```

I interpreted the required endpoint as the focal-cell scalar in the prompt:
`n_degs`, the number of measured genes in `151 TH Prkcd Grin2c Glut` nuclei
with Benjamini-Hochberg adjusted Wilcoxon `pvals_adj < 0.05`, after acute
P16 AAV-PHP.eB CRISPR loss of the requested target and P37-P44 snRNA-seq.

The focal Allen label needs one disambiguation for this gene: in
`151 TH Prkcd Grin2c Glut`, `TH` is the atlas abbreviation for thalamus, not
the gene `Th` or tyrosine hydroxylase. The assayed cells are thalamic
glutamatergic neurons marked by `Prkcd` and `Grin2c`; dopaminergic classes are
marked separately as `Dopa` in this dataset vocabulary.

## Sources used

- Differential-expression parquet:
  `[local file: training_de_all_cell_groups.parquet]`
- Focal-cell training DEG counts:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- Requested-target manifest:
  `[local file: 224_Sry.csv]`
- Internal same-experiment corpus:
  Distributed Agents corpus `perturbai-july-260713-sourceguard-1773-v1`
- Run-local profile comparisons over the focal DE signatures, using
  `logfoldchanges` as the signed vector and `pvals_adj < 0.05` as the
  significant-feature threshold
- External literature for `Sry` function:
  Sekido et al. 2004, DOI 10.1016/j.ydbio.2004.07.011; Sekido 2009,
  DOI 10.1016/j.biocel.2009.12.005; Kashimada and Koopman 2010,
  DOI 10.1242/dev.048983; Mayer et al. 2000, DOI 10.1007/s100480000093;
  Milsted et al. 2004, DOI 10.1016/j.neulet.2004.07.052; Dewing et al. 2006,
  DOI 10.1016/j.cub.2006.01.017.

## Dataset calibration

The focal training table has 1,674 non-held-out perturbations. It is highly
zero-inflated:

- 1,205 of 1,674 perturbations, 72.0%, have `n_degs = 0`.
- 1,512 of 1,674 perturbations, 90.3%, have `n_degs <= 2`.
- The median is 0, the 75th percentile is 1, the 90th percentile is 2, and only
  a small tail of essential RNA-processing, proteasome, and transcriptional
  perturbations reaches hundreds to thousands of DEGs.

I then selected mechanistic neighbors of `Sry` that were actually present in
the training table and inspected both their focal DEG counts and their focal
log-fold-change signatures.

Represented direct or near-direct developmental sex-determination comparators
were all null in the focal group:

| comparator | relationship to Sry biology | 151 TH Prkcd Grin2c Glut n_degs |
|---|---|---:|
| `Sox9` | direct SRY-induced Sertoli/testis effector and HMG-box SOX factor | 0 |
| `Wt1` | gonadal ridge regulator upstream of the Sry/Sox9 axis | 0 |
| `Nr5a1` | SF1 cofactor that cooperates with SRY on Sox9 testis enhancer | 0 |
| `Nr5a2` | NR5A paralog | 0 |
| `Gata4`, `Gata6` | gonadal/endocrine developmental GATA-family comparators | 0 |
| `Foxl2`, `Foxl1` | ovarian/cell-fate counterpathway and FOX comparator | 0 |

Many textbook nodes in the SRY-SOX9 gonadal network, including `Cbx2`,
`Dmrt1`, `Fgf9`, `Wnt4`, `Rspo1`, `Amh`, and `Nr0b1`, were not in the focal
training count table. Other mouse Y-linked genes such as `Ddx3y`, `Eif2s3y`,
`Kdm5d`, `Uty`, `Usp9y`, `Zfy1`, and `Zfy2` were absent as perturbation targets
too, so there was no within-dataset Y-chromosome panel to use.

The represented SOX/HMG family also argues against a generic SOX-like
thalamic response:

| comparator | focal n_degs | focal significant genes |
|---|---:|---|
| `Sox2` | 2 | `Tnnt1` down, `Stam` down |
| `Sox4` | 0 | none |
| `Sox5` | 2 | `Dgkh` up, `Tnnt1` up |
| `Sox9` | 0 | none |
| `Sox10` | 0 | none |
| `Sox11` | 0 | none |
| `Sox17` | 0 | none |
| `Sox18` | 0 | none |

For the mechanistically closest inspected set, `Sox9`, `Sox2`, `Sox5`, `Wt1`,
and `Nr5a1`, the profile comparison reported no FDR-significant genes for
`Sox9`, `Wt1`, or `Nr5a1`, and only two each for `Sox2` and `Sox5`.
`Sox9` had zero significant-feature intersections with `Sox2`, `Sox5`, and the
other SOX/gonadal peers. The top-50 signed-tail overlap between `Sox9` and each
of the SOX or gonadal peers was also tiny, with only 1 to 5 shared top-tail
features out of unions of 95 to 99 in most inspected pairs. This was useful as
a rejection test: the near-null SOX/gonadal surfaces are not hiding an obvious
coordinated subthreshold signature.

The same-experiment Distributed Agents corpus did not contain a direct `Sry` target
record. It did, however, agree with the raw focal evidence around the measured
analogs:

- `Sox9` findings in `perturbai-july-260713-sourceguard-1773-v1` summarize
  Sox9 loss as essentially silent in the NeuN-enriched postmitotic neuronal
  screen, with no convincing SOX/NFI/Notch-STAT/BMP phenocopy among measured
  comparators.
- `Sox2`/`Sox5` findings support that the tiny thalamic `Tnnt1` effects are
  target-specific and even sign-discordant rather than a generic SOX or
  HMG-box response.
- `Wt1` findings report that Wt1 was a uniform postnatal neuronal
  non-responder at FDR<0.10 across 22 measured cell groups and had no hidden
  convergent module among data-driven or WT1 literature comparators.

## Target-specific reasoning

### Sry

External biological role:

`Sry` is a Y-linked HMG-box transcription factor. Its canonical role is a
brief embryonic action in Sertoli-cell precursors: SRY directly turns on the
testis pathway by activating `Sox9`, with `Sox9` then reinforcing Sertoli-cell
differentiation and testis morphogenesis. This places `Sox9`, `Wt1`, `Nr5a1`,
`Gata4`, and male/female gonadal fate genes as the natural literature-derived
comparison class for `Sry`, but that network is an embryonic gonadal ridge
program, not an acute postmitotic thalamic neuronal program.

There is credible adult brain expression and function for `Sry`, so I did not
treat `Sry` as automatically irrelevant just because it is famous for testis
determination. Mayer et al. detected postnatal, linear `Sry` transcripts in
male mouse diencephalon, midbrain, and cortex by RT-PCR. Milsted et al. showed
that rat Sry can activate the tyrosine-hydroxylase promoter in a PC12 reporter
system, and Dewing et al. found SRY in adult male substantia nigra
tyrosine-hydroxylase-positive neurons, where antisense Sry down-regulated `Th`
and caused motor deficits.

Why the measured analogs point to zero here:

The closest represented gonadal effector, `Sox9`, had `n_degs = 0` in the
focal thalamic group. Its corpus-level same-experiment interpretation is a
near-null postmitotic neuronal perturbation, not a broad glial, gonadal, or
SOX-family neuronal signature. Upstream or cooperating gonadal regulators
available in the table were also null in the same focal group: `Wt1`, `Nr5a1`,
`Nr5a2`, `Gata4`, `Gata6`, and `Foxl2` all had 0 DEGs. Among the assayed SOX
family, the only nonzero examples were tiny two-gene `Sox2` and `Sox5`
responses, and those were not interchangeable: they moved `Tnnt1` in opposite
directions, with `Sox2` additionally lowering `Stam` and `Sox5` additionally
raising `Dgkh`. That pattern is a counterexample to using HMG-box family
membership to predict a shared `Sry` response.

I therefore predict that acute `Sry` CRISPR in `151 TH Prkcd Grin2c Glut`
will be below the focal assay's detection threshold. Even if `Sry` is expressed
in a subset of male diencephalic neurons, the perturbation is delivered and
counted in a mixed-sex screen, so XX nuclei assigned to an `Sry` guide have no
Y-linked `Sry` locus to edit. The best-supported neural `Sry` effect in the
literature is in male nigral dopamine neurons through `Th`, whereas this focal
cluster is thalamic and glutamatergic. Combining that cell-context mismatch
with the flat measured `Sox9`/gonadal comparator panel makes the expected FDR
burden indistinguishable from the null bulk of the training distribution.

Prediction: `0` DEGs.

## Limits

- There was no direct `Sry` expression signature in the input parquet or
  target record in the Distributed Agents corpus, by construction and by retrieval.
  The estimate is extrapolated from `Sry` biology and from represented SOX and
  gonadal regulators.
- The training universe lacked several key SRY-pathway genes, including
  `Cbx2`, `Dmrt1`, `Fgf9`, `Wnt4`, `Rspo1`, `Amh`, and `Nr0b1`, and lacked
  other Y-linked perturbation targets, so I could not validate a complete
  sex-determination or Y-chromosome module inside the same experiment.
- Bulk RT-PCR evidence for postnatal `Sry` in diencephalon does not resolve
  whether the `151 TH Prkcd Grin2c Glut` subtype expresses translatable Sry.
  Conversely, the nigral dopamine literature proves a possible adult neural
  role but not a thalamic glutamatergic one.
- The screen is sparse, mosaic, mixed-sex, survivor-conditioned, and uses a
  nuclear RNA Wilcoxon endpoint. A prediction of `0` DEGs means no measured
  gene is expected to pass BH FDR 0.05 in this assay; it does not claim that
  `Sry` has no molecular function anywhere in male brain.
