# Trace

Target: `Tubb3` in `151 TH Prkcd Grin2c Glut`.

## Evidence used

- The holdout manifest contains a single target, `Tubb3`.
- The declared biology bundle places `Tubb3` well within reach of the focal population: the `Tubb3` transcript was detected in 23,097 / 23,679 non-target nuclei from `151 TH Prkcd Grin2c Glut` and averaged 7.31 raw UMIs per nucleus.
- The same bundle characterizes TUBB3 as a neuronal beta-tubulin structural subunit. A disruptive edit should stop new functional TUBB3 supply, but it does not poison already incorporated tubulin; operative microtubules are mixed beta-tubulin pools, and other beta-tubulin isotypes compensated for germline Tubb3 loss well enough to preserve adult mouse brain pan-beta-tubulin and baseline nervous-system phenotypes. Total brain tubulin turnover is days to weeks, so some TUBB3 replacement should occur by the 21-28 day harvest while leaving strong paralog buffering plausible.
- The declared `151 TH Prkcd Grin2c Glut` training count table is mostly silent: among 1,674 measured training targets, 1,205 had `n_degs = 0`, the median was 0, the 75th percentile was 1, and only 132 targets reached at least 5 DEGs.
- The closest measured beta/alpha-tubulin perturbations were low-yield in the same table: `Tubb4b = 1`, `Tubb5 = 1`, `Tuba4a = 2`, and `Tuba1a = 7`. Other microtubule structural or motor-adjacent targets were similarly small in this class (`Map1b = 1`, `Mapt = 1`, `Map6 = 0`, `Mapre2 = 1`, `Stmn2 = 1`, `Kif5a = 1`, `Kif5c = 1`), whereas the larger `Dctn1 = 75` sterol response was a dynein-dynactin transport outlier rather than a generic tubulin-like signature.
- Direct Parquet rows for the matched tubulin analogs confirmed that `Tubb4b` and `Tubb5` each had exactly one FDR<0.05 gene in `151 TH Prkcd Grin2c Glut`, and that gene was the perturbed transcript itself. `Tuba1a` was the main exception, with seven FDR<0.05 genes: down-regulation of `Tuba1a` plus up-regulation of several tubulin paralogs including `Tubb3`.
- The packaged same-experiment corpus summarized the same beta-tubulin boundary: `Tubb4b` and `Tubb5` were buffered beta-tubulin losses without a broad postnatal nuclear-RNA program, while the restricted tubulin-paralog mRNA feedback was `Tuba1a`-specific among the represented tubulin and microtubule-related perturbations.

## Synthesis

I treated the count-table background as a strong prior for a zero-or-one outcome and used the beta-tubulin analogs to choose between them. `Tubb3` is highly expressed in the assayed thalamic population, so a self-transcript Wilcoxon call is more plausible than a complete statistical null if the edit destabilizes edited `Tubb3` mRNA. At the same time, the biology card and measured analogs argue against a broad downstream program: beta-tubulin loss can be buffered at the operative microtubule level, and direct `Tubb4b`/`Tubb5` loss produced self-only signatures rather than the multi-paralog compensation seen after alpha-tubulin `Tuba1a` loss.

My point prediction is therefore a self-only response:

`predicted_n_degs = 1`
