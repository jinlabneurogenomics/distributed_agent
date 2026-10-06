# Direct forecast for Nlgn1 in `151 TH Prkcd Grin2c Glut`

## Target and endpoint

- Held-out target: `Nlgn1`.
- Endpoint: `n_degs`, the number of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05` in `151 TH Prkcd Grin2c Glut`.
- Declared focal expression reach for `Nlgn1`: feature available, 10,867/23,679 non-target nuclei expressing the transcript, 45.89% expressing, mean raw UMI 0.714, mean cp10k 0.449, pseudobulk CPM 44.73.
- I did not use a target `Nlgn1` Perturb-seq signature, target DEG count, calibrated response probability, labeled-neighbor outcome, or endpoint-selection metadata.

## Biology bearing

The biology bundle supports that the P16 CRISPR perturbation should be capable of removing operative NLGN1 by the P37-P44 harvest: NLGN1 is a dynamic postsynaptic transmembrane adhesion/scaffold component at excitatory synapses, existing surface molecules exchange or can be cleaved on hour-scale observations, and P21 conditional loss in postmitotic CA1 neurons removed an NLGN1-dependent mature-neuron function within 2-3 weeks. This argues against treating the perturbation as biologically inert.

That same evidence does not imply a large nuclear-RNA response in the thalamic recovered-cell assay. The best functional timing evidence is hippocampal electrophysiology, not thalamic snRNA-seq, and the NLGN1 operation is local postsynaptic adhesion rather than a chromatin, splicing, proteostasis, or metabolic hub.

## Training-count evidence

The declared focal count table has 1,674 measured training perturbations and is highly zero-inflated:

- 1,205/1,674 have `n_degs = 0`.
- Median = 0, 75th percentile = 1, 90th percentile = 2.
- Only 106/1,674 are at least 10, and the extreme right tail is dominated by broad nuclear or proteostasis perturbations such as `Uba5`, `Tpr`, `Sin3a`, and `Rnpc3`.

The nearest hand-selected NLGN1-like training perturbations were all small-count except the broad NMDA core-subunit perturbation:

| training perturbation | focal `n_degs` |
|---|---:|
| `Nlgn3` | 1 |
| `Lrrtm1` | 1 |
| `Lrrtm3` | 0 |
| `Lrrtm4` | 0 |
| `Nrxn1` | 1 |
| `Nrxn2` | 0 |
| `Nrxn3` | 0 |
| `Adgrl1` | 1 |
| `Adgrl2` | 1 |
| `Adgrl3` | 1 |
| `Cadm2` | 1 |
| `Cntnap1` | 1 |
| `Cntnap2` | 1 |
| `Dlg4` | 1 |
| `Shank2` | 0 |
| `Shank3` | 2 |
| `Grin2a` | 1 |
| `Grin2b` | 2 |
| `Grin1` | 89 |

The Parquet rows for these genes show that the count-1 adhesion and scaffold donors were mostly single self-transcript calls: `Nlgn3`, `Nrxn1`, `Cadm2`, `Cntnap1`, `Cntnap2`, `Adgrl1`, `Adgrl2`, `Adgrl3`, `Dlg4`, and `Grin2a` each had only the perturbed transcript pass FDR in the focal class. `Lrrtm1` had one non-self significant feature, `R3hdm2`; `Shank3` had two significant features, including itself; and `Grin1` was the clear receptor-complex exception with 89 DEGs.

## Synthesis

I expect `Nlgn1` to look closer to the neuroligin/LRRTM/neurexin/adhesion set than to `Grin1`: enough expression and surface-pool turnover to plausibly yield a detectable perturbation, but little reason to transfer the broad 89-gene NMDA core-subunit state. The point estimate is therefore one FDR-significant gene, most likely a self-transcript-scale call with no broad downstream footprint.

## Prediction

`Nlgn1`: `1`
