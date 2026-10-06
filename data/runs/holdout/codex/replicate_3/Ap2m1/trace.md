# Ap2m1 direct n_degs forecast

## Target and endpoint

- Target: `Ap2m1`.
- Cell group: `151 TH Prkcd Grin2c Glut`.
- Endpoint: count of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05` in the held-out `Ap2m1` perturbation.

The held-out target's own signature was not used. The prediction used the declared `Ap2m1` biology bundle, the training-only `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` table, bounded same-experiment Finding summaries for training perturbations, and an observed-profile comparison among selected training perturbations in `151 TH Prkcd Grin2c Glut`.

## Target prior

`Ap2m1` is well reached in the focal population: the declared exact non-target expression card reports expression in 21,579 of 23,679 `151 TH Prkcd Grin2c Glut` nuclei, or 91.13%, with mean raw UMI 3.57 and pseudobulk CPM 223.5.

The biology card supports realized functional loss by harvest. AP-2 mu is the single mammalian AP-2 mu subunit, participates in synaptic-vesicle/cargo sorting and TrkB-autophagosome transport, and its dynamic neuronal stock should be substantially depleted over the P16 to P37-P44 interval: the bundle cites a 5.35 day neuronal-culture half-life, direct conditional depletion below 15% in mouse hippocampal neurons, mature-neuron effects by 4 weeks, and early postnatal thalamic degeneration after neuron-specific `Ap2m1` loss. This made a pure zero forecast less plausible than it would be for an unexpressed, redundant, or stock-persistent target.

Two caveats kept the prior moderate rather than Rab7-like high:

- AP-2 loss is a cargo-sorting/synaptic/endocytic lesion, not a terminal lysosome blockade.
- The single-nucleus readout is conditioned on recovered surviving nuclei, so the most damaged `Ap2m1`-null thalamic cells could be attenuated or absent by harvest.

## Training counts used

The 1,674-gene training table for the same cell class is highly zero-inflated:

- median = 0
- 75th percentile = 1
- 90th percentile = 2
- 95th percentile = 18
- mean = 14.05, dominated by a small right tail

The direct AP/clathrin/synaptic-vesicle analogs were at the floor:

| training perturbation set | `151` n_degs |
| --- | ---: |
| AP-family adaptors: `Ap1b1`, `Ap1s2`, `Ap3b1`, `Ap4s1` | 1, 0, 0, 0 |
| core clathrin/endocytosis: `Cltc`, `Dnm1`, `Synj1`, `Nsf` | 3, 1, 1, 0 |
| synaptic-vesicle machinery: `Syp`, `Sv2a`, `Stxbp1`, `Vamp1`, `Pclo`, `Bsn`, `Unc13a` | 1, 1, 1, 1, 0, 0, 0 |
| represented basal autophagy genes: `Atg5`, `Atg16l1`, `Becn1`, `Rubcn`, `Rb1cc1` | 0, 0, 0, 0, 4 |

The modest high-side trafficking references were:

| training perturbation | role in interpretation | `151` n_degs |
| --- | --- | ---: |
| `Vps35` | retromer/endosomal recycling, selective 151 signature | 17 |
| `Vps54` | endomembrane trafficking reference | 31 |
| `Wdfy3` | autophagy/endolysosomal-adjacent reference | 17 |
| `Dhdds` | lipid-linked trafficking/stress reference, broader and less directly AP-2-like | 116 |
| `Atp2a2` | ER-calcium/stress reference, not local to AP-2 | 187 |
| `Rab7` | late endosomal/lysosomal stress upper bound | 501 |

Same-experiment Findings resolved how to weight these rows. `Ap3b1` was reported as transcriptionally buffered across 18 recovered neuronal groups, and measurable AP-family comparators did not show a shared nuclear AP-adaptor response. `Cltc` produced a selective clathrin response, but the same reports state that canonical synaptic endocytosis/uncoating targets such as `Dnm1` and `Synj1` did not phenocopy it. `Vps35` was restricted mostly to `151` and lacked the broad lysosomal branch. `Rab7` was much broader, with late-endosomal/lysosomal, sterol, ISR/UPR, autophagy, redox/apoptotic, and proteasome compensation, and HOPS/retromer/WASH/V-ATPase comparators mostly failed to phenocopy it at FDR level. I therefore treated `Rab7` as a stress-state ceiling rather than as a magnitude donor.

The direct profile comparison over 61 selected training perturbations in `151 TH Prkcd Grin2c Glut` supported this split: among the focal material nodes, `Cltc` had 3 significant genes, `Vps35` had 17, `Vps54` had 31, `Vps41` had 0, and `Rab7` had 501. Significant-gene overlap between `Rab7` and the low AP/autophagy peers was essentially absent, while `Vps35`/`Vps54` gave the closest modest trafficking-scale references.

## Point forecast

The AP-2 mu lesion should be stronger than the observed AP-1/AP-3/AP-4 and synaptic-vesicle floor because `Ap2m1` is highly expressed in the target class, nonredundant, and expected to lose operative stock within the screen window. At the same time, the closest measured AP/clathrin/endocytosis rows argue that a trafficking perturbation usually does not explode into hundreds of nuclear DE genes in recovered `151` neurons, and the broad `Rab7` response is off-axis for a plasma-membrane AP-2 cargo adaptor.

I placed `Ap2m1` below the `Vps35`/`Vps54` retromer/GARP modest-response bracket but clearly above the 0-3 DEG AP/clathrin/synaptic floor, giving:

`predicted_n_degs = 12`
