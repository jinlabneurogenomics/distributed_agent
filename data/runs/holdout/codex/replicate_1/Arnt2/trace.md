# Direct forecast trace

Target: `Arnt2`

Cell class: `151 TH Prkcd Grin2c Glut`

Endpoint: number of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`
in the focal class.

## Biology used

The declared target bundle identifies ARNT2 as a dynamic neuronal bHLH-PAS
DNA-binding transcriptional partner. In mouse neurons, ARNT2 occupies
regulatory elements with NCoR2 at baseline and with activity-induced NPAS4
after depolarization. A P16 disruptive edit should stop new intact ARNT2
supply, and the bundle adjudicates functional ARNT2 stock as likely
substantially depleted by the P37-P44 harvest window.

The bundle also keeps the major dampening uncertainties:

- the severe mouse loss phenotype is an embryonic hypothalamic differentiation
  phenotype, not a postnatal thalamic neuron maintenance test;
- Arnt has partial functional overlap with Arnt2 in embryo/embryonic cortical
  contexts;
- no ARNT2-specific postmitotic thalamic protein lifetime or matched latency
  experiment is available.

The exact in-assay focal reach argues that this is not an absent target, but
that it is sparse enough to be diluted in an aggregate class: `Arnt2` was
detected in `7219 / 23679` non-target focal nuclei, `30.4869%`, with mean raw
UMI `0.4939`, mean log1p CP10k `0.2003`, and pseudobulk CPM `30.957`.

## Training measurements used

The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` table contains
1674 observed training targets for this endpoint. Its count distribution is
strongly concentrated at zero:

| statistic | value |
| --- | ---: |
| zero-count targets | 1205 / 1674 |
| median | 0 |
| 75th percentile | 1 |
| 90th percentile | 2 |
| 95th percentile | 18 |
| mean | 14.05 |
| maximum | 2677 |

The closest ARNT2-adjacent training perturbations that I found in the count
table were quiet or nearly quiet in the focal class:

| training target | focal `n_degs` |
| --- | ---: |
| `Ahr` | 0 |
| `Ahrr` | 0 |
| `Arnt` | 0 |
| `Hif1a` | 0 |
| `Ep300` | 0 |
| `Clock` | 3 |
| `Crebbp` | 8 |

`Npas4` and `Ncor2`, the specific ARNT2 neuronal partners named by the biology
bundle, were not present in the focal count table. I treated `Sin3a` as a
broad chromatin/corepressor boundary rather than a quantitative donor: its
`n_degs = 1433` profile is far larger than the ARNT/AHR/HIF1A-axis
perturbations and less specific to ARNT2.

I also compared the focal Parquet profiles for `Ahr`, `Ahrr`, `Arnt`, `Clock`,
`Crebbp`, `Ep300`, `Hif1a`, and `Sin3a` with the declared profile tool. In
that exact cell class, `Ahr`, `Ahrr`, `Arnt`, `Ep300`, and `Hif1a` all had
`0` significant features among `17259` measured features; `Clock` had `3`;
`Crebbp` had `8`; only the broad boundary `Sin3a` had a large significant set.
Thus the endpoint-matched observed neighborhood did not show a recurrent
high-count state for bHLH-PAS/ARNT-related perturbations.

## Synthesis

I started from the focal training distribution, whose modal outcome is no
detectable DEG. Arnt2 is a real, expressed transcriptional regulator in the
focal population, and the edit should be realized within the 21-28 day window,
so I did not collapse the forecast all the way to an absolute zero prior. The
counterweight is that the closest assayed ARNT/AHR/HIF1A/coactivator
perturbations are zero to single-digit in this same class, while the strongest
published Arnt2 loss phenotype is developmental and outside the postnatal
thalamic context.

My point forecast is therefore a trace response, just above the zero mode but
well below a broad chromatin-regulator footprint:

`predicted_n_degs = 1`
