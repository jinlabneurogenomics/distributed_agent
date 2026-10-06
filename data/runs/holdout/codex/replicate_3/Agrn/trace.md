# Agrn direct n_degs forecast

## Declared target and endpoint

- Target: `Agrn`
- Focal population: `151 TH Prkcd Grin2c Glut`
- Endpoint: count of measured genes with Wilcoxon `pvals_adj < 0.05`
- Declared outcome status: the `Agrn` perturbation signature and its target DEG count were not used; the forecast used the one-row manifest, the `Agrn` biology-only bundle, the `151 TH Prkcd Grin2c Glut` training count table, and the declared all-cell-group training Parquet.

## Biology that sets the prior

The exact in-assay target measurement in `biology_bundles/Agrn.json` reports broad focal-cell expression: `Agrn` was detected in 23,534 of 23,679 non-target nuclei in `151 TH Prkcd Grin2c Glut` (`99.3876%`, mean `5.4917` CP10k). That makes target reach high in this class.

The same bundle also argues that realized protein loss should be partial rather than immediate and complete. Its curated functional-stock card describes AGRN as a multi-pool extracellular/transmembrane synaptic organizer; a P16 edit stops new supply but does not actively clear pre-existing membrane or extracellular matrix AGRN. The turnover evidence brackets different neuronal pools: transmembrane AGRN can drop within 3-7 days after knockdown, while aggregate AGRN in mature mouse cortical neurons had an estimated half-life near 23 days. At the P37-P44 harvest, 21-28 days after editing, the card therefore concludes `functional_stock_by_harvest = partially_depleted_or_leading_edge`.

That combination predicts that the CRISPR edit is present in the right nuclei but should resemble loss of a locally renewed synaptic/ECM signal more than a direct loss of a nuclear transcription factor or housekeeping complex. I therefore used the count table to prioritize training perturbations in the AGRN receptor / synaptic organizer / ECM neighborhood rather than the genome-wide high-DEG tail.

## Training measurements

The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` contains 1,674 training targets. Its empirical distribution is sparse:

- 1,205 / 1,674 training perturbations have `n_degs = 0`.
- The median is `0`; the 75th percentile is `1`.
- 1,481 / 1,674 are `<= 1`, 1,512 are `<= 2`, and 1,571 are `<= 10`.
- The large-count tail exists, but it is concentrated in broad nuclear or proteostasis regulators such as `Uba5` at 2,677, `Tpr` at 1,768, `Sin3a` at 1,433, and `Psmb4` at 742, not in the AGRN-like ECM/receptor class.

Counts for the most relevant training comparators in the same focal population were:

| training target | local rationale | n_degs |
|---|---:|---:|
| `Lrp4` | AGRN receptor / related effector in the curated AGRN biology card | 0 |
| `Musk` | LRP4-MuSK AGRN pathway partner | 0 |
| `Ror2` | AGRN-LRP4-ROR2 hippocampal signaling partner in the biology card | 0 |
| `Dag1` | AGRN-binding ECM receptor and DGC organizer | 0 |
| `Gpc6` | heparan-sulfate synaptic / ECM proteoglycan | 0 |
| `Nrxn1` | synaptic organizer with Dag1 comparison support | 1 |
| `App` | neuronal membrane/synaptic ligand-like comparator | 1 |

A slightly broader prefix-based synaptic/ECM panel was also quiet: `Nrxn2`, `Nrxn3`, `Nlgn3`, `Dlg4`, `Ncam1`, `Epha4`, many integrins, `Lrp1`, `Lrp5`, `Slit2`, and multiple `Ptpr*` genes were all either 0 or singleton self-transcript effects in this class. The main exception was `Rora` at 278 DEGs, but `Rora` is a nuclear receptor/transcription factor and not an AGRN operation analogue.

## Same-experiment corpus and profile check

The packaged Findings for these training targets are same-experiment semantic summaries, not independent replication, and support the same interpretation:

- `Dag1:F001` reports a global FDR-defined null for `Dag1`, with zero downstream genes in 22 measured cell groups.
- `Gpc6:F001` reports a pan-tested postnatal neuronal null surface for `Gpc6`.
- `Lrp4:F002` reports `Lrp4` as globally buffered, with only 1 of 371,796 downstream tests reaching FDR < 0.10 across the all-cell screen.
- `Musk:F002` reports that the sampled neuronal `Musk` response was uncoupled from the canonical agrin-LRP4-MuSK-Dok7-AChR module.
- `Ror2:F003` reports that `Ror2` did not engage the thalamic beta-catenin/TCF transcriptional module despite detectable `Ctnnb1` and `Lrp6` thalamic responses.

I then checked the declared training Parquet directly for `151 TH Prkcd Grin2c Glut`. `Lrp4`, `Musk`, `Ror2`, `Dag1`, and `Gpc6` each had all 17,259 measured genes present and zero `pvals_adj < 0.05` genes. `App`, `Nrxn1`, `Dlg4`, `Epha4`, `Ncam1`, and `Nlgn3` each had exactly one significant gene, always the self-transcript. `Lrp6` had four significant genes and `Ctnnb1` had 383, confirming that this class can show a Wnt-linked thalamic program when a central effector is perturbed but that AGRN-adjacent surface receptors did not trigger it.

A bounded `dataset.candidate_profile_review` comparison over `Lrp4`, `Musk`, `Ror2`, `Dag1`, `Gpc6`, `Nrxn1`, `App`, `Ncam1`, `Nlgn3`, `Dlg4`, `Epha4`, `Lrp6`, and `Ctnnb1` wrote `workbench/agrn_profile_compare.json` and was inspected through `workbench/agrn_profile_inspect.json`. The five closest AGRN-neighborhood analogues all had `response_activity_status = no_significant_features`. Their pairwise comparisons to the singleton self-transcript nodes had zero significant-feature intersections, and the broad `Ctnnb1` program had zero significant-feature intersections with the zero-count AGRN-neighborhood analogues by construction. No profile evidence suggested a hidden thalamic module around `Lrp4`, `Musk`, `Ror2`, `Dag1`, or `Gpc6`.

## Forecast synthesis

The upward evidence is real but limited: `Agrn` is expressed in almost every focal non-target nucleus, no close replacement gene is known, and some neuronal AGRN pools should lose new supply within the assay window.

The downward evidence is stronger for this endpoint: much of the installed extracellular/synaptic AGRN stock may persist to harvest; the best-matched receptor and ECM perturbations are exact nulls in this same cell class; broader synaptic adhesion perturbations are 0-1 events dominated by self-transcript loss; and central pathway effectors with large footprints are mechanistically too far downstream or too nuclear to transfer to Agrn. I therefore expect any Agrn effect in recovered thalamic nuclei to fall below the BH 0.05 cutoff rather than to create a multi-gene nuclear RNA program.

Point forecast: `0`.
