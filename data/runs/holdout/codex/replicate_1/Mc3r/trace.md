# Mc3r n_degs forecast

## Target and endpoint

- Target perturbation: `Mc3r`.
- Cell class: `151 TH Prkcd Grin2c Glut`.
- Endpoint: number of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`.
- Prediction: `0`.

## Evidence used

1. The declared target bundle says `Mc3r` is a melanocortin-activated, Gs-coupled seven-pass membrane receptor. Its edited receptor stock should plausibly decline during the P16 to P37-P44 window because new MC3R supply stops and activated receptor can internalize toward lysosomes, but no direct postmitotic mouse-thalamus MC3R half-life or P16 edit-to-harvest timing measurement was available.

2. Exact focal-population reach is weak. In matched non-target nuclei from `151 TH Prkcd Grin2c Glut`, `Mc3r` had 376 total UMIs across 23,679 nuclei, 289 expressing nuclei, `pct_cells_expressing = 1.22049`, `mean_raw_umi = 0.015879`, and `mean_log1p_cp10k = 0.007341`. That supports possible target engagement in a small subset but argues against a large class-aggregate survivor RNA footprint.

3. The training count table for this same cell class is highly zero-inflated: 1,205 of 1,674 training perturbations had `n_degs = 0`; the median was 0, the 75th percentile was 1, the 90th percentile was 2, and only the far tail reached large counts.

4. The closest represented melanocortin-system perturbations in the training table were flat in this exact endpoint: `Agrp = 0`, `Mc1r = 0`, `Mc2r = 0`, and `Atrn = 1`. The same-experiment corpus Claim `claim:a37db0dd68ddbbfdd6ab` summarized those represented `Agrp`, `Atrn`, `Mc1r`, and `Mc2r` perturbations as providing no evidence for a captured basal neuronal melanocortin transcriptional module, while explicitly noting that central `Mc3r`, `Mc4r`, and `Pomc` perturbations were not represented there.

5. Broader receptor and GPCR/cAMP comparators also supported a near-zero prior in this group. `Adcy3`, `Drd4`, `Drd5`, `Gnal`, `Gnas`, `Glp1r`, `Npsr1`, `Pde1c`, and `Pth1r` all had zero DEGs, as did assayed serotonin and nonapeptide receptors checked from the count table. A direct profile comparison over 15 melanocortin/GPCR/cAMP training perturbations found 12 nodes with no significant features and only three with 1-9 significant features, without a shared FDR-supported program that would justify transferring a hidden multi-gene receptor signature to `Mc3r`.

## Synthesis

I treated MC3R loss as biologically realizable over the assay window, not as a failed perturbation. The limiting factors were instead endpoint reach and assay mode: the receptor is very sparsely detected in this thalamic aggregate, its strongest training-neighbor receptor systems are silent or singleton-scale at the same FDR threshold, and the broad postnatal basal snRNA-seq readout does not preserve a common neuromodulatory GPCR/cAMP transcriptional module. Against a training distribution whose median and mode are both zero, those bearings put `Mc3r` at the zero/singleton boundary; the exact melanocortin and receptor comparators favor the lower side of that boundary.

The integer point forecast is therefore:

```tsv
target_name	predicted_n_degs
Mc3r	0
```
