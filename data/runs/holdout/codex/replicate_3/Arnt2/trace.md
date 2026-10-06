# Arnt2 n_degs forecast

Target: `Arnt2` in `151 TH Prkcd Grin2c Glut`.

Endpoint: number of measured genes in the focal class with Wilcoxon BH-adjusted
`p < 0.05`.

## Evidence used

### Declared target biology

- The one-row holdout manifest and the declared biology bundle both name
  `Arnt2`.
- Exact in-assay focal expression is present but not broad: non-target
  `151 TH Prkcd Grin2c Glut` nuclei have mean raw expression 0.494 UMI,
  mean CP10K 0.322, pseudobulk CPM 30.96, and 7,219/23,679 cells expressing
  `Arnt2` RNA, or 30.49%.
- The functional-stock card calls ARNT2 a dynamic nuclear bHLH-PAS
  transcriptional-complex component. A P16 disruptive edit should stop new
  intact ARNT2 supply, and because the P37-P44 harvest is 21-28 days later,
  ARNT2 functional stock is likely substantially depleted.
- Endpoint observability is weaker than realization: the strong mouse loss
  phenotype is embryonic hypothalamic differentiation/perinatal survival rather
  than an inducible postnatal thalamic-neuron assay, ARNT can preserve some
  overlapping bHLH-PAS functions, and the card marks postnatal relevance,
  phenotype latency, and redundancy in the focal context as unresolved.

### Training counts in the same focal population

The declared focal count table contains 1,674 observed training perturbations
and is extremely sparse:

- 1,205/1,674 have `n_degs = 0`.
- median = 0.
- 75th percentile = 1.
- 1,527/1,674 have `n_degs <= 3`.

### Chosen observed perturbations

I used PAS-family, ARNT/HIF/AHR-proximal, and activity-TF comparators rather
than generic chromatin-regulator hits.

| perturbation | rationale | focal `n_degs` |
| --- | --- | ---: |
| `Arnt` | closest paralog / partial functional overlap named in the Arnt2 biology bundle | 0 |
| `Ahr` | bHLH-PAS receptor using the ARNT-family dimerization axis | 0 |
| `Ahrr` | AHR-axis regulator | 0 |
| `Hif1a` | bHLH-PAS hypoxia partner whose activity can use ARNT/ARNT2-family dimers | 0 |
| `Npas3` | neuronal PAS-family TF in the screen | 0 |
| `Nr4a1` | activity-linked nuclear receptor control | 0 |
| `Clock` | core bHLH-PAS clock factor | 3 |
| `Creb1` | broader activity-dependent TF | 10 |
| `Bmal1` | bHLH-PAS circadian partner | 103 |

The expression Parquet confirmed that the closest zero-count comparators were
not near threshold in `151 TH Prkcd Grin2c Glut`: the smallest focal adjusted
p-values were 1.0 for `Arnt`, `Ahrr`, `Npas3`, and `Nr4a1`, 0.306 for `Hif1a`,
and 0.221 for `Ahr`; matched perturbed-cell recovery for these analogs was
ordinary for this focal class, 93-209 nuclei. The only larger PAS-family count,
`Bmal1`, was led by canonical circadian genes (`Dbp`, `Nr1d2`, `Nr1d1`), so I
treated it as an off-axis circadian program rather than a scale-matched ARNT2
proxy.

## Synthesis

The perturbation should plausibly remove much of the renewable ARNT2 pool by
harvest, so I did not treat the edit as biologically impossible. The assay
projection is still weak: only about one third of focal non-target nuclei show
detectable `Arnt2`, postnatal thalamic dependence is untested, and ARNT-family
redundancy is a real buffer. In the exact measured population, the closest
observed partner/paralog/PAS analogs are null at FDR 0.05, and the focal
training distribution strongly favors zero or one DEG for non-core regulators.

Those facts make a broad survivor transcriptional program less likely than a
quiet or subthreshold perturbation, and the more distant `Bmal1` circadian
response is not an appropriate magnitude donor. I therefore predict the
zero-DEG mode.

Predicted `n_degs`: 0
