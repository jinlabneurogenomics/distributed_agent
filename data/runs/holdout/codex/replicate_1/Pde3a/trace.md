# Direct forecast for Pde3a in 151 TH Prkcd Grin2c Glut

Predicted `n_degs`: **0**

## Evidence used

### Held-out target biology

The one-row holdout manifest names `Pde3a`; the biology-only bundle is for the
same target and exposes no target DEG count or target expression signature.

The exact focal-population reach of `Pde3a` is very sparse in non-target
controls from `151 TH Prkcd Grin2c Glut`:

| quantity | value |
| --- | ---: |
| non-target nuclei | 23,679 |
| nuclei with `Pde3a` UMI | 671 |
| percent expressing | 2.8337% |
| mean raw UMI | 0.03839 |
| mean log1p CP10k | 0.01595 |
| pseudobulk CPM | 2.40594 |

The biological prior is also weak for a class-wide 3-4 week nuclear RNA
signature. `Pde3a` encodes a cyclic-nucleotide phosphodiesterase; a P16
disruptive edit should stop new PDE3A synthesis, but pre-edit catalytic protein
can remain active until turnover. The only target-specific protein-clearance
observation in the bundle is stress-induced cardiomyocyte degradation, which
does not establish basal clearance in juvenile thalamic neurons. The established
single-gene mouse phenotype is reproductive rather than postnatal neuronal, and
the bundle only supports low adult thalamic expression plus unquantified adult
forebrain neuronal/endothelial PDE3A localization.

### Training counts selected by biology

The declared training count table has 1,674 measured targets for this same
`151 TH Prkcd Grin2c Glut` endpoint. It is zero-heavy: 1,205/1,674 targets
have `n_degs = 0`, and 1,481/1,674 have `n_degs <= 1`.

The closest assayed PDE-family training perturbations are all exact zeros in
the same endpoint:

| training target | same-class `n_degs` |
| --- | ---: |
| `Pde1c` | 0 |
| `Pde4b` | 0 |
| `Pde4d` | 0 |
| `Pde10a` | 0 |

Other proximal cAMP/cyclic-nucleotide signaling targets were likewise flat or
self-only in this focal class:

| training target | same-class `n_degs` |
| --- | ---: |
| `Adcy1` | 0 |
| `Adcy3` | 0 |
| `Adcy5` | 0 |
| `Gnas` | 0 |
| `Rapgef2` | 0 |
| `Rapgef4` | 0 |
| `Prkaca` | 1 |
| `Prkar1a` | 1 |

Scanning the declared expression Parquet for these matched same-class training
rows confirmed that the PDE comparators had no hidden near-FDR signal:

| target | BH < 0.05 | BH < 0.10 | minimum BH-adjusted p |
| --- | ---: | ---: | ---: |
| `Pde1c` | 0 | 0 | 0.180 |
| `Pde4b` | 0 | 0 | 0.922 |
| `Pde4d` | 0 | 0 | 1.000 |
| `Pde10a` | 0 | 0 | 0.304 |
| `Adcy1` | 0 | 0 | 0.139 |
| `Adcy3` | 0 | 0 | 0.112 |
| `Adcy5` | 0 | 0 | 0.912 |

The only significant `Prkaca` and `Prkar1a` rows in this same Parquet slice were
their own target transcripts, so those rows do not show a transferred downstream
cAMP/CREB program in the class.

### Same-experiment corpus context

The same-experiment Findings, which are packaged interpretations of the same
Perturb-seq experiment rather than independent replication, supported the
training-table readout:

| Finding | bearing |
| --- | --- |
| `Pde1c:F001`, `Pde4d:F001` | pan-recovered neuronal null/buffered PDE responses |
| `Pde4b:F004` | `Pde4b` loss did not induce a detectable cAMP/CREB immediate-early transcriptional program |
| `Prkaca:F001`, `Prkar1a:F001` | PKA perturbations were downstream-null across their recovered neuronal groups |
| `Adcy1:F005`, `Adcy5:F003` | represented transmembrane adenylyl cyclases shared absence of downstream DE |
| `Rapgef4:F001` | EPAC/Rap signaling was flat across recovered neuronal groups |

## Synthesis

The generic class prior is already concentrated at zero, and the biology-matched
training subset is even more concentrated there: all exposed PDE comparators and
adenylyl cyclases were exact zeros in `151 TH Prkcd Grin2c Glut`, while PKA
gave only self-transcript hits. The two visible nuclear CREB/CBP examples
(`Creb1`, `Crebbp`) are downstream transcriptional regulators and are less
proximal to `Pde3a` than the PDE and upstream cAMP controls.

I therefore expect any P16 `Pde3a` edit in this class to be diluted by very low
target reach, possible persistence of pre-edit enzyme, pathway buffering, and
the general failure of basal cyclic-nucleotide perturbations to create a broad
survivor-state RNA signature. Those features make a zero-count result more
likely than a singleton self-transcript result or a small downstream response.

I did not inspect the held-out `Pde3a` target outcome.
