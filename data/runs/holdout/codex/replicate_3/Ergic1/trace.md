# Ergic1 `151 TH Prkcd Grin2c Glut` DEG-count forecast

## Declared target

- Target: `Ergic1`
- Endpoint: `n_degs`, the count of measured genes in `151 TH Prkcd Grin2c Glut` with Wilcoxon BH-adjusted `p < 0.05`.
- Held-out target provenance: `[local file: Ergic1.csv]`
- Biology bundle provenance: `[local file: Ergic1.json]`
- Training count provenance: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- Raw profile provenance: `[local file: training_de_all_cell_groups.parquet]`

## Evidence used

The exact target-expression entry in the declared `Ergic1` biology bundle makes the perturbation observable in the focal class: in non-target nuclei from `151 TH Prkcd Grin2c Glut`, `Ergic1` was detected in 22,288 of 23,679 cells, 94.1%, with mean raw UMI 3.97, mean CP10k 2.47, and mean log1p CP10k 1.145. I treated this as enough expression reach for a response if the lesion is functionally realized, but not as evidence for a large signature.

The same bundle identifies ERGIC1 as a cycling ER-ERGIC-Golgi membrane protein that interacts with ERGIC3. The functional-stock adjudication is unresolved for this assay window: a P16 edit should stop new functional ERGIC1 synthesis, but it does not directly clear pre-existing membrane protein, and no Ergic1-specific degradation, residence-time, or post-edit clearance clock was found for postmitotic neurons. The mouse knockout prior is also nonlocal: constitutive homozygous loss caused preweaning lethality and heterozygotes had decreased grip strength, but neither isolates an acute postnatal thalamic neuronal phenotype.

The `151 TH Prkcd Grin2c Glut` training count table is strongly zero-inflated: 1,205 of 1,674 training targets had `n_degs = 0`, the median was 0, the 75th percentile was 1, and the 90th percentile was 2. The large-count tail was real but exceptional, with 43/1,674 targets at least 100 DEGs and 15/1,674 at least 500 DEGs.

I used the ER/Golgi trafficking perturbations available in the declared training table as the closest operation-level comparators:

| comparator | role relative to Ergic1 | training `n_degs` |
| --- | --- | ---: |
| `Copa` | COPI coat, early secretory retrograde trafficking | 0 |
| `Copg1` | COPI coat | 1 |
| `Lman2l` | secretory cargo/ER-Golgi lectin-family branch | 0 |
| `Sar1b` | COPII vesicle initiation | 0 |
| `Sec23a` | COPII coat | 0 |
| `Stx5a` | ER-Golgi/TGN SNARE | 0 |
| `Sec63` | ER translocation/proteostasis, looser than ERGIC | 11 |
| `Vps35` | retromer endosome-to-Golgi, looser than ERGIC | 17 |
| `Vps54` | GARP retrograde trafficking, looser than ERGIC | 31 |

I then checked the raw thalamic profiles for the same nine genes in `training_de_all_cell_groups.parquet` with a profile comparison artifact at `workbench/ergic1_analogue_profile_compare.json` and inspection artifact at `workbench/ergic1_analogue_profile_inspect.json`. In that raw-signature check, five of the nine comparators had no significant features in the focal cell class, one had 1-9, and three had 10-49. The most local COPI/COPII/ERGIC-adjacent subset contributed one focal-class DEG in six perturbations.

The same-experiment corpus summaries support interpreting those zeros as a recurrent buffered secretory-trafficking pattern rather than an artifact of the count table. `Copa` was summarized as a strict whole-transcriptome neuronal null; `Copg1` did not recover canonical COPI-failure ER-stress, UPR/ISR, or STING/type-I-IFN programs; `Lman2l` was silent in every recovered neuronal group; `Sar1b` did not induce a detectable COPII, UPR, or ISR compensation program; `Sec23a` produced no adjusted downstream response in any measured postmitotic neuronal group; and `Stx5a` was almost empty across its measured surface.

## Synthesis

High `Ergic1` expression argues against dismissing the perturbation for lack of target reach, and the constitutive mouse phenotype argues that the gene is biologically important somewhere. Those bearings were outweighed for this specific endpoint by the unresolved acute functional-stock depletion and by the measured behavior of the nearest ER/Golgi trafficking losses. In this atlas, COPI and COPII disruption did not automatically turn into a thalamic nuclear UPR, ISR, STING, or broad trafficking-failure signature. Because `Ergic1` is another early-secretory membrane component with an indeterminate residual pool at 21-28 days after editing, the closest measured evidence places it at the floor of the count distribution.

I therefore used the modal local result, with a small allowance for uncertainty from expression reach and developmental essentiality, and predicted no BH-significant downstream genes:

`predicted_n_degs = 0`
