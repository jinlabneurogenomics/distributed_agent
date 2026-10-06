# Nrl direct DEG-count forecast

## Target and endpoint

- Manifest target: `Nrl`.
- Endpoint: `n_degs` in `151 TH Prkcd Grin2c Glut`, defined as the number of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`.
- Training endpoint source: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Matched DE source for spot checks: `[local file: training_de_all_cell_groups.parquet]`.
- Held-out biology source: `[local file: Nrl.json]`, canonical bundle SHA256 `34676d2c625895bd270d9de8310f607ed0a9854dc3b9492e410bf5f710d4dec7`.

## Evidence used

The `Nrl` perturbation resolves to the `Lcn2` locus.  The biology bundle describes LCN2 as a secreted siderophore-binding lipocalin with possible postnatal neural phenotypes outside the assayed thalamic context, and adjudicates its functional stock as likely substantially depleted by the P37-P44 harvest if the edited cell had been producing it.  That supports target engagement at the level of newly synthesized product, but it does not by itself imply a basal cell-autonomous thalamic transcriptional response.

The exact in-assay reach argues strongly downward for this focal population:

- In non-targeting `151 TH Prkcd Grin2c Glut` nuclei, only 4 of 23,679 cells had any `Nrl` RNA.
- The expressing fraction was `0.01689260526204654%`.
- The whole population had only 4 total target UMIs, mean raw UMI `0.0001689260526204654`, mean CP10K `0.0000979168601166287`, and pseudobulk CPM `0.010587194750364893`.

Thus the source product can plausibly turn over within 21-28 days, but the assayed healthy thalamic neuronal population had almost no detectable basal Lcn2 transcript to remove.  The likely limiting factor is context/reach rather than stale protein.

The declared `151 TH Prkcd Grin2c Glut` training count table is extremely zero-inflated:

- 1,674 held-in perturbations.
- 1,205 had `n_degs = 0`.
- 1,481 had `n_degs <= 1`.
- Median `n_degs = 0`; 90th percentile `= 2`; 95th percentile `= 18`.

I treated the relevant training analogues as unstimulated innate, complement, TLR, NF-kB, IRF, and inflammatory receptor/pathway perturbations that would expose a basal neuronal inflammatory module if one were active.  All of the following had `n_degs = 0` in the focal count table, and a direct Parquet check found zero `pvals_adj < 0.05` genes for each in `151 TH Prkcd Grin2c Glut`: `Ager`, `C3`, `Cd14`, `Cd36`, `Cd46`, `Tlr2`, `Tlr3`, `Tlr4`, `Tlr5`, `Tlr7`, `Tlr8`, `Nfkb1`, `Rel`, `Chuk`, `Irf3`, `Traf3`, `Map3k7`, and `Il1r1`.

Same-experiment corpus Finding `Tlr4:F001` reports that acute `Tlr4` loss was pan-neuronally null across recovered NeuN-positive cell groups, and Findings `Tlr4:F002`-`Tlr4:F003` report absence of the expected basal TLR4 to NF-kB/IRF output and lack of convergence across represented TLR-family and NF-kB/IRF relatives.  Those Findings are semantic summaries of the same Perturb-seq experiment, not independent replication, but they support interpreting the zero counts as a broader off-state innate-inflammatory axis in unstimulated juvenile neurons rather than as a one-gene anomaly.

## Synthesis

The upward evidence is that LCN2 is a real secreted protein with postnatal neural phenotypes elsewhere and little reason for a pre-edit intracellular stock to persist for a month.  The downward evidence is more directly matched to this endpoint: Lcn2/Nrl RNA was essentially absent in the exact thalamic non-target nuclei, the assay excludes glial/immune/vascular compartments where lipocalin and innate-inflammatory biology are most likely to be active, and the represented basal innate-inflammatory perturbations were uniformly null in the same high-yield class.

On that balance, the most likely integer count is exactly zero rather than a small positive response.

Predicted `n_degs`: `0`
