# Question

I interpreted the task as a point prediction of the held-out focal-cell DEG
burden for `Hmgb1`, with
`n_degs = count(pvals_adj < 0.05)` in `151 TH Prkcd Grin2c Glut` nuclei.  The
training endpoint CSV is direct evidence for that exact count in non-held-out
perturbations.  The all-cell differential-expression Parquet is direct evidence
for the expression signatures of those same non-held-out perturbations.  The
`Hmgb1` perturbation itself is absent from both files by design, so any estimate
for it is extrapolation from training targets plus external gene-function
knowledge.

# Sources

- Declared training DEG counts:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
  This table had 1,674 unique training targets.  Its focal-cell counts were
  highly sparse: median 0, 75th percentile 1, 90th percentile 2, 95th
  percentile 18, and mean 14.1 DEGs.
- Declared differential-expression Parquet:
  `training differential-expression dataset`.
  I queried exact focal-cell rows for mechanistically chosen training targets,
  ordered by adjusted Wilcoxon p value, and checked that no `Hmgb1`,
  `Hmgb2`, `Hmgb3`, `Hmgb4`, `Hmgn*`, or `Hmga*` perturbation was represented.
- Run-local manifest:
  `single-target request for Hmgb1`.
  It contains exactly one requested target, `Hmgb1`, with no duplicate and no
  overlap with the training-count CSV.
- Internal same-experiment interpretation: PerturbAI July 260713 sourceguard
  1773 v1 Findings ledger.  I used it only for packaged interpretation of
  visible training comparators such as `Baz1b`, `Chd2`, `H3f3a`, and `Setd2`;
  it is a semantic layer over the same experiment, not an independent
  replicate.
- External literature:
  - Calogero et al. 1999, Nature Genetics, DOI 10.1038/10338, PMID 10391216:
    germline `Hmg1`/`Hmgb1`-null mouse pups are born alive but die of neonatal
    hypoglycaemia; the protein is a chromatin architectural factor needed for
    particular transcription-factor outputs rather than gross cell growth.
  - Stros 2010, Biochimica et Biophysica Acta, DOI
    10.1016/j.bbagrm.2009.09.008, PMID 20123072: HMGB proteins are abundant
    HMG-box DNA chaperones that bend/loop DNA, bind nucleosomes dynamically,
    compete with histone H1, and influence transcription, replication,
    recombination, repair, and genome stability.
  - Lange and Vasquez 2009, Molecular Carcinogenesis, DOI 10.1002/mc.20544,
    PMID 19360789: HMGB1 binds distorted or damaged DNA and participates in
    multiple DNA-repair contexts.
  - Tang et al. 2023, Nature Reviews Immunology, DOI
    10.1038/s41577-023-00894-6, PMID 37322174: HMGB1 also has cytosolic and
    extracellular stress and innate-immune roles.  Those functions are less
    directly sampled here because the assay is NeuN-enriched neuronal nuclei
    from recovered cells, with glia and immune cells largely absent.

# Computational Basis

I first confirmed the requested set and training split:

```text
requested target: Hmgb1
requested duplicates: 0
training duplicates: 0
requested/training overlap: empty
```

Then I queried the focal cell group in the Parquet for all biologically
plausible comparators.  The most relevant exact paralogs or HMG-domain
architectural perturbations were unavailable: no represented `Hmgb*`, `Hmgn*`,
or `Hmga*` perturbation appeared in either the focal count table or the
Parquet.  `Hmgcr` was the only `Hmg`-prefixed target and is a cholesterol
biosynthesis enzyme, not a chromatin analog.

The focal-cell DEG counts I used as the local scale were:

| training target | focal `n_degs` | why it was inspected |
|---|---:|---|
| `H3f3a` | 0 | core H3.3 histone gene; tests an abundant chromatin component with known buffering by a paralog |
| `H2ac8` | 0 | replication-dependent core histone gene; weak analog but useful as a redundant nucleosomal-component counterexample |
| `H4c11` | 0 | replication-dependent core histone gene; weak analog but useful as a redundant nucleosomal-component counterexample |
| `Set` | 0 | nonenzymatic chromatin-associated histone chaperone/inhibitor protein |
| `Baz1b` | 1 | non-ATPase WICH chromatin-remodeling component with a direct self-transcript DEG but almost no downstream cascade |
| `Setd2` | 1 | chromatin regulator whose broad canonical programs were buffered in this juvenile neuronal assay |
| `Chd2` | 34 | positive counterexample: a disease-linked ATP-dependent chromatin remodeler can make a real but still moderate 151 TH signature |
| `Chd4` | 100 | broader NuRD remodeler counterexample |
| `Chd8` | 61 | broader CHD-family counterexample |
| `Smarcc2` | 185 | broad BAF-complex counterexample |
| `Setd1a` | 368 | broad H3K4 methyltransferase-complex counterexample |
| `Sin3a` | 1433 | very broad scaffolded HDAC-corepressor counterexample |

The focal expression rows supported the same separation.  `H3f3a`, `H2ac8`,
`H4c11`, and `Set` had no adjusted p value below 0.05; their best focal rows
had FDR values of 1.0, 0.96, 1.0, and 0.66 respectively.  `Baz1b` had a strong
self-transcript decrease (`log2FC = -0.68`, FDR `5.32e-09`) but only one focal
DEG, so a verified target-RNA change did not expand into a broad secondary
signature.  `Setd2` had only one focal DEG, `Septin5`, in the packaged report.
By contrast, `Chd2`, `Chd4`, `Chd8`, `Setd1a`, `Smarcc2`, and `Sin3a` all had
clear focal signatures headed by genes with FDR values between `1e-11` and
`1e-34`; these are useful upper counterexamples but not tight HMGB1 analogs
because they disrupt enzymatic or multi-subunit remodeler/corepressor
machinery.

# Target-specific Reasoning

## Hmgb1

HMGB1 is an abundant non-histone HMG-box chromatin protein.  It binds bent DNA
and linker/nucleosomal DNA dynamically and acts as a DNA chaperone rather than
as a single obligate subunit of an ATP-dependent remodeler or a histone
methyltransferase complex.  External literature therefore makes the perturbation
biologically plausible, but it does not imply a large whole-gene mRNA response
after sparse partial CRISPR loss in already postmitotic neurons.

The most direct missingness is important: the training set did not contain
`Hmgb2` or `Hmgb3`, so the estimate cannot be transferred from a near paralog.
I therefore weighted the internal examples that ask a narrower question: when
this screen perturbs a broadly acting, abundant chromatin-associated component
in juvenile neurons, does the 3-4 week survivor-conditioned nuclear RNA profile
explode into many FDR-significant genes?  The closest visible answers were
mostly no.  `H3f3a`, `Set`, `H2ac8`, and `H4c11` were FDR-flat in the same cell
group.  The July corpus report for `H3f3a` also called this a broad negative
result across all measured neuronal classes, and the report noted no detectable
induction of `H3f3b`, `Hira`, `Daxx`, or `Atrx`, so the zero is not simply a
single low-powered focal observation.  `Baz1b` is an even more useful
calibration point because it showed a strong focal self-transcript decrease
without a broad downstream cascade; its same-experiment report interpreted the
response as an extremely sparse postnatal neuronal signature despite known
developmental chromatin biology.  `Setd2` similarly contributed only a
single-gene focal signature.

The broader chromatin positives argue against predicting an impossible zero for
every nuclear factor: `Chd2`, `Chd4`, `Chd8`, `Smarcc2`, `Setd1a`, and `Sin3a`
all produced real 151 TH responses.  I treated these as upper counterexamples,
not as the main transfer set.  Their causal perturbations remove ATP-dependent
remodeler subunits, histone methyltransferase machinery, BAF subunits, or an
HDAC-corepressor scaffold.  Those interventions are more likely than a partial
HMGB1 depletion to make coordinated Pol II, nucleosome-positioning, or
corepressor-state changes with FDR-level mRNA consequences.  The HMGB1
intervention is also plausibly buffered by other HMGB-family proteins and by
the fact that its best-known extracellular alarmin functions would require
injury, glial/immune partners, or secretion contexts that are outside a
NeuN-enriched recovered-neuron DE contrast.

The resulting causal chain for the requested experiment is:

`AAV CRISPR Hmgb1 loss of function -> partial depletion of nuclear HMGB1 in
postmitotic thalamic neurons -> altered local chromatin bending/DNA-repair or
transcription-factor facilitation, with potential HMGB-family buffering ->
survival and recovery 3-4 weeks later -> single-nucleus Wilcoxon DEGs`.

At the propagation stage, the evidence for a large same-direction transfer is
weak: broad complex losses such as `Sin3a` and `Smarcc2` are too different,
whereas low-burden architectural perturbations are closer.  At the sampling
stage, the endpoint is conditioned on recovered nuclei, so any cell-fitness
effect upstream of recovery would be incompletely observed.  I therefore
predict no gene crossing focal FDR 0.05 rather than a moderate chromatin-like
count.

Point prediction: `Hmgb1 = 0`.

# Limits

- No `Hmgb1` DEG count or signature was available in the declared inputs, and
  no `Hmgb2`/`Hmgb3`/`Hmgb4` perturbation was available for a paralog transfer.
- The histone-gene zeros are imperfect analogs because individual canonical
  histone genes are highly redundant in a way that `Hmgb1` may not be.
- The broad chromatin positives show that 151 TH neurons can detect loss of
  some chromatin regulators; the decision to keep `Hmgb1` at zero rests on
  mechanistic distance from those multi-subunit or enzymatic regulators.
- HMGB1's extracellular inflammatory and damage-associated roles are supported
  in the literature, but this neuronal nuclei dataset largely omits astrocytes,
  microglia, peripheral immune cells, and secreted protein measurements.
- The CRISPR perturbation is sparse and partial at the assayed RNA level, and
  the DEG count is a power-dependent FDR endpoint.  A predicted zero should be
  read as no measured focal transcript passing BH 0.05, not as no HMGB1 biology.
