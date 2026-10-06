# Reasoning trace

## Question and resolved ambiguities

The requested prediction is the integer number of genes that would pass
Benjamini-Hochberg FDR 0.05 after an `Adora2a` CRISPR loss-of-function
perturbation in the held-out cell group `151 TH Prkcd Grin2c Glut`.

The manifest at
`manifests/004_Adora2a.csv` contains one requested target:

```tsv
target_name
Adora2a
```

`Adora2a` is absent from both the training endpoint CSV and the
differential-expression parquet as a `gene_target`, so its answer must be
transferred from held-in perturbations. I interpreted `TH` according to the
dataset context as thalamus, not tyrosine hydroxylase; the requested group is a
thalamic glutamatergic class marked by `Prkcd`/`Grin2c`, not a dopaminergic or
striatal medium spiny neuron class.

## Sources used

- Direct training endpoint:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
  This has 1,674 non-held-out targets in the focal cell group; 1,205 have
  `n_degs = 0`, 363 have 1-9 DEGs, 63 have 10-89 DEGs, and 43 have at least 100
  DEGs. The median is 0 and the 95th percentile is 18.

- Direct differential-expression parquet:
  `[local file: training_de_all_cell_groups.parquet]`.
  I used this only for held-in targets, filtering to
  `group_name == "151 TH Prkcd Grin2c Glut"` and to mechanistically relevant
  `gene_target` values. The focal group has 17,259 measured genes per target.

- Same-experiment semantic layer: Distributed Agents corpus release
  `perturbai-july-260713-sourceguard-1773-v1`. The release has no `Adora2a`
  target node, but it does contain curated same-experiment findings and claims
  for held-in pathway analogs including `Drd2`, `Drd5`, `Gnal`, `Gnas`, `Adcy5`,
  and `Pde10a`.

- External biology: PubMed literature and prior database knowledge from
  UniProt/MGI/Alliance-style gene-function annotations. Specific papers used
  for A2A receptor biology were:
  - Schiffmann et al. 2007, `10.1016/j.pneurobio.2007.05.001`, PMID
    `17646043`: adenosine A2A receptors are enriched in enkephalinergic
    striatopallidal GABA neurons, interact antagonistically with dopamine D2
    receptors, and trigger cAMP/PKA signaling.
  - Ferre et al. 2004, `10.1016/j.parkreldis.2004.02.014`, PMID `15196504`,
    and Fuxe et al. 2003, `10.1212/01.wnl.0000095206.44418.5c`, PMID
    `14663004`: A2A/D2 receptor heteromers and A2A/mGluR5 interactions in
    striatopallidal neurons.
  - Heiman et al. 2008, `10.1016/j.cell.2008.10.028`, PMID `19013281`, and
    Lobo et al. 2006, `10.1038/nn1654`, PMID `16491081`: transcriptomic
    separation of striatonigral and striatopallidal medium spiny neuron
    subtypes.
  - Siuciak et al. 2006, `10.1016/j.neuropharm.2006.04.013`, PMID `16780899`:
    PDE10A inhibition in striatal medium spiny neurons increases cyclic
    nucleotide signaling and CREB/ERK phosphorylation.
  - Lein et al. 2006, `10.1038/nature05453`, PMID `17151600`: the Allen Mouse
    Brain Atlas as an anatomical expression reference; this supports treating
    `Adora2a` biology as basal-ganglia enriched rather than broadly thalamic.

## Computation over the training inputs

For the endpoint CSV, I summarized the empirical distribution of `n_degs` and
queried exact held-in counts for receptor-family and GPCR/cAMP candidates:

- dopamine/cAMP source arm: `Drd2`, `Drd4`, `Drd5`, `Gnal`, `Gnas`, `Gnao1`,
  `Gnb5`, `Adcy1`, `Adcy3`, `Adcy5`
- cyclic-nucleotide degradation and PKA/CREB arm: `Pde10a`, `Pde1c`, `Pde4b`,
  `Pde4d`, `Prkaca`, `Prkar1a`, `Creb1`, `Crebbp`
- other neuromodulatory or metabotropic receptor counterexamples in the same
  focal group: `Htr1a`, `Htr2a`, `Htr2c`, `Oprm1`, `Gabbr1`, `Gabbr2`, `Grm1`,
  `Grm5`, `Grm7`, `Grm8`

For the parquet, I used a column-pruned, predicate-filtered `pyarrow.dataset`
scan:

```python
filt = (
    ds.field("group_name") == "151 TH Prkcd Grin2c Glut"
) & ds.field("gene_target").isin(candidates)
tab = ds.dataset(parquet, format="parquet").to_table(
    columns=["names", "gene_target", "scores", "logfoldchanges",
             "pvals", "pvals_adj", "n_pert_matched", "n_ctrl_matched"],
    filter=filt,
)
```

I then counted `pvals_adj < 0.05`, recorded each candidate's minimum adjusted
p-value in the focal group, and inspected the strongest absolute Wilcoxon-score
genes. This was a check that the endpoint zeros were genuine focal null
signatures rather than transcriptional patterns hidden just below the training
CSV threshold.

## Target-specific reasoning

### Adora2a

`ADORA2A` is a seven-transmembrane adenosine A2A receptor. Its best-established
neuronal setting is the striatopallidal medium spiny neuron, where it opposes
`DRD2` and stimulates Gs/Golf-to-adenylyl-cyclase-to-cAMP/PKA signaling rather
than constituting an obligate transcription factor or chromatin complex. The
held-out target therefore has three good held-in proxy classes:

| Held-in proxy in `151 TH Prkcd Grin2c Glut` | Observed `n_degs` | Focal expression-pattern evidence | Why it is informative |
|---|---:|---|---|
| `Drd2` | 0 | all 17,259 measured genes were FDR-flat; min focal `pvals_adj = 1.0` | closest represented antagonist/partner of A2A on striatopallidal neurons |
| `Drd4`, `Drd5` | 0, 0 | both focal signatures were completely FDR-flat; each min focal `pvals_adj = 1.0` | dopamine GPCR family counterexamples represented in the same CRISPR screen |
| `Gnal` | 0 | all focal genes FDR-flat; min focal `pvals_adj = 1.0` | Golf alpha is the canonical striatal transducer downstream of D1/A2A-class receptors |
| `Gnas` | 0 | all focal genes FDR-flat; min focal `pvals_adj = 1.0` | general Gs alpha proxy for A2A coupling |
| `Adcy5` | 0 | all focal genes FDR-flat; min focal `pvals_adj = 0.912` | major striatal adenylyl cyclase downstream of D1/A2A/Golf signaling |
| `Adcy1`, `Adcy3` | 0, 0 | no focal FDR 0.05 genes; min focal `pvals_adj = 0.139` and `0.112` | represented membrane adenylyl-cyclase paralogs; direct loss of a single cAMP source was buffered |
| `Pde10a` | 0 | all focal genes FDR-flat; min focal `pvals_adj = 0.304` | strongest striatal cAMP/cGMP degradation-arm comparator |
| `Pde1c`, `Pde4b`, `Pde4d` | 0, 0, 0 | no focal FDR 0.05 genes; `Pde4b` and `Pde4d` min focal `pvals_adj` were 0.922 and 1.0 | PDE family counterexamples; the cAMP axis was not a generic focal RNA module |
| `Prkaca`, `Prkar1a` | 1, 1 | the only FDR 0.05 genes were the perturbed transcripts themselves | direct PKA subunits were edited enough to depress target RNA but still did not make a downstream focal program |
| `Creb1`, `Crebbp` | 10, 8 | a compact focal nuclear-transcription response was visible for `Creb1`, with `Crem` up as the top hit | downstream CREB-family/nuclear nodes can be detected in this focal group, so upstream receptor nulls are not simply because the assay cannot call any cAMP-linked genes |
| `Gabbr1`, `Gabbr2`, `Grm1`, `Grm7` | 1, 1, 1, 1 | each focal response was only the perturbed receptor transcript | thalamic GPCR or metabotropic-receptor edits tend to give target-only or no DE, not broad cell-state responses |
| `Oprm1`, `Htr1a`, `Htr2a`, `Htr2c`, `Grm5`, `Grm8` | 0 each | no FDR 0.05 focal genes | additional neuromodulatory receptor counterexamples in the same focal analysis |

The same-experiment Distributed Agents corpus supports the same interpretation away from
the exact focal cell group. It reports that `Adcy5` perturbation had no
downstream FDR signal across recovered neuronal groups, that represented
membrane adenylyl cyclases did not form a downstream module, and that
represented dopamine/GPCR and cAMP-pathway perturbations did not collapse into
a shared durable basal neuronal mRNA module. In the one striatal/LGE GABA
context where `Pde10a` generated the canonical compact `Scg2`/`Crem` response,
the receptor-to-cyclase source arm was flat: `Gnal`, `Gnas`, `Adcy5`, `Drd2`,
`Gnao1`, and `Pde4b` did not reproduce the `Pde10a` response. This is an
important counterexample: the assay can see a cAMP-linked output when a
degradation arm is perturbed in a striatal-like population, but receptor/G
protein/adenylyl-cyclase loss did not create a comparable basal transcriptome.

External biology pushes in the same direction for the requested thalamic
glutamatergic group. A2A is strongly associated with basal-ganglia indirect
pathway GABAergic neurons and presynaptic regulation of cortico- and
thalamo-striatal glutamatergic terminals, not with thalamic Prkcd/Grin2c
glutamatergic somata as an intrinsic developmental transcriptional regulator.
The held-in genes most likely to expose a striatal A2A-like signal (`Drd2`,
`Gnal`, `Adcy5`, `Pde10a`, `Gnas`) all had zero focal DEGs, and the training
endpoint is highly zero-inflated in this focal group. A positive call for
`Adora2a` would therefore require assuming that held-out A2A receptor loss is
more transcriptionally active in thalamic glutamatergic neurons than either
direct striatal cAMP components or other focal neuromodulatory GPCRs, and the
within-dataset evidence does not support that.

The point prediction is `0` DEGs.

## Limits of the prediction

- `Adora2a` itself was held out and absent from the Distributed Agents same-experiment
  corpus, so no direct `Adora2a` expression signature, corpus Finding, or
  corpus Claim was available.
- `Adora1`, `Adora2b`, and `Adora3` were not training perturbations in the focal
  endpoint CSV, so adenosine-receptor paralogs could not be checked directly.
  `Drd1`, `Ppp1r1b`, `Pde1b`, `Pde2a`, `Rgs9`, `Gpr88`, `Penk`, and `Pdyn` were
  also absent, leaving an incomplete striatal pathway panel.
- The best positive `Pde10a` result in the corpus came from a broad
  `059 CNU-LGE LSX GABA` group, not from a purified A2A-positive D2 medium spiny
  neuron type and not from the requested thalamic group.
- The experiment measured basal nuclear RNA 3-4 weeks after sparse P16 CRISPR.
  It did not measure adenosine ligand tone, acute GPCR signaling, cAMP,
  phospho-PKA, phospho-CREB, receptor heteromerization, presynaptic
  thalamo-striatal terminals, or electrophysiology. The zero prediction is
  specific to the FDR 0.05 snRNA-seq DEG-count endpoint, not to A2A receptor
  functional importance.
- Focal target-transcript rows were used only as pattern context. A weak
  self-transcript effect was not treated as evidence of failed editing, and a
  strong self-transcript effect was not treated as evidence for a broad
  downstream response.
