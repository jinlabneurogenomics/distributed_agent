# Trace

## Question and endpoint

I interpreted the requested prediction as a count prediction for one held-out
perturbation, `Tubb3`, in `151 TH Prkcd Grin2c Glut` thalamic glutamatergic
neurons. The endpoint is the exact `n_degs` used in the supplied training CSV:
the number of measured genes in the focal cell group with Benjamini-Hochberg
adjusted Wilcoxon `pvals_adj < 0.05` after CRISPR loss of the target gene.
Self-target rows count if they pass this FDR threshold. `Tubb3` was held out
from both the per-gene differential-expression parquet and the focal training
count table, so its requested count is absent from the declared inputs and must
be inferred from non-held-out perturbations.

## Sources used

- Declared differential-expression parquet
  `training_de_all_cell_groups.parquet`: direct per-gene perturbation signatures
  for non-held-out genes.
- Declared focal training counts
  `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`: direct observed `n_degs`
  for 1,674 non-held-out perturbations in `151 TH Prkcd Grin2c Glut`.
- Declared requested-target manifest `b0217.csv`: the single held-out target,
  `Tubb3`.
- Run-local dataset portrait, task bindings, compact source coverage, and
  capability manifest.
- Internal same-experiment corpus:
  `perturbai-july-260713-sourceguard-1773-v1`, queried for the curated `Tuba1a`,
  `Tubb4b`, and `Tubb5` Findings and for resolved `Tuba1a` evidence.
- External literature:
  - Tischfield et al. 2010, DOI `10.1016/j.cell.2009.12.011`, PMID `20074521`.
    This paper established that human TUBB3 missense alleles alter microtubule
    dynamics, kinesin interactions, and axon guidance.
  - Puri, Barry, and Engle 2023, DOI `10.3389/fnins.2023.1226181`, PMID
    `37600020`. This review summarizes TUBB3 as neuron-enriched beta-tubulin
    III and places pathogenic TUBB3 and KIF21A alleles in microtubule-dependent
    axon growth and guidance.
  - Hausrat et al. 2020, DOI `10.1002/dneu.22745`, PMID `32293117`. This work
    measured alpha- and beta-tubulin isotype expression during mouse brain
    development.
  - Lin et al. 2020, DOI `10.1126/science.aaz4352`, PMID `31727855`; and
    Hopfler et al. 2023, DOI `10.1016/j.molcel.2023.05.020`, PMID `37295431`.
    These papers describe tubulin autoregulation through nascent-tubulin
    recognition by TTC5 and recruitment of mRNA decay machinery.

The parquet and the internal corpus are different representations of the same
Perturb-seq experiment, not independent replications.

## Dataset calculations

I first summarized the focal training counts. The focal endpoint is highly
zero-inflated: among 1,674 training perturbations, 1,205 had `n_degs = 0`,
469 had a positive count, the median was 0, the 75th percentile was 1, and only
the top 5% exceeded 18 DEGs. That distribution set a strong prior against
predicting a large count for a structural microtubule gene unless a close
training analog had a broad focal response.

I then filtered the focal parquet rows to tubulin and microtubule-related
training perturbations and counted rows with `pvals_adj < 0.05`. The main
focal-cell analogs were:

| training perturbation | focal `n_degs` | focal expression-pattern evidence |
| --- | ---: | --- |
| `Tuba1a` | 7 | Seven FDR<0.05 genes: the depleted `Tuba1a` self transcript and induction of `Tubb3`, `Tubb2a`, `Tuba4a`, `Tubb4a`, `Tubb4b`, and `Tubb5`. This is a narrow tubulin-isotype compensation module, not a broad stress or synaptic-collapse program. |
| `Tuba4a` | 2 | `Tuba4a` itself passed FDR and `Mast1` was a single additional call. Other tubulin isotypes, including `Tubb3`, were far from FDR<0.05. |
| `Tubb4b` | 1 | Only the `Tubb4b` self transcript passed FDR<0.05. `Tubb5`, `Tubb3`, `Tubb4a`, and other tubulin genes were directionally small and nonsignificant. |
| `Tubb5` | 1 | Only the `Tubb5` self transcript passed FDR<0.05 in the focal group despite a strong self row. No beta/alpha-tubulin replacement module appeared. |
| `Kif1a`, `Kif5a`, `Mapt`, `Map1b`, `Stmn2` | 1 each | These microtubule motor, MAP, or tubulin-dynamics perturbations were self-row or near-self-row only in the focal group and did not produce a Tuba1a-like beta/alpha-tubulin module. |
| `Spast`, `Dync2h1`, `Dync2i1` | 0 | Additional cytoskeletal comparators that were flat in the focal endpoint. |

The internal corpus supplied the same contrast at report level. The `Tuba1a`
report describes a real, selective alpha/beta-tubulin mRNA response in `151 TH
Prkcd Grin2c Glut` and `052 Pvalb Gaba`, and its `E002` evidence gives the
focal statistics: 121 perturbed cells versus 23,679 controls; `Tubb3` logFC
`0.576`, FDR `6.37e-9`; `Tubb2a` logFC `0.523`, FDR `2.68e-7`; `Tuba4a` logFC
`0.696`, FDR `1.14e-5`; `Tubb4a` logFC `0.506`, FDR `2.85e-5`; `Tubb4b` logFC
`0.513`, FDR `2.66e-4`; and `Tubb5` logFC `0.620`, FDR `2.86e-4`.

The direct beta-tubulin reports were the key counterexamples. `Tubb4b:F001`
summarizes zero non-self genes at FDR<0.10 in all 22 recovered neuronal cell
groups after `Tubb4b` loss, and `Tubb4b:F002` notes that `Tubb4b` did not induce
the alpha/beta tubulin replacement program that was visible after `Tuba1a`
loss. `Tubb5:F002` likewise reports a measured `Tubb5` mRNA decrease often
uncoupled from any stable nuclear RNA program, and `Tubb5:F003` records that
`Tuba1a`, but not `Tubb5` or `Tubb4b`, elicited the tubulin-paralog feedback
signature.

## Target-specific reasoning

### `Tubb3`

`Tubb3` encodes neuron-enriched beta-III tubulin, a bona fide neuronal
microtubule subunit. TUBB3 missense alleles can disrupt microtubule dynamics,
kinesin interactions, and axon guidance, and human TUBB3/KIF21A syndromes show
that this biology is not interchangeable with every other cytoskeletal gene
(Tischfield et al. 2010; Puri et al. 2023). However, those disease alleles are
mostly dominant missense variants that can poison the microtubule lattice. The
assay here is a sparse, postnatal, acute loss-of-function perturbation in
surviving NeuN-positive nuclei. That causal chain is therefore:

`Tubb3` CRISPR loss -> reduced or mutated beta-III-tubulin pool -> possible
local changes in microtubule composition, dynamics, or motor interactions ->
compensation by other alpha/beta isotypes if the beta-III pool is limiting in
these thalamic neurons -> only effects present in recovered nuclei after 3-4
weeks can become FDR-significant nuclear RNA changes.

The strongest positive analog is `Tuba1a`, because TUBA1A and TUBB3 are
partner alpha/beta tubulin building blocks and `Tuba1a` loss directly drove
`Tubb3` upward in the same focal cells. That shows that the focal cells can
activate and statistically resolve tubulin-isotype feedback. It does not,
however, imply that `Tubb3` loss should give seven DEGs: `Tuba1a` is a major
neuronal alpha-tubulin and was the exceptional structural tubulin perturbation
in the training data.

The closest same-class counterexamples are more informative for the expected
count. Loss of the two visible beta-tubulin paralogs, `Tubb4b` and `Tubb5`,
caused only one focal DEG apiece, their own target transcript, even with clear
self-row depletion and even though the Tuba1a signature included up-regulation
of both genes. `Tuba4a` was also very small at two DEGs. Other microtubule
motors or MAPs did not reveal a generic microtubule-failure transcriptional
state. Together, these observations argue that loss of an individual
beta-tubulin in recovered postnatal thalamic neurons is usually buffered at the
snRNA-seq DEG-count endpoint, while the on-target tubulin transcript itself can
still cross FDR.

My zero/nonzero call for `Tubb3` is therefore nonzero, driven mainly by
within-dataset beta-tubulin self-row behavior plus the high expression and
neuronal identity of TUBB3. I did not extrapolate the full `Tuba1a`
compensation module to `Tubb3`, because the causal transfer fails at the
isotype-specific feedback step: direct beta-tubulin perturbations in the same
experiment did not trigger multi-isotype compensation. I predicted one DEG,
corresponding to a self-transcript-only or nearly self-only response.

## Limits

The prediction is an extrapolation because no `Tubb3` perturbation rows are in
the supplied parquet. The closest beta-tubulin training genes are `Tubb4b` and
`Tubb5`, but beta-tubulin isotypes differ by cell type, developmental timing,
and polymer specialization, so `Tubb3` could be more responsive than either
one. Conversely, a functional CRISPR allele need not reduce the nuclear
`Tubb3` transcript; if nonsense-mediated decay is weak, even the self row could
miss FDR and the true endpoint could be zero. The external TUBB3 disease
literature establishes microtubule and axon-guidance function, but most of it
does not measure sparse juvenile loss-of-function in postmitotic thalamic
neurons and should not be read as evidence for a large 3-4 week nuclear RNA
signature.
