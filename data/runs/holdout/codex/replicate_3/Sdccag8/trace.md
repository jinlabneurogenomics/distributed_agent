# Direct DEG-count forecast for Sdccag8

## Target and endpoint

- Holdout target: `Sdccag8`, from the declared one-row manifest.
- Endpoint: `n_degs` in `151 TH Prkcd Grin2c Glut`, the number of measured genes with BH-adjusted Wilcoxon `p < 0.05`.
- Training measurements used: the declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` count table and the matching rows of `training_de_all_cell_groups.parquet`.
- Same-experiment corpus evidence was used only for training perturbations. I did not use the withheld `Sdccag8` signature or DEG count.

## Target biology

The biology bundle places SDCCAG8 at centrioles and centriolar satellites, with PCM1-associated roles in pericentriolar-material recruitment, microtubule organization, neuronal migration, and cilium organization. It also states that the mouse neuronal evidence comes from embryonic cortical development or specialized retinal/renal contexts, not from postnatal thalamic neurons. The functional-stock card therefore treats SDCCAG8 as an already installed structural component: a disruptive edit should block new SDCCAG8 supply, but there is no target-specific turnover or acute-depletion measurement proving that the centriolar or ciliary functional pool is gone by the 21-28 day P16-to-P37/P44 interval.

Exact in-assay reach is not limiting: `Sdccag8` is detected in `18,573 / 23,679` non-target nuclei in this focal population, or `78.44%`, with mean expression `1.1176` CP10k. That argues against a zero solely from lack of transcript detection, but the functional-stock uncertainty and developmental mismatch make a large postnatal survivor-state transcriptional program unlikely.

## Training evidence

The requested cell class is sparse in the held-in count table:

- 1,205 of 1,674 training perturbations have `n_degs = 0`.
- 1,481 of 1,674 have `n_degs <= 1`.
- 1,512 of 1,674 have `n_degs <= 2`.
- The median is `0`, the 75th percentile is `1`, and the heavy right tail is dominated by housekeeping, splicing, proteostasis, chromatin, or transcriptional regulators rather than ciliary/centrosomal genes.

The closest represented ciliary/centrosomal training perturbations were quiet in the exact `151 TH Prkcd Grin2c Glut` count table:

| perturbation | role used for this forecast | 151 n_degs |
| --- | --- | ---: |
| `B9d1` | transition-zone / ciliopathy comparator | 0 |
| `Bbs5` | BBSome comparator | 0 |
| `Cep290` | transition-zone comparator | 0 |
| `Dync2h1` | retrograde IFT / ciliary dynein comparator | 0 |
| `Ift43` | IFT-A comparator | 0 |
| `Ift81` | IFT-B comparator | 0 |
| `Ift88` | IFT-B comparator | 0 |
| `Kif3b` | anterograde ciliary kinesin / KIF3 comparator | 0 |
| `Nin` | centrosome comparator | 0 |
| `Rpgrip1l` | transition-zone comparator | 0 |
| `Ttc21b` | IFT-A comparator | 0 |
| `Arl3` | ciliary trafficking comparator | 1 |
| `Ttc8` | BBSome comparator | 1 |

A matched Parquet profile comparison over those 13 measured perturbations recovered no missing profiles and found 11 with no FDR-significant genes in this cell class; the five most central zero-count comparators inspected directly (`B9d1`, `Bbs5`, `Cep290`, `Dync2h1`, `Ift88`) each had `significant_feature_count = 0`. Their self-transcript rows in `151 TH Prkcd Grin2c Glut` were also non-significant for `B9d1`, `Bbs5`, `Cep290`, `Ift43`, `Ift81`, `Ift88`, `Kif3b`, `Nin`, `Rpgrip1l`, and `Ttc21b`, so the zeroes are not just a downstream program hidden beneath self-knockdown singletons.

The packaged Finding ledger for these training ciliary genes independently summarizes the same Perturb-seq surface as broadly buffered: `Cep290`, `Dync2h1`, `Ift43`, `Ift81`, `Kif3b`, `Nin`, `Rpgrip1l`, and `Ttc8` are described as null or nearly null across recovered postnatal neuronal groups, and expected Hedgehog, ciliary-GPCR, IFT, or BBSome transcriptional modules were not recovered after several of these perturbations. This is not independent replication, but it supports interpreting their zero `151` counts as an assay-local ciliary buffering pattern rather than a CSV artifact.

## Synthesis

`Pcm1`, the most direct SDCCAG8 partner named in the biology card, is absent from the `151` count table, so the forecast cannot use an exact PCM1-satellite training analogue. I therefore weighted the represented ciliopathy/transition-zone/IFT/BBSome genes above weaker cytoskeletal comparators such as `Dctn1`, `Tuba1a`, or `Wdr26`.

The upward evidence is real but limited: `Sdccag8` is detectably expressed in the focal thalamic nuclei and no close paralog was found. The downward evidence is stronger: SDCCAG8 is an installed centrosomal/satellite component with unresolved depletion by harvest, its demonstrated neuronal phenotype is developmental rather than acute postnatal thalamic, and the best available ciliary training perturbations are almost all `0` in the requested population. A single self-transcript hit is possible, but the matched ciliary rows show that even negative self log-fold changes often fail the BH threshold in this class.

Point forecast: `0` DEGs.
