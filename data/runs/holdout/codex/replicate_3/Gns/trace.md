# DEG-count forecast for `Gns`

## Endpoint and declared target

- Target/cell class: `Gns` in `151 TH Prkcd Grin2c Glut`.
- Endpoint: number of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`.
- The held-out target was absent from the declared 151-class training count table: 1,674 rows, no `Gns`.
- The biology bundle exposed only target characterization and exact non-target expression reach for `Gns`, not the target DE signature or target DEG count.

## Biology used

The canonical `Gns` bundle made target engagement plausible by harvest but did not make a large RNA response likely by itself.

- `Gns` encodes a soluble lysosomal N-acetylglucosamine-6-sulfatase in heparan- and keratan-sulfate degradation.
- Existing lysosomal enzyme activity should be diluted after editing rather than persisting as a stable installed structure. The functional-stock card therefore judged `functional_stock_by_harvest = likely_substantially_depleted`; its most direct timing support was a mouse-brain recombinant GNS activity half-life of about 1.1 days, far shorter than the P16-to-P37/P44 interval.
- `Gns` is detectably expressed in the exact focal population: 18,103 of 23,679 non-target nuclei expressed it, with mean CP10K 1.0636 and mean raw UMI 1.7302. This made the locus reachable and left a self-transcript DEG plausible if the induced alleles produced nonsense-mediated decay.
- The disease prior was slower and mixed-cell: constitutive `Gns` loss causes progressive lysosomal/neuroinflammatory pathology including thalamus, but the first detailed mouse histology in the bundle was at 12 weeks, not 21-28 days after an acute neuronal edit. NeuN-positive nuclei also exclude the glial and inflammatory compartments that drive much of the congenital storage phenotype.

## Training measurements used

From the declared 151-class count table:

- Median `n_degs` across training targets was 0.
- 469/1,674 targets had any significant gene.
- 232/1,674 had any significant non-self gene in the matched 151 parquet rows.
- 319/1,642 targets with their own transcript measured had a significant self transcript.
- 237 targets had exactly one significant gene and no non-self significant gene.

The more mechanistically specific GAG-catabolism genes were not available as training perturbations: `Ids`, `Sgsh`, `Naglu`, `Hgsnat`, `Galns`, `Arsb`, `Gusb`, `Glb1`, `Hexa`, `Hexb`, and `Arsa` were absent from the declared count table. I therefore used the available lysosomal or lysosome-adjacent perturbations, checking their exact 151-class parquet rows:

| training target | `n_degs` in 151 | self logFC | self adjusted p | interpretation |
| --- | ---: | ---: | ---: | --- |
| `Ppt1` | 1 | -0.5361 | 1.34e-05 | one DEG, only the target transcript |
| `Ctsb` | 1 | -1.4797 | 8.54e-43 | one DEG, only the target transcript |
| `Atp6v0a1` | 1 | -0.6395 | 4.52e-12 | one DEG, only the target transcript |
| `Lamp2` | 0 | -0.3802 | 0.0537 | no DEG despite a near-threshold self decrease |
| `Atp6v1a` | 0 | -0.2363 | 1.0 | no DEG |
| `Mtor` | 2 | -0.4127 | 0.2562 | two downstream DEGs, no significant self transcript |

Across all assayed classes, `Ppt1`, `Ctsb`, and `Atp6v0a1` likewise produced only isolated one-gene calls where detected rather than a recurrent downstream lysosomal program. That made broad stress induction from an acute neuronal lysosomal perturbation a poor fit for this dataset, even in high-yield `151 TH Prkcd Grin2c Glut`.

## Synthesis

`Gns` should be expressed and its soluble enzymatic activity should be substantially depleted by P37-P44, so I did not treat it as an unreached null. The matched training perturbations argue, however, that lysosomal hits with detectable self knockdown usually do not generate a multi-gene 151-class signature over the same harvest window. Because the exact `Gns` disease phenotype is progressive and the screen samples surviving neurons rather than glia, the strongest point estimate is a single significant gene: either the `Gns` self transcript, if NMD is visible, or one immediate storage-response transcript.

Point prediction: `1`.
