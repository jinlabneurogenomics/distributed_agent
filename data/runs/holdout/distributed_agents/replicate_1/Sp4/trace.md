# Predicting held-out DEG count for `151 TH Prkcd Grin2c Glut`

## Question interpreted

The held-out endpoint is `n_degs`: the number of measured transcripts with Wilcoxon
Benjamini-Hochberg adjusted `pvals_adj < 0.05` after acute sparse AAV-PHP.eB
CRISPR loss of a target gene in postnatal `151 TH Prkcd Grin2c Glut` neurons.
The readout is a focal-cell, assay-powered breadth count, not a direct measure
of biological importance, edited-cell abundance, or target mRNA knockdown.

This run requested one held-out perturbation, `Sp4`, in
`single-target request for Sp4`.
The target was absent from both supplied training inputs.

## Sources used

- Supplied endpoint table:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Supplied differential-expression Parquet:
  `training differential-expression dataset`.
- Run-local metadata: `codex_runtime/pipeline/task_bindings.json`,
  `coverage.json`, and `capabilities.json`.
- Internal same-experiment corpus: PerturbAI July 260713 sourceguard v1
  Finding reports for `Sp7` and `Klf9`. These are curated summaries over the
  same experiment, not independent replication.
- External SP4 literature, used as functional priors:
  - Ramos et al. 2007, PNAS, DOI `10.1073/pnas.0701946104`, PMID `17535924`.
  - Ramos et al. 2009, Molecular and Cellular Neuroscience, DOI
    `10.1016/j.mcn.2009.06.008`, PMID `19555762`.
  - Johar et al. 2014, European Journal of Neuroscience, DOI
    `10.1111/ejn.12415`, PMID `24219545`.
  - Nair et al. 2016, Biochimica et Biophysica Acta, DOI
    `10.1016/j.bbamcr.2015.10.005`, PMID `26469128`.
  - Zhang et al. 2020, BBA Gene Regulatory Mechanisms, DOI
    `10.1016/j.bbagrm.2020.194597`, PMID `32603878`.

## Quantitative calibration

The 151-cell training count table had 1,674 visible biological perturbations.
It was strongly sparse:

| subset | count |
|---|---:|
| training targets with `n_degs = 0` | 1,205 |
| training targets with `n_degs > 0` | 469 |
| median `n_degs` | 0 |
| 75th percentile | 1 |
| 90th percentile | 2 |
| 95th percentile | 18 |
| maximum | 2,677 |

I treated this as a prior that ordinary single-gene perturbations have no or
very few FDR-significant genes in this focal class unless the within-dataset
analogs show a robust postnatal thalamic transcriptional footprint.

The closest exact Sp-family training perturbation was `Sp7`, with `n_degs = 0`
in `151 TH Prkcd Grin2c Glut`. The internal `Sp7` report recorded that `Sp7`
loss had only a two-gene response at FDR 0.10 in `308 CB GABA` and was null or
weak in the other 21 measured neuronal groups, including the focal thalamic
class. It also noted that the canonical osteoblast ECM/mineralization program
and an oligodendrocyte ECM/node-of-Ranvier program were absent from the
NeuN-enriched neuronal surface. That makes `Sp7` an exact-family assay
calibrator for a lineage-gated Sp transcription factor, although it is not a
direct SP4 neuronal analog.

I next checked represented Kruppel/C2H2 transcription factors in the focal
training counts:

| target | `n_degs` in 151 |
|---|---:|
| `Klf9` | 19 |
| `Klf7` | 1 |
| `Klf11` | 0 |
| `Klf12` | 0 |
| `Klf13` | 0 |
| `Sp7` | 0 |

The `Klf9` internal report described a genuine but restricted response:
19 mostly upregulated genes in `151 TH Prkcd Grin2c Glut` and one `L1cam`
hit in `005 L4-5 IT CTX Glut`. The same report emphasized that `Klf13`,
`Klf7`, `Klf11`, and `Klf12` did not phenocopy `Klf9` in the focal class even
where KLF9/KLF13 have published overlap in other contexts. I therefore used
`Klf9` as the high side of the expected range for a related neuronal zinc-finger
factor, not as a one-to-one proxy.

I also checked obvious SP7 osteogenic-pathway comparators represented in the
training table. `Runx2`, `Dlx3`, `Dlx6`, `Bmpr1a`, `Bmpr1b`, `Smad1`, `Smad4`,
`Lrp5`, `Msx2`, and `Sox9` were all zero in the focal class; `Lrp6` had only
4 DEGs. These were counterexamples against predicting a large shared Sp-family
or osteogenic-program response in this thalamic glutamatergic class.

Finally, broad transcriptional regulators demonstrate the scale that I did
*not* transfer to `Sp4`: `Zbtb7a` had 841 focal DEGs at FDR 0.05 and `Rora` had
278, but their internal evidence and biology point to different regulatory
programs. They show that the focal class can support large TF-driven signatures
when an acute perturbation lands on a limiting function; they do not make every
C2H2 factor a broad responder.

## Target-specific prediction

### `Sp4`

**Within-dataset analogs and counterexamples.** The exact Sp-family analog in
training, `Sp7`, was 0 in the focal class despite 233 matched perturbed nuclei
and 23,679 matched controls. Its lowest focal adjusted p-values were all 1.0,
with only nominal positive shifts such as `Tspyl2`, `Bhlhe40`, and `Fads1`;
no downstream gene approached the requested FDR 0.05 threshold. The represented
osteogenic SP7-axis perturbations were likewise focal-null except `Lrp6`
with 4 DEGs, so there is no evidence that a generic SP/KLF zinc-finger or
BMP/Wnt/Runx2/Sp7 regulatory axis produces a large focal thalamic footprint.

The closest useful neuronal Kruppel-like comparator was `Klf9`, which produced
19 focal DEGs. That was a real small module headed by `Wsb1`, `Rasgrp2`, `Pld3`,
`Dzip1`, `Maged2`, `Mest`, `Cep70`, and `Hcn3`, but the KLF9 report explicitly
found that related `Klf13`, `Klf7`, `Klf11`, and `Klf12` were flat or distinct.
I therefore treated a count around the KLF9 value as an upper bound for SP4,
and the `Sp7`/KLF-paralog nulls as the stronger local evidence.

**External biology.** SP4 is more plausibly neuronal than SP7: Ramos et al.
showed that SP4 controls cerebellar dendritic patterning during maturation, and
then identified SP4-dependent repression of `Ntf3` as one mechanism limiting
dendritic branching. Other neuron-culture studies reported SP4 regulation of
Na/K ATPase, inhibitory GABA receptor, and serine racemase transcription. These
data argue against assigning `Sp4` a hard biological null merely because the
closest exact family member `Sp7` is lineage-displaced in the atlas.

Those SP4 studies do not, however, directly measure the requested endpoint:
they are in cerebellar, cortical, or cultured neuronal systems; some are
developmental or activity-linked; and they do not establish that 3-4 weeks of
sparse postnatal SP4 loss should broadly remodel thalamic glutamatergic nuclear
RNA. The training data also show that close transcription-factor paralogy often
fails to transfer at FDR-level strength in this assay.

**Point estimate.** I predict a nonzero but tiny response, well below `Klf9`
and close to the empirical 75th-90th percentile of the focal training
distribution. The selected point estimate is **2 DEGs** for `Sp4`.

## Limits

This prediction extrapolates from analogs because `Sp4` was completely held out
from the Parquet and the count CSV. `Sp7` is an exact-family comparator but has
bone, oligodendrocyte, and olfactory-bulb biology that differs from SP4.
`Klf9` is a genuine focal neuronal zinc-finger response but is not an SP-family
factor and its own closest KLF paralogs were not interchangeable in the screen.
The external SP4 literature establishes neuronal transcriptional functions but
not their strength in the `151 TH Prkcd Grin2c Glut` state, not the sparse AAV
CRISPR modality, and not the FDR 0.05 DEG-count endpoint. The response-breadth
count is also power dependent, so two DEGs should be read as "near-null but
detectable" rather than as a precise biological magnitude.
