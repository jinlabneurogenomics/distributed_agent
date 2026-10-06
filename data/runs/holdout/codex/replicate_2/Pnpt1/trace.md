# Pnpt1 direct n_degs prediction

## Target and endpoint

- Target manifest: `Pnpt1`.
- Cell class: `151 TH Prkcd Grin2c Glut`.
- Endpoint: number of measured genes with Wilcoxon BH-adjusted `p < 0.05`.
- Held-out status: `Pnpt1` was absent from the declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` count table, so the point below is inferred from the biology-only `Pnpt1` bundle, training counts, and training-profile context.

## Pnpt1 prior

The prediction-safe biology bundle supports reach and possible realization:

- `Pnpt1` is expressed in the assayed thalamic non-target population: mean raw UMI `1.696`, mean log1p CP10k `0.632`, and `18,215 / 23,679` non-target nuclei expressing the transcript.
- PNPase is a renewable homotrimeric mitochondrial RNA-processing/import exoribonuclease with continuous substrate demand.
- The CRISPR perturbation should halt new PNPase production while existing trimers decay; the bundle adjudicates functional stock at the P37-P44 harvest as likely substantially depleted but only partially evidenced because a target-specific neuronal protein half-life was not found.
- Postnatal Pnpt1 loss is consequential in mouse sensory hair cells by a 3-4 week scale, but that evidence is developmental and non-thalamic, so it raises observability without proving a thalamic ISR/interferon response after a sparse P16 neuronal edit.

## Training evidence that set the scale

The `151 TH Prkcd Grin2c Glut` training count table was sparse: among `1,674` training perturbations, the median `n_degs` was `0`, `469` had at least one DEG, `106` had at least `10`, and `43` had at least `100`.

For Pnpt1's closest represented mitochondrial RNA/metabolism references, the exact focal counts were all null:

| class | training targets | focal `n_degs` |
| --- | --- | --- |
| mitochondrial RNA / translation-adjacent | `Lrpprc`, `Rars2`, `Fars2`, `Lars2` | `0`, `0`, `0`, `0` |
| mitochondrial proteostasis | `Clpp`, `Clpx`, `Lonp1`, `Yme1l1` | `0`, `0`, `0`, `0` |
| respiratory-chain / import / TCA comparators | `Cox11`, `Cox4i1`, `Cox5a`, `Cox6a1`, `Cox7b`, `Cox8a`, `Ndufa9`, `Ndufs2`, `Ndufs4`, `Ndufs8`, `Tomm40`, `Timmdc1`, `Uqcrfs1`, `Uqcrc2`, `Slc25a4`, `Abcb7`, `Aco2` | median `0`, maximum `1` |

The exact Parquet slice for a deliberately small 18-target mitochondrial comparison had the same pattern: `15 / 18` selected references had no significant features in this class; the exceptions were `Tomm40` with `1`, `Opa1` with `37`, and `Nrf1` with `138`. The cohort profile comparison did not reveal a tight positive transcriptional module that could make the zero-count mitochondrial RNA targets look like hidden large responders: median positive top-tail overlap was only `0.07`, with no FDR-level shared significant program across the mostly-null profiles.

Packaged same-experiment interpretation reinforced the count table. `Lrpprc`, the closest measured target affecting mitochondrial mRNA handling, had a pan-measured neuronal transcriptional null and lacked the expected mtDNA mRNA, ISR, or UPR-mt programs. `Clpp` and `Clpx` similarly failed to induce canonical mitochondrial protease/stress output. `Opa1` demonstrates that the assay can see a secondary mitochondrial ATF4/ISR-like state, including in this population, but corpus claims explicitly caution that same-organelle mitochondrial perturbations are branch-specific rather than interchangeable.

## Synthesis

`Pnpt1` has better focal expression than many quiet genes and no established close paralog, so I did not treat it as a generic null target. The reason to keep the point at the floor is that the endpoint is a thresholded nuclear snRNA-seq response in recovered postmitotic thalamic neurons, and the represented mitochondrial RNA, translation, proteostasis, OXPHOS, import, and TCA perturbations overwhelmingly sit at `0` or `1` in the same `151` count table. The high-count mitochondrial-stress positives are real but are downstream-state boundaries, not direct Pnpt1-scale donors.

Balancing those facts, I put the expected response below one FDR-significant gene and rounded to the nearest feasible count:

`predicted_n_degs = 0`
