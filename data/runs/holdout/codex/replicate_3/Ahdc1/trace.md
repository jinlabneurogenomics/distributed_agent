# Ahdc1 151 TH Prkcd Grin2c Glut n_degs forecast

## Target biology used

The held-out manifest target is `Ahdc1`. I used only the declared biology-only bundle for the target, not an Ahdc1 same-experiment expression signature or Ahdc1 DEG count.

Key bundle facts:

- In the focal non-target 151 TH Prkcd Grin2c Glut nuclei, `Ahdc1` is present but not saturating: 15,863 / 23,679 nuclei expressed it, or 66.99%, with mean raw UMI 1.273 and mean log1p CP10k 0.499.
- AHDC1/Gibbin is a chromatin-associated enhancer/promoter regulator that maintains selected local regulatory contacts.
- The strongest loss-of-function evidence is developmental or systemic: human germline neurodevelopmental genetics, severe chimeric mouse developmental patterning defects, and post-weaning systemic phenotypes in surviving heterozygous mice. The bundle had no matched acute postnatal thalamic-neuron Ahdc1 loss phenotype.
- The functional-stock card called the P16-to-P37/P44 lesion `partially_depleted_or_leading_edge`: new AHDC1 synthesis should stop, but pre-existing chromatin-bound protein and downstream chromatin configurations may persist through part of the 21-28 day window.

## Training measurements used

The declared 151-class training count table has 1,674 measured training perturbations and is heavily zero-inflated for this endpoint:

- 1,205 / 1,674 targets have `n_degs = 0`.
- median = 0, 75th percentile = 1, 90th percentile = 2, 95th percentile = 18.

The chromatin/NDD regulator counts in the focal class split into a large quiet group, a sparse active group, and a separate broad-footprint group:

| Training target | n_degs in 151 |
| --- | ---: |
| Chd7 | 0 |
| Kat6a | 0 |
| Kat6b | 0 |
| Ep300 | 0 |
| Tcf4 | 0 |
| Mbd5 | 0 |
| Foxp2 | 0 |
| Arid1b | 1 |
| Mef2c | 1 |
| Ash1l | 1 |
| Smarca2 | 1 |
| Brd1 | 4 |
| Ehmt1 | 4 |
| Crebbp | 8 |
| Setd5 | 9 |
| Kdm5c | 18 |
| Ankrd11 | 20 |
| Kmt2a | 24 |
| Adnp | 25 |
| Chd2 | 34 |
| Chd8 | 61 |

Broader global transcriptional or chromatin-maintenance perturbations were not used as direct scale anchors for Ahdc1 because they had much larger footprints in the same table: `Cic = 576`, `Yy1 = 720`, `Sin3a = 1433`, `Wac = 384`, `Brd4 = 311`, and `Setd1a = 368`.

## Profile and corpus checks

I compared the selected chromatin/NDD training perturbations directly in `training_de_all_cell_groups.parquet`, filtered to `group_name = "151 TH Prkcd Grin2c Glut"`, using `logfoldchanges` as the signed profile value and `pvals_adj < 0.05` as the significance call.

The profile comparison recovered exactly the expected low-to-high split among the 29 checked chromatin/transcriptional nodes: 12 had no significant feature, 8 had 1-9, 4 had 10-49, and 5 had at least 50. Within the focal sparse-to-moderate anchors, the task-matched p < 0.05 counts were `Setd5 = 9`, `Kdm5c = 18`, `Kmt2a = 24`, `Chd2 = 34`, and `Chd8 = 61`. The selected zero responders such as `Chd7`, `Kat6a`, `Kat6b`, and `Ep300` had whole-profile correlations to those anchors but no FDR-level overlap, so family or pathway identity alone did not justify promoting Ahdc1 into a broad-response class.

The same-experiment corpus pointed the same way. Chd8 findings state that represented CHD paralogs, Wnt/beta-catenin targets, BAF components, and ASD chromatin genes did not phenocopy Chd8 in the P16 neuronal assay. Setd5 findings state that its P16 postmitotic output was a localized thalamic module, not a broad chromatin-fidelity collapse, and that SET-family, MLL/COMPASS, CBP/p300, and chromatin-NDD comparators failed to phenocopy the exact Setd5 FDR signature. Kdm5c and Crebbp were also narrow, target-specific 151 responses rather than interchangeable chromatin-regulator outputs.

## Forecast

Ahdc1 has enough 151-class expression reach and no close paralog signal to keep the forecast above the mode of zero, but its evidence is mostly developmental, the acute postnatal neuronal role is unresolved, and the bundle's functional-stock adjudication argues that the harvested nuclei may only see the leading edge of loss. I therefore placed Ahdc1 below the active Setd5/Crebbp/Kdm5c scale and above the fully buffered developmental-chromatin group.

Final point forecast: `5` significant measured genes at BH-adjusted Wilcoxon `p < 0.05`.
