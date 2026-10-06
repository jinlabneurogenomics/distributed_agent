# Acox1 DEG-count forecast

## Declared target and endpoint

- Target: `Acox1`
- Cell class: `151 TH Prkcd Grin2c Glut`
- Endpoint: `n_degs`, the count of measured genes in this perturbation/cell-class contrast with BH-adjusted Wilcoxon `pvals_adj < 0.05`.
- The declared training count table contains 1,674 non-Acox1 targets for this same thalamic glutamatergic class; 1,205/1,674 have `n_degs = 0`, 469 have at least one DEG, 193 have more than one DEG, and the median is 0. The nonzero tail is very skewed and headed by core RNA/proteostasis/chromatin perturbations rather than ordinary metabolic enzymes.

## Acox1 biology bundle

- The exact in-assay non-target expression bundle reports `Acox1` expression in the focal class in 16,272/23,679 nuclei, 68.7% expressing, with mean CP10K 0.827. Thus the target transcript is present in the relevant recovered thalamic population, so a null prediction should not be based on lack of expression.
- The biology card identifies ACOX1 as a soluble peroxisomal matrix enzyme carrying the first/rate-limiting oxidation of straight-chain long and very-long-chain acyl-CoAs in peroxisomal beta-oxidation. A disruptive P16 edit should stop new enzyme production but leaves pre-existing enzyme initially active.
- The functional-stock adjudication concludes that ACOX1 capacity is likely substantially depleted by P37-P44 because 21-28 days exceeds the typical 3-13 day lifetime of most measured mouse-brain proteins; this is partial evidence because ACOX1-specific neuronal turnover was not measured.
- Stronger organism-level phenotypes are only weak timing guides for this endpoint: germline mouse loss is dominated by postnatal liver pathology, and biallelic human ACOX1 deficiency is developmental/childhood neurological disease rather than sparse postnatal mouse thalamic deletion over 3-4 weeks.
- Related Acox2/Acox3 oxidases have partially overlapping substrates but were not measured as thalamic compensators, so they add uncertainty rather than a quantitative reason to expect a large or small count.

## Training perturbations used

The closest measured pathway context in the declared training table was peroxisome import, peroxisomal lipid transport, peroxisomal beta-oxidation, ether-lipid/peroxisome-linked lipid biology, and basal lipid nuclear-receptor or sterol-control factors. Re-reading those targets in the expression Parquet for `151 TH Prkcd Grin2c Glut` gave the exact `FDR < 0.05` focal counts:

| target | focal `n_degs` at 0.05 | interpretation |
| --- | ---: | --- |
| `Abcd3` | 0 | peroxisomal ABC transporter; no focal downstream or self DEG |
| `Acbd5` | 0 | peroxisome-ER/VLCFA-linked node; no focal downstream or self DEG |
| `Hsd17b4` | 0 | peroxisomal beta-oxidation enzyme; no focal downstream or self DEG |
| `Pex1` | 0 | peroxisome import/biogenesis; no focal DEGs at 0.05 |
| `Pex14` | 1 | self-transcript only in the focal 0.05 count; 0 downstream focal genes |
| `Agps` | 1 | one focal downstream hit at 0.05, `Dhcr24`; two more sterol-like genes appear only at 0.10 |
| `Far1` | 2 | one self hit plus one focal downstream hit, `Tial1` |
| `Mff` | 0 | organelle/fission comparator; no focal downstream or self DEG |
| `Ppara`, `Ppard`, `Pparg`, `Ppargc1a`, `Rxra`, `Rxrb`, `Rxrg` | 0 each | basal PPAR/RXR/PGC lipid-control perturbations were flat in the focal class |
| `Srebf2` | 7 | positive lipid-transcription contrast: six downstream cholesterol-biosynthesis genes plus self, showing that sterol RNA modules are detectable when engaged |

The packaged same-experiment Findings agree with the direct Parquet check, but are not independent replication. They summarize `Abcd3`, `Acbd5`, `Hsd17b4`, `Pex1`, and `Pex14` as flat or nearly flat across postmitotic neuronal groups, with a released Claim stating that represented peroxisome-linked lipid, transporter, import, beta-oxidation, ether-lipid, and maintenance perturbations are predominantly flat, sparse, or target-specific rather than converging on a shared acute neuronal transcriptomic module.

## Synthesis

Two signals point upward from the baseline: `Acox1` is readily expressed in the assayed thalamic class, and the pre-existing soluble enzyme pool should usually decay across 21-28 days. Those signals make a real biochemical lesion plausible.

The stronger endpoint-specific signal points downward. In this same Perturb-seq readout, perturbing represented peroxisomal transporter/import/beta-oxidation neighbors rarely converted a lipid-organelle lesion into a nuclear RNA signature by P37-P44. The flatness is not a generic inability to detect lipid transcription: `Srebf2` produced a small but coherent cholesterol-biosynthesis signature in the same class. It is therefore more consistent to treat acute Acox1 loss as another peroxisomal metabolic perturbation whose primary consequences are buffered, biochemical, outside NeuN-positive neurons, or below this snRNA-seq FDR threshold.

The `n_degs` field includes the self-target transcript when significant. In the focal class only 319/1,642 training targets with a measured self row had self `pvals_adj < 0.05`, and many close peroxisome/lipid comparators had no self hit despite negative self log-fold changes. Because the dataset-wide self-transcript change is not a reliable editing-strength proxy and because ACOX1 functional loss need not produce a strong Acox1 nuclear-RNA drop, I did not reserve a singleton self DEG.

**Predicted `n_degs`: 0**
