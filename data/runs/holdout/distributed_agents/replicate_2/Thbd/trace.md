# DEG-count prediction for held-out Thbd

## Question and resolution of ambiguities

The requested held-out perturbation file, `237_Thbd.csv`, contains one target:
`Thbd`. I interpreted the task as predicting the integer number of measured
genes that would pass BH-adjusted Wilcoxon `pvals_adj < 0.05` in the focal
`151 TH Prkcd Grin2c Glut` neuronal group after sparse AAV-CRISPR loss of
function of `Thbd`. `151 TH Prkcd Grin2c Glut` was treated as the Allen-style
thalamic glutamatergic cell-group label described in the task; `TH` was not
interpreted as tyrosine hydroxylase.

The held-out `Thbd` expression signature and DEG count are absent from both
supplied inputs, so the prediction below transfers from training perturbations
that were mechanistically adjacent to thrombomodulin, endothelial receptor
signaling, thrombin/coagulation, or neuroimmune inflammation.

## Sources used

- Differential-expression parquet:
  `[local file: training_de_all_cell_groups.parquet]`.
  I used it for exact focal-cell `pvals_adj`, log fold changes, and matched
  nucleus counts for selected training analogs.
- Focal-cell training endpoint table:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
  I used this as the authoritative training `n_degs` table for non-held-out
  targets.
- Requested-target manifest:
  `[local file: 237_Thbd.csv]`.
- Same-experiment semantic corpus:
  Distributed Agents corpus release `perturbai-july-260713-sourceguard-1773-v1`. I used
  its curated findings for represented pathway relatives such as `F2`, `Kdr`,
  `Tek`, `Axl`, `Mertk`, and `Eng`.
- PubMed literature searches for the biology of thrombomodulin/THBD.
  Key papers were Conway 2011, DOI `10.1007/s00281-011-0282-8`, PMID
  `21805323`; Ito and Maruyama 2011, DOI `10.1111/j.1538-7836.2011.04319.x`,
  PMID `21781252`; Weiler 2004, DOI `10.1160/TH04-05-0307`, PMID `15351842`;
  Tran et al. 1996, DOI `10.1161/01.str.27.12.2304`, PMID `8969798`; Wang et
  al. 1998, DOI `10.1016/s0049-3848(98)00135-2`, PMID `9851812`; and Wenzel
  et al. 2020, DOI `10.1161/ATVBAHA.120.315061`, PMID `33028093`.

## Computational checks over the supplied data

I read the manifest and focal training-count CSV to confirm that there was
exactly one requested target, that it was not duplicated, and that it was not
present in the training endpoint table. The training endpoint table contained
1,674 perturbations; 1,205 of them, 71.98 percent, had zero DEGs in
`151 TH Prkcd Grin2c Glut`, with a median of 0, 75th percentile of 1, 90th
percentile of 2, and 95th percentile of 18. Thus a silent prediction is common
but not automatic; a target needed a mechanistic reason to be compared with the
silent class.

For mechanistic neighbors of `Thbd`, I filtered the parquet to
`group_name == "151 TH Prkcd Grin2c Glut"` and to exact `gene_target` values
that represent thrombin/coagulation, endothelial receptor signaling,
TGF-beta/BMP vascular signaling, or adjacent neuroimmune biology. Each selected
perturbation had 17,259 measured-gene rows in this focal cell group, so the
counts below are direct `sum(pvals_adj < 0.05)` values from the same focal
contrast.

| training perturbation | focal `n_degs` | expression-pattern evidence and relevance to `Thbd` |
| --- | ---: | --- |
| `F2` | 0 | Direct thrombin-pathway ligand of thrombomodulin biology. In the focal parquet it had no significant genes and a minimum adjusted p value of 0.698. The Distributed Agents corpus reports that `F2` loss produced a pan-neuronal transcriptional null rather than a coagulation, PAR, stress, or synaptic program, and had no meaningful positive or negative transcriptomic neighbor. |
| `Kdr` | 0 | Endothelial VEGF receptor comparator. In the focal parquet every BH-adjusted p value was 1.0. The corpus reports an almost completely flat postnatal neuronal DE surface and no canonical VEGF/endothelial program. |
| `Tek` | 0 | Endothelial TIE2 receptor comparator. It had zero focal DEGs with every adjusted p value equal to 1.0. The corpus reports that `Tek` was transcriptomically silent across all 23 assayed NeuN-enriched neuronal groups, and represented endothelial and PI3K/Notch relatives failed to phenocopy it in neurons. |
| `Eng`, `Acvrl1`, `Bmpr2`, `Smad9`, `Atp13a3`, `Eif2ak4` | 0 each | These are vascular PAH/PVOD or TGF-beta/BMP/endothelial-adjacent comparators. All had zero focal DEGs. The corpus reports a pan-null `Eng` result and a broader absence of a coherent neuronal module for represented PAH/PVOD/BMP-SMAD/TGF-beta-superfamily genes. |
| `Axl`, `Mertk`, `C3` | 0 each | `Thbd` has anti-inflammatory, complement, HMGB1, and vascular-barrier links, so I checked neuroimmune/phagocytic/complement comparators rather than only coagulation genes. `Axl`, `Mertk`, and `C3` all had zero focal DEGs; in the corpus, `Axl` and `Mertk` were flat or noise-scale across NeuN-positive neuronal groups rather than forming a TAM/efferocytosis module. |
| `Serpine2` | 2 | A partial counterexample: this serine-protease inhibitor perturbation did have a tiny focal signature, but the two passing genes were `Serpine2` itself and `Clip2`. This suggests the assay could detect a protease-inhibitor perturbation when the target was read out, but it does not make a thrombomodulin-like endothelial program likely. |
| `Serpini1`, `Serpinb6a`, `Flt4`, `Notch1`, `Notch2`, `Pik3r1` | 0 each | Additional protease-inhibitor, vascular, Notch, and PI3K comparators that bound the pathway search. None produced focal DEGs. |

As a low-expression sanity check rather than an editing-efficiency filter, I
also extracted rows where the measured gene was `Thbd` across all 1,674
non-held-out perturbations in the focal cell group. The `Thbd` measured
transcript had `pvals_adj == 1.0` in all 1,674 contrasts, consistent with no
detectable `Thbd` RNA variation in these recovered thalamic glutamatergic
nuclei. I did not use the unobserved self-knockdown of held-out `Thbd` as an
editing metric.

## Target-specific reasoning

### Thbd

Thrombomodulin is a transmembrane endothelial cofactor that binds thrombin and
promotes activation of the protein C anticoagulant pathway, while its
extracellular domains also connect to anti-inflammatory, anti-fibrinolytic,
HMGB1, and complement-related functions. This biology is reviewed by Conway
2011, Ito and Maruyama 2011, and Weiler 2004. In the brain, the evidence I
found was also vascular: brain capillary endothelial cells express
thrombomodulin mRNA and activate protein C in vitro or ex vivo in the
Tran et al. 1996 and Wang et al. 1998 studies, and Wenzel et al. 2020 deleted
`Thbd` specifically in brain endothelial cells to show an endothelial
angiogenesis/vessel-diameter role after ischemic stroke.

The focal assay is the wrong compartment for those mechanisms. It perturbed
postnatal cells sparsely, recovered NeuN-positive neuronal nuclei, and scored a
basal thalamic glutamatergic RNA phenotype rather than endothelial surface
coagulation, vascular permeability, platelet/thrombin signaling, microglial
efferocytosis, or injury-induced angiogenesis. The direct within-dataset
comparators fit that compartment mismatch: `F2`, the closest represented
thrombin-pathway perturbation, had zero focal DEGs and the curated corpus found
no PAR/AP-1/NF-kappaB injury program after `F2` loss. Endothelial receptor
comparators were similarly silent: `Kdr`, `Tek`, `Eng`, `Acvrl1`, `Bmpr2`, and
`Smad9` all had zero focal DEGs. The complement/TAM/neuroimmune side also did
not provide an active analog because `C3`, `Axl`, and `Mertk` were all zero in
the focal endpoint.

`Serpine2` was the main nonzero counterexample among protease-pathway genes,
with two focal DEGs, but that small signature was anchored by the target's own
RNA and one additional transcript. I treated it as evidence that serpin-like
labels should not be force-set to zero by name alone, but not as a strong analog
for an endothelial cell-surface thrombin cofactor. Overall, the training
signatures and the external biology both supported no FDR-significant
cell-autonomous response in `151 TH Prkcd Grin2c Glut`.

Predicted `Thbd` count: 0 DEGs.

## Limits and extrapolation

- There was no target-specific Distributed Agents corpus entry for held-out `Thbd`, and
  no `Thbd` perturbation signature was available in the supplied training
  parquet, so the prediction is an extrapolation from pathway relatives.
- The best biochemical partners of THBD, such as endothelial protein C receptor,
  protein C, protein S, and PAR-family thrombin receptors, were not all present
  as focal training perturbations. `F2` is a close thrombin-side comparator, but
  loss of thrombin itself is not identical to loss of endothelial
  thrombomodulin.
- A zero neuronal DEG prediction does not imply that `Thbd` is biologically
  unimportant. The literature-supported THBD phenotypes are vascular,
  coagulation, BBB, and injury-context phenotypes that this NeuN-enriched
  snRNA-seq endpoint is largely unable to observe.
- The focal group had hundreds, not thousands, of matched perturbed nuclei for
  the relevant analogs. Very small transcriptional changes or rare
  non-cell-autonomous effects could fall below the Wilcoxon/BH threshold.
