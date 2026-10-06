# Crebrf DEG-count forecast

## Target and endpoint

- Holdout manifest target: `Crebrf`.
- Focal population: `151 TH Prkcd Grin2c Glut`.
- Predicted endpoint: `n_degs`, the number of measured genes with Wilcoxon `pvals_adj < 0.05`.
- The held-out `Crebrf` signature and held-out `Crebrf` count were not used.

## Biology that sets the direction

The supplied Crebrf biology bundle makes a successful acute loss plausible in this
cell class: in the exact 151 non-target population, Crebrf was detected in
16,464 of 23,679 nuclei, with 69.53% of nuclei expressing the feature,
mean raw UMI 1.351, mean log1p CP10k 0.530, and pseudobulk CPM 84.67. Thus I
did not treat the perturbation as unreachable for lack of baseline expression.

The functional-stock card also argues that a P16 edit should substantially
deplete operative CREBRF by the P37-P44 harvest. CREBRF is represented as a
soluble nuclear CREB3-family/glucocorticoid-response coregulator rather than a
stable installed cellular structure, and the matched evidence says ectopic
mouse CREBRF is proteasome-sensitive. That supports 21-28 day realization, but
only with partial evidence because the kinetic observation was in Neuro2a
overexpression rather than endogenous juvenile thalamic neurons.

The same bundle keeps the assay-specific effect uncertain. Adult constitutive
Crebrf-null mice had behavior and glucocorticoid phenotypes, but those are
systemic/global and developmental-context observations, not an acute thalamic
neuronal transcriptional response. The bundle found no close mouse paralog, but
network-level buffering remained unresolved.

## Matched training measurements

The declared 151 count table is heavily zero-inflated even in this high-yield
class: 1,205 of 1,674 training perturbations had `n_degs = 0`, 469 were nonzero,
106 reached at least 10 DEGs, and 43 reached at least 100 DEGs. A reachable
target therefore still needs endpoint-specific evidence before expecting a
large count.

I used the Crebrf operation and source facts to choose measured transcriptional,
ER-stress, and glucocorticoid comparators rather than broad high-count
housekeeping perturbations. In the declared count table their exact
FDR<0.05 counts were:

| training target | `n_degs` |
| --- | ---: |
| Atf6 | 0 |
| Nfe2l1 | 0 |
| Nfe2l2 | 0 |
| Eif2ak4 | 0 |
| Nr3c1 | 0 |
| Nr3c2 | 0 |
| Jund | 0 |
| Fosl2 | 0 |
| Hsp90ab1 | 1 |
| Hspa5 | 5 |
| Crebbp | 8 |
| Hspa8 | 9 |
| Creb1 | 10 |

The raw 151 Parquet rows confirmed the same pattern for an expanded
14-comparator cohort: 9 of 14 had no significant measured gene, 4 had only
1-9, and only Creb1 reached 10. The significant genes that did appear were
small, target-specific tails: Hspa5 up-regulated ER quality-control genes such
as Hsp90b1, Nfe2l1, Pdia4, and Derl3; Hspa8 induced chaperone-linked genes; and
Creb1/Crebbp produced small thalamic regulatory responses rather than a shared
CREB3 or immediate-early program. The profile comparison over the same 14 nodes
showed no recurrent significant positive or negative program across this
cohort.

The corpus summaries for the same experiment sharpened the ER-stress boundary:
basal Atf6 loss was a corrected-transcriptome null; Hspa5, not Atf6, exposed a
detectable 151 ER quality-control module; and Atf6, Edem3, Hspa8, Nfe2l1,
Nfe2l2, Sil1, and Vcp did not recapitulate the Hspa5 signature. Direct ER
homeostasis lesions in the table can be large in 151, for example Gfpt1 = 311,
Atp2a2 = 187, and Dhdds = 116, but Crebrf is a CREB3-family transcriptional
coregulator rather than an ER folding, calcium, or glycosylation component.

## Forecast

Crebrf is expressed and the target stock should be perturbed, so I did not force
a technical zero. The closest measured biology nevertheless placed basal
stress-response transcription factors and glucocorticoid receptors at zero,
placed chaperone/coregulator relatives in only the 1-10 DEG range, and reserved
large 151 signatures for more proximal ER or housekeeping lesions. With Creb3
itself absent from the training table and no measured analogue supporting a
broad survivor-state response, the biology-conditioned mode is a null or
near-null result. I therefore used the null as the integer point forecast:
`predicted_n_degs = 0`.
