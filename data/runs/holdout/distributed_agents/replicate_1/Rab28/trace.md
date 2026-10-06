# Trace

## Question and endpoint

I interpreted the task as a scalar prediction for one held-out perturbation,
`Rab28`, in `151 TH Prkcd Grin2c Glut` thalamic glutamatergic neurons.  The
quantity to predict is `n_degs`, the count of measured genes with
Benjamini-Hochberg adjusted Wilcoxon `pvals_adj < 0.05` after acute sparse
P16 AAV CRISPR loss of function and P37-P44 snRNA-seq.

The held-out endpoint is absent for `Rab28`: neither the `Rab28` perturbation's
signature nor its true DEG count is present in the declared parquet or training
count CSV.  The training count CSV is a direct observation of the same endpoint
for 1,674 non-held-out targets.  The parquet is direct focal-cell and
cross-cell differential expression for those same non-held-out perturbations.
The July 260713 Sourceguard 1773 v1 PerturbAI corpus was used as a packaged
same-experiment interpretation layer, not as independent replication.  External
RAB28 biology was taken from PubMed-indexed primary literature and reviews.

I resolved the only threshold ambiguity by using the task's FDR 0.05 endpoint
for all point counts.  Some same-experiment corpus summaries describe FDR 0.10
surfaces; those were used only to understand broad analog behavior, while exact
counts below are the focal-cell FDR 0.05 counts from the supplied CSV/parquet.

## Quantitative calibration against the supplied data

From `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`, the focal endpoint is
strongly zero-inflated:

- training perturbations: 1,674
- perturbations with `n_degs = 0`: 1,205, or 72.0%
- median `n_degs`: 0
- 75th percentile: 1
- 90th percentile: 2
- 95th percentile: 18

I queried only `group_name = '151 TH Prkcd Grin2c Glut'` rows from
`training_de_all_cell_groups.parquet` for targets that could mechanistically
bound Rab28: Rab-family trafficking genes, the RAB3GAP/Rab18 axis, and
represented ciliary or ciliopathy genes.  No held-out `Rab28` perturbation rows
were present, as expected.

## Target-specific evidence

### Rab28

**External function prior.**  Mammalian RAB28 is an atypical farnesylated
Rab/Ras-family small GTPase (Brauers et al. 1996, PMID: 8647132; Lee et al.
2008, DOI: 10.1016/j.febslet.2008.11.008) best connected to photoreceptor and
ciliary trafficking.  Human biallelic RAB28 variants cause autosomal recessive
cone-rod dystrophy with RAB28 localized to the photoreceptor basal body/ciliary
rootlet (Roosing et al. 2013, DOI: 10.1016/j.ajhg.2013.05.005), mouse Rab28
loss impairs cone outer-segment shedding/phagocytosis (Ying et al. 2018,
DOI: 10.1074/jbc.RA118.005484), and C. elegans Rab28/BBSome work places RAB28
at ciliary extracellular-vesicle control (Akella et al. 2020,
DOI: 10.7554/eLife.50580).  These are strong functions in retina, RPE, and
ciliated sensory biology, but they do not make Rab28 a core late-endosomal
housekeeping Rab like Rab7 in juvenile NeuN-positive thalamic neurons.

**Rab-family analogs in the training endpoint.**

- `Rab18`: 0 DEGs in the focal class.  The focal parquet rows had no corrected
  downstream signal; the best row was the `Rab18` self transcript at
  logFC -0.468, FDR 0.912 from 117 perturbed nuclei.  The internal corpus
  reported that `Rab18` had only one FDR 0.10 downstream transcript across
  21 measured neuronal groups and no canonical ER/lipid-droplet, autophagy,
  lysosomal, or lipid-homeostasis program.
- `Rab27a`: 0 DEGs.  The best focal row was `Klhl9`, logFC -0.523,
  FDR 0.950 from 135 perturbed nuclei.  The corpus describes `Rab27a` as a
  complete corrected transcriptomic null across all recovered NeuN-positive
  neuronal groups, despite its known role in regulated secretory vesicles.
- `Rab3gap1`: 0 DEGs.  The focal class had no row below FDR 1.0 from
  159 perturbed nuclei.  The corpus reported pan-measured neuronal buffering
  for the RAB3GAP-Rab18 module.
- `Rab3gap2`: 0 DEGs.  The best focal row was `Pnn`, FDR 0.830 from
  152 perturbed nuclei.  Its same-complex partner `Rab3gap1` and downstream
  Rab `Rab18` did not phenocopy a shared postnatal neuronal transcriptional
  program in the July corpus.

The important counterexample is `Rab7`, which had 501 DEGs at FDR 0.05 in this
same focal class from 215 perturbed nuclei.  Its strongest rows included
`Atp6v1b2`, `Dpp7`, `Scpep1`, `Lamp2`, V-ATPase components, and sterol genes,
matching a lysosomal/late-endosomal compensation program.  This shows the assay
can detect Rab-dependent endolysosomal stress in `151 TH Prkcd Grin2c Glut`
neurons, but `Rab7` is a core late-endosome/lysosome regulator.  Rab28 is a
distant ciliary/farnesylated GTPase rather than an obligate member of the Rab7
lysosomal limiting function, so the causal chain from `Rab7` intervention to
Rab7-dependent lysosomal traffic to lysosomal/sterol compensation does not
transfer to `Rab28` loss.

**Ciliary and retinal-dystrophy analogs.**

The represented ciliary comparator set was also nearly silent in the focal
endpoint:

- `Ttll5`: 0 DEGs; best focal row `Nsmce2`, FDR 0.946 from 163 perturbed
  nuclei.  The corpus reported no FDR 0.10 downstream genes in any of
  22 recovered neuronal classes and explicitly contrasted this brain silence
  with TTLL5/RPGR photoreceptor biology.
- `Rpgr`: 0 DEGs; best focal row `Pcgf6`, FDR 0.648 from 108 perturbed nuclei.
  The corpus likewise reported 0 FDR 0.10 downstream genes across the
  21 measured postmitotic NeuN-positive brain groups.
- `Bbs5`: 0 DEGs; best focal row `Ptprn`, FDR 0.220 from 121 perturbed nuclei.
  Same-experiment BBSome summaries found only one narrow non-focal event and
  no shared Hedgehog, ciliary GPCR, UPR/ISR, autophagy, or BBSome transcriptional
  program.
- `Ift88`, `Ift81`, `Ift43`, `Kif3b`, `Cep290`, and `Ttc21b`: all 0 focal
  DEGs.
- `Arl3`: 1 focal DEG, but that single significant row was `Arl3` itself
  (logFC -0.418, FDR 0.018) with no downstream gene below 0.05.  The corpus
  framed `Arl3` as a ciliary lipidated-cargo GTPase whose acute loss produced
  no robust downstream brain neuronal transcriptome.

This set is a closer causal transfer model for Rab28 than Rab7:

```
Rab28 CRISPR LoF
-> altered farnesylated ciliary small-GTPase function, strongest in photoreceptor outer-segment/RPE ciliary contexts
-> possible changes in ciliary cargo or extracellular-vesicle handling
-> no known obligate juvenile thalamic lysosomal, sterol, UPR, or synaptic transcriptional cascade
-> recovered NeuN-positive 151 TH nuclei 3-4 weeks after P16 perturbation
-> predicted no genes passing BH FDR 0.05
```

The same-experiment analogs support the same direction at each stage: retinal
and primary-cilium genes represented in the screen were commonly flat in the
postnatal brain snRNA-seq readout, and the few nonzero examples were either a
self-transcript change or isolated one-gene responses, not a broad focal-class
program.

**Downstream expression of Rab28 itself.**  `Rab28` as a measured transcript was
significant after only 1 of 1,674 focal training perturbations.  The one row was
`Elp1 -> Rab28`, logFC 0.293, FDR 0.0276.  The next lowest adjusted p-values
for `Rab28` were already above 0.12.  Thus `Rab28` is not a recurrent marker of
one of the broad stress signatures in this focal cell class.

## Prediction

I predicted `Rab28 = 0`.  This is driven mainly by the supplied data: the focal
endpoint's high mass at zero; 0-DEG focal surfaces for the represented
`Rab18`, `Rab27a`, `Rab3gap1`, `Rab3gap2`, `Bbs5`, `Ttll5`, `Rpgr`, `Ift88`,
`Cep290`, and related ciliary targets; and absence of a recurrent downstream
`Rab28` expression module.  External biology reinforces the prediction because
the strongest published Rab28 phenotypes are in photoreceptor/RPE ciliary outer
segment biology, lineages excluded from this NeuN-positive whole-brain screen.

## Limits

The result is an extrapolation because the actual held-out `Rab28` signature was
not supplied.  Rab28 could have a thalamus-specific ciliary role that was not
captured by `Bbs5`, `Rpgr`, `Ttll5`, `Arl3`, or IFT/Cep perturbations, and many
immediate RAB28 trafficking partners were not represented as perturbation
targets.  The assay also measures survivor-conditioned nuclear RNA, not ciliary
localization, extracellular vesicle shedding, photoreceptor outer-segment
phagocytosis, RPE physiology, or indels.  Therefore the prediction is
specifically a count of focal-cell FDR-significant nuclear transcriptional
changes, not a prediction that Rab28 is biologically dispensable.
