# Question and endpoint

The requested held-out target was `Cep164`. I interpreted the task as a point
prediction for `n_degs`, the count of measured genes whose Wilcoxon
Benjamini-Hochberg adjusted p-value is below 0.05 in the
`151 TH Prkcd Grin2c Glut` cell group after a sparse postnatal CRISPR
loss-of-function perturbation. The count is assay-specific and includes any
measured gene that passes FDR, including the target transcript if it is detected
and significant; it is not a direct measure of editing efficiency or neuronal
importance.

The held-out endpoint for `Cep164` was absent by design. `Cep164` was present in
the requested-target CSV, absent from the focal training-count CSV, and absent
from the same-experiment July report corpus, so I used visible ciliary
perturbations as counterfactuals rather than reading any same-target result.

# Sources

- Differential-expression Parquet:
  `training differential-expression dataset`
- Training focal DEG counts:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`
- Requested held-out manifest:
  `single-target request for Cep164`
- Internal same-experiment interpretation corpus:
  `perturbai-july-260713-sourceguard-1773-v1`, used for visible comparator
  reports and Findings only.
- External literature via NCBI PubMed E-utilities: Cajanek and Nigg 2014
  (DOI: 10.1073/pnas.1401777111), Oda et al. 2014
  (DOI: 10.1111/gtc.12191), Rosa e Silva et al. 2021
  (DOI: 10.1016/j.str.2021.08.007), Siller et al. 2017
  (DOI: 10.1371/journal.pgen.1007128), Reed et al. 2022
  (DOI: 10.1371/journal.pgen.1010154), Chaki et al. 2012
  (DOI: 10.1016/j.cell.2012.06.028), Humbert et al. 2012
  (DOI: 10.1073/pnas.1210916109), and Berbari et al. 2008
  (DOI: 10.1073/pnas.0711027105).

# Quantitative calibration

The focal training set contains 1,674 visible non-held-out perturbations. Its
response burden is strongly skewed toward zero:

| statistic | value |
| --- | ---: |
| `n_degs == 0` | 1,205 / 1,674 = 71.98% |
| `n_degs == 1` | 276 / 1,674 = 16.49% |
| median | 0 |
| 90th percentile | 2 |
| 95th percentile | 18 |
| maximum | 2,677 |

I then looked for visible training perturbations that were either close
centrosomal/ciliogenesis analogs of `Cep164` or part of the same ciliary
transport and signaling machinery that should be affected after a distal
appendage ciliogenesis defect. In the training counts, the focal `151 TH Prkcd
Grin2c Glut` burdens were:

| training target | focal `n_degs` | focal Parquet pattern |
| --- | ---: | --- |
| `Cep120` | 0 | 17,259 genes tested, 184 perturbed nuclei, minimum FDR 1.0 |
| `Cep290` | 0 | 17,259 genes tested, 99 perturbed nuclei, minimum FDR 0.650 |
| `Cep112` | 0 | 17,259 genes tested, 106 perturbed nuclei, minimum FDR 1.0 |
| `Cep85l` | 0 | 17,259 genes tested, 173 perturbed nuclei, minimum FDR 1.0 |
| `B9d1` | 0 | 17,259 genes tested, 180 perturbed nuclei, minimum FDR 1.0 |
| `Rpgrip1l` | 0 | 17,259 genes tested, 137 perturbed nuclei, minimum FDR 0.184 |
| `Sclt1` | 0 | 17,259 genes tested, 122 perturbed nuclei, minimum FDR 1.0 |
| `Ift43` | 0 | 17,259 genes tested, 328 perturbed nuclei, minimum FDR 0.847 |
| `Ift81` | 0 | 17,259 genes tested, 152 perturbed nuclei, minimum FDR 0.391 |
| `Ift88` | 0 | 17,259 genes tested, 143 perturbed nuclei, minimum FDR 1.0 |
| `Bbs5` | 0 | 17,259 genes tested, 121 perturbed nuclei, minimum FDR 0.220 |
| `Dync2h1` | 0 | 17,259 genes tested, 98 perturbed nuclei, minimum FDR 0.348 |
| `Dync2i1` | 0 | 17,259 genes tested, 229 perturbed nuclei, minimum FDR 1.0 |
| `Kif3b` | 0 | 17,259 genes tested, 156 perturbed nuclei, minimum FDR 1.0 |
| `Alms1` | 0 | 17,259 genes tested, 110 perturbed nuclei, minimum FDR 1.0 |
| `Arl3` | 1 | The single FDR<0.05 focal call was `Arl3` itself; the next-best row was `Myt1`, FDR 0.103 |

This panel is not a generic family-frequency count. `Cep120`, `Cep290`,
`Rpgrip1l`, and `B9d1` test centrosomal or transition-zone ciliopathy genes;
`Sclt1` is a distal-appendage assembly comparator; `Ift43`, `Ift81`, `Ift88`,
`Dync2h1`, `Dync2i1`, and `Kif3b` test the intraflagellar transport motors and
particles that would become mislocalized or nonfunctional after failure to form
a proper basal-body/ciliary gate; `Bbs5` and `Arl3` test the ciliary cargo
trafficking layer downstream of a formed cilium. Their shared result in the
focal cell group was therefore strong evidence that acute perturbation of the
ciliogenesis/transport axis is usually buffered at the FDR-thresholded nuclear
RNA level in postnatal `151 TH Prkcd Grin2c Glut` neurons.

# Expression-pattern and corpus evidence

I used the July same-experiment corpus to inspect the broader expression
patterns of visible ciliary analogs:

- `Cep120` is a pan-measured neuronal transcriptional null in the July report:
  zero downstream genes at FDR<0.10 in all 22 measured neuronal groups,
  including highly sampled thalamic and midbrain groups. The report explicitly
  contrasted `Cep120` with measured ciliary relatives including `Bbs5`,
  `Cep290`, `Dync2h1`, `Dync2i1`, `Ift43`, `Ift81`, `Ift88`, `Kif3b`,
  `Rpgrip1l`, and `Ttc8` and did not find a shared positive ciliary
  transcriptome.
- `Cep290`, a transition-zone ciliopathy gene downstream of distal appendage
  assembly, had zero downstream genes at FDR<0.10 in its 20 measured neuronal
  groups. Its focal `151` comparison had 99 perturbed nuclei, self-transcript
  FDR 1.0, and no downstream row with FDR below 0.65. Its curated ciliary,
  GPCR, and Hedgehog marker genes also did not appear at FDR<0.10.
- `Ift81`, a core IFT-B component, had zero downstream genes at FDR<0.10 in all
  22 measured groups. Its report checked Hedgehog and neuronal ciliary GPCR
  transcripts and found no FDR-level response.
- `Ift88` was almost silent: the corpus found only a singleton `Pcsk1n` call in
  `155 MB Glut`, no multi-gene IFT-B or Gli/Ptch program, and no focal `151`
  DEGs.
- `Dync2h1` and `Dync2i1` were complete postnatal neuronal nulls in the corpus
  despite their roles in retrograde IFT and Sonic Hedgehog/Gli trafficking.
- `Bbs5` had only an isolated extra-focal `Sirt5` response in `046 CTX-CGE
  GABA`; it did not activate ciliary GPCR, Hedgehog, UPR, ISR, or autophagy
  expression programs in the measured neuronal atlas.

The corpus and the Parquet are different representations of the same
Perturb-seq experiment, so I treated the report statements as bounded summaries
of the training data, not as independent replication.

# Biological rationale for `Cep164`

CEP164 is an early centriolar distal-appendage protein. Cajanek and Nigg 2014
showed that Cep164 recruits active TTBK2 to the mother centriole, initiating
ciliogenesis through CP110 removal and IFT recruitment; Oda et al. 2014
likewise showed that the CEP164-binding motif in TTBK2 is needed for its
centriolar localization, CP110 removal, and ciliogenesis. Rosa e Silva et al.
2021 structurally mapped the CEP164-TTBK2 complex and showed how human
ciliopathy mutations compromise that interaction. Siller et al. 2017 showed in
conditional mouse models that Cep164 is required for basal-body docking and
multiciliogenesis in airway, oviduct, and ependymal cells, and Reed et al. 2022
showed that deleting Cep164 in mouse photoreceptors disrupts basal-body docking
or, after docking, destabilizes IFT at the connecting cilium.

Those functions make `Cep120`, `Cep290`, `Sclt1`, `Rpgrip1l`, IFT, and
dynein-2 perturbations mechanistically relevant but not obligate positive
same-endpoint priors. The causal chain for the requested experiment is:

`Cep164` CRISPR loss of function -> impaired distal appendage/basal-body
docking and TTBK2-dependent IFT recruitment -> defective cilium assembly or
ciliary cargo localization -> altered Hedgehog/GPCR/ciliary signaling in
surviving postmitotic neurons if those pathways are active -> a possible
secondary steady-state nuclear RNA program in recovered thalamic nuclei.

The training data show breaks in the last two steps. P16/P37-44 NeuN+
thalamic neurons did not mount an FDR-level transcriptomic response when
nearby centrosomal and transition-zone genes were perturbed, and even direct
IFT, dynein-2, BBSome, and ARL-module perturbations were zero or singleton.
External literature does not supply a stronger mature thalamic nuclear
transcription program for CEP164 that would override those same-assay zeros:
human CEP164 variants cause nephronophthisis-related ciliopathy and can affect
kidney, retina, ependymal, and motile-ciliated tissues (Chaki et al. 2012;
Siller et al. 2017; Devlin et al. 2020, DOI: 10.1371/journal.pone.0221914;
Devlin et al. 2022, DOI: 10.1111/cge.14251), while a ciliary protein
interaction with ARL13B/PDE6D/INPP5E connects CEP164 to ciliary targeting
machinery (Humbert et al. 2012). Berbari et al. 2008 showed that BBS proteins
are required to localize GPCRs such as SSTR3 and MCHR1 to central-neuron
cilia, but the atlas BBS/IFT/TZ perturbations did not convert that subcellular
phenotype into a broad `151` snRNA-seq signature.

I therefore predicted **zero** DEGs for `Cep164`. This is driven primarily by
the within-dataset behavior of mechanistically adjacent ciliary targets in the
same focal cell group, with the external literature used to decide that those
zeros are the right analogs for a distal-appendage gene.

# Limits

The prediction is a context-specific FDR-count prediction, not a claim that
`Cep164` is biologically dispensable. The experiment did not measure DNA
indels, CEP164 protein, cilium assembly, TTBK2 recruitment, GPCR localization,
IFT accumulation, Hedgehog protein processing, neuronal electrophysiology, or
cell loss before nuclei were recovered. Ependymal cells, kidney, retina,
airway, reproductive multiciliated cells, olfactory epithelium, and most
developmental progenitor windows that are prominent in CEP164 biology were
outside this NeuN-enriched P16 perturbation assay. The held-out `Cep164`
signature itself is absent, so the point estimate extrapolates from related
genes whose exact biochemical positions are not identical: a distal appendage
assembly defect could be stronger than transition-zone or IFT perturbations if
it hit a thalamic ciliary signaling input absent from the visible comparators.
Nevertheless, the focal training counts put all close available ciliary
comparators at zero except for an `Arl3` self-transcript singleton, making a
zero count the most defensible point estimate.
