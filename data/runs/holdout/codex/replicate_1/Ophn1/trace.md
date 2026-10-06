# Ophn1 `n_degs` forecast

## Target and endpoint

- Held-out manifest target: `Ophn1`.
- Cell group: `151 TH Prkcd Grin2c Glut`.
- Endpoint: number of measured genes in that cell group with BH-adjusted Wilcoxon `pvals_adj < 0.05`.
- The declared training count table contains 1,674 observed perturbations and no `Ophn1` row.

## Biology prior from the declared bundle

The canonical `Ophn1` biology bundle supports target engagement being biologically plausible by P37-P44: OPHN1 supplies Rho-family GAP activity and synaptic scaffolding/trafficking functions, neuronal RNAi evidence places protein depletion and synaptic/spine effects within 2-8 days, and the card adjudicates the 21-28 day CRISPR window as `likely_substantially_depleted`. The bundle also makes the main dilution caveat explicit: the exact in-assay focal-population reach in `151 TH Prkcd Grin2c Glut` is moderate rather than universal, with `Ophn1` detected in 11,715 of 23,679 non-target nuclei, or 49.474% of the group.

That argues against a failed perturbation prior, but it also argues against assigning a broad transcriptional program by default. The best-supported OPHN1 loss biology is local Rho/cytoskeletal and excitatory-synapse regulation, not a core chromatin, ribosome, spliceosome, mitochondrial, or proteasome lesion expected to reshape many nuclear RNA abundances in most recovered thalamic neurons.

## Training analog counts

I nominated eligible analogs from typed mouse annotations against the actual training universe with the gene-analog nominator and then joined the result to the declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` count table. The specific OPHN1/Rho-cycle tranche was uniformly quiet:

| analog | relationship used | observed `151` n_degs |
|---|---|---:|
| `Arhgap32` | RhoGAP / Rho-family GTPase-cycle narrow module | 0 |
| `Baiap2` | Rho/actin postsynaptic effector | 0 |
| `Cdc42` | direct OPHN1 substrate-side Rho-family GTPase | 1 |
| `Rac1` | direct OPHN1 substrate-side Rho-family GTPase | 0 |
| `Myo9a` | actin-linked RhoGAP fallback | 0 |
| `Ocrl` | Rho-cycle/endocytic module member | 0 |
| `Limk1` | Rho-actin effector | 0 |
| `Syngap1` | postsynaptic GAP fallback | 0 |

The broader narrow-module hits that came mostly through Hedgehog or axon-guidance annotations were also low and less operation-matched: `L1cam` = 1, `Unc5c` = 1, `Nrcam` = 2, `Nrp1` = 0, `Nrp2` = 0, `Ptch1` = 0, `Vldlr` = 0, `Gli1` = 0, and `Adgrg1` = 0. Synaptic receptor/scaffold boundaries did not justify moving to a larger response: `Dlg4` had 1 DEG, while the less scale-matched receptor subunit `Grin1` was the outlier at 89 DEGs.

As background scale, the same count table is zero-heavy in this high-yield cell group: 1,205/1,674 training perturbations have 0 DEGs and 1,512/1,674 have at most 2 DEGs.

## Matched profile check

I compared the 22 retained analog and boundary profiles in the declared Parquet, restricted to `group_name == "151 TH Prkcd Grin2c Glut"`, with `scores` as the signed value and `pvals_adj < 0.05` as the significant-feature definition. Fifteen of the 22 reviewed analogs had no significant genes, six had 1-9, and only `Grin1` reached the `at_least_50_significant_features` bucket.

The pairwise signed-profile comparison did not expose a hidden shared subthreshold RhoGAP program that would argue for a larger rounded count: `Arhgap32`, `Baiap2`, and `Syngap1` each had no significant features, `Cdc42` had one negative significant feature, and their Pearson/cosine similarities to the Rho-cycle peers were all near zero with no significant-program intersections.

## Numeric synthesis

Functional OPHN1 depletion should be reached in edited, target-positive neurons, so a nonzero biological effect is plausible. For this exact endpoint, however, the expression reach is only about half of recovered `151` nuclei, the expected state is local synaptic/Rho-cytoskeletal, and every direct RhoGAP, Rho-family substrate, and actin/synapse comparator in the training table landed at 0 or 1 DEG. I therefore used the operation-matched analog center, with the broader `Grin1` boundary excluded as a stronger off-axis receptor lesion, and rounded to the modal/median observed direct-analog count.

Predicted `n_degs`: **0**
