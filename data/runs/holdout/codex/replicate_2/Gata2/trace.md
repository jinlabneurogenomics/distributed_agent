# Gata2 direct DEG-count forecast

Endpoint: number of genes in `151 TH Prkcd Grin2c Glut` with BH-adjusted Wilcoxon `p < 0.05` after the held-out `Gata2` perturbation.

## Evidence used

- The declared holdout manifest names a single target, `Gata2`; `Gata2` is not present in the 1,674-row training count table.
- The training endpoint is highly zero-inflated in this class: 1,205 of 1,674 training perturbations have `n_degs = 0`, 1,481 have at most one DEG, and 1,512 have at most two DEGs. The training median is 0 and the mean is 14.05 because a small upper tail carries most nonzero counts.
- The canonical `Gata2` biology bundle reports exact focal-population target reach of only 38 total `Gata2` UMIs in 23,679 matched non-target nuclei: 35 nuclei expressing, 0.1478% expressing, mean raw UMI 0.00160, and pseudobulk CPM 0.1006 in `151 TH Prkcd Grin2c Glut`.
- The same bundle makes Gata2 a free nuclear GATA-family transcription factor whose functional protein stock should usually deplete over the 21-28 day edit-to-harvest interval, but the matched loss evidence is developmental midbrain/neonatal rather than P16 postmitotic thalamus. Adult mouse thalamus has only low bulk Gata2 signal, with unresolved neuronal reach.
- GATA-family training perturbations in the exact endpoint were flat. The count table gives `Gata1 = 0`, `Gata3 = 0`, `Gata4 = 0`, `Gata6 = 0`, and `Zfpm2 = 0`; Parquet rows for the focal group confirmed 17,259 measured genes and zero BH < 0.05 rows for `Gata1` and `Gata3`.
- Packaged same-experiment Findings for the measured family members place this in context, not as an independent replicate: `Gata1` was a complete neuronal DE null across all 23 measured cell groups, while `Gata3` was almost completely buffered and the represented GATA/Zfpm2 perturbations did not form a shared postmitotic neuronal module.

## Synthesis

Gata2 has the right molecular form for a coding edit to deplete function by harvest, so I did not down-weight it for persistent stock. The decisive evidence was reach and context: this aggregate thalamic class contains almost no detected `Gata2` RNA, the supporting loss phenotype is an embryonic midbrain fate-selector phenotype rather than a postnatal thalamic-maintenance phenotype, and the represented GATA-family axis was quiet in the same postmitotic neuronal screen.

A rare subpopulation effect could be missed because nuclear RNA is sparse and the assay is survivor-conditioned, but the target asks for class-level FDR-significant Wilcoxon genes. Given the target expression reach and the zero counts for the closest measured local comparators, the most likely integer is no detected genes.

Point prediction: `0`.
