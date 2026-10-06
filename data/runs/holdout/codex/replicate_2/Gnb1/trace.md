# Gnb1 direct DEG-count forecast

## Endpoint

I predicted the held-out count for `Gnb1` in `151 TH Prkcd Grin2c Glut`, where `n_degs` is the number of measured genes with Wilcoxon BH-adjusted `pvals_adj < 0.05`. The focal count table contains 1,674 training targets and excludes `Gnb1`; in that table the response is zero-inflated in this class: 1,205/1,674 targets have `n_degs = 0`, the median is 0, the 75th percentile is 1, and the 95th percentile is 18.

## Gnb1 biology

The declared biology bundle supports real target reach rather than a missing-expression null: in non-target nuclei from the exact focal population, `Gnb1` was detected in 19,830/23,679 cells, with mean CP10k 1.38 and 83.75% of cells expressing. Its functional-stock card also judged that a productive edit should substantially deplete the reusable Gbeta1 pool by the P37-P44 harvest, because a P16 edit stops new intact Gbeta1 supply and the 21-28 day interval is longer than several typical neural-protein lifetimes.

That makes weak engagement an unlikely explanation for a low forecast. The limiting uncertainty is endpoint coupling: Gbeta1 is a heterotrimeric GPCR beta subunit and Gbeta-gamma effector component, not a transcriptional regulator or proteostasis/splicing factor like the largest training responders. Published mouse evidence establishes embryonic neural nonredundancy and postnatal neuronal expression, but does not directly test complete Gnb1 loss initiated at P16 in thalamic neurons.

## Training analogs

I nominated training-available analogs with the curated mouse annotation/corpus nominator against the actual 1,674-gene training universe. The leading specific candidates were proximal GPCR/Gbeta-gamma nodes rather than generic high-response genes:

| nominee rank | target | relation to `Gnb1` | focal `n_degs` |
|---:|---|---|---:|
| 1 | `Gnas` | exact ortholog-projected CORUM heterotrimeric complexes plus GPCR modules | 0 |
| 2 | `Gnb5` | Gbeta/G-protein modules | 0 |
| 3 | `Plcb1` | Gbeta-gamma signaling through PLC beta | 0 |
| 4 | `Adcy5` | GPCR/cAMP signaling modules | 0 |
| 5 | `Calm1` | calcium signaling modules | 14 |
| 6 | `Prkaca` | PKA/cAMP modules | 1 |
| 7 | `Prkar1a` | PKA/cAMP modules | 1 |
| 8 | `Gabbr1` | GABAB/G-protein-gated potassium modules | 1 |
| 9 | `Adcy1` | GPCR/cAMP modules | 0 |
| 10 | `Gnal` | G-protein module and physical interaction evidence | 0 |
| 11 | `Gabbr2` | GABAB/G-protein-gated potassium modules | 1 |
| 12 | `Gnao1` | G-protein module and physical interaction evidence | 1 |
| 13 | `Adcy3` | GPCR/cAMP modules | 0 |
| 14 | `Itpr1` | PLC/calcium effector module | 0 |
| 15 | `Adra2a` | GPCR module | 0 |
| 16 | `Mapk1` | downstream signaling | 0 |
| 17 | `Kcnj6` | G-protein-gated potassium effector | 0 |
| 18 | `Glp1r` | GPCR module | 0 |
| 19 | `Pth1r` | exact ortholog-projected CORUM GPCR complexes | 0 |
| 20 | `Calm3` | calcium signaling modules | 1 |

Among these 20 biologically closest available nominees, 13 had zero DEGs, 6 had only 1-9 DEGs, and only `Calm1` exceeded one DEG. Their median `n_degs` was 0 and their mean was 1.0. A profile comparison in the exact focal class recovered 17,259 measured features for every nominee and confirmed the same sparse pattern: `Gnas`, `Gnb5`, `Plcb1`, and `Adcy5` had no BH-significant genes at all, while `Gnao1` had a single significant gene. The 20-gene corpus topology was a connected explicit-Finding component, so this is a coherent GPCR/G-protein neighborhood rather than an arbitrary list, but its task-matched Perturb-seq outcomes remain nearly null.

## Synthesis

I therefore weighted the analog count distribution more heavily than the broad loss-of-function plausibility. `Gnb1` is expressed and likely edited into a real functional deficit, so I would not treat it like a safe-target negative control; however, the available subunits, receptors, adenylyl cyclases, PLC/calcium nodes, GABAB nodes, and PKA nodes show that perturbing this signaling neighborhood rarely crosses BH FDR in recovered `151 TH Prkcd Grin2c Glut` nuclei. The integer point estimate is:

`predicted_n_degs = 0`
