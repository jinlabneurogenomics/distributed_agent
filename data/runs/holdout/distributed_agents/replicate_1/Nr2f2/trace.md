# Question and endpoint

The requested endpoint is the held-out `n_degs` for one absent perturbation,
`Nr2f2`, in `151 TH Prkcd Grin2c Glut`. I treated this as a point
prediction for the number of measured genes with Wilcoxon BH-adjusted
`pvals_adj < 0.05` in recovered focal-class nuclei after acute AAV CRISPR loss
of function.

The focal readout is directly observed for 1,674 non-held-out training
perturbations in
`151 TH Prkcd Grin2c Glut` but absent for `Nr2f2`. I therefore used the
training count table as the direct calibration endpoint, and used the
differential-expression Parquet only for within-dataset pattern checks among
candidate analog perturbations and for expression of `Nr2f2` as a measured
transcript in the focal class. I did not treat self-transcript knockdown as
editing efficiency.

# Sources

- Declared training endpoint:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared DE table:
  `training differential-expression dataset`.
- Requested holdout manifest:
  `single-target request for Nr2f2`.
- Run-local PerturbAI atlas dataset portrait and measurement registry.
- Internal same-experiment semantic corpus: `perturbai-july-260713-sourceguard-1773-v1`.
  I made an exact BioKG check for Findings that reported `Nr2f2` as a comparator
  and found no records, so this corpus did not provide a target-specific
  mechanistic shortcut for this held-out gene.
- External literature found through NCBI PubMed E-utilities:
  Qiu et al. 1996, doi `10.1016/0960-0760(95)00225-1`, PubMed `8603050`;
  Tripodi et al. 2004, doi `10.1242/dev.01530`, PubMed `15548577`;
  Kanatani et al. 2008, doi `10.1523/JNEUROSCI.2132-08.2008`,
  PubMed `19074032`; Cai et al. 2013, doi `10.1002/cne.23186`,
  PubMed `22791192`; Kanatani et al. 2015, doi `10.1073/pnas.1420701112`,
  PubMed `26305926`; Yang et al. 2017, doi `10.1016/bs.ctdb.2016.12.002`,
  PubMed `28527575`.

# Computation over the supplied data

I read the requested-target CSV and found exactly one target, `Nr2f2`. In the
training count CSV, the focal-cell endpoint was strongly sparse:

- 1,674 training perturbations total.
- 1,205 had `n_degs = 0`.
- 469 had a nonzero count.
- Median `n_degs = 0`, 75th percentile `= 1`, 90th percentile `= 2`,
  95th percentile `= 18`, and 99th percentile about `436`.

I then queried the focal-class Parquet rows for mechanistically nearby nuclear
receptors and developmental transcription factors and counted rows with
`pvals_adj < 0.05`. The relevant training perturbations were:

| training perturbation | focal `n_degs` | focal expression-pattern evidence |
|---|---:|---|
| `Nr2f1` | 2 | Closest screened COUP-TF paralog. Only `Sorl1` was increased, log2FC `0.488`, FDR `0.00994`; and `Sema7a` was decreased, log2FC `-0.350`, FDR `0.04075`. Matched counts were 306 perturbed nuclei and 23,679 controls. |
| `Nr2f6` | 0 | Same NR2F subfamily but more immunoregulatory and much less compelling as a neuronal paralog. The most extreme focal rows all had FDR `1.0`; no focal DEG passed 0.05. |
| `Nr2c1` | 0 | Nuclear receptor counterexample; no focal FDR-significant genes. |
| `Nr2c2` | 3 | Another NR2-family nuclear receptor with only three focal DEGs: `Stxbp2`, `Ccdc84`, and `Miga1`, all decreased. This supported a low-count prior for orphan nuclear receptors rather than a broad response. |
| `Rxra`, `Rxrb`, `Rxrg` | 0 each | Retinoid X receptors that can bind related AGGTCA nuclear-receptor response elements were all null in the focal endpoint, arguing against generic retinoid/nuclear-receptor membership as enough for a large count. |
| `Rarb`, `Rarg` | 0 each | Retinoic-acid receptors were likewise null in the focal endpoint. |
| `Thra` | 3 | A nuclear receptor with only a tiny focal hit set, again consistent with most ligand-dependent nuclear receptors being quiet in this cell class. |
| `Rora` | 278 | A useful counterexample, not a close analog: `Rora` is a cell-state nuclear receptor with a large focal response, showing that the assay can detect a TF-like nuclear-receptor perturbation when it is active, but its biology is not the COUP-TF embryonic migration/arealization program. |
| `Tcf7l2` | 106 | A thalamus-relevant developmental TF counterexample. Its broad signature shows that postnatal perturbation of the right thalamic regulator can move this class, but `Tcf7l2` is Wnt-effector/thalamic-patterning biology rather than a NR2F paralog. |
| `Prox1` | 50 | Another developmental TF counterexample with a moderate focal response, used to check that a developmental annotation alone should not force a zero call. |

I also asked whether `Nr2f2` itself emerged as a focal measured gene in other
visible perturbations. It was FDR-significantly increased only in two very
large, generic response-breadth perturbations, `Uba5` with 2,677 focal DEGs
and `Zbtb7a` with 841 focal DEGs; it was weaker and not significant in `Tsc2`
and `Ufc1`. This did not identify a coherent, `Nr2f2`-centered module.

# Target-specific prediction

## `Nr2f2`

`Nr2f2` encodes COUP-TFII, an orphan steroid/thyroid nuclear-receptor-family
transcription factor. It is close to `Nr2f1`/COUP-TFI and can compete with or
antagonize other AGGTCA-binding nuclear receptors at shared response elements
(Qiu et al. 1996). In the developing nervous system, COUP-TF genes have strong
roles in forebrain morphogenesis and interneuron specification (Yang et al.
2017). COUP-TFII is especially tied to embryonic caudal ganglionic eminence,
preoptic-area, and migrating GABAergic interneuron programs: it regulates
tangential migration routes (Tripodi et al. 2004), promotes caudal migration of
CGE-derived cells (Kanatani et al. 2008), marks spatially and temporally
distinct neocortical interneuron subsets (Cai et al. 2013), and can steer
diencephalon-derived GABAergic neurons through a COUP-TFII/Nrp2 switch
(Kanatani et al. 2015).

The closest training analog in the PerturbAI data is the acute `Nr2f1`
perturbation, not the retinoic-acid or ROR receptors. `Nr2f1` transferred in
the same direction in the causal model because both interventions impair a
COUP-TF transcription factor, but the transfer was weak: the published
COUP-TFII programs are largely embryonic, ventral-telencephalic, or
interneuron-migratory, whereas the assay perturbs sparse postnatal neurons and
the requested class is thalamic glutamatergic. In the focal training endpoint
the `Nr2f1` perturbation was already only barely nonzero, with two DEGs, and
the `Sema7a` change is compatible with COUP-TF migration/cue biology but not a
broad postnatal state switch. `Nr2f6`, `Nr2c1`, `Nr2c2`, `Rxra/Rxrb/Rxrg`, and
`Rarb/Rarg` served as near-family counterexamples and were all zero to tiny.
`Rora`, `Tcf7l2`, and `Prox1` showed that this cell class can return tens to
hundreds of DEGs after acute perturbation of an active regulator, but they are
not same-function NR2F comparators.

I therefore predict a tiny positive footprint, lower than or at most comparable
to the `Nr2f1` count. The zero/nonzero decision is mainly driven by the
within-dataset `Nr2f1` result and its plausible `Sema7a` link to COUP-TFII
guidance biology; the downward pull comes from the embryonic/interneuron
emphasis of the external COUP-TFII literature, the focal thalamic
glutamatergic context, and the null behavior of the other screened nuclear
receptors.

Final point prediction: `Nr2f2 = 1` focal DEG.

# Limits and extrapolation

The prediction is an extrapolation because the actual `Nr2f2` expression
signature and count were held out. The closest internal analog, `Nr2f1`, was
itself near the detection boundary, so a count of 0 or 2 would be almost as
plausible as 1. The external literature is strong for developmental COUP-TFII
mechanisms but mostly in embryonic forebrain, caudal ganglionic eminence,
preoptic area, or GABAergic interneuron migration, not in acutely edited
postnatal thalamic glutamatergic neurons. The same-experiment corpus did not
contain a direct exact `Nr2f2` comparator Finding for this run, and the Parquet
and corpus are both representations of the same atlas rather than independent
replication.
