# Atp6v0c direct forecast trace

## Endpoint

- Target: `Atp6v0c`.
- Cell class: `151 TH Prkcd Grin2c Glut`.
- Forecast endpoint: `n_degs`, the count of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`.

## Evidence used

- The declared biology bundle places `Atp6v0c` in the focal assay population: the target feature is available and detected in 23,481 of 23,679 matched non-target nuclei in `151 TH Prkcd Grin2c Glut` (`99.16%`; mean raw UMI 9.16). This supports target reach but is not a target-outcome measurement.
- The same bundle characterizes Atp6v0c as the membrane c subunit of the V0 proton pore. It found limited same-subunit redundancy and substantial pre-edit installation of the operative membrane pool; the closest in-vivo mouse-brain turnover evidence puts a synaptic-vesicle Atp6v0c lifetime on the same order as the 21-28 day edit-to-harvest interval. The within-window stock conclusion was therefore `partially_depleted_or_leading_edge`, not complete clearance.
- The packaged same-experiment corpus had no `Atp6v0c` Findings or Claims, so it supplied no hidden target signature. It did contain V-ATPase training-target context. `Atp6v0a1:F001` reported self-detection with no downstream FDR<0.10 transcriptional response across 22 neuronal groups; `Atp6v0a1:F003`, `Atp6v1a:F004`, `Atp6v1e1:F005`, and `Atp6ap2:F004` all treated represented V-ATPase subunits/accessory factors as sparse, divergent, or flat rather than a shared lysosomal-collapse module.
- Curated mouse analog nomination intersected with the actual 1,674-gene training universe recovered the closest specific training analogs as `Atp6v1a`, `Atp6v1b2`, `Atp6v1e1`, `Atp6v0a1`, and `Atp6ap2`. The first four are V-ATPase core subunits or exact-complex/narrow-module relatives; `Atp6ap2` is an accessory physical-interaction comparator.
- In the declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` table, those closest perturbations had counts `Atp6v1a=0`, `Atp6v1b2=0`, `Atp6v1e1=0`, `Atp6v0a1=1`, and `Atp6ap2=2`.
- Direct Parquet inspection in `151 TH Prkcd Grin2c Glut` confirmed the significant rows behind that near-null count pattern: `Atp6v0a1` had only `Atp6v0a1` itself significant; `Atp6ap2` had only `Atp6ap2` and `Atp6v0a1`; the V1 subunit perturbations had no FDR<0.05 genes. Their recovered perturbed-cell counts ranged from 32 to 197 nuclei against 23,679 matched controls, so some individual analogs were underpowered but the shared empirical regime was still flat.
- Broader endolysosomal and proteostasis perturbations were retained only as boundaries. `Rab7`, `Psmb4`, and `Tsc2` produced 501, 742, and 86 focal DEGs respectively, showing that the assay can detect large endolysosomal/proteostatic or growth-control states in this class. They are not direct V-ATPase subunit analogs; the Atp6ap2 corpus report also described the Rab7 lysosomal/V-ATPase compensation program as opposite to the Atp6ap2 mini-signature.

## Synthesis

`Atp6v0c` is well expressed and should eventually be a material acidification lesion because it has no close same-subunit replacement. The 3-4 week PerturbAI readout, however, is survivor-conditioned and falls only around one Atp6v0c protein-lifetime estimate for an already-installed vesicle pool. The best task-matched training evidence is therefore the core V-ATPase cohort, not high-burden lysosome/proteasome stress perturbations reached through broader annotations. Those direct analogs were consistently null or one-to-two-gene in `151`, and their significant calls were self or another V-ATPase transcript rather than a coordinated TFEB/autophagy/UPR module.

The point forecast is `1`: near-null, with one possible BH-significant self/proximal V-ATPase transcript favored over an exact zero because Atp6v0c is highly expressed in the focal population and the two non-V1 V-ATPase-proximal analogs each retained a self/proximal hit.
