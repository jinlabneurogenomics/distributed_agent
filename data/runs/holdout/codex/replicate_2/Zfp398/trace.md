# Zfp398 151 TH Prkcd Grin2c Glut DEG-count forecast

Prediction: **0** BH-significant downstream genes at `pvals_adj < 0.05`.

## Declared target and endpoint

- Target manifest: `Zfp398`.
- Endpoint: `n_degs` in `151 TH Prkcd Grin2c Glut`, the number of measured genes with BH-adjusted Wilcoxon `p < 0.05`.
- Same-experiment ledgers, the count table, and the Parquet are alternate views of the same PerturbAI atlas experiment, so I treated corpus Findings as interpretation of the training measurements rather than independent validation.
- The held-out `Zfp398` 151 TH response was not used.

## Target biology

The biology bundle supports target reach but only weakly supports a large acute neuronal state:

- The exact in-assay non-target expression measurement for the focal population marked `Zfp398` available, with 17,892 of 23,679 focal non-target nuclei expressing it, `pct_cells_expressing = 75.56`, `mean_cp10k = 1.03`, and `pseudobulk_cpm = 100.89`.
- The functional-stock card classifies Zfp398 as a dynamic KRAB/C2H2 nuclear transcription regulator whose new protein supply should stop after a disruptive CRISPR edit; the 21-28 day P16-to-P37/P44 interval is likely long enough for substantial stock depletion.
- That stock conclusion is partial and low-confidence. No target-specific Zfp398 protein half-life or chromatin residence time was found.
- The main function prior comes from human pluripotent-cell ZNF398 promoter/enhancer occupancy with SMAD3 and EP300, plus official mouse thalamic expression. A transferable postnatal mouse thalamic neuron loss phenotype was not found.
- The bounded paralog search did not identify a close same-context compensating paralog, but broad KRAB/C2H2 family redundancy or unrelated buffering remain possible.

So Zfp398 is not an expression-null target; still, the bundle does not tie it to a known postnatal thalamic process, pan-neuronal chromatin effector, or acute stress machinery expected to yield hundreds of DE genes.

## Training counts

The declared 151 TH training count table contained 1,674 observed targets:

- median `n_degs` = 0; mean = 14.05; maximum = 2,677.
- 1,205/1,674 targets had 0 DEGs.
- 276 had exactly 1 DEG.
- 65 had 2-5, 50 had 6-20, 36 had 21-100, and 42 had more than 100.

The local zinc-finger set was even more zero-inflated. Among the 30 measured `Zfp*`/`Zfpm2` training perturbations in this focal population, the exact counts were:

```text
Zfp423 150
Zfp236 19
Zfp148 8
Zfp612 1
Zfp692 1
25 other Zfp*/Zfpm2 targets 0
```

Thus the family-local empirical mode was zero: 25/30 were flat at BH `p < 0.05`, and only one, `Zfp423`, exceeded 20 DEGs.

## Parquet profile evidence from the Zfp-family cohort

I compared the 30 measured `Zfp*`/`Zfpm2` 151 TH profiles directly in the declared Parquet using `gene_target`, `names`, `logfoldchanges`, and `pvals_adj < 0.05`.

- All 30 selected training nodes had available 151 TH profiles.
- Significant-feature statuses were: 25 with no significant features, 3 with 1-9, 1 with 10-49, and 1 with at least 50.
- The cohort did not share a recurrent FDR-supported response: the positive-tail pairwise significant-program overlap was present for only 10 of 435 pairs and had mean overlap coefficient 0.02 with median 0; the negative-tail overlap was present for only 3 of 435 pairs and had mean overlap coefficient 0.024 with median 0.

That makes the isolated high counts in the Zfp cohort poor quantitative donors for Zfp398. They are not the top of a coherent zinc-finger response branch; they are target-specific states.

## Same-experiment Finding interpretation

Corpus Findings for measured training targets reinforced the same boundary:

- `Zfp397` was transcriptionally silent in all measured recovered neuronal groups, and measured SCAN/zinc-finger relatives did not phenocopy it as a coherent family module.
- `Zfp644` had no FDR-significant downstream gene in any of the 20 neuronal groups where it was recovered; detectable `Ehmt1` and `Setdb1` responses showed that H3K9-linked chromatin biology was not globally invisible.
- `Zfp1` had no downstream gene-level DE in any of 23 recovered neuronal groups, while `Setdb1` had a modest detectable surface, arguing that an individual KRAB-ZFP can be non-rate-limiting for the Setdb1-sensitive neuronal response.
- `Zfp961` was also mostly buffered, with only a two-gene hippocampal/limbic response and no broad KRAB, PPAR, lipid, or stress module.
- `Zfp236` and `Zfp423` were the principal Zfp-family nonzero outliers, but their Findings attributed their responses to specific Ogt/Eif4a2/metabolic or thalamic identity/adhesion states and explicitly rejected generic zinc-finger or obvious family-member phenocopy explanations.
- The very broad `Zbtb7a` response was useful only as a detectability control for neuronal transcription-factor perturbations; it is a BTB factor with a proteostasis/endomembrane signature and did not define a Zfp398-like KRAB/C2H2 branch.

## Forecast

Expression reach and likely protein turnover make a small effect plausible, but the Zfp398 biology bundle lacks a postnatal thalamic demand signal and the observed KRAB/C2H2 or SCAN/C2H2 training perturbations overwhelmingly fell at zero. The few nonzero zinc-finger responses were idiosyncratic and did not create a shared Parquet-level FDR program to transfer.

I therefore used the Zfp-family mode, with the target-expression prior preventing me from treating zero as certain but not moving the integer point off zero.

`predicted_n_degs = 0`
