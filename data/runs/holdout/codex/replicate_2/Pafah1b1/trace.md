# Pafah1b1 n_degs forecast

Target: Pafah1b1

Cell class: 151 TH Prkcd Grin2c Glut

Predicted `n_degs`: 12

## Evidence used

- The holdout manifest contains one target, `Pafah1b1`. The endpoint is the count of measured genes in `151 TH Prkcd Grin2c Glut` with BH-adjusted Wilcoxon `pvals_adj < 0.05`.
- The target biology bundle reports exact expression reach in the focal non-targeting thalamic population: Pafah1b1 is detected in 20,713 of 23,679 non-target nuclei, with 87.47% expressing, mean raw UMI 2.71, mean CP10K 1.65, and pseudobulk CPM 170.08. This made no-expression an unlikely explanation for a target null, but it was not used as an editing-efficiency estimate.
- The structured biology for Pafah1b1/LIS1 supports a real molecular lesion in principle: LIS1 positively regulates cytoplasmic dynein and is also the noncatalytic regulatory beta subunit of cytosolic PAF-AH(I). Pafah1b1 transcript is present in adult mouse thalamus, and germline mouse loss is dose-sensitive with severe neuronal-migration phenotypes.
- The same biology bundle also weakened transfer to this exact endpoint. The strongest mouse phenotypes are germline or developmental, the P30/young-adult circuit phenotype follows germline haploinsufficiency in hippocampal GABAergic neurons, and no endogenous mouse-neuron LIS1 turnover or dynein-complex persistence measurement was identified. Functional stock after a P16 edit and 21-28 day harvest window was therefore indeterminate rather than confidently depleted.
- The selected corpus release had no packaged same-experiment Findings, Claims, or explicit references for `Pafah1b1`, so no hidden same-target measured profile was available.
- The 151 training count table is highly zero-inflated: among 1,674 training targets, 1,205 had 0 DEGs, the median was 0, the 75th percentile was 1, the 90th was 2, and the 95th was 18. Biology had to move the forecast upward from this base rate.
- Exact focal-class counts for measured mechanistic comparators separated three regimes:
  - broad endolysosomal/sterol or dynactin-linked responses: `Rab7` 501, `Tsc2` 86, `Dctn1` 75, `Mib1` 27, `Vps35` 17, `Marchf6` 14;
  - sparse tubulin/sterol boundary responses: `Tbcd` 12, `Tuba1a` 7, `Srebf2` 7, `Selenoi` 5, `Htt` 3, `Tuba4a` 2;
  - null or self-only microtubule, migration, centrosome, and Reelin-neighborhood responses: `Map6` 0, `Nin` 0, `Cep85l` 0, `Reln` 0, `Vldlr` 0, `Lrp8` 0, `Dync2h1` 0, `Dync2i1` 0, `Kif2a` 0, `Ttll5` 0, `Hap1` 0, `Vps41` 0, and `Map1b`, `Mapre2`, `Mapt`, `Stmn2`, `Tubb4b`, `Tubb5`, `Kif5a`, `Kif5c` each 1.
- Direct Parquet inspection of the 151 rows confirmed that `Dctn1` had 75 total FDR<0.05 calls and 74 downstream calls, dominated by up-regulated SREBF2-like sterol genes such as `Insig1`, `Msmo1`, `Hmgcs1`, `Cyp51`, `Hmgcr`, `Fdft1`, `Fasn`, `Sqle`, and `Dhcr24`. The same direct query confirmed that the one-call cytoskeletal cases were self-only, while `Tuba4a` had only one downstream significant gene.
- Same-experiment corpus findings for `Dctn1`, `Map6`, `Nin`, and `Tuba4a` made the quantitative counts interpretable: `Dctn1` elicits a detectable sterol/cholesterol module, but `Map6`, `Nin`, and `Tuba4a` are explicitly uncoupled from that broad response despite being in the sampled cytoskeleton or microtubule neighborhood. `Tuba1a` shows only a narrow tubulin-isotype rebound rather than a generic injury program.

## Synthesis

The forecast treats `Dctn1` as the upper local bearing, not as a one-to-one donor. LIS1 loss can plausibly impair cytoplasmic-dynein function over three to four weeks, and focal Pafah1b1 RNA is broadly present, so I did not collapse the prediction to the screen-wide median of 0. However, the exact acute P16 assay is postmitotic and survivor-conditioned, while the strongest Pafah1b1 phenotypes are developmental; the target-specific protein persistence evidence is missing; and many represented migration, Reelin, centrosomal, tubulin, and microtubule-neighborhood perturbations in the same 151 population were zero or self-only.

I therefore forecast a sparse positive signature: near the `Tbcd`/`Tuba1a` boundary rather than the 75-DEG `Dctn1` sterol state or the 501-DEG `Rab7` lysosomal state.
