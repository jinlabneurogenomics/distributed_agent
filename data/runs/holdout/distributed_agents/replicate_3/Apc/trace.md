# Apc DEG-count prediction

## Question and resolved ambiguities

The held-out manifest `015_Apc.csv` contains one requested perturbation, `Apc`.
The endpoint to predict is the number of measured genes in `151 TH Prkcd
Grin2c Glut` with Benjamini-Hochberg adjusted Wilcoxon `pvals_adj < 0.05`
after acute AAV-CRISPR loss of the target gene. I treated this as a point
prediction for the same single-nucleus test used in the supplied training CSV,
not as a pathway activity score or a direction-specific count.

`Apc` is absent from both the training DEG parquet as a `gene_target` and from
the focal training-count CSV, so the prediction is extrapolated from non-held
out perturbations plus external APC/Wnt biology.

## Sources used

- `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
  for observed `n_degs` in the focal cell group.
- `[local file: training_de_all_cell_groups.parquet]`
  for focal-cell log fold changes, adjusted p-values, perturbed/control nucleus
  counts, and sentinel Wnt target behavior.
- Run-local Distributed Agents corpus, release
  `perturbai-july-260713-sourceguard-1773-v1`, via `target_context` and
  `candidate_set_topology`, for same-experiment findings about `Ctnnb1`,
  `Tcf7l2`, `Lrp6`, `Gsk3b`, and `Kremen1`.
- Distributed Agents runtime `profile_neighbors`, using the focal parquet signatures for
  the declared Wnt/catenin comparator cohort.
- PubMed literature:
  - Stamos and Weis 2013, "The beta-catenin destruction complex",
    DOI `10.1101/cshperspect.a007898`, PMID `23169527`.
  - Pronobis, Rusan and Peifer 2015, "A novel GSK3-regulated APC:Axin
    interaction regulates Wnt signaling by driving a catalytic cycle of
    efficient beta-catenin destruction", DOI `10.7554/eLife.08022`,
    PMID `26393419`.
  - van Kappel and Maurice 2017, "Molecular regulation and pharmacological
    targeting of the beta-catenin destruction complex",
    DOI `10.1111/bph.13922`, PMID `28634996`.
  - Mohn et al. 2014, "Adenomatous polyposis coli protein deletion leads to
    cognitive and autism-like disabilities", DOI `10.1038/mp.2014.61`,
    PMID `24934177`.
  - Pirone et al. 2016, "APC conditional knock-out mouse is a model of infantile
    spasms with elevated neuronal beta-catenin levels, neonatal spasms, and
    chronic seizures", DOI `10.1016/j.nbd.2016.11.002`, PMID `27852007`.

## Computations over the training data

I first verified that the requested target is only `Apc` and that the focal
training table has 1674 non-held-out perturbations. Its distribution is very
zero-inflated: 469 of 1674 perturbations have any q<0.05 genes in `151`, the
median is 0, the 75th percentile is 1, the 95th percentile is 18, and only the
top 1 percent exceed roughly 436 DEGs.

I then filtered the parquet to
`group_name == "151 TH Prkcd Grin2c Glut"` and to Wnt/beta-catenin
comparators observed in the training endpoint table. The operation was:

```python
df151 = parquet[
    (group_name == "151 TH Prkcd Grin2c Glut")
    & gene_target.isin(wnt_comparator_targets)
]
n_degs = (df151.pvals_adj < 0.05).groupby(df151.gene_target).sum()
```

The key observed focal counts were:

| training target | `n_degs` in 151 | perturbed nuclei | interpretation for Apc |
| --- | ---: | ---: | --- |
| `Ctnnb1` | 383 | 171 | Central beta-catenin effector; strong but opposite genetic sign from `Apc` loss. |
| `Tcf7l2` | 106 | 111 | Downstream beta-catenin/TCF transcriptional partner; shows the TCF arm is active in this cell group. |
| `Lrp6` | 4 | 120 | Positive upstream Wnt co-receptor; only a tiny LRP6-dependent receptor input is visible. |
| `Gsk3b` | 6 | 108 | Sign-matched negative regulator; isolated `Gsk3b` loss is buffered and does not induce canonical Wnt reporters. |
| `Kremen1` | 0 | - | Extracellular Wnt antagonist; no derepressed Wnt program. |
| `Lrp5` | 0 | - | LRP paralog; not interchangeable with `Lrp6` in this focal response. |
| `Fzd2`, `Fzd4`, `Fzd6`, `Fzd9` | 0 each | - | Single Frizzled receptors did not phenocopy the core Wnt perturbations. |
| `Macf1`, `Cdk8`, `Prickle1`, `Tbl1x` | 0 each | - | Wnt-adjacent or TCF-associated nodes that were FDR-flat in this readout. |
| `Csnk2b` | 25 | 110 | Casein kinase II subunit, not the core CK1 destruction-complex kinase; weak and not canonical. |
| `Chd8` | 61 | 197 | Wnt-linked chromatin factor in some systems, but the same-experiment corpus classified its juvenile neuronal response as non-phenocopying `Ctnnb1`/`Tcf7l2`. |
| `Rora` | 278 | 139 | Strong thalamic transcription-factor response, but a downstream differentiation comparator rather than an APC/beta-catenin destruction-complex analog. |

Sentinel genes supported the same split. `Ctnnb1` loss strongly reduced Wnt
feedback and thalamic terminal-state transcripts in this focal cell class:
`Axin2` logFC -0.94, q=1.2e-6; `Lef1` -0.62, q=1.6e-13; `Notum` -1.19,
q=0.0016; `Wnt9b` -1.11, q=0.0038; `Vangl1` -0.82, q=1.9e-10; and
`Ramp3`, `Gabra4`, `Gabrb2`, `Grin2b`, `Pcsk2`, and `Cpe` were also
significantly down. `Tcf7l2` reproduced the `Ramp3`/`Kcnc2`/`Pcsk2`/`Cpe`
side of that state and reduced `Lef1`, but it did not reduce every canonical
feedback gene. `Lrp6` trended in the `Ctnnb1` direction for `Axin2`
(-0.80, q=0.073) but had only four q<0.05 genes. `Gsk3b`, `Kremen1`, and
`Prickle1` left these sentinel genes nonsignificant.

The Distributed Agents corpus was concordant with those direct counts. Its `Ctnnb1` and
`Tcf7l2` claims describe a 151-enriched beta-catenin/TCF transcriptional
signature; its `Lrp6` findings report the restricted six-gene q<0.10 response
and same-direction `Lrp6`/`Ctnnb1` convergence; its `Gsk3b` findings explicitly
note that isolated `Gsk3b` loss produced only a small 151-specific response and
did not induce canonical Wnt/beta-catenin transcription; and its `Kremen1`
findings identify a pan-neuronal FDR-flat result despite detectable
`Ctnnb1`/`Tcf7l2`/`Lrp6` Wnt output in the same cell group.

## Target-specific reasoning for `Apc`

APC is in the core beta-catenin destruction complex with AXIN scaffolds, GSK3,
and CK1. Loss of APC should be the opposite sign of `Ctnnb1` or `Lrp6` loss:
it should stabilize beta-catenin and increase, rather than decrease, TCF/LEF
target transcription. APC is also a physical and regulatory component of the
AXIN complex rather than an extracellular ligand/receptor modulator, and
biochemical work argues that APC:AXIN interactions make beta-catenin
destruction efficient. That made the flat receptor-level genes
`Fzd2`/`Fzd4`/`Fzd6`/`Fzd9`, `Lrp5`, `Kremen1`, `Ror1`, `Ror2`, `Ryk`, and
`Lgr4` useful lower-bound counterexamples but too distant to drive the
prediction to zero.

The best focal analog for pathway capacity is `Ctnnb1`: it caused 383 q<0.05
genes and reduced a combined Wnt-feedback, adhesion, calcium, and synaptic
program. The best downstream transcriptional comparator is `Tcf7l2`, with
106 q<0.05 genes. Those counts argue that this particular thalamic glutamatergic
class can mount a beta-catenin/TCF mRNA response after P16 editing. However,
`Apc` loss is an activation of the pathway, not loss of the coactivator or TCF
factor, so I did not mirror the full `Ctnnb1` count. Overactivating beta-catenin
should up-regulate negative-feedback genes such as `Axin2`, `Notum`, and `Nkd1`,
but it need not erase the same thalamic terminal excitability genes that fell
after `Ctnnb1` or `Tcf7l2` loss.

The best sign-matched training comparator is `Gsk3b`, another negative
destruction-complex regulator, but `Gsk3b` loss caused only 6 q<0.05 genes and
the corpus found no canonical Wnt output. I downweighted that near-zero result
because GSK3A can buffer isolated `Gsk3b` loss and because GSK3B has many
beta-catenin-independent kinase roles. APC is more directly tied to AXIN and
beta-catenin turnover. I treated the 0-DEG `Kremen1` result similarly: it is
also sign-matched for Wnt derepression but acts through a DKK/LRP receptor arm
that was uncoupled from the basal postmitotic 151 state.

External neuronal data support a nonzero direction: neuronal/forebrain APC
conditional knockout in mice raises beta-catenin, changes canonical Wnt target
gene expression and N-cadherin synaptic adhesion complexes, alters dendritic
spines and synaptic physiology, and produces seizure/autism-like phenotypes
(Mohn et al. 2014; Pirone et al. 2016). Those models are stronger and more
developmental than this sparse AAV perturbation, so I used them only to reject
a zero prediction, not to inflate `Apc` to hundreds of DEGs.

Putting those pieces together, I predict that `Apc` will have a modest but
clearly nonzero 151 response: larger than `Gsk3b`/`Lrp6`/`Kremen1`, because
APC sits at the core of beta-catenin turnover, but smaller than `Tcf7l2` and
far smaller than `Ctnnb1`, because the perturbation sign is opposite and likely
feedback-limited. The point estimate is:

| target | predicted `n_degs` |
| --- | ---: |
| `Apc` | 52 |

## Limits

The extrapolation is imperfect. No training perturbation removes APC itself,
AXIN1/2, APC2, DVL, LEF1, PORCN, WLS, or a Wnt ligand in this focal context, so
the true immediate neighbor in the destruction complex is missing. All
sign-matched Wnt antagonist losses in the training table are weak or upstream,
while the strong `Ctnnb1` and `Tcf7l2` comparators are the opposite biochemical
sign. The experiment measures nuclear RNA 3-4 weeks after sparse juvenile
editing and does not assay indels, beta-catenin protein stabilization,
subcellular localization, cadherin complexes, phosphorylation, morphology,
seizures, or viability. The published APC conditional knockouts use different
timing, cell coverage, and often stronger recombination than this AAV CRISPR
screen. Finally, the DEG count is sensitive to the held-out `Apc` guide
efficiency and perturbed-cell recovery, neither of which is available for the
held-out readout.
