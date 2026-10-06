# Direct n_degs forecast for Tmem63a

Endpoint: number of measured genes with BH-adjusted Wilcoxon `p < 0.05` in `151 TH Prkcd Grin2c Glut`.

## Evidence used

1. The one-row holdout manifest names `Tmem63a`; the requested cell class resolves exactly to `151 TH Prkcd Grin2c Glut`.
2. The declared biology bundle gives low exact focal reach for the target: in non-target thalamic nuclei, `Tmem63a` had mean CP10K 0.06695, mean raw UMI 0.10934, and expression in 2,257 of 23,679 cells, or 9.53%. The same bundle describes the assayed population as survivor-conditioned NeuN-positive thalamic neuronal nuclei after P16 editing and P37-P44 harvest.
3. The biology prior supports TMEM63A as a mechanically activated cation channel, but the strongest postnatal mouse CNS loss phenotype is oligodendrocyte-autonomous myelination, not a demonstrated NeuN-positive neuronal requirement. Reported postnatal brain protein was concentrated in differentiated oligodendrocytes with little NeuN-positive neuronal signal. Editing should stop new channel production, but the card could not resolve how much pre-existing membrane/organellar channel stock is lost within 21-28 days.
4. The training count table for this exact focal class is sparse: 1,205 of 1,674 training perturbations have `n_degs = 0`; the median is 0; the 75th percentile is 1.
5. Curated mouse annotations place the closest perturbed functional comparator, `Tmem63b`, with `Tmem63a` in GO:0008381 mechanosensitive monoatomic ion channel activity; GO:1990760 osmolarity-sensing monoatomic cation channel activity also contains `Tmem63b`, `Tmem63c`, and a few TRP-channel controls in the training universe.
6. Those channel comparators were quiet in the declared training endpoint: `Tmem63b` had `n_degs = 1`, while `Tmem63c`, `Trpa1`, `Trpv1`, and `Trpm3` each had `n_degs = 0`.
7. Direct inspection of the `151 TH Prkcd Grin2c Glut` Parquet rows showed that the single BH-significant `Tmem63b` feature was the self transcript `Tmem63b` itself (`logfoldchanges = -0.701`, adjusted `p = 4.16e-17`); `Tmem63c`, `Trpa1`, `Trpv1`, `Trpm3`, `Sox10`, and `Myrf` had no significant features.

## Synthesis

The target is in a population where its measured expression is low and sparse, the postnatal phenotype is strongest in non-assayed oligodendrocytes, and the 21-28 day neuronal loss-of-function realization is uncertain because pre-existing channel stock may persist. The sparse global count distribution already puts an uninformative perturbation near zero, and the biologically closest measured channel perturbations in the same thalamic population are 0-1 DEG cases rather than moderate responders. Because `Tmem63b` reached 1 DEG only through self-transcript loss and `Tmem63a` itself has very low focal expression, the best point forecast is no BH-significant measured gene.

Predicted `n_degs`: 0
