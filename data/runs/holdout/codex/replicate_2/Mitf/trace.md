# Direct Mitf n_degs forecast

## Declared target

- Holdout manifest target: `Mitf`
- Cell group: `151 TH Prkcd Grin2c Glut`
- Endpoint: count of measured genes in this cell group with BH-adjusted Wilcoxon `pvals_adj < 0.05`

## Evidence used

1. The declared manifest has one target, `Mitf`.
2. The canonical `Mitf` biology bundle identifies this packet target as Entrez Gene 667838, official mouse symbol `Naip3`, with `Mitf` as an alias. The bundle's selected evidence says `Naip3` is a pseudogene with no established protein-coding molecular operation, no established Naip3 protein-turnover entity, no target-specific mouse loss phenotype found by the bounded phenotype search, and no matched thalamic/postnatal neural perturbation evidence.
3. The same biology bundle gives exact focal non-target expression in `151 TH Prkcd Grin2c Glut`: `mean_raw_umi = 0.188648`, `mean_log1p_cp10k = 0.082302`, `pseudobulk_cpm = 11.82325`, and `n_cells_expressing = 3740 / 23679 = 15.79%`.
4. The declared focal training count table contains 1,674 training perturbations. Its `n_degs` distribution is strongly zero-centered: 1,205/1,674 targets have 0 DEGs, 276 have 1 DEG, the median is 0, and the 75th percentile is 1.
5. Direct inspection of the declared expression Parquet for the same focal cell group showed 17,259 measured features for each of the 1,674 training targets. Among the 276 one-DEG training perturbations, 237 have the self transcript as significant at `pvals_adj < 0.05`, so a one-count outcome in this distribution is usually a target-transcript-only event rather than a broader downstream program.

## Reasoning

I treated the exact `Mitf` expression as sufficient for guide exposure and transcript observation, but not as evidence of an operative post-edit function. The target is not the microphthalmia-associated transcription factor; it is the `Naip3` pseudogene alias. The strongest biological prior is therefore absence of a known protein product or loss phenotype in postmitotic thalamic neurons, with functional Naip paralogs discounted because they only establish related innate-immune genes, not a Naip3-dependent neuronal stock.

That biology puts `Mitf` near the null mode of the focal training distribution rather than in the broad-response tail occupied by essential RNA-processing, proteasome, and transcriptional regulators. I also kept the point at 0 rather than 1: the target RNA is detectable in only a minority of focal non-target nuclei and a pseudogene transcript is not expected to undergo a clean protein-coding self-knockdown/NMD response, so even a self-only significant row is possible but not the central forecast.

Predicted `n_degs`: 0.
