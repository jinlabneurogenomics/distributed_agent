# Question

The requested held-out target list contained one mouse perturbation, `Cc2d1a`.
I interpreted the task as a point prediction of the number of measured genes
with Wilcoxon Benjamini-Hochberg `pvals_adj < 0.05` in the focal
`151 TH Prkcd Grin2c Glut` class after acute sparse CRISPR loss of `Cc2d1a`.
The target itself was held out, so its own focal-cell DEG count and its
expression vector were absent from both visible input files.

The predicted endpoint is directly observed for the 1,674 visible training
perturbations in
`../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
The matching per-gene DE rows in
`training differential-expression dataset`
are direct expression-pattern evidence for those same training perturbations.
Neither file directly observes the requested held-out outcome for `Cc2d1a`.

# Sources Used

- The supplied focal-class training count CSV, used as the calibrated
  distribution of the `n_degs` endpoint among non-held-out perturbations.
- The supplied training DE Parquet, filtered to `151 TH Prkcd Grin2c Glut`
  equivalent rows with `group_name == "151 TH Prkcd Grin2c Glut"` for
  literature-relevant visible analogs and counterexamples.
- The run-local PerturbAI July 260713 sourceguard 1773 v1 same-experiment
  corpus reports for `Htr1a`, `Drd2`, `Deaf1`, and `Camk2b`. These reports are
  a packaged interpretation of the same experiment, not an independent
  replicate.
- PubMed-indexed external literature:
  Ou et al. 2003, `10.1523/JNEUROSCI.23-19-07415.2003` / PMID 12917378;
  Rogaeva and Albert 2007, `10.1111/j.1460-9568.2007.05727.x` /
  PMID 17714190; Hadjighassem et al. 2010,
  `10.1111/j.1460-9568.2010.07498.x` / PMID 21155902; Al-Tawashi et al. 2012,
  `10.1074/jbc.M111.261875` / PMID 22375002; Al-Tawashi and Gehring 2013,
  `10.1186/1478-811X-11-47` / PMID 23826796; Oaks et al. 2017,
  `10.1093/cercor/bhw009` / PMID 26826102; Vahid-Ansari et al. 2017,
  `10.1523/JNEUROSCI.1668-17.2017` / PMID 29101244; Yang et al. 2019,
  `10.1523/JNEUROSCI.2395-18.2019` / PMID 30992372; Kondaurova et al. 2021,
  `10.3390/ijms222413319` / PMID 34948116; Yang et al. 2021,
  `10.1007/s13311-021-01072-z` / PMID 34132974; Belokopytova et al. 2022,
  `10.1134/S0006297922100145` / PMID 36273889; Bhattacharya et al. 2024,
  `10.1093/hmg/ddae070` / PMID 38652285; Galaraga et al. 2024,
  `10.3390/ijms25116194` / PMID 38892382.

# Local Calibration

The focal training counts are very sparse. Among 1,674 visible biological
training perturbations, 1,205 had `n_degs == 0`, only 469 were nonzero, the
median was 0, the 75th percentile was 1, the 90th percentile was 2, the 95th
percentile was 18, and the upper tail was dominated by a small number of
global regulators such as `Uba5` with 2,677 DEGs, `Tpr` with 1,768, and `Sin3a`
with 1,433. I therefore used zero as the calibrated default for a target whose
closest visible mechanistic neighbors were also flat in this same cell class.

For visible analogs, I filtered the declared Parquet to the focal class and to
relevant `gene_target` values, then counted `pvals_adj < 0.05` genes and
inspected the FDR-supported rows. The close CC2D1A paralog `Cc2d1b` was not in
the visible training target list, so no same-family expression signature was
available. The relevant visible CRISPR counts in `151 TH Prkcd Grin2c Glut`
were:

| visible perturbation | focal `n_degs` | relevance to `Cc2d1a` |
| --- | ---: | --- |
| `Htr1a` | 0 | direct Freud-1/CC2D1A transcriptional target in serotonin signaling; no detectable focal RNA cascade after receptor loss |
| `Htr1b` | 0 | Gi/o-coupled serotonin receptor counterexample |
| `Htr2a`, `Htr2b`, `Htr2c`, `Htr7` | 0 each | alternate serotonin receptor branches; all flat in this class |
| `Drd2`, `Drd4`, `Drd5` | 0 each | dopamine receptor counterexamples; `Drd2` is a reported Freud-regulated receptor |
| `Nfkb1` | 0 | NF-kappaB pathway probe; flat in the focal class |
| `Camk2a`, `Camk2g`, `Camkmt` | 0 each | CaMK/cAMP-signaling context around Freud-1 regulation; no focal DEGs |
| `Camk2b` | 1 | CaMK family counterexample; the one significant gene was its own transcript |
| `Deaf1` | 3 | another HTR1A transcriptional repressor; only `Eif4g3`, `B4gat1`, and `Rac3` passed FDR 0.05 |
| `Crebbp` | 8 | CREB coactivator context; small response |
| `Creb1` | 10 | cAMP/PKA/CREB axis downstream of CC2D1A/PDE4D; small response |

The Parquet filter found 17,259 measured gene rows per recovered target in the
focal class. `Htr1a`, `Drd2`, and `Nfkb1` each had 0 genes with
`pvals_adj < 0.05`; `Camk2b` had only `Camk2b` itself
(`log2FC = -0.439`, `pvals_adj = 1.27e-10`); `Deaf1` had only `Eif4g3`
(`log2FC = -0.661`, `pvals_adj = 2.84e-21`), `B4gat1`
(`log2FC = -0.694`, `pvals_adj = 7.44e-7`), and `Rac3`
(`log2FC = -0.674`, `pvals_adj = 0.0244`); `Creb1` and `Crebbp` crossed FDR
for only 10 and 8 genes. The same-experiment `Htr1a`, `Drd2`, and `Camk2b`
reports also found essentially flat surfaces across all recovered neuronal
classes and no broad convergent serotonin, dopamine, or CaMKII transcriptomic
module.

# Target-Specific Reasoning

## `Cc2d1a`

`Cc2d1a` encodes CC2D1A/Freud-1, a conserved DM14/C2-domain protein. External
work supports two relevant functional faces: it can act in the nucleus as a
calcium-regulated repressor of `Htr1a` and `Drd2` promoters, and it can act as
a signaling scaffold for cAMP/PKA/CREB and PDE4D regulation. Ou et al. 2003 and
Rogaeva and Albert 2007 identified Freud-1 as a calcium-regulated 5-HT1A
repressor; Hadjighassem et al. 2010 showed that the paralog CC2D1B/Freud-2
also represses the 5-HT1A dual repressor element; Galaraga et al. 2024 showed
that CaMKIV phosphorylation can inhibit Freud-1 repression of 5-HT1A and
dopamine D2 reporter targets. Al-Tawashi et al. 2012, Al-Tawashi and Gehring
2013, and Bhattacharya et al. 2024 connect CC2D1A loss or patient variants to
defective cAMP/PKA/CREB signaling through PDE4D regulation. Neuronal mouse
deletions produce synaptic, dendritic, plasticity, and behavior phenotypes:
Oaks et al. 2017 deleted `Cc2d1a` postnatally in forebrain, Yang et al. 2019
implicated Rac1 hyperactivity in hippocampal defects, and Yang et al. 2021
found autistic-like phenotypes after glutamatergic-neuron deletion.

Those functions establish biological importance, but they do not point to a
hundreds-of-DEGs focal thalamic RNA phenotype in this assay. The intervention
here is sparse AAV CRISPR loss starting at P16, the direct molecular
consequence is partial mosaic CC2D1A loss, and the measured endpoint is basal
nuclear RNA in recovered postnatal thalamic glutamatergic nuclei 3 to 4 weeks
later. Many well-supported CC2D1A consequences occur as promoter derepression,
cAMP/PKA/CREB pulses, Rac1 activity, dendrite/spine morphology, synaptic
plasticity, or behavior rather than a large survivor-state transcriptome.
Developmental phenotypes from germline or embryonic glutamatergic deletion are
also partly upstream of a P16 perturbation.

The most endpoint-proximal visible perturbations supported a low prediction.
Loss of `Htr1a`, `Htr1b`, or `Drd2` in the same focal class gave 0 DEGs,
arguing that receptor-level serotonin/dopamine perturbations are decoupled
from a large steady-state snRNA-seq response here. This is a counterexample
rather than a same-direction analog because `Cc2d1a` loss may derepress some
receptors whereas receptor CRISPR removes receptor function, but it still shows
that the basal transcriptomic readout is insensitive to this monoaminergic
branch. `Nfkb1`, `Camk2a`, and `Camk2g` were also 0-DEG perturbations;
`Camk2b`, the closest visible CaMK perturbation with a nonzero call, had only
one focal significant gene and that was its own transcript. `Creb1` and
`Crebbp` had nonzero but still small focal counts of 10 and 8. `Deaf1`, another
5-HT1A repressor whose same-experiment report found no detectable regulation
of `Htr1a` in the sampled neuronal groups, had only three focal DEGs.

I therefore predict no FDR<0.05 genes for `Cc2d1a` in
`151 TH Prkcd Grin2c Glut`. The zero is driven mainly by the visible
within-dataset endpoint counts of Freud/monoamine/cAMP-related analogs, with
external literature used to decide that those were the appropriate analogs and
that stronger germline or cell-type-specific neurodevelopmental phenotypes
should not be transferred wholesale to this basal postnatal DEG-count endpoint.

# Limits

The prediction is extrapolative because neither `Cc2d1a` nor `Cc2d1b` was
visible as a training perturbation. CC2D1A is a scaffold and transcriptional
regulator with several possible causal exits, so `Htr1a`, `Drd2`, `Nfkb1`,
`Camk2`, `Deaf1`, `Creb1`, and `Crebbp` are partial analogs rather than
obligate complex partners. The Cc2d1a literature largely used germline,
conditional Cre-lox, or shRNA perturbations in cortex, hippocampus, raphe, or
hippocampal slices; different timing, anatomy, and perturbation strength could
unmask a phenotype not seen in `151 TH Prkcd Grin2c Glut`. Conversely, the
screen only measures recovered nuclear RNA, so a zero DEG count would not rule
out disrupted PKA/CREB phosphorylation, Rac1 activity, dendritic spines,
serotonin/dopamine receptor physiology, or behavior.
