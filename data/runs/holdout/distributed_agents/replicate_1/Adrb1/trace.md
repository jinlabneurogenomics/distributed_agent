# Held-out DEG-count prediction trace

## Question and endpoint

I interpreted the task as a point prediction of the held-out focal-cell endpoint

`n_degs = count(measured genes with Wilcoxon BH-adjusted p < 0.05)`

for each requested genetic perturbation in `151 TH Prkcd Grin2c Glut` neurons. The requested-target manifest contained one target, `Adrb1`, and the target order was therefore just:

1. `Adrb1`

The prediction is for acute sparse AAV-CRISPR loss of function delivered at P16 and read out by basal snRNA-seq at P37-P44. I did not treat germline knockout, pharmacologic agonism/antagonism, receptor desensitization assays, or evoked electrophysiology as measurements of this endpoint. Those sources were used only to decide which visible perturbations are mechanistically appropriate analogs.

## Sources used

- Direct training endpoint: `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Direct differential-expression rows: `training differential-expression dataset`.
- Run-local held-out manifest: `single-target request for Adrb1`.
- Run-local dataset portrait, task bindings, measurement registry, coverage summary, and capability manifest.
- Same-experiment semantic corpus: `perturbai-july-260713-sourceguard-1773-v1`; I queried the July Findings/graph layer only for visible analogs, not for `Adrb1`, which was held out from the input experiment.
- External mechanism priors from PubMed-indexed literature:
  - Meitzen, Luoma, Stern and Mermelstein 2011, J Neurochem, DOI `10.1111/j.1471-4159.2010.07137.x`, PMID `21143600`: beta1 adrenergic receptor activation in cultured striatal neurons can stimulate cAMP production and also receptor-tyrosine-kinase/Ras/Raf/MEK/MAPK/MSK signaling leading to CREB phosphorylation, CRE-dependent transcription, and increased `c-fos`.
  - Wallukat 2002, Herz, DOI `10.1007/s00059-002-2434-z`, PMID `12439640`: beta-adrenergic receptors are GPCRs that signal through the adenylyl-cyclase/cAMP/PKA cascade after catecholamine stimulation.
  - Fu, Kim, Soto et al. 2014, J Biol Chem, DOI `10.1074/jbc.M113.542589`, PMID `24713698`: beta1AR stimulation can sustain cAMP/PKA signaling under prolonged agonist exposure and is regulated by receptor-associated PDE4D8.

## Computations over the training data

I first loaded the requested-target CSV and confirmed that it contained exactly one value, `Adrb1`. I then checked the direct endpoint CSV:

- 1,674 visible training perturbations in the focal cell group.
- 1,205/1,674 had `n_degs = 0`; the median was `0`.
- 276 had `n_degs = 1`; the focal-cell endpoint is therefore heavily concentrated at no BH-significant response.
- `Adrb1` was absent from this training count table.

I used DuckDB scans over the focal-cell rows of the Parquet to compute, for mechanistic analogs, the exact number of FDR<0.05 genes, the best adjusted p value, and the matched perturbed/control nucleus counts in `151 TH Prkcd Grin2c Glut`. For example, the query grouped by `gene_target` after filtering `group_name = '151 TH Prkcd Grin2c Glut'` and `gene_target in (...)`, then counted `pvals_adj < 0.05` and summarized `min(pvals_adj)`. I separately confirmed that `Adrb1` had zero Parquet rows as a `gene_target`, while its transcript was among the measured `names` rows in other perturbation contrasts; the held-out target is absent as an intervention, not absent from the feature space.

## Within-dataset analogs

The closest focal-cell analogs were the other beta-adrenergic receptors:

| target | focal `n_degs` | perturbed nuclei | best focal FDR | expression-pattern evidence |
|---|---:|---:|---:|---|
| `Adrb2` | 0 | 252 | 0.551 | no BH-significant focal genes; no `Arc`/`Bdnf`/`Crem`/`Egr1`/`Fos`/`Jun`/`Npas4`/`Nr4a1` CREB or immediate-early program across Adrb2 groups in the July corpus |
| `Adrb3` | 0 | 274 | 1.000 | no BH-significant focal genes and pan-neuronal downstream null in the July corpus |

These two are the most informative paralog controls for `Adrb1`: all three receptors are catecholamine-activated beta-adrenergic GPCRs and use cAMP-linked signaling, so sparse loss of `Adrb1` in basal neurons should most resemble loss of a ligand-gated beta receptor rather than loss of a chromatin regulator or core proteostasis factor. `Adrb2` and `Adrb3` were also well powered in the focal group, with more perturbed nuclei than many nonzero training perturbations, so their focal zeros were not low-cell-count edge cases.

I then used visible adrenergic and cAMP-pathway perturbations as counterexamples to the simple model that any receptor or cAMP perturbation creates a focal transcriptional state:

| target | focal `n_degs` | perturbed nuclei | best focal FDR | rationale |
|---|---:|---:|---:|---|
| `Adra1a` | 0 | 154 | 1.000 | alpha-adrenergic GPCR comparator; July corpus found no meaningful neuronal basal transcriptomic module |
| `Adra2a` | 0 | 168 | 1.000 | Gi/o-coupled adrenergic receptor; only sparse interneuron hits elsewhere, not a focal TH response |
| `Adra2b` | 0 | 196 | 1.000 | Gi/o-coupled adrenergic receptor; one-gene effect elsewhere, no focal TH response |
| `Gnas` | 0 | 306 | 1.000 | proximal Gs alpha transducer for beta-receptor-to-cAMP signaling; no focal effect |
| `Adcy1` | 0 | 88 | 0.139 | membrane adenylyl cyclase downstream of Gs and calcium; no focal effect |
| `Adcy3` | 0 | 223 | 0.112 | membrane/ciliary adenylyl cyclase; no focal effect |
| `Adcy5` | 0 | 154 | 0.912 | membrane adenylyl cyclase; no focal effect |
| `Prkaca` | 1 | 192 | `7.9e-22` | PKA catalytic subunit; the sole focal call was the self-transcript `Prkaca`, so it did not yield a broad downstream cAMP/CREB state |
| `Prkar1a` | 1 | 98 | `1.4e-03` | PKA regulatory subunit; the sole focal call was the self-transcript `Prkar1a` |
| `Creb1` | 10 | 126 | `3.8e-07` | direct nuclear CREB-family perturbation did produce a small `Crem`-centered response |
| `Crebbp` | 8 | 61 | `5.0e-04` | direct CREB coactivator/chromatin perturbation produced a small focal response |

The strongest counterexample is `Creb1`: the same dataset could detect a CREB-family transcriptional response when the nuclear effector was perturbed directly. In contrast, the beta receptors, `Gnas`, `Adcy1/3/5`, and the nearest PKA components were silent, self-only, or isolated singletons in the focal endpoint. The July corpus independently summarized the same pattern as pathway uncoupling for `Adrb2`, `Adrb3`, `Gnas`, `Adcy1`, `Adcy3`, `Adcy5`, and `Prkaca`: ligand-receptor and proximal second-messenger perturbations did not phenocopy the small `Creb1`/`Crebbp` nuclear responses.

## Target-specific prediction

### `Adrb1`

`Adrb1` encodes beta1 adrenergic receptor, a catecholamine GPCR whose activated state signals through Gs/cAMP/PKA and, in neurons, can activate CREB and `c-fos` through both cAMP production and a Ras/MAPK/MSK branch. That mechanism makes `Adrb2`, `Adrb3`, `Gnas`, `Adcy1/3/5`, `Prkaca`, and `Creb1` the relevant visible training set.

The causal transfer chain I used was:

`Adrb1` loss -> reduced beta1AR responsiveness to norepinephrine/epinephrine -> altered cAMP/PKA or MAPK/MSK/CREB propagation only when that receptor is occupied or tonically active -> possible CREB/immediate-early gene changes in exposed recovered neurons -> focal-cell Wilcoxon/BH DEG count.

The weak link is not the receptor-to-effector biochemistry; beta1AR can clearly drive cAMP and CREB in stimulated neurons. The weak link is the exposure and endpoint stage. The screen read basal recovered nuclei after sparse P16 loss, with no synchronized adrenergic agonist, behavioral stimulation, electrophysiology, or inflammatory challenge. In the same assay, deleting two other beta receptors left `151 TH Prkcd Grin2c Glut` at `0` DEGs, deleting the shared Gs transducer `Gnas` also left it at `0`, and deleting three single adenylyl-cyclase genes left it at `0`. The focal `Adrb2` perturbation also did not show even a borderline CREB/immediate-early sentinel pattern: its best adjusted p value in the focal cell group was 0.551.

I therefore predict a true endpoint zero rather than a small positive count. `Adrb1` could still change evoked cAMP, synaptic integration, CREB phosphorylation minutes after norepinephrine, or glial/circuit states outside the NeuN-enriched basal assay, but those are not well captured by a 3 to 4 week resting nuclear RNA Wilcoxon count. The only positive analogs, direct `Creb1` and `Crebbp`, sit downstream at the transcriptional layer and are not close enough to override the receptor/proximal-cAMP zeros.

Final point estimate: `Adrb1 = 0` FDR<0.05 DEGs.

## Limits

The requested `Adrb1` perturbation and its expression signature were completely absent from the declared inputs, so this is a transfer prediction from paralogs and pathway neighbors rather than a direct measurement. No visible same-experiment `Adrb1` report was available. The closest paralog, `Adrb2`, can couple differently from `Adrb1`, and none of `Adrb2`, `Adrb3`, `Gnas`, `Adcy1`, `Adcy3`, or `Adcy5` proves that focal thalamic beta1AR is inactive. The prediction is specifically that acute sparse `Adrb1` loss will not create enough durable, cell-autonomous basal nuclear RNA shift to pass BH FDR 0.05 in this assay; it is not a prediction of absent adrenergic physiology.
