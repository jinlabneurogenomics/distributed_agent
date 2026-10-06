# Direct forecast trace

## Target and endpoint

- Target: `Ophn1`.
- Cell class: `151 TH Prkcd Grin2c Glut`.
- Endpoint: number of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05` in the declared focal-class contrast table.
- Inputs used: the one-row `Ophn1` holdout manifest, the declared `Ophn1` biology bundle, the focal-class training count CSV, and focal-class rows from the declared training DE Parquet.
- Outcome exclusion: the `Ophn1` perturbation contrast and `Ophn1` target DEG count were not present in the declared training count CSV or Parquet rows used here. The selected same-experiment corpus release had no `Ophn1` target report, Finding, Claim, or explicit reference.

## Biology used

The exact expression card shows that `Ophn1` is observed in this class: `11,715 / 23,679` non-target 151-class nuclei expressed it, with `49.474%` expressing nuclei, mean raw UMI `0.7447`, mean log1p CP10K `0.3174`, and pseudobulk CPM `46.67`. That makes the target transcript reachable enough that a self-transcript DEG is plausible, although self-knockdown was not treated as an editing-strength estimate.

The functional-stock card favored real target engagement by harvest. OPHN1 is a dynamically used Rho-family GAP and synaptic scaffolding/trafficking protein, and the bundle judged the functional stock as `likely_substantially_depleted` over the 21-28 day P16 to P37-P44 interval because neuronal RNAi depleted OPHN1 protein and produced spine/synaptic effects within 2-8 days. The bundle also marked the evidence as only partial: the timing evidence is rat/hippocampal and the mouse phenotypes are hippocampal, germline, or conditional rather than an acute thalamic P16 edit.

## Training-count scale

The 151-class count table contains 1,674 training perturbations.

- 1,205 / 1,674 have `n_degs = 0`.
- 469 / 1,674 have at least one DEG.
- Quantiles of `n_degs`: median `0`, 75th percentile `1`, 90th percentile `2`, 95th percentile `18`, 99th percentile `430`.

Thus the empirical prior for an arbitrary observed training perturbation in this exact class is a zero or a one-gene footprint, with a small high-count tail.

## Mechanistic comparators

I used OPHN1's source-card mechanism, not outcome labels, to choose available Rho-family, actin/spine, and excitatory-synapse perturbations from the training count table. Their 151-class DEG burdens were low:

| training target | `n_degs` | DEGs in the filtered Parquet when present |
|---|---:|---|
| `Rac1` | 0 | none |
| `Cdc42` | 1 | `Cdc42` only |
| `Pak1` | 1 | `Pak1` only |
| `Pak3` | 0 | none |
| `Kalrn` | 0 | none |
| `Dock3` | 0 | none |
| `Arhgef9` | 1 | `Arhgef9` only |
| `Limk1` | 0 | none |
| `Cyfip1` | 0 | none |
| `Cyfip2` | 1 | `Cyfip2` only |
| `Dlg4` | 1 | `Dlg4` only |
| `Shank3` | 2 | `Shank3`, `Uba5` |
| `Syngap1` | 0 | none |
| `Grin2a` | 1 | `Grin2a` only |
| `Grin2b` | 2 | `Grin2b`, `Pianp` |
| `Camk2a` | 0 | none |
| `Camk2b` | 1 | `Camk2b` only |

The close pathway genes available in training therefore argue strongly against placing `Ophn1` in the medium or high transcriptional-response tail. Most nonzero analog counts were just the perturbed gene itself, with little evidence for a broad downstream nuclear RNA program in recovered 151-class neurons.

## Point synthesis

Two forces set the point forecast:

- Upward from zero: `Ophn1` is expressed in nearly half of focal non-target nuclei, the operative OPHN1 stock is predicted to clear within the experimental window, and mouse/rat neural evidence supports a postmitotic synaptic phenotype.
- Downward toward the quiet majority: the evidence is transferred from hippocampus rather than exact thalamus, OPHN1 is a localized RhoGAP/synaptic regulator rather than a core transcriptional or proteostasis factor, and observed Rho/synaptic training perturbations in this same focal class are almost all `0`, `1`, or `2` DEGs.

I therefore choose the low nonzero point: one significant measured gene.
