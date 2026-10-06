# Pten direct n_degs forecast

Target: `Pten`

Focal population: `151 TH Prkcd Grin2c Glut`

Endpoint: number of measured genes with BH-adjusted Wilcoxon `p < 0.05` in the focal population.

## Evidence used

- The one-row holdout manifest names `Pten`; the declared count table contains 1,674 visible training perturbations for `151 TH Prkcd Grin2c Glut`; the target Pten differential-expression profile and count were absent from the training parquet and count table.
- The canonical Pten biology bundle is outcome-blind and supports realized perturbation in the assayed window:
  - exact focal reach: `Pten` was detected in 21,905 of 23,679 matched non-target nuclei, 92.508% of cells, with mean CP10K 2.081;
  - operative role: PTEN removes the D3 phosphate from PIP3 and restrains PI3K-AKT-mTOR signaling;
  - stock: CRISPR stops new intact PTEN production, and the 21-28 day edit-to-harvest interval spans many 35.811-41.456 h neuronal PTEN half-lives, so the bundle adjudicates the enzyme stock as likely substantially depleted by harvest;
  - caveats: the direct phenotypic evidence is from postnatal neurons outside this exact thalamic subtype, phenotype timing was not mapped to the P16-to-P37/P44 window, Tpte buffering was unresolved, and the readout remains survivor-conditioned nuclear RNA.
- The visible `151 TH Prkcd Grin2c Glut` count table is very sparse: 1,205/1,674 perturbations have zero DEGs, the median is 0, the 90th percentile is 2, the 95th percentile is 18, and the 97.5th percentile is 100.5. Pten therefore should not inherit a high count just because its pathway is famous.
- Visible mTOR-axis counts in the training table separate sign-compatible activation analogs from broad pathway neighbors:
  - `Tsc2`: 86 DEGs;
  - `Depdc5`: 13 DEGs;
  - `Mtor`: 2 DEGs;
  - `Rptor`, `Akt3`, `Pik3r1`, `Pik3r2`, `Pik3cb`, `Strada`, and `Fmr1`: 0 DEGs.
- Exact focal-parquet queries reproduced those visible counts and showed that `Tsc2` has a broad signed program, 58 significant up and 28 significant down genes, whereas `Depdc5` is smaller, 10 up and 3 down. `Mtor` is only a 2-gene response, and the other selected pathway members above are null.
- In the symmetric profile comparison over `Tsc2`, `Depdc5`, `Mtor`, `Rptor`, `Akt3`, `Pik3r1`, `Pik3r2`, `Pik3cb`, `Strada`, and `Fmr1`, `Tsc2` and `Depdc5` were the only same-sign mTORC1-relief comparators with more than two significant genes. Their significant programs overlap directly: 5 of the 10 Depdc5 significant up genes and all 3 Depdc5 significant down genes were also significant in Tsc2, with no significant-direction conflicts.
- A full eligible-neighborhood scan around `Tsc2` and `Depdc5` did not uncover a coherent, larger PI3K/mTOR training module with stronger endpoint support. The top neighbors by whole-profile Pearson/cosine or signed tails were mostly biologically off-axis genes, and `Tsc2` and `Depdc5` were not each other's top local neighbors.

## Synthesis

I used `Tsc2` as the main quantitative anchor because loss of TSC2 directly releases mTORC1, matching the mTOR-dependent arm expected after PTEN loss. I treated `Depdc5` as a weaker same-direction lower anchor because it also releases mTORC1 through nutrient-sensing control but produced a much smaller observed program. I did not average in `Mtor`, `Rptor`, PI3K catalytic/regulatory, or `Akt3` losses as equal quantitative analogs, because those perturbations are sign-opposed or indirect relative to PTEN loss and were mostly null in the observed recovered-cell endpoint.

The Pten biology bundle pushes the prediction upward from the genome-wide median and from the Depdc5-scale lower anchor: focal expression is broad, PTEN protein should not persist for the whole assay window, and Pten loss has mTOR-dependent neuronal consequences in postnatal mouse neurons. I discounted a full `Tsc2` transfer because PTEN is upstream of TSC2, depends on local PI3K/PIP3 tone, has unresolved thalamic latency and survivor-conditioning risks, and the training data show that visible pathway perturbations other than Tsc2 are often quiet.

I therefore placed Pten below the 86-DEG Tsc2 count but well above Depdc5's 13-DEG count, at 64 DEGs.
