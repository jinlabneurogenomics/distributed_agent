# Direct `n_degs` forecast for Arl6ip1

## Declared target and endpoint

- Target: `Arl6ip1`, from the one-row holdout manifest.
- Cell class: `151 TH Prkcd Grin2c Glut`.
- Endpoint: count of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`.
- Held-out hygiene: `Arl6ip1` is absent from the declared 1,674-row training count table, and I did not use any Arl6ip1 expression signature or outcome rows.

## Biology bundle

- Exact focal-population reach is real but not saturated: `Arl6ip1` was detected in 15,296 of 23,679 non-target nuclei in `151 TH Prkcd Grin2c Glut`, `pct_cells_expressing = 64.5973`, `mean_raw_umi = 1.1955`, and `mean_cp10k = 0.7345`.
- The source card describes ARL6IP1 as an integral ER membrane-shaping component that promotes FAM134/RETREG-dependent ER remodeling and ER-phagy.
- Constitutive mouse loss causes progressive neural and neuromuscular degeneration, supporting neuronal relevance, but the evidence is germline/long-horizon and not an acute P16-to-P37/P44 thalamic loss test.
- Functional stock by harvest is indeterminate: an edit should stop new synthesis, but ARL6IP1 already embedded in ER membranes and the coupled ER architecture are not expected to disappear instantly, and no postmitotic-neuron ARL6IP1 half-life or ER-structure exchange clock was available.

## Training measurements used

The focal count table was extremely sparse:

- 1,205 / 1,674 training targets had `n_degs = 0`.
- The median was 0 and the 90th percentile was only 2.
- 276 targets had exactly one DEG.

I used the declared Parquet only for training perturbations. Among all 1,674 training targets in the focal class, 237 of the 276 singleton responses were self-transcript-only. Thus a one-gene count often marks only target-mRNA reduction rather than a broad downstream state.

The closest measured ER-phagy comparator was `Retreg1`, the mouse FAM134B homolog and a named ARL6IP1 partner in the biology bundle.

- `Retreg1` had `n_degs = 1` in `151 TH Prkcd Grin2c Glut`.
- The sole significant focal row was `Retreg1` itself (`logfoldchanges = -0.7764`, `pvals_adj = 5.13e-7`, `n_pert_matched = 188`, `n_ctrl_matched = 23679`).
- Across all assayed classes, the `Retreg1` FDR<0.05 surface contained only three self-transcript rows and one downstream singleton (`Srsf7` in `191 MB P MY GABA`).

The same-experiment Retreg1 Findings independently summarized that Retreg1 loss produced an almost empty central-neuron transcriptomic surface, lacked a canonical ER-stress/UPR/autophagy/lysosomal compensation program, and that measured ER-phagy, macroautophagy, and HSAN2-pathway relatives failed to phenocopy the Retreg1 singleton downstream hits. In the focal count table those represented relatives were also quiet to very small: `Atg5 = 0`, `Atl3 = 0`, `Wnk1 = 0`, `Kif1a = 1`, `Sqstm1 = 1`, `Mtor = 2`, and `Rb1cc1 = 4`.

## Synthesis

The Arl6ip1 bundle supports that the perturbation can matter biologically, but not that the acute mosaic postnatal thalamic assay should mount a broad recovered-cell RNA response. The closest measured FAM134/ER-phagy surface, Retreg1, was self-only in the focal class, and the broader ER-phagy/autophagy relatives sat in the 0-4 DEG range. That makes a high count implausible.

I placed Arl6ip1 just above zero rather than at zero because its exact focal expression reach is sufficient for a target-transcript row to be testable and an ARL6IP1 lesion is at least as proximal to the heteromeric ER-shaping cluster as Retreg1. The unresolved functional-stock timing and the absence of a Retreg1 downstream response keep the forecast at a singleton.

Predicted `n_degs`: 1.
