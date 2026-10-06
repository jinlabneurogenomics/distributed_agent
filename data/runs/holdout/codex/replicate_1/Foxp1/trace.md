# Foxp1 in `151 TH Prkcd Grin2c Glut`

## Endpoint and declared target

- Target: `Foxp1`, from the one-row holdout manifest.
- Endpoint: `n_degs`, the number of measured genes with Wilcoxon BH-adjusted `p < 0.05` in `151 TH Prkcd Grin2c Glut`.
- I used the declared biology bundle, the declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` count table, and the declared `training_de_all_cell_groups.parquet` training expression profiles. I did not use a Foxp1 perturbation signature or a Foxp1 DEG count.

## Target biology

- The in-assay focal-population reach is real but incomplete: in matched non-target nuclei from `151 TH Prkcd Grin2c Glut`, `Foxp1` had mean CP10K `0.7517`, mean raw UMI `1.1523`, and was detected in `11868 / 23679` nuclei, or `50.12%`.
- The functional-stock card classifies Foxp1 as a soluble nuclear DNA-binding transcription factor, not an installed structural product; by P37-P44 after P16 editing, intact pre-edit functional stock is expected to be substantially depleted if the genomic lesion is present.
- The observability card keeps the effect uncertain rather than high. Foxp1 has postnatal mouse neuronal relevance, but the direct evidence is striatal/forebrain rather than thalamic, and thalamic expression is regionally restricted. Foxp2/Foxp4 compensation is also possible but untested in the focal thalamic neurons.

Interpretation: target mRNA expression and expected protein turnover argue against a pure "target absent" prediction, but half-population expression plus untested thalamic dependence predict a small, potentially diluted survivor-state RNA footprint.

## Training measurements that set the scale

The direct count table for `151 TH Prkcd Grin2c Glut` is extremely floor-heavy:

- total training perturbations: `1674`
- `n_degs = 0`: `1205`
- `n_degs = 1`: `276`
- `n_degs = 2`: `31`
- `n_degs = 3-9`: `56`
- `n_degs = 10-49`: `47`
- `n_degs = 50-499`: `44`
- `n_degs >= 500`: `15`

The median count is `0`, the 90th percentile is `2`, and the mean is pulled up to `14.05` by a small number of very large RNA-processing/proteostasis/chromatin perturbations.

I then used a hand-selected Foxp1-like training cohort of FOXP/forkhead and neural transcriptional regulators. Their focal-class counts were:

| Training perturbation | `n_degs` |
|---|---:|
| Foxp2 | 0 |
| Foxa2 | 0 |
| Foxj3 | 0 |
| Foxk2 | 0 |
| Foxl1 | 0 |
| Foxl2 | 0 |
| Foxn1 | 0 |
| Foxp3 | 0 |
| Bcl11b | 0 |
| Mef2c | 1 |
| Tcf4 | 0 |
| Satb2 | 0 |
| Sox5 | 2 |
| Tbr1 | 0 |
| Sox11 | 0 |
| Mecp2 | 16 |

Within the profile-analysis subset with complete focal-class profiles, `9 / 12` analog perturbations had no BH-significant features, `2 / 12` had only `1-9`, and `1 / 12` had `10-49`. The count mean for those 12 was `1.58`, the median was `0`, and the maximum was the broader neuronal regulator `Mecp2` at `16`.

## Same-experiment corpus checks

The packaged Foxp2 report was the most relevant same-family training evidence:

- `Foxp2:F001`: Foxp2 produced no FDR `< 0.10` downstream response in any of its 22 measured neuronal groups.
- `Foxp2:F004`: postnatal transcription-factor detectability is factor-specific; Tbr1 and Mef2c had real DE surfaces in matched groups, whereas Foxp2, Bcl11b, and Satb2 were flat.

That makes the Foxp2 null informative rather than simply an assay-wide inability to detect TF perturbations.

## Synthesis

I weighted the closest family/training evidence toward the floor: Foxp2 and the represented forkhead factors were all `0` in the focal class, and most neurodevelopmental TFs around the same developmental identity axis were also `0`. I did not use the large-count housekeeping and RNA-processing perturbations as analogs because Foxp1 is a regionally expressed neuronal TF rather than a ubiquitous core expression/proteostasis factor.

I moved the point slightly above `0` because the exact focal reach shows Foxp1 is expressed in half of the relevant thalamic nuclei and the biology bundle supports depletion of an actively renewed nuclear regulator by harvest. The resulting forecast is a tiny but nonzero response, below `Mecp2` and close to the weakest active TF comparators.

Predicted `n_degs`: `2`.
