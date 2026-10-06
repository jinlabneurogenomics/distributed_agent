# Lmbr1 direct DEG-count forecast

Target: `Lmbr1`

Focal population: `151 TH Prkcd Grin2c Glut`

Endpoint: number of measured genes in the focal population with Wilcoxon BH-adjusted `p < 0.05`.

## Evidence Used

The declared holdout manifest contains the single target `Lmbr1`. `Lmbr1` is absent from the declared 1,674-row focal training count table, and the direct paralog named in the biology bundle, `Lmbr1l`, is also absent from that training table.

The canonical biology bundle shows measurable but modest `Lmbr1` transcript reach in the focal non-target nuclei: 8,203 of 23,679 cells expressing, 34.6425% expressing, mean CP10k 0.27536, mean log1p CP10k 0.19502, and pseudobulk CPM 28.7628. The exact expression reach establishes that the transcript was assayed in this population, but it does not establish editing efficiency or postnatal functional dependence.

The same bundle points to weak endpoint observability for this P16 neuronal coding perturbation:

- LMBR1 is an LMBR1-like multipass membrane protein encoded at a locus that also contains the intronic ZRS Shh enhancer, but the enhancer is a distinct regulatory element and cannot substitute for the protein's operative entity.
- The direct protein function in postmitotic thalamic neurons is unresolved.
- The available causal phenotypes are embryonic limb or systemic allele phenotypes, not a postnatal neural phenotype.
- No target-specific half-life, membrane-residence, or perturbation-to-stock-loss timing measurement was found, so functional stock at P37-P44 after a P16 edit is indeterminate.
- The card therefore discounts embryonic Shh/ZRS limb evidence, broad expression, and the related `Lmbr1l` gene for the kinetic decision.

Curated analog nomination against the actual focal training universe returned no training-available exact paralog, narrow-module member, direct interaction, dependency, or reciprocal corpus comparator for `Lmbr1`; all 824 available nominees were broad functional fallbacks from annotations such as embryonic limb or digit morphogenesis, transmembrane signaling receptor activity, signal transduction, membrane, plasma membrane, or receptor.

The declared focal count table is strongly zero-inflated:

- 1,205 / 1,674 training perturbations have `n_degs = 0`.
- The median is 0.
- The 75th percentile is 1.
- The 90th percentile is 2.
- The arithmetic mean is 14.05 only because of a small heavy tail, with 42 / 1,674 targets above 100 DEGs.

The broad fallback analogs did not justify moving upward from that zero-centered prior. Among the first 100 inspection-priority broad nominees, 85 had zero focal DEGs and the median was 0. Among the first 25 nominees, 20 had zero focal DEGs; the only very large value was `Ctnnb1` at 383, which reflects canonical Wnt/developmental signaling rather than a direct analogue for the poorly resolved LMBR1 protein product.

Because the Lmbr1 literature evidence is partly tied to the Shh/ZRS limb locus, I separately inspected available Shh-pathway training genes in the same focal count table. `Ptch1`, `Ptch2`, `Smo`, `Gli1`, and `Gli2` all had `n_degs = 0`.

Finally, I checked the declared expression Parquet for the leading broad nominees and these Shh-pathway genes under `group_name = "151 TH Prkcd Grin2c Glut"`. Each selected perturbation had focal rows, with the Parquet significant-row totals matching the count table; thus the zero counts above were measured contrasts in the focal population rather than missing entries.

## Synthesis

`Lmbr1` has enough focal transcript reach for an edit to be observable, but the biology bundle leaves the relevant P16-to-P37/P44 loss of LMBR1 protein function unresolved and gives no postnatal thalamic mechanism that would resemble the rare high-DEG training perturbations. The direct paralog is unavailable, the curated substitutes are only broad developmental or membrane annotations, and the closest Shh-pathway checks are all transcriptionally quiet in this assay.

I therefore treat the zero-inflated focal training distribution, the mostly zero broad nominees, and the all-zero Shh-pathway comparators as stronger quantitative bearings than the generic all-target mean. The most likely count is no BH-significant genes.

Predicted `n_degs`: 0
