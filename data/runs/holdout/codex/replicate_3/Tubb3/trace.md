# Direct forecast trace

## Target and endpoint

- Target: `Tubb3`
- Focal population: `151 TH Prkcd Grin2c Glut`
- Endpoint: number of measured genes with BH-adjusted Wilcoxon `p < 0.05`

## Evidence used

- Exact reach in the focal controls is high: `Tubb3` is detected in
  23,097 of 23,679 non-target nuclei in `151 TH Prkcd Grin2c Glut`
  (`97.54%`), with mean log1p CP10K `1.5771`, mean raw UMI `7.314`,
  and pseudobulk CPM `458.39`. This makes a self-transcript call possible,
  but target RNA abundance is not itself evidence of a large downstream
  response.

- The canonical biology bundle classifies TUBB3 as a beta-tubulin structural
  subunit whose edit stops new TUBB3 production but does not directly poison
  pre-existing heterodimers or lattice-incorporated tubulin. The operative pool
  is redundant: adult germline-null mouse neural tissue preserves total
  beta-tubulin by other isotypes and has no detected baseline neurobehavioral
  or neuropathological deficit, although sensory axon regeneration is slower.
  Total brain tubulin turns over on a days-to-weeks scale, so acute P16 editing
  should realize some loss by P37-P44, but the available timing evidence is not
  an exact thalamic-neuron match.

- The declared 151-class training count table is extremely sparse: among 1,674
  training perturbations, 1,205 have `0` DE genes, 276 have `1`, the median is
  `0`, and the 75th percentile is `1`. A forecast above one therefore needs
  target-specific evidence for a real downstream module.

- Same-context beta-tubulin perturbations are the closest training
  comparators. In the 151-class count table, `Tubb4b` has `n_degs = 1` and
  `Tubb5` has `n_degs = 1`. Directly in the training Parquet those are
  self-transcript rows only:
  `Tubb4b -> Tubb4b`, logFC `-0.5966`, adjusted `p = 1.07e-07`; and
  `Tubb5 -> Tubb5`, logFC `-1.4783`, adjusted `p = 7.71e-23`.

- The main positive tubulin exception is `Tuba1a`, not beta-tubulin loss:
  `Tuba1a` has `n_degs = 7` in this focal population, consisting of its self
  row plus up-regulated `Tubb3`, `Tubb2a`, `Tuba4a`, `Tubb4a`, `Tubb4b`, and
  `Tubb5`. Same-experiment packaged reports independently interpret this as a
  restricted `Tuba1a` alpha/beta-tubulin feedback program that is not
  phenocopied by `Tubb4b` or `Tubb5`.

- Other cytoskeletal comparators in the same count table were also weak in
  `151 TH Prkcd Grin2c Glut`: `Mapt`, `Map1b`, `Stmn2`, `Nefl`, `Nefm`,
  `Kif5a`, `Kif5c`, and `Mapre2` each had `1`; `Tuba4a` had `2`; `Map6` and
  `Kif2a` had `0`. The same-experiment report corpus summarizes `Tubb4b` as
  having zero non-self genes in all 22 measured groups at FDR < 0.10, and
  `Tubb5` as producing only fragmented single-gene effects rather than a
  coherent microtubule, p53, or stress module.

## Synthesis

The high focal expression of `Tubb3` makes a detectable self-row decrease more
plausible than a pure zero if the guides reduce nuclear target transcript.
However, the direct beta-tubulin comparators show self knockdown without a
downstream isotype-replacement program in the same screen, and the broader
postnatal microtubule/cytoskeleton cohort is mostly self-only or flat. The
held-out target differs from `Tubb4b` and `Tubb5` by neuronal specialization,
but the biology bundle's best evidence says the basal operative microtubule
stock is largely buffered over this window. I therefore predict a minimal
single-gene signature rather than a multi-gene `Tuba1a`-like program.

Predicted `n_degs`: `1`
