# Reasoning trace

## Question and endpoint

The requested prediction is the hidden `n_degs` for the held-out `Snap25`
perturbation in `151 TH Prkcd Grin2c Glut` cells. I interpreted `n_degs`
literally as the number of measured genes with `pvals_adj < 0.05` in the
focal class, including the perturbed transcript itself if it passes the
threshold. `Snap25` was absent from both declared training inputs: it had no
row in the training-count CSV and a direct Parquet query returned zero
`gene_target = 'Snap25'` rows.

The endpoint is directly observed for the 1,674 non-held-out perturbations in
`151 TH Prkcd Grin2c Glut`; the requested `Snap25` endpoint is absent by
construction and must be inferred from held-in analogs plus gene-function
priors.

## Sources used

- Declared Perturb-seq DE Parquet:
  `training differential-expression dataset`.
  I queried only rows from this declared input and treated it as the
  authoritative source for focal expression signatures.
- Declared training count CSV:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
  This was the authoritative source for observed focal `n_degs` in held-in
  perturbations.
- Requested-target manifest:
  `single-target request for Snap25`;
  it contained exactly one target, `Snap25`.
- Run-local dataset registry and the PerturbAI atlas dataset portrait, used
  for column semantics, focal-cell identity, and the guard that target-mRNA
  loss is not a quantitative editing-efficiency measure.
- PerturbAI July 260713 sourceguard-1773 corpus v1
  (`perturbai-july-260713-sourceguard-1773-v1`), limited to curated reports
  for held-in comparator genes. These reports are same-experiment summaries,
  not independent replication.
- PubMed literature for the external SNARE mechanism prior:
  Washbourne et al. 2002, Nature Neuroscience, DOI `10.1038/nn783`, PMID
  `11753414`; Rizo and Sudhof 2012, Annual Review of Cell and Developmental
  Biology, DOI `10.1146/annurev-cellbio-101011-155818`, PMID `23057743`;
  Rizo 2022, Annual Review of Biophysics, DOI
  `10.1146/annurev-biophys-111821-104732`, PMID `35167762`; Monteggia et al.
  2018, Neuroscience, DOI `10.1016/j.neuroscience.2018.08.014`, PMID
  `30144509`.

I did not use the rank-calibration workbench, ordering validator, or predictive
graph-review tooling because the capability manifest marks those operations as
unavailable for this scalar DEG-count task.

## Computation over the training inputs

The training count distribution in the focal class is extremely sparse:

| summary | value |
|---|---:|
| held-in perturbations | 1,674 |
| `n_degs = 0` | 1,205 |
| `n_degs = 1` | 276 |
| `n_degs <= 1` | 88.5% |
| median `n_degs` | 0 |
| 90th percentile | 2 |
| 95th percentile | 18 |

I selected held-in perturbations from the presynaptic SNARE and vesicle-release
apparatus as mechanistic analogs for `Snap25`, then queried their focal
Parquet rows and recomputed `sum(pvals_adj < 0.05)` to verify agreement with
the count table. The query was conceptually:

```sql
select gene_target,
       count(*) as measured_genes,
       sum(case when pvals_adj < 0.05 then 1 else 0 end) as n_degs
from read_parquet(:training_parquet)
where group_name = '151 TH Prkcd Grin2c Glut'
  and gene_target in (:held_in_synaptic_analogs)
group by gene_target;
```

Key held-in analogs all had focal signatures of only zero or one FDR 0.05 DEG:

| analog | observed focal `n_degs` | expression-pattern evidence in `151 TH Prkcd Grin2c Glut` | relationship to `Snap25` |
|---|---:|---|---|
| `Stx1b` | 0 | 17,259 measured genes, no FDR 0.05 calls | Syntaxin-1B is a plasma-membrane t-SNARE partner of SNAP-25; a close core-complex comparator. |
| `Vamp1` | 1 | 17,259 measured genes; the only call was `Vamp1` itself, log2FC -0.465, adjusted p 0.00187 | Synaptobrevin/VAMP is the vesicle v-SNARE opposing the syntaxin/SNAP-25 t-SNARE. `Vamp2`, the dominant central isoform, was held out, so `Vamp1` is a weaker but still same-machinery comparator. |
| `Stxbp1` | 1 | 17,259 measured genes; the only focal call was `Stxbp1` itself, log2FC -0.663, adjusted p 9.4e-19 | Munc18-1/STXBP1 templates and gates SNARE-complex assembly. It is a counterexample in the broader dataset because other neuronal classes had larger responses, but in the focal thalamic class it was a one-DEG perturbation. |
| `Cplx1` | 1 | 17,259 measured genes; the only focal call was `Cplx1` itself, log2FC -0.863, adjusted p 4.3e-24 | Complexin binds partly assembled SNARE complexes and regulates Ca2+-triggered release. |
| `Cplx2` | 0 | 17,259 measured genes, no FDR 0.05 calls | Complexin paralog and functional comparator for `Cplx1`; useful as a null counterexample within the same release machinery. |
| `Unc13a` | 0 | 17,259 measured genes, no FDR 0.05 calls | Munc13 opens syntaxin-1 and primes SNARE-mediated fusion upstream of the SNAP-25/syntaxin/VAMP complex. |
| `Unc13b` | 0 | 17,259 measured genes, no FDR 0.05 calls | Munc13 paralog; only 63 matched perturbed focal nuclei, so its focal null is underpowered but directionally consistent with `Unc13a`. |
| `Unc13c` | 0 | 17,259 measured genes, no FDR 0.05 calls | Munc13 paralog and release-priming comparator. |
| `Syp` | 1 | 17,259 measured genes; the only focal call was `Syp` itself, log2FC -1.78, adjusted p 8.0e-66 | Synaptic vesicle protein; less direct than SNAREs but a presynaptic vesicle-cycle comparator with a strong visible self-transcript call and no downstream focal program. |
| `Sv2a` | 1 | 17,259 measured genes; the only focal call was `Sv2a` itself, log2FC -1.05, adjusted p 1.9e-38 | Synaptic-vesicle release regulator; like `Syp`, informative mostly as a same-compartment null. |
| `Syn1` | 1 | 17,259 measured genes; the only focal call was `Syn1` itself, log2FC -0.834, adjusted p 1.6e-24 | Synaptic-vesicle reserve-pool regulator; indirect but consistent with a presynaptic perturbation causing only self-transcript DE. |
| `Syn2` | 0 | 17,259 measured genes, no FDR 0.05 calls | Synapsin paralog and null counterexample. |

The same-experiment July corpus agreed with the raw pattern for the closest
held-in analogs: its curated `Stx1b`, `Cplx1`, and `Cplx2` reports described
these targets as transcriptionally null or buffered across the assayed
neuronal groups and explicitly separated altered vesicle fusion from a large
nuclear RNA program. The corpus also noted that `Stxbp1` is a meaningful
counterexample: it can produce a larger response in selected classes, but in
the requested thalamic glutamatergic class its FDR 0.05 burden was still only
one gene.

Across the 16 most relevant available focal comparators
(`Stx1b`, `Stxbp1`, `Vamp1`, `Cplx1`, `Cplx2`, `Syn1`, `Syn2`, `Syp`, `Sv2a`,
`Syt2`, `Unc13a`, `Unc13b`, `Unc13c`, `Snca`, `Sncb`, `Napb`), the median
observed count was `0`, the mean was `0.44`, and the maximum was `1`. That
maximum matters: the direct presynaptic analogs did not include any perturbation
with a focal multi-gene downstream response.

## Target-specific biological transfer for Snap25

SNAP-25 is one of the core neuronal SNAREs. External biochemical and genetic
work places SNAP-25 in the heterotrimeric release complex with syntaxin-1 and
synaptobrevin/VAMP; Munc18-1/STXBP1 and Munc13 organize syntaxin and SNARE
assembly, while complexin and synaptotagmin regulate the primed SNARE complex
for Ca2+-evoked fusion. Washbourne et al. showed that complete genetic ablation
of SNAP-25 is essential for evoked transmission at neuromuscular junctions and
central synapses, and the Rizo reviews synthesize the same molecular model of
SNARE-dependent neurotransmitter release. This makes `Stx1b`, `Vamp1`,
`Stxbp1`, `Cplx1/Cplx2`, and `Unc13a/b/c` appropriate held-in comparators at
the level of intervention -> impaired presynaptic release machinery.

The transfer chain still weakens at the readout stage. The Perturb-seq assay
measured steady-state nuclear RNA in recovered, class-assigned nuclei 3 to 4
weeks after a sparse postnatal CRISPR perturbation. It did not measure vesicle
fusion probability, synaptic transmission, presynaptic protein abundance, or
loss of cells before FACS. The held-in analogs show that acute impairment of
core vesicle-release proteins is usually silent in this nuclear DEG endpoint
even when the same proteins are essential in electrophysiological assays.
`Stx1b`, the closest available t-SNARE analog, had zero focal DEGs; Munc13 and
complexin perturbations also failed to drive any downstream focal program.
`Stxbp1` demonstrated that the atlas can detect a broader presynaptic-stress
program when one occurs, but its requested-cell response was still just the
on-target transcript.

I therefore predict a nonzero but minimal endpoint. The nonzero call is driven
by the expectation that `Snap25` itself, a highly expressed neuronal mRNA, is
likely to be measured as the sole FDR-significant transcript after direct
CRISPR targeting, analogous to `Cplx1`, `Stxbp1`, `Syp`, `Sv2a`, `Syn1`, and
`Vamp1`. The lack of a larger count is driven by the stronger within-dataset
evidence: every biologically close held-in focal comparator was in the `0` to
`1` DEG range, and the same-experiment corpus characterized the SNARE-cycle
analogs as buffered rather than as a coherent low-amplitude transcriptional
module.

Final point prediction:

| target | predicted `n_degs` |
|---|---:|
| `Snap25` | 1 |

## Limits

- `Snap25` itself was held out, as was `Vamp2`, the predominant synaptobrevin
  isoform at many central synapses; `Vamp1` is an imperfect v-SNARE substitute.
- The most decisive phenotypes of SNAP-25, syntaxin, VAMP, Munc18, Munc13,
  complexin, and synaptotagmin are biochemical or electrophysiological. The
  supplied endpoint is an FDR threshold over nuclear RNA from surviving
  nuclei, so the correct count can be close to zero even for an essential
  fusion gene.
- Single-gene DEG calls in this assay often reflect the targeted transcript.
  I included that transcript because the endpoint definition includes every
  measured gene, but a visible self call is not evidence for the magnitude of
  downstream pathway disruption.
- Monteggia et al. showed mild phenotypes in adult heterozygous `Snap25` null
  mice, supporting dosage buffering, but those mice are not the same as sparse
  four-guide AAV CRISPR in postnatal thalamic glutamatergic neurons.
- `Unc13b` and `Unc13c` had lower or incomplete class recovery than the best
  analogs, so their focal zeros carry less weight than the `Stx1b`, `Cplx1`,
  `Cplx2`, `Unc13a`, and `Stxbp1` comparisons.
