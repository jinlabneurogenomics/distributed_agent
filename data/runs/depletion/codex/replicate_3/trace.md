# Trace

## Local data used

- Read the parquet metadata for `[local file: wilcoxon_de_results_group_name_final_data_no_multi_guide_cells_nocounts.parquet]`.
- The table has 745,758,369 Wilcoxon rows, 23 `group_name` values, 2,046 `gene_target` values, and 17,994 measured transcript names.
- The requested group, `151 TH Prkcd Grin2c Glut`, contributes 35,311,914 rows, comprising 2,046 perturbations x 17,259 assayed transcripts.
- I verified that all reported perturbations occur as `gene_target` values in the requested group and did not use any `Safe_target_*`, `Non_target`, or supplied odd-ranked genes.

## How the predictions were made

The odd-ranked positives were treated as endpoint evidence for the hidden cell-loss ranking, not as a whitelist.  They fell into several recurrent mechanisms:

- vesicle acidification and endolysosomal function: `Atp6v1b2`, `Atp6v1a`
- ER/Golgi, clathrin, and endosomal trafficking: `Cltc`, `Gbf1`, `Sec31a`, `Stx5a`, `Chmp4b`, `Snf8`
- proteostasis and mitochondrial stress resistance: `Psmb4`, `Pomp`, `Hspa9`, `Gpx4`
- RNA processing, nuclear transport, and transcriptional maintenance: `Son`, `Tnpo3`, `Polr3b`, `Ddx23`, `Thoc1`, `Taf1`, `Brd4`, `Kansl1`, `Cnot1`
- thalamic/developmental regulators and neuronal maintenance genes: `Six6`, `Six3`, `Myt1l`, `Nfix`, `Dmd`, `Kif1a`, `Atp8a2`, `Ank3`

For each perturbation in `151 TH Prkcd Grin2c Glut`, I then aggregated the Wilcoxon rows by `gene_target`, counting FDR < 0.05 transcripts and p < 0.001 transcripts and averaging absolute Wilcoxon scores/log fold changes.  That recovered a strong DE-burden signal for several supplied endpoints, including `Ppp2r1a`, `Psmb4`, `Hspa9`, `Tnpo3`, `Brd4`, `Thoc1`, `Ddx23`, and `Ank3`.  The highest-burden unlisted perturbations were enriched for spliceosome/RNA-processing hits (`Srsf1`, `Rnpc3`, `U2af2`, `Hnrnpu`, `Prpf6`, `Snrnp70`, `Tardbp`, `Matr3`), proteostasis genes (`Uba5`, `Ufc1`, `Psmc5`, `Psmc1`), nuclear transport or chromatin/transcriptional regulators (`Tpr`, `Xpo1`, `Sin3a`, `Trrap`, `Yy1`, `Phf12`, `Setd1a`, `Kmt2d`, `Smarcb1`, `Ctcf`, `Bptf`), and Wnt/cell-fate regulators (`Apc`, `Ctnnb1`, `Tcf7l2`, `Rora`, `Cic`).

I adjusted the final ordering toward unlisted genes in the same mechanistic neighborhoods as the strongest odd-ranked endpoints.  In particular, `Atp6v0c` was promoted because the two V-ATPase subunits in the revealed ranking bracket the very top of the screen, and trafficking hits such as `Sec23a`, `Sec63`, `Copa`, `Rab7`, `Vps35`, and `Ap2m1` were retained despite being somewhat lower by pure FDR burden because `Cltc`, `Gbf1`, `Sec31a`, `Stx5a`, `Chmp4b`, and `Snf8` show that vesicle/endolysosomal collapse is a repeated depletion phenotype in the truth set.

## Literature and corpus evidence

- Jin et al. established that pooled CRISPR perturbations can be delivered in vivo in developing mouse brain and read out by single-cell RNA-seq, and that loss-of-function of neurodevelopmental genes can yield recurrent, cell-type-specific neuronal and glial transcriptional phenotypes (Science 2020, PMID:33243861, doi:10.1126/science.aaz6063).  The assay here is a larger, postnatal, whole-brain version of the same conceptual strategy.
- ATP6V0C is part of the V-ATPase complex that controls vesicular acidification.  Its knockdown in neuronally differentiated SH-SY5Y cells impaired lysosomal acidification and autophagic flux and sensitized cells to neurite defects and cell death under bafilomycin A1 challenge (Mangieri et al., PLoS One 2014, PMID:24695574, doi:10.1371/journal.pone.0093257).  That supports the prediction that additional V-ATPase subunits such as `Atp6v0c` and `Atp6v1e1` should behave like `Atp6v1b2`/`Atp6v1a`.
- Biallelic human `UBA5` variants disrupt the UFM1 cascade and cause early-onset encephalopathy, with supporting biochemical and model-organism evidence that UBA5 loss impairs ER structure and neural function (Colin et al., Am J Hum Genet 2016, PMID:27545681, doi:10.1016/j.ajhg.2016.06.030).  This made the strong local `Uba5` DE signature plausible as a real vulnerability rather than a generic outlier.
- External PubMed searches also recovered broad ferroptosis literature around `GPX4`, consistent with the supplied `Gpx4` endpoint, but no direct papers that identify the exact `151 TH Prkcd Grin2c Glut` depletion genes.  I therefore used the literature as pathway support, not as a source of exact candidate ranks.

## Limitations

The provided parquet is a DE table over recovered nuclei.  The depletion ranking is a pre-readout abundance phenotype, so a perturbation can be a true strong depleter while leaving very few or relatively transcription-normal nuclei for the Wilcoxon test.  This is visible in the revealed endpoints: top-ranked `Atp6v1b2`, `Taf1`, and `Pafah1b1` have modest DE burden in the 151 TH slice, whereas some lower-ranked positives have many significant DE rows.  The answer is therefore a mechanistically weighted completion of the partially revealed ranking, not a direct sorting of a count statistic contained in the parquet.
