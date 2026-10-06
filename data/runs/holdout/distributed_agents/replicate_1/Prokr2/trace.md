# DEG-count prediction trace

## Question and endpoint

The requested prediction is the number of genes that would pass
Benjamini-Hochberg FDR 0.05 in the held-out `Prokr2` perturbation in
`151 TH Prkcd Grin2c Glut` cells. I treated `n_degs` as an assay- and
power-dependent count of focal-cell Wilcoxon DEGs in recovered nuclei, not as a
direct measure of editing efficiency, biological importance, cell depletion, or
germline developmental severity.

The single requested target was `Prokr2`, in exactly the order supplied by
`single-target request for Prokr2`.
`Prokr2`, its ligand `Prok2`, and the paralogous receptor `Prokr1` were absent
from the visible focal-cell training-count table, so there was no exact
prokineticin ligand/receptor perturbation to copy within the split.

## Sources used

- Declared training endpoint:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared full differential-expression parquet:
  `training differential-expression dataset`.
- Run-local manifest and guards:
  `codex_runtime/pipeline/task_bindings.json`,
  `codex_runtime/pipeline/coverage.json`,
  `codex_runtime/pipeline/capabilities.json`, and
  `codex_runtime/pipeline/measurement_registry.json`.
- PerturbAI July 260713 sourceguard-1773 corpus v1 BioKG. I used it only as a
  same-experiment semantic index and found no visible Finding in which
  `Prokr2` was a comparator; this provided no positive endpoint evidence.
- PubMed-indexed external literature for `PROK2`/`PROKR2` biology:
  Zhao et al. 2018, DOI `10.1016/bs.pmbts.2018.09.006`;
  Prosser et al. 2007, DOI `10.1073/pnas.0606884104`;
  Wen et al. 2019, DOI `10.1002/cne.24719`;
  Wang et al. 2023, DOI `10.1093/hmg/ddad014`.

## Dataset calculations

From the focal-cell training counts I computed the empirical response scale:
1,205 of 1,674 visible perturbations had `n_degs = 0`; the median was 0, the
75th percentile was 1, the 90th percentile was 2, the 95th percentile was 18,
and the largest responses were global RNA processing, proteasome, ubiquitin-like
conjugation, chromatin, or transcriptional regulators rather than ordinary
cell-surface receptors.

I then filtered the full parquet to rows with
`group_name == "151 TH Prkcd Grin2c Glut"` for visible genes that are either
neuropeptide/GPCR analogs, shared second-messenger components, or
GnRH/Kallmann-development counterexamples. For each comparator I counted rows
with `pvals_adj < 0.05`, inspected the most significant rows, and checked the
matched perturbed-nucleus count. The key rows were:

| comparator | relationship to Prokr2 | focal `n_degs` | focal signature evidence |
|---|---|---:|---|
| `Kiss1r` | neuropeptide GPCR, hypothalamic reproductive-axis receptor | 0 | no adjusted p-value below 0.05; 192 perturbed nuclei |
| `Tacr3` | neuropeptide GPCR and hypogonadotropic-hypogonadism gene, but not the Prok2 receptor | 0 | no adjusted p-value below 0.05; 115 perturbed nuclei |
| `Gnrhr` | reproductive-axis GPCR downstream of GnRH | 0 | no adjusted p-value below 0.05; 156 perturbed nuclei |
| `Avpr1a` / `Avpr1b` / `Crhr1` | Gq-coupled neuropeptide GPCRs | 0, 0, 0 | no adjusted p-value below 0.05 despite 183-234 perturbed nuclei |
| `Cckar` / `Cckbr`, `Npy1r` / `Npy2r` / `Npy5r`, `Galr1`, `Sstr5` | other neuropeptide GPCR receptor perturbations assayed in the same cell group | all 0 | no receptor produced a focal-cell FDR-significant downstream gene |
| `Gpr158`, `Gprasp2`, `Gnao1`, `Prkcg` | GPCR-associated genes with one significant DEG each | 1, 1, 1, 1 | the only FDR-significant row for each was its own transcript, so these did not show a propagated transcriptional state |
| `Gnas`, `Gnal`, `Gnb5`, `Rgs6`, `Adcy1`, `Adcy3`, `Adcy5`, `Plcb1`, `Prkca`, `Mapk1`, `Mapk9` | shared GPCR/second-messenger components | all 0 | no adjusted p-value below 0.05 |
| `Ntrk1`, `Ntrk2`, `Ntrk3` | neuronal trophic receptors, broader signaling counterexamples | 0, 3, 0 | `Ntrk2` had only `Ntrk2`, `Atp2a2`, and `Vgf` significant |
| `Fgfr1`, `Chd7`, `Il17rd`, `Flrt3`, `Fezf1`, `Plxna1`, `Otx2`, `Lhx3`, `Lhx4`, `Hesx1` | developmental or GnRH/Kallmann-associated genes closer to `PROKR2` disease biology than to its acute receptor biochemistry | all 0 | no adjusted p-value below 0.05 in this mature thalamic class |

These rows place a Prokr2 perturbation next to two within-dataset facts:
ordinary neuropeptide receptor perturbations were almost always transcriptionally
silent in `151 TH Prkcd Grin2c Glut`, and the developmental genes whose human
phenotypes overlap with `PROKR2` also failed to produce a broad acute signature
in this postnatal thalamic class.

## Target-specific reasoning

### Prokr2

`Prokr2` encodes prokineticin receptor 2, a GPCR activated by prokineticins.
The prokineticin pathway is biologically real in brain: Zhao et al. reviewed
PROK1/PROK2 signaling through PROKR1/PROKR2 and the established roles of
`PROK2`/`PROKR2` loss in idiopathic hypogonadotropic hypogonadism; Wang et al.
showed that many IHH-associated `PROKR2` alleles impair ligand-induced G-alpha-q
signaling. In mouse, Prosser et al. showed that germline `Prokr2` null mutation
alters circadian behavioral and thermoregulatory output from the
suprachiasmatic nucleus, and Wen et al. showed that `Prok2`/`Prokr2` mutants
have severe olfactory-bulb interneuron migration defects.

Those mechanisms do not transfer strongly to this Perturb-seq endpoint. The
experimental intervention here is an acute, sparse, P16 AAV CRISPR loss of
function assayed 3-4 weeks later in recovered NeuN-positive thalamic
glutamatergic nuclei. The developmental `Prokr2` phenotypes occur through
embryonic or SVZ/olfactory migratory programs, and the circadian phenotype is
centered on SCN network output; neither supplies an obligate direct
Prok2-Prokr2 link in the assayed `151 TH Prkcd Grin2c Glut` cells. The causal
chain from intervention to the measured endpoint is therefore:

`Prokr2` editing -> reduced prokineticin receptor signaling, if these thalamic
neurons express and use the receptor -> altered Gq/other downstream signaling
within surviving neurons -> sustained transcriptional state at P37-P44 -> BH
FDR-significant genes. The weak link is the cell-context and time-window
exposure: the known large `Prokr2` phenotypes are not broad cell-autonomous
transcriptional programs in juvenile thalamic glutamatergic neurons.

The visible training perturbations reinforce the null prediction. `Kiss1r`,
`Tacr3`, and `Gnrhr` are better reproductive-axis neuropeptide receptor analogs
than global regulators, yet all had zero DEGs in the focal class. The
Gq/neuropeptide receptor panel (`Avpr1a`, `Avpr1b`, `Crhr1`, `Cckar`, `Cckbr`,
`Galr1`, `Npy1r`, `Npy2r`, `Npy5r`, `Sstr5`) was also entirely zero. More
generic signaling genes were also quiet: `Gnas`, `Gnal`, `Gnb5`, `Rgs6`,
`Adcy1`, `Adcy3`, `Adcy5`, `Plcb1`, `Prkca`, `Mapk1`, and `Mapk9` had no
significant focal-cell rows. The one nearby nonzero neurotrophic receptor,
`Ntrk2`, had only three DEGs and is a receptor tyrosine kinase with a known
neurotrophin-responsive `Vgf` output, not a direct prokineticin substitute.

I therefore predicted `Prokr2` to be below the FDR-significant boundary rather
than assigning a small positive count. The point prediction is:

| target | predicted `n_degs` |
|---|---:|
| `Prokr2` | 0 |

## Limits and uncertainty

- The exact ligand and receptor analogs, `Prok2` and `Prokr1`, were not visible
  training targets in this split; the closest within-dataset analogs are
  receptor-class and disease-neighborhood comparators rather than an obligate
  same-pathway transfer.
- External `PROKR2` evidence is strong for GnRH neuron development, olfactory
  bulb interneuron migration, and SCN circadian physiology, but it is mostly
  germline, developmental, or SCN-specific. It is therefore context evidence,
  not direct support for a focal thalamic DEG count.
- Matched focal-cell perturbed-nucleus counts for the receptor comparators were
  generally in the 100-300 range, so a weak `Prokr2` transcriptional shift could
  remain underpowered. The prediction is a point estimate of zero FDR 0.05 DEGs,
  not a claim that `Prokr2` is irrelevant in every neuron or that CRISPR editing
  would fail.
- The PerturbAI July corpus and BioKG are structured interpretations of the
  same experiment, not independent replication; their absence of a `Prokr2`
  comparator record was only used to check whether there was an obvious
  same-experiment semantic bridge.
