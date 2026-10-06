# Direct n_degs forecast for Max in 151 TH Prkcd Grin2c Glut

## Target and endpoint

- Target: `Max`.
- Endpoint: measured genes in `151 TH Prkcd Grin2c Glut` with Wilcoxon BH-adjusted `pvals_adj < 0.05`.
- The prediction used the declared one-row holdout manifest, the target `Max` biology bundle, the `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` training count table, and targeted reads of `training_de_all_cell_groups.parquet`. The held-out `Max` signature and DEG count were not available in those inputs.

## Target prior

The canonical `Max` bundle supports target reach but not a broad mature-neuron effect. In non-target nuclei from the focal class, `Max` was detected in 11,468 of 23,679 nuclei, with mean CP10K 0.452 and pseudobulk CPM 45.75, so the transcript is present in enough of the assayed class that a CRISPR effect was biologically reachable.

Functionally, MAX is a small bHLHZip component of MYC-family, MNT/MXD-family, and MGA repressive transcription-factor complexes. The bundle adjudicates MAX as a renewable dynamic-complex component whose functional stock is likely substantially depleted by the P37-P44 harvest after P16 editing, because new dimerization-competent MAX supply should stop and hourly-scale pre-edit MAX protein should turn over across the 21-28 day window. That is only a partial, biology-level prior: the matched postnatal thalamic-neuron deletion phenotype was not found, MYC/MAX partner usage is state dependent, and MLX-like compensation is unresolved rather than ruled out.

## Same-class training counts

The 1,674 visible training counts in this exact class were strongly zero-inflated:

- 1,205 / 1,674 targets had `n_degs = 0`.
- median `n_degs = 0`; 75th percentile = 1; 90th percentile = 2; 95th percentile = 18.
- The mean was 14.05 only because of a small high-response tail, topped by `Uba5 = 2677`, `Tpr = 1768`, and `Sin3a = 1433`.

The direct MAX-network and adjacent transcriptional comparators present in the count table were quiet in the focal class:

| target | n_degs |
|---|---:|
| `Myc` | 0 |
| `Mycn` | 0 |
| `Mnt` | 0 |
| `Mlxip` | 0 |
| `E2f1` | 0 |
| `Tfap4` | 0 |
| `Trp53` | 0 |
| `Srebf1` | 0 |
| `Mga` | 2 |
| `Tfdp1` | 2 |
| `Srebf2` | 7 |

The same Parquet rows showed adequate local sample sizes for these null or tiny calls: for example `Myc`, `Mycn`, `Mnt`, `Mlxip`, `E2f1`, `Tfdp1`, and `Tfap4` each had 182-320 perturbed nuclei against the same 23,679 matched controls. The exact FDR rows also kept `Mga` tiny: only `Obscn` and `Stag3` were below 0.05 in this class, with `Tasor` just above at adjusted p = 0.052.

Large transcriptional responses were detectable in the same class when the perturbed biology drove them. `Sin3a` had 1,433 FDR 0.05 genes, `Gfpt1` had 311, `Tsc2` had 86, and `Setdb1` had 22. I therefore did not treat the MAX-neighborhood zeros as a global failure of the `151 TH Prkcd Grin2c Glut` endpoint.

## Same-experiment corpus/profile evidence

The packaged corpus had no `Max` report, Finding, Claim, or explicit reference in this release, so there was no same-experiment semantic record for the withheld target. Reports for measured neighbors supported a narrow transfer:

- `Myc` was reported as a pan-neuronal transcriptomic null across recovered groups, with the expected MYC growth/ribosome/cell-cycle program absent.
- `Mnt` loss failed to derepress a detectable MYC-like growth, ribosome, cell-cycle, or apoptosis program.
- `Mlxip` was transcriptomically silent across recovered juvenile neuronal groups.
- `Mycn` and `Mga` produced only sparse, cell-restricted signatures, and the release summarized represented MYC/MAX-network and adjacent E2F/Mondo/metabolic perturbations as not forming a shared postmitotic neuronal transcriptomic module.
- `Sin3a` was a strong chromatin/proteostasis responder but was a boundary rather than a magnitude donor for `Max`: loss of a corepressor scaffold created a broad, indirect stress and RNA-processing state, while `Mnt`, an upstream MAX-network SIN3A recruiter, was flat in the same class.

I also symmetrically compared `Myc`, `Mycn`, `Mnt`, `Mga`, `Mlxip`, `E2f1`, `Tfdp1`, `Srebf1`, `Srebf2`, `Tfap4`, and `Trp53` score vectors in `151 TH Prkcd Grin2c Glut`. All 55 pairwise whole-profile similarities were near zero; `Mga`'s strongest in-cohort Pearson neighbor was only `Mnt` at 0.030, and `Myc` versus `Mga` was -0.010. No comparator pair in this cohort shared a significant positive or negative FDR 0.05 program. This reinforced the count-level readout: low DEG burdens were not hiding a coherent subthreshold MYC/MAX module.

## Synthesis

`Max` is reachable and should lose dimerization-competent stock by harvest, so a purely technical zero was too pessimistic. The only close measured MAX-network perturbation with a focal-class signal was `Mga`, with two genes, and direct MYC, MYCN, MNT, MLXIP, E2F, p53, and AP4 relatives were zero in this same cell class. The profile analysis did not identify a latent shared program that would justify borrowing the much larger `Sin3a`, `Gfpt1`, `Tsc2`, or `Setdb1` magnitudes. Balancing central MAX function against the almost-flat observed neighborhood, I predicted a tiny nonzero burden, below the `Mga` count because MAX loss need not reproduce MGA/PRC1.6-specific `Stag3` derepression.

Predicted `n_degs`: 1.
