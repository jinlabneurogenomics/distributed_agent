# Question and endpoint

The requested prediction is the number of genes that would pass BH-adjusted
Wilcoxon `pvals_adj < 0.05` after an acute mosaic CRISPR loss of the held-out
gene `Ppp2r1a` in `151 TH Prkcd Grin2c Glut` thalamic glutamatergic neurons.
`Ppp2r1a` was absent from both the supplied differential-expression Parquet and
the focal-cell training count CSV, so the target's own DEG count and expression
signature are not directly observed. The training count table is a direct
measurement of the same endpoint for non-held-out perturbations; the Parquet is
direct expression-pattern evidence for those same perturbations. The held-out
endpoint itself is absent from the declared inputs and has to be inferred.

I resolved one small ambiguity conservatively: the requested output is a point
prediction for an assay- and power-dependent DEG count, not for PP2A functional
importance, neuronal viability, synaptic strength, or phosphatase activity.

# Sources

- Supplied `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`: observed
  `pvals_adj < 0.05` DEG counts for 1,674 visible perturbations in the focal
  `151 TH Prkcd Grin2c Glut` group.
- Supplied `training_de_all_cell_groups.parquet`: per-gene Wilcoxon statistics,
  exact focal-cell adjusted p values, log2 fold changes, and matched nucleus
  counts for all non-held-out perturbations.
- `dataset.perturbseq_features` workbench: cached target-level summaries from
  the declared Parquet. The summarize step ran over 616,253,184 rows and wrote
  `evidence/perturbseq_features.parquet`. The nested calibration subcommand
  correctly did not run because this task has no active ranked or partial-ranked
  supervision in `task_bindings.json`.
- July 2026 PerturbAI same-experiment corpus,
  `perturbai-july-260713-sourceguard-1773-v1`: gene-scoped Findings and
  packaged Evidence/Reference records for the represented PP2A and calcineurin
  comparators. This corpus is an interpretation layer over the same experiment,
  not independent replication.
- PubMed literature for PP2A mechanism and neural phenotypes:
  Verbinnen et al. 2021, DOI `10.1042/BST20201313`, PMID `34241636`;
  Biswas et al. 2020, DOI `10.3390/ijms21041286`, PMID `32074998`;
  Papke et al. 2021, DOI `10.1016/j.jbc.2021.100313`, PMID `33482199`;
  Wang et al. 2025, DOI `10.1172/JCI185602`, PMID `40839403`.

# Computation

I first inspected the full focal-cell training count distribution. It is
strongly concentrated at zero: 1,205 of 1,674 perturbations had `n_degs = 0`;
the median was 0, the 75th percentile was 1, the 95th percentile was 18, and a
few high-yield targets accounted for the heavy tail.

I then used the Parquet, filtered to `151 TH Prkcd Grin2c Glut`, to verify that
the PP2A and protein-phosphatase analog counts were the same in the exact
Wilcoxon rows and to inspect the boundary adjusted p values:

```python
import pyarrow.compute as pc
import pyarrow.dataset as ds

dset = ds.dataset("training_de_all_cell_groups.parquet", format="parquet")
targets = ["Ppp2r2b", "Ppp2r5d", "Ppp3ca", "Ppp3cc", "Ppp3r1"]
expr = (
    (pc.field("group_name") == "151 TH Prkcd Grin2c Glut")
    & pc.field("gene_target").isin(targets)
)
rows = dset.to_table(
    columns=[
        "names", "scores", "logfoldchanges", "pvals", "pvals_adj",
        "gene_target", "n_pert_matched", "n_ctrl_matched",
    ],
    filter=expr,
).to_pandas()
```

Each PP2A regulatory target had 17,259 measured focal rows, corresponding to
all measured genes in this cell group. The two direct PP2A training analogs
were flat at the requested threshold:

| training perturbation | relationship to `Ppp2r1a` | focal matched perturbed nuclei | focal `n_degs` | smallest focal `pvals_adj` |
| --- | --- | ---: | ---: | ---: |
| `Ppp2r2b` | PP2A B55-beta substrate-targeting regulatory subunit | 151 | 0 | 0.3617 |
| `Ppp2r5d` | PP2A B56-delta substrate-targeting regulatory subunit | 141 | 0 | 0.4050 |
| `Ppp3ca` | calcineurin catalytic subunit; PPP phosphatase but not PP2A | 240 | 4 | 6.35e-12 |
| `Ppp3cc` | calcineurin catalytic paralog; PPP phosphatase but not PP2A | 104 | 0 | 1.0 |
| `Ppp3r1` | calcineurin regulatory subunit; not PP2A | 93 | 9 | 2.21e-07 |

The whole-Parquet feature summary gave the same qualitative picture across all
22 measured neuronal groups: `Ppp2r2b` had zero genes at FDR 0.05 or 0.10
screen-wide; `Ppp2r5d` had only two genes at FDR 0.05 and four at FDR 0.10
screen-wide; calcineurin perturbations were also small, with 8, 0, and 11
FDR-0.05 genes for `Ppp3ca`, `Ppp3cc`, and `Ppp3r1`.

# Target-specific reasoning

## `Ppp2r1a`

`Ppp2r1a` encodes the PP2A A scaffold subunit. PP2A holoenzymes are assemblies
of a scaffold A subunit, a catalytic C subunit, and one of many substrate-
targeting B regulatory subunits; the B subunit controls substrate choice and
subcellular localization. PPP2R1A, PPP2R5D, and PPP2CA variants all cause
overlapping PP2A-related neurodevelopmental syndromes, so `Ppp2r1a` is not a
biological null gene. In mouse forebrain excitatory neurons, heterozygous
`Ppp2r1a` loss altered excitatory synaptic transmission and spatial learning
through an endocannabinoid-linked mechanism. Those data support endpoint
relevance at the level of neuronal physiology and PP2A assembly, but they are
developmental/forebrain phenotypes and do not directly predict a 3-4 week
postnatal sparse-CRISPR snRNA-seq DEG count in thalamic neurons.

The two direct represented PP2A subunits in the training set, `Ppp2r2b` and
`Ppp2r5d`, were the main local analogs. They are not obligate surrogates for
the A scaffold: knocking out a B55 or B56 regulatory subunit removes only a
subset of PP2A holoenzymes, whereas disrupting the A scaffold should impair a
broader assembly step. That direction argues that `Ppp2r1a` could be at least
as strong as either regulatory subunit. However, the exact same assay found no
focal-cell genes at BH < 0.05 for either `Ppp2r2b` or `Ppp2r5d`. The boundary
genes were not near the threshold: `Ppp2r2b`'s smallest adjusted p value in the
focal group was 0.3617, and `Ppp2r5d`'s was 0.4050. The July same-experiment
corpus also summarized `Ppp2r2b` as having zero downstream FDR < 0.10 genes in
all 22 measured cell groups, with no FDR-level compensation by `Ppp2r2a`,
`Ppp2r2c`, `Ppp2r2d`, or `Ppp2r5d` transcripts. For `Ppp2r5d`, the packaged
corpus recorded only three FDR < 0.10 downstream genes across the entire screen,
restricted to two superficial intratelencephalic cortical groups and absent
from `151 TH Prkcd Grin2c Glut`.

I used PP2A-linked kinase and cytoskeletal pathways as counterexamples rather
than as direct analogs. Some of their focal counts were nonzero, for example
`Tsc2` = 86, `Opa1` = 37, `Ctnnb1` = 383, and `Gsk3b` = 6. Others in the same
expected PP2A-adjacent space were flat or nearly flat, including `Mtor` = 2,
`Rptor` = 0, `Akt3` = 0, `Pik3cb` = 0, `Pik3r1` = 0, `Pik3r2` = 0, `Mapt` = 1,
`App` = 1, `Mff` = 0, `Prkar1a` = 1, and `Dnm1` = 1. This split matters because
PP2A regulates phosphorylation of many substrates, but the local screen shows
that disrupting a substrate pathway can produce a thalamic RNA state while loss
of the represented PP2A regulatory subunits does not automatically propagate
into that state at the mRNA level.

The closest phosphatase-family comparators did not justify moving the
prediction into the heavy tail. `Ppp3r1` and `Ppp3ca` weakened the calcineurin
holoenzyme and produced only 9 and 4 focal DEGs at FDR 0.05; the same-experiment
corpus reported that they shared only the `Pcsk1n` response in this cell group
and lacked the broad NFAT or immediate-early program expected from a generic
calcium/calcineurin model. `Ppp3cc`, the represented catalytic paralog, had
zero focal DEGs. These are useful bounds because they show that acute loss of a
neuronal Ser/Thr phosphatase holoenzyme component can be visible but still
sparse in `151 TH Prkcd Grin2c Glut`.

My causal transfer model was: AAV CRISPR frameshifts `Ppp2r1a` in a sparse
postmitotic neuron subset -> reduced PP2A A-alpha scaffold compromises some
ACB holoenzyme assembly -> phosphosite changes propagate through many
regulatory B-subunit-specific substrates, including AKT/mTOR/RPS6,
tau-kinase, mitochondrial, and synaptic pathways -> exposed thalamic neurons
either buffer phosphorylation changes or adjust state over 3-4 weeks -> only
surviving, recovered nuclei are sampled for nuclear RNA -> the endpoint counts
genes passing BH < 0.05. The represented PP2A B-subunit interventions act at
the same holoenzyme layer but affect narrower complexes; in the same screen
their substrate consequences were mostly buffered before the nuclear RNA
endpoint. There is no candidate-specific reason to expect `Ppp2r1a` loss to
reverse those effects, but the broader scaffold role is not enough, by itself,
to transfer the large `Tsc2`, `Opa1`, or `Ctnnb1` transcriptional outputs to
`Ppp2r1a`.

I therefore predict no FDR-passing focal DEGs for `Ppp2r1a`: biologically the
gene is PP2A-core and potentially active in neurons, but the directly observed
PP2A regulatory-subunit knockouts were all below threshold in this assay and
the broader PPP phosphatase comparators were sparse.

# Limits

The prediction is an extrapolation from PP2A regulatory subunits to the
PP2A A-alpha scaffold because `Ppp2r1a`, `Ppp2r1b`, `Ppp2ca`, `Ppp2cb`,
`Ppp2r5c`, and striatin PP2A-family components were not represented as training
perturbations. A scaffold knockout could disrupt more holoenzymes than either
`Ppp2r2b` or `Ppp2r5d`; conversely, partial mosaic CRISPR editing and recovery
of only surviving nuclei could hide an earlier cell-selection effect. The local
Parquet measures nuclear RNA, not protein abundance, PP2A activity, RPS6/tau/
Drp1 phosphorylation, mitochondrial morphology, synaptic physiology, or
endocannabinoid abundance. PP2A disease variants are often dominant missense
variants, whereas this experiment used acute loss-of-function indels, so human
variant studies define mechanism but not DEG count magnitude.
