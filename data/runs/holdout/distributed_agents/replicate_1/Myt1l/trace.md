# Reasoning trace

## Question and endpoint

The task asks for one scalar holdout prediction: the number of genes expected to pass
Benjamini-Hochberg adjusted Wilcoxon `pvals_adj < 0.05` after acute CRISPR
loss-of-function of `Myt1l` in the focal `151 TH Prkcd Grin2c Glut` neuronal group.
The held-out `Myt1l` rows are absent from both the supplied per-gene
differential-expression parquet and the focal-cell training DEG-count table, so the
answer must be inferred from non-held-out perturbations plus target biology.

I treated the focal training `n_degs` CSV as the direct endpoint for observed
perturbations. The all-cell differential-expression parquet is a direct
measurement of individual expression changes for the non-held-out targets and was
used only for those targets. Packaged Findings and direct-evidence slices from the
internal July 2026 PerturbAI same-experiment corpus were used to interpret
same-experiment analogs; they are annotations of the same screen, not independent
replication. External literature was used for MYT1L mechanism because `Myt1l` was
not visible as either a report target or a comparator in the internal corpus graph.

## Quantitative checks over the supplied data

I first loaded
`151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`. It contains 1,674
non-held-out targets. The focal endpoint is heavily zero-inflated and long-tailed:
the median is 0 DEGs, 469/1,674 targets are nonzero, 193 have at least 2 DEGs, 106
have at least 10, 80 have at least 20, 59 have at least 50, and only three exceed
1,000. Thus famous or neurodevelopmental genes cannot simply be assigned a large
count.

I then used DuckDB filters on the declared parquet restricted to
`group_name = '151 TH Prkcd Grin2c Glut'` to inspect candidate analogs. The
observed focal DEG counts were:

| training perturbation | focal `n_degs` | relationship to `Myt1l` |
|---|---:|---|
| `Sin3a` | 1433 | broad chromatin corepressor; `Myt1l` recruits SIN3B/HDACs, but `Sin3a` perturbation disrupts many MYT1L-independent complexes |
| `Chd4` | 100 | NuRD ATPase chromatin remodeler; another large postmitotic chromatin response, not a MYT1L complex member |
| `Chd8` | 61 | ASD chromatin regulator with a focal subcortical-biased expression response |
| `Chd2` | 34 | chromatin remodeler with a moderate 151-cell response |
| `Arid1a` | 22 | cBAF selector with a compact synaptic/signaling signature in 151 cells |
| `Mecp2` | 16 | sequence-specific methyl-CpG regulator; biologically important in neurons but modest in this exact assay |
| `Arid1b` | 1 | close ARID1A paralog that did not phenocopy `Arid1a` |
| `Bcl11a`, `Bcl11b`, `Foxp2`, `Neurod2`, `Sox11`, `Tbr1`, `Tcf4` | 0 each | neuronal developmental/transcription-factor counterexamples |

The analog expression programs were not interchangeable. In the focal cell group,
the `Sin3a` 1433-gene response and `Chd8` 61-gene response shared only 21 FDR genes
in either direction and 12 with the same sign; `Sin3a` and `Chd4` shared 36 genes,
15 same-sign; `Chd4` and `Arid1a` shared just one significant gene and none in the
same direction. Within the internal corpus, `Chd4` reports likewise noted that
NuRD-related `Gatad2b` and `Mbd2` did not phenocopy `Chd4`, and `Arid1a` reports
noted that the close cBAF paralog `Arid1b` had only one downstream DEG. I therefore
used these large chromatin perturbations as upper-bound evidence rather than as
direct count donors.

As a small regulatory check, `Myt1l` itself is an assayed transcript in all 1,674
focal training contrasts and was significantly changed in eight of them; the
strongest were `Yy1`, `Zbtb7a`, `U2af2`, `Sin3a`, `Psmb4`, `Snrnp70`, `Rab7`, and
`Phf12`. This shows that MYT1L transcript abundance is part of the measured 151-cell
state in the training data, but these upstream-looking hits are mainly very broad
RNA-processing, proteostasis, and chromatin perturbations. I did not use them to
infer the missing `Myt1l` endpoint directly.

## Target-specific biological transfer

### Myt1l

The strongest external prior is that MYT1L is a pan-neuronal CCHHC zinc-finger
factor that helps maintain neuronal identity. Mall et al. 2017 showed in mouse
fibroblast-to-neuron reprogramming, developing brain, and primary postmitotic
neurons that MYT1L directly represses many non-neuronal programs except the
neuronal program; the repressive function required an N-terminal domain that
recruits a SIN3B-containing complex, and MYT1L loss derepressed somatic-lineage and
Notch-pathway genes including `Hes1` (Nature 2017, DOI 10.1038/nature21722,
PMID 28379941). Romm et al. 2005 previously found that MYT1/MYT1L family proteins
interact with SIN3B and recruit HDAC1/HDAC2, supporting a direct corepressor
mechanism (Journal of Neurochemistry 2005, DOI 10.1111/j.1471-4159.2005.03131.x,
PMID 15935060). Chen et al. 2023 mapped MYT1L binding in developing cortex and adult
prefrontal cortex and found that MYT1L loss activates earlier neuronal-development
programs, increases active histone marks at promoters and enhancers, and that MYT1L
interacts with HDAC2 and SIN3B in vivo (Genome Research 2023, DOI
10.1101/gr.277413.122, PMID 37100461). Germline heterozygous mouse work also shows
that partial MYT1L deficiency is phenotypically relevant, with postnatal age-
dependent transcriptomic, synaptic, and behavioral changes (Kim et al. 2022, DOI
10.1016/j.celrep.2022.111398, PMID 36130507) and obesity/behavioral phenotypes
that model MYT1L syndrome (Woehr et al. 2022, DOI 10.1186/s13229-022-00497-3,
PMID 35538503).

I model the expected experimental chain as:

`Myt1l` CRISPR disruption -> reduced MYT1L DNA-binding repression at selected open
chromatin sites -> derepression of earlier developmental and non-neuronal identity
genes through loss of SIN3B/HDAC-mediated repression -> altered expression in
recovered postnatal thalamic glutamatergic neurons.

This is a same-direction prior for a nonzero transcriptional response, because
MYT1L has a direct repressive role in postmitotic neurons rather than only an
embryonic progenitor role. It is not a same-scale prior for `Sin3a`: MYT1L recruits
SIN3B/HDACs to a restricted set of DNA sites, while `Sin3a` loss in the screen gave
a massive, partly proteostasis/RNA-processing signature and down-regulated `Myt1l`
itself. Disrupting the DNA-binding factor should hit a narrower subset of targets
than removing a broad chromatin scaffold. It is also not well modeled by layer-
identity TFs such as `Tbr1`, `Bcl11b`, or `Tcf4`, which were flat here despite being
important during cortical development; unlike those, MYT1L continues to act as a
general neuronal-identity repressor.

The closest observed response-breadth anchors are therefore the modest chromatin
and methyl-DNA factors, especially `Mecp2` at 16 DEGs, `Arid1a` at 22, and `Chd2`
at 34, with the many zero-count neuronal TFs pulling the estimate down and
`Sin3a`/`Chd4` treated as mechanistically too broad. I predict that acute partial
`Myt1l` loss will cross FDR for a small but real number of genes in these 151 TH
Prkcd Grin2c Glut nuclei, below the low tens-to-100 chromatin remodeler responses.

Final point prediction: **12 DEGs**.

## Limits

The predicted endpoint for `Myt1l` is not directly present in the declared inputs,
and the internal PerturbAI July 2026 report corpus contained no `Myt1l` target
report or Myt1l-comparator record to anchor it in the same experiment. No measured
`Myt1`, `St18`/`Myt3`, `Sin3b`, `Hdac1`, or `Hdac2` perturbation was available in
the 151-cell training count table, so the causal transfer has to bridge from
`Sin3a` and general chromatin regulators. The MYT1L literature includes shRNA,
germline heterozygous, and cortical or in vitro neuronal systems; those establish
the repressive mechanism but differ from sparse AAV CRISPR at P16 with a recovered
single-nucleus readout at P37-P44. The sign and exact breadth of a thalamic
postmitotic MYT1L response could therefore be smaller than the external studies
would suggest, including zero if this neuronal subtype is buffered or if affected
nuclei are under-sampled.
