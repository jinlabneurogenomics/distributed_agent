# Vapb direct n_degs forecast

## Target and endpoint

- Target: `Vapb`
- Cell population: `151 TH Prkcd Grin2c Glut`
- Endpoint: number of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`
- Training count source: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- Training profile source: `[local file: training_de_all_cell_groups.parquet]`
- Target biology source: `[local file: Vapb.json]`

The `Vapb` target is absent from the 1,674-row training count table, so its held-out DEG count was not used. The profile analysis below used only observed training targets and the matched `151 TH Prkcd Grin2c Glut` Parquet rows.

## Target biology used

The target-biology bundle reports strong in-assay focal-population reach: `Vapb` was detected in 18,327 of 23,679 matched non-target nuclei in `151 TH Prkcd Grin2c Glut` cells, with 77.40% of nuclei expressing the transcript, mean raw UMI 1.73, mean log1p CP10K 0.638, and pseudobulk 108.57 CPM. This supports perturbability in the assayed population but was not treated as editing efficiency.

The same bundle adjudicates VAPB as a renewable ER membrane adaptor rather than a long-lived preinstalled structure. Its functional-stock conclusion is `likely_substantially_depleted` by P37-P44 because the P16 edit stops new VAPB supply and the available target-specific chase gives wild-type VAPB a roughly 17-hour half-time, far shorter than the 21-28 day editing window.

The biological phenotype prior is real but not transcriptionally broad by itself. Vapb-null ventrobasal thalamic neurons have reduced native HCN/Ih current, directly placing the gene in a relevant thalamic neuronal context, while single Vapb loss is buffered by overlapping Vapa and constitutive Vapb knockout mice have mild long-latency motor phenotypes. I therefore treated Vapb as more likely to be measurable than an unexpressed target, but closer to channel/ER-contact-site perturbations than to high-burden spliceosome, proteasome, or global transcriptional regulators.

## Training measurements used

The full `151 TH Prkcd Grin2c Glut` training table is highly sparse: median `n_degs` is 0, mean is 14.05, 72.0% of training targets have 0 DEGs, 93.7% have fewer than 10, and only 2.6% have at least 100. This made a high count inappropriate without a close high-burden analogue.

I selected training targets by functional relation to VAPB's ER adaptor, membrane-contact-site, HCN/channel-trafficking, SNARE/vesicle, and ER/endolysosomal biology, then compared their exact focal-population profiles. Their measured counts were:

| Target | `n_degs` |
|---|---:|
| `Cert1` | 0 |
| `Hcn1` | 0 |
| `Hcn2` | 1 |
| `Vcp` | 2 |
| `Vps13a` | 0 |
| `Vps13b` | 0 |
| `Vps13c` | 0 |
| `Vps35` | 17 |
| `Vps54` | 31 |
| `Vps41` | 0 |
| `Vps53` | 0 |
| `Atg5` | 0 |
| `Atg16l1` | 0 |
| `Dnajc5` | 1 |
| `Stx16` | 1 |
| `Stx1b` | 0 |
| `Stx5a` | 0 |
| `Stxbp1` | 1 |
| `Vamp1` | 1 |
| `Sec23a` | 0 |
| `Sec63` | 11 |
| `Tomm40` | 1 |
| `Rab18` | 0 |
| `Rab27a` | 0 |
| `Rab3gap1` | 0 |
| `Rab3gap2` | 0 |
| `Kif5a` | 1 |
| `Spast` | 0 |
| `App` | 1 |
| `Grn` | 1 |

Across these 30 biologically chosen observed profiles, the median count was 0; 17 had no significant genes, 10 had 1-9, and only `Sec63`, `Vps35`, and `Vps54` reached 10-49. The profile comparison in `./vapb_training_profile_compare.json` reproduced the same low-activity structure: 17 profiles had no significant features, 10 had 1-9 significant features, and 3 had 10-49.

## Synthesis

The direct VAPB operations point to CERT/FFAT lipid-contact-site biology and HCN-channel trafficking, whose assayed perturbation anchors were `Cert1` = 0, `Hcn1` = 0, and `Hcn2` = 1. Broader ER or vesicle targets that produced 11-31 DEGs were retained as an upper-tail possibility, but they perturb core ER translocation or endosomal sorting more directly than loss of the VAPB adaptor. VAPB expression and stock depletion argue against assigning a pure null prior, while the sparse direct anchors and partial VAPA buffering argue against a multi-dozen-gene response.

Point prediction: `Vapb` produces a minimal but detectable transcriptional footprint in `151 TH Prkcd Grin2c Glut`, so the forecast is 1 DEG.
