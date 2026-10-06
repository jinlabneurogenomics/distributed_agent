# Irf7 DEG-count forecast

## Target and endpoint

- Target perturbation: `Irf7`.
- Cell class: `151 TH Prkcd Grin2c Glut`.
- Endpoint: `n_degs`, the count of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05` in this cell class.
- Forecast: `0`.

## Evidence used

### Exact focal-population target reach

The prediction-safe `Irf7` biology bundle reports that `Irf7` itself is detectable but very sparse in the matched non-target 151-class nuclei:

- `762 / 23679` matched non-target nuclei express `Irf7`, i.e. `3.2180413024198655%`.
- `mean_log1p_cp10k = 0.020752198995954377`.
- `mean_raw_umi = 0.04784830440474682`.
- `pseudobulk_cpm = 2.998822913040856`.

This made broad loss-of-function realization plausible only for the small homeostatic subset that actually expresses `Irf7`; most recovered thalamic glutamatergic nuclei have no detected baseline transcript.

### Biology of the perturbation

The canonical `Irf7` bundle supports true depletion of IRF7 protein by P37-P44 where the gene is edited and expressed: IRF7 is an inducible DNA-binding transcription factor, its measured mouse protein turnover is on an hours scale, and the functional-stock card calls its stock `likely_substantially_depleted` by the 21-28 day harvest window.

The same bundle also argues that the relevant operation is context-dependent. The strongest Irf7-loss phenotypes are type-I-interferon and viral-encephalitis phenotypes, while uninfected mouse CNS has low constitutive IRF7 and viral infection induces IRF7 in CNS cells including neurons. Therefore the edit should remove an inducible antiviral amplifier, but the uninfected, postnatal, recovered thalamic-neuron assay has weak evidence for a standing IRF7-dependent transcriptional program.

### 151-class training counts

The declared 151-class training count table contains 1,674 observed perturbations:

- 1,205 have `n_degs = 0`.
- Median `n_degs = 0`.
- 75th percentile `n_degs = 1`.
- 90th percentile `n_degs = 2`.
- Mean `n_degs = 14.05`, pulled upward by a very small high-burden tail.

Thus a zero-DEG result is common even in this high-yield cell class; large DEG counts are outlier events and need a matched reason to transfer.

### Matched innate / interferon training perturbations

I used the count table to choose observed perturbations that sit near the IRF7 antiviral circuit, then checked their exact row-level results in the expression Parquet for `151 TH Prkcd Grin2c Glut`.

IRF-family targets:

| target | n_degs |
|---|---:|
| `Irf1` | 0 |
| `Irf2` | 0 |
| `Irf3` | 0 |
| `Irf5` | 0 |
| `Irf8` | 0 |
| `Irf9` | 0 |

Innate receptor targets:

| target | n_degs |
|---|---:|
| `Ifih1` | 0 |
| `Tlr2` | 0 |
| `Tlr3` | 0 |
| `Tlr4` | 0 |
| `Tlr5` | 0 |
| `Tlr7` | 0 |
| `Tlr8` | 0 |

Downstream innate / interferon regulators available in the same table:

| target | n_degs |
|---|---:|
| `Adar` | 0 |
| `Nfkb1` | 0 |
| `Stat1` | 1 |
| `Stat2` | 0 |
| `Traf3` | 0 |

The Parquet slice confirmed that each of these perturbations had 17,259 measured rows in the focal class. Across all 18 selected perturbations, the only BH-significant row was `Stat1` under `Stat1` perturbation, with `pvals_adj = 0.0270288`; the IRF-family, TLR-family, `Ifih1`, `Adar`, `Nfkb1`, `Stat2`, and `Traf3` perturbations had no significant measured genes. Interferon-stimulated module rows such as `Oas1g`, `Usp18`, `Ifi44`, `Ifitm3`, and `Rsad2` were not significant in this matched quiescent 151-class context.

## Synthesis

I treated the training count table as the calibrated experimental scale and used the Parquet only to verify that the near-neighbor innate genes were true focal-class nulls rather than count-table artifacts.

The edit should deplete IRF7 protein in the rare nuclei with active target expression, so I did not downweight for protein persistence. The limiting factors were instead reach and state: `Irf7` is detected in only 3.2% of matched non-target 151-class nuclei, its biological role is inducible antiviral transcription rather than a constitutive neuronal maintenance process, and the matched observed knockouts of IRF-family, TLR-family, and interferon-pathway genes are almost all zero-DEG perturbations in exactly this cell class. The one significant comparator row, `Stat1` self-knockdown, is not evidence for a broad interferon-response shift.

The rare high-`n_degs` 151-class perturbations are dominated by broadly used chromatin, RNA-processing, proteostasis, and core cellular genes. `Irf7` does not resemble those broad-effect training targets under unchallenged thalamic-neuron conditions. My point forecast is therefore the modal matched outcome:

```tsv
target_name	predicted_n_degs
Irf7	0
```
