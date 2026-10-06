target_name: Hnrnpa1
cell_class: 151 TH Prkcd Grin2c Glut
endpoint: measured genes with BH-adjusted Wilcoxon p < 0.05
predicted_n_degs: 48

Evidence used:

- The declared holdout manifest contains one target, Hnrnpa1. Hnrnpa1 is absent from the 151 TH Prkcd Grin2c Glut training count table, so no target outcome or target signature was used.
- The biology bundle reports exact focal-population expression for Hnrnpa1 in this assayed class: 11,396 of 23,679 non-target nuclei expressed Hnrnpa1, 48.13%, with mean CP10K 0.443. That is sufficient reach for a survivor-state signal, but it also leaves substantial dilution/dropout risk.
- The same bundle classifies hnRNP A1 as a dynamic RNA-binding/ribonucleoprotein component whose existing protein stock should decline after editing rather than remain permanently installed. The stock conclusion was "likely_substantially_depleted": a 5.27 day neuronal protein half-life places the 21 to 28 day experiment at roughly four to five half-lives. This makes complete functional persistence unlikely.
- The target-card phenotype evidence supports RNA-processing and neuronal consequences but does not exactly match this experiment: mouse cortical neurons showed splicing and dendritic/synaptic abnormalities after 14 days of hnRNP A1 depletion, whereas the requested assay is sparse P16 CRISPR in postnatal thalamic neurons at P37-P44.
- The 151 TH training table is highly zero-inflated: 1,205 of 1,674 training perturbations had 0 DEGs, the median was 0, the 75th percentile was 1, the 95th percentile was 18, and the 99th percentile was about 436. A nonzero prediction already places Hnrnpa1 above most assayed targets.
- The closest measured family row, Hnrnpa2b1, had 11 DEGs in 151 TH and only 25 downstream FDR<0.10 calls across all six responding classes in the corpus summary. Its response up-regulated Hnrnpa1 in the two main glutamatergic responder classes, consistent with a buffered A/B hnRNP-family response rather than a spliceosome-collapse state.
- Other hnRNP/RBP rows bracketed that lower anchor: Hnrnpdl had 1 DEG, Hnrnph2 had 4, Hnrnpc had 122, Matr3 had 149, Tardbp had 210, and Hnrnpu had 733 in 151 TH. Corpus comparisons also described Hnrnpa2b1 as far weaker than Hnrnpu, Tardbp, Matr3, and Hnrnpc.
- Core or near-core splicing perturbations were treated as an upper ceiling rather than direct Hnrnpa1 analogues: Rnpc3, U2af2, Cdc40, Prpf6, and Snrnp70 had 868, 828, 624, 454, and 213 DEGs, and their reports describe broad RNA-processing/proteostasis states. Hnrnpa1 is an abundant alternative RNA-binding protein, but it is not the same kind of U2AF or snRNP lesion.
- A matched 151 TH profile comparison over 12 RNA-binding/splicing training perturbations confirmed the count split: Hnrnpa2b1 had 11 significant features, Hnrnpc 122, Tardbp 210, Hnrnpu 733, and U2af2 828. Hnrnpa2b1 was positively correlated with the broader RNA-processing profiles but shared very few same-direction FDR features, so its small count was not simply a random subsample of the high spliceosome state.

Synthesis:

The target is expressed in enough focal nuclei and has turnover fast enough that acute P16 editing should be biologically realized by harvest, so I did not use the population baseline of zero. At the same time, the exact A/B-family training analogue was only 11 DEGs and the broad 450 to 868 DEG core-splicing signatures represent much more proximal spliceosome failure than Hnrnpa1 loss. The strongest scale-bearing band is therefore between Hnrnpa2b1 and the moderate nuclear RBP rows Hnrnpc/Matr3/Tardbp, with uncertainty widened downward by survivor conditioning and incomplete thalamus-specific evidence. I placed Hnrnpa1 above the close Hnrnpa2b1 lower anchor but well below the 100 to 200 DEG broader RBP band, yielding a low-to-moderate nonzero forecast of 48 DEGs.
