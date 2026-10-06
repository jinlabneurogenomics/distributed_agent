# Ffar1 direct DEG-count forecast

## Target and endpoint

- Held-out perturbation: `Ffar1`.
- Focal population: `151 TH Prkcd Grin2c Glut`.
- Endpoint: `n_degs`, the number of measured genes in this focal class with BH-adjusted Wilcoxon `p < 0.05`.
- Point forecast: `0`.

## Evidence used

The run-local task binding identifies `Ffar1` as the single manifest target and maps the requested cell context exactly to `151 TH Prkcd Grin2c Glut`.

The prediction-safe biology bundle for `Ffar1` reports exact focal-population reach from the assay: in the matched non-target nuclei for `151 TH Prkcd Grin2c Glut`, `Ffar1` was a measured feature but had `0` total target UMI, `0` pseudobulk CPM, `0` mean CP10K, and `0 / 23679` non-target cells expressing. That strongly argues against a cell-autonomous transcriptional response from losing FFAR1 in recovered thalamic neurons.

The same bundle supports the edit-realization side only conditionally: FFAR1 is a dynamic cell-surface fatty-acid GPCR whose newly synthesized receptor pool should substantially decline during the P16-to-P37/P44 interval if edited cells expressed it. The positive mouse neural evidence is hypothalamic, including POMC-neuron function, rather than thalamic, and no matched thalamic compensation or latency evidence was available.

The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` table is sparse in this exact class:

```text
training targets: 1674
0-DEG targets:    1205
1-DEG targets:     276
median n_degs:       0
75th percentile:     1
90th percentile:     2
95th percentile:    18
max:              2677
```

The handpicked receptor/GPCR-like training comparators in the expression parquet were all transcriptionally quiet in this class. `Adgra1`, `Adgrb1`, `Adgrb3`, `Adgrg1`, `Adgrg2`, `Adgrg6`, `Adgrv1`, `Gpr156`, `Gpr161`, `Gpr179`, and `Gpr45` each had `0` FDR-significant genes. `Adgrl1`, `Adgrl2`, `Adgrl3`, `Gabbr1`, `Gabbr2`, `Gpr158`, `Gprasp2`, `Grm1`, `Grm7`, `Paqr7`, `Paqr8`, and `Pgrmc1` each had exactly `1`, and in each of those cases the only significant gene was the perturbed receptor or receptor-associated transcript itself. `Cnr1` also had `1`, but its single significant transcript was `Srcap`.

## Synthesis

The decisive feature is the exact zero expression of `Ffar1` in the focal non-target nuclei. In the sparse thalamic training distribution, even expressed neuronal GPCR or surface-receptor perturbations usually have either no downstream DEG or only a self-transcript DEG; a target with no detectable transcript in the focal cells should lose even that self-hit route. I therefore put `Ffar1` at the modal and mechanistically preferred outcome, `0`, with only residual uncertainty from guide/off-target effects, very rare unsampled expressing thalamic cells, or survivor-conditioned indirect effects.
