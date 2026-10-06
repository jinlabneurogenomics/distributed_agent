# Direct forecast for Tubb2a in 151 TH Prkcd Grin2c Glut

## Endpoint

The requested endpoint is the focal-population `n_degs`: measured genes with
BH-adjusted Wilcoxon `pvals_adj < 0.05` in `151 TH Prkcd Grin2c Glut`.
The target perturbation is `Tubb2a`.

## Evidence used

- **Declared target biology bundle.** `Tubb2a` is detectably expressed in the
  exact focal non-target population: mean CP10K `3.6003`, mean raw UMI
  `5.9313`, and `22,847 / 23,679` non-target nuclei expressing it
  (`96.49%`). Editing from P16 to P37-P44 is expected to stop new TUBB2A
  supply while pre-existing soluble and lattice pools persist initially but
  should substantially decline by harvest. The card also flags unresolved
  redundancy from the nearly identical `Tubb2b` paralog and notes that the
  closest mouse loss evidence is mild, developmental, and cortical rather than
  a matched postnatal thalamic loss phenotype.
- **Declared training count table.** The focal training table has `1,674`
  targets. It is zero-heavy: `1,205` targets have `n_degs = 0`, the median is
  `0`, the 75th percentile is `1`, the 90th percentile is `2`, and the 95th
  percentile is `18`.
- **Typed analog nomination from the explicit training universe.** The
  highest-priority training-available tubulin subunit comparators were
  `Tuba1a`, `Tuba4a`, and `Tubb4b`; `Tubb5` was recovered as a beta-tubulin
  by broader microtubule annotations. The closest paralog `Tubb2b`, and
  `Tubb2a` itself, were not in the focal training table.
- **Focal Parquet rows for those training analogs.** In
  `151 TH Prkcd Grin2c Glut`, the exact significant rows were:
  `Tubb4b = 1`, the self transcript only; `Tubb5 = 1`, the self transcript
  only; `Tuba4a = 2`, self plus `Mast1`; and `Tuba1a = 7`, self plus an
  alpha/beta tubulin compensation set. Matched perturbed nuclei for these
  four analogs were modest but usable: `121-199` against `23,679` controls.
- **Same-experiment corpus for the training analogs.** The packaged
  interpretation separates the `Tuba1a` compensation state from beta-tubulin
  perturbations: `Tubb4b` did not induce the alpha/beta tubulin replacement
  program, and `Tubb5` was interpreted as postnatally buffered with only
  fragmented one-gene effects across recovered neuronal groups. I used these
  corpus Findings only to interpret the measured training signatures; they are
  alternate representations of the same experiment, not independent
  replication.

## Synthesis

`Tubb2a` has strong focal expression and enough post-edit time for functional
TUBB2A stock to fall, so a completely invisible perturbation is less favored
than a detectable one-row footprint. The broad biology, however, points toward
buffering: `TUBB2A` is a beta-tubulin isotype, has a nearly identical `Tubb2b`
paralog, and the closest available beta-tubulin perturbations were
`Tubb4b` and `Tubb5`, both self-transcript-only at the requested FDR threshold
in this thalamic group.

I therefore treated the seven-gene `Tuba1a` focal response as an upper
contextual bound for a special alpha-tubulin feedback trigger, not as the
expected magnitude for `Tubb2a`. `Tuba4a` supplied an intermediate sparse
alpha-tubulin point at `2`, while the two beta-tubulin points at `1` were the
closest direct quantitative anchors. The final point forecast is one
FDR-significant gene, representing likely visibility of the target transcript
with little or no additional downstream beta-tubulin response in recovered
`151 TH Prkcd Grin2c Glut` nuclei.

Predicted `n_degs`: **1**
