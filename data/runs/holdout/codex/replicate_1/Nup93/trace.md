# Nup93 direct DEG-count forecast

## Target and endpoint

- Target manifest row: `Nup93`
- Cell class: `151 TH Prkcd Grin2c Glut`
- Endpoint: number of measured genes with Wilcoxon `pvals_adj < 0.05`
- Training endpoint table: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- Training row-level profile table: `[local file: training_de_all_cell_groups.parquet]`
- Target biology bundle: `[local file: Nup93.json]`

I used the target-safe `biology` characterization view for `Nup93`; it exposed no target outcome and no labeled-neighbor outcomes. I did not query or reconstruct the held-out `Nup93` differential-expression signature or count.

## Training-count context

The declared one-class training table contains 1,674 measured perturbation targets in `151 TH Prkcd Grin2c Glut`.

- `1205 / 1674 = 71.98%` had `0` FDR<0.05 genes.
- `276 / 1674` had exactly `1`.
- `1546 / 1674 = 92.35%` had `<=5`.
- The table is heavy-tailed: median `0`, mean `14.05`, 99th percentile `430`, maximum `2677`.

This makes a near-zero call the default unless the target biology looks like a fast and well-realized perturbation whose product is needed over the P16 to P37-P44 window.

## Nup93 biology

The exact focal-population expression card says `Nup93` is available in the assayed thalamic class: `19,848 / 23,679` non-target nuclei expressed it, with `mean_raw_umi = 2.3358`, `mean_log1p_cp10k = 0.7947`, and `pseudobulk_cpm = 146.39`. Expression therefore was not the limiting factor.

The limiting factor was target-stock realization. The characterization card classified the operative entity as an installed nuclear-pore scaffold/linker and concluded that functional pore-incorporated NUP93 likely persists through harvest. The selected facts were:

- `Nup93.operation.1`: NUP93 is a conserved nuclear-pore inner-ring linker/scaffold needed for structurally complete, transport-competent pores.
- `Nup93.turnover_rate.2`: in postmitotic rat neuronal nuclei, the Nup93/Nup155/Nup205 scaffold subcomplex retained old isotope for many months.
- `Nup93.turnover_rate.3`: mouse postmitotic myotubes showed very little Nup93 exchange over 14 days.
- `Nup93.prior_phenotype.1`: the closest mature mouse conditional loss model, differentiated podocyte deletion, developed overt dysfunction over roughly 4-6 months, far beyond the 21-28 day Perturb-seq window.

The card also found no close mouse `Nup93` paralog, so the low forecast is not because NUP93 is redundant. It is because P16 editing stops new supply but should not rapidly dismantle most pre-existing postmitotic NPC inner-ring stock before the P37-P44 readout.

## Comparator counts actually used

Curated annotation lookup put `Nup93` in broad nuclear-pore and nucleocytoplasmic-transport sets, but not in a clean, observed, same-operation inner-ring training cohort:

- CORUM:human-ortholog projected `Nuclear pore complex`, set `8674`, contributed only `Ranbp2` and `Tpr` besides held-out `Nup93` among perturbation targets.
- GO `nuclear pore inner ring` had `Nup155`, `Nup188`, and `Nup205`, but none was perturbed in the training table.
- KEGG `Nucleocytoplasmic transport` contributed a broader and mechanistically mixed set.

Counts in the declared `151 TH Prkcd Grin2c Glut` table for observed broad nuclear-pore/transport targets were:

| target | n_degs | interpretation for Nup93 |
| --- | ---: | --- |
| `Ranbp2` | 0 | structural NPC/SUMO/nuclear-pore comparator that was quiet in the focal class |
| `Tpr` | 1768 | high boundary; nuclear-basket/export perturbation with a strong RNA-processing/proteostasis state |
| `Tnpo3` | 618 | high boundary; SR-splicing cargo import, not a structural NPC stock analogue |
| `Thoc1` | 303 | high boundary; THO/TREX mRNA export/RNA-processing machinery |
| `Upf3b` | 1 | nearly quiet broader transport-pathway member |
| `Chmp4b` | 0 | quiet broader nuclear-pore annotation |
| `Ddx39b` | 0 | quiet broader mRNA-export member in this focal class |
| `Eif5a` | 0 | quiet broader nuclear-pore annotation |
| `Kpna3` | 0 | quiet broader importin member |
| `Xpo7` | 0 | quiet broader exportin member |

The same-experiment corpus supported the same partition. `Tpr`, `Tnpo3`, and `Thoc1` had strong reports tied to nuclear export, spliceosome/RNA-processing, and proteostasis response programs. The `Tnpo3` report explicitly separated its convergence with spliceosome/RNA-processing perturbations from the absence of a generic broad nuclear-transport phenocopy: `Kpna3` and `Xpo7` shared no FDR-level calls with `Tnpo3`, and `Ranbp2` shared only a small MB-Glut-restricted component. The `Ranbp2` report showed a response in other classes, but not in `151 TH Prkcd Grin2c Glut`.

I also compared the observed broad transport cohort in the focal-class Parquet using Wilcoxon score profiles with `pvals_adj < 0.05`. `Tpr`, `Tnpo3`, and `Thoc1` were the only high-response nodes; `Ranbp2` had `0` significant features. Within the compared set, `Tpr` was closest to `Tnpo3` and `Thoc1`, reinforcing that the large `Tpr` count reflects an RNA-export/RNA-processing state rather than a transferable inner-ring scaffold depletion state.

## Numeric synthesis

`Nup93` has enough focal expression and little paralog protection, so a small self-transcript or partial-NPC signal is biologically possible. I nevertheless put the point at the zero mode because the direct operation is buffered by long-lived preassembled NPC stock, the available strict structural comparator `Ranbp2` is quiet in the exact focal class, and the large observed pathway neighbors are dynamic transport/export/RNA-processing perturbations rather than inner-ring scaffold analogues.

Predicted `n_degs`: `0`
