# Hsf4 DEG-count forecast

## Target and endpoint

- Target manifest: `Hsf4`.
- Endpoint: number of genes in `151 TH Prkcd Grin2c Glut` with Wilcoxon BH-adjusted `pvals_adj < 0.05`.
- The declared training count table contains 1,674 non-Hsf4 perturbations; Hsf4 and Hsf2 are absent from that table, while Hsf1 is present.

## Target biology used

- The exact in-assay expression card measured Hsf4 in the focal non-target population: 6,879 of 23,679 nuclei expressed Hsf4, or 29.051%, with pseudobulk 23.97 CPM and mean 0.237 CP10k. That supports some reachable thalamic expression, but in a minority of nuclei and at low abundance.
- The biology bundle judged the P16-to-P37/P44 perturbation as likely to substantially deplete functional HSF4 stock by harvest: HSF4 is a diffusible, DNA-binding heat-shock transcription factor and the 21-28 day interval is long relative to proxy mouse-brain protein lifetimes. This makes the perturbation plausible rather than an installed-stock null.
- The same bundle did not establish a strong juvenile thalamic requirement. The direct single-gene loss phenotype was lens differentiation, while the nearest neural evidence was an aged Hsf1/Hsf4 compound-mutant interaction; Hsf1/Hsf2 remain possible, unquantified buffers.

## Training measurements used

The focal count table is extremely sparse overall:

- 1,205 / 1,674 training perturbations have `n_degs = 0`.
- Median = 0, 75th percentile = 1, 90th percentile = 2, 95th percentile = 18.

The only represented heat-shock factor, Hsf1, is a small positive responder in this exact cell class rather than a broad stress perturbation:

| target | n_degs in 151 |
| --- | ---: |
| Hsf1 | 6 |
| Hspa8 | 9 |
| Hspa5 | 5 |
| Hsp90ab1 | 1 |
| Dnajc5 | 1 |
| Dnajc13 | 1 |
| Dnajb4 | 0 |
| Dnajb6 | 0 |
| Dnajc19 | 0 |

The declared Parquet rows for `151 TH Prkcd Grin2c Glut` show what the scalar Hsf1 count means mechanistically. Hsf1 has 6 significant rows, all negative and dominated by direct HSP/co-chaperone output:

| gene | logFC | p_adj |
| --- | ---: | ---: |
| Hsph1 | -0.484 | 1.69e-08 |
| Hsp90aa1 | -0.282 | 2.85e-04 |
| Rsrp1 | -0.175 | 8.06e-04 |
| Hsp90ab1 | -0.345 | 8.96e-04 |
| Mat2a | -0.234 | 7.37e-03 |
| Ahsa2 | -0.294 | 8.27e-03 |

Hsp90ab1 has only one FDR 0.05 hit in the same class, its own transcript, despite a large Hsp90ab1 logFC of -1.42. Hspa5 and Hspa8 give small, separate ER-UPR and cytosolic Hsp70 counterinduction signatures with 5 and 9 genes respectively.

## Corpus/profile interpretation

- Packaged same-experiment Findings for Hsf1 state that Hsf1 loss reduced a small HSP90/HSP110 co-chaperone module and did not induce a large proteotoxic, UPR/ISR, proteasome-bounce-back, redox, apoptosis, or mitochondrial-stress transcriptome.
- Packaged Hsp90ab1/Hspa8 Findings place the single heat-shock and chaperone perturbations in a buffered, non-collapsed neighborhood: Hsp90ab1 loss was downstream-flat, Hspa8 was a small HSP counterinduction response, and DnaJ-family perturbations were mostly flat.
- A fresh profile-neighborhood scan over all 1,674 eligible training nodes confirmed that the Hsf1, Hspa8, Hspa5, and Hsp90ab1 anchors each have only 1-9 significant features in 151 and did not reveal a high-count HSF/chaperone analogue. Hspa5 and Hspa8 were each other's strongest positive-tail overlap, but their counts were still only 5 and 9.

## Forecast

Hsf4 should be reachable by the edit window, but the focal target expression is modest and the biology bundle leaves isolated juvenile-thalamic demand unresolved. The Hsf1 analogue argues that losing an HSF transcription factor can be seen by this assay, while the measured chaperone neighborhood argues against transferring a broad proteostasis-stress count to Hsf4. I therefore put Hsf4 below Hsf1/Hspa8 and close to the buffered single-node HSP/DnaJ floor: most likely no broad downstream program, with one FDR hit possible from Hsf4 itself or a tiny direct target.

Point prediction: **1** DEG.
