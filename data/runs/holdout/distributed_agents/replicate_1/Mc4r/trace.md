# Held-out DEG-count prediction for 151 TH Prkcd Grin2c Glut

## Question and endpoint

The task asks for one scalar prediction: the number of measured genes that would
pass Benjamini-Hochberg FDR 0.05 in the `151 TH Prkcd Grin2c Glut` contrast
after a held-out `Mc4r` perturbation.  I treated `151 TH Prkcd Grin2c Glut` as
the exact Allen-derived thalamic glutamatergic class label from the dataset
portrait, not as a tyrosine-hydroxylase cell type.  The requested readout is a
3-4 week, survivor-conditioned snRNA-seq Wilcoxon DEG burden, so feeding,
obesity, receptor coupling, cAMP, and phospho-CREB evidence are mechanistic
priors unless the same chain is expected to create a basal RNA program in this
class.

There was a single requested target:

```tsv
target_name
Mc4r
```

`Mc4r` had zero rows in the supplied Parquet and was absent from the focal
training-count CSV, as expected for a completely held-out perturbation.

## Sources used

- Direct endpoint source: `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Direct expression-pattern source:
  `training differential-expression dataset`.
- Run-local target manifest:
  `single-target request for Mc4r`.
- Dataset context, task bindings, compact coverage, capability manifest, and
  measurement registry under `codex_runtime/pipeline`.
- Internal same-experiment corpus:
  `perturbai-july-260713-sourceguard-1773-v1`, queried only for bounded
  curated reports around visible comparators `Gpr45`, `Adcy3`, and `Gnas`.
- PubMed literature:
  Krashes, Lowell, and Garfield 2016, DOI `10.1038/nn.4202`, PMID `26814590`;
  Podyma et al. 2018, DOI `10.1074/jbc.RA118.003450`, PMID `29794140`;
  Singh et al. 2023, DOI `10.1016/j.physbeh.2023.114105`, PMID `36736416`;
  Cho et al. 2023, DOI `10.1523/JNEUROSCI.0704-23.2023`, PMID `37591737`;
  Xun et al. 2025, DOI `10.1126/science.adp3989`, PMID `40472089`.

## Computation

I used the focal training-count CSV to calibrate the response scale of the
endpoint.  The focal response distribution across 1,674 visible training
perturbations was strongly zero-inflated: 1,205 targets had `n_degs = 0`, the
median was 0, the 75th percentile was 1, the 90th percentile was 2, and only the
largest stress, splicing, proteasome, transport, and chromatin targets reached
hundreds to thousands of DEGs.

I then looked up the endpoint counts for biologically relevant receptor and
melanocortin/cAMP perturbations that were actually present in the training
file.  The direct focal-class counts were:

```tsv
target_name	n_degs
Mc1r	0
Mc2r	0
Mchr1	0
Adcy1	0
Adcy3	0
Adcy5	0
Gnas	0
Gpr45	0
Htr2c	0
Lepr	0
Npy1r	0
Npy2r	0
Npy5r	0
Ntsr1	0
Agrp	0
Ntrk2	3
Pcsk2	1
```

For expression-pattern evidence, I read only the Parquet row groups containing
the focal cell class and summarized the same analog targets by FDR support,
minimum adjusted p value, the largest absolute log2 fold-change in that class,
and recovered perturbed nuclei.  The relevant focal results were:

```tsv
gene_target	n_degs	min_padj	n_pert
Ntrk2	3	2.33e-05	149
Pcsk2	1	1.19e-28	107
Adcy3	0	0.112	223
Adcy1	0	0.139	88
Adcy5	0	0.912	154
Gnas	0	1	306
Gpr45	0	1	190
Htr2c	0	1	126
Lepr	0	1	202
Mc1r	0	1	257
Mc2r	0	1	160
Npy1r	0	1	67
Npy2r	0	0.958	120
Npy5r	0	1	100
Ntsr1	0	1	225
Agrp	0	1	261
Glp1r	0	1	132
Galr1	0	1	266
```

The singleton and three-gene responses were also mostly self-target or
same-axis-negative controls rather than broad pathway states.  `Pcsk2`
registered only `Pcsk2` itself in the focal class; `Gpr158` and `Gprasp2`,
two unrelated GPCR-associated examples, likewise registered only their own
target transcripts.  `Gnao1` had one focal DEG, also its own transcript.
`Ntrk2` had three focal DEGs: `Ntrk2`, `Atp2a2`, and `Vgf`.  That BDNF receptor
perturbation is a useful counterexample because it shows that a neurotrophic
receptor can produce a small signal, but it is not a close Mc4r phenocopy:
NTRK2 signals through Ras/MAPK, PI3K/AKT, and PLC-gamma as well as CREB-linked
arms, whereas MC4R is primarily a Gs/cAMP melanocortin receptor.

I also scanned these analogs across all cell classes.  The Mc4r-adjacent
ciliary/cAMP targets remained very sparse: `Gpr45`, `Gnas`, `Lepr`, `Htr2c`,
`Npy1r`, `Npy2r`, `Npy5r`, and the melanocortin receptors represented in the
training data had no FDR 0.05 calls in the focal class, and `Adcy3` had only two
one-gene calls outside the focal class.  This argues that the focal zero is not
an isolated thalamic miss for a receptor axis that was otherwise producing
large RNA signatures elsewhere in the same assay.

## Target-specific reasoning

### Mc4r

The direct molecular effect of the held-out perturbation is loss of
melanocortin 4 receptor in edited neurons.  Canonical MC4R biology is strong:
the receptor is a central melanocortin GPCR that integrates POMC-derived
agonists and AgRP antagonism to control feeding, energy expenditure, glucose
homeostasis, and autonomic output (Krashes, Lowell, and Garfield 2016, PMID
26814590).  In mouse MC4R-expressing cells, Gs-alpha loss disrupts normal energy
balance and blunts MC4R agonist responses (Podyma et al. 2018, PMID 29794140).
More recent work places GPR45, MC4R, and ADCY3 together at primary cilia in
paraventricular hypothalamic MC4R neurons (Xun et al. 2025, PMID 40472089).
MC4R also has non-PVH circuit roles, including ventral-subiculum MC4R neurons
that receive input from anterior paraventricular thalamus and regulate food
motivation (Singh et al. 2023, PMID 36736416).  A neighboring melanocortin
receptor, MC3R, is expressed in paraventricular thalamic neurons and links
melanocortin input to anxiety and feeding (Cho et al. 2023, PMID 37591737).

The causal transfer chain for this task is therefore:

`Mc4r sgRNAs -> reduced MC4R function -> weaker melanocortin GPCR/ciliary
Gs-alpha/ADCY3/cAMP signaling in the edited neurons that express Mc4r -> possible
changes in CREB-dependent transcription or circuit-state genes -> surviving
NeuN-positive nuclei assigned to broad thalamic class 151 -> Wilcoxon DEG
count`.

The literature supports the first three steps in MC4R-expressing hypothalamic
and hippocampal/circuit neurons, but the endpoint-bearing transfer is weak at
the last three steps.  The focal population is a broad thalamic glutamatergic
class rather than a PVH or receptor-defined MC4R class, and the assay measures
a basal RNA state 3-4 weeks after mosaic postnatal loss, not synchronized ligand
stimulation, cAMP, phosphoprotein signaling, food intake, or body weight.  A
downstream melanocortin or cAMP perturbation should have promoted `Mc4r` only if
it produced a durable broad RNA signature in this same design.  It did not:

- `Gpr45`, the ciliary MC4R/ADCY3 modulator, was `n_degs = 0` in class 151 with
  190 perturbed nuclei.  The same-experiment July corpus called it an all-null
  P16-to-P37/44 perturbation at broad neuronal class resolution and noted that
  expected POMC/JAK-STAT/melanocortin/cAMP transcriptional readouts were absent.
- `Adcy3`, the ciliary adenylyl cyclase downstream of MC4R and GPR45, was
  `n_degs = 0` in class 151 with minimum adjusted p value 0.112.  The curated
  `Adcy3` report summarized it as a pan-neuronal downstream null and found that
  `Adcy1`, `Adcy5`, `Gnas`, `Gnal`, PDE, PKA, and CREB-axis perturbations did
  not form an interchangeable cAMP transcriptome in the atlas.
- `Gnas`, the canonical Gs-alpha transducer, was `n_degs = 0` in class 151 and
  had no hypothalamic-class response in the same corpus despite external
  evidence that Gs-alpha in MC4R-expressing cells is required for whole-animal
  metabolic phenotypes.
- `Lepr`, `Agrp`, `Htr2c`, `Npy1r`, `Npy2r`, `Npy5r`, `Ntsr1`, `Mchr1`,
  `Glp1r`, and `Galr1` were all focal zeros.  They are not exact MC4R molecular
  substitutes, but they are peptide or metabolic GPCR/circuit components that
  would have revealed a general durable neuropeptide-receptor RNA response if
  this assay and cell class were sensitive to one.
- `Mc1r` and `Mc2r` were also zero.  They are melanocortin receptor paralogs and
  much weaker neuronal analogs of MC4R, so I used them only as counterexamples
  to a generic melanocortin-receptor-family signal.

The exact point estimate is therefore driven mainly by the direct training
counts and focal expression patterns of `Gpr45`, `Adcy3`, `Gnas`, and receptor
analogs.  External biology says `Mc4r` is functionally important, but in this
screen an acute mosaic knockout of several more proximal or downstream
melanocortin/cAMP components was transcriptionally buffered or invisible at
class resolution.  I predict no genes will cross FDR 0.05 for held-out `Mc4r` in
`151 TH Prkcd Grin2c Glut`.

Prediction: `Mc4r -> 0`.

## Limits

This is an extrapolation from related visible perturbations, not a direct MC4R
signature.  The in-dataset analogs mostly cover cAMP transduction, ciliary
ADCY3/GPR45 modulation, and broad neuropeptide GPCR behavior; none is the same
intervention as deleting `Mc4r`.  The strongest published MC4R effects are
cell-type- and circuit-physiology endpoints in PVH, vSUB, autonomic, and
feeding circuits, while the requested endpoint is a basal snRNA-seq count in a
broad thalamic class.  The broad class could dilute a rare MC4R-positive
subpopulation, and sparse AAV CRISPR may not synchronize a ligand-gated GPCR
program.  For that reason the prediction is high confidence for zero detectable
FDR genes under this assay, but not evidence that MC4R itself is biologically
irrelevant or unedited.
