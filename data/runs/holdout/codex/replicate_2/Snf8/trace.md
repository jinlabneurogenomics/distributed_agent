# Snf8 direct DEG-count prediction

## Target and endpoint

- Target: `Snf8`
- Cell group: `151 TH Prkcd Grin2c Glut`
- Endpoint: number of measured genes with BH-adjusted Wilcoxon `p < 0.05`

## Evidence used

- The declared biology bundle identified Snf8 as a core ESCRT-II subunit for endosomal cargo sequestration and multivesicular-body vesicle formation. It judged the operative entity to be a dynamic complex component whose functional stock is likely substantially depleted over the P16-to-P37/P44 perturbation window, but with only partial evidence because neither SNF8 protein half-life nor ESCRT-II exchange was measured in postmitotic neurons.

- The exact focal-population expression reach in the declared bundle supports target accessibility in this class: `Snf8` was detected in 16,160 of 23,679 non-target nuclei, or 68.246%, with mean log1p CP10K 0.505 and pseudobulk CPM 80.195. I used this as evidence that lack of target expression should not be the main reason for a null.

- The 151 training count table is zero-heavy and long-tailed: among 1,674 training perturbations, 1,205 have `n_degs = 0`, the median is 0, the 75th percentile is 1, the 95th percentile is 18, the 99th percentile is 430, and the maximum is 2,677. Thus a 15 to 30 gene response is already high relative to most perturbations in this exact endpoint even though it is far below the `Rab7`/proteostasis tail.

- I queried the declared Parquet only for the same 151 class and training perturbations. Candidate counts at adjusted `p < 0.05` were:

  | training target | 151 `n_degs` |
  | --- | ---: |
  | `Rab7` | 501 |
  | `Tsc2` | 86 |
  | `Dctn1` | 75 |
  | `Vps54` | 31 |
  | `Vps35` | 17 |
  | `Depdc5` | 13 |
  | `Rb1cc1` | 4 |
  | `Cltc` | 3 |
  | `Mtor` | 2 |
  | `Sqstm1` | 1 |
  | `Chmp4b` | 0 |
  | `Vps41` | 0 |
  | `Vps53` | 0 |
  | `Atg5` | 0 |
  | `Atg16l1` | 0 |
  | `Becn1` | 0 |
  | `Lamp2` | 0 |

- The same-experiment corpus, treated as interpretation of the same Perturb-seq experiment rather than replication, put these counts in context:
  - `Rab7` anchors a large late-endosomal/lysosomal compensation state with V-ATPase, lysosomal hydrolase, sterol, proteasome, ISR/UPR, and synaptic-downshift arms.
  - `Vps35` and `Vps54` are much narrower 151-biased trafficking states: `Vps35` had a selective 151 response, while `Vps54` had a one-class 151 response that lacked the broad lysosomal, UPR/ISR, proteasome, and sphingolipid program expected from a severe GARP collapse.
  - `Chmp4b` produced only one corrected downstream change outside 151 and did not form a recurrent ESCRT/autophagy/cargo signature.
  - `Litaf` was flat across recovered postmitotic neuronal classes; its report notes that the most direct ESCRT partners were unavailable, but active `Rab7`, `Dctn1`, `Vps35`, and `Vps54` showed the assay could detect endolysosomal stress when it crossed a transcriptional threshold.
  - Core autophagy targets were not strong 151 donors: `Atg5`, `Atg16l1`, and `Becn1` all had zero significant genes in 151, matching the corpus conclusion that represented autophagy perturbations do not collapse into one acute neuronal RNA program.

- I also compared the signed 151 Wilcoxon-score profiles for an 18-node endolysosomal/trafficking cohort. The profile cohort had low shared structure overall, with median positive and negative top-tail overlap coefficients of 0.0575 and 0.0700 across candidate pairs. `Rab7` was directionally close to `Vps41` over the continuous vector even though `Vps41` had no 151 FDR-significant genes, and `Rab7` had only modest whole-profile Pearson correlations to `Vps54` and `Vps35` of 0.187 and 0.143. I therefore used `Rab7` as an upper detectability/stress-state anchor, not as a scale donor for Snf8.

## Synthesis

The upward evidence is that Snf8 is expressed in the focal class, has no established close paralog in the biology bundle, and should progressively lose new ESCRT-II supply over the 21 to 28 day window. That makes a nonzero 151 response more plausible than it would be for the many pathway genes with poor reach, durable pre-existing function, or obvious buffering.

The downward evidence is that acute juvenile snRNA readout is often buffered for lysosome, autophagy, ESCRT-adjacent, and trafficking perturbations. The exact ESCRT-II partners `Vps25` and `Vps36` and ESCRT-I/0 comparators such as `Tsg101`, `Hgs`, and `Stam` were not in the training count table, and the closest represented ESCRT-family perturbation, `Chmp4b`, had zero 151 genes. `Vps41` and `Vps53` also had zero 151 genes despite being in adjacent late-endosomal or retrograde trafficking complexes.

I therefore placed Snf8 below the broad `Rab7` state and closer to the focal thalamic trafficking responders `Vps35` and `Vps54`, with a small upward adjustment from `Vps35` because the Snf8 bundle supports expression and low paralogous replacement. The resulting point prediction is:

```text
Snf8 n_degs = 20
```
