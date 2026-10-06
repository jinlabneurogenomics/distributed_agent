# Six6 direct DEG-count forecast

## Endpoint

- Target from the one-row holdout manifest: `Six6`.
- Focal population: `151 TH Prkcd Grin2c Glut`.
- Endpoint: `n_degs`, the count of measured genes in that perturbation/population contrast with BH-adjusted Wilcoxon `p < 0.05`.
- Point prediction: `0`.

## Evidence

**Declared Six6 biology bundle**

- `biology_bundles/Six6.json` reports exact in-assay focal-population reach for `Six6`: the feature was available, but non-target `151 TH Prkcd Grin2c Glut` nuclei had only 9 total `Six6` UMIs across 23,679 cells, 9 expressing cells, `pct_cells_expressing = 0.038008%`, `mean_raw_umi = 0.000380`, `mean_cp10k = 0.000274`, and pseudobulk `0.0238` CPM.
- The same bundle identifies Six6 as a homeodomain transcription factor with mouse neural developmental phenotypes in GnRH neurons and the suprachiasmatic nucleus, but the matched P16-to-P37/P44 postmitotic thalamic context is unresolved.
- Adult mouse thalamic bulk RNA-seq and P56 in situ data summarized in the bundle did not detect Six6. That qualitative non-detection is weaker than the exact in-assay 9-UMI reach, but points in the same direction: little target transcript is present in the assayed thalamic population.
- The functional-stock card judged functional Six6 depletion by harvest as indeterminate: a P16 edit should stop new intact SIX6 synthesis in successfully edited Six6-expressing cells, but target-specific protein turnover was not found and any pre-edit transcription-factor pool over 21-28 days is not timed.

**Same-experiment corpus**

- `corpus.target_context(Six6)` in release `perturbai-july-260713-sourceguard-1773-v1` returned no packaged Six6 Findings or Claims, so there was no same-target report to use.
- `Six3` was the closest represented Six paralog in the corpus. Its report described only a single `Slc6a6` signal in `007 L2-3 IT CTX Glut` at the report's FDR cutoff and specifically did not recover a broad Wnt/BMP/SHH/FGF/anterior-forebrain program.
- `Six5` was a second represented SIX-family comparator. Its report called the P16-to-P37/P44 neuronal response pan-neuronally null at FDR < 0.10 and found no latent cross-perturbation module.
- These corpus records are interpreted views of the same PerturbAI experiment, not independent replication.

**Training count table and Parquet**

- The focal training table `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` contains 1,674 held-in targets. Its endpoint distribution is highly concentrated at zero: 1,205 targets, or 72.0%, had `n_degs = 0`; the median was 0 and the 75th percentile was 1.
- The large-count tail is biologically different from Six6. Only 42/1,674 targets had more than 100 DE genes, and the largest included broad RNA-processing, ubiquitin/proteasome, nuclear-transport, and chromatin/transcriptional regulators such as `Uba5`, `Tpr`, `Sin3a`, `Rnpc3`, `U2af2`, `Psmb4`, `Hnrnpu`, and `Yy1`.
- Represented homeobox/SIX/developmental comparators were flat in the exact focal class: `Six3 = 0`, `Six5 = 0`, `Pax6 = 0`, `Otx2 = 0`, `Rax = 0`, `Hesx1 = 0`, `Gli2 = 0`, `Smo = 0`, `Fgfr1 = 0`, `Dlx6 = 0`, `Meis2 = 0`, and `Dach1 = 0`; `Sox2` was only 2.
- A column-filtered query of `training_de_all_cell_groups.parquet` for the same comparator set in `151 TH Prkcd Grin2c Glut` found no BH < 0.05 rows for those zero-count targets and two rows for `Sox2`. `Ctnnb1` was retained as a positive Wnt-pathway control and had 383 focal BH < 0.05 genes, showing that this class can score a Wnt-linked transcriptional response when the matched perturbation is strongly active.

## Synthesis

Six6 has a transcription-factor mechanism that could be high leverage in the right lineage, so a nonzero response is biologically possible in a small hidden Six6-positive subpopulation. The decisive counterweights are the exact focal reach and context: only 9 of 23,679 non-target nuclei carried any Six6 UMI, the closest functional literature is developmental hypothalamic/retinal rather than acute postmitotic thalamic, and protein-stock clearance by 21-28 days is unknown. In an aggregated class-level Wilcoxon contrast, any sparse Six6-dependent state should be diluted below genome-wide BH significance unless the edited cells are both much more common functionally than observed by RNA and undergo a large shared survivor-state change.

The training measurements make the zero forecast more likely than a one- or two-gene forecast. Most perturbations in this high-yield class are still null, and the closest held-in developmental/SIX/homeobox comparators are exactly null in this focal table, whereas the few strong positives are broader regulators with much clearer postnatal neuronal expression or core pathway leverage. I therefore used the modal/biologically matched endpoint rather than the long-tailed mean.

Prediction: `n_degs = 0`.
