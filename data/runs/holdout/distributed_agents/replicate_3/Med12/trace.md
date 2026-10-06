# DEG-count prediction trace

## Question and resolved ambiguities

The requested held-out target is the single gene in
`136_Med12.csv`:

```tsv
target_name
Med12
```

I interpreted the endpoint as the exact focal-cell count used in the training
CSV: the number of measured genes with `pvals_adj < 0.05` in
`151 TH Prkcd Grin2c Glut` after acute AAV-CRISPR loss of the named mouse
target. `Med12` itself is absent from both the training DEG-count CSV and the DE
parquet, so the prediction has to be transferred from other perturbations. The
key ambiguity was whether to treat `Med12` as a broad Wnt/Mediator transcription
factor dependency or as a narrow postmitotic Mediator kinase-module
perturbation. I used the directly measured Mediator-family behavior in this
dataset to resolve that toward a small, nonzero thalamic response rather than a
global transcriptional collapse.

## Sources used

- Input focal training endpoint:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Input per-gene DE parquet:
  `[local file: training_de_all_cell_groups.parquet]`.
- Requested-target manifest:
  `[local file: 136_Med12.csv]`.
- Same-experiment internal corpus: Distributed Agents corpus release
  `perturbai-july-260713-sourceguard-1773-v1`; I queried frozen claims and
  target contexts for `Med13`, `Med15`, `Med23`, `Med13l`, and `Cdk8`.
- Distributed Agents runtime profile comparison over the focal `logfoldchanges` matrix,
  using `pvals_adj < 0.05` as the significant-feature threshold.
- External literature from PubMed/BioEval Literature:
  Knuesel et al. 2008, DOI `10.1128/MCB.00993-08`, PMID `19047373`;
  Park et al. 2018, DOI `10.1074/jbc.RA118.001725`, PMID `29440396`;
  Klatt et al. 2020, DOI `10.1073/pnas.1917635117`, PMID `31988137`;
  Fant and Taatjes 2018, DOI `10.1080/21541264.2018.1556915`,
  PMID `30585107`; Rocha et al. 2010, DOI `10.1242/dev.053660`,
  PMID `20630950`; Graham and Schwartz 2013, DOI `10.1002/ajmg.a.36183`,
  PMID `24123922`; Chao et al. 2024, DOI `10.1016/j.molcel.2024.09.001`,
  PMID `39321804`; Schiano et al. 2023, DOI `10.1016/j.lfs.2023.121986`,
  PMID `37516429`.

## Dataset computations

I first read the focal training count table to get the observed
`151 TH Prkcd Grin2c Glut` counts for mechanistically relevant measured genes.
The whole training table has 1,674 non-held-out perturbations; only 469 have any
focal DEGs, and the median target has 0 DEGs, so a nonzero prediction needs
target-specific support.

For the parquet, I filtered to:

- `group_name = '151 TH Prkcd Grin2c Glut'`
- `gene_target in ('Med13','Med15','Med23','Med13l','Cdk8')`

and recomputed `sum(pvals_adj < 0.05)` from the raw rows. This verified the
training CSV counts and also extracted the significant genes and matched-cell
depths:

| perturbation | matched perturbed nuclei | observed focal `n_degs` | focal FDR pattern |
| --- | ---: | ---: | --- |
| `Med13` | 154 | 11 | 10 down, 1 up |
| `Med15` | 158 | 19 | 19 down |
| `Med23` | 160 | 13 | 13 down |
| `Med13l` | 200 | 1 | `Grm1` down only |
| `Cdk8` | 192 | 0 | no FDR hits |

The shared FDR genes show that the first three are not merely all weak
transcriptional regulators; they hit the same 151-thalamic down-module.

| comparison | shared same-direction FDR hits at `pvals_adj < 0.05` |
| --- | --- |
| `Med13` vs `Med15` | 7 down: `Prkcd`, `Plekhg1`, `Pcp4`, `Atp2a2`, `Grm1`, `Ildr2`, `Kcnc2` |
| `Med13` vs `Med23` | 7 down: `Prkcd`, `Pcp4`, `Lrrtm1`, `Plekhg1`, `Grm1`, `Atp2a2`, `Grin2b` |
| `Med15` vs `Med23` | 8 down: `Prkcd`, `Grm1`, `Pcp4`, `Lef1`, `Plekhg1`, `Atp2b1`, `Ptpn3`, `Atp2a2` |
| `Med13l` vs the module | only the `Grm1` down hit |
| `Cdk8` vs the module | no FDR-level overlap because `Cdk8` has 0 focal hits |

The Distributed Agents runtime comparison produced the same FDR-level structure: `Med13`
shared 7 of its 10 downregulated focal hits with `Med15` and 7 with `Med23`,
`Med15` and `Med23` shared 8, `Med13l` shared only 1, and `Cdk8` shared 0. I did
not rely on the whole-vector cosine values because the full `logfoldchanges`
vectors contain many unexpressed-tail genes with saturated fold changes; the
significant-gene intersections are the interpretable evidence.

## Same-experiment corpus evidence

The Distributed Agents corpus had no direct `Med12` entry in this filtered release. Its
Mediator claims nevertheless matched the direct parquet analysis:

- Claim `5e659f9635ae7c6756a7`: in directly measured Mediator perturbations,
  `Med13`, `Med15`, and `Med23` converge on a downregulated
  `151 TH Prkcd Grin2c Glut` neuronal module, whereas `Med13l` provides only a
  narrow `Grm1` overlap and `Cdk8` does not phenocopy the module.
- Claim `c9b421b0631e4be67b3b`: represented kinase-module components are not
  interchangeable in postnatal neurons because `Cdk8` is flat and `Med13l` only
  weakly overlaps the broader `Med13`/`Med15`/`Med23` thalamic module.
- The `Med15` and `Med23` target contexts emphasize that their focal signatures
  downregulate differentiated neuronal synaptic, calcium/ion-handling, receptor,
  and adhesion genes rather than activating a generic stress, cholesterol, or
  unfolded-protein program.
- The `Cdk8` target context is an important boundary: `Cdk8` had 0 downstream
  FDR<0.10 genes in all recovered neuronal groups, and in 151 cells other
  transcriptional regulators such as `Brd4`, `Phf12`, `Chd8`, and `Med23` were
  readily detected. Thus the kinase subunit's zero is target-specific rather
  than a failure of this cell group to report transcription-factor loss.

## Target-specific reasoning

### `Med12`

**Biological placement.** `MED12` is one of the four subunits of the Mediator
kinase module with `MED13`, `CDK8` or `CDK19`, and `CCNC`; `MED12` stimulates
Cyclin C-CDK8/19 kinase activity, and `MED13` helps join the module to core
Mediator (Knuesel et al. 2008; Park et al. 2018; Fant and Taatjes 2018; Klatt
et al. 2020). A recent human Mediator structure also shows MED12 and MED13
together anchoring the kinase module onto core Mediator (Chao et al. 2024).
`MED12` is developmentally important: Med12 hypomorphic mice have severe early
developmental defects with impaired canonical Wnt and Wnt/planar-cell-polarity
signaling, and human MED12 variants cause X-linked neurodevelopmental syndromes
(Rocha et al. 2010; Graham and Schwartz 2013; Schiano et al. 2023).

**Closest within-dataset analogs.** The best measured analog is `Med13`: it is
the represented scaffold partner in the same kinase module and had 11 focal
DEGs, mostly downregulated `Prkcd`, `Grin2b`, `Plekhg1`, `Atp2a2`, `Lrrtm1`,
`Pcp4`, `Grm1`, `Ildr2`, `Ramp3`, and `Kcnc2`, plus upregulated `Scnm1`.
`Med15` and `Med23` are not kinase-module subunits but are observed Mediator
subunits with stronger expression-pattern convergence than the measured
`Med13` paralog: they had 19 and 13 focal DEGs and repeatedly hit `Prkcd`,
`Pcp4`, `Grm1`, `Plekhg1`, `Atp2a2`, `Atp2b1`, `Lef1`, and `Ptpn3` in the same
direction. Those counts put the Mediator-sensitive 151 response in the
low-teens to about 20-DEG range.

**Counterexamples.** `Cdk8` is the enzymatic partner of `Med12` but had 0 focal
DEGs despite 192 matched perturbed nuclei, so acute loss of the CDK8 catalytic
subunit cannot be used to call `Med12` zero: the training data show that
kinase-module members are not interchangeable. Conversely, `Med13l` is a
paralog of `Med13` and is in a related kinase-module scaffold family, but it
had only 1 focal DEG, the shared downregulated `Grm1`; this prevents predicting
a broad multi-hundred DEG response just from the external importance of
Mediator disease genes. `Ctnnb1` and `Tcf7l2` had much broader focal responses
of 383 and 106 DEGs, respectively, showing that a Wnt/TCF axis is readable in
these cells, but the observed `Med13`, `Med15`, and `Med23` signatures captured
only a small subset of that state. I therefore treated Wnt as a reason for
`Med12` to be nonzero, not as a reason to copy the `Ctnnb1` scale.

**Prediction.** The evidence supports a nonzero but narrow postmitotic effect.
The point estimate is `13` DEGs: essentially the observed `Med13`/`Med23`
response breadth, below `Med15`, and far below broad chromatin or beta-catenin
perturbations. This is driven mainly by the within-dataset Mediator module;
external literature decides that `Med12` should be compared first with
`Med13`, `Med15`, and `Med23`, while `Cdk8`, `Med13l`, `Ctnnb1`, and `Tcf7l2`
serve as boundaries.

## Limits

- There is no direct `Med12`, `Med12l`, `Ccnc`, or `Cdk19` perturbation in the
  supplied training universe, so the prediction extrapolates from neighboring
  Mediator subunits rather than from a same-subunit paralog.
- `Med12` has embryonic and Wnt-dependent biology that the P16-to-P37/44
  postmitotic neuronal design deliberately under-samples; the estimate should
  not be read as a germline or cortical-progenitor loss-of-function phenotype.
- The observed Mediator module is specific to `151 TH Prkcd Grin2c Glut` cells
  and only 11 to 19 FDR<0.05 genes wide for the closest positives. A one- or
  two-gene threshold change would noticeably change the reported count.
- None of these data measure DNA indels, MED12 protein loss, or kinase activity.
  Weak target-RNA depletion in an snRNA-seq row would not itself prove a failed
  knockout.

## Final point prediction

| target_name | predicted_n_degs |
| --- | ---: |
| `Med12` | 13 |
