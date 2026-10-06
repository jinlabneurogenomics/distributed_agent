# Prediction trace

## Question and endpoint

I interpreted the task as a point prediction of `n_degs` for the held-out
perturbation `Uqcrc1` in `151 TH Prkcd Grin2c Glut` thalamic glutamatergic
neurons. `n_degs` counts all measured genes whose Wilcoxon
Benjamini-Hochberg-adjusted p-value is below 0.05 in that cell group after the
gene-targeting AAV CRISPR perturbation. The held-out `Uqcrc1` rows are absent
from both the parquet and the training count table, so the requested endpoint
is absent for `Uqcrc1`; the training count table directly observes the same
endpoint for non-held-out perturbations and the parquet directly observes the
per-gene DE patterns behind those training counts.

I counted the target transcript itself when present, because the supplied
training endpoint is simply `pvals_adj < 0.05` across measured genes and does
not exclude `names == gene_target`.

## Sources used

- Declared DE parquet:
  `training differential-expression dataset`.
  I queried it only for the focal cell group and a small respiratory-chain
  comparator set.
- Declared focal-cell training count CSV:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared held-out-target manifest:
  `single-target request for Uqcrc1`.
- Dataset metadata generated for this run:
  `codex_runtime/pipeline/dataset_context.md`,
  `codex_runtime/pipeline/task_bindings.json`,
  `codex_runtime/pipeline/coverage.json`,
  `codex_runtime/pipeline/capabilities.json`, and
  `codex_runtime/pipeline/measurement_registry.json`.
- Same-experiment semantic layer:
  `perturbai-july-260713-sourceguard-1773-v1` Findings corpus and its BioKG
  projection. I used this corpus to read packaged interpretations of visible
  complex-III comparators such as `Uqcrc2`, `Uqcrb`, `Cyc1`, and `Ttc19`.
  The BioKG query was used only to navigate explicit comparators in the
  `Uqcrc2` report; graph relation presence and multiplicity were not used as
  quantitative evidence.
- External gene-function references:
  - MitoCarta3.0 places UQCRC1, UQCRC2, UQCRB, UQCRFS1, UQCRH, UQCRQ, and
    CYC1 in mitochondrial oxidative phosphorylation / complex III
    annotations (Rath et al. 2021, Nucleic Acids Research,
    DOI 10.1093/nar/gkaa1011, PMID 33174596).
  - The UQCRFS1 precursor is incorporated last into complex III and its
    N-terminal fragment lies between the two core subunits UQCRC1 and UQCRC2;
    TTC19 acts in quality control of this UQCRFS1-containing complex-III
    state (Fernandez-Vizarra and Zeviani 2018, Cell Cycle,
    DOI 10.1080/15384101.2017.1417707, PMID 29243944).
  - Rare UQCRC1 variants impair complex-III activity and mitochondrial
    ultrastructure in cellular, fly, and mouse Parkinsonism models
    (Lin et al. 2020, Brain, DOI 10.1093/brain/awaa279, PMID 33141179).
  - Depleting UQCRC1 in human neuronal cells and flies can release
    cytochrome c and activate a caspase-dependent neurodegenerative program
    (Hung et al. 2021, Cell Reports, DOI 10.1016/j.celrep.2021.109729,
    PMID 34551295).

## Dataset calculations

I first read the held-out CSV and found a single requested row,
`target_name = Uqcrc1`. In the 1,674 non-held-out focal-cell training
perturbations, the response-breadth endpoint is highly sparse: the median is
0, the 75th percentile is 1, and 1,205 perturbations have no FDR 0.05 DEGs.
Thus complex membership or broad essentiality should not by itself imply a
large count in this assay.

I then pulled visible respiratory-chain comparators from the training count
CSV. The closest same-complex panel was:

| comparator | relationship to Uqcrc1 | focal `n_degs` |
| --- | --- | ---: |
| `Uqcrc2` | second complex-III core subunit | 1 |
| `Uqcrb` | complex-III subunit | 0 |
| `Uqcrfs1` | complex-III Rieske Fe-S subunit | 0 |
| `Uqcrh` | complex-III hinge subunit | 0 |
| `Uqcrq` | complex-III subunit | 1 |
| `Cyc1` | complex-III cytochrome c1 subunit | 1 |
| `Ttc19` | complex-III assembly / quality-control factor | 1 |

The mean of this direct complex-III group is 0.57 and its maximum is 1 DEG.
Other visible OXPHOS genes were similarly weak: 23 `Nduf*` complex-I genes
had 11 total focal DEGs, all as 0 or 1, and the visible cytochrome-c-oxidase
structural genes were also 0 or 1. The main mitochondrial outlier among the
queried comparators was `Opa1` with 37 focal DEGs. I treated `Opa1` as a
positive control that the snRNA/Wilcoxon workflow can detect a mitochondrial
ATF4/ISR-like stress state, not as a close phenocopy of complex-III subunit
loss, because OPA1 controls inner-membrane fusion and cristae organization
rather than occupying complex III.

For the focal cell group I also queried the parquet for the best per-gene DE
rows of these analog perturbations. `Uqcrc2`, `Cyc1`, `Ttc19`, `Cox5a`,
`Sdha`, `Ndufs2`, and `Park7` each had exactly one significant focal gene and
in each case that gene was the perturbed transcript itself. `Uqcrc2` had
`Uqcrc2` down at log2FC -0.576 and FDR 0.003 in 142 matched perturbed nuclei.
`Cyc1` had self down at log2FC -0.739 and FDR 2.94e-15 in 221 nuclei, and
`Ttc19` had self down at log2FC -0.517 and FDR 1.42e-22 in 267 nuclei.
By contrast, `Uqcrfs1`, `Uqcrb`, and `Uqcrh` had no focal FDR 0.05 gene.
`Uqcrq` had one FDR 0.05 gene, `Gpr180`, while `Uqcrq` itself was not
significant. Pairwise focal log-fold-change correlations between `Uqcrc2` and
`Uqcrb`, `Uqcrq`, `Uqcrfs1`, `Uqcrh`, `Cyc1`, and `Ttc19` ranged from 0.60 to
0.70 over all measured genes, but the same-complex targets did not share a
multi-gene FDR-significant stress module.

The July Findings corpus makes the same point at report level. Its `Uqcrc2`
report describes `Uqcrc2` as downstream-null in represented neuronal groups:
the canonical ATF4/ATF5, `Ddit3`, `Asns`, `Chac1`, `Slc7a5`, one-carbon,
chaperone/protease, redox, and mitophagy sentinels had minimum FDR 1.0 after
`Uqcrc2`. The same report explicitly compared `Uqcrc2` with `Uqcrb`,
`Uqcrfs1`, `Uqcrh`, `Uqcrq`, `Cyc1`, and `Ttc19` and concluded that
represented complex-III relatives were nearly flat rather than revealing a
hidden common program. `Ttc19` and `Uqcrb` reports independently described
the same lack of a generic complex-III nuclear stress signature; their rare
non-self hits were private singleton events in other cell groups. These are
same-experiment interpretations of the visible parquet, not independent
replication.

## Target-specific causal transfer

### Uqcrc1

`Uqcrc1` encodes a nuclear complex-III core subunit. The expected perturbation
chain is:

`Uqcrc1` CRISPR loss of function -> reduced or mutant UQCRC1 in a subset of
postmitotic neurons -> impaired or partly destabilized complex-III assembly
and electron transfer, especially through the core-subunit scaffold shared
with UQCRC2 -> possible mitochondrial stress, redox signaling, apoptosis, or
selective loss before capture -> nuclear RNA profile among surviving
`151 TH Prkcd Grin2c Glut` nuclei.

The closest training perturbation is `Uqcrc2`, because UQCRC1 and UQCRC2 are
the pair of large complex-III core subunits and the UQCRFS1 processing
intermediate is physically placed between them. That is a same-limiting-machine
prior: impairing either core subunit should push complex-III assembly or
stability in the same direction. In the actual Perturb-seq assay, however,
`Uqcrc2` produced only one focal DEG, its own transcript, and the internal
report found no downstream FDR 0.10 response across represented neuronal
groups. The other complex-III structural/assembly analogs bracket that result:
`Cyc1` and `Ttc19` were also self-only with one focal DEG, `Uqcrq` had only
one unrelated focal DEG, and `Uqcrb`, `Uqcrfs1`, and `Uqcrh` were focal-null.

External biology raises the prior that stronger UQCRC1 loss can be
pathogenic. Human Parkinsonism variants and neuronal depletion studies link
UQCRC1 to complex-III dysfunction, cytochrome-c release, and neuronal
degeneration. Those systems used stronger alleles, cell lines, flies, or
longer disease models, so they do not override the sparse P16 mosaic mouse
snRNA evidence. The visible same-complex perturbations say that acute partial
complex-III lesions did not cross the threshold for a broad ATF4/ISR, redox,
mitophagy, or compensatory OXPHOS transcriptomic response in recovered
juvenile neurons. Severe early selection could in principle remove affected
neurons before snRNA-seq, but the supplied DE endpoint only counts genes in
surviving captured nuclei.

I therefore predicted the same focal response breadth as the closest core
subunit, `Uqcrc2`: a nonzero but self-only count of **1 DEG**. A true zero is
plausible if `Uqcrc1` target RNA was less detectably depleted than `Uqcrc2`;
a count above a few genes would require `Uqcrc1` to breach a stress threshold
that `Uqcrc2`, `Uqcrb`, `Uqcrfs1`, `Uqcrh`, `Uqcrq`, `Cyc1`, and `Ttc19` did
not breach.

## Limits

The prediction is an extrapolation because the requested `Uqcrc1`
differential-expression signature was fully held out and no exact
same-experiment `Uqcrc1` report was available. The strongest analog,
`Uqcrc2`, is biochemical rather than a measured `Uqcrc1` phenocopy. The
parquet measures nuclear RNA in recovered nuclei only; it does not measure
UQCRC1 protein, complex-III activity, oxygen consumption, ROS, ATP, apoptosis,
or cell loss. The self-transcript contribution is also stochastic across guide
sets in this mosaic CRISPR experiment, so one DEG rather than zero is a
low-resolution call near the assay floor.
