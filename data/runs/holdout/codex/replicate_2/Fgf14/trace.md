# Forecast trace

## Target and endpoint

- Target: `Fgf14`
- Cell class: `151 TH Prkcd Grin2c Glut`
- Endpoint: number of measured genes with BH-adjusted Wilcoxon `p < 0.05`
- Prediction: `1`

## Declared target biology

The declared holdout manifest contains only `Fgf14`. The same-experiment corpus has no `Fgf14` report or Claim in this held-out run, so no packaged same-experiment `Fgf14` signature or outcome was used.

The canonical biology bundle supports target reach but not a large-response prior:

- Exact focal expression is available: `Fgf14` is detected in 18,223 of 23,679 focal non-target cells, or 76.96%, with mean log1p CP10k 0.642 and mean raw UMI 1.755.
- FGF14 is an intracellular FHF regulator of voltage-gated sodium-channel complexes, including axon-initial-segment channel assemblies.
- Editing at P16 should stop new intact FGF14 supply; because this is a dynamic intracellular component and the P37-P44 harvest occurs 21-28 days later, functional stock is likely substantially depleted by harvest.
- Evidence is still partial for this exact endpoint: no target-specific neuronal half-life was available, and germline Fgf14 phenotypes were not acute thalamic postnatal loss tests.

## Training measurements used

The focal training table contains 1,674 measured training perturbations and excludes `Fgf14`.

Its count distribution is sparse and heavy-tailed:

| subset | value |
| --- | ---: |
| zeros | 1,205 / 1,674 |
| median `n_degs` | 0 |
| 75th percentile | 1 |
| 90th percentile | 2 |
| mean | 14.1 |
| maximum | 2,677 |

I used the declared focal count table and a direct slice of the training parquet for observed intracellular FHF and ion-channel comparators in the exact `151 TH Prkcd Grin2c Glut` group:

| comparator class | focal `n_degs` |
| --- | --- |
| FHF / FGF-related | `Fgf12 = 0`, `Fgf13 = 2`, `Fgf1 = 0`, `Fgfr1 = 0`, `Fgfr2 = 0`, `Fgfr3 = 0`, `Fgfrl1 = 0` |
| sodium-channel apparatus | `Scn1a = 1`, `Scn1b = 2`, `Scn2a = 1`, `Scn3a = 0`, `Scn8a = 1` |
| selected calcium / potassium channels | `Cacna1a = 0`, `Cacna1d = 0`, `Kcna1 = 0`, `Kcna2 = 0`, `Kcnq2 = 1`, `Kcnq3 = 1` |

Matched perturbed-cell counts for the focal parquet rows of these functional comparators ranged from 90 to 283 against 23,679 matched controls, so the low counts are not just single-nucleus dropouts. In the focal parquet slice, most significant rows for sodium-channel and potassium-channel perturbations were the edited target transcript itself. `Fgf13` had two focal significant genes, `Fgf13` and one downstream marker, `Rell2`; `Scn1b` had `Scn1b` and one downstream marker, `Jun`; the other sodium-channel targets had one self row or no significant gene.

## Packaged same-experiment context for comparators

The training reports support the same interpretation as the raw counts:

- `Fgf13`, the closest represented intracellular FHF, was described as mostly transcriptomically buffered, with a single thalamic downstream marker and no robust convergence with represented FHF, NaV, or receptor-FGF perturbations.
- `Fgf12` was almost completely buffered in the atlas, with its lone reported downstream singleton occurring outside the requested `151 TH Prkcd Grin2c Glut` group.
- `Scn1a`, `Scn1b`, `Scn2a`, `Scn3a`, and `Scn8a` reports all separated channel physiology from a broad stable nuclear RNA response; their perturbations did not induce a recurrent immediate-early, channel-compensation, or generic stress transcriptome.
- `Cacna1a`, `Cacna1d`, and `Kcnq2` reports similarly cautioned that loss of an electrophysiologically important channel can be nearly flat in basal survivor-conditioned snRNA-seq.

## Synthesis

The upward evidence is real focal expression and a functional-stock call that FGF14 should be substantially affected by the edit-to-harvest interval. Adult neural phenotypes in single-null Fgf14 mice also argue against total paralog redundancy.

The downward evidence is stronger for the requested numeric endpoint. The closest measured P16-edited postmitotic comparators, especially `Fgf12`, `Fgf13`, and NaV-channel genes, cluster between zero and two DEGs in the same high-yield thalamic class, usually with no more than a self-transcript hit. Their same-experiment reports explicitly reject a large shared FHF/Nav mRNA module. FGF14 is therefore biologically reachable, but the expected survivor-conditioned nuclear response is a singleton-scale effect rather than a broad transcriptional state.

I forecast `Fgf14` at the center of the direct FHF/Nav comparator range: one FDR-significant measured gene.
