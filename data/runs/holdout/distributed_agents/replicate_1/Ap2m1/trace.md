# Held-out DEG-count prediction for `151 TH Prkcd Grin2c Glut`

## Question and endpoint

The task asks for a point prediction of `n_degs` for held-out `Ap2m1` loss of
function in `151 TH Prkcd Grin2c Glut` thalamic glutamatergic neurons.
`n_degs` is the number of measured genes with Wilcoxon BH-adjusted
`pvals_adj < 0.05` in perturbed nuclei versus matched controls. I treated this
as an assay-specific response-breadth endpoint, not as a direct measure of
essentiality, viability, editing efficiency, or synaptic function.

There was no supplied rank supervision: the requested-target manifest contains
only the unranked scalar target `Ap2m1`. I therefore did not use the ranking
workbench or ordering validator; those capabilities were unavailable for this
count-prediction task.

## Sources used

- Direct inputs:
  - `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`
  - `training differential-expression dataset`
  - `single-target request for Ap2m1`
- Run-local task metadata:
  - `codex_runtime/pipeline/dataset_context.md`
  - `codex_runtime/pipeline/task_bindings.json`
  - `codex_runtime/pipeline/coverage.json`
  - `codex_runtime/pipeline/capabilities.json`
  - `codex_runtime/pipeline/measurement_registry.json`
- Internal same-experiment corpus:
  - PerturbAI July sourceguard corpus
    `july_260713_sourceguard_1773_v1`
  - There was no packaged `Ap2m1` report or `Ap2m1` Finding in the filtered
    source; I used the packaged `Cltc`, `Dnm1`, and `Rab7` reports only to
    interpret adjacent visible perturbations from the same experiment.
- External biological literature:
  - Helbig et al., 2019, *American Journal of Human Genetics*,
    DOI `10.1016/j.ajhg.2019.04.001`, PubMed `31104773`: recurrent
    AP2M1 p.Arg170Trp in developmental and epileptic encephalopathy, with AP-2
    conformational activation and transferrin uptake defects.
  - Bonifacino and Traub, 2003, *Annual Review of Biochemistry*,
    DOI `10.1146/annurev.biochem.72.121801.161800`, PubMed `12651740`:
    AP complexes, including AP-2, recognize cytosolic sorting motifs and couple
    transmembrane cargo to coated-vesicle sorting.
  - Koscielny et al., 2017, *Molecular Neurobiology*,
    DOI `10.1007/s12035-017-0436-3`, PubMed `28190237`: neuronal AP-2
    subunit knockdown affects dendrite morphology through mTOR-dependent GluA2
    expression in developing rat hippocampal neurons.
  - Liu et al., 2021, *Science Signaling*,
    DOI `10.1126/scisignal.abg3555`, PubMed `34315807`: LRRK2-dependent
    AP2M1 phosphorylation regulates clathrin-coated vesicle cycling and links
    AP-2 regulation to dopaminergic neurodegeneration models.
  - Gonzalez-Gaitan and Jackle, 1997, *Cell*,
    DOI `10.1016/s0092-8674(00)81923-6`, PubMed `9118220`: alpha-adaptin/AP-2
    participates in presynaptic vesicle recycling in Drosophila.

## Computation over the declared data

I first verified the held-out setup. The requested manifest has exactly one
target, `Ap2m1`; it is absent from the training count CSV, and an exact
`pyarrow.dataset` query of the focal-cell Parquet rows returned zero rows for
`gene_target == "Ap2m1"`.

I then used the training CSV as the observed quantitative scale for the focal
cell group. It contains 1,674 unique training targets. The endpoint is highly
zero-inflated in this group: 1,205 targets have zero DEGs, the median is 0, the
75th percentile is 1, the 90th percentile is 2, the 95th percentile is 18, and
the maximum is 2,677. A prediction of a few DEGs is therefore already above the
typical focal-cell perturbation.

Finally, I pulled the exact focal signatures for a bounded mechanistic panel
with:

```python
scanner = dataset.scanner(
    columns=[
        "names", "gene_target", "group_name", "scores",
        "logfoldchanges", "pvals_adj",
        "n_pert_matched", "n_ctrl_matched",
    ],
    filter=(
        (pc.field("group_name") == "151 TH Prkcd Grin2c Glut") &
        pc.field("gene_target").isin(candidate_genes)
    ),
)
```

Those focal Parquet rows were used to inspect which genes passed
`pvals_adj < 0.05`, the best subthreshold genes, and matched nucleus counts for
the analogs below.

## `Ap2m1` analogs and counterexamples

### Core clathrin/AP-2 analog: `Cltc`

`Ap2m1` encodes the mu2 cargo-binding subunit of the heterotetrameric AP-2
adaptor, the major adaptor that recruits selected plasma-membrane cargo into
clathrin-coated pits. Its nearest visible perturbation by proximal function was
`Cltc`, the clathrin heavy chain.

`Cltc` produced 3 focal DEGs at FDR 0.05 in the training endpoint. In the
Parquet it had only 32 matched perturbed `151` nuclei against 23,679 matched
controls. The three FDR<0.05 genes were small, down-regulated neuronal genes:
`Gabra4`, `Rbms1`, and `Ero1b`, each at `pvals_adj = 0.0424`. Four additional
genes were just below the looser FDR 0.10 threshold in the packaged report:
`Grid2ip`, `Synpo2`, `Gabbr1`, and `Jund`. That pattern means focal thalamic
neurons crossed the threshold only weakly after a core clathrin perturbation:
there was a trace of receptor/spine and stress remodeling, but no broad
lysosomal or proteasome program.

I used `Cltc` as the anchor for the point estimate rather than as a guarantee
of a large effect. AP2M1 loss should impair AP-2-dependent cargo selection at
the first clathrin-coated-pit step, so the causal chain
`Ap2m1 LoF -> impaired AP-2 coat/cargo function -> impaired receptor and
synaptic membrane endocytosis -> possible delayed neuronal compensation ->
snRNA DE among recovered nuclei` is the same early-endocytic direction as
`Cltc`. However, AP-2 is a specific adaptor, whereas clathrin heavy chain also
supports multiple clathrin-coated transport steps, so `Cltc` can be an upper
or only partially overlapping analog.

### Synaptic endocytosis and uncoating controls: `Dnm1`, `Synj1`, `Hspa8`,
`Nsf`, `Dnajc5`, `Bin1`, and `Stxbp1`

The `Cltc` same-experiment report explicitly showed that the canonical vesicle
fission or uncoating genes did not phenocopy the `Cltc` nuclear state. The
focal FDR<0.05 endpoint supported the same boundary:

| training perturbation | focal `n_degs` | focal interpretation |
| --- | ---: | --- |
| `Dnm1` | 1 | only the `Dnm1` transcript itself passed FDR |
| `Synj1` | 1 | only the `Synj1` transcript itself passed FDR |
| `Nsf` | 0 | no adjusted downstream response |
| `Dnajc5` | 1 | only the `Dnajc5` transcript itself passed FDR |
| `Bin1` | 1 | only the `Bin1` transcript itself passed FDR |
| `Stxbp1` | 1 | only the `Stxbp1` transcript itself passed FDR |
| `Hspa8` | 9 | weak heat-shock/cochaperone response, not a `Cltc` phenocopy |

These are counterexamples to a large prediction. The neuronal literature makes
AP-2, clathrin, dynamin, synaptojanin, auxilin/Hsc70, and related machinery all
important for membrane traffic, but the PerturbAI readout does not report every
vesicle-cycle defect as a broad nuclear expression response after P16 mosaic
CRISPR. For `Ap2m1`, an AP-2 coat defect is upstream of cargo internalization
and closer to `Cltc` than to isolated vesicle fission, but these flat or
self-only perturbations argue that a zero-to-single-digit DEG count is the
right local scale.

### Other adaptor complexes: `Ap1b1`, `Ap1s2`, `Ap3b1`, and `Ap4s1`

The visible AP-complex subunit perturbations also sat at the floor:

| training perturbation | focal `n_degs` | focal interpretation |
| --- | ---: | --- |
| `Ap1b1` | 1 | only the `Ap1b1` transcript itself passed FDR |
| `Ap1s2` | 0 | no adjusted focal response |
| `Ap3b1` | 0 | no adjusted focal response |
| `Ap4s1` | 0 | no adjusted focal response |

I used these as pathway-adaptor counterexamples rather than as direct
paralogs. AP-1/AP-3/AP-4 work in endosomal or trans-Golgi sorting, not in the
same plasma-membrane AP-2 complex as AP2M1. Their near-null counts therefore
show that being an adaptor-complex subunit is not enough to trigger a broad
151-class transcriptional state.

### Late endosomal and proteostasis counterexamples: `Rab7`, `Psmb4`, `Psmc1`,
and `Caml`

The focal training set contains very large stress endpoints for other
trafficking or proteostasis lesions: `Rab7` had 501 DEGs, `Psmb4` 742,
`Psmc1` 430, and `Caml` 28. I did not transfer those counts to `Ap2m1`.
The `Rab7` report showed a 151-class lysosomal/autophagy, sterol, ISR, and
proteasome-recovery state, with `Atp6v1b2`, `Dpp7`, `Insig1`, `Atp6v0b`,
`Atp2a2`, `Msmo1`, `Grin2b`, and `Fdft1` among the strongest focal genes.
The `Psmb4`/`Psmc1` states similarly represent proteasome recovery and
secondary stress. Those causal chains start at degradative lysosomal or
proteasome failure rather than AP-2-dependent cargo capture at the plasma
membrane, and visible early endocytic perturbations did not reproduce them.

## Biological decision for `Ap2m1`

AP2M1 is an obligate AP-2 subunit, so I predicted a nonzero response rather
than a strict null. The strongest external evidence is functional: the
pathogenic recurrent AP2M1 Arg170Trp variant impairs AP-2 conformational
activation and clathrin-mediated uptake, and AP-2 perturbation in neurons can
alter receptor trafficking and dendrite development. Those data make AP2M1 a
real neuronal endocytic perturbation, not a superficial family member.

The count, however, should remain near the `Cltc`/endocytosis local floor. The
requested experiment is an acute, partial, sparse postnatal CRISPR loss in
surviving NeuN-positive nuclei. It does not assay embryonic AP2M1 functions,
patient missense variants, synaptic-vesicle physiology, receptor
internalization, or dendritic arbor morphology directly. In the same focal
cell type, perturbing `Cltc` yielded 3 DEGs and the visible fission/uncoating,
AP-complex, and exocytosis genes were 0 or 1 except for the small `Hspa8`
stress response. I therefore assigned the point estimate equal to the observed
`Cltc` focal endpoint:

`Ap2m1 -> predicted_n_degs = 3`.

## Limits

`Ap2m1` itself was held out, AP-2 alpha, beta2, sigma2 and several auxilin
targets were not available as exact focal training perturbations, and the
dataset provides no DNA-indel, AP2M1 protein, transferrin-uptake,
AMPA-receptor-internalization, electrophysiology, or cell-depletion readout.
The prediction is consequently a transfer from a small `Cltc` signature and
near-null endocytic neighbors, not a direct observation. A stronger or more
complete AP2M1 perturbation, an embryonic developmental assay, or a human
Arg170Trp missense model could produce a much broader phenotype than this P16
mosaic loss-of-function snRNA endpoint.
