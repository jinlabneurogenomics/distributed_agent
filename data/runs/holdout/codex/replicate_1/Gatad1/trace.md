# Gatad1 forecast

## Endpoint

- Target: `Gatad1`
- Cell group: `151 TH Prkcd Grin2c Glut`
- Endpoint: measured genes in that group with BH-adjusted Wilcoxon `pvals_adj < 0.05`

The declared target manifest and the canonical biology bundle both identify the single held-out perturbation as `Gatad1`. The same-experiment corpus had no Gatad1 report, Finding, Claim, or explicit comparator path in this release, so no packaged same-experiment Gatad1 outcome was exposed.

## Target biology

The biology bundle places GATAD1 as a nuclear component of an H3K4me3-associated EMSY/KDM5A/SIN3B chromatin complex, not as a core catalytic ATPase or a histone mark itself. The focal-cell expression measurement is present but modest: `Gatad1` RNA is detected in 10,176 of 23,679 matched non-target nuclei in `151 TH Prkcd Grin2c Glut` (`42.9748%`; mean raw UMI `0.6073`; pseudobulk CPM `38.061`). That is enough for the perturbation to be biologically reachable in part of the assayed population, but it also leaves substantial dilution risk.

The functional-stock card is sparse and explicitly indeterminate. Editing should stop new intact GATAD1 supply, but there is no direct half-life, chromatin-residence, or complex-loss timing anchor showing how completely a pre-existing GATAD1-containing chromatin complex is lost by the P37-P44 harvest. Global embryonic lethality and broad adult brain RNA detection support biological plausibility, whereas the non-neural cardiomyocyte conditional result and lack of a postnatal neuronal loss model do not establish a large acute neuronal transcriptome.

## Training endpoint scale

The declared `151 TH Prkcd Grin2c Glut` training count table contains 1,674 observed perturbations, of which 1,205 have zero focal DEGs. The distribution is sharply zero-inflated: median `0`, 75th percentile `1`, 90th percentile `2`, 95th percentile `18`, 99th percentile `430`, mean `14.05`, max `2677`.

Gatad1 is a GO chromatin-remodeling/chromatin-organization member, but those curated priors did not yield a stable count scale. In the 62 available GO:0006338 chromatin-remodeling training targets, the median was `0`, the 75th percentile was `8`, and the high mean was driven by a tail of broad responders. Directly relevant measured chromatin factors were heterogeneous:

| comparator class | focal training counts |
|---|---:|
| Kdm5b | 0 |
| Mbd2 | 0 |
| Gatad2b | 1 |
| Kdm5c | 18 |
| Kmt2a | 24 |
| Chd4 | 100 |
| Sin3a | 1433 |

The low end is more relevant for Gatad1 than the high end. Kdm5b shows that a represented KDM5 paralog can be fully flat, Gatad2b and Mbd2 show that NuRD-adjacent bridge/reader perturbations can be buffered in the P16 neuronal assay, and Kdm5c provides the clearest sparse H3K4-demethylase-side responder at only 18 focal DEGs. Chd4 and especially Sin3a are broader complex-level perturbations, not scale-matched loss of a minor EMSY/KDM5A/SIN3B-associated component.

## Same-experiment profile checks

I compared `Gatad2b`, `Mbd2`, `Kdm5b`, `Kdm5c`, `Kmt2a`, `Chd4`, `Sin3a`, and `Zmynd8` on their focal `151 TH Prkcd Grin2c Glut` log-fold-change profiles. The node activities recapitulated the count table for the low-to-intermediate candidates:

| node | focal DEGs |
|---|---:|
| Gatad2b | 1 |
| Mbd2 | 0 |
| Kdm5b | 0 |
| Kdm5c | 18 |
| Kmt2a | 24 |

The pairwise result did not support pulling Gatad1 toward the `Sin3a` or `Chd4` tail. Kdm5c shared 14 positive significant genes with Zmynd8, but only 3 with Chd4 and 1 with Sin3a; Kmt2a shared no positive significant genes with Chd4 and only 2 with Sin3a. The flat or one-gene nodes necessarily had no positive significant overlap with Chd4, Sin3a, or Zmynd8. This makes the high-count anchors useful only as evidence that the assay can see large chromatin responses, not as quantitative analogs for Gatad1.

The corpus summaries agreed with that interpretation. Kdm5c was reported as a sparse, thalamic, mostly up-regulated responder that is not interchangeable with Kdm5b, Rest, or Kmt2a. Gatad2b was nearly flat and did not phenocopy Chd4 or Mbd2. Mbd2 had no focal response. Sin3a produced a broad 3,761-call multi-cell-group response with proteostasis, RNA-processing, lipid/metabolic, lysosomal, and ciliary arms, and the corpus explicitly separated it from simple REST/MeCP2/SIN3A equivalence. These are the same experiment's interpreted reports, not independent replication, but they clarify why broad chromatin membership should be down-weighted.

## Point forecast

I forecast a very small detectable focal response:

- upward from `0` because Gatad1 is expressed in the focal class, lacks an obvious close paralog, and is in a chromatin-regulatory assembly with H3K4/KDM5/SIN3 links;
- downward from the 18-100 DEG sparse/intermediate chromatin anchors because GATAD1's operative stock at harvest is unresolved, it is not a core ATPase or global scaffold, its exact complex was not represented among measured perturbations, and the most bridge-like measured targets were `0` or `1`.

Balancing those terms places the point just above the count-table null mode:

`predicted_n_degs = 2`
