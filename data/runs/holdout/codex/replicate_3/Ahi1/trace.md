# Direct forecast trace

## Target and endpoint

- Target perturbation: `Ahi1`.
- Focal population: `151 TH Prkcd Grin2c Glut`.
- Endpoint: `n_degs`, the number of measured genes in this population with BH-adjusted Wilcoxon `p < 0.05`.

## Evidence used

1. The declared `Ahi1` biology bundle shows exact focal-population reach: `Ahi1` was assayed in `151 TH Prkcd Grin2c Glut`, with mean CP10K 2.192 and expression in 21,822 of 23,679 non-target nuclei, or 92.16%. This made absence of target expression an unlikely explanation for a null signature, while still not proving editing efficiency or downstream dependence.

2. The same bundle supports postnatal neuronal relevance but only partial realization of the acute lesion. Ahi1 acts both at neuronal ciliary transition zones and in endocytic signaling; loss produces mouse neural phenotypes in retina and neuronal conditional models. The P16 edit would stop new Ahi1 supply, but the bundle adjudicates `functional_stock_by_harvest` as `partially_depleted_or_leading_edge` because existing cytoplasmic and ciliary pools could persist into the P37-P44 harvest.

3. I used the declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` count table to inspect pathway-matched, outcome-observed training perturbations. Core primary-cilium/transition-zone or IFT comparators were all focal nulls:

| training perturbation | rationale | focal `n_degs` |
|---|---|---:|
| `B9d1` | ciliary transition-zone/B9 complex | 0 |
| `Bbs5` | BBSome/ciliary trafficking | 0 |
| `Cep290` | transition-zone ciliopathy gene | 0 |
| `Dync2h1` | dynein-2 retrograde IFT | 0 |
| `Ift43` | IFT-A | 0 |
| `Ift88` | IFT-B | 0 |
| `Kif3b` | anterograde ciliary kinesin | 0 |
| `Rpgrip1l` | transition-zone ciliopathy gene | 0 |
| `Ttc21b` | IFT-A / ciliary transport | 0 |

4. The Ahi1 source card also linked Ahi1 to the Hap1/TrkB trafficking axis. Its closest observed training readouts were again weak in this focal class: `Hap1` had 0 DEGs, and `Ntrk2` had 3.

5. I treated `Rab7` as a boundary rather than a numeric analogue. It had 501 focal DEGs, but its same-experiment findings describe a broad late-endosomal/lysosomal, sterol, ISR/UPR, amino-acid, autophagy, and redox/apoptotic stress state. That is a much larger endolysosomal response than the Ahi1 card supports for an acute transition-zone/trafficking scaffold lesion.

6. I checked the signed Wilcoxon profiles for `B9d1`, `Bbs5`, `Cep290`, `Dync2h1`, `Ift43`, `Ift88`, `Kif3b`, `Rpgrip1l`, `Ttc21b`, `Hap1`, `Ntrk2`, and `Rab7` in the training Parquet, filtered to `151 TH Prkcd Grin2c Glut`. Ten of the twelve selected nodes had no FDR-significant features, `Ntrk2` was in the 1-9 bin, and only the boundary node `Rab7` was in the at-least-50 bin. Across all 66 selected pairs, the cohort had mean positive and negative top-tail overlap coefficients of only 0.0249 and 0.0316, so these perturbations did not hide a coherent ciliary response that would justify lifting Ahi1 far above the focal count table's null ciliary comparators.

## Synthesis

The most direct quantitative evidence was the focal count table: every training perturbation that most closely matched Ahi1's ciliary-transition-zone/IFT biology had `n_degs = 0`, and the two Ahi1-linked TrkB/Hap1 trafficking nodes were 0 and 3. Exact Ahi1 expression in the assayed cells and incomplete evidence for redundancy argue that a small nonzero response was possible, but the acute P16/P37-P44 design, uncertain installed ciliary protein turnover, and repeated transcriptional buffering of ciliary machinery in the same atlas made a null thalamic signature the strongest point prediction.

Predicted `n_degs`: 0.
