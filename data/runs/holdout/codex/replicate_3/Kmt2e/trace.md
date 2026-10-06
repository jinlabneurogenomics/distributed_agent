## Forecast trace for Kmt2e

Target and endpoint:

- Target: `Kmt2e`
- Endpoint: `n_degs` in `151 TH Prkcd Grin2c Glut`, counting measured genes with BH-adjusted Wilcoxon `p < 0.05`
- Held-out target measurements used: none. The target expression signature and target DEG count were absent from the declared training count table and expression parquet.

Biology from the declared Kmt2e bundle:

- Kmt2e is well within the assay's focal population rather than being an expression-reach miss: in matched non-target nuclei from `151 TH Prkcd Grin2c Glut`, 20,409 of 23,679 cells expressed Kmt2e, with mean raw UMI 2.309 and mean log1p(CP10k) 0.810.
- The card adjudicates KMT2E as a chromatin-associated H3K4me3 reader/transcriptional regulator, not as a demonstrated intrinsic histone methyltransferase. That made the closest analogs noncanonical SET/H3K4/chromatin regulators, not generic essential enzymes.
- Functional stock was judged likely to be substantially depleted by the P37-P44 harvest after P16 editing, because new KMT2E resupply should stop and brain protein turnover over a 21-28 day window makes appreciable renewal plausible. The conclusion is low-confidence and partial because no target-specific Kmt2e half-life or acute thalamic-neuron perturbation clock was found, and an OGT/USP7-stabilized pool could leave residual function.
- Mouse neural phenotype evidence exists for constitutive heterozygous Kmt2e loss, but it is germline/developmental and amygdala-centered. I treated it as weak support for neural relevance, not as evidence for a large acute thalamic transcriptional footprint.

Training endpoint context:

- The declared count table for the focal class has 1,674 measured training perturbations.
- Its distribution is sparse: 1,205/1,674 are zero, the median is 0, the 75th percentile is 1, the 95th percentile is 18, and only 43/1,674 training perturbations have at least 100 DEGs.
- Thus a high-expression chromatin target should not be assigned a broad response by default; strong tail behavior needs a close measured reason.

Chromatin-regulator measurements in the same focal class:

- Closest measured family/axis anchors were low to modest:
  - `Setd5`: 9 DEGs
  - `Kmt2a`: 24 DEGs
  - `Kmt2c`: 0 DEGs
  - `Setd2`: 1 DEG
  - `Ogt`: 4 DEGs
- Broader chromatin regulators demonstrate that large responses are possible but not typical for this class:
  - `Setd1a`: 368 DEGs
  - `Smarcc2`: 185 DEGs
  - `Chd4`: 100 DEGs
  - `Chd8`: 61 DEGs
  - `Chd2`: 34 DEGs
  - `Arid2`: 56 DEGs
- A focal profile comparison among these chromatin perturbations showed generally same-direction whole-profile correlations, but little exact overlap among their BH-significant genes; for example, `Setd5` had no significant DEG overlap with `Kmt2a`, `Setd1a`, or `Ogt`. I therefore used the analogs as magnitude anchors rather than as a coherent shared signature that would justify borrowing a high-count profile wholesale.

Synthesis:

Kmt2e has enough expression and likely enough protein turnover to expect a real recovered-cell perturbation, so the point estimate should sit above the screen-wide zero mode. Its closest available noncanonical SET relative, Setd5, was a 9-DEG perturbation, and other H3K4/chromatin-associated comparators ranged from 0 to 24 unless they belonged to stronger, more central catalytic or remodeling complexes. The developmental-only phenotype evidence and uncertain acute thalamic postmitotic requirement kept the estimate well below the Setd1a/SWI-SNF/CHD tail.

I therefore predict a low double-digit response:

`Kmt2e -> 12`
