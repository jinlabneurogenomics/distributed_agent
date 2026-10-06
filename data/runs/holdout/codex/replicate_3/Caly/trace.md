# Caly n_degs forecast

Endpoint: `n_degs` in `151 TH Prkcd Grin2c Glut`, defined as the number of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`.

Prediction: **2**

## Allowed target evidence

- The one-row manifest target is `Caly`.
- The canonical `Caly` biology bundle exposed exact focal-population reach but not the held-out DE signature or count. In matched non-target nuclei from `151 TH Prkcd Grin2c Glut`, `Caly` was detected in 20,881/23,679 nuclei, or 88.18%, with mean 2.81 raw UMI, mean log1p CP10k 0.907, and pseudobulk CPM 176.1.
- The source card places calcyon on vesicular/endosomal traffic: a neuronal single-pass membrane protein that binds clathrin light chain and promotes clathrin-mediated endocytosis/cargo sorting. Germline/null evidence supports neuronal function through activity-dependent AMPA-receptor internalization, CA1 LTD, and NRG1/ErbB4-linked GABA transmission.
- The same bundle judged `functional_stock_by_harvest` indeterminate. A P16 disruptive edit should stop new calcyon synthesis, but already embedded vesicular calcyon is not directly disabled, and no Caly-specific protein half-life or acute loss-to-clearance time course established how much stock is gone after the 21-28 day screen window.

## Training endpoint scale

I used `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]` as the direct count table. It contains 1,674 training perturbations:

- 1,205/1,674 have `n_degs = 0`;
- 276 have exactly 1 DEG;
- 193 have at least 2 DEGs;
- 132 have at least 5 DEGs;
- 59 have at least 50 DEGs;
- the median is 0 and the mean is 14.05, reflecting a very sparse distribution with a long high-response tail.

The closest assayed family members named by the Caly card, `Nsg1` and `Nsg2`, were not present in this training count table, so the usable local comparators were more distant endocytic, adaptor, cargo, receptor, and endolysosomal perturbations.

## Comparator counts used

Low receptor/cargo and clathrin-adjacent anchors in the `151` count table:

| target | n_degs |
| --- | ---: |
| Ap3b1 | 0 |
| Erbb4 | 0 |
| Gria1 | 0 |
| Gria2 | 0 |
| Nrg1 | 0 |
| Ap1b1 | 1 |
| Dnm1 | 1 |
| Synj1 | 1 |
| Cltc | 3 |

More central endolysosomal/retrograde trafficking anchors in the same count table:

| target | n_degs |
| --- | ---: |
| Vps35 | 17 |
| Vps54 | 31 |
| Rab7 | 501 |

Packaged same-experiment Findings for these training perturbations were consistent with that split: `Ap3b1`, `Dnm1`, `Nrg1`, `Erbb4`, `Gria1`, and `Gria2` were interpreted as largely or broadly transcriptionally buffered; `Cltc` had a selective coated-vesicle secondary response; `Vps35` and `Vps54` had restricted `151` responses; and `Rab7` induced a much broader late-endosomal/lysosomal, lipid, ISR/UPR, autophagy, and redox/apoptotic stress program.

## Profile evidence from the declared parquet

I compared the 12 selected training profiles in the declared DE parquet, filtered to `group_name == "151 TH Prkcd Grin2c Glut"` and using `logfoldchanges` with `pvals_adj < 0.05` as the significance flag. All 12 profiles were available. The cohort contained five no-response nodes, four 1-9 DEG nodes, two 10-49 DEG nodes, and only one `>=50` node, `Rab7`.

The pairwise profile inspection supported treating `Rab7` as a loose upper-bound biology state, not as a numeric analog for Caly:

- `Cltc`, the most direct represented clathrin anchor, shared no FDR-significant `151` genes with `Vps35` or `Vps54`.
- `Vps35` and `Rab7` shared only 7 significant genes in the same direction, with 2 significant direction conflicts, despite both acting in late endosome/retrograde traffic.
- `Vps54` and `Rab7` shared 13 significant genes, whereas corpus Finding summaries noted that `Rab7` extends into lysosomal, sterol, autophagy, PERK, and apoptosis genes absent after `Vps54` perturbation.
- The cohort showed weak overlap among positive tails overall: across all 66 selected pairs, the mean positive top-tail overlap coefficient was 0.0665.

## Synthesis

The exact in-assay expression makes failed context reach unlikely for `Caly`: most recovered `151` nuclei express the transcript. The mouse null literature also argues that Caly is not functionally silent once calcyon is absent.

I nevertheless downweighted the high endolysosomal anchors. `Rab7` loss is a central late-endosome failure with a broad catabolic stress response, while `Vps35` and `Vps54` perturb retromer/GARP machinery with much more direct effects on receptor, retrograde, and degradative traffic. Calcyon is a cargo-selective accessory component: the card explicitly notes preserved basal AMPA surface levels/recycling in tested systems, unresolved turnover by harvest, and related NEEP21-family proteins with overlapping neuronal trafficking biology. Those facts put Caly nearer the quiet clathrin, AP, AMPAR, neuregulin, and synaptic-vesicle anchors than the high `Rab7` state.

Balancing strong `151` target reach and a real but cargo-selective neuronal operation against the low observed counts for the most direct training anchors, I forecast a small nonzero response, closest to `Cltc`/`Dnm1`/`Synj1`/`Ap1b1` and well below `Vps35`/`Vps54`.
