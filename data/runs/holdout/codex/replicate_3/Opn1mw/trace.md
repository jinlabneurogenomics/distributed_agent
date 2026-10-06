# Direct n_degs forecast for 151 TH Prkcd Grin2c Glut

## Target

- Holdout manifest: `Opn1mw.csv`
- Target: `Opn1mw`
- Endpoint: `n_degs`, measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05` in `151 TH Prkcd Grin2c Glut`
- Point prediction: `0`

## Evidence used

The canonical `Opn1mw` biology bundle indicates a retinal cone photopigment, not a thalamic neuronal effector. Functional Opn1mw is installed in cone outer-segment membrane and supports medium-wave phototransduction; the mouse loss phenotypes in the bundle are retinal and do not transfer a molecular function into the assayed thalamic NeuN-positive nuclei. The 21-28 day P16-to-P37/P44 window should be long enough to deplete newly synthesized Opn1mw in an edited cone, but the relevant protein stock is still explicitly retinal outer-segment opsin.

The exact focal-population expression reach was very low despite the feature being available: `Opn1mw` had 1,012 UMIs among 377,814,907 non-target-cell UMIs in this class, or 2.679 pseudobulk CPM; only 885 of 23,679 non-target nuclei had any UMI, 3.74%, with mean raw expression 0.0427 UMI per cell. I interpreted this as near-absent/off-lineage sampling rather than evidence for an active M-opsin phototransduction pathway in thalamic glutamatergic neurons.

The same-experiment corpus had no target-centered Findings or Claims for `Opn1mw`, preserving the held-out state. It did provide same-assay comparator context for biologically adjacent retinal targets:

- `Opn1sw:F001` reported no FDR<0.10 downstream DE for the S-cone opsin perturbation in recovered brain-neuron cell groups.
- `Opn1sw:F003` reported that represented opsin and photoreceptor-regulatory perturbations did not phenocopy `Opn1sw` in matched brain-neuron groups.
- `Rho:F001` reported an almost inert rhodopsin loss-of-function surface in sampled juvenile brain neurons.
- `Rho:F003` reported that measurable photoreceptor relatives, including `Gucy2e`, `Spata7`, `Crx`, `Nr2e3`, `Opn1sw`, `Rpgr`, and `Rpgrip1l`, also failed to produce FDR<0.10 signatures in the Rho-matched brain groups.

Those Findings are packaged interpretations of the same Perturb-seq experiment, not independent replication, so I used them only to choose the relevant retinal-axis training perturbations and then checked the declared count table and expression Parquet directly.

The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` table is zero-heavy overall, with 1,205 of 1,674 training targets at `n_degs = 0`, median `0`, and 75th percentile `1`. More importantly, the retinal and photoreceptor comparators closest to Opn1mw were also zero in the exact focal population:

| comparator | focal n_degs |
| --- | ---: |
| `Opn1sw` | 0 |
| `Rho` | 0 |
| `Crx` | 0 |
| `Nr2e3` | 0 |
| `Rxrg` | 0 |
| `Thrb` | 0 |
| `Gucy2e` | 0 |
| `Spata7` | 0 |
| `Rpgr` | 0 |
| `Rpgrip1l` | 0 |

A direct Parquet filter for `151 TH Prkcd Grin2c Glut` confirmed that all 10 of those nominated comparator perturbations had zero rows at `pvals_adj < 0.05` and zero rows at `pvals_adj < 0.10`; each had 17,259 measured-gene rows in this population.

## Synthesis

The forecast is a focal-population null. Opn1mw has real postnatal biology after loss in retinal cones, and the stock card supports functional depletion within the experiment's 3-4 week window if the edited cell were an Opn1mw-expressing cone. The assayed population is instead thalamic glutamatergic neurons with only trace Opn1mw RNA, and same-screen retinal opsin, photoreceptor-transcription-factor, cGMP-recovery, and photoreceptor-cilium targets were transcriptionally silent in the same class. That combination makes an FDR-significant thalamic survivor-state signature unlikely; the residual risk is just a one- or two-gene off-lineage singleton in a high-yield class, which is not enough to move the integer point above zero.
