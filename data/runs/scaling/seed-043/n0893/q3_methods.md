# Q3 literature-agreement methods

## Eligibility

The target scope was the complete manifest in `[local file: n0893.targets.json]`: 893 gene targets. I filtered the whole-screen parquet to those targets, retained rows from the 23 allowed `group_name` values, then marked a perturbation by cell-type pair eligible when at least one downstream row satisfied:

```text
gene_target in manifest
and group_name in allowed_cell_groups
and pvals_adj < 0.10
and lower(names) != lower(gene_target)
```

That self-transcript exclusion was applied before grouping, so a target whose only significant row was its own transcript would not be emitted. The query found 135,055 significant downstream rows and 2,324 eligible perturbation by cell-type pairs; all 2,324 pairs are emitted in `q3_cell_type_specificity.jsonl`.

## Phenotype Characterization

For every eligible pair, I sorted the post-filter significant genes by Benjamini-Hochberg adjusted Wilcoxon p-value and used the lowest-FDR genes, their log fold changes, the number of significant up- and down-regulated downstream genes, and `n_pert_matched`/`n_ctrl_matched` as the dataset-derived phenotype. The evidence file contains one evidence row per emitted pair with the 10 lowest-FDR downstream genes, or all significant genes when fewer than 10 passed FDR.

Response modules were chosen from the actual significant genes, not from target identity alone. Directly interpretable modules included `Srebf2` loss with down-regulated sterol-biosynthesis genes (`Dhcr24`, `Insig1`, `Cyp51`, `Msmo1`, `Hmgcr`, `Hmgcs1`, `Ldlr`, `Fdft1`, `Sqle`, `Lss`, `Fdps`, `Acaca`), `Bmal1`/`Clock` loss with down-regulated circadian output genes (`Dbp`, `Nr1d1`, `Nr1d2`, `Tef`, `Per3`, `Cry1`, `Npas2`), `Hsf1` loss with down-regulated heat-shock chaperones, and `Apc` loss with increased canonical Wnt feedback genes (`Axin2`, `Nkd1`). `Adarb1` pairs were reduced to the recurrent `Flnb` effect because it dominated 13 eligible cell types. `Tsc1`, `Tsc2`, and multi-gene `Pten` pairs were treated as mTOR-adjacent only when their own significant genes contained lysosomal, PI3K, or sterol-pathway transcripts rather than by assuming every downstream gene was an mTOR readout.

## Literature Search And Flagging

Pair-level PubMed/PMC searches combined the perturbed target with the leading significant genes or module terms, for example `Srebf2 HMGCR LDLR Cyp51`, `Clock Bmal1 Dbp Nr1d1 direct E-box transcription`, `APC loss Axin2 Nkd1 beta-catenin Wnt target transcription`, `ADARB1 FLNB filamin B RNA editing`, `TSC1 TSC2 mTORC1 SREBP cholesterol biosynthesis`, and `Hsf1 Hsp90aa1 Hsph1 heat shock transcription`. Returned PubMed and PubMed Central records were reviewed for a target-to-effect relationship; broad disease, family, or pathway papers were rejected unless they supplied a mechanistic bridge to the measured genes.

I assigned `Agree` when the cited relationship predicted the sign of the measured response: SREBP-2 loss decreasing sterol-pathway transcripts, Bmal1 or Clock loss decreasing E-box circadian outputs, Hsf1 loss decreasing heat-shock chaperone transcripts, and Apc loss increasing beta-catenin feedback targets. I assigned `Inferred` where literature supplied a specific but incomplete bridge: ADARB1 edits FLNB but the available Adar2-null mouse heart data did not show an FLNB abundance decrease, and TSC/PTEN papers connect the targets to neuronal mTORC1/SREBP signaling without documenting the exact acute Perturb-seq mRNA modules. All other pairs were assigned `No Literature` when target-plus-leading-gene searches did not find a direct or biologically specific partial target-to-response bridge.

## Context Transfer

Species, cell-type, stage, and modality differences were recorded in `lit_context` but were not by themselves used to downgrade direct, directionally interpretable transcription-factor relationships. The `indirect` context was used only for partial chains such as TSC/PTEN to mTORC1/SREBP to a sterol-like response and ADARB1 to FLNB RNA editing to unresolved FLNB mRNA abundance.

## Multi-Module And Difficult Pairs

When a pair contained several FDR-supported modules, the pair-level flag follows the most central, lowest-FDR coherent response with a target-specific bridge; scattered secondary significant genes were not used to override the central module. The difficult, lower-confidence decisions were mostly single-gene pairs and large RNA-processing or proteostasis signatures for splicing, transport, proteasome, and chromatin targets. Those pairs often had extensive target literature, but searches did not identify a bridge to the exact leading mRNA changes, so they were left as `No Literature` rather than converted into generic transcriptional-dysregulation support.

## Counts

- Eligible perturbation by cell-type pairs: 2,324
- Emitted pair rows: 2,324
- Evidence rows: 2,324
- Cited literature references: 10
- Flags: {'Agree': 27, 'Inferred': 36, 'No Literature': 2261}
- Reference uses: {'R001': 27, 'R002': 14, 'R003': 14, 'R004': 4, 'R005': 2, 'R006': 13, 'R007': 7, 'R008': 3, 'R009': 23, 'R010': 13}
- Incompletely reviewed pairs: 0
