# Rbfox1 DEG-count prediction

## Question and resolved ambiguities

The held-out target manifest contains one requested perturbation:

```tsv
target_name
Rbfox1
```

I interpreted the task as a point prediction for the number of whole-gene
Wilcoxon differential-expression calls at `pvals_adj < 0.05` in
`151 TH Prkcd Grin2c Glut` nuclei after acute AAV-CRISPR loss of `Rbfox1`.
The response to predict is the training endpoint `n_degs`, not the number of
alternative-splicing changes and not a direct estimate of knockout efficiency or
physiologic severity.

The most important ambiguity was how to transfer from RNA-binding and splicing
factors whose biology is primarily post-transcriptional. I resolved this by
calibrating against the same screen's gene-abundance consequences of measured
RNA-processing targets, then using the RBFOX literature only to decide which of
those measured targets are plausible analogs versus overly severe
counterexamples.

## Sources

- Input DEG parquet:
  `[local file: training_de_all_cell_groups.parquet]`.
- Input focal endpoint CSV:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Requested-target manifest:
  `[local file: 196_Rbfox1.csv]`.
- Internal same-experiment corpus: Distributed Agents corpus
  `perturbai-july-260713-sourceguard-1773-v1`.
- External literature database: NCBI PubMed, queried for `Rbfox1`/`A2BP1`
  neuronal splicing, knockout, and CLIP studies.

The Distributed Agents corpus had no direct `Rbfox1` target card or claim in this release.
It was still informative for the training comparators because it contains
perturbation-centered findings for `Hnrnpu`, `Hnrnpc`, `Hnrnpa2b1`, `Matr3`,
`Tardbp`, and `Son` in the same mouse P16-to-P37/44 screen.

## Computation over the supplied data

I first verified the target list and summarized the focal training-count table.
The focal endpoint has 1,674 non-held-out perturbations; 1,205 have
`n_degs = 0`, the median is 0, the 75th percentile is 1, the 90th percentile is
2, and a long right tail is driven by broad RNA-processing, proteostasis, and
chromatin/transcription perturbations such as `Uba5` with 2,677 DEGs and `Tpr`
with 1,768 DEGs.

I then searched the focal endpoint for RBFOX paralogs and RNA-binding or
splicing regulators that are actually represented in training. `Rbfox2`,
`Rbfox3`, `Nova1`, `Nova2`, `Mbnl1`, `Mbnl2`, `Mbnl3`, `Celf1`-`Celf4`,
`Elavl2`-`Elavl4`, `Ptbp1`, `Ptbp2`, `Srrm3`, and `Srrm4` are not present as
training targets, so there is no same-family or same-neuronal-AS factor with an
observed focal count. The measured RNA/RNP candidates and their observed
`151 TH Prkcd Grin2c Glut` counts were:

```tsv
target_name	n_degs
Hnrnpu	733
Tardbp	210
Matr3	149
Hnrnpc	122
Hnrnpa2b1	11
Atxn2	8
Ddx3x	8
Zc3h14	6
Hnrnph2	4
Hnrnpdl	1
Ylpm1	1
Ddx39b	0
Fmr1	0
Rbm28	0
Son	0
Tia1	0
```

For the same targets I read the focal rows from the parquet and recomputed
`sum(pvals_adj < 0.05)` to make sure the expression signatures matched the
training endpoint. The focal group had 17,259 measured genes per listed
perturbation. I also inspected the FDR-significant genes to determine whether a
count reflected target-proximal RBP remodeling or a much broader cell-stress
state.

## Within-dataset analogs and counterexamples

`Hnrnpa2b1`, 11 DEGs, is a useful weak RBP analog. Its focal signature was small
but RNA-factor-flavored: `Rbm25`, `Hnrnpa1`, `Tcerg1`, and `Drosha` increased,
while `Hnrnpu` and `Fam193b` decreased. The Distributed Agents `Hnrnpa2b1` card reports
only 25 FDR<0.10 calls across 6 of 21 measured groups and notes that
`Hnrnpa2b1` was far weaker than `Hnrnpu`, `Tardbp`, `Matr3`, and `Hnrnpc`.
This is an appropriate positive lower-bound analog because it shows that an
abundant nuclear RBP can produce a tiny but nonzero gene-abundance signature in
the focal thalamic group.

`Atxn2`, 8 DEGs, is a cytoplasmic RNA-binding/stress-granule comparator rather
than a spliceosome factor. Its focal DEGs were sparse and mixed, with `Srsf11`
and `Rsrp1` down and `Syt7`, `Crmp1`, `Sncb`, and `Cspg5` up. The Distributed Agents
corpus specifically concluded that ALS-linked or RNP-granule-family membership
does not imply a shared juvenile-neuron transcriptomic module: `Atxn2`,
`Matr3`, `Tardbp`, and `Tia1` are divergent or only partially overlapping.
`Atxn2` therefore supports the idea that a neuronal RBP can be visible without
becoming a broad stress perturbation.

`Hnrnph2`, 4 DEGs, `Hnrnpdl`, 1 DEG, and `Son`, 0 focal DEGs, are boundary
examples. `Hnrnph2` changed only `Rsrp1`, `Idh3g`, `Hnrnph2`, and `Ogdh` at
FDR 0.05 in the focal group. `Hnrnpdl` had only `Hnrnpu` up. `Son` had no focal
DEGs despite being a nuclear speckle/RNA-processing factor; the Distributed Agents `Son`
card notes that other RNA-processing factors such as `Prpf6`, `U2af2`,
`Hnrnpu`, `Snrnp70`, and `Tardbp` were much broader in the same screen. These
are appropriate for `Rbfox1` because RBFOX1 is also expected to have its most
direct effect at the splice-isoform level, which the whole-gene Wilcoxon readout
does not measure.

`Hnrnpc`, 122 DEGs, `Matr3`, 149 DEGs, and `Tardbp`, 210 DEGs, are moderate
RBP/splicing counterexamples. They show that the assay can detect RNA-binding
perturbations in `151 TH Prkcd Grin2c Glut`, but their expression patterns are
not close to an RBFOX-specific neuronal-AS expectation. `Hnrnpc` induced
`Txnl1`, `Tspan33`, `Cacna1a`, mitochondrial/nucleotide genes such as `Mterf3`
and `Slc25a36`, and proteostasis genes; `Matr3` induced `Ddhd1`, `Atp9b`,
`E2f4`, `Zkscan3`, `Sugp2`, `Gpt2`, and `Uggt2`; `Tardbp` induced a strong
`Ppp6c`/`Gabpa`/`Usp15`/`Uggt2` ER-lysosomal and organelle-maintenance module.
The Distributed Agents claims explicitly reject collapsing hnRNP-family or ALS/RBP
membership into one state. I therefore treated these as evidence for
detectability of RBP stress, not as count templates for `Rbfox1`.

`Hnrnpu` and the core spliceosome factors are high-end counterexamples:
`Hnrnpu` had 733 focal DEGs and `Rnpc3`, `U2af2`, `Cdc40`, `Prpf6`,
`Snrnp70`, and `Thoc1` ranged from 213 to 868 DEGs. Their signatures contain
broad RNA-processing, proteostasis, integrated-stress, synaptic, and
metabolic responses. The Distributed Agents corpus reports that core or adjacent
spliceosome/RNA-processing perturbations can share a recurrent neuronal module,
but that even this module is not generic to every spliceosome-associated target.
These targets are poor quantitative analogs for `Rbfox1` because RBFOX1 binds
UGCAUG elements to select regulated neuronal exons, whereas these perturbations
attack constitutive mRNA maturation or large RNP scaffolds.

## Rbfox1-specific biology

RBFOX1/A2BP1 is a neuronal and muscle RNA-binding splicing regulator. Its RRM
binds UGCAUG elements, and RBFOX1/2/3 CLIP in mouse brain defined more than one
thousand direct Rbfox-regulated alternative splicing events, including events in
synaptic and autism-risk genes (Weyn-Vanhentenryck et al. 2014,
doi:10.1016/j.celrep.2014.02.005, PMID:24613350). Human neuronal
differentiation data likewise place RBFOX1 over many alternative-splicing
events and a downstream neurodevelopmental gene-expression network (Fogel et al.
2012, doi:10.1093/hmg/dds240, PMID:22730494).

Mouse brain data point in the same direction but are important for the endpoint
here: CNS-specific `Rbfox1` deletion caused seizures and dentate-gyrus
hyperexcitability while producing many splicing changes with comparatively few
overall transcript-abundance changes (Gehman et al. 2011,
doi:10.1038/ng.841, PMID:21623373). Developmental expression mapping found
`A2bp1/Rbfox1` expression in postmitotic forebrain neurons and dense expression
in the ventrobasal dorsal thalamic complex postnatally (Hammock and Levitt
2011, doi:10.1159/000323732, PMID:21346316), so `Rbfox1` is not dismissed as
irrelevant to the focal thalamic glutamatergic class.

## Prediction

I predict a zero focal DEG count for `Rbfox1`.

The nonzero side of the decision is supported by biology: `Rbfox1` is a bona
fide neuronal RNA regulator, it is expressed in thalamic/forebrain neurons, and
full CNS deletion changes neuronal excitability. The zero side is stronger for
this endpoint. The 10x Flex whole-gene Wilcoxon test is not an exon-junction or
isoform assay, and the best mouse loss-of-function study reports splicing
defects with few changes in gene abundance. In the training table, the
regulators whose signatures are closest to "specific post-transcriptional RBP
biology without generic spliceosome collapse" sit at 0 to 11 DEGs in the focal
group, whereas the 100 to 800 DEG comparators are qualitatively broader stress
or core-maturation states. I therefore expect any `Rbfox1` whole-gene shifts in
`151 TH Prkcd Grin2c Glut` to fall below the Benjamini-Hochberg 0.05 cutoff.

```tsv
target_name	predicted_n_degs
Rbfox1	0
```

## Limits

No in-screen `Rbfox2` or `Rbfox3` perturbation was available, and neither were
the common neuronal splicing comparators `Nova1/2`, `Mbnl1/2/3`, `Elavl2/3/4`,
`Celf1`-`Celf4`, `Ptbp1/2`, or `Srrm3/4`. The strongest within-dataset
comparisons are therefore broad RBP/spliceosome counterexamples, not close
paralog phenocopies.

The parquet reports whole-gene abundance only. A prediction of zero DEGs should
not be read as a prediction that `Rbfox1` editing is phenotypically neutral: a
real exon-inclusion, cytoplasmic isoform, translation, or electrophysiologic
effect could be invisible to this readout. The estimate also extrapolates from
germline/CNS-deletion and in vitro RBFOX biology to sparse juvenile AAV-CRISPR,
where editing fraction, survival of edited nuclei, and cell-class composition
are not available for the held-out target.
