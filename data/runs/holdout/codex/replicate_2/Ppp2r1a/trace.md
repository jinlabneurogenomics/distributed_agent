# Ppp2r1a n_degs forecast

Target and endpoint:

- Target: `Ppp2r1a`
- Cell class: `151 TH Prkcd Grin2c Glut`
- Endpoint: count of measured genes with Wilcoxon `pvals_adj < 0.05`
- The declared all-cell-group training Parquet has no `Ppp2r1a` rows in the focal class, and I did not use a target expression signature or target outcome.

Evidence that moved the point forecast:

- The canonical biology bundle makes a realized edit plausible. `Ppp2r1a` is detected in the exact focal non-target population with `pct_cells_expressing = 94.003%`, `mean_cp10k = 2.661`, and `pseudobulk_cpm = 275.749`. Its functional-stock card calls A-alpha stock "likely_substantially_depleted" by the P37-P44 harvest because PP2A holoenzymes remodel and the reported adult-thalamus Ppp2r1a protein T50 is 5.7435 days, so the 21-28 day interval spans about 3.66-4.88 half-lives. This argues against a pure no-engagement prediction.
- The focal training count table is very sparse: among 1,674 training targets in this same class, 1,205 are zero, the median is 0, the 75th percentile is 1, the 95th percentile is 18, and only 106 targets have at least 10 DEGs. So any prediction above the teens needs a strong reason to treat `Ppp2r1a` like a global RNA-processing/chromatin/stress hit.
- The closest same-complex training perturbations are PP2A regulatory subunits, not the A-alpha scaffold or catalytic core. Both were flat in this exact class: `Ppp2r2b = 0`, `Ppp2r5d = 0`. Same-experiment reports described `Ppp2r2b` as producing no FDR<0.10 downstream response in any measured neuronal class, and `Ppp2r5d` as a very sparse, non-thalamic response with no detectable AKT-mTOR/RPS6, tau/CDK5/GSK3b, Wnt, ISR, UPR, autophagy, proteasome, or apoptotic transcriptome.
- Broader phosphatase/signaling training comparators in `151 TH Prkcd Grin2c Glut` were also low: `Ppp3ca = 4`, `Ppp3r1 = 9`, `Mtor = 2`, `Gsk3b = 6`, `Akt3 = 0`, `Mapt = 1`, `App = 1`, `Dnm1 = 1`, `Prkar1a = 1`. `Tsc2 = 86`, `Opa1 = 37`, and `Csnk2b = 25` showed that the assay can report larger signaling or organelle responses, but their same-experiment interpretations point to mTOR-, mitochondrial-, or CK2-specific RNA programs rather than to a generic phosphatase scaffold scale.
- Direct profile review of the declared Parquet in the focal class matched the count evidence. In a PP2A/calcineurin/mTOR cohort, `Ppp2r2b` and `Ppp2r5d` each had 0 significant features out of 17,259 measured rows, whereas `Ppp3ca`, `Ppp3r1`, and `Tsc2` had 4, 9, and 86. Whole-profile nearest-neighbor correlations for the PP2A regulatory anchors were weak (`Ppp2r2b` top Pearson 0.055; `Ppp2r5d` top Pearson 0.083), and their pairwise correlations to `Mtor`, `Gsk3b`, `Akt3`, `App`, `Mapt`, `Rptor`, `Opa1`, `Mff`, `Dnm1`, and `Prkar1a` all had no shared significant features.

Synthesis:

I treated `Ppp2r1a` as stronger than the individual assayed B-subunit losses because A-alpha is the core PP2A scaffold, is broadly expressed in the focal neurons, and should largely turn over by harvest. I did not scale it to `Tsc2`, `Opa1`, or the large chromatin/splicing tail because A-beta can buffer A-alpha loss, the PP2A B-subunit reports show that this phosphatase family can be almost entirely post-translational at basal nuclear RNA, and the mTOR/tau comparators named from `Ppp2r5d` were mostly 0-6 DEGs in the exact class. Balancing a near-zero PP2A-family training prior against stronger scaffold reach gives a low single-digit-to-very-low-teens expectation; I used `8` as the integer point.
