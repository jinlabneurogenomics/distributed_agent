# Dlx5 prediction trace

## Question and resolved scope

The requested held-out target list contains a single gene, `Dlx5`. I interpreted the requested value as the number of measured genes with `pvals_adj < 0.05` after a `Dlx5` CRISPR loss-of-function perturbation in the `151 TH Prkcd Grin2c Glut` focal cell group. The value is a point prediction of the Perturb-seq DEG-count endpoint, not a prediction of embryonic phenotypic severity or whether a Dlx-family perturbation is biologically important in another tissue or developmental stage.

Two details shaped the call:

- The focal group is thalamic glutamatergic neurons. I did not interpret `TH` as dopaminergic tyrosine hydroxylase, and I did not transfer Dlx forebrain GABAergic expectations wholesale to this glutamatergic thalamic state.
- The perturbation is a sparse acute P16 AAV-CRISPR coding knockout read out 3-4 weeks later from recovered NeuN-positive nuclei. Embryonic germline `Dlx5`/`Dlx6` phenotypes and paired enhancer/locus perturbations are informative for target function, but they are imperfect analogs for this endpoint.

## Sources

- `training_de_all_cell_groups.parquet`, queried for the `151 TH Prkcd Grin2c Glut` rows and for the Dlx/ventral-forebrain comparator targets' Wilcoxon scores and BH-adjusted P values.
- `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`, used as the authoritative observed `n_degs` endpoint for non-held-out training targets.
- `057_Dlx5.csv`, used as the requested-target manifest. It contains exactly `Dlx5`.
- Distributed Agents same-experiment corpus `perturbai-july-260713-sourceguard-1773-v1`, used for packaged same-atlas interpretation around the observed `Dlx6` perturbation. The corpus had no direct `Dlx5` card, but it linked `Dlx6` with `Dlx3`, `Arx`, `Nkx2-1`, `Gad2`, `Mef2c`, `Meis2`, and related counterexamples through Dlx-family and forebrain GABAergic-pathway findings.
- PubMed literature:
  - Eisenstat et al., 1999, PMID 10516593, DOI `10.1002/(sici)1096-9861(19991115)414:2<217::aid-cne6>3.0.co;2-i`.
  - Poitras et al., 2007, PMID 17409112, DOI `10.1242/dev.02845`.
  - Wang et al., 2011, PMID 21452241, DOI `10.1002/cne.22618`.
  - Fazel Darbandi et al., 2016, PMID 27983964, DOI `10.1016/j.ydbio.2016.10.015`.
  - Le et al., 2017, PMID 28821666, DOI `10.1523/JNEUROSCI.2125-16.2017`.
  - Bond et al., 2009, PMID 19620975, DOI `10.1038/nn.2371`.

## Dataset operations

The full parquet is large, so I filtered to `group_name == "151 TH Prkcd Grin2c Glut"` and used the training-count CSV for exact FDR DEG counts. I then inspected biologically chosen analogs and counterexamples rather than assigning `Dlx5` from a global average:

1. Read the requested manifest and confirmed that only `Dlx5` had to be predicted.
2. Read the focal training-count CSV and pulled Dlx-family, homeobox, and developmental transcription-factor counts.
3. Queried the focal parquet rows for the best represented analogs: `Dlx6`, `Dlx3`, `Arx`, `Gad2`, `Nkx2-1`, `Six3`, `Meis2`, `Pax6`, `Foxp2`, and `Mef2c`.
4. Compared the complete signed-Wilcoxon profiles for `Dlx6`, `Dlx3`, `Arx`, `Nkx2-1`, `Meis2`, `Pax6`, `Foxp2`, and `Mef2c` inside the `151` group with the Distributed Agents runtime. This used all 17,259 measured focal genes per target, Pearson/Spearman/cosine over signed scores, and top-tail overlap to test for a weak but coherent Dlx-like profile hidden under the FDR threshold.
5. Checked specific Dlx/GABAergic marker readouts, including `Dlx5`, `Dlx6`, `Gad1`, `Gad2`, `Slc32a1`, `Pvalb`, `Sst`, `Arx`, `Lhx6`, `Nkx2-1`, `Meis2`, and `Pax6`, under the observed Dlx-pathway comparators.

## Target-specific reasoning

### `Dlx5`

`Dlx5` is not present in either training input as a perturbation target, so the closest direct within-dataset analog is `Dlx6`: it is the adjacent Dlx5/Dlx6 bigene-cluster paralog represented in the screen. In the focal `151 TH Prkcd Grin2c Glut` group, `Dlx6` had `n_degs = 0`; every row had `pvals_adj >= 0.05`, with the best rows still adjusted to 1.0. The top signed features under `Dlx6` were small, nonsignificant score excursions, for example `Ruvbl1` score 3.42 and `Nbas` score -3.78, both with `pvals_adj = 1.0`. The biologically expected marker rows were also flat under `Dlx6`: `Dlx5` score -0.107, `Gad1` 0.657, `Gad2` 0.289, `Slc32a1` 0.322, `Lhx6` -0.066, and all had `pvals_adj = 1.0`.

The same-family counterexample `Dlx3` was also null in the focal group (`n_degs = 0`, minimum adjusted P value 1.0). `Dlx3` is a weak Dlx5 analog because its canonical functions are outside the forebrain GABAergic Dlx1/2/5/6 axis, but it helps reject a generic Dlx-homeobox transcriptional footprint. The strongest literature-adjacent ventral-forebrain and homeobox comparators likewise argued for an off-window state in this focal group: `Arx = 0`, `Gad2 = 0`, `Nkx2-1 = 0`, `Six3 = 0`, `Meis2 = 0`, `Pax6 = 0`, and `Foxp2 = 0` DEGs in the training-count CSV. `Mef2c` had only one focal DEG, its own target transcript, so even a detectable neural transcription-factor perturbation did not produce a broad Dlx/GABAergic module in these thalamic glutamatergic cells.

The profile comparison confirmed that this was not a weak, coherent subthreshold Dlx-like state. `Dlx6` was classified as `no_significant_features`, and its whole-profile correlations to mechanistic comparators were essentially null: Pearson -0.004 with `Dlx3`, -0.001 with `Arx`, -0.003 with `Nkx2-1`, 0.084 with `Meis2`, 0.006 with `Pax6`, 0.017 with `Foxp2`, and 0.049 with `Mef2c`. Top-tail overlaps were correspondingly tiny, only 1.5-6% for the positive tail and 1-5.5% for the negative tail. None of the comparators shared a significant positive or negative feature with `Dlx6` because `Dlx6` had no significant focal features.

The external biology explains why `Dlx5` can be developmentally important yet predicted null here. Eisenstat et al. showed that Dlx genes mark embryonic basal forebrain differentiation, with `Dlx2`, then `Dlx1`, then `Dlx5`/`Dlx6` expressed in differentiating ventral forebrain cells. Poitras et al. described the combined `Dlx1`, `Dlx2`, `Dlx5`, and `Dlx6` program as required for GABAergic interneurons born in ventral telencephalic proliferative zones and migrating to cortex, hippocampus, and olfactory bulb. Le et al. placed the GABA synthesis genes `Gad1` and `Gad2` downstream of Dlx homeobox factors, and Fazel Darbandi et al. showed that deleting the embryonic I56ii enhancer at the `Dlx5`/`Dlx6` locus impairs developing forebrain Dlx/GABAergic patterning. Bond et al. likewise tied the Evf2 noncoding RNA/Dlx5-Dlx6 locus to embryonic GABA circuitry. Those are strong developmental priors, but they point to embryonic ventral telencephalic GABAergic specification, enhancer dosage, and paired Dlx regulation, not an autonomous P16-to-P37 response in thalamic glutamatergic neurons. Consistent with that, Wang et al. found that a `Dlx6` coding mutant affected striatal and central amygdala molecular properties but did not produce major E18.5 striatal array-level expression changes.

I therefore treat `Dlx6` as the primary dataset analog for `Dlx5` and the broader `Arx`/`Nkx2-1`/`Gad2`/`Meis2` set as boundary evidence. The zero/nonzero decision is driven mainly by the within-dataset Dlx6 and Dlx-pathway nulls; the literature explains that the apparent conflict with strong DLX biology is an assay-window and cell-type mismatch. I predict that `Dlx5` will have no FDR-significant genes in the focal group.

Predicted `n_degs`: `0`.

## Limits and extrapolations

- The exact same-gene perturbation, `Dlx5`, is held out. The prediction extrapolates from `Dlx6` and pathway neighbors rather than from an observed `Dlx5` signature.
- `Dlx6` is the best coding paralog in the dataset, but the embryonic forebrain literature often involves `Dlx1`/`Dlx2`, paired `Dlx5`/`Dlx6` regulation, or enhancer deletion. A single sparse P16 `Dlx5` cut could, in principle, diverge from single `Dlx6`.
- The focal group is thalamic and glutamatergic; absence of a focal DEG response should not be read as a general null for `Dlx5` in embryonic ventral telencephalic GABAergic progenitors, neural crest, skull, or limb development.
- Several comparator signatures had only 138-294 matched perturbed nuclei in the focal group, so small true effects could remain below BH FDR 0.05. The requested endpoint is exactly this powered FDR count, so the prediction is a visible-DEG prediction rather than a claim of zero molecular consequence.
