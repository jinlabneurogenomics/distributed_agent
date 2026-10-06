# Gapdh hold-out DEG-count prediction

## Question and endpoint

I treated the requested readout as a scalar endpoint: for each held-out perturbation,
predict the integer number of measured genes with `pvals_adj < 0.05` in `151 TH
Prkcd Grin2c Glut` cells after acute AAV CRISPR-Cas9 loss of the target gene.
The focal class label was used exactly as a thalamic glutamatergic class; `TH`
was not interpreted as tyrosine hydroxylase. The target was held out, so the
`Gapdh`-KO signature itself was not available.

The prediction below uses:

- The declared training endpoint
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Targeted focal-cell reads from
  `training differential-expression dataset`.
- The run-local measurement registry and dataset portrait, which define the
  Parquet as same-experiment differential-expression summaries over recovered
  nuclei and warn that self-transcript log fold change is QC context rather than
  a functional editing-efficiency measurement.
- The selected same-experiment semantic corpus,
  `perturbai-july-260713-sourceguard-1773-v1`. A BioKG lookup for `Gapdh`
  returned no `Gene`/`TargetGene` node, so no target-specific same-experiment
  Finding text for `Gapdh` was used.
- External pathway/function priors from KEGG PATHWAY/Glycolysis,
  mmu00010, accessed 2026-09-03; KEGG is described in Kanehisa et al. 2025,
  Nucleic Acids Research, DOI `10.1093/nar/gkae909`.
- External literature that established GAPDH as the glycolytic
  glyceraldehyde-3-phosphate dehydrogenase and summarized its extraglycolytic
  stress/apoptosis activities: Nicholls et al. 2012, DOI
  `10.1111/j.1440-1681.2011.05599.x`; neuronal-apoptosis examples include
  Ishitani and Chuang 1996, DOI `10.1073/pnas.93.18.9937`, Saunders et al.
  1999, DOI `10.1046/j.1471-4159.1999.0720925.x`, and the review by Mazzola
  and Sirover 2002, DOI `10.1016/s0161-813x(02)00062-1`.

## Quantitative calibration from training perturbations

The focal-cell training endpoint is sparse and highly skewed. Among 1,674
non-held-out perturbations, 1,205 had `n_degs = 0`, the median was 0, the 75th
percentile was 1, and only the 95th percentile exceeded 18 DEGs.

Because the held-out target is `Gapdh`, I queried the focal-cell Parquet rows
for represented core glycolysis and adjacent carbon-metabolism genes rather
than using unrelated large-footprint transcription or spliceosome genes as
analogs. The most directly relevant training perturbations were:

| training KO | focal `n_degs` | focal expression-pattern evidence | interpretation for `Gapdh` |
| --- | ---: | --- | --- |
| `Hk1` | 1 | the only significant gene was `Hk1`; self log2FC -0.768, BH 9.86e-05 | early glycolysis and ATP-coupled glucose phosphorylation; CRISPR produced a detectable self-transcript hit but no broad survivor-state response |
| `Gpi1` | 1 | the only significant gene was `Gpi1`; self log2FC -0.673, BH 2.14e-07 | core glycolysis/gluconeogenesis enzyme just downstream of HK; again self-only |
| `Pfkm` | 1 | the only significant gene was `Pfkm`; self log2FC -0.857, BH 6.42e-14 | rate-controlling glycolysis step; self-only despite strong target RNA depletion |
| `Tpi1` | 1 | the only significant gene was `Tpi1`; self log2FC -1.010, BH 6.23e-12 | triose-phosphate interconversion immediately upstream of GAPDH substrate production; self-only |
| `Eno1` | 0 | no gene reached BH < 0.05 | downstream glycolysis enzyme; a counterexample showing that a represented glycolytic target can be completely quiet in this endpoint |
| `Mdh1` | 29 | 29 significant genes, led by `Mdh1`, `Cars`, `Gls`, `Ncdn`, `Bicd2`, `Atp2a2`, `Zcchc7` | cytosolic malate dehydrogenase / NADH shuttle rather than a glycolytic step; useful only as an upper-scale counterexample for neighboring carbon metabolism |

Other represented mitochondrial/TCA perturbations were also mostly null or
self-only in this class: `Mdh2`, `Pdha1`, `Sdha`, and `Glud1` each had 1 DEG,
and `Aco2` and `Ogdh` had 0. The major high-count tail of the training
distribution instead came from genes such as `Uba5`, `Tpr`, `Sin3a`, `Rnpc3`,
`U2af2`, `Psmb4`, and `Hnrnpu`, whose spliceosome, proteostasis, nuclear-pore,
and chromatin mechanisms are not close causal analogs for partial acute
`Gapdh` loss in recovered postmitotic neurons.

## Target-specific prediction

### `Gapdh`: predicted `n_degs = 1`

`Gapdh` encodes the canonical NAD-dependent glyceraldehyde-3-phosphate
dehydrogenase in the middle of glycolysis, converting glyceraldehyde
3-phosphate to 1,3-bisphosphoglycerate. KEGG places mouse `Gapdh` in the same
core glycolytic sequence as `Hk1`, `Gpi1`, `Pfkm`, `Tpi1`, and `Eno1`. GAPDH
also has non-glycolytic stress, RNA-binding, nuclear, and apoptotic functions
that have been reported in neuronal injury settings, so complete GAPDH
perturbation can be consequential outside simple glucose flux.

The Perturb-seq intervention and endpoint make a broad response unlikely,
however. The experiment perturbs postnatal, postmitotic neurons with sparse
AAV-delivered CRISPR and observes only nuclei that survive, are recovered, and
remain class assigned 3-4 weeks later. The closest training KOs show that acute
partial perturbation of individual glycolytic enzymes usually did not create a
large FDR-significant transcriptional state in `151 TH Prkcd Grin2c Glut`:
`Hk1`, `Gpi1`, `Pfkm`, and `Tpi1` were all exactly one-gene calls, and those
calls were their own target transcripts. `Eno1` had zero DEGs. That pattern
argues against importing GAPDH's essentiality or apoptotic moonlighting into a
large `n_degs` estimate for the recovered-nucleus DE endpoint.

The nonzero part of the prediction comes from the same four self-only
glycolysis anchors. They establish that in this focal class, a core
glycolytic-enzyme CRISPR perturbation often produces one robust FDR-significant
feature through the target transcript itself, even when no downstream gene
passes the threshold. `Gapdh` is not guaranteed to do so, because target RNA
depletion is not a deterministic proxy for editing strength and `Eno1` is a
zero counterexample. Still, the target is an abundant housekeeping glycolysis
transcript and the nearest anchors favor a count of one over a strict null.

Thus I predict one significant measured gene for held-out `Gapdh`: the
on-target `Gapdh` transcript is expected to be the most likely call, while a
broader glycolysis-stress or apoptotic survivor-state program is not expected
to pass BH 0.05 in enough genes to move the count above the self-only analogs.

## Limits

This prediction is driven primarily by same-experiment endpoint analogs and
only secondarily by external GAPDH biology. The external literature mostly
comes from cultured neurons, disease, or immune/cancer metabolic systems and
therefore supports biochemical plausibility rather than a calibrated DEG count
in juvenile thalamic glutamatergic nuclei. The exact held-out `Gapdh`
self-transcript row was absent, so the one-DEG prediction extrapolates from
neighboring glycolysis KOs. A severe early selection effect could make the
surviving `Gapdh`-edited cells transcriptionally quiet, and an unexpectedly
strong oxidative-stress program could make the count higher; neither behavior
was supported by the represented focal-cell glycolysis anchors.
