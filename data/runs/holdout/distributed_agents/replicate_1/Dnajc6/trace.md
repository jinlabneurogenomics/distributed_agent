# Question and endpoint

I predicted the held-out `151 TH Prkcd Grin2c Glut` DEG-count endpoint for one
requested perturbation, `Dnajc6`.  The requested integer is the count of measured
genes with Scanpy Wilcoxon Benjamini-Hochberg `pvals_adj < 0.05` in the focal
thalamic glutamatergic class after sparse postnatal AAV-CRISPR loss of
function.  I treated this as an assay- and power-dependent nuclear RNA breadth
endpoint, not as a direct score for synaptic vesicle recycling, editing
efficiency, or neuronal survival.

The requested `Dnajc6` perturbation itself is held out: it is absent from the
training DEG-count CSV and absent as a `gene_target` in the differential-
expression Parquet.  Counts in the supplied training endpoint include the
perturbed transcript itself if that transcript passes FDR; therefore a
prediction of 1 DEG can mean "detectable target-RNA reduction but no downstream
program".

# Sources used

- Declared Perturb-seq training inputs:
  - `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`
  - `training differential-expression dataset`
- Run-local requested-target manifest:
  - `single-target request for Dnajc6`
- Run-local Distributed Agents dataset portrait, task bindings, measurement registry,
  corpus coverage, and capability manifest.
- Internal same-experiment semantic corpus:
  `perturbai-july-260713-sourceguard-1773-v1`, July atomic Finding/Claim
  projection.  The corpus had no explicit `Dnajc6` Finding in this release, so I
  used it only to interpret measured training perturbations such as `Dnajc5`,
  `Dnm1`, `Synj1`, `Hspa8`, `Cltc`, and `Vps35`.
- External mechanism sources:
  - UniProtKB mouse `Dnajc6` entry `Q80TZ3`, with GO terms for clathrin coat
    disassembly, clathrin-dependent endocytosis, synaptic vesicle recycling, and
    synaptic vesicle uncoating.
  - Reactome Content Service, queried for mouse `DNAJC6`, which places DNAJC6 in
    a `GAK,DNAJC6` cytosolic set.
  - Morgan et al. 2001, Neuron, DOI `10.1016/s0896-6273(01)00467-6`,
    PMID `11683998`: Hsc70 and auxilin are required for clathrin-coated vesicle
    uncoating at presynaptic terminals.
  - Yim et al. 2010, PNAS, DOI `10.1073/pnas.1000738107`,
    PMID `20160091`: auxilin knockout mouse synapses accumulate clathrin-coated
    vesicles/cages and have impaired clathrin-mediated synaptic-vesicle
    endocytosis, with partial compensation by GAK up-regulation.
  - Hayashi et al. 2008, PNAS, DOI `10.1073/pnas.0712171105`,
    PMID `18250322`: Dnm1-null and Synj1-null synapses both accumulate clathrin-
    coated endocytic intermediates in activity- and synapse-dependent ways.
  - Gorenberg and Chandra 2017, Frontiers in Neuroscience,
    DOI `10.3389/fnins.2017.00248`, PMID `28579939`: DNAJC5, DNAJC6, and
    DNAJC13 are specialized synaptic/endosomal Hsp40 co-chaperones that all
    work with Hsc70 but have different clients and compartments.
  - McMahon and Boucrot 2011, Nature Reviews Molecular Cell Biology,
    DOI `10.1038/nrm3151`, PMID `21779028`: clathrin-mediated endocytosis uses
    modular initiation, adaptor, coat, scission, and Hsc70/auxilin uncoating
    steps.
  - Edvardson et al. 2012, PLoS ONE, DOI `10.1371/journal.pone.0036458`,
    PMID `22563501`; Ng et al. 2020, Movement Disorders,
    DOI `10.1002/mds.28063`, PMID `32472658`; Vidyadhara et al. 2023, Cell
    Reports, DOI `10.1016/j.celrep.2023.112231`, PMID `36920906`; Abela et al.
    2024, Brain, DOI `10.1093/brain/awae020`, PMID `38242634`: recessive
    DNAJC6 loss causes auxilin deficiency with synaptic vesicle recycling or
    dopamine-homeostasis defects in patient and mouse models.

# Quantitative checks

The focal training endpoint is highly zero-inflated.  Among 1,674 non-held-out
training perturbations, 71.98% had `n_degs = 0`, the median was 0, the 75th
percentile was 1, and the 95th percentile was 18.  Thus any prediction of a
multi-gene response needs target-specific evidence.

I queried the Parquet only for `group_name = '151 TH Prkcd Grin2c Glut'` and
for biologically plausible endocytic, Hsp40/Hsc70, retromer, and Parkinson
counterexample targets:

```sql
select gene_target,
       sum(pvals_adj < 0.05) as fdr05,
       sum(pvals_adj < 0.05 and names <> gene_target) as downstream_fdr05,
       max(case when names = gene_target then logfoldchanges end) as self_lfc,
       max(case when names = gene_target then pvals_adj end) as self_q
from read_parquet($declared_parquet)
where group_name = '151 TH Prkcd Grin2c Glut'
  and gene_target in (...)
group by gene_target;
```

The informative focal-cell counts were:

| training perturbation | `n_degs` | downstream FDR<0.05 genes in 151 | why it is relevant |
| --- | ---: | ---: | --- |
| `Synj1` | 1 | 0 | PI(4,5)P2/Sac phosphatase in synaptic vesicle uncoating after fission |
| `Dnm1` | 1 | 0 | neuronal dynamin GTPase for vesicle fission, immediately upstream of uncoating |
| `Dnajc5` | 1 | 0 | synaptic Hsp40/Hsc70 co-chaperone; client/compartment-specific comparator |
| `Dnajc13` | 1 | 0 | endosomal J-domain Hsc70 co-chaperone comparator |
| `Atp13a2` | 1 | 0 | PD/endolysosomal counterexample, not a clathrin-uncoating enzyme |
| `Park7` | 1 | 0 | PD counterexample with a different oxidative-stress mechanism |
| `Cltc` | 3 | 3 | core clathrin heavy chain, an upstream coat component used broadly |
| `Hspa8` | 9 | 9 | Hsc70 partner of auxilin and many other chaperone systems |
| `Vps35` | 17 | 16 | retromer cargo-recycling component, endosomal but not a presynaptic coat-uncoating factor |
| `Vps54` | 31 | 31 | GARP tether, Golgi/endosome trafficking counterexample |
| `Rab7` | 501 | 500 | late-endosomal Rab, a broad lysosome/proteostasis response outlier |

Exact AP-2 subunits, `Picalm`, `Gak`, `Clta`, `Cltb`, and `Sh3gl2` were absent
from the focal training-count CSV, so I did not impute from unobserved training
endpoints.  `Stxbp1`, `Nsf`, and `Vamp1` were present but are exocytic release
genes rather than auxilin-like clathrin-uncoating genes; their focal counts were
low (`Stxbp1 = 1`, `Nsf = 0`, `Vamp1 = 1`) and were used only as weak
background against a large vesicle-cycle response.

The actual 151 FDR rows further separated self-transcript signals from
downstream programs:

- `Synj1`: only `Synj1` itself, log2FC -0.58, q = `3.1e-7`.
- `Dnm1`: only `Dnm1` itself, log2FC -0.71, q = `4.1e-25`.
- `Dnajc5`: only `Dnajc5` itself, log2FC -0.48, q = `0.010`.
- `Dnajc13`: only `Dnajc13` itself, log2FC -0.45, q = `0.0046`.
- `Hspa8`: `Dnaja1`, `Hspa4l`, `Syt4`, `Hsp90aa1`, `Cct6a`, and four smaller
  hits; this is an Hsp70/HSF-like counterinduction program, not a clathrin
  uncoating signature.
- `Cltc`: three downstream hits, `Ero1b`, `Gabra4`, and `Rbms1`, at q = 0.042.
- `Vps35`: 17 hits including the self transcript and downstream `Atp2a2`,
  `Brsk1`, `Grin2b`, `Ccdc136`, `Rims3`, `Plekhg1`, and `Kcnc2`.
- `Rab7`: 501 hits led by V-ATPase, endolysosomal, cholesterol, stress, and
  proteostasis genes, too broad and too far downstream for direct transfer to
  auxilin.

Focal-cell Pearson/Spearman score correlations among these analog signatures
were near zero for `Synj1`, `Dnm1`, and `Dnajc5`, while `Cltc`, `Hspa8`,
`Vps35`, and `Rab7` had only weak relationships to each other.  For example,
Pearson correlations in 151 were `Synj1` versus `Dnm1` = 0.019, `Synj1` versus
`Dnajc5` = -0.013, `Dnajc5` versus `Dnajc13` = 0.103, `Hspa8` versus `Cltc` =
0.169, and `Rab7` versus `Vps35` = 0.143.  This made a broad shared signature a
poor quantitative basis for `Dnajc6`; the count estimate should come from the
observed sparsity of the intervention-level analogs rather than from a generic
endolysosomal response.

# Target-specific prediction

## `Dnajc6`: predicted 1 DEG

`Dnajc6` encodes auxilin, a neuronal J-domain co-chaperone that recruits
HSPA8/Hsc70 to clathrin-coated vesicles and uncoats them after endocytosis.
The causal chain I used was:

1. sparse CRISPR loss of `Dnajc6`
2. reduced auxilin function at presynaptic clathrin-coated vesicles
3. less efficient Hsc70-dependent uncoating and vesicle recycling, partly
   buffered by GAK and other endocytic mechanisms
4. possible altered synaptic vesicle availability or dopamine-terminal stress
   in susceptible contexts
5. survivor-conditioned nuclear RNA measured 3 to 4 weeks later in a thalamic
   glutamatergic class

The first three steps are well supported by UniProtKB/GO, Reactome, Morgan
2001, Yim 2010, and Gorenberg and Chandra 2017.  The important point for this
prediction is that the step from vesicle-uncoating physiology to a broad basal
nuclear DEG response is weak in the supplied screen.  The closest measured
interventions at the same synaptic vesicle endocytosis layer, `Synj1` and
`Dnm1`, had one DEG each in 151 and no downstream FDR<0.05 genes.  The closest
measured Hsp40 co-chaperones, `Dnajc5` and `Dnajc13`, also had one DEG each,
again only the self transcript.  Those four perturbations argue that acute,
sparse CRISPR disruption of specialized presynaptic uncoating/co-chaperone
machinery is usually visible, if at all, as self-RNA loss rather than as a
large secondary state in this focal thalamic class.

`Hspa8` is an obligate auxilin partner but a counterexample rather than a direct
count donor: auxilin loss removes a co-chaperone that brings Hsc70 to clathrin
cages, whereas `Hspa8` loss perturbs the constitutive chaperone used by many
cytosolic clients.  Its nine DEGs in 151 were led by `Dnaja1`, `Hspa4l`,
`Hsp90aa1`, and `Cct6a`, consistent with chaperone counterinduction.  I
therefore treated the HSPA8 signal as evidence that the assay can see Hsc70
stress, but not as evidence that `Dnajc6` itself should induce nine genes.

`Cltc` and `Vps35` bound the high side.  `Cltc` acts upstream as the heavy-chain
coat for multiple clathrin-dependent routes, not only presynaptic uncoating, and
produced only three focal DEGs despite that central role.  `Vps35` and `Rab7`
operate in late endosomal/retromer cargo traffic, where the 151 responses
included receptor, lysosomal, cholesterol, and proteostasis genes absent from
`Synj1`/`Dnm1`/`Dnajc5`; those signatures made a broad endolysosomal estimate
inappropriate for `Dnajc6`.

I predicted a nonzero but minimal count, `1`, because `Dnajc6` is a neuronal
gene in a pathway whose similarly specialized training members often reached
the FDR gate only through their own perturbed transcript.  I did not predict a
larger count because the biologically closest downstream analogs gave no
downstream 151 hits, and because the external literature for auxilin mainly
establishes clathrin-coated vesicle accumulation, synaptic vesicle recycling
defects, and dopaminergic vulnerability, none of which guarantees a broad
steady-state snRNA-seq response in surviving juvenile thalamic glutamatergic
neurons.

# Limits and uncertainty

- `Dnajc6` itself was not measured as a perturbation, and exact targets such as
  `Gak`, AP-2, `Picalm`, `Clta`, `Cltb`, and `Sh3gl2` were absent from the
  training endpoint.  The prediction therefore extrapolates from adjacent
  synaptic vesicle and Hsp40/Hsc70 perturbations.
- The expected direct phenotype is protein- and membrane-level clathrin-coated
  vesicle uncoating.  The supplied endpoint is nuclear RNA after recovery and
  multiple-testing thresholding, so the endpoint can stay at one or zero even
  if auxilin function is impaired.
- Complete auxilin knockout mice, human recessive DNAJC6 disease, and
  iPSC-derived midbrain dopaminergic models involve different dosage, time,
  cell-type exposure, and in some cases degeneration.  They support the
  direction of the molecular lesion but do not imply a large 151 TH DEG count.
- A prediction of `1` relies partly on self-transcript behavior in analogous
  genes.  The dataset portrait warns that self-target RNA is not an editing
  efficiency readout; I used it only because the required endpoint counts any
  measured transcript below FDR 0.05, including the target transcript itself.
- The difference between `0` and `1` DEG is within the noise of guide
  performance, expression level, and FDR thresholding.  The robust conclusion is
  that `Dnajc6` should be near the sparse end of the training distribution, not
  near the retromer or late-endosomal outliers.
