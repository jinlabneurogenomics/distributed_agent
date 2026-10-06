# Adora2a n_degs forecast

Target and endpoint: `Adora2a` in `151 TH Prkcd Grin2c Glut`; `n_degs` counts
measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05` in this one focal
class.

## Evidence used

- The declared manifest contains the single held-out target `Adora2a`.
- The declared biology bundle gives exact non-target expression in the focal
  class: 434 of 23,679 nuclei expressed `Adora2a` RNA, or 1.8328%; mean raw
  expression was 0.0315 UMI per nucleus, mean CP10K was 0.0160, mean
  `log1p(CP10K)` was 0.00988, and pseudobulk expression was 1.97 CPM. This
  establishes that the receptor was detectable but nearly absent across the
  recovered thalamic glutamatergic population.
- The functional-stock card supports substantial loss of A2A receptor after a
  successful edit over the P16 to P37-P44 window, because A2A is a renewed
  plasma-membrane GPCR and conditional neuronal deletion can nearly abolish
  receptor binding in targeted adult regions. That argues against an installed
  protein-stock null, but it only applies to cells with receptor stock to lose.
- The same card reports forebrain and striatal postnatal phenotypes rather than
  matched thalamic phenotypes, and it records unresolved adenosine-receptor
  compensation. I therefore treated biology as "active where expressed, weakly
  projected to this class" rather than as a guaranteed 151-class response.

## Training measurements

The requested 151-class training count table has 1,674 held-in targets. It is
heavily zero-inflated in this endpoint: 1,205 targets have `n_degs = 0`, 1,481
have `n_degs <= 1`, the median is 0, and the top tail is driven by a small
number of housekeeping/chromatin/RNA-processing perturbations.

I used the mouse annotation store to nominate training-available analogs for
`Adora2a`, then interpreted the nominated perturbations in the 151-class count
table and Parquet. The exact/narrow/direct Adora2a nominees available in the
training table were:

| nominee | strongest relationship tier | 151-class n_degs |
|---|---:|---:|
| P2ry12 | narrow purinergic/nucleotide GPCR module | 0 |
| Drd2 | human-ortholog-projected ADORA2A receptor complex | 0 |
| Adra2a | narrow GPCR module | 0 |
| Lpar6 | narrow nucleotide/GPCR module | 0 |
| Gnas | direct STRING physical interaction plus GPCR signaling | 0 |
| Grm5 | human-ortholog-projected ADORA2A-GRM5 complex | 0 |
| P2ry14 | narrow purinergic/nucleotide GPCR module | 0 |
| Cnr1 | human-ortholog-projected ADORA2A-CNR1 complexes | 1 |
| Htr1a | human-ortholog-projected ADORA2A-HTR1A complex | 0 |
| Gata6 | narrow module nominee | 0 |
| Dmbt1 | narrow module nominee | 0 |

The declared Parquet confirmed that these 11 perturbations all had profiles in
`151 TH Prkcd Grin2c Glut`, each with 17,259 measured rows and matched control
size 23,679. Ten had no significant genes; `Cnr1` had only one, `Srcap`
with log-fold change 0.2998. The 11-node profile cohort had no shared
significant-program overlap, so there was no coherent hidden nonzero module to
transfer upward.

As a broader receptor baseline, every one of the 95 training genes annotated to
GO:0004930, "G protein-coupled receptor activity", had `n_degs <= 1` in this
class; 85 of 95 had exactly 0. Adenylyl-cyclase-activating GPCR signaling was
similar: 31 of the 35 annotated training genes had 0 and all had at most 1.
Direct mouse adenosine-family donors `Adora1`, `Adora2b`, and `Adora3` were not
present in the training table, so this could not be calibrated from a
same-family measured knockout.

## Synthesis

The upward evidence is that edited `Adora2a` should eventually lose functional
A2A receptor in cells that normally maintain it. The downward evidence is
stronger for this endpoint: only 1.83% of focal non-target nuclei detect the
target, external mouse phenotypes are from other neural contexts, receptor and
GPCR training perturbations in this thalamic class are almost uniformly exact
nulls, and the closest receptor-complex/nucleotide-GPCR nominees are 0 except
for a single-gene `Cnr1` response.

I therefore predict the Wilcoxon BH-significant count will round to the null
case rather than to a small positive count.

Predicted `n_degs`: 0
