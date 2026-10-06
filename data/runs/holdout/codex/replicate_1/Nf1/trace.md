# Nf1 DEG-count forecast

## Endpoint and target

- Target: `Nf1`
- Cell group: `151 TH Prkcd Grin2c Glut`
- Endpoint: number of measured genes with BH-adjusted Wilcoxon `p < 0.05`

The held-out `Nf1` differential-expression signature and its `n_degs` value were not used. I used the declared one-row manifest, the canonical Nf1 biology bundle, the `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` training count table, the training-only DE Parquet, and same-experiment corpus summaries for measured training genes only.

## Determining evidence

### Nf1 is reachable but not guaranteed to be large

The canonical bundle places Nf1 in reach for this assay: in non-target `151 TH Prkcd Grin2c Glut` nuclei, Nf1 is detected in 20,079 of 23,679 nuclei, or 84.8%, with mean raw UMI 2.22 and pseudobulk 139 CPM. The same bundle adjudicates edited neurofibromin stock as `likely_substantially_depleted` by P37-P44 because neurofibromin is a soluble Ras-GAP homodimer with a multi-day rather than multi-week turnover estimate, so a P16 disruptive edit should have time to reduce new functional protein supply before the 21-28 day harvest.

That pushes away from treating Nf1 as an unexpressed or unrealized perturbation. It does not, by itself, imply a broad nuclear-RNA response: the bundle's best postnatal timing anchor is adult oligodendrocyte loss rather than juvenile thalamic neurons, same-context Ras-GAP compensation is unresolved, and the readout is a basal, survivor-conditioned single-nucleus transcriptome.

### The 151 training endpoint is sparse

In the 1,674-gene 151 training count table, 1,205 targets had `n_degs = 0`, the median was 0, the 90th percentile was 2, the 95th percentile was 18, and only 43 targets reached at least 100 DEGs. This thalamic class can yield very large responses, but most single-gene perturbations still remain at 0-2 corrected genes.

### Ras/MAPK comparators argue for a tiny response

The closest measured Ras/MAPK loss-of-function training targets in the same 151 population were flat or nearly flat at FDR 0.05:

| Training target | 151 `n_degs` |
| --- | ---: |
| `Spred1` | 0 |
| `Spred2` | 0 |
| `Ptpn11` | 0 |
| `Rasa2` | 0 |
| `Sos1` | 0 |
| `Kras` | 0 |
| `Hras` | 0 |
| `Raf1` | 0 |
| `Mapk1` | 0 |
| `Map2k2` | 0 |
| `Lztr1` | 1 |
| `Shoc2` | 1 |
| `Ntrk2` | 3 |
| `Braf` | 4 |
| `Map2k1` | 4 |

The training reports agreed with the direct Parquet counts. `Spred1` was a pan-measured-neuronal basal-transcriptome null, `Spred2` was a pan-neuronal basal-transcriptome null despite ERK/TrkB sentinel testing, and `Ptpn11` was flat across all recovered neuronal groups at FDR < 0.10. `Braf` and `Map2k1` showed that RAF/MEK-pathway transcription is detectable in this assay, but only as a very small 151 branch centered on Vgf/Ptpn5/Unc13a rather than as a large MAPK activation program.

### Larger mTORC1 responses are real but less proximal

`Tsc2` had a larger 151 response, with 86 genes at FDR 0.05, and the same-experiment interpretation recovered sterol, lysosomal, and stress outputs consistent with mTORC1 activation. I treated that as an upper contextual anchor rather than the main Nf1 analogue: TSC2 is a direct brake on Rheb/mTORC1, while NF1 primarily restrains Ras-GTP; most represented upstream PI3K/mTOR components in the 151 table were flat or very small (`Akt3`, `Pik3cb`, `Pik3r1`, `Pik3r2`, `Igf1r`, `Irs1`, and `Rptor` were 0; `Mtor` was 2; `Depdc5` was 13).

## Synthesis

I put the prediction just above the modal zero. Nf1 is expressed and should be functionally depleted, so a complete miss is not the only plausible outcome; however, loss of SPRED-family Ras/MAPK inhibitors and SHP2/RAF/ERK pathway genes was mostly invisible to basal snRNA-seq, and the few positive RAF/MEK relatives produced 1-4 DEGs rather than tens. The final point is therefore a single significant gene, representing a trace or self-limited thalamic response rather than a Tsc2-like metabolic/stress program.

Predicted `n_degs`: **1**
