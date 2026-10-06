# Trace

## Question and resolved ambiguities

The requested endpoint is the integer number of genes with
`pvals_adj < 0.05` after loss of each held-out target in
`151 TH Prkcd Grin2c Glut` neurons. The manifest
`245_Trhr.csv` contains one target:

```tsv
target_name
Trhr
```

I interpreted `151 TH Prkcd Grin2c Glut` as the Allen-style thalamic
glutamatergic class described in the task, not as tyrosine-hydroxylase cells.
The input count table has 1,674 non-held-out training targets; its focal-cell
distribution is very zero-inflated, with median `n_degs = 0`, 469/1674 targets
nonzero, 75th percentile 1, and 95th percentile 18. Thus a one-gene or zero
prediction is the calibrated default for isolated receptor perturbations unless
the held-out biology matches a measured high-yield module.

The held-out `Trhr` perturbation itself was absent from both the training
Parquet as a `gene_target` and the focal training count CSV, as expected. It
also had no target-centered Finding in the filtered Distributed Agents corpus view, so
the prediction had to be transferred from other measured receptor and
second-messenger perturbations.

## Sources used

- `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
  for exact observed `n_degs` values in the focal cell group.
- `[local file: training_de_all_cell_groups.parquet]`
  for focal-cell Wilcoxon statistics, FDR calls, matched perturbed/control
  nucleus counts, and top rows for mechanistic comparator targets.
- Distributed Agents same-experiment corpus
  `perturbai-july-260713-sourceguard-1773-v1` for curated claims and Findings
  describing measured Gq/PLC, serotonergic, NPY, endocrine GPCR, cAMP, and
  receptor-family perturbation surfaces in the same Perturb-seq experiment.
- Distributed Agents runtime focal-profile comparison for a compact check that measured
  GPCR and second-messenger analogs are near-null and do not form a coherent
  multi-gene focal module: all inspected core analogs had
  `significant_feature_count = 0`; pairwise Pearson/cosine values among
  representative null GPCRs and effectors were near zero, e.g. `Plcb1` versus
  `Adcy3` Pearson -0.0309 and `Htr2c` versus `Adcy3` Pearson 0.0162.
- PubMed literature for TRHR biology: TRHR is a GPCR that signals mainly
  through Gq/11, PLC, Ca2+, and PKC and is regulated by rapid arrestin-mediated
  desensitization/internalization (Hinkle, Gehret, and Jones 2012,
  DOI: 10.3389/fnins.2012.00180, PMID: 23248581; Trubacova, Drastichova, and
  Novotny 2022, DOI: 10.3389/fcell.2022.981452, PMID: 36147745). Gq-family
  coupling is required for TRHR calcium signaling in a mouse Gq/G11-deficient
  cell system (Yu and Hinkle 1999, DOI: 10.1074/jbc.274.22.15745,
  PMID: 10336475). Rat brain in situ hybridization showed anatomically
  selective, not pan-neuronal, TRHR mRNA expression (Calza et al. 1992,
  DOI: 10.1016/0306-4522(92)90528-a, PMID: 1488129). Mouse TRH-R1 mediates most
  whole-brain TRH analog binding and behavioral TRH analog effects
  (Thirunarayanan et al. 2012, DOI: 10.1038/npp.2012.256, PMID: 23303050);
  germline Trh-r1 loss affects the hypothalamic-pituitary-thyroid axis and
  affective behavior (Zeng et al. 2007, DOI: 10.1210/me.2007-0048,
  PMID: 17666589).

## Computations over the supplied tables

I used the focal training count CSV to get exact endpoint values for candidate
analogs. I then filtered the Parquet to the focal cell group and a set of
literature-obvious GPCR and second-messenger comparators:

```python
ds.dataset(parquet).to_table(
    columns=["names", "gene_target", "scores", "logfoldchanges",
             "pvals_adj", "n_pert_matched", "n_ctrl_matched"],
    filter=(
        (pc.field("group_name") == "151 TH Prkcd Grin2c Glut")
        & pc.field("gene_target").isin(analogs)
    ),
)
```

For each comparator I counted focal genes with `pvals_adj < 0.05`, checked
whether any significant rows were only self-transcript reductions, and inspected
the smallest FDR and top absolute Wilcoxon scores. This distinguished true
multi-gene focal responses from effectively flat profiles.

## Target-specific reasoning

### `Trhr`

`Trhr` encodes the thyrotropin-releasing hormone receptor, a peptide GPCR whose
canonical signaling goes primarily through Gq/11 to PLC beta, IP3/Ca2+, DAG/PKC,
and in some contexts ERK or arrestin-dependent arms. That made the measured
Gq/PLC receptor set more relevant than broad endocrine transcription factors or
thyroid-hormone nuclear receptors.

The closest pathway analog in the training set was `Plcb1`, the PLC beta node
immediately downstream of many Gq-coupled receptors. In the focal group,
`Plcb1` had 160 matched perturbed nuclei, 23,679 matched controls, and
`n_degs = 0`; its most extreme focal row still had `pvals_adj = 1`. The
same-experiment corpus reports a high-confidence direct negative Finding:
`Plcb1` produced no robust downstream response in any recovered neuronal group,
0/22 groups at FDR 0.10 after excluding Plcb1 itself. It also records that the
expected activity-response panel, including `Arc`, `Fos/Fosb`, `Jun/Junb/Jund`,
`Egr1-4`, `Npas4`, `Nr4a1/2`, `Homer1`, `Bdnf`, `Rgs2/4`, and `Dusp1/6`,
stayed absent after `Plcb1` perturbation. That is an important counterexample:
even a core Gq/PLC effector with known neuronal excitability biology did not
leave a durable basal nuclear-RNA state in this assay.

Other directly measured Gq/PLC receptors in the focal group were similarly
flat. `Chrm3`, a Gq-coupled muscarinic receptor, had `n_degs = 0`; `Grm5`, a
group-I metabotropic glutamate receptor, had `n_degs = 0`; `Htr2a`, `Htr2b`,
and `Htr2c`, the closest represented 5-HT2 Gq branch, each had `n_degs = 0`;
and `Kiss1r`, another peptide Gq receptor, had `n_degs = 0`. The Distributed Agents
corpus summarized these observations as a moderate-confidence claim that
single-gene perturbations of represented neuromodulatory GPCR receptors and
proximal second-messenger effectors generally fail to produce a shared basal
neuronal nuclear-transcriptome module. The Plcb1-centered Finding specifically
compared `Chrm3`, `Grm1`, `Grm5`, `Htr2a`, `Htr2b`, `Htr2c`, `Itpr1`, `Prkca`,
and `Prkcg` and found shared absence or only isolated one-gene effects rather
than a hidden Gq/PLC RNA module.

The focal group also did not show a broad response after loss of downstream
calcium/PKC nodes: `Itpr1` had `n_degs = 0`, `Prkca` had `0`, and `Prkcg` had
`1`, with the only significant `Prkcg` row being the `Prkcg` self transcript.
`Grm1` also had `n_degs = 1`, again the perturbed transcript itself, not a
downstream module. I therefore treated `Grm1` and `Prkcg` as weak self-row
counterexamples, not evidence for a Trhr-regulated multi-gene state.

Broader neuropeptide GPCRs supplied a negative calibration set. In the focal
training endpoint, `Agtr1a`, `Agtr2`, `Cckar`, `Cckbr`, `Crhr1`, `Galr1`,
`Gnrhr`, `Npy1r`, `Npy2r`, `Npy5r`, `Ntsr1`, and `Tacr3` all had
`n_degs = 0`. The corpus similarly reports that single loss of represented NPY
receptors is buffered in basal neuronal snRNA-seq, that serotonin-receptor
responses are receptor- and cell-context-specific rather than shared
G-protein outputs, and that the canonical neuronal/pituitary GnRHR endocrine
program was absent after basal postnatal neuronal `Gnrhr` perturbation.
These are imperfect mechanistic analogs because their ligand, anatomical
source, and G-protein coupling differ from TRHR, but as a group they show that
this assay rarely converts isolated loss of a ligand-gated peptide receptor
into a stable thalamic DEG burden.

The cAMP side of GPCR signaling was also largely silent in the focal group:
`Adcy1`, `Adcy3`, `Adcy5`, `Gnal`, `Gnas`, `Pde1c`, `Pde4b`, `Pde4d`, and
`Pde10a` all had `n_degs = 0`; `Gnao1`, `Prkaca`, and `Prkar1a` had
`n_degs = 1` each. This is not the direct biochemical path for TRHR, but it is
a useful assay-level boundary. A high-confidence Distributed Agents claim states that
represented dopamine/GPCR and cAMP-pathway perturbations do not collapse into
one shared durable basal neuronal mRNA module; individual adenylyl cyclases and
Gs/Golf nodes were flat or nonconvergent even when downstream CREB responses
were detectable for other perturbations.

I also considered `Tshr` because its name is easy to confuse with `Trhr` and
because it is an endocrine GPCR in the thyroid axis. It is not a close paralog:
TSHR is a glycoprotein-hormone receptor activated by TSH, while TRHR is the
receptor for hypothalamic TRH. Still, the measured `Tshr` perturbation was a
useful negative control for a hormone GPCR: in the focal class `Tshr` had
`n_degs = 0`, and the corpus reports only three isolated singleton FDR 0.10
genes over its whole neuronal surface, not a shared basal glycoprotein-hormone
receptor transcriptional program with `Fshr` or `Lhcgr`.

Putting these together, the strongest within-dataset evidence points to no
FDR 0.05 gene in the focal `Trhr` knockout. The exact analogs are not positive
signature neighbors; they are a repeated null class. External TRHR biology
argues for an evoked second-messenger and electrophysiologic response, with
rapid receptor desensitization, rather than a constitutive broad mRNA program
3-4 weeks after sparse CRISPR loss in recovered NeuN-positive thalamic nuclei.
I therefore predicted zero rather than one or a small positive count.

## Limits

This is an extrapolation from pathway and receptor-class behavior, because the
held-out `Trhr` signature and count are deliberately absent. TRHR itself could
be more highly expressed or more tonically engaged in a subset of
`151 TH Prkcd Grin2c Glut` nuclei than the assayed Gq receptors, and the focal
broad class could hide a small responsive anatomical subpopulation. Conversely,
if `Trhr` target RNA were efficiently degraded after editing, the endpoint
might contain a self-transcript-only call even without any downstream response.
The assay does not measure receptor occupancy, TRH tone, PIP2/DAG/IP3, calcium,
PKC, ERK phosphorylation, firing, or arrestin trafficking, so a predicted
zero means only no measured gene is expected to pass the single-nucleus
Wilcoxon FDR threshold in this endpoint.

## Final point

`Trhr`: predicted `n_degs = 0`.
