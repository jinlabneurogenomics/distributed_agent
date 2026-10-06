# Snap25 direct DEG-count forecast

## Target and endpoint

- Target from the declared one-row holdout manifest: `Snap25`.
- Focal population: `151 TH Prkcd Grin2c Glut`.
- Endpoint: `n_degs`, the count of measured genes with BH-adjusted Wilcoxon `p < 0.05` in that focal population.
- The target was absent from the declared 1,674-row training count table, and its held-out expression profile was not queried.

## Biology of the held-out perturbation

The declared `Snap25` biology bundle supports real target engagement by harvest:

- `Snap25` is almost ubiquitous in the focal non-target cells:
  `23673 / 23679` expressing cells, `99.9747%`, with mean log1p CP10K
  `3.0643` in `151 TH Prkcd Grin2c Glut`.
- The operative product is SNAP-25 protein in a dynamic presynaptic SNARE pool.
  The card adjudicates pre-edit functional stock as likely substantially
  depleted over the 21-28 day P16-to-P37/P44 perturbation interval.
- Prior mouse evidence supports a postnatal neuronal requirement, but in a
  different projection-neuron context. Thus functional loss is plausible, while
  the exact short-window thalamic single-nucleus transcriptional consequence is
  not directly established by the card.

This moves the forecast away from a pure failed-engagement zero, but it does
not by itself imply a broad nuclear DEG program.

## Training perturbations used

I used deterministic, endpoint-blind annotation sets containing `Snap25` and
intersected them with the declared training count table.

Closest core-SNARE complex targets available in training:

| target | n_degs |
| --- | ---: |
| Cplx1 | 1 |
| Cplx2 | 0 |
| Stx1b | 0 |
| Syn2 | 0 |
| Vamp1 | 1 |

`log1p` mean for this core set: `0.320` DEGs; maximum: `1`.

Synaptic-vesicle exocytosis/priming targets available in training:

| target | n_degs |
| --- | ---: |
| Cadps2 | 0 |
| Cplx1 | 1 |
| Cplx2 | 0 |
| Snca | 0 |
| Stx1b | 0 |
| Stxbp1 | 1 |
| Sv2a | 1 |
| Synj1 | 1 |
| Unc13a | 0 |
| Unc13b | 0 |
| Vamp1 | 1 |

`log1p` mean for this exocytosis/priming set: `0.370` DEGs; maximum: `1`.

Broader neurotransmitter-release and synaptic-vesicle-cycle annotations stayed
low as well. The Reactome neurotransmitter-release intersection had median
`0`, maximum `9`, with `Hspa8` as the 9-DEG broad chaperone outlier; the KEGG
synaptic-vesicle-cycle intersection had median `0`, maximum `3`.

## Focal expression-profile check

I compared the `151 TH Prkcd Grin2c Glut` differential-expression profiles for
31 available neurotransmitter-release / vesicle-cycle training perturbations
from the expression parquet.

- All 31 supplied profiles were present.
- `17 / 31` had no significant genes in this focal population.
- The remaining `14 / 31` all had only `1_to_9_significant_features`.
- In the five closest focal release factors that were inspected in detail,
  `Cplx2` and `Stx1b` had zero significant genes, while `Cplx1`, `Stxbp1`, and
  `Vamp1` each had one significant gene.

The significant rows in the parquet showed that the one-gene signals for the
nearest direct release factors were target-transcript rows:

| target | significant row |
| --- | --- |
| Cplx1 | Cplx1 |
| Stxbp1 | Stxbp1 |
| Vamp1 | Vamp1 |
| Sv2a | Sv2a |
| Synj1 | Synj1 |

So the same-class profile evidence did not reveal a recurrent downstream
program shared by presynaptic-fusion perturbations; their detected burden was
mostly zero or a single self-transcript row.

## Synthesis

The key upward bearings are that `Snap25` is expressed in essentially all focal
cells and the expected functional stock should be depleted within the
experimental window. The key downward bearing is stronger for the requested
endpoint: disrupting nearby SNARE-complex and vesicle-fusion factors in the
same class almost never yielded more than one FDR-significant measured gene.

Because `n_degs` includes the target transcript itself, high and broad Snap25
expression makes a single detected row more plausible than an exact zero.
Because the closest operation-matched perturbations lack a broader survivor
nuclear response, I do not project a multi-gene program.

Predicted `n_degs`: **1**.
