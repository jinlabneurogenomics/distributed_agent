# Rhobtb2 focal-class n_degs forecast

## Requested target

- Manifest target: `Rhobtb2`
- Focal population: `151 TH Prkcd Grin2c Glut`
- Endpoint: `n_degs`, the count of measured genes in that perturbation and focal population with BH-adjusted Wilcoxon `p < 0.05`

## Declared evidence used

- The declared one-row holdout manifest names only `Rhobtb2`.
- The outcome-blind Rhobtb2 biology bundle reports exact focal-population reach but no target outcome. In the focal non-target baseline, `Rhobtb2` was measured in 16,698 of 23,679 nuclei, `pct_cells_expressing = 70.518%`, `mean_raw_umi = 1.377`, and `mean_cp10k = 0.876`, so the target is detectably expressed in the assayed thalamic population.
- The same bundle adjudicates RhoBTB2 as a dynamic CUL3 substrate adaptor whose operative protein stock should likely be substantially depleted 21-28 days after P16 editing. That supports functional realization by harvest, but the evidence is partial: the direct RhoBTB2 degradation and substrate work is in human cell systems, the mouse neurological phenotype evidence is constitutive/developmental, and no timed postnatal thalamic-neuron loss phenotype was available.
- The selected July same-experiment corpus had no `Rhobtb2` target record, so there were no Rhobtb2 Findings or Claims to use as packaged same-experiment interpretation.

## Training scale

From the declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` count table:

- 1,674 training perturbations were available.
- 1,205 of 1,674 had `n_degs = 0`.
- The median was 0, the 75th percentile was 1, the 90th percentile was 2, and the 95th percentile was 18.
- This focal endpoint is therefore extremely zero-inflated: a weak but reachable perturbation is much more likely to land at 0 or 1 than at a broad hundreds-gene response.

## Comparator measurements that set the scale

I nominated training-available annotation analogs for unavailable `Rhobtb2`. The typed nominee set contained no exact same-complex/paralog perturbation in training; the highest-specificity available set was four Reactome RHOBTB/RHOBTB2 GTPase-cycle co-members:

| comparator | typed relation used for inspection | focal `n_degs` |
| --- | --- | ---: |
| `Hsp90ab1` | RHOBTB/RHOBTB2 Reactome co-member | 1 |
| `Myo6` | RHOBTB/RHOBTB2 Reactome co-member | 0 |
| `Ddx39b` | RHOBTB/RHOBTB2 Reactome co-member | 0 |
| `Hnrnpc` | RHOBTB/RHOBTB2 Reactome co-member | 122 |

The Hnrnpc count was not scale-bearing for Rhobtb2. The Hnrnpc report in the same-experiment corpus describes a target-specific RNA-processing/splicing compensation state, including RNA-processing, proteostasis, mitochondrial, synaptic, and structural genes. That is a poor match to a CUL3 RhoBTB2 substrate adaptor.

I therefore put more weight on low-count CUL3/adaptor-like perturbations and the non-Hnrnpc RHOBTB co-members:

| comparator | rationale | focal `n_degs` |
| --- | --- | ---: |
| `Hsp90ab1` | RHOBTB Reactome co-member, but chaperone biology; focal significant row was only `Hsp90ab1` itself | 1 |
| `Myo6` | RHOBTB Reactome co-member; same-experiment report calls it transcriptionally null across neuronal groups | 0 |
| `Ddx39b` | RHOBTB Reactome co-member; no focal significant rows | 0 |
| `Lztr1` | CUL3-RING ubiquitin ligase adaptor annotation; focal significant row was only `Lztr1` itself | 1 |
| `Fbxo11` | substrate-adaptor annotation | 1 |
| `Fbxw7` | substrate-adaptor annotation | 1 |
| `Klhl20` | CUL3-RING ubiquitin ligase/adaptor annotation | 0 |
| `Kbtbd7` | CUL3-RING ubiquitin ligase/adaptor annotation | 0 |
| `Klhl7` | CUL3-RING ubiquitin ligase/adaptor annotation | 0 |

Across the 30 highest-priority typed nominees, 19 had no focal significant genes, 26 had at most one, and 27 had at most two; the median was 0. A symmetric profile comparison over those 30 nominees in `151 TH Prkcd Grin2c Glut` likewise found 19 no-response profiles, 9 profiles with 1-9 significant features, one 10-49 profile, and only Hnrnpc above 50.

## Synthesis

RhoBTB2 should be functionally reachable by the P37-P44 harvest because it is a renewed CUL3-associated adaptor rather than a pre-installed durable product, and its RNA is present in the exact assayed focal population. That argues against treating Rhobtb2 as an expression-absent or unrealized perturbation.

The available task-matched comparators argue against a broad focal transcriptome: CUL3/Kelch/adaptor-like perturbations were mostly 0-1, the closest RHOBTB Reactome neighbors were 0, 0, and a self-only 1 after excluding the Hnrnpc RNA-processing outlier, and whole-profile inspection did not reveal a recurrent large analogue program. Because singleton rows in this endpoint can be the perturbed gene itself and because the exact Rhobtb2 expression reach is high, I placed the point one notch above a pure null but still within the focal-class singleton regime.

Predicted `n_degs`: 1
