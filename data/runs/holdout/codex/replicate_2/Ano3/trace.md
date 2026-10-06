# Ano3 direct forecast

## Target and endpoint

- Target: `Ano3`
- Cell class: `151 TH Prkcd Grin2c Glut`
- Endpoint: number of measured genes with BH-adjusted Wilcoxon `p < 0.05`

## Evidence used

The declared biology bundle reports exact in-assay reach for `Ano3` in the focal
population: `Ano3` was detected in 2,987 of 23,679 matched non-target nuclei
from `151 TH Prkcd Grin2c Glut` (`12.61%`), with mean raw UMI `0.185` and mean
CP10K `0.108`. Thus the perturbation is not expression-absent, but any direct
cell-intrinsic Ano3-loss program is expected to be diluted across the aggregated
thalamic class.

The functional-stock card makes the P16-to-P37/P44 realization uncertain rather
than clearly strong: the edit should stop new intact ANO3 supply, but
pre-existing membrane-associated ANO3 protein, lipid state, and the
KCNT1/Slack-regulatory pool have no target-specific clearance or residence
clock. The main neural loss evidence is a rat DRG germline knockout phenotype,
not an acute mouse thalamic perturbation, so it supports possible neuronal
relevance but not a large 21-28 day thalamic transcriptomic footprint.

The training count table for this exact class is sparse. Among 1,674 available
training perturbations, 1,205 have `n_degs = 0`, 1,481 have `n_degs <= 1`, the
median is `0`, the 75th percentile is `1`, and the 90th percentile is `2`.
Large responses exist but are concentrated in a small tail headed by broad
process genes such as `Uba5`, `Tpr`, and `Sin3a`, a different regime from a
lowly expressed membrane scramblase/channel regulator.

I used the Ano3 biology card to prioritize two observed comparator lanes:

- `Kcnt1`, the Slack channel linked to TMEM16C/ANO3 in rat sensory neurons, is
  present in the training table and has `n_degs = 0` in the focal class. Direct
  Parquet aggregation in `151 TH Prkcd Grin2c Glut` found 17,259 measured genes
  for the `Kcnt1` perturbation and no genes with `pvals_adj < 0.05`.
- Typed gene-analog nomination found no exact Anoctamin paralog, no reciprocal
  corpus comparator, no narrow module, and no direct-interaction candidate in
  the training universe. The usable nominees were all broad functional
  fallbacks. The leading phospholipid-translocation / ion-channel fallbacks
  were mostly quiet in the count table: `Tmem63b = 1`, `Atp11c = 0`,
  `Atp8a2 = 0`, `Atp9a = 1`, `Ngfr = 0`, `Abca1 = 0`, `Abca7 = 0`,
  `Add2 = 0`, `Atp2b3 = 1`, and `Trpm7 = 0`.

## Synthesis

The focal expression measurement keeps `Ano3` eligible for an effect, but its
expression is restricted and low. The best target-specific biology points to
membrane-associated, possibly long-lived or incompletely renewed operations,
with no evidence that acute postnatal editing eliminates the operative pool by
harvest. The most direct observed partner, `Kcnt1`, is null in this cell class,
and the broader lipid/channel comparators fall on the zero/one-DEG boundary.

Those observations favor the modal low-count outcome rather than the long
right-tail response. I expect, at most, a tiny threshold crossing program; the
most likely integer count is therefore:

`0`
