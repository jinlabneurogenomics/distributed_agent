# Direct forecast trace for Mpdz

## Declared target and endpoint

- Target: `Mpdz`, from the one-row holdout manifest `Mpdz.csv` and the declared biology bundle `Mpdz.json`.
- Focal endpoint: `n_degs` in `151 TH Prkcd Grin2c Glut`, the number of measured rows with BH-adjusted Wilcoxon `pvals_adj < 0.05`.
- Direct training endpoint source: `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Direct row-level source used for profile checks: `training_de_all_cell_groups.parquet`, restricted to `group_name == "151 TH Prkcd Grin2c Glut"`.
- The report/Finding corpus was used only as the same-experiment semantic interpretation of already-measured training perturbations, not as independent replication.

## Biology of the held-out perturbation

The biology-only `Mpdz` bundle supports target presence but not a strong matched thalamic transcriptional prior. In focal non-target nuclei, `Mpdz` was detected in 15,396 of 23,679 cells, 65.02%, with mean CP10K 0.800 and mean raw UMI 1.251, so the transcript was reachable in the exact cell population rather than absent. The source card, however, places the best direct mouse mechanism in ependymal, choroid-plexus, epithelial, and sensory hair-cell junction biology: MPDZ is a 13-PDZ-domain scaffold that organizes tight-junction, adherens-junction, receptor, and Crumbs-polarity complexes; global or developmental neural-lineage loss causes early-postnatal hydrocephalus through ventricular barrier defects. That is evidence for biological activity of MPDZ, but it is not a matched P16 postmitotic thalamic-neuron assay.

The functional-stock card also lowered the expected acute RNA footprint. A disruptive P16 edit should stop new MPDZ supply, but MPDZ is already incorporated into localized protein assemblies; no target-specific neuronal residence time or post-edit clearance curve was found, and `Patj`/`Inadl` compensation in juvenile thalamic neurons is unknown. Thus the 21-28 day window is long enough for some renewal-driven effect but not enough to assume wholesale removal of pre-existing MPDZ scaffold.

## Training measurements that set the scale

The focal training count table contained 1,674 measured training perturbations and was extremely zero-heavy: 1,205 targets had `n_degs = 0`, 276 had `n_degs = 1`, 90 had 2-10, and only 103/1,674 exceeded 10 DEGs. Because `Mpdz` is a scaffold/polarity gene rather than a transcriptional, proteasomal, or core RNA-processing factor, the bulk table argued for a low count unless close structural perturbations contradicted that.

The most relevant reachable scaffold, adhesion, and postsynaptic training perturbations were at the low edge in the exact `151` count table:

- `Ctnna2`, `Magi2`, `Shank2`, `Syngap1`, `Homer2`, `Nrxn2`, `Nrxn3`, and `Gria1`: 0 DEGs.
- `Ctnnd2`, `Dlg4`, `Nlgn3`, and `Nrxn1`: 1 DEG each, corresponding in the Parquet to the self-transcript only for the rows I inspected.
- `Shank3` and `Dlgap4`: 2 DEGs each.

Two nearby but mechanistically different boundary genes had much larger focal responses: `Grin1` had 89 DEGs and `Ctnnb1` had 383. Their corpus Findings described NMDAR-subunit or beta-catenin/Wnt thalamic programs, while the same corpus described `Dlg4` and `Magi2` as globally or pan-neuronally flat at the downstream snRNA level and `Shank3` as only a two-singleton response across the assayed groups. I therefore treated `Grin1` and `Ctnnb1` as proof that the `151` assay can respond, not as close quantitative analogs for MPDZ.

I also compared 16 selected training profiles in the focal class with signed Wilcoxon-score vectors. Across all 120 pairwise comparisons among those scaffold/receptor/catenin boundary nodes, mean top-tail overlap was low in both directions, 0.026 for positive tails and 0.033 for negative tails, and significant-program overlap had median 0.0. That supported the same interpretation as the count table and corpus: this local biology did not hide a shared high-DEG scaffold module that should override the low observed counts.

## Point synthesis

The exact `Mpdz` expression reach prevents treating the target as an expression-absent null. The installed-scaffold stock uncertainty and the fact that the strongest MPDZ mouse phenotypes are ventricular-barrier rather than thalamic NeuN-positive phenotypes argue against a large 151 thalamic survivor-state program. The closest task-matched structural perturbations usually produced zero or a single significant row, often only the perturbed transcript itself. I therefore predict the low nonzero edge of that distribution:

`Mpdz predicted_n_degs = 1`
