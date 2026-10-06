# Dlx5 forecast for `151 TH Prkcd Grin2c Glut`

## Target and endpoint

The manifest target is `Dlx5`.  The requested endpoint is the 151-class `n_degs`, defined as the number of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`.

## Evidence used

### Exact target reach in the focal population

The declared Dlx5 biology bundle reports very low in-assay Dlx5 expression in non-targeting nuclei from `151 TH Prkcd Grin2c Glut`:

- `n_cells_expressing = 207` of `n_non_target_cells = 23679`
- `pct_cells_expressing = 0.8741923223109084`
- `mean_raw_umi = 0.010937961907175135`
- `pseudobulk_cpm = 0.6855208600861268`

This exact expression reach supersedes qualitative expression priors.  Dlx5 perturbation may be functionally realized in the rare cells that actually express the transcription factor, but the bulk of this aggregated thalamic glutamatergic class has no direct Dlx5 substrate to lose.

### Dlx5 biology

The biology-only Dlx5 characterization says DLX5 is a soluble nuclear homeobox transcription factor whose functional stock is likely substantially depleted by the 21-28 day post-edit harvest if new protein production is stopped.  That supports treating the CRISPR edit as plausible in Dlx5-positive cells.

The same bundle also makes two downward adjustments for this endpoint:

- adult neural Dlx5 expression is described as restricted to GABAergic interneuron classes rather than broad postnatal neurons;
- available neural phenotypes come from developmental or combined Dlx5/Dlx6 GABA-lineage manipulations, not from acute P16 Dlx5-only loss in thalamic glutamatergic neurons.

So the target is a plausible local transcription-factor perturbation in a tiny positive compartment, not a broadly expressed core regulator of this 151-class population.

### Declared 151-class training counts

The training count table for `151 TH Prkcd Grin2c Glut` contains 1,674 non-held-out perturbations.  Its empirical burden is highly zero-inflated:

- 1,205 / 1,674 training targets have `n_degs = 0`;
- the median is `0`;
- the 75th percentile is `1`;
- only 78 targets have more than 20 DEGs.

The extreme high-count tail in this class is led by broad essential regulators such as `Uba5 = 2677`, `Tpr = 1768`, `Sin3a = 1433`, `U2af2 = 828`, `Psmb4 = 742`, and `Hnrnpu = 733`.  Dlx5 has neither their broad 151-class expression nor their core RNA/proteostasis/chromatin role.

### Training perturbations selected as analogs and boundaries

I weighted the close developmental and GABA-identity comparators above generic transcription-factor counts because Dlx5's limiting feature is cell-state reach.  In the same declared 151-class count table:

| comparator | reason considered | `151 TH Prkcd Grin2c Glut` `n_degs` |
| --- | --- | ---: |
| `Dlx6` | paired DLX5/DLX6 homeobox paralog | 0 |
| `Dlx3` | Dlx-family homeobox perturbation | 0 |
| `Arx` | forebrain GABAergic developmental TF, partly related to DLX programs | 0 |
| `Gad2` | GABA synthesis marker, transmitter-axis mismatch in glutamatergic cells | 0 |
| `Slc32a1` | vesicular GABA transporter, transmitter-axis mismatch | 0 |
| `Msx2` | developmental homeobox TF with Dlx5 among expected embryonic outputs | 0 |
| `Pax6` | developmental neural TF with mostly off-window postnatal response | 0 |

I then checked the Parquet rows for these comparators in the exact 151-class context rather than relying only on count-table totals.  `Dlx6`, `Dlx3`, `Arx`, `Gad2`, `Slc32a1`, `Msx2`, `Pax6`, `Nkx2-1`, `Nkx6-2`, `Foxp2`, `Tcf4`, `Sox11`, `Ebf1`, `Ebf2`, and `Ebf3` each had 17,259 measured genes in `151 TH Prkcd Grin2c Glut` and zero genes even at the looser `pvals_adj < 0.10` cutoff.

### Same-experiment corpus context for the selected analogs

The July sourceguard corpus reinforced the same interpretation for training perturbations that are not held out:

- `Dlx6` had an all-null FDR surface across all 23 measured neuronal groups, and its forebrain GABAergic DLX/GAD/Vgat/Pvalb expected program was not transcriptionally engaged.
- `Dlx3` had no downstream gene at FDR < 0.10 in 22 recovered neuronal groups.
- `Pax6` was transcriptionally silent across 22 recovered NeuN+ neuronal groups after P16 loss.
- `Slc32a1` was downstream pan-null; in glutamatergic and dopaminergic groups that flat surface was interpreted as the expected transmitter mismatch.

These records are interpretations of the same PerturbAI experiment rather than independent replication, but they are useful checks that the zero counts for close training analogs are biologically coherent rather than isolated counting artifacts.

## Synthesis

Dlx5 loss should remove a real regulatory protein where Dlx5 is expressed, but the exact 151-class expression reach is under 1% of non-target nuclei.  The closest assayed DLX-family comparator, `Dlx6`, was completely silent even in recovered GABAergic groups and was also 0 in this thalamic glutamatergic endpoint.  Other off-window developmental transcription factors and direct GABA-axis perturbations were likewise flat in 151.  Against a training baseline where three quarters of targets produce at most one DEG and high responses are concentrated in broadly active regulators, the evidence points to no BH-significant genes in the aggregated 151-class contrast.

Predicted `n_degs`: `0`.
