# Q3 Literature Curation Methods

## Eligibility

The target manifest contained 205 assigned perturbations. I filtered the full Wilcoxon parquet to those `gene_target` values, required the exact allowed `group_name` labels, removed target-transcript rows with a case-insensitive `names != gene_target` comparison, and called a perturbation by cell-type pair eligible when at least one remaining downstream row had `pvals_adj < 0.10`.

That query yielded 918 eligible pairs. `q3_cell_type_specificity.jsonl` emits 918 rows, so every eligible pair is represented exactly once and no ineligible target-only pairs are emitted.

## Phenotype Characterization

For each eligible pair, all downstream FDR-significant rows were sorted by adjusted p-value. The evidence table records the number of FDR<0.10 downstream genes, the numbers with positive and negative log-fold changes, the matched perturbed and control nucleus counts, and the top FDR-ranked genes with log fold changes and adjusted p-values.

When a pair contained a recognizable central module, I annotated it using small marker sets for ATF4/UPR genes, SREBP sterol-biosynthesis genes, Wnt/beta-catenin targets, proteasome subunits, heat-shock chaperones, or circadian clock output genes. Multi-module pairs were reduced to the literature relationship with the strongest target-specific support; when materially different modules remained, the pair summary states that the cited relationship does not explain all FDR-supported genes.

## Literature Search

Before assigning flags, I queried PubMed for the target symbol plus the strongest FDR-ranked genes and, where the measured genes formed an interpretable module, for the target plus module terms such as `SREBP`, `cholesterol`, `beta-catenin`, `unfolded protein response`, `ATF4`, `proteasome`, `NFE2L1`, `HSF1`, or `CLOCK:BMAL1`. Searches used PubMed title/abstract fields for high-specificity target-to-response checks and broader PubMed searches for known aliases such as SERCA2 for ATP2A2, REV-ERB for NR1D1, and ADAR2 for ADARB1.

Cited papers were fetched from PubMed and retained only when they documented a target-specific relationship or a specific mechanistic bridge to the observed module. General target function, disease association, family membership, or pathway membership was not used as support for `Agree`, `Disagree`, or `Inferred` unless it connected the perturbed gene to the measured transcriptomic effect.

## Flag Rules

`Agree` was used when literature predicted the measured direction, allowing differences in species, cell type, developmental stage, and perturbation modality. Examples include APC loss increasing Wnt target genes, CTNNB1 loss decreasing the same module, SREBF2 loss decreasing sterol genes, TSC2 loss increasing mTORC1/SREBP2 sterol output, CLOCK loss decreasing clock-output genes, HSF1 loss decreasing heat-shock chaperones, and OPA1 or ATP2A2 loss increasing ATF4/UPR genes.

`Inferred` was used when the target-specific bridge was biologically close but incomplete. Examples include DHDDS loss to ER glycosylation stress, DEPDC5 loss through GATOR1 and mTORC1 to SREBP2, and POMP or PSMB4 loss to proteasome stress where the screen also showed broad neuronal transcript decreases that were not directly explained by proteasome feedback.

No sufficiently resolved contradictions were found, so no pair was assigned `Disagree`. Pairs with only isolated downstream genes, recurrent but unexplained screen-wide signatures, or broad disease/pathway background without a target-to-effect bridge were assigned `No Literature` after a pair-specific search for that target and measured response.

## Difficult or Low-Confidence Pairs

The lowest-confidence decisions were broad proteostasis perturbations, especially `Psmb4` and `Pomp`, because the literature predicts proteasome or ER-stress feedback for part of the measured response while many of the largest effects were decreased neuronal or synaptic transcripts. These were kept as `Inferred` when a proteasome/UPR/heat-shock submodule was present rather than promoted to a complete agreement call.

The sterol programs after `Chp1`, `Dctn1`, `Mib1`, and `Pcyt2` were also difficult: the modules were coherent and recurrent, but searches did not find a target-specific link comparable to the `Tsc2`, `Depdc5`, or `Srebf2` mechanisms, so those pairs were left as `No Literature` unless another cited target-specific module was present.

Eligible pairs: 918. Emitted pair rows: 918. Incompletely reviewed pairs: 0. Flag counts: Agree=43, Inferred=21, No Literature=854.
