# Direct forecast for `Sdccag8`

## Target and endpoint

- **Target:** `Sdccag8`
- **Focal population:** `151 TH Prkcd Grin2c Glut`
- **Endpoint:** `n_degs`, the count of measured genes with BH-adjusted Wilcoxon `p < 0.05`
- **Point prediction:** `0`

The target was read from the one-row holdout manifest / declared biology bundle. I did not use a held-out `Sdccag8` differential-expression signature or `Sdccag8` DEG count.

## Biology used

The prediction-safe `Sdccag8` characterization bundle describes SDCCAG8 as an installed centrosomal / centriolar-satellite and ciliary structural component:

- SDCCAG8 localizes to centrioles and cytoplasmic centriolar-satellite puncta, interacts or co-trafficks with PCM1, and can affect centrosomal gamma-tubulin / pericentrin recruitment in developing mouse cortical neurons.
- The mouse loss phenotype in the bundle is developmental or tissue-specialized: cortical neuronal migration / positioning, retina, and kidney. The card did not find a matched acute post-P16 thalamic-neuron loss phenotype.
- The functional-stock adjudication says a coding edit should stop new SDCCAG8 production, but an already installed centrosomal/ciliary pool need not be dismantled immediately; no target-specific turnover or 21-28 day functional-depletion evidence was available.
- The exact non-target focal-population expression measurement does show that `Sdccag8` is transcriptionally reachable in this cell class: mean 1.12 cp10k, mean raw UMI 1.73, and 18,573 / 23,679 cells expressing, or 78.4%.

My read is therefore: the target is genuinely present in the assayed thalamic nuclei, but the operation is a structural/ciliary loss whose acute realization in postmitotic neurons is uncertain. That pushes the expected focal signature toward the quiet structural-cilia training perturbations rather than toward high-DEG developmental or broad RNA-processing perturbations.

## Training measurements used

The focal-class training count table contains 1,674 perturbations. Its `n_degs` distribution is highly zero-skewed:

- median `0`
- 75th percentile `1`
- 90th percentile `2`
- 95th percentile `18`
- mean `14.05`, driven by a small high-count tail
- 469 / 1,674 nonzero

I used the deterministic gene-annotation store to choose ciliary / centrosomal training perturbations related to `Sdccag8`, rather than selecting by symbol spelling.

Closest structural groups in the same focal count table were mostly null:

| prior group | training targets | median `n_degs` | mean `n_degs` | informative counts |
| --- | ---: | ---: | ---: | --- |
| GO centriolar satellite, `GO:0034451` | 19 | 0 | 1.63 | `Mib1` 27, `Cltc` 3, `Ttc8` 1, all other members 0 |
| GO regulation of cilium assembly, `GO:1902017` | 5 | 0 | 0.40 | `Cdkl5` 1, `Syne1` 1, `Atg5` / `Cyld` / `Ift88` 0 |
| Reactome 9+0 primary-cilium assembly, `R-MMU-9975921` | 29 | 0 | 3.10 | `Dctn1` 75, `Tuba1a` 7, six one-count targets, and 21 zeros |
| Reactome BBSome-mediated cargo targeting to cilium, `R-MMU-5620922` | 4 | 0 | 0.25 | `Ttc8` 1, `Bbs5` / `Lztfl1` / `Mchr1` 0 |

I then inspected the raw focal-class Parquet for a closer hand-bounded ciliary/transition-zone/IFT cohort:

`B9d1`, `Bbs5`, `Cep290`, `Cspp1`, `Dzip1`, `Ift43`, `Ift88`, `Iqcb1`, `Lztfl1`, `Rpgrip1l`, `Sclt1`, `Ttc21b`, `Ttc8`, `Arl3`, `Dync2h1`, `Ift81`, `Kif3b`.

All 17 profiles were present in the training Parquet for `151 TH Prkcd Grin2c Glut`. Their exact focal `n_degs` were:

- `Arl3`: 1
- `Ttc8`: 1
- all other 15 selected structural genes: 0

The only FDR-significant genes in the two one-count cases were the perturbed transcripts themselves:

| target | significant feature | logFC | BH-adjusted p |
| --- | --- | ---: | ---: |
| `Arl3` | `Arl3` | -0.418 | 0.0184 |
| `Ttc8` | `Ttc8` | -0.663 | 0.000031 |

Thus this local analog set did not show any reproducible downstream thalamic glutamatergic response. The 15 / 17 zero rate, the analog median of 0, and the lack of any non-self significant feature in the two weakly nonzero profiles were the quantitative observations that determined the forecast.

## Synthesis

`Sdccag8` has enough focal expression that an RNA effect was possible. I did not round it down merely because the target is absent from the count table. The stronger evidence, however, was that acute perturbation of structurally close ciliary/centriolar-satellite and IFT/transition-zone genes in this exact cell class was almost always below the BH `p < 0.05` endpoint, even before discounting genes like `Dctn1`, `Mib1`, `Cltc`, and tubulins whose higher counts plausibly reflect broader cytoskeletal or ubiquitin/signaling functions rather than SDCCAG8-like transition-zone stock depletion.

The bundle's functional-stock call adds a second downward bearing: a disruptive edit is expected to stop new functional SDCCAG8 supply, but available evidence does not establish that the already installed centriolar/ciliary material is depleted by the P37-P44 harvest. I therefore placed the target at the modal quiet outcome of the closest training analogs.

Final predicted `n_degs`: **0**
