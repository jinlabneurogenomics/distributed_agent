# Opn1mw forecast trace

## Target and endpoint

- Target from the declared one-row holdout manifest: `Opn1mw`.
- Requested endpoint: `n_degs` in `151 TH Prkcd Grin2c Glut`, the number of measured genes with BH-adjusted Wilcoxon `p < 0.05`.
- The `Opn1mw` perturbation outcome was not present in the declared training count table or the same-experiment corpus.

## Evidence used

- The declared canonical `Opn1mw` biology bundle identified the target as a medium-wave cone opsin. It should be functionally consequential in expressing retinal cones because a disruptive edit stops replenishment of a photopigment installed in continuously renewed cone outer-segment membrane, but the established mouse loss phenotypes are retinal rather than thalamic.

- The same bundle gave exact focal-population reach in matched non-target nuclei for `151 TH Prkcd Grin2c Glut`: `Opn1mw` had only 1,012 total UMIs among 23,679 thalamic nuclei, mean raw expression 0.042738 UMI per nucleus, mean CP10K 0.027021, and any count in 885 nuclei, or 3.74%. That is tiny reach for an acute CRISPR perturbation in a sparse postmitotic brain-neuron assay.

- The declared 151 TH training count table was strongly concentrated at zero: 1,205 of 1,674 training perturbations had `n_degs = 0`; the median was 0, the 75th percentile was 1, and the 90th percentile was 2.

- Retina and photoreceptor-axis training perturbations were effectively silent in the same focal class. In the count table, `Crx`, `Gucy2c`, `Gucy2e`, `Neurod1`, `Nr2e3`, `Opn1sw`, `Otx2`, `Pax6`, `Rax`, `Rho`, `Rpgr`, `Rpgrip1l`, `Rxrg`, `Spata7`, `Thrb`, and `Vsx2` all had `n_degs = 0`; the broader retinal/developmental comparator `Sox2` had only 2.

- A direct scan of the declared expression Parquet in `151 TH Prkcd Grin2c Glut` confirmed zero BH<0.05 genes across 17,259 measured features for each of `Crx`, `Nr2e3`, `Opn1sw`, `Otx2`, `Pax6`, `Rho`, and `Vsx2`.

- Packaged same-experiment Findings gave the same qualitative boundary for the closest family member. `Opn1sw`, the represented S-cone opsin, had no FDR<0.10 downstream differential expression in any recovered brain-neuron class, and its curated comparison to `Rho`, `Crx`, `Nr2e3`, `Rxrg`, and `Thrb` found no shared photoreceptor-like program in the postnatal brain assay.

## Synthesis

`Opn1mw` is a real, low-redundancy cone photopigment in retina, so the perturbation is not intrinsically inert. The requested readout, however, is survivor-conditioned nuclear RNA from thalamic NeuN-positive neurons, and exact focal expression shows that essentially none of that cellular substrate carries meaningful `Opn1mw` mRNA. The nearest available biology in training was not a generic transcription factor but the same off-lineage photoreceptor axis, especially `Opn1sw`; those perturbations were flat in the focal class and, for `Opn1sw`, across all represented recovered brain classes. Combining the near-zero reach with the all-zero focal outcomes of the photoreceptor comparators, my point forecast is zero BH<0.05 genes.
