# Apc DEG-count forecast

## Target and endpoint

- Target: `Apc`
- Cell group: `151 TH Prkcd Grin2c Glut`
- Endpoint: number of measured genes with Wilcoxon BH-adjusted `pvals_adj < 0.05`
- Point forecast: `6`

## Evidence used

### Declared Apc biology bundle

Source: `biology_bundles/Apc.json`

The canonical biology bundle supports effective target reach and functional
realization, but it does not make the perturbation an obligate large
transcriptional responder.

- `Apc` is well detected in the exact focal non-target population:
  22,354 / 23,679 nuclei expressing, 94.4% expressing, mean raw UMI 3.79,
  mean CP10k 2.36.
- The stock card calls full-length APC by harvest
  `likely_substantially_depleted`.
- APC loss in a postmitotic-neuron conditional model had molecular/synaptic
  consequences on an approximately one-month axis, close enough to the P16 to
  P37-P44 window to support observability.
- The same card keeps material caveats: APC works through several WNT,
  microtubule, adhesion, centrosomal, and synaptic scaffold pools; stable
  N-terminal fragments can be allele-dependent; Apc2 may provide
  context-dependent redundancy.

### Same-cell-group training scale

Source: `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`

`Apc` is not present in the 1,674-row training count table. The cell group is
mostly quiet for held targets:

- 1,205 / 1,674 training genes are zero at BH < 0.05.
- Median = 0; 75th percentile = 1; 90th percentile = 2; 95th percentile = 18.
- The arithmetic mean is 14.05 only because a small tail of chromatin,
  proteostasis, and RNA-processing perturbations has hundreds to thousands of
  DEGs.

Observed WNT/catenin and APC-neighbor counts at the requested BH < 0.05
threshold:

| target | n_degs | interpretation |
|---|---:|---|
| `Ctnnb1` | 383 | large beta-catenin loss state |
| `Tcf7l2` | 106 | broad thalamic TCF7L2 terminal-state program |
| `Gsk3b` | 6 | small destruction-complex kinase / WNT-adjacent response |
| `Lrp6` | 4 | sparse receptor-input response |
| `Lrp5` | 0 | receptor-family boundary |
| `Fzd2`, `Fzd4`, `Fzd6`, `Fzd9` | 0 each | single-Frizzled boundaries |
| `Ctnnd2` | 1 | self-only catenin boundary |
| `Map1b`, `Mapt`, `Kif5a`, `Kif5c`, `Dlg4` | 1 each | mostly self-only cytoskeletal/synaptic boundaries |
| `Shank2` | 0 | synaptic-scaffold boundary |
| `Shank3` | 2 | synaptic-scaffold boundary |
| `Macf1`, `Prickle1`, `Kremen1`, `Ror1`, `Ror2`, `Ryk`, `Gpc6`, `Antxr1`, `Antxr2` | 0 each | WNT-adjacent boundaries |

The exact Parquet rows confirmed that the small structural counts are often
the perturbed transcript itself. For example, `Ctnnd2`, `Dlg4`, `Kif5a`,
`Kif5c`, `Map1b`, and `Mapt` each had a single BH < 0.05 row, the self row.
`Gsk3b` had six BH < 0.05 rows, one of them `Gsk3b`; `Lrp6` had four
downstream BH < 0.05 rows.

### Same-experiment corpus context for the training comparators

Source: selected-release Finding/Claim contexts for observed training targets.
These reports summarize the same experiment as the Parquet, so I used them for
semantics, not as independent replication.

- `Ctnnb1` and `Tcf7l2` truly converge in this thalamic group, and their large
  counts are not generic WNT-neighborhood behavior.
- `Lrp6` was a sharply restricted and sparse WNT input: six genes at the
  corpus report's FDR < 0.10 surface, corresponding to four genes at the
  task's stricter BH < 0.05 threshold.
- The represented receptor and receptor-family perturbations
  `Lrp5`, `Fzd2`, `Fzd4`, `Fzd6`, `Fzd9`, `Ror1`, `Ror2`, and `Ryk` did not
  phenocopy `Lrp6`.
- `Gsk3b` loss was also 151-restricted but only small, and its report explicitly
  says canonical beta-catenin transcription was not broadly induced after
  isolated `Gsk3b` loss despite strong `Ctnnb1` and `Tcf7l2` detectability.

## Synthesis

I placed `Apc` above the genome-wide zero/singleton prior because the target is
strongly expressed in this focal population and full-length APC function should
be substantially reduced by harvest. The perturbation is also downstream of the
`Lrp6` ligand/receptor gate and should more directly release beta-catenin than
single Frizzled or `Lrp5` loss, so a pure zero call would underweight the
biology.

I did not transfer the 106 to 383 DEG scale from `Tcf7l2` or `Ctnnb1`.
`Tcf7l2` is the terminal thalamic transcription factor, `Ctnnb1` loss removes
both beta-catenin transcriptional activity and cadherin-linked beta-catenin
functions, while `Apc` loss is the opposite sign on beta-catenin stability and
has APC2, fragment, and pool-specific caveats. The exact training data show
that WNT-adjacent upstream or cytoskeletal perturbations usually remain at 0 to
6 DEGs in this endpoint.

The resulting forecast is a small nonzero response centered on the
`Lrp6`/`Gsk3b` scale, allowing one possible self-transcript call because `Apc`
is well expressed but not using self-knockdown as evidence for a larger
downstream response: `predicted_n_degs = 6`.
