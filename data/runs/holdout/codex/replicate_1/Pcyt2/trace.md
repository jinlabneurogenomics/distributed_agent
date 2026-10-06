# Pcyt2 DEG-count forecast

## Target and endpoint

- Target: `Pcyt2`
- Focal population: `151 TH Prkcd Grin2c Glut`
- Endpoint: number of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`
- Point forecast: `6`

## Evidence used

The one-row manifest names `Pcyt2`, and `Pcyt2` is absent from the declared focal training count table, so the target count itself was not used.

The exact focal non-target expression card supports target reach in this population: `Pcyt2` was detected in 20,185 of 23,679 matched non-target nuclei, with 85.24% of cells expressing, mean raw UMI 2.44, mean CP10K 1.51, and pseudobulk 152.7 CPM. This supports enough baseline expression for a perturbation to be realized in thalamic glutamatergic neurons, while not saying anything about editing efficiency or the withheld response.

The functional-stock card puts the P16 edit in an intermediate timing regime. `Pcyt2` is the ethanolamine-phosphate cytidylyltransferase for new CDP-ethanolamine pathway phosphatidylethanolamine and ether-PE synthesis, and synaptic PE turns over on a several-day scale, so some Pcyt2-dependent membrane supply should be stressed by the P37-P44 harvest. At the same time, the perturbation does not remove pre-existing enzyme or pre-installed PE directly, target-protein clearance is unknown, slower lipid pools can persist over most of the assay window, and the mitochondrial `Pisd` route can supply some PE. I therefore treated `Pcyt2` as biologically real and probably assay-reachable, but not as an acute core-machinery lesion expected to produce hundreds of DEGs.

Among the source-card pathway genes `Pcyt1a`, `Pcyt1b`, `Pisd`, and `Selenoi`, only `Selenoi` was present in the focal training count table. Its observed focal count was 5 DEGs. The exact Parquet rows for `Selenoi` in `151 TH Prkcd Grin2c Glut` had typical sampling depth, 172 perturbed nuclei versus the training median of 177, and the five FDR-significant genes were `Insig1`, `Msmo1`, `Selenoi`, `Fdft1`, and `Nos1ap`. That profile is a narrow sterol/lipid-homeostasis response with direct self-transcript loss, not a broad stress or identity program.

For scale, the whole focal training table had 1,674 perturbations, median 0 DEGs, 75th percentile 1, 90th percentile 2, 95th percentile 18, and a very sparse high-count tail. `Selenoi`'s count of 5 already lands above 92% of training perturbations, but it is far below the recurrent high-burden RNA-processing, proteasome, and transcriptional-regulator examples.

## Synthesis

I centered the forecast on the one observed same-pathway comparator, then nudged slightly upward from `Selenoi` because `Pcyt2` is the upstream regulatory cytidylyltransferase and is broadly expressed in the focal cells. I kept the point in the same low single-digit regime because the best target-specific biology predicts only partial acute depletion by harvest, with residual enzyme, retained membrane lipid, and `Pisd`-dependent bypass as strong dampers.

Predicted `n_degs`: `6`
