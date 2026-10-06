# Myt1l n_degs forecast

## Target and endpoint

- Target: `Myt1l`
- Cell class: `151 TH Prkcd Grin2c Glut`
- Endpoint: number of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`
- Prediction: `96`

## Evidence used

The declared count table for this exact thalamic glutamatergic class contains 1,674 training perturbations and is highly zero-inflated:

| Quantity | Value |
| --- | ---: |
| zero DEG targets | 1,205 |
| median | 0 |
| 75th percentile | 1 |
| 90th percentile | 2 |
| 95th percentile | 18 |
| 99th percentile | 430 |
| maximum | 2,677 |

This makes zero the default for an arbitrary target, and a forecast above 50 already places a perturbation in the visible upper tail.

The declared `Myt1l` biology bundle argues against treating `Myt1l` as an arbitrary null:

- Exact focal-class expression is strong: `Myt1l` is detected in 23,238 of 23,679 non-target nuclei, or 98.14%, with mean raw UMI 6.24 and mean log1p-CP10k 1.505.
- MYT1L is a nuclear C2HC zinc-finger transcription factor that represses non-neuronal and earlier neuronal transcriptional programs.
- The operative stock is the MYT1L protein itself, with no durable downstream carrier identified; stopping new synthesis at P16 should likely deplete a substantial fraction of functional protein over the 21-28 day window.
- Adult-brain and postmitotic hippocampal evidence supports an ongoing neuronal role, but it is not an exact P16 thalamic perturbation.

The same bundle leaves several downward scale uncertainties:

- Endogenous MYT1L turnover in postmitotic thalamic neurons was not measured.
- Existing MYT1L protein is not directly destroyed by Cas9 editing.
- Paralog compensation by `Myt1` or `St18` is unresolved.
- Existing phenotype evidence is from hippocampal, cortical, germline, or adult-deficient systems rather than the exact recovered thalamic population.

Measured training perturbations gave these focal-class DEG counts for a hand-selected transcription-factor/chromatin bracket:

| Training target | `n_degs` |
| --- | ---: |
| `Sin3a` | 1433 |
| `Zbtb7a` | 841 |
| `Yy1` | 720 |
| `Cic` | 576 |
| `Phf12` | 403 |
| `Brd4` | 311 |
| `Rora` | 278 |
| `Zfp423` | 150 |
| `Tcf7l2` | 106 |
| `Chd4` | 100 |
| `Chd8` | 61 |
| `Adnp` | 25 |
| `Mecp2` | 16 |
| `Setd5` | 9 |
| `Mef2c` | 1 |
| `Tcf4` | 0 |
| `Bcl11a` | 0 |
| `Satb2` | 0 |
| `Sox11` | 0 |

The very large `Sin3a`/`Yy1`/`Cic`/`Zbtb7a` values show the scale of broad regulatory hits but are too global for `Myt1l`. Conversely, many postmitotic or developmental neuronal TFs are exact zeros. I treated `Rora`, `Zfp423`, `Tcf7l2`, and `Chd8` as the nearest quantitative bracket for an expressed, neuron-relevant transcriptional regulator with a nonzero but focused response; their counts span 61-278 and center near one hundred on a log scale. `Adnp`, `Mecp2`, and `Setd5` were kept as lower active boundaries.

The expression-profile comparison of these observed regulators in `151 TH Prkcd Grin2c Glut` did not reveal a discrete profile module that should override the direct counts. `Rora` had 278 significant genes, `Zfp423` 150, `Chd8` 61, and `Adnp` 25, with both positive and negative significant features in each profile. The closest whole-profile neighbors of `Rora` and `Zfp423` included lower-count or zero-count TFs as well as active regulators, so profile topology supported a broad TF/chromatin response class rather than a calibrated DEG burden.

## Synthesis

`Myt1l` is likely expressed and functionally reachable at harvest, so I moved well above the empirical zero/low-count prior. I kept the point far below broad chromatin and RNA-processing outliers because MYT1L is a sequence-specific neuronal-identity repressor and because the timing, residual protein, and thalamic transfer uncertainties all make a thousand-gene survivor signature unlikely. The resulting point, `96`, sits near `Tcf7l2` and between the `Chd8` and `Zfp423` training responses: a clearly detectable but not catastrophic response.

No `Myt1l` target expression signature or `Myt1l` endpoint count was used.
