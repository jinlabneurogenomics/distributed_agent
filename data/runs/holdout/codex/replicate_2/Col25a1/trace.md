# Col25a1 direct DEG-count forecast

Target: `Col25a1`

Cell group: `151 TH Prkcd Grin2c Glut`

Endpoint: measured genes with Wilcoxon `pvals_adj < 0.05` in the focal group.

Predicted `n_degs`: `0`

## Evidence Used

The declared `Col25a1` biology-only bundle made the perturbation plausible but not a strong acute transcriptional driver in this experiment. In the exact focal population, `Col25a1` was detected in 12,027 of 23,679 matched non-target nuclei, or 50.8%, with mean CP10K 0.838. The biology card also judged the P16 to P37-P44 functional stock as only `partially_depleted_or_leading_edge`: COL25A1 has a membrane precursor and a shed extracellular ectodomain, editing should stop new supply, but previously deposited extracellular material may persist, and no target-specific half-life was available. The P25 expression evidence supports observability in postnatal thalamic neurons, while the strong knockout phenotype was embryonic motor-system loss and was not directly transferable to postnatal thalamic glutamatergic nuclei.

The declared focal count table was dominated by silent perturbations. Among 1,674 training targets in `151 TH Prkcd Grin2c Glut`, the median count was 0, 1,205 targets had 0 DEGs, 1,481 had at most 1 DEG, and 1,546 had at most 5 DEGs. Recomputing the self-gene split from `training_de_all_cell_groups.parquet` showed that 1,442 of 1,674 training targets had no non-self DEG in the focal class; target-transcript rows were FDR-significant for only 319 of the 1,642 training targets whose own transcript was measured.

The closest MACIT paralogs nominated by the biology card, `Col23a1` and `Col13a1`, were absent from the training count table. The available collagen comparators were quiet: `Col11a1` had 0 DEGs and `Col2a1` had 0. A broader ECM/adhesion/guidance set was also quiet:

| target | n_degs |
| --- | ---: |
| Adam10 | 0 |
| Adam22 | 1 |
| Adamts17 | 0 |
| Col11a1 | 0 |
| Col2a1 | 0 |
| Cspg4 | 0 |
| Dag1 | 0 |
| Dcc | 0 |
| Epha4 | 1 |
| Itgb1 | 0 |
| Nrxn1 | 1 |
| Nrxn2 | 0 |
| Nrxn3 | 0 |
| Reln | 0 |
| Robo1 | 1 |
| Robo2 | 0 |
| Slit2 | 0 |

Those 17 analogs had a mean count of 0.235 and a maximum of 1. Direct Parquet inspection of the focal class showed that the four 1-DEG cases in this set, `Adam22`, `Epha4`, `Nrxn1`, and `Robo1`, were self-target-only; every listed analog had 0 downstream DEGs after excluding `names == gene_target`. Their matched perturbed-cell counts ranged from 69 to 312 against 23,679 matched controls, so the zeros were observed with ordinary focal-class recovery rather than being a pure missingness boundary.

Profile comparison for 15 matrix/guidance analogs in the exact focal class (`Adam10`, `Adam22`, `Col11a1`, `Col2a1`, `Dag1`, `Dcc`, `Epha4`, `Itgb1`, `Nrxn1`, `Nrxn2`, `Nrxn3`, `Reln`, `Robo1`, `Robo2`, `Slit2`) found 11 profiles with no significant feature and 4 with only 1 to 9 significant features. Across all 105 analog pairs, mean top-tail overlap was 0.040 for positive tails and 0.054 for negative tails, with no recurring significant downstream program.

## Synthesis

`Col25a1` is expressed in the focal thalamic population, so a measurable edit was possible. The operative material, however, is partly extracellular and potentially persistent over the 21-28 day post-edit window; the strongest known loss phenotype is embryonic and in motor neurons rather than an acute postnatal thalamic response; and the available matrix/adhesion/guidance perturbations in the training set were overwhelmingly null in this exact cell group. The only nonzero counts among close functional analogs were single self-transcript hits, while `Col25a1` has no training evidence for a broader shared downstream module. The highest-probability integer forecast is therefore the modal silent outcome:

`predicted_n_degs = 0`
