# Stim1 DEG-count prediction trace

## Question and resolved ambiguities

The held-out target list for this run contains one mouse gene, `Stim1`, and the requested scalar is the number of genes with `pvals_adj < 0.05` after perturbing that gene in `151 TH Prkcd Grin2c Glut` cells. I treated the count as exactly the endpoint in `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`, not as a genome-wide importance score, a viability score, or a self-transcript editing score. The held-out `Stim1` perturbation itself is absent from both input files, so all numerical evidence below comes from non-held-out perturbations.

`151 TH Prkcd Grin2c Glut` was interpreted as the focal thalamic glutamatergic neuronal class, with `TH` denoting thalamus in the Allen-derived class name.

## Sources used

- The supplied training endpoint file `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`, which provided exact FDR 0.05 DEG counts for 1,674 non-held-out perturbations.
- The supplied `training_de_all_cell_groups.parquet`, queried in the focal cell group for per-gene log2 fold changes, Wilcoxon scores, and adjusted p values.
- Distributed Agents same-experiment semantic corpus `perturbai-july-260713-sourceguard-1773-v1`, especially `target_context` for `Atp2a2`, `Itpr1`, and `Calm1`, plus `candidate_set_topology` over a calcium/ER-quality-control comparator panel.
- Distributed Agents runtime `profile_compare` / `profile_inspect` over a caller-nominated 30-target calcium/ER panel in the focal cell group. This was used only to inspect pairwise observed signatures; it did not assign the prediction.
- External PubMed literature on STIM/Orai calcium signaling:
  - Zhang et al. 2005, Nature, DOI `10.1038/nature04147`, PMID `16208375`.
  - Hartmann et al. 2014, Neuron, DOI `10.1016/j.neuron.2014.03.027`, PMID `24811382`.
  - Kraft 2015, Channels, DOI `10.1080/19336950.2015.1071747`, PMID `26218135`.
  - Ryu et al. 2017, Journal of Neuroscience, DOI `10.1523/JNEUROSCI.3973-16.2017`, PMID `28821659`.
  - Sun et al. 2014, Neuron, DOI `10.1016/j.neuron.2014.02.019`, PMID `24698269`.

## Computational steps

1. Read the requested-target manifest; it contained exactly `Stim1`.
2. Read the 1,674-row training count CSV. The endpoint was sparse: 1,205/1,674 perturbations had `n_degs = 0`; 363 had 1-9; 63 had 10-89; and 43 had at least 100. The maximum in the focal group was `Uba5 = 2677`.
3. Inspected Parquet metadata and used row-group statistics on `group_name` to extract just `151 TH Prkcd Grin2c Glut` into `workbench/focal_151.parquet`. This focal slice contained 28,891,566 rows, equal to 1,674 training targets times 17,259 measured genes.
4. Nominated a mechanistic comparator panel before looking at its exact focal counts: ER calcium-store refilling and SOCE neighbors (`Atp2a2`, PMCA/SPCA pumps, `Itpr1`, `Ryr2`, `Ryr3`, `Atf6`), calcium/calmodulin and postsynaptic effectors (`Calm1/2/3`, `Camk2*`, `Ppp3*`, `Cacna1g`, `Grm1`, `Homer2`, `Plcb1`, `Prkca`, `Prkcg`, `Nfatc3`), and ER proteostasis-state comparators (`Hspa5`, `Gfpt1`, `Dhdds`, `Sec63`, `Elp2`).
5. For each comparator in the focal slice, counted genes with `pvals_adj < 0.05` and then inspected the Atp2a2 UPR/ISR marker genes. The relevant exact counts were:

| comparator | focal `n_degs` | interpretation for `Stim1` |
| --- | ---: | --- |
| `Atp2a2` | 187 | SERCA2 ER-store refilling loss; strongest local ER-Ca positive comparator, but a more direct store-depletion lesion than `Stim1`. |
| `Atp2b1` | 22 | Plasma-membrane Ca2+ pump with a small thalamic activity signature but no Ddit3/Xbp1/Hspa5 ER-stress module. |
| `Atp2b2`, `Atp2b3`, `Atp2c1` | 1, 1, 1 | Other calcium pumps were nearly silent in this cell group. |
| `Itpr1`, `Ryr2`, `Ryr3` | 0, 0, 0 | ER calcium-release channels were fully silent at FDR 0.05. |
| `Atf6` | 0 | Isolated UPR-transcription-factor arm did not create a detected response. |
| `Calm1`, `Calm2`, `Calm3` | 14, 0, 1 | Single calmodulin loci produced sparse or absent signatures. |
| `Camk2a`, `Camk2b`, `Camk2g` | 0, 1, 0 | CaMKII nodes did not yield a coordinated focal response. |
| `Ppp3ca`, `Ppp3cc`, `Ppp3r1`, `Nfatc3` | 4, 0, 9, 0 | Calcineurin/NFAT perturbations were weak or null. |
| `Cacna1g` | 12 | A small thalamic calcium-channel response; not an ER-store analogue. |
| `Grm1`, `Homer2`, `Plcb1`, `Prkca`, `Prkcg` | 1, 0, 0, 0, 1 | mGluR/IP3-adjacent nodes were flat or singleton. |
| `Gfpt1`, `Dhdds`, `Elp2` | 311, 116, 150 | Strong same-direction Atp2a2 UPR/ISR state analogs, but they perturb glycosylation, dolichol supply, or Elongator rather than SOCE. |
| `Sec63`, `Hspa5` | 11, 5 | ER-client/BiP-axis state comparators with much smaller focal counts. |

The key pattern was that `Atp2a2` itself gave 105 up and 82 down significant genes, headed by canonical ER-stress/ISR genes including `Ddit3`, `Chac1`, `Xbp1`, `Herpud1`, `Hspa5`, `Asns`, `Slc38a1`, `Slc38a2`, `Slc1a4`, `Slc7a5`, `Shmt2`, `Mthfd2`, `Psph`, `Aldh1l2`, `Trib3`, and `Sesn2`. `Gfpt1`, `Dhdds`, and `Elp2` overlapped 94, 47, and 53 of the 187 Atp2a2 FDR 0.05 genes respectively, all in the same direction. By contrast the immediate calcium-release and SOCE-adjacent training perturbations had no such significant overlap: `Itpr1`, `Ryr2`, `Ryr3`, `Atp2b2`, `Atp2b3`, `Atp2c1`, and `Atf6` shared zero FDR 0.05 genes with the Atp2a2 signature in `151`.

## Target-specific reasoning

### `Stim1`

External mechanism put `Stim1` upstream of store-operated calcium entry rather than in the ER pump itself. STIM1 is an ER luminal calcium sensor that oligomerizes and couples ER-store depletion to Orai/CRAC channel opening at ER-plasma-membrane junctions (Zhang et al. 2005). In neurons, STIM/Orai biology is real but isoform- and compartment-specific: Kraft 2015 summarizes that STIM1 controls ER Ca2+ store replenishment in cerebellar Purkinje neurons, while STIM2 is particularly tied to hippocampal/cortical neuronal SOCE; Hartmann et al. 2014 and Ryu et al. 2017 showed that Purkinje-cell Stim1 loss changes mGluR1-dependent calcium signaling, somatic Ca2+ handling, firing, and cerebellar motor behavior. Sun et al. 2014 separately places STIM2, not STIM1, in a basal hippocampal mushroom-spine nSOC-CaMKII maintenance pathway.

Those external results kept me from treating `Stim1` as a generic null gene: a STIM1 loss can plausibly change neuronal calcium homeostasis. However, they also argued against assigning the full Atp2a2-like 187-DEG ER-stress count. SERCA2/`Atp2a2` loss directly impairs Ca2+ import back into the ER and in this exact assay activated a Ddit3/Xbp1/Chac1/Hspa5 ISR/UPR state. `Stim1` loss instead prevents the ER store-depletion sensor from productively engaging Orai/TRPC channels. That should reduce a refilling route after store depletion, especially during activity, but it is not equivalent to blocking the pump that continuously loads the ER.

The same-experiment corpus reinforced that distinction. `Atp2a2:F007` and the high-confidence corpus claim `claim:16ed634c5b3dc2e0831c` state that Atp2a2/SERCA2 selectively activated the neuronal ER-stress ISR/UPR state and that assayed calcium-release channels, PMCA/SPCA pumps, and isolated `Atf6` did not phenocopy it. `Itpr1:F004` explicitly reported that `Itpr1` had 0 downstream genes in `151` while `Atp2a2` induced Ddit3/Xbp1/Herpud1/Hspa5/Chac1/Atf4. `Itpr1:F005` and `Calm1:F004` further bounded the mGluR/IP3R and CaM/calcineurin/CaMKII branches as mostly flat or divergent under basal 3-4-week postnatal snRNA-seq.

The within-dataset analogs therefore split into three groups:

- Strong Atp2a2/Gfpt1/Dhdds/Elp2 ER-quality-control state donors with 116-311 DEGs are useful to show what a UPR/ISR state looks like in `151`, but they are downstream-state analogs rather than direct `Stim1` analogs.
- Directly relevant calcium-homeostasis counterexamples, including `Itpr1 = 0`, `Ryr2 = 0`, `Ryr3 = 0`, `Atf6 = 0`, `Atp2b2 = 1`, `Atp2b3 = 1`, `Atp2c1 = 1`, `Calm2 = 0`, and `Camk2a = 0`, show that perturbing canonical Ca2+ signaling hardware usually did not trigger a detectable focal nuclear-RNA state.
- A few thalamic calcium/activity nodes were weakly but nonzero: `Atp2b1 = 22`, `Calm1 = 14`, `Cacna1g = 12`, and `Ppp3r1 = 9`.

I therefore predict that `Stim1` will be weakly detectable, because it can limit store refilling upstream of ER-stress and activity pathways in vulnerable neurons, but near the bottom of the nonzero range because the direct pathway comparators were overwhelmingly FDR-null and because `Stim1` has a more stimulus-dependent, redundant, compartmentalized neuronal role than `Atp2a2`. The point prediction is `3` DEGs.

## Limits

The strongest gap is that the strict SOCE paralog/channel comparators `Stim2`, `Orai1`, `Orai2`, and `Orai3` were absent from the training count file, so the prediction extrapolates from ER pumps, ER-release channels, PMCA/SPCA pumps, and calmodulin/calcineurin/CaMKII nodes instead of from a true same-complex perturbation. External literature is dominated by Purkinje, hippocampal, cortical, cultured, glial, or older conditional-knockout contexts, none of which exactly match a sparse P16-to-P37/P44 CRISPR loss in thalamic `151` nuclei. A transient calcium or activity phenotype, a subcellular spine phenotype, or a survival phenotype could be missed by this nuclear RNA endpoint. Finally, the predicted value is a point estimate for an assay-power-dependent FDR count; a change of only a few marginal genes around FDR 0.05 would move the integer noticeably.
