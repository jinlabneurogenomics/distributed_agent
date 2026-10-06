# Scn9a DEG-count prediction

## Question and endpoint

The task asks for one held-out perturbation, `Scn9a`, to be assigned an integer
prediction for `n_degs` in `151 TH Prkcd Grin2c Glut` cells. I interpreted
`n_degs` exactly as the focal training CSV defines it: the number of measured
genes with Wilcoxon Benjamini-Hochberg adjusted `pvals_adj < 0.05` in the
perturbed nuclei versus matched non-targeting controls. The requested
perturbation itself was withheld from both the focal count table and the full DE
parquet, so its count is absent and must be inferred.

I treated the input training count CSV as the direct endpoint for visible
perturbations and the all-cell DE parquet as the source for exact focal-cell
signatures of mechanistic analogs. The same-experiment semantic corpus
`perturbai-july-260713-sourceguard-1773-v1` was used only to interpret bounded
visible comparisons among sodium-channel, FHF, ankyrin, and KCNQ perturbations;
it is a report layer over the same experiment, not independent replication. For
external biology I used NCBI PubMed literature searches focused on SCN9A/Nav1.7
localization and voltage-gated sodium-channel biology.

## Training-data calibration

The focal-cell training CSV contains 1,674 unique visible perturbations. The
endpoint is heavily concentrated near zero: 1,205 of 1,674 targets had 0 DEGs,
276 had 1 DEG, 31 had 2 DEGs, the median was 0, and the mean was 14.1 because a
small tail of RNA-processing, ubiquitin, proteasome, or chromatin perturbations
had hundreds to thousands of DEGs.

I then restricted the declared parquet to `group_name == "151 TH Prkcd Grin2c
Glut"` and to voltage-gated sodium-channel analogs and nearby channel
localization or excitability genes. Each queried perturbation had 17,259
measured-gene rows in the focal cell group. The closest available sodium-channel
targets were all at the noise floor:

| visible perturbation | focal `n_degs` | focal signature details |
|---|---:|---|
| `Scn1a` | 1 | only `Scn1a` itself passed FDR 0.05, `p_adj = 5.87e-38`, log2FC -1.075 |
| `Scn2a` | 1 | only `Scn2a` itself passed, `p_adj = 6.46e-06`, log2FC -0.401 |
| `Scn3a` | 0 | no gene passed; minimum adjusted p-value was 1.0 in this focal class |
| `Scn8a` | 1 | only `Scn8a` itself passed, `p_adj = 1.34e-05`, log2FC -0.458 |
| `Scn1b` | 2 | `Scn1b` itself and `Jun` passed; `Jun` was a singleton downstream hit |
| `Fgf12` | 0 | intracellular Nav-channel modulator; no focal DEG |
| `Fgf13` | 2 | FHF/Nav modulator; `Fgf13` plus singleton `Rell2` |
| `Ank2` | 0 | ankyrin channel/cytoskeleton scaffold; no focal DEG |
| `Kcnq2` | 1 | other axonal excitability channel; only self transcript |
| `Kcnq3` | 1 | other axonal excitability channel; only self transcript |
| `Cacna1g` | 12 | thalamic T-type calcium-channel outlier among queried ion channels |

This comparison matters in two ways. First, the pore-forming Nav alpha genes
that are actually used throughout central neurons, `Scn1a`, `Scn2a`, and
`Scn8a`, did not produce broad nuclear RNA programs in the focal thalamic
glutamatergic class after the same P16 mosaic CRISPR loss-of-function
perturbation. Their counts would have been zero if self transcript were
excluded. Second, accessory or localization proteins that could have revealed a
generic sodium-channel homeostatic response, including `Scn1b`, `Fgf12`,
`Fgf13`, and `Ank2`, also stayed at 0-2 DEGs. The declared corpus summarized the
same observation in its `Ank2` pathway-uncoupling finding: visible `Scn1b`,
`Scn1a`, and `Kcnq2` perturbations had strong target-transcript effects but
little downstream RNA output, so Ank2-linked excitability and axon-initial-
segment biology did not emerge as broad `Scn` or `Kcnq` mRNA changes in sparse
postmitotic snRNA-seq (`Ank2:F004`). Its `Scn1a` report likewise concluded that
postnatal mosaic `Scn1a` loss was transcriptomically buffered across the atlas,
with the main expected phenotype being electrical rather than a
transcription-factor-like RNA program (`Scn1a:F001`, `Scn1a:F005`).

I also queried the row where each sodium-channel gene was the measured
transcript across all 1,674 visible focal-cell perturbations. `Scn9a` was never
significant; its minimum adjusted p-value across these visible perturbations
was 0.395. By contrast the endogenous central-channel transcripts were readily
detectable as self hits when their own loci were perturbed: `Scn1a`,
`Scn1b`, `Scn2a`, and `Scn8a` each had an adjusted self-transcript p-value from
`5.87e-38` to `1.34e-05`. This is not a direct baseline-expression assay, but it
is consistent with the thalamic glutamatergic nuclei carrying little or no
detectable `Scn9a` signal while expressing several other Nav components.

## External biological prior

`Scn9a` encodes the Nav1.7 voltage-gated sodium-channel alpha subunit. Nav1.7 is
best established as a threshold channel for primary somatic and visceral
sensory neurons, olfactory sensory neurons, and sympathetic ganglion neurons,
where it accumulates in peripheral nerve endings and amplifies small
depolarizations (Dib-Hajj et al. 2012, Nat Rev Neurosci,
doi:10.1038/nrn3404, PMID:23232607). Human loss-of-function mutations in
`SCN9A` cause congenital insensitivity to pain, while gain-of-function alleles
cause inherited erythromelalgia, paroxysmal extreme pain disorder, and small
fiber neuropathy (Lampert et al. 2010, Pflugers Arch,
doi:10.1007/s00424-009-0779-3, PMID:20101409; Bennett and Woods 2014, Lancet
Neurol, doi:10.1016/S1474-4422(14)70024-9, PMID:24813307). A mouse/human study
showed that Nav1.7 is also required for olfaction by olfactory sensory neurons
(Weiss et al. 2011, Nature, doi:10.1038/nature09975, PMID:21441906).

Those tissues are a poor match to this Perturb-seq sample. The input nuclei are
NeuN-positive brain neurons from whole brain excluding olfactory bulb and
hindbrain, and the focal class is thalamic glutamatergic, not dorsal-root,
visceral, sympathetic, or olfactory sensory neurons. The causal transfer chain
therefore breaks at exposure/context: loss of `Scn9a` should impair a
Nav1.7-dependent excitability threshold where Nav1.7 is present, but the
limiting molecular function is not expected to be active in the recovered
`151 TH Prkcd Grin2c Glut` nuclei. This makes `Scn9a` weaker than the visible
central Nav analogs, not stronger.

## Target-specific prediction

### `Scn9a`

Relevant within-dataset analogs were the visible Nav alpha-subunit knockouts
`Scn1a`, `Scn2a`, `Scn3a`, and `Scn8a`; the beta subunit `Scn1b`; the FHF
intracellular Nav regulators `Fgf12` and `Fgf13`; and the ankyrin scaffold
`Ank2`. All were flat or almost flat in `151 TH Prkcd Grin2c Glut`. The nearest
alpha-channel analogs had 0-1 DEGs and did not trigger a shared immediate-early,
stress, or channel-compensation program. `Fgf13` and `Scn1b` each had one
non-self singleton in this class, but the same-experiment reports showed that
FHF/Nav perturbations did not phenocopy each other (`Fgf12:F004`,
`Fgf13:F004`, `Scn1a:F003`), so those singleton markers are counterexamples to
a generic sodium-channel DEG module rather than a reason to lift `Scn9a`.

Externally, Nav1.7 biology points away from the assayed thalamic glutamatergic
neurons and toward peripheral nociceptors, sympathetic neurons, and olfactory
sensory neurons. Because the visible central Nav channels were already
transcriptionally buffered in this assay, a peripheral-skewed Nav channel is
unlikely to exceed the FDR 0.05 threshold in the focal class. I therefore
predict no measured genes passing FDR 0.05:

`Scn9a -> 0` DEGs.

## Limits and uncertainty

The requested endpoint itself is absent by construction, and the parquet does
not contain raw per-nucleus expression that would let me directly quantify
baseline `Scn9a` expression in `151 TH Prkcd Grin2c Glut`. The `Scn9a`
measured-gene rows under other perturbations only indirectly support low focal
expression. The visible sodium-channel analogs are imperfect because Nav1.1,
Nav1.2, Nav1.6, beta1, FHFs, and ankyrins are central-neuron channels or
scaffolds whereas Nav1.7 is peripheral and olfactory-skewed. However, that
difference lowers the expected focal DEG count: even better-expressed central
Nav perturbations did not produce broad DEG responses after sparse postnatal
CRISPR loss. The single nonzero alternative I considered was a one-DEG
self-transcript-only prediction, but the available focal data give no sign that
`Scn9a` is as detectably expressed in this thalamic class as `Scn1a`, `Scn2a`,
or `Scn8a`.
