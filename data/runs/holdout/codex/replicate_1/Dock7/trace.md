# Direct Dock7 n_degs forecast

## Target and endpoint

- Target: `Dock7`
- Focal population: `151 TH Prkcd Grin2c Glut`
- Endpoint: `n_degs`, the count of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05` in the focal population.

## Evidence used

### Declared Dock7 biology bundle

The canonical biology-only bundle marked the in-assay focal-population reach as high:

- `Dock7` was detected in `22,177 / 23,679` non-target nuclei in `151 TH Prkcd Grin2c Glut`, or `93.6568%`.
- Mean expression was `2.2779` cp10k and `3.5935` raw UMI per non-target nucleus.
- The functional-stock adjudication concluded that Dock7 protein is `likely_substantially_depleted` by the P37-P44 harvest after a P16 edit, based on an approximately 16-17 h mouse-cell protein half-life and a postnatal neural RNAi phenotype by 7 d.

The bundle therefore supports target reach and perturbation realization, but the biological operations it names are mainly local Rac/Cdc42 exchange and scaffold roles in polarity, migration, Tacc3, and ErbB4 signaling. Its strongest postnatal neural phenotype is V-SVZ neuroblast migration, not a matched mature thalamic transcriptional program.

### Training count distribution

The declared count table for `151 TH Prkcd Grin2c Glut` contains 1,674 training perturbations:

- 1,205 / 1,674 are exactly zero.
- The median is 0.
- 276 have exactly 1 DEG.
- Only 29 have more than 200 DEGs; the arithmetic mean is inflated to 14.05 by this long tail.

So the quantitative prior for an unspecified perturbation in this population is sharply concentrated at 0-1 with rare large outliers.

### Matched pathway analogs in the count table and Parquet

I treated directly represented Rac/Cdc42/DOCK/PAK/GEF/GAP cytoskeletal perturbations as the most relevant observed training set because Dock7 is a DOCK-C Rac/Cdc42 exchange/scaffold protein:

| training target | focal `n_degs` |
|---|---:|
| Arhgap18 | 0 |
| Arhgap32 | 0 |
| Arhgef9 | 1 |
| Cdc42 | 1 |
| Cfl2 | 0 |
| Dock3 | 0 |
| Erbb4 | 0 |
| Kalrn | 0 |
| Limk1 | 0 |
| Pak1 | 1 |
| Pak2 | 0 |
| Pak3 | 0 |
| Rac1 | 0 |
| Tiam1 | 0 |

This 14-target analog set has mean `0.214`, median `0`, eleven zeroes, three singletons, and no focal count above 1.

I then checked the declared Parquet for the narrower hand-picked anchors `Dock3`, `Rac1`, `Cdc42`, `Erbb4`, `Arhgef9`, `Kalrn`, `Pak1`, and `Tiam1` in `151 TH Prkcd Grin2c Glut`. Each had the full 17,259 measured-gene surface. `Dock3`, `Rac1`, `Erbb4`, `Kalrn`, and `Tiam1` had no BH-significant feature. The only three significant rows were the perturbed transcript itself:

| training target | significant gene | logfoldchange | adjusted p |
|---|---|---:|---:|
| Arhgef9 | Arhgef9 | -0.570876 | 3.703483e-08 |
| Cdc42 | Cdc42 | -0.593281 | 8.622241e-05 |
| Pak1 | Pak1 | -0.599053 | 5.018880e-08 |

Thus the best matched training perturbations show either no DEG or an isolated self-transcript call, not a Dock7-like downstream module.

### Same-experiment corpus context

Packaged same-experiment reports for the observed analogs matched the raw-count conclusion:

- `Dock3`, the represented DOCK-family comparator, produced no robust downstream snRNA-seq response in any recovered neuronal cell group.
- `Cdc42` reports no downstream DE and explicitly separate local actin/spine signaling from steady-state nuclear RNA after P16 perturbation.
- `Rac1`, `Pak1`, `Tiam1`, `Kalrn`, `Limk1`, `Cfl2`, and related Rac/Cdc42-linked actin-cytoskeleton targets are summarized in the corpus as transcriptionally buffered or singleton/nonconvergent rather than forming a recurrent shared nuclear mRNA module.
- `Erbb4`, one Dock7 scaffold partner axis represented in the training set, had no focal response and no coherent ErbB/neuregulin transcriptional module in the same sparse neuronal assay.

## Synthesis

Dock7 was reachable and its dynamic protein stock should have had time to deplete, so I did not treat it as an assay-inaccessible long-stock null. The decisive counterweight was endpoint specificity: the nearest observed perturbations in Rac/Cdc42, PAK/LIMK/cofilin, and related DOCK/GEF/GAP actin signaling were almost all zero in the exact thalamic class, and the few count-1 cases were self-transcript reductions only. Those data argue that this pathway can be functional yet buffered from a broad survivor-conditioned nuclear RNA state in juvenile neurons.

The high target-expression reach leaves a possibility of a one-gene self-transcript call, but the focal analog set's modal count is 0 and Dock7 has no training evidence for a stronger downstream class. I therefore used the zero-inflated pathway analog distribution rather than the screen-wide heavy tail and forecast:

`predicted_n_degs = 0`
