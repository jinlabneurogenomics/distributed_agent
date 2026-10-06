# Question and interpretation

The task is to predict, for each target in `005_Adrb1.csv`, how many measured
genes will have `pvals_adj < 0.05` in `151 TH Prkcd Grin2c Glut` after the
held-out acute sparse CRISPR loss-of-function perturbation.

The manifest contains one held-out target:

| target_name |
|---|
| Adrb1 |

I treated the requested endpoint as the integer count in the held-out
differential-expression table for the focal cell group, not as a count of genes
expected from a germline knockout, a beta-adrenergic agonist, a pharmacologic
antagonist, or any non-neuronal experiment. I also treated target-transcript
changes as QC context only: in this AAV-PHP.eB Perturb-seq experiment, weak
self-mRNA depletion is not a failed-edit call and strong self-mRNA depletion is
not a quantitative predictor of a larger downstream signature.

# Sources used

- Primary input: `[local file: training_de_all_cell_groups.parquet]`.
- Primary input endpoint table:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Requested-target manifest:
  `[local file: 005_Adrb1.csv]`.
- Same-experiment Distributed Agents corpus
  `perturbai-july-260713-sourceguard-1773-v1`, especially interpreted
  findings for `Adrb2`, `Adrb3`, `Gnas`, `Adcy1`, `Adcy5`, `Prkaca`,
  `Prkar1a`, and `Creb1`.
- PubMed literature for the external biology of beta-1 adrenergic receptor
  signaling and neuronal beta-adrenergic/cAMP/CREB signaling.

External facts used only as priors:

- `Adrb1` encodes the beta-1 adrenergic receptor, a catecholamine GPCR in the
  adrenoceptor family. Human beta-1 adrenergic receptor couples to the
  heterotrimeric Gs protein in structural/biochemical reconstitution assays
  and can drive adenylyl cyclase/cAMP signaling (Kock et al., 2022,
  DOI:10.1016/j.jmb.2022.167687; Merino et al., 2025,
  DOI:10.1016/j.str.2025.07.020).
- In cultured striatal neurons, beta-1 adrenergic stimulation can raise cAMP
  and, through a distinct receptor-tyrosine-kinase/Ras/Raf/MEK/MAPK/MSK branch,
  rapidly phosphorylate CREB, activate CRE-dependent transcription, and
  increase `c-fos` expression (Meitzen et al., 2011,
  DOI:10.1111/j.1471-4159.2010.07137.x).
- `Adrb1` has CNS functions outside purely cardiac biology: for example,
  amygdala `Adrb1` was validated as a direct miR-19b target whose reduction
  after chronic social defeat changed fear-conditioning and noradrenergic
  measures (Volk et al., 2014, DOI:10.1523/JNEUROSCI.0855-14.2014).
- CREB/CREM are a canonical transcriptional output of cAMP signaling
  (Sassone-Corsi, 1998, PMID:9597751), making `Creb1` and especially `Crem`
  useful internal sentinels for a propagated cAMP transcriptional response.

# Computations over the training data

I first read the focal training-count CSV. It contains 1,674 non-held-out
perturbations for `151 TH Prkcd Grin2c Glut`; 1,205 of them have zero DEGs at
BH-adjusted Wilcoxon `pvals_adj < 0.05`, and 1,480 have one or zero DEGs. The
distribution is therefore highly zero-inflated and a GPCR target needs direct
same-pathway evidence before assigning a positive count.

I then queried the Parquet with `pyarrow.dataset`, filtering rows to
`group_name == "151 TH Prkcd Grin2c Glut"` and to mechanistically relevant
training perturbations. For each selected training target I counted focal rows
with `pvals_adj < 0.05` and inspected both the lowest adjusted p-values and
canonical cAMP/immediate-early sentinels including `Crem`, `Fos`, `Fosb`,
`Jun`, `Arc`, `Npas4`, `Bdnf`, `Egr1`, `Nr4a1`, and `Scg2`.

The most relevant focal-cell counts were:

| training perturbation | matched perturbed nuclei | focal `n_degs` at FDR<0.05 | interpretation |
|---|---:|---:|---|
| `Adrb2` | 252 | 0 | direct beta-adrenergic paralog, no focal DEGs |
| `Adrb3` | 274 | 0 | direct beta-adrenergic paralog, no focal DEGs |
| `Adra1a` | 154 | 0 | adrenergic-family counterexample |
| `Adra2a` | 168 | 0 | adrenergic-family counterexample |
| `Adra2b` | 196 | 0 | adrenergic-family counterexample |
| `Gnas` | 306 | 0 | canonical Gs alpha node, no focal DEGs |
| `Adcy1` | 88 | 0 | adenylyl-cyclase comparator, no focal DEGs |
| `Adcy3` | 223 | 0 | adenylyl-cyclase comparator, no focal DEGs |
| `Adcy5` | 154 | 0 | adenylyl-cyclase comparator, no focal DEGs |
| `Pde10a` | checked | 0 | cAMP PDE comparator, no focal DEGs |
| `Pde1c` | checked | 0 | cAMP PDE comparator, no focal DEGs |
| `Pde4b` | checked | 0 | cAMP PDE comparator, no focal DEGs |
| `Pde4d` | checked | 0 | cAMP PDE comparator, no focal DEGs |
| `Prkaca` | 192 | 1 | the single focal hit was `Prkaca` itself |
| `Prkar1a` | 98 | 1 | the single focal hit was `Prkar1a` itself |
| `Creb1` | 126 | 10 | small positive control for the nuclear CREB node |

This comparison separates the upstream receptor/second-messenger layer from the
measurable transcription-factor layer. In the focal cell group, `Creb1`
perturbation robustly up-regulated `Crem` (`log2FC 1.092`, FDR
`3.816e-07`) and produced a 10-gene response, but `Adrb2`, `Adrb3`, `Gnas`,
`Adcy1`, `Adcy3`, `Adcy5`, and `Prkaca` all left `Crem`, `Fos`, `Arc`,
`Npas4`, `Bdnf`, `Egr1`, `Nr4a1`, and `Scg2` at FDR 1.0 in the same focal
class. The one-count `Prkaca` and `Prkar1a` rows were just their own
transcripts, not downstream cAMP/CREB responses.

I also confirmed that `Adrb1` is completely absent from the training count CSV
and has zero rows as a `gene_target` in the training Parquet.

# Same-experiment corpus evidence

The Distributed Agents corpus had no direct `Adrb1` finding, which is expected for this
held-out target. It did have interpreted same-experiment findings for the best
available analogs:

- `Adrb2:F001`: `Adrb2` was a complete basal neuronal transcriptomic null; all
  23 recovered cell groups had zero downstream genes at FDR<0.10.
- `Adrb2:F002`: expected CREB and immediate-early sentinels downstream of
  beta-adrenergic cAMP signaling were absent after `Adrb2` perturbation.
- `Adrb2:F003`: `Adrb3`, `Adcy1`, `Adcy3`, `Adcy5`, and `Prkaca` were flat
  alongside `Adrb2`; `Gnas` had only one isolated cortical `Snx29` hit; direct
  `Creb1` perturbation gave a small recurrent `Crem` response.
- `Adrb3:F001` and `Adrb3:F002`: `Adrb3` was pan-null across all 23 recovered
  neuronal groups and did not engage the canonical beta-adrenergic
  cAMP/PKA/thermogenic transcriptional chain. Corpus evidence explicitly notes
  that `Adrb1` was the untested beta paralog.
- `Gnas` findings: `Gnas` produced only a one-gene deep-layer cortical response
  across the atlas and did not induce the expected cAMP/CREB immediate-early
  module.
- `Adcy1`/`Adcy5` findings: represented membrane adenylyl-cyclase perturbations
  were family-wide buffered at the downstream RNA level.
- `Prkaca`/`Prkar1a` findings: the represented PKA catalytic and regulatory
  nodes were buffered at the downstream RNA level, even when own-transcript
  depletion was detectable.

The corpus reports most of these signatures at FDR<0.10 across all recovered
groups. Any all-zero FDR<0.10 surface is also zero at the task's stricter
FDR<0.05 cutoff.

# Target-specific reasoning

## `Adrb1`

**Appropriate analogs.** The closest measured perturbations are `Adrb2` and
`Adrb3`, the other beta-adrenergic receptor paralogs. Both are catecholamine
GPCRs that can stimulate cAMP through Gs-family signaling, and both were
training perturbations. In the focal group, `Adrb2` had 252 matched perturbed
nuclei and 0 DEGs; `Adrb3` had 274 matched perturbed nuclei and 0 DEGs. Their
focal signatures were not near threshold: the lowest `Adrb2` adjusted p-value
was 0.551 and all adjusted p-values in the `Adrb3` focal profile were 1.0.
The corpus further showed that `Adrb2` and `Adrb3` were downstream-null across
all 23 recovered neuronal groups at FDR<0.10, so the focal zero is part of an
atlas-wide receptor-level null rather than a one-cell-class accident.

`Adra1a`, `Adra2a`, and `Adra2b` are less direct because alpha-adrenergic
receptors have different G-protein coupling, but they test the broader idea
that removing a postsynaptic adrenergic receptor in this screen creates a
catecholamine response. Each had 0 focal DEGs. Other monoaminergic or
neuromodulatory GPCRs in the training count table were also mostly flat in the
focal class (`Drd2`, `Drd4`, `Drd5`, `Htr6`, `Chrm3`, `Grm5`, `Agtr1a`,
`Agtr2`, `Avpr1a`, `Avpr1b`, `Oxtr` all had 0; `Grm1` had 1), which keeps the
beta-receptor nulls from looking like an exception to a large GPCR response
class.

The downstream pathway tests make the beta-receptor comparison stronger.
`Gnas`, `Adcy1`, `Adcy3`, `Adcy5`, and the cAMP PDEs `Pde10a`, `Pde1c`,
`Pde4b`, and `Pde4d` all had zero focal DEGs. `Prkaca` and `Prkar1a` each had
one focal DEG, but the one was the perturbed gene itself, so neither knockout
propagated to `Crem` or an immediate-early module. Direct `Creb1` loss is an
important counterexample: it produced 10 focal DEGs, headed by `Crem`, so the
focal `151` group can report a CRE-family nuclear response when the
transcription factor itself is hit. The absence of that `Crem` response after
`Adrb2`, `Adrb3`, `Gnas`, `Adcy1`, `Adcy3`, `Adcy5`, and `Prkaca` argues that
the upstream beta/cAMP layer was uncoupled from basal nuclear RNA in this
experiment.

**External biology.** External literature would make `Adrb1` a plausible
upstream member of the beta-adrenergic/cAMP/CREB pathway rather than a random
GPCR: beta-1 adrenergic receptor engages Gs/cAMP biochemistry in human
reconstitution assays, and beta-1 stimulation can activate CREB and `c-fos` in
striatal neurons. That prior points to the exact comparators queried above:
`Adrb2`, `Adrb3`, `Gnas`, adenylyl cyclases, PKA, and `Creb1`/`Crem`.

**Zero/nonzero decision.** The within-dataset evidence is more relevant to this
readout than ligand-stimulation or chronic circuit literature. `Adrb1` is the
untested beta paralog, so there is residual subtype uncertainty, but every
measured beta receptor and proximal beta/cAMP transducer was transcriptionally
silent in the focal thalamic group. The best positive control is downstream
`Creb1`, and its 10-gene response was not approached by any receptor or
adenylyl-cyclase comparator. I therefore predict no FDR<0.05 genes for
`Adrb1`.

# Prediction

| target_name | predicted_n_degs |
|---|---:|
| Adrb1 | 0 |

# Limits and uncertainty

- `Adrb1` itself was held out, so the prediction is extrapolated from beta
  paralogs and downstream cAMP components rather than measured `Adrb1` rows.
- `Adrb1`, `Adrb2`, and `Adrb3` are not interchangeable. They differ in
  expression, localization, ligand sensitivity, desensitization, and in some
  contexts beta-1 receptor activation has signaling features that beta-2 or
  beta-3 do not. The prediction assumes those differences do not override the
  strong receptor/proximal-cAMP null surface in this basal focal-cell readout.
- The training Parquet gives differential-expression statistics, not raw
  baseline expression, receptor protein abundance, receptor occupancy, indel
  rates, phospho-CREB, cAMP, electrophysiology, or cell abundance.
- The assay was resting single-nucleus RNA-seq after postnatal sparse CRISPR
  editing. It did not stimulate norepinephrine release, impose fear learning,
  activate beta receptors pharmacologically, or assay rapid phospho-CREB.
- Whole brain minus hindbrain/olfactory bulb and NeuN+ sorting under-sample
  locus-coeruleus, peripheral, immune, vascular, and glial biology where beta
  adrenergic receptors may have stronger transcriptional outputs.
- The prediction is for the focal `151 TH Prkcd Grin2c Glut` adjusted
  Wilcoxon endpoint only. A zero here should not be read as no function for
  beta-1 adrenergic signaling in neurons.
