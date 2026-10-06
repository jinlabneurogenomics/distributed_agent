# Myt1l n_degs forecast for 151 TH Prkcd Grin2c Glut

Endpoint: `n_degs` is the number of measured genes in `151 TH Prkcd Grin2c Glut` with Wilcoxon `pvals_adj < 0.05`.

## Target biology used

- The held-out target is `Myt1l`.
- The declared biology bundle was used in its `biology` view only; it reports no target outcome and no labeled-neighbor outcomes.
- Exact focal expression reach is strong: `Myt1l` is detected in 23,238 of 23,679 non-target cells in this class, `98.1376%`, with mean raw UMI `6.2434` and mean CP10K `3.9438`.
- The curated functional-stock card calls MYT1L a nuclear DNA-binding transcriptional repressor rather than a durable installed product. Successful editing should stop new functional MYT1L supply, and active stock is expected to be substantially depleted over the 21-28 day P16-to-P37/P44 interval.
- Adult and postmitotic neural evidence supports a continuing role in neuronal transcriptional maintenance: MYT1L suppresses non-neuronal and earlier neuronal programs and has been linked to SIN3B-HDAC2-associated repression in adult mouse brain.
- The main downward uncertainties are real: no transferable post-P16 thalamic loss timing experiment was available, endogenous neuronal MYT1L half-life was not measured, and compensation by MYT-family paralogs after Myt1l loss in postmitotic thalamic neurons was unresolved.

## Matched training evidence

The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` contains 1,674 visible training targets. Its distribution is zero-inflated and extremely skewed:

- minimum `0`
- median `0`
- 75th percentile `1`
- 90th percentile `2`
- 95th percentile `18`
- 97.5th percentile `100`
- maximum `2677`

I then inspected a training cohort of chromatin and postmitotic transcriptional regulators in the declared DE Parquet, all in the exact focal cell class. Their `pvals_adj < 0.05` counts were:

| target | n_degs |
|---|---:|
| Sin3a | 1433 |
| Chd4 | 100 |
| Chd8 | 61 |
| Kmt2a | 24 |
| Mecp2 | 16 |
| Phf21a | 6 |
| Zbtb18 | 5 |
| Bcl11a | 0 |
| Bcl11b | 0 |
| Foxp2 | 0 |
| Kmt2c | 0 |
| Rest | 0 |
| Zbtb20 | 0 |

The run-local profile comparison over those 13 training perturbations completed with no missing profiles. Six of the 13 were null in this context, two had 1-9 significant genes, two had 10-49, and three had at least 50. The cohort did not form a single tight FDR-level program: significant-program overlaps were sparse, and the largest source, `Sin3a`, shared only 4 same-direction FDR genes with `Mecp2` despite broad whole-profile score correlation.

## Corpus evidence used to interpret those counts

- `Sin3a` was treated as an upper-bound rather than a scale donor. The same-experiment corpus reports that `Sin3a` loss had 3,761 downstream FDR<0.10 calls across 14 of 21 measured cell groups, dominated by `151 TH Prkcd Grin2c Glut`, `155 MB Glut`, and `052 Pvalb Gaba`. Its program included ER/protein-quality-control, nuclear-speckle/splicing, lipid/cholesterol/mitochondrial/redox, and endolysosomal arms, which is much broader than the Myt1l prior.
- `Sin3a:F010` and the associated Claim separate `Sin3a` from simple REST-mediated or MeCP2-equivalent repression: `Rest` and `Mecp2` did not converge with `Sin3a` in measured postnatal neurons.
- `Mecp2` was the closest same-assay scale reference: it is a postmitotic neuronal chromatin regulator with Rett biology, and the corpus reports a sparse acute P16 response restricted to 4 of 22 measured groups, strongest in `151 TH Prkcd Grin2c Glut`. In the stricter requested `pvals_adj < 0.05` table this corresponds to 16 DEGs in the focal class.
- `Rest` was a mechanistic boundary: despite textbook chromatin-repressor biology, acute P16 `Rest` perturbation produced a pan-neuronal transcriptional zero at FDR<0.10 and did not phenocopy measurable REST-adjacent chromatin regulators such as `Sin3a`, `Chd4`, `Zmynd8`, or `Mecp2`.

## Point synthesis

I projected `Myt1l` above the screen median and above null REST/BCL11/FOXP/ZBTB20-like transcription factors because it is expressed in nearly all focal non-target cells and the card-supported operative stock should erode during the assay window. I kept it far below `Sin3a` and below the `Chd4`/`Chd8` range because MYT1L is a sequence-biased identity regulator with unresolved post-edit depletion kinetics, not a pan-complex scaffold whose loss in the atlas drove proteostasis and homeostatic stress modules.

The count-table analogs put a plausible focal response near `Mecp2`/`Kmt2a` rather than near the 100-1433 outliers. My point forecast is therefore:

`Myt1l`: `24`
