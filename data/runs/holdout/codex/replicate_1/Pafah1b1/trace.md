# Direct DEG-count forecast

## Target and endpoint

- Target: `Pafah1b1`
- Focal population: `151 TH Prkcd Grin2c Glut`
- Endpoint: number of measured genes in this focal population with BH-adjusted Wilcoxon `pvals_adj < 0.05`, counting the target transcript if that row is significant.

## Evidence used

The held-out target bundle identifies Pafah1b1 as readily detectable in the exact assayed focal population: in non-target nuclei from `151 TH Prkcd Grin2c Glut`, Pafah1b1 had mean raw UMI 2.7138, mean log1p CP10K 0.8757, pseudobulk CPM 170.08, and 20,713 / 23,679 nuclei expressing it, or 87.47%. That made a self-transcript call plausible on power grounds, although the atlas context warns that target mRNA reduction should not be treated as a quantitative editing-efficiency readout.

The same bundle made the expected downstream response uncertain rather than high. LIS1/Pafah1b1 regulates cytoplasmic dynein and is a noncatalytic PAF-AH(I) regulatory subunit, so loss is not a one-time developmental structural lesion only. However, the strongest mouse loss phenotypes in the card were germline or developmental neuronal-migration phenotypes, with postnatal hippocampal circuit abnormalities still confounded by germline haploinsufficiency. The functional-stock adjudication was indeterminate for the P16-to-P37/P44 Perturb-seq window: editing stops new LIS1 synthesis, but pre-existing dynein-regulatory and PAF-AH(I) pools are not immediately removed and no mouse-neuron LIS1 half-life or LIS1-dynein persistence measurement was available.

The target has no packaged same-experiment Findings or Claims in the selected corpus release, so I used adjacent training perturbations from the declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` and the focal Parquet rows. The full 1,674-target training count table is extremely sparse in this cell class: the median is 0, 1,205 targets are zero, 1,481 are <=1, and 1,546 are <=5 at FDR 0.05. The high-count tail is small and dominated by broad RNA-processing and proteostasis perturbations.

Within the nearest measured dynein, kinesin, microtubule, and neuronal-migration comparators, the focal Parquet counts were mostly self-only or zero:

| training perturbation | focal FDR<0.05 genes | interpretation |
| --- | ---: | --- |
| `Dctn1` | 75 | true broader state, led by up-regulation of sterol genes such as `Insig1`, `Msmo1`, `Hmgcs1`, `Hmgcr`, and `Fdft1` |
| `Tuba1a` | 7 | self plus an alpha/beta-tubulin compensation module |
| `Tuba4a` | 2 | self plus a single `Mast1` response in 151 |
| `Kif1a`, `Kif5a`, `Kif5c`, `Map1b`, `Tubb4b`, `Tubb5` | 1 each | significant self-transcript row without a broader focal response |
| `Dab1`, `Dync2h1`, `Dync2i1`, `Kif1b`, `Kif3b`, `Reln`, `Spast`, `Vldlr` | 0 each | no focal FDR<0.05 row |

The report ledger agreed that the broad `Dctn1` phenotype is a special vesicle/sterol response, not a universal motor-cytoskeleton signature: canonical kinesins, `Kifbp`, `Vps41`, and structural tubulin or MAP perturbations generally did not phenocopy it, while `Map1b`, `Kif5a`, `Tubb4b`, `Tubb5`, `Spast`, `Dync2i1`, `Kif3b`, `Dab1`, and `Vldlr` were described as buffered or flat in the recovered postnatal neuronal transcriptome.

## Synthesis

I treated `Dctn1` as an upper analogue rather than the center of the forecast because Pafah1b1/LIS1 touches dynein regulation but is not the dynactin subunit whose perturbation in this assay gives an SREBF2-like sterol/vesicle-transport state. The structural microtubule, kinesin, and developmental Reelin comparators put more mass on no downstream response or a self-only response in 151.

The point prediction is therefore the self-only case: high Pafah1b1 expression makes one significant target-transcript row plausible, while the biology bundle's unresolved acute postmitotic requirement and the training set's buffered motor/cytoskeleton behavior argue against projecting tens of downstream DEGs.
