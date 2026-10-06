# Nup93 direct DEG-count forecast

## Declared target and endpoint

- Target: `Nup93`
- Cell population: `151 TH Prkcd Grin2c Glut`
- Endpoint: `n_degs`, the number of measured genes in this cell population with BH-adjusted Wilcoxon `p < 0.05`

## Evidence used

1. **Canonical Nup93 biology bundle**

   The declared one-row manifest and biology bundle both identify `Nup93` as the only held-out target. The bundle reports exact in-assay target reach in the non-targeting cells of `151 TH Prkcd Grin2c Glut`: `Nup93` was detected in 19,848 of 23,679 nuclei, 83.821% of the population, with mean CP10K `1.4793`, mean log1p CP10K `0.7947`, and mean raw UMI `2.3358`. That establishes that the target transcript is observable in the focal population, but, per the bundle and the dataset portrait, it does not quantify editing efficiency or functional loss.

   The functional-stock adjudication is the dominant Nup93-specific prior. NUP93 is an inner-ring/linker nuclear-pore component. A P16 CRISPR loss-of-function edit should stop new NUP93 synthesis in edited alleles, but the operative material is pre-existing pore-incorporated scaffold. The bundle adjudicates `functional_stock_by_harvest = likely_persists`, with high-confidence support that postmitotic neuronal NPC scaffold components exchange extremely slowly and that old pore-bound NUP93/NUP205/NUP155 material can persist for months. The loss model closest to a mature postmitotic context was also slow, with overt podocyte dysfunction over months rather than over the 21-28 day neuronal assay window.

2. **Training count table**

   The exact focal-population training table contains 1,674 observed training perturbations and excludes `Nup93`. It is sparse: 1,205 of 1,674 training perturbations have `n_degs = 0`; the median is `0`, the 75th percentile is `1`, the 90th percentile is `2`, the 95th percentile is `18`, and the 99th percentile is `454`. This makes a null or near-null count the default expectation for a perturbation whose functional lesion is buffered at harvest.

3. **Training-available biological comparators**

   I nominated training genes with the typed gene-analog index and then inspected their focal-population counts rather than selecting by a `Nup*` name pattern. The only high-priority, NPC-relevant exact-complex comparators in the training table were split:

   - `Ranbp2`: exact-complex / transport-module / STRING-physical nominee; `n_degs = 0`
   - `Tpr`: exact-complex / STRING-physical NPC nominee; `n_degs = 1768`

   Broader nucleocytoplasmic-transport nominees also split:

   - `Xpo7`: `n_degs = 0`
   - `Kpna3`: `n_degs = 0`
   - `Tnpo3`: `n_degs = 618`

   The remaining exact or narrow nominees were not better scale donors for Nup93 inner-ring stock loss: `Hspa8 = 9`, `Hspa5 = 5`, `Snrpb = 0`, `Hnrnpc = 122`, `Nek9 = 0`, and `Prkca = 0`. Several are RNA-processing, heat-shock, or mitotic-envelope annotations rather than installed NPC inner-ring scaffolds.

4. **Observed profile review of selected comparators**

   A symmetric profile comparison over 15 selected nominees in `151 TH Prkcd Grin2c Glut` found no missing training profiles and preserved all 105 pairwise comparisons. The node activity distribution was heterogeneous: 7 nominees had no significant features, 3 had 1-9 significant features, and 5 had at least 50. In the focal NPC/transport subset, `Ranbp2`, `Xpo7`, and `Kpna3` were null, while `Tpr` and `Tnpo3` were large responses. The training profiles therefore did not define a coherent “nuclear pore / transport” count scale; they separated into quiet stable or soluble-transport controls and acute RNA-transport/RNA-processing responders.

## Synthesis

The upward evidence is that `Nup93` is expressed in the assayed cells, has no close compensating paralog in the bundle, and is an essential NPC scaffold in the long run. The downward evidence is more directly matched to the P16-to-P37/P44 Perturb-seq design: most existing, functional NUP93 should remain pore-incorporated during the 21-28 day window, the declared neuronal readout samples surviving postmitotic nuclei, and the best genuine NPC training boundary includes a null `Ranbp2` perturbation. I therefore treated the very large `Tpr` and `Tnpo3` profiles as evidence that nuclear-pore-associated processes can respond strongly when a more dynamic basket or transport/RNA-processing step is perturbed, but not as a scale transfer for a buffered inner-ring `Nup93` supply cutoff.

The point forecast is the focal-population null:

`predicted_n_degs = 0`
