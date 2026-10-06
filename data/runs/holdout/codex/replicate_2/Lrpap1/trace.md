# Lrpap1 direct DEG-count forecast

## Endpoint

- Target: `Lrpap1`
- Cell class: `151 TH Prkcd Grin2c Glut`
- Quantity: number of measured genes with BH-adjusted Wilcoxon `p < 0.05`

## Evidence used

The canonical biology bundle supports reachable perturbation in the focal
population but not a large obligatory transcriptional footprint. `Lrpap1` is
detected in the matching non-target thalamic population in 17,528 of 23,679
nuclei, or 74.0%, with mean 1.00 CP10K. The bundle adjudicates functional
stock by harvest as likely substantially depleted: a disruptive edit should
stop new RAP/LRPAP1 chaperone supply, mature pre-edit receptor clients should
turn over during the 21-28 day edit-to-harvest window, and RAP-null neural
evidence establishes impaired LRP maturation/localization. The same card marks
the phenotypic bridge as incomplete because the direct mouse neural evidence is
germline/hippocampal and reported normal gross brain architecture and cultured
hippocampal-neuron survival rather than an induced postnatal thalamic
transcriptional phenotype.

The declared `151 TH Prkcd Grin2c Glut` training count table is extremely
sparse: among 1,674 training targets the median `n_degs` is 0, 1,205 targets
have 0 DEGs, the 75th percentile is 1 DEG, and the 90th percentile is 2 DEGs.
Thus even a biologically realized edit commonly has a zero or one-gene FDR
footprint in this endpoint.

The most operation-proximal measured comparators were LDL-receptor-family
targets and adjacent receptor-trafficking genes, not the high-burden chromatin,
spliceosome, or proteasome hits in the far tail. Their same-endpoint training
counts were:

| comparator | `n_degs` |
| --- | ---: |
| `Lrp1` | 0 |
| `Lrp2` | 0 |
| `Lrp4` | 0 |
| `Lrp5` | 0 |
| `Lrp6` | 4 |
| `Lrp8` | 0 |
| `Vldlr` | 0 |
| `Sort1` | 0 |
| `Sorl1` | 0 |

Direct parquet inspection for the same cell class confirmed that these LDLR
family profiles were actually present with 120-230 matched perturbed nuclei and
17,259 measured genes apiece; the zeros therefore are observed quiet profiles,
not missing count-table entries. Broader secretory/ER stress reference
perturbations were also only low-count in the same table: `Manf` had 3 DEGs,
`Hspa5` had 5, and `Sec63` had 11.

## Synthesis

The biology argues against treating `Lrpap1` as an unreachable target: the
gene is broadly expressed in the assayed nuclei and receptor-client stock
should decline by harvest. The nearest quantitative endpoint evidence argues
against a large count: perturbing the known RAP clients `Lrp1` and `Lrp2`
produced no significant genes in the focal class, the extended receptor-family
set was almost entirely zero, and mild ER/secretory perturbations stayed in the
3-11 DEG range. I therefore centered the forecast at the bottom of the
non-zero single-gene regime rather than at the table-wide high-response tail.

Predicted `n_degs`: 1
