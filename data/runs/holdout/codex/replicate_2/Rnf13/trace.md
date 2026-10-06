# Rnf13 DEG-count forecast

## Target and endpoint

- Target: `Rnf13`
- Focal population: `151 TH Prkcd Grin2c Glut`
- Endpoint: number of measured genes with BH-adjusted Wilcoxon `p < 0.05`
- Forecast: `1`

## Biology used

The declared target bundle identifies RNF13 as a PA-TM-RING E3 ubiquitin
ligase with full-length endosomal-membrane and processed cytoplasmic pools.  In
mouse hippocampus, RNF13 ubiquitinated snapin in a pathway linked to
snapin-SNAP25 association and SNARE-complex assembly; constitutive
`Rnf13`-null mice had adult hippocampal synaptic-vesicle, active-zone,
SNARE-assembly, and learning phenotypes.  The direct phenotype is therefore
neural and synaptic, but it is hippocampal and constitutive rather than an
acute P16 loss in thalamic glutamatergic neurons.

The functional-stock card calls post-edit RNF13 stock likely substantially
depleted by the P37-P44 harvest: editing should not remove pre-existing
protein instantly, but RNF13 is proteolytically processed and its ligase pools
should require renewal across the 21-28 day assay window.  The same bundle also
marks the relevant uncertainties: no acute neuronal half-life, no timed
conditional knockout, unresolved same-context compensation by related
PA-TM-RING proteins, and unresolved separation of adult postnatal demand from
developmental installation.

Exact focal-population expression supports reach in the assayed cells rather
than a pure absence prior: in matched non-target nuclei from `151 TH Prkcd
Grin2c Glut`, `Rnf13` had mean CP10k 0.855, mean raw UMI 1.413, and was
detected in 16,324 of 23,679 nuclei, or 68.94%.

## Training measurements used

The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` table contains
1,674 non-held-out training targets.  It is extremely zero-heavy in this focal
class:

- `n_degs = 0`: 1,205 targets
- `n_degs = 1`: 276 targets
- median: 0
- 75th percentile: 1
- 90th percentile: 2

The nearest PA-TM-RING family genes named in the Rnf13 bundle were absent from
the training count table, so I used broader, observed controls around the
curated biology: synaptic active-zone/SNARE genes, endocytic machinery, and
ubiquitin/proteostasis perturbations.  Their focal counts stayed very low:

| observed training target | rationale | `n_degs` |
| --- | --- | ---: |
| `Bsn` | synaptic active-zone control | 0 |
| `Pclo` | synaptic active-zone control | 0 |
| `Nsf` | SNARE disassembly machinery | 0 |
| `Stx1b` | synaptic syntaxin/SNARE family | 0 |
| `Stxbp1` | synaptic vesicle fusion regulator | 1 |
| `Syp` | synaptic vesicle marker/regulator | 1 |
| `Stx16` | syntaxin/endosomal traffic | 1 |
| `Stx5a` | syntaxin/trafficking family | 0 |
| `Cltc` | clathrin/endocytosis | 3 |
| `Ube3a` | neural E3 ubiquitin ligase | 0 |
| `Cblb` | E3 ubiquitin ligase | 0 |
| `Vcp` | ubiquitin-proteostasis machinery | 2 |

I then compared those 12 observed profiles in the training Parquet after
filtering to `group_name == "151 TH Prkcd Grin2c Glut"`, using signed
`logfoldchanges` and `pvals_adj < 0.05` as the significance annotation.  All
12 profiles were available.  Seven had no significant feature and five had
only 1 to 9 significant features in the profile-comparison summary.  Across
the 66 selected training-target pairs, top-tail sharing was weak: mean
positive-tail overlap coefficient 0.038 and mean negative-tail overlap
coefficient 0.066, with no positive significant-program overlap and zero
negative significant-program overlap among the non-null overlaps.  Thus the
observed training perturbations closest to the Rnf13 mechanism define a
low-count scale reference, not a conserved high-count thalamic response.

## Synthesis

Rnf13 should be expressed and functionally reachable in many recovered nuclei,
so I did not round down to an assured transcriptional null.  The biology,
however, points mainly to post-translational endosomal/synaptic-vesicle
regulation, and the best neural loss evidence is a constitutive hippocampal
phenotype rather than an acute thalamic transcriptional state.  In the actual
focal training table, nearby SNARE/synaptic and ubiquitin/endocytic
perturbations are almost all at 0, 1, 2, or 3 DEGs, while the whole table has
75% of perturbations at at most one DEG and 90% at at most two DEGs.

I therefore placed `Rnf13` just above zero to allow one isolated significant
measured gene from a reachable but narrow perturbation, while excluding the
long high-count tail reserved for core RNA-processing, proteasome, UFMylation,
or broad transcriptional regulators such as `Uba5`, `Tpr`, `Sin3a`, `Ufc1`,
and `Psmb4`.  No withheld `Rnf13` expression signature or target DEG count was
used.
