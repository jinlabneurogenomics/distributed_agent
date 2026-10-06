# Gatad1 direct DEG-count forecast

## Target and endpoint

- Target: `Gatad1`.
- Cell group: `151 TH Prkcd Grin2c Glut`.
- Endpoint: count of measured genes with BH-adjusted Wilcoxon `p < 0.05` in this one cell group.
- The declared training count table has 1,674 measured training perturbations and excludes `Gatad1`; 1,205/1,674 have `n_degs = 0`, the median is 0, the mean is 14.05, the 90th percentile is 2, and the maximum is 2,677. Thus this population is highly zero-inflated even though a few perturbations are very broad.

## Gatad1 biology-only evidence

- The declared Gatad1 biology bundle reports exact focal-population expression: the Gatad1 feature is available in `151 TH Prkcd Grin2c Glut`, with mean CP10K 0.379 and detection in 10,176/23,679 non-target nuclei, or 42.97%.
- The same bundle places GATAD1 as a nuclear H3K4me3-linked EMSY/KDM5A/SIN3B chromatin-complex component.
- Functional-stock support is sparse: the card found no direct GATAD1 half-life, chromatin residence, or complex-loss time-course measurement. A P16 edit should stop new intact GATAD1 supply, but the amount of pre-existing GATAD1-containing complex left by the P37-P44 harvest is indeterminate.
- The card found broad brain-region RNA expression but no postnatal neuronal perturbation phenotype; global mouse loss was embryonic-lethal, while the available conditional adult-loss study was non-neural.
- The selected July corpus has no Gatad1 same-experiment Finding, Claim, or explicit target context, so no packaged Gatad1 outcome was used.

## Training perturbations used

The most relevant measured anchors split into a large-response chromatin envelope and a quieter same-axis/same-neighborhood set:

| training perturbation | 151 `n_degs` | interpretation |
| --- | ---: | --- |
| `Sin3a` | 1433 | SIN3 scaffold; a strong upper-boundary chromatin-corepressor response, but much broader than a single EMSY/KDM5A-associated component |
| `Phf12` | 403 | SIN3A-associated PHF/Pf1 adaptor; broad caudal response, and the corpus reports that it is not phenocopied by Sin3a |
| `Chd4` | 100 | NuRD ATPase; response concentrated in the same thalamic class but the corpus reports that measured MBD/GATAD2B NuRD cofactors did not phenocopy it |
| `Kdm5c` | 18 | closest represented KDM5/H3K4 eraser-side response; narrow and target-specific |
| `Gatad2b` | 1 | represented GATA-domain/NuRD bridge subunit; nearly flat in 151 |
| `Mbd2`, `Kdm5b`, `Kmt2c`, `Smarca4`, `Smarcc1` | 0 | chromatin or H3K4/NuRD/BAF-adjacent boundaries that were flat in this same cell group |

Other H3K4 or chromatin regulators showed that the assay can report some nuclear regulators when they are active (`Setd1a = 368`, `Kmt2a = 24`), but they are writer-side or otherwise less direct than the low/null KDM5 and NuRD-adjacent comparators.

## Profile comparison

I compared the 151 log-fold-change profiles for a small Gatad1-relevant panel: `Sin3a`, `Phf12`, `Chd4`, `Kdm5c`, `Gatad2b`, `Kdm5b`, `Mbd2`, `Kmt2a`, `Setd1a`, `Smarca2`, `Smarca4`, `Smarcc1`, and `Kmt2c`.

The panel itself was heterogeneous: 5/13 nodes had no significant 151 features, 2/13 had one to nine, 2/13 had 10 to 49, and 4/13 had at least 50. Significant-gene overlap was sparse even between the broad responders and the closer low/null nodes. For example, `Sin3a` versus `Kdm5c` shared only one positive significant feature and no negative significant features; `Phf12` versus `Kdm5c` likewise shared one positive and no negative significant feature; `Sin3a` versus `Phf12` still had only 23 same-positive and 29 same-negative significant intersections plus 30 direction conflicts despite both being very broad. This supported treating `Sin3a`, `Phf12`, and `Chd4` as an upper envelope, not as direct quantitative donors.

## Synthesis

Gatad1 has enough focal expression for the perturbation to be observable in principle, and it lacks a known close paralog that would make a strong redundancy prior. Those features keep the forecast above a hard zero. However, its operative biology is a chromatin-complex component with unknown turnover, not an enzyme or obligate ATPase; no postnatal neural Gatad1-loss prior was available; and the most direct same-assay neighborhoods argue for target-specific or buffered responses. `Gatad2b` and `Mbd2` show that NuRD bridge/recruiter perturbations can be almost silent while `Chd4` is active, and `Kdm5b` shows that an H3K4/KDM5-family perturbation can be completely flat while `Kdm5c`, `Setd1a`, and `Sin3a` are detectable.

The large `Sin3a` and `Phf12` counts therefore define a plausible but unlikely broad-stress tail rather than the center for Gatad1. The center is closer to the `Mbd2`/`Kdm5b`/`Gatad2b`/`Kdm5c` band: mostly zero or one gene, with a small chance of a narrow thalamic derepression response. I chose `1` as the point forecast to represent an essentially buffered response with at most an isolated FDR call.
