# Direct forecast for Zfhx4

## Target and endpoint

- Target: `Zfhx4`
- Cell group: `151 TH Prkcd Grin2c Glut`
- Endpoint: number of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`
- Forecast: `1`

The declared biology bundle for `Zfhx4` was served as the biology-only view:
`target_outcome_exposed=false` and `labeled_neighbors_exposed=false`. The same
release corpus had no `Zfhx4` Claims, Findings, or explicit comparator
references, so no same-experiment target result was available.

## Biology that affected the forecast

`Zfhx4` is detectably expressed in the exact focal population: in matched
non-target nuclei from `151 TH Prkcd Grin2c Glut`, 13,397 of 23,679 nuclei
expressed it, with mean raw UMI 1.115 and pseudobulk 69.9 CPM. That makes a
postnatal thalamic perturbation technically reachable by the assay.

The perturbation also plausibly depletes the operative molecule by harvest:
ZFHX4 is a nuclear DNA-binding transcription factor, not a permanently installed
extracellular or structural stock, and the P16 edit leaves 21-28 days before
P37-P44 harvest. The functional-stock card therefore called stock at harvest
`likely_substantially_depleted`, but only with partial evidence because no
ZFHX4-specific turnover measurement or postnatal thalamic loss clock was found.

The prior phenotype evidence did not justify a large thalamic transcriptional
signature on its own. The direct neural loss evidence is germline embryonic
brainstem development and neonatal breathing, the skeletal evidence is
non-neural, and the `Zfhx3` paralog note has no compensation test in thalamic
neurons.

## Matched training evidence

The `151 TH Prkcd Grin2c Glut` training count table contains 1,674 perturbations
and is strongly concentrated at zero:

- 1,205 of 1,674 have 0 DEGs.
- The median is 0.
- The 75th percentile is 1.
- The 90th percentile is 2.
- Only 106 perturbations have at least 10 DEGs.
- Only 43 perturbations have at least 100 DEGs.

The closest direct biological checks were flat in the same count table:

- `Zfhx2`, the only screened `Zfhx` family member in this training endpoint:
  0 DEGs.
- `Phox2b`, the brainstem developmental target in the Zfhx4-null mouse story:
  0 DEGs.
- `Runx2` and `Sp7`, the non-neural skeletal ZFHX4 partner axis: 0 DEGs each.

Several broad transcriptional or chromatin regulators do produce large thalamic
signatures, including `Zbtb7a` with 841 DEGs, `Yy1` with 720, `Cic` with 576,
`Thap11` with 478, `Phf12` with 403, and `Wac` with 384. I did not transfer
that hundreds-of-DEGs scale to `Zfhx4`, because these are broad active-regulator
contrasts rather than a demonstrated ZFHX4 module or a thalamic ZFH-family
analogue.

## Parquet profile check

Direct Parquet inspection in the focal group confirmed that the 0-count
biological anchors were measured profiles rather than absent rows: `Zfhx2`,
`Phox2b`, `Runx2`, and `Sp7` each had 17,259 measured-gene rows and 0
significant features at `pvals_adj < 0.05`.

A rank-profile comparison over the selected anchors likewise separated the
flat direct anchors from the active broad-regulator branch:

- `Zfhx2`, `Phox2b`, `Runx2`, and `Sp7` were all in the
  `no_significant_features` activity state.
- `Zbtb7a`, `Yy1`, `Cic`, `Thap11`, `Phf12`, `Wac`, `Tcf7l2`, `Nrf1`, and
  `Nr1d1` were all in the `at_least_50_significant_features` activity state.
- The closest eligible whole-profile neighbors around `Zfhx2` were mostly
  zero or near-zero count perturbations: `Nr1h4` 0, `Cd46` 0, `Fgfr3` 0,
  `Arih1` 7, `Baz1b` 1, and `Tshz2` 0.

## Synthesis

The endpoint prior alone favors 0-1 DEGs. `Zfhx4` expression in more than half
of focal nuclei and likely protein-stock depletion move the point forecast above
a hard zero, but the available task-matched training analogues closest to the
published ZFHX4 story are all exactly flat, and the high-count training examples
are generic broad regulators with no established ZFHX4-specific bridge.

I therefore placed `Zfhx4` at the tiny-response edge of the training
distribution and rounded to 1 DEG.
