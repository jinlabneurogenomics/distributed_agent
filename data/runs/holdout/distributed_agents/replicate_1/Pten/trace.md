# Question and endpoint

The requested held-out perturbation was `Pten` in `151 TH Prkcd Grin2c Glut`
cells. I interpreted the prediction target as an assay-specific scalar:

`n_degs = count(pvals_adj < 0.05)` for measured genes in the focal thalamic
glutamatergic group after acute postnatal AAV-CRISPR loss of the target gene.

Zero therefore means no measured gene is expected to pass the Scanpy Wilcoxon
BH-FDR threshold in this cell group; a nonzero value means a detectable
transcriptional response breadth, not a viability, editing-efficiency, or target
expression estimate. `Pten` was absent from both supplied training tables and
from the selected July PerturbAI same-experiment semantic graph, so its count
had to be transferred from non-held-out perturbations plus external molecular
knowledge.

# Sources used

- Declared training endpoint file:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared differential-expression parquet:
  `training differential-expression dataset`.
- Requested-target manifest:
  `single-target request for Pten`.
- Internal same-experiment corpus checked for coverage: PerturbAI July
  `july_260713_sourceguard_1773_v1`. The run-local coverage file had no matched
  target for `Pten`; a BioKG lookup found no `Pten` TargetGene node; and
  story-count queries for `Tsc2`, `Mtor`, `Rheb`, `Pik3ca`, and `Akt1` returned
  no packaged Findings. I therefore did not use corpus graph topology or Finding
  text as endpoint evidence.
- External biological priors:
  Bar-Peled et al. 2013, Science, DOI `10.1126/science.1232044`, PMID
  `23723238`, for DEPDC5/NPRL2/NPRL3 GATOR1 as a GAP complex that negatively
  regulates Rag-dependent mTORC1 recruitment and signaling.
  Weston et al. 2014, Frontiers in Molecular Neuroscience, DOI
  `10.3389/fnmol.2014.00001`, PMID `24574959`, for direct comparison of neuronal
  `Pten` and `Tsc1` loss: both increase mTORC1 signaling and neuronal size, but
  `Pten` also elevates AKT signaling and gives synaptic effects that are not
  identical to `Tsc1`.
  LaSarge and Danzer 2014, Frontiers in Molecular Neuroscience, DOI
  `10.3389/fnmol.2014.00018`, PMID `24672426`, for PTEN, TSC1, and TSC2 as
  established negative regulators whose loss produces mTOR hyperactivation and
  neuronal hyperexcitability phenotypes.
  D'Amore et al. 2025, Molecular Psychiatry, DOI
  `10.1038/s41380-025-02916-2`, PMID `39953287`, for neuron-specific `Pten`
  deletion increasing AKT/mTORC1-linked signaling and inducing a cortical
  transcriptome broader and partly different from neuron-specific `Tsc2`
  deletion.

# Dataset calculations

I used the training count CSV to calibrate the scale in the exact focal cell
class. It contained 1,674 non-held-out perturbations. The distribution was
highly zero-inflated and heavy-tailed:

| summary | value |
| --- | ---: |
| median `n_degs` | 0 |
| 75th percentile | 1 |
| 90th percentile | 2 |
| 95th percentile | 18 |
| 99th percentile | 436 |
| maximum | 2677 |
| nonzero targets | 469 / 1674 |
| targets with at least 50 DEGs | 59 / 1674 |

I then queried the parquet only for `151 TH Prkcd Grin2c Glut` rows for
mechanistically chosen PI3K/AKT/mTOR targets. The relevant operation was:

```python
ds.dataset(training_parquet).to_table(
    columns=[
        "names", "gene_target", "logfoldchanges", "pvals_adj", "scores",
        "n_pert_matched", "n_ctrl_matched",
    ],
    filter=(
        (pc.field("group_name") == "151 TH Prkcd Grin2c Glut")
        & pc.field("gene_target").isin(targets)
    ),
)
```

This exact extraction reproduced the training counts and gave matched focal
cell sample sizes:

| training perturbation | role relative to PTEN | `n_degs` | perturbed nuclei |
| --- | --- | ---: | ---: |
| `Tsc2` | closest assayed negative regulator of Rheb/mTORC1 | 86 | 177 |
| `Depdc5` | GATOR1 negative regulator of Rag/mTORC1 | 13 | 121 |
| `Mtor` | mTOR kinase; loss is opposite-sign to PTEN loss at mTORC1 | 2 | 188 |
| `Rptor` | mTORC1 scaffold; loss is opposite-sign to PTEN loss at mTORC1 | 0 | 173 |
| `Akt3` | positive PI3K/AKT signal transducer, not a PTEN-loss phenocopy | 0 | 159 |
| `Pik3cb` | class I PI3K catalytic subunit, opposite to PTEN loss | 0 | 123 |
| `Pik3r1` | class I PI3K regulatory subunit, opposite to PTEN loss | 0 | 154 |
| `Pik3r2` | class I PI3K regulatory subunit, opposite to PTEN loss | 0 | 117 |
| `Strada` | LKB1/AMPK-axis mTOR modulator, indirect | 0 | 110 |
| `Sos1` | Ras exchange factor upstream of MAPK/PI3K | 0 | 146 |
| `Mapk1` | ERK2, parallel MAPK output | 0 | 156 |

The `Tsc2` DEG set was the only broad directly relevant footprint. Its leading
focal-cell changes included `Nrbp2` down, `Cyp51` up, `Pik3r3` up, `Nefm` up,
`Slc2a6` up, `Dusp1` up, `Amy1` down, and `Snhg11` down. `Depdc5` recapitulated
the direction of several of the same genes despite lower power and lower DEG
burden: eight of its 13 significant genes were also significant in `Tsc2`
(`Amy1`, `Ldlr`, `Msmo1`, `Pik3r1`, `Pik3r3`, `Rnpc3`, `Snhg11`, `Tubb3`), and
all eight had the same sign in the two perturbations.

As a falsification step, I also scanned every training perturbation over the 86
`Tsc2`-significant genes and computed the Pearson correlation of log-fold
changes with the `Tsc2` vector. `Depdc5` was the only high-similarity hit with
a direct negative-regulator relationship to mTORC1. Some larger responses, such
as `Rab7` with 501 DEGs and `Psmc1` with 430 DEGs, also correlated with the
`Tsc2` signature over those genes, but they perturb endolysosomal/proteasomal
state rather than the PIP3 -> AKT -> TSC2 -> Rheb inhibitory chain. I treated
them as evidence that the observed `Tsc2` module is partly a growth and
metabolic stress program that can be reached by other routes, not as quantitative
PTEN analogs.

# Target-specific causal transfer

## `Pten`

**Causal model.** The intended intervention is acute loss of PTEN in sparse
postnatal neurons. PTEN normally dephosphorylates PIP3 and opposes class-I
PI3K, limiting AKT activation. AKT inactivates the TSC1/TSC2/TBC1D7 GAP,
permitting Rheb-GTP to stimulate mTORC1; PTEN loss should therefore increase
AKT signaling, inhibit TSC function, and activate mTORC1. That is the same
downstream direction as `Tsc2` loss at Rheb/mTORC1, and also the same broad
endpoint direction as `Depdc5` loss at amino-acid/Rag-dependent mTORC1
activation. It is the opposite molecular direction from loss of `Mtor` or
`Rptor`, and it is not well mimicked by loss of PI3K or AKT positive regulators.

**Training analogs and counterexamples.** `Tsc2` is the strongest assayed
same-direction comparator and set the main count scale at 86 DEGs. The overlap
between `Tsc2` and `Depdc5`, especially induction of `Pik3r3`, `Pik3r1`, `Ldlr`,
`Msmo1`, and tubulin/neurofilament-associated genes, supports a recurrent
mTORC1-negative-regulator transcriptional program in this focal cell type, but
`Depdc5` had only 13 DEGs and 121 matched perturbed nuclei, so it argues for a
detectable response without forcing a much larger count. The near-null
`Mtor`/`Rptor` rows do not contradict a PTEN/TSC2-like prediction because loss
of a required mTORC1 component should reduce signaling rather than release the
Rheb brake. The `Akt3`, `Pik3cb`, `Pik3r1`, and `Pik3r2` null rows also are
opposite-sign or redundant positive-regulator losses rather than loss of the
negative phosphatase.

**External mechanism.** Published neuronal models support transfer from TSC
loss to PTEN loss because both interventions activate mTORC1 and enlarge
neurons, while also warning that PTEN is not simply another TSC subunit:
neuronal `Pten` loss can elevate AKT and induce synapse, extracellular-matrix,
and myelination programs that differ from `Tsc2` loss. I therefore placed PTEN
slightly above the observed `Tsc2` breadth rather than at the lower `Depdc5`
value, but still in the same order of magnitude because the assay used a sparse
postnatal mosaic CRISPR exposure and neither `Mtor` nor the assayed PI3K genes
showed broad loss-of-function signatures in this cell group.

**Prediction.** I predict a nonzero response and a broad but not extreme
footprint: `96` DEGs.

# Limits

The endpoint itself is directly observed for `Tsc2`, `Depdc5`, `Mtor`, `Rptor`,
and PI3K/AKT counterexamples, but it is absent for the held-out `Pten`
perturbation. The PTEN estimate is therefore a mechanistic interpolation from
related negative regulators, not a measured or cross-validated count. `Tsc1`
and `Rheb`, which would have been even more direct same-chain comparators, were
not in the training endpoint table. External neuronal PTEN/TSC experiments used
different Cre drivers, ages, brain regions, and often stronger biallelic loss
than the AAV-PHP.eB mosaic CRISPR design here; I used them to establish causal
direction, not to import absolute DEG counts. The `Tsc2` and `Depdc5`
expression-pattern overlap is same-experiment evidence from the same parquet,
so it is not independent replication.
