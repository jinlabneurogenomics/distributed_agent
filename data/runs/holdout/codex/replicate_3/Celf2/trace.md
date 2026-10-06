# Celf2 DEG-count forecast

Endpoint: `n_degs`, the number of measured genes in `151 TH Prkcd Grin2c Glut` with BH-adjusted Wilcoxon `p < 0.05`.

Prediction target: `Celf2`.

Evidence used:

- The held-out-free training table contains 1,674 targets for the same thalamic class. Its distribution is highly zero-inflated: 1,205/1,674 targets have `n_degs = 0`, the median is 0, the 75th percentile is 1, the 90th percentile is 2, the 95th percentile is 18, and 43 targets have at least 100 DEGs.
- The Celf2 biology bundle shows excellent exact reach in the focal population: Celf2 is expressed in 23,453 of 23,679 non-target nuclei, 99.05%, with mean 4.50 CP10K and 7.11 raw UMI. Dilution by absent target expression is therefore not the main downward risk.
- The same bundle supports likely but not proven depletion of operative CELF2 by the 21-28 day harvest window. CELF2 is a continuously needed RNA-binding/alternative-splicing regulator rather than a durable installed structure, but the evidence is incomplete because no endogenous CELF2 half-life in juvenile thalamic neurons was available and most mouse phenotypes came from developmental loss rather than P16 acute loss.
- Annotation-based analog nomination over the actual training universe found no exact CELF paralog, exact complex partner, narrow module, direct interaction, or reciprocal corpus comparator for Celf2. The 1,101 available nominees were all broad functional fallbacks, so their counts were treated as scale references, not as transferable endpoint labels.
- In the exact `151 TH Prkcd Grin2c Glut` Parquet rows, the closest non-core RNA-binding/post-transcriptional references were sparse: `Syncrip = 0`, `Tia1 = 0`, `Fmr1 = 0`, `Hnrnpdl = 1`, `Hnrnph2 = 4`, `Zc3h14 = 6`, `Ddx3x = 8`, and `Hnrnpa2b1 = 11`. Corpus reports for `Zc3h14` and `Hnrnpa2b1` likewise described narrow or weak gene-level responses despite RNA-binding biology.
- Much larger RNA/RNP perturbations were available but less operation-matched: `Hnrnpc = 122`, `Matr3 = 149`, `Tardbp = 210`, `Snrnp70 = 213`, `Prpf6 = 454`, `Cdc40 = 624`, `Hnrnpu = 733`, `U2af2 = 828`, and `Rnpc3 = 868`. These define an upper scale for severe nuclear RNP or core spliceosome disruption. `Celf2` lacks evidence for that kind of obligate spliceosome-core collapse, and the whole-gene 10x readout can miss the isoform changes expected from a CELF-family regulator.

Synthesis: high Celf2 expression and the renewable RBP mechanism make a true zero less attractive than for an absent or durable target. The direct molecular effect is nevertheless expected to be alternative-splicing/isoform remodeling, not broad whole-gene abundance collapse, and the training analogs that are closest to that non-core RBP regime cluster in the 0-11 DEG range. I therefore place Celf2 near `Ddx3x`/`Zc3h14`/`Hnrnpa2b1`, above the quiet buffered RBPs but far below Hnrnpc/Tardbp/core-spliceosome responses.

Predicted `n_degs`: 8
