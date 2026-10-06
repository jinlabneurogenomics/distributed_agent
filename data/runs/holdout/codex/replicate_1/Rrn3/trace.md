# Rrn3 direct n_degs forecast

## Target and endpoint

- Target: `Rrn3`
- Cell class: `151 TH Prkcd Grin2c Glut`
- Endpoint: `n_degs`, the number of measured genes with BH-adjusted Wilcoxon `p < 0.05`
- Point prediction: `48`

## Evidence used

The outcome-blind Rrn3 biology bundle supported target engagement and focal-cell reach. Rrn3 is the RRN3/TIF-IA RNA polymerase I initiation factor for ongoing pre-rRNA synthesis. Exact non-target expression in the focal population was available and high: 18,688 of 23,679 nuclei expressed Rrn3, with mean raw UMI 1.8419, mean log1p CP10K 0.6679, and pseudobulk CPM 115.44. The functional-stock adjudication concluded that RRN3-dependent initiation capacity is likely substantially depleted by harvest: adult-neuron Rrn3 deletion suppresses nascent 47S pre-rRNA and nucleolar RRN3 by about one month, and the target protein itself is unlikely to persist for the 21-28 day edit-to-harvest interval.

That same bundle also argued against an immediate, unbuffered catastrophe in recovered nuclei. Mature 18S rRNA was not significantly reduced one month after adult hippocampal neuronal Rrn3 deletion despite strong pre-rRNA inhibition, so newly lost Pol I initiation is buffered by an installed rRNA/ribosome pool. This makes a nonzero survivor-state transcriptional response likely, but not a thousand-gene response by itself.

The declared 151-class training table contained 1,674 observed targets. Its distribution was extremely sparse and long-tailed: 1,205 targets had zero DEGs, the median was 0, the 90th percentile was 2, the 95th percentile was 18, the 99th percentile was 430, and the maximum was 2,677. Only 78 of 1,674 targets exceeded 20 DEGs, and only 15 exceeded 500.

The closest measured RNA-production and ribosome-biogenesis comparators in the exact endpoint were small to intermediate rather than tail events:

| training target | 151 n_degs |
| --- | ---: |
| `Taf1b` | 0 |
| `Las1l` | 0 |
| `Rbm28` | 0 |
| `Mtor` | 2 |
| `Bdp1` | 8 |
| `Ddx3x` | 8 |
| `Polr3b` | 8 |
| `Nop56` | 25 |
| `Tsc2` | 86 |

The same Parquet, queried in `151 TH Prkcd Grin2c Glut`, showed that these counts were not hiding broad rank-level signatures comparable to the high tail. `Nop56` had 25 total FDR<0.05 genes in 151, with a compact RNA-processing branch headed by `Rsrp1`, `Ddx17`, `Srsf5`, `Tcea2`, `Srsf11`, and `Ddx5`. `Polr3b` and `Ddx3x` each had 8 151-class calls. In contrast, broad stress and RNA-processing perturbations in the top tail, such as `Uba5`, `Rnpc3`, `U2af2`, `Psmb4`, `Ufc1`, and `Psmc1`, had 430-2,677 DEGs in the same table and much larger signed Wilcoxon tails.

Packaged same-experiment Findings were useful for interpreting the analogs rather than just reading their counts. `Nop56` was reported as a narrow postnatal neuronal response concentrated in 151 TH, without activation of a canonical p53, unfolded-protein, integrated-stress, or autophagy program. `Taf1b`, a core SL1/Pol I initiation factor, was flat across the recovered juvenile neuronal mRNA surface, and the report explicitly treated direct 47S pre-rRNA, nucleolar morphology, and DNA engagement as unmeasured. `Polr3b` produced a sparse, cell-selective protein-coding mRNA module rather than a broad Pol III or transcription-production shutdown signature. Together these training results show that nearby RNA-production hits are factor-specific and often buffered in this assay.

## Forecast rationale

I placed Rrn3 above the immediate 0-25 neighborhood of `Taf1b`, `Polr3b`, and `Nop56` because the target has high focal-population expression, no close redundant initiation factor in the bundle, and direct adult-neuron evidence that RRN3-dependent pre-rRNA synthesis is strongly impaired on the same approximate time scale as harvest.

I placed it below the hundreds-to-thousands tail because the survivor-conditioned snRNA endpoint repeatedly damped nucleolar, Pol I/III, and ribosome-processing perturbations, mature rRNA can persist for the relevant interval, and Rrn3 biology does not point to the unfolded-protein, UFMylation, proteasome, or spliceosome programs that dominate the broadest 151 signatures.

Numerically, that made `Tsc2 = 86` an approximate upper training anchor for a translation/growth-state disturbance and `Nop56 = 25` the closest nucleolar lower anchor. I selected a midpoint biased toward `Nop56`, giving a final direct point forecast of 48 DEGs.
