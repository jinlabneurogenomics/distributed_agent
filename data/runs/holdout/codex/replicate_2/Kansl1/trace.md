# Kansl1 direct `n_degs` forecast

## Endpoint

- Target: `Kansl1`.
- Focal population: `151 TH Prkcd Grin2c Glut`.
- Endpoint: number of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`.

## Biology used

- The in-assay reach for the target is high: `Kansl1` was measured in 19,567 of 23,679 focal non-target nuclei, 82.63 percent expressing, with mean raw UMI 2.10 and mean CP10K 1.31. This made a complete expression-gating failure unlikely in this thalamic population, while not proving editing efficiency.
- The functional-stock card calls KANSL1 by harvest `likely_substantially_depleted`, with partial evidence. The important positives are that a disruptive edit should stop new KANSL1 production; KANSL1 is a renewable nuclear NSL/KAT8 histone-acetyltransferase regulatory component; and inducible loss in primary mouse hippocampal neurons lowered STX17 and impaired mitophagy within days.
- The important restraints are that the neuronal acute evidence is hippocampal culture rather than juvenile thalamus in vivo, no target-specific KANSL1 protein half-life was identified, and the closest direct mechanism is an indirect STX17/autophagosome-fusion route rather than a measured pan-transcriptional collapse in the assayed cell class.
- The most direct perturbation analogs, `Kat8`, `Kansl2`, `Kansl3`, `Stx17`, `Snap29`, `Vamp8`, and `Kansl1l`, were absent from the focal training count table, so the forecast had to use weaker analogs.

## Training measurements used

The declared `151` count table contains 1,674 observed training perturbations. It is heavily zero-inflated:

- 1,205 perturbations had `n_degs = 0`.
- 469 perturbations had at least one DEG.
- The median was 0, the 75th percentile was 1, the 90th percentile was 2, and the 95th percentile was 18.
- The mean was 14.05 because a small tail reached hundreds to thousands of DEGs.

I compared Kansl1 against two noisy biological neighborhoods in the declared expression Parquet for `151 TH Prkcd Grin2c Glut`:

- Chromatin or broad transcriptional regulators spanned very strong, modest, and null outcomes: `Setd1a` 368, `Brd4` 311, `Ctnnb1` 383, `Smarcc2` 185, `Chd8` 61, `Arid2` 56, `Chd2` 34, `Kmt2a` 24, `Crebbp` 8, `Setd2` 1, `Ep300` 0, `Kdm5b` 0.
- Autophagy, endolysosomal, or mitochondrial comparators also split: `Rab7` 501, `Tsc2` 86, `Opa1` 37, `Vps54` 31, `Vps35` 17, but `Mtor` 2, `Sqstm1` 1, `Atg5` 0, and `Becn1` 0.

The selected 21 observed analogs all had 17,259 measured focal features in the Parquet. Their profile comparison was not a single shared module: 8 had at least 50 significant features, 5 had 10 to 49, 4 had 1 to 9, and 4 had none; across 210 pairwise comparisons, the mean top-tail overlap coefficient was only 0.041 for positive tails and 0.059 for negative tails. I therefore treated the large chromatin and Rab7-like footprints as proof that the endpoint can report chromatin or organelle stress in this population, but not as a quantitative expectation for noncatalytic KANSL1.

## Synthesis

`Kansl1` is expressed in most focal control nuclei and has a plausible renewable post-edit function by P37-P44, so I did not forecast the count-table median of zero. At the same time, the exact NSL/STX17 partners were not observed perturbations, direct autophagy knockouts were mostly quiet in `151`, and the indirect chromatin comparators were highly heterogeneous, including `Ep300 = 0`, `Kdm5b = 0`, `Setd2 = 1`, and `Crebbp = 8`.

The resulting point estimate is a small nonzero signature, closest to the low HAT/chromatin examples rather than the broad essential transcriptional regulators:

`predicted_n_degs = 8`
