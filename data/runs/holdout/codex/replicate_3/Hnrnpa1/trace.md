# Hnrnpa1 direct forecast

## Target and declared endpoint

- Target: `Hnrnpa1`
- Cell group: `151 TH Prkcd Grin2c Glut`
- Endpoint: number of measured genes with BH-adjusted Wilcoxon `p < 0.05`

The forecast used the declared biology bundle for `Hnrnpa1`, the declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` training counts, the declared `training_de_all_cell_groups.parquet` for same-cell profile comparisons among training perturbations, curated gene memberships from `gene-annotation-skill`, and same-experiment corpus context for training perturbations only. I did not inspect a measured `Hnrnpa1` perturbation signature or target count.

## Biology bearing

The canonical `Hnrnpa1` bundle supports an observable postnatal effect but with only partial context match:

- The target transcript is present in the focal population: 11,396 of 23,679 non-target `151 TH Prkcd Grin2c Glut` nuclei expressed `Hnrnpa1` in the exact reach table, with 48.13% expression, mean raw UMI 0.706, and pseudobulk CPM 44.22.
- hnRNP A1 is a dynamic nuclear/cytoplasmic pre-mRNA-binding RNP component involved in splice-site selection and mRNA export, not a long-lived preinstalled structure.
- Functional stock should be mostly depleted over the 21-28 day P16-to-P37/P44 screen window if editing prevents new productive protein synthesis: the bundle cites a 5.27 day rat cortical-neuron Hnrnpa1 half-life, corresponding to roughly four to five half-lives by harvest.
- Published mouse-neuron perturbation evidence showed splicing plus dendritic/synaptic abnormalities by 14 days, but in primary cortical culture and partly with combined A1/A2 loss, so the evidence transfers imperfectly to postnatal thalamic neurons.
- Embryonic Hnrnpa1-null mice are severe and the bundle records incomplete compensation by `Hnrnpa2b1` in that context, which argues against treating `Hnrnpa1` as fully buffered. That evidence is non-neural and embryonic, so I used it only to move the forecast above the very weak `Hnrnpa2b1` anchor.

## Training measurements that set the scale

The focal training count table is sparse overall:

- 1,674 training perturbations
- median 0 DEGs
- 75th percentile 1 DEG
- 90th percentile 2 DEGs
- 95th percentile 18 DEGs
- 99th percentile 430 DEGs

`Hnrnpa1` is not a generic target: curated membership places it in `GO:0000398` mRNA splicing via spliceosome, `GO:0000380` alternative mRNA splicing via spliceosome, KEGG spliceosome, Reactome mRNA splicing, WikiPathways mRNA processing, and the `rna_binding` functional class. The exact training members in these RNA-processing groups span a wide range:

- Closest measured hnRNP-family anchors in `151`: `Hnrnpa2b1` 11, `Hnrnpc` 122, `Hnrnpu` 733, `Hnrnph2` 4, `Hnrnpdl` 1
- Broader compact RBP anchor: `Tardbp` 210
- Core spliceosome or spliceosome-adjacent perturbations: `Snrnp70` 213, `Prpf6` 454, `Cdc40` 624, `U2af2` 828, `Rnpc3` 868
- WikiPathways mRNA-processing targets had median 1 but a high tail dominated by the core spliceosome/RBP genes above
- `GO:0000398` mRNA-splicing targets in the training table had 10/13 nonzero responses, median 11, and a mean of 240.85

Same-cell profile comparison on the declared Parquet confirmed that these counts are not one exchangeable RNA-processing module. `Hnrnpa2b1` had 11 significant features and near-zero whole-profile cosine to core spliceosome factors: about 0.036 to `U2af2`, 0.033 to `Rnpc3`, 0.057 to `Prpf6`, and 0.058 to `Snrnp70`. `Hnrnpc` was a 122-DEG, weaker hnRNP branch whose strongest selected cosine was to `Prpf6` at 0.106, while `Hnrnpu` was a much broader 733-DEG state with higher cosines to `Prpf6`, `U2af2`, and `Snrnp70` around 0.22-0.24. `Tardbp` sat between them with 210 DEGs and moderate profile overlap to splicing perturbations.

Packaged corpus Findings for these training perturbations matched that quantitative picture: `Hnrnpa2b1` was explicitly weaker than `Hnrnpu`, `Tardbp`, `Matr3`, and `Hnrnpc`; `Hnrnpc` was spliceosome-adjacent but weaker and restricted relative to core spliceosome factors; and `Hnrnpu` carried broad RNA-processing plus chromatin/proteostasis programs.

## Forecast

I placed `Hnrnpa1` above `Hnrnpa2b1` because the focal population expresses it, the functional pool should turn over within the experiment, and the source bundle argues that `Hnrnpa2b1` is not guaranteed to compensate for A1 loss. I placed it below `Hnrnpc`, `Tardbp`, `Hnrnpu`, and the high core-spliceosome factors because `Hnrnpa1` is a dynamic hnRNP branch rather than a U2AF/core snRNP factor or an `Hnrnpu`-like chromatin-scaffold perturbation, and the observed hnRNP perturbations are highly non-interchangeable.

The resulting point estimate is a moderate response near the `Hnrnpc` scale but slightly lower:

`predicted_n_degs = 96`
