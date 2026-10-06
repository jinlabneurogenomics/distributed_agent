# Dhx9 n_degs forecast

## Target and endpoint

- Target: `Dhx9`.
- Requested population: `151 TH Prkcd Grin2c Glut`.
- Endpoint: number of measured genes with Wilcoxon `pvals_adj < 0.05`.

## Evidence used

1. The declared biology bundle places Dhx9 expression squarely in the focal population: 20,305 of 23,679 matched non-target nuclei expressed Dhx9, with mean CP10K 1.51 and mean raw UMI 2.45. This supports reach of the perturbation in the assayed thalamic nuclei, while not measuring editing efficiency.

2. The functional-stock card calls DHX9 a renewable ATP-dependent nucleic-acid helicase whose pre-edit protein is likely substantially depleted over the 21-28 days from P16 editing to P37-P44 harvest. The most direct turnover proxy was non-neural, however, and the loss-phenotype card found only developmental mouse neural phenotypes plus incomplete adult systemic shRNA evidence, so the postnatal thalamic endpoint remains uncertain.

3. Dhx9 had no same-experiment Findings or Claims in the selected released corpus, so no direct semantic report for the held-out target was used.

4. In the declared `151 TH Prkcd Grin2c Glut` training count table, 1,205 of 1,674 visible perturbations had zero DEGs; the median was 0, the 90th percentile was 2, and the 95th percentile was 18, with a very long RNA-processing/proteostasis tail.

5. I treated DDX/DHX and nearby RNP or spliceosome perturbations as the most relevant measured anchors, then checked their focal-class Parquet rows. The closest helicase anchors were weak:
   - `Ddx3x`: 8 DEGs, including self-downregulation and a few modest synaptic/neurite genes.
   - `Ddx39b`: 0 DEGs.

6. Broader RNA-binding and spliceosome anchors showed that the assay can produce very large signatures when a core RNP node drives a recurrent stress/RNA-processing state:
   - `Hnrnpc`: 122
   - `Tardbp`: 210
   - `Snrnp70`: 213
   - `Prpf6`: 454
   - `Cdc40`: 624
   - `Hnrnpu`: 733
   - `U2af2`: 828
   - `Rnpc3`: 868

7. A profile comparison over these 13 RNA-helicase/RNP/spliceosome anchors confirmed the scale split: `Ddx3x` had only 8 significant features, `Ddx39b`, `Fmr1`, and `Rbm28` had none, and nine spliceosome/RNP/nuclear-transport perturbations had at least 50. The corpus summaries likewise described `Ddx3x` as a narrow two-population response that did not align with the stronger `Hnrnpu`/`Hnrnpc` programs, and `Ddx39b` as restricted outside the focal thalamic class.

## Synthesis

Dhx9 is well expressed and its renewable helicase stock should be kinetically perturbed by the harvest window, so I did not use the zero-heavy global median as the point prediction. At the same time, it is not a canonical tri-snRNP/U2AF spliceosome component, and the measured DDX-family anchors closest to that operation were far below the several-hundred-DEG spliceosome signatures. I therefore forecast a small nonzero response, slightly above the `Ddx3x` focal count and within the upper decile but below the 95th percentile of the training-count table.

Predicted `n_degs`: 12
