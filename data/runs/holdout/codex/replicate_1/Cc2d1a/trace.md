# Cc2d1a DEG-count forecast

## Target and endpoint

The requested target is `Cc2d1a` in `151 TH Prkcd Grin2c Glut`.  The endpoint is the count of measured genes in that focal population with BH-adjusted Wilcoxon `pvals_adj < 0.05`.

The declared focal-class training table contains 1,674 observed targets and the declared all-cell-group Parquet contains no `gene_target = Cc2d1a` rows, so this forecast did not use a `Cc2d1a` expression signature or endpoint count.

## Biology bearing

The declared `Cc2d1a` biology bundle supports target realization but not a large, class-wide RNA effect:

- Exact in-assay focal expression is moderate: `Cc2d1a` is detected in 12,152 of 23,679 matched non-target `151 TH Prkcd Grin2c Glut` nuclei, or 51.32%, with mean CP10k 0.494.
- The functional-stock card calls the operative CC2D1A protein pool `likely_substantially_depleted` by the P37-P44 harvest because the perturbation stops new production of a dynamic scaffold/regulator and adult AAV-Cre deletion removed detectable CC2D1A protein by three weeks.
- The observability card supports a postnatal neuronal consequence in other mouse neural contexts, but the strongest phenotype evidence is forebrain or hippocampal rather than juvenile thalamus, and no quantitative thalamic protein half-life was known.
- CC2D1A directly binds and regulates CHMP4B/ESCRT-III, but its paralog `Cc2d1b` and its scaffold-like rather than core-subunit operation make a full late-endosome failure program uncertain.

## Training measurements used

The count table for `151 TH Prkcd Grin2c Glut` is sparse.  Of 1,674 training targets, 1,205 have 0 DEGs, 276 have 1 DEG, 31 have 2 DEGs, 34 have 3-5 DEGs, 62 have 6-25 DEGs, and only 66 have more than 25 DEGs.  The median is 0, the 75th percentile is 1, the 90th percentile is 2, and the 95th percentile is 18, with the mean inflated to 14.05 by a small set of very broad responders.

The most direct training comparator was `Chmp4b`, the only exact CC2D1A/ESCRT-III cue from the bundle present in the training count table.  `Chmp4b` has 0 DEGs in the requested focal class, and direct inspection of the matched Parquet also found 0 genes with `pvals_adj < 0.05` among its 17,259 focal rows.  A focal profile-neighborhood scan of `Chmp4b` against all 1,674 eligible observed training targets likewise classified `Chmp4b` as having no significant positive or negative program.  Its leading whole-profile neighbors were mostly zero-count targets: `Oprk1` 0, `Adam22` 1, `Appl1` 0, `Alx1` 0, `Gal` 0, `Cyld` 0, `Lrp6` 4, `Pi4kb` 1, `Pcsk2` 1, and `Depdc5` 13.

The same-experiment corpus made the same boundary biologically interpretable without serving as an independent measurement: the `Chmp4b` report found only one corrected downstream change anywhere in the atlas, in another neuronal class, and concluded that `Chmp4b` did not produce a robust recurrent ESCRT, autophagy, or cargo-turnover signature.  Conversely, the broader late-endosome control `Rab7` is a 501-DEG high outlier in this focal class with a lysosomal/sterol compensation program; related or report-listed cargo/autophagy comparators near `Chmp4b` were mostly quiet here (`Atg5` 0, `Becn1` 0, `Sqstm1` 1, `Spast` 0, `Atp6v1a` 0, `Atp6v1e1` 0, `Vps41` 0), with `Vps35` 17 and `Grin1` 89 marking broader upper-bound states rather than same-scale CC2D1A analogs.

## Synthesis

I put most weight on the direct-local bracket.  `Cc2d1a` should be functionally depleted in edited, target-expressing neurons by harvest and has postnatal neuronal phenotypes, so an exact zero is not forced.  But its focal transcript reach is only moderate across the aggregated thalamic class, the direct `Chmp4b` perturbation is flat in `151 TH Prkcd Grin2c Glut`, and the same training data show that many ESCRT/autophagy/cargo-adjacent perturbations are 0- or 1-DEG events rather than `Rab7`-scale lysosomal stress states.

The point forecast is therefore at the first nonzero count, `1`: slightly above the modal null because the CC2D1A card supports realized postnatal neuronal loss, but still within the bottom quartile of observed focal-class training responses because the task-matched direct comparator and its measured neighborhood argue for only an isolated recovered-nucleus transcriptional effect.
