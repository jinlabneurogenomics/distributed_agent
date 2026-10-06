# Direct outcome-blind trace

Target and endpoint:

- Manifest target: `Pten`.
- Focal population: `151 TH Prkcd Grin2c Glut`.
- Endpoint: `n_degs`, the count of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05` in that population.
- Held-out target rows were not queried or available in the declared training count table or training expression parquet.

Evidence that determined the forecast:

- The declared count table for `151 TH Prkcd Grin2c Glut` contained 1,674 visible training perturbations. Its DEG burden was highly sparse: 1,205/1,674 rows had zero DEGs, the median was 0, the 75th percentile was 1, the 95th percentile was 18, the 97.5th percentile was about 100, and the maximum was 2,677.
- The `Pten` biology bundle resolved PTEN as a PIP3 3-phosphatase and negative regulator of PI3K-AKT/mTOR signaling. In the exact focal population, the `Pten` transcript was directly measurable in 21,905/23,679 non-target cells, 92.5% of nuclei, with mean 3.27 raw UMIs and pseudobulk 205 CPM. This supports in-class reach but does not measure editing strength or the held-out DEG count.
- The same biology bundle judged functional PTEN stock likely to be substantially depleted by the P37-P44 harvest: the P16-to-harvest interval spans roughly 12-19 measured neuronal PTEN half-lives. That makes residual pre-edit protein a weak reason for a null endpoint.
- Visible PI3K/AKT/mTOR-side training rows in the 151-class count table were mostly quiet: `Tsc2` had 86 DEGs, `Gsk3b` had 6, `Mtor` had 2, and `Rptor`, `Akt3`, `Pik3cb`, `Pik3r1`, `Pik3r2`, `Fmr1`, and `Strada` had 0. Direct Parquet aggregation for the same ten perturbations reproduced those counts and showed that `Tsc2` split into 58 positive and 28 negative significant genes.
- A symmetric profile comparison of those ten visible pathway-adjacent perturbations found no significant-feature overlap between `Tsc2` and the silent or near-silent PI3K/mTOR rows. A `Tsc2` all-training neighborhood projection produced a mixed 62-node neighbor union dominated by zero- or one-DEG perturbations, aside from an unrelated high-count `Rab7`; therefore I treated `Tsc2` as the main quantitative anchor rather than as the center of a coherent active cohort.

Synthesis:

- The upward evidence is stronger than for an arbitrary training gene: `Pten` is well expressed in the exact assayed population, its protein stock should turn over within the experimental window, and loss of its lipid-phosphatase activity is expected to release PI3K-AKT/mTOR signaling.
- I did not transfer the full `Tsc2` burden. `Tsc2` is a direct TSC-complex brake on mTORC1, whereas PTEN acts upstream through PIP3 and AKT; published neuronal `Pten` phenotypes establish postnatal sensitivity in other neuronal populations but do not fix the 21-28 day thalamic transcriptomic latency; and most assayed neighboring pathway perturbations were measured as null or near-null in this cell class.
- I therefore placed `Pten` below `Tsc2`'s 86 DEGs but above the count-table 95th percentile of 18 DEGs. The selected point, 42, is a moderate active response, approximately half the visible `Tsc2` count and at the 96.5th percentile of the visible 151-class training distribution.

Predicted `n_degs`: 42
